import os
import shutil
import subprocess
import tkinter as tk
from tkinter import messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
import threading
import concurrent.futures

# Function to delete folder using Windows rd command for speed


def parallel_delete_folder(folder_path, num_workers=64):
    """Recursively delete a folder and its contents in parallel."""
    errors = []

    def delete_file(path):
        try:
            os.remove(path)
        except FileNotFoundError:
            pass  # Already deleted, ignore
        except Exception as e:
            errors.append((path, str(e)))

    def delete_dir(path):
        try:
            os.rmdir(path)
        except FileNotFoundError:
            pass  # Already deleted, ignore
        except Exception as e:
            errors.append((path, str(e)))
    # Walk the tree, collect files and dirs
    files = []
    dirs = []
    for root, dirnames, filenames in os.walk(folder_path, topdown=False):
        for f in filenames:
            files.append(os.path.join(root, f))
        for d in dirnames:
            dirs.append(os.path.join(root, d))
    # Delete files in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
        list(executor.map(delete_file, files))
    # Delete directories in parallel (bottom-up)
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
        list(executor.map(delete_dir, dirs))
    # Finally, delete the root folder
    try:
        os.rmdir(folder_path)
    except Exception as e:
        errors.append((folder_path, str(e)))
    if errors:
        return False, f"Errors occurred: {errors}"
    return True, f"Deleted: {folder_path}"


def fast_delete_folder(folder_path, num_workers=64):
    try:
        return parallel_delete_folder(folder_path, num_workers=num_workers)
    except Exception as e:
        return False, str(e)

# GUI App


class FastFolderDeleteApp(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        self.title("Fast Folder Delete")
        self.geometry("400x250")
        self.configure(bg="#f8f8f8")

        self.label = tk.Label(self, text="Drag and drop a folder here to delete it SUPER FAST!",
                              bg="#f8f8f8", fg="#333", font=("Segoe UI", 12))
        self.label.pack(pady=20)

        # Add entry for number of workers
        self.worker_frame = tk.Frame(self, bg="#f8f8f8")
        self.worker_frame.pack(pady=5)
        self.worker_label = tk.Label(
            self.worker_frame, text="Number of workers:", bg="#f8f8f8", fg="#333", font=("Segoe UI", 10))
        self.worker_label.pack(side=tk.LEFT)
        self.worker_var = tk.StringVar(value="64")
        self.worker_entry = tk.Entry(
            self.worker_frame, textvariable=self.worker_var, width=6)
        self.worker_entry.pack(side=tk.LEFT, padx=5)

        self.status = tk.Label(self, text="", bg="#f8f8f8",
                               fg="#007700", font=("Segoe UI", 10))
        self.status.pack(pady=10)

        self.drop_target_register(DND_FILES)
        self.dnd_bind('<<Drop>>', self.on_drop)

    def on_drop(self, event):
        folder_path = event.data.strip('{}')  # Remove curly braces if present
        if not os.path.isdir(folder_path):
            self.status.config(text="Not a valid folder!", fg="#bb0000")
            return
        confirm = messagebox.askyesno(
            "Confirm Delete", f"Are you sure you want to delete this folder?\n{folder_path}")
        if confirm:
            self.status.config(text="Deleting...", fg="#333333")
            try:
                num_workers = int(self.worker_var.get())
                if num_workers < 1:
                    raise ValueError
            except ValueError:
                self.status.config(
                    text="Invalid number of workers!", fg="#bb0000")
                return
            threading.Thread(target=self.delete_folder_thread,
                             args=(folder_path, num_workers), daemon=True).start()
        else:
            self.status.config(text="Deletion cancelled.", fg="#333333")

    def delete_folder_thread(self, folder_path, num_workers):
        success, msg = fast_delete_folder(folder_path, num_workers=num_workers)
        self.after(0, self.update_status, success, msg)

    def update_status(self, success, msg):
        self.status.config(text=msg, fg="#007700" if success else "#bb0000")


if __name__ == "__main__":
    try:
        from tkinterdnd2 import TkinterDnD
    except ImportError:
        import sys
        print("You need to install tkinterdnd2: pip install tkinterdnd2")
        sys.exit(1)
    app = FastFolderDeleteApp()
    app.mainloop()
