# FastFolderDelete

A super-fast Windows folder deletion tool with a drag-and-drop GUI, leveraging parallel file operations for maximum speed. Ideal for deleting large folders with thousands of files and subfolders.

## Features

- **Drag and drop** folders to delete them instantly
- **Parallel deletion** using multiple worker threads (configurable)
- **Simple GUI** built with Tkinter and tkinterdnd2
- **Test folder generator** for benchmarking

## Requirements

- Python 3.7+
- Windows OS (uses Windows-specific commands and paths)
- [tkinterdnd2](https://pypi.org/project/tkinterdnd2/)

## Installation

1. Clone this repository or download the files.
2. Install dependencies:
   ```bash
   pip install tkinterdnd2
   ```

## Usage

### Option 1: Use the Precompiled Windows Executable

A precompiled executable (`fast_folder_delete_gui.exe`) is available in the `output` folder. You do not need Python or any dependencies to use this version.

1. Open the `output` folder.
2. Double-click `fast_folder_delete_gui.exe` to launch the app.
3. Drag and drop a folder onto the window.
4. Confirm deletion when prompted.
5. Optionally, set the number of worker threads for parallel deletion (default: 64).

### Option 2: Run from Python Source

1. Run the GUI:
   ```bash
   python fast_folder_delete_gui.py
   ```
2. Drag and drop a folder onto the window.
3. Confirm deletion when prompted.
4. Optionally, set the number of worker threads for parallel deletion (default: 64).

### Generate a Large Test Folder

To create a large folder structure for testing:

```bash
python generate_big_folder.py
```

This will create a folder named `test_big_folder` with 1000 subfolders, each containing 30 files.

## Notes

- **Warning:** This tool permanently deletes folders and their contents. Use with caution!
- The deletion process is optimized for NTFS file systems on Windows.
- If you encounter issues with drag-and-drop, ensure `tkinterdnd2` is installed and you are running on Windows.

## License

MIT License
