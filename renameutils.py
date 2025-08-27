import os
import re

def batch_rename(dir_path, pattern=None, replacement=None, prefix=None, start=1):
    """批量重命名文件"""
    files = os.listdir(dir_path)
    index = start
    for filename in files:
        old_path = os.path.join(dir_path, filename)
        if not os.path.isfile(old_path):
            continue

        name, ext = os.path.splitext(filename)
        if pattern:
            name = re.sub(pattern, replacement, name)
        if prefix:
            name = f"{prefix}{index}"
            index += 1

        new_name = f"{name}{ext}"
        new_path = os.path.join(dir_path, new_name)
        os.rename(old_path, new_path)
        print(f"🔁 重命名: {filename} → {new_name}")
