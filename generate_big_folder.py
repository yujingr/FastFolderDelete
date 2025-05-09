import os
from concurrent.futures import ThreadPoolExecutor

base = 'test_big_folder'
if not os.path.exists(base):
    os.makedirs(base)


def create_files_in_subfolder(i):
    subfolder = os.path.join(base, f'folder_{i}')
    os.makedirs(subfolder, exist_ok=True)
    for j in range(30):
        with open(os.path.join(subfolder, f'file_{i}_{j}.txt'), 'w') as f:
            f.write('hello world')


with ThreadPoolExecutor(max_workers=64) as executor:
    executor.map(create_files_in_subfolder, range(1, 1000))

print('Generated test_big_folder with 1000 subfolders and files.')
