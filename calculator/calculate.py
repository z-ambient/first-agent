
import os

def get_files_info(directory=None):
    if directory is None:
        directory = os.getcwd()
    
    files_info = {}
    with os.scandir(directory) as entries:
        for entry in entries:
            info = {
                'is_dir': entry.is_dir(),
                'size': entry.stat().st_size
            }
            files_info[entry.name] = info
    return files_info

def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

def add(a, b):
    return a + b
