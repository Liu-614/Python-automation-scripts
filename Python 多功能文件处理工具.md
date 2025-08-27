# Python 多功能文件处理工具
本脚本是一个功能强大的命令行工具，支持以下功能：
- 批量重命名文件（支持正则表达式替换、序号追加等）
- 图片格式批量转换（如 PNG → JPG，支持质量压缩）
- 文件哈希值计算（支持 MD5、SHA1、SHA256）
- 多线程处理，提升大文件处理效率
## 文件结构
```
file-processor/
├── file_processor.py     # 主程序入口
├── utils/
│   ├── hash_utils.py     # 哈希计算工具
│   ├── image_utils.py    # 图片处理工具
│   └── rename_utils.py   # 文件重命名工具
└── README.md             # 说明文档
```
---
## 代码实现
### `file_processor.py`
```python
import os
import argparse
from concurrent.futures import ThreadPoolExecutor
from utils.hash_utils import compute_file_hash
from utils.image_utils import convert_image
from utils.rename_utils import batch_rename_files
def main():
    parser = argparse.ArgumentParser(description="多功能文件处理工具")
    subparsers = parser.add_subparsers(dest='command', required=True)
    # 重命名子命令
    rename_parser = subparsers.add_parser('rename', help='批量重命名文件')
    rename_parser.add_argument('--path', required=True, help='目标文件夹路径')
    rename_parser.add_argument('--pattern', help='正则表达式匹配模式')
    rename_parser.add_argument('--replacement', help='替换内容')
    rename_parser.add_argument('--prefix', help='文件名前缀')
    rename_parser.add_argument('--start', type=int, default=1, help='起始序号')
    # 图片转换子命令
    convert_parser = subparsers.add_parser('convert', help='图片格式转换')
    convert_parser.add_argument('--path', required=True, help='目标文件夹路径')
    convert_parser.add_argument('--from_ext', required=True, help='原扩展名，如 png')
    convert_parser.add_argument('--to_ext', required=True, help='目标扩展名，如 jpg')
    convert_parser.add_argument('--quality', type=int, default=85, help='压缩质量（仅对 jpg 有效）')
    # 哈希计算子命令
    hash_parser = subparsers.add_parser('hash', help='计算文件哈希值')
    hash_parser.add_argument('--path', required=True, help='目标文件或文件夹路径')
    hash_parser.add_argument('--algo', default='md5', choices=['md5', 'sha1', 'sha256'], help='哈希算法')
    args = parser.parse_args()
    if args.command == 'rename':
        batch_rename_files(args.path, args.pattern, args.replacement, args.prefix, args.start)
    elif args.command == 'convert':
        with ThreadPoolExecutor() as executor:
            for filename in os.listdir(args.path):
                if filename.endswith(f'.{args.from_ext}'):
                    executor.submit(convert_image, os.path.join(args.path, filename), args.to_ext, args.quality)
    elif args.command == 'hash':
        if os.path.isfile(args.path):
            print(f"{args.algo.upper()}: {compute_file_hash(args.path, args.algo)}")
        elif os.path.isdir(args.path):
            for filename in os.listdir(args.path):
                filepath = os.path.join(args.path, filename)
                if os.path.isfile(filepath):
                    print(f"{filename}: {compute_file_hash(filepath, args.algo)}")
if __name__ == '__main__':
    main()
```
---
### `utils/hash_utils.py`
```python
import hashlib
def compute_file_hash(filepath, algorithm='md5'):
    hash_func = hashlib.new(algorithm)
    with open(filepath, 'rb') as f:
        while chunk := f.read(8192):
            hash_func.update(chunk)
    return hash_func.hexdigest()
```
---
### `utils/image_utils.py`
```python
from PIL import Image
def convert_image(image_path, target_format='jpg', quality=85):
    try:
        img = Image.open(image_path)
        rgb_img = img.convert('RGB')
        new_path = image_path.rsplit('.', 1)[0] + f'.{target_format}'
        rgb_img.save(new_path, format=target_format, quality=quality)
        print(f"Converted: {image_path} → {new_path}")
    except Exception as e:
        print(f"Failed to convert {image_path}: {e}")
```
---
### `utils/rename_utils.py`
```python
import os
import re
def batch_rename_files(dir_path, pattern=None, replacement=None, prefix=None, start=1):
    files = sorted(os.listdir(dir_path))
    for filename in files:
        old_path = os.path.join(dir_path, filename)
        if not os.path.isfile(old_path):
            continue
        name, ext = os.path.splitext(filename)
        if pattern:
            name = re.sub(pattern, replacement, name)
        if prefix:
            name = f"{prefix}_{start}"
            start += 1
        new_name = f"{name}{ext}"
        new_path = os.path.join(dir_path, new_name)
        os.rename(old_path, new_path)
        print(f"Renamed: {filename} → {new_name}")
```
---
## 使用示例
### 1. 批量重命名文件
```bash
python file_processor.py rename --path ./images --pattern "(.+)" --replacement "photo_\1" --prefix "IMG"
```
### 2. 图片格式转换
```bash
python file_processor.py convert --path ./images --from_ext png --to_ext jpg --quality 90
```
### 3. 计算文件哈希
```bash
python file_processor.py hash --path ./images/sample.jpg --algo sha256
```
---
## 技术实现
- 使用 `argparse` 构建命令行界面
- 使用 `concurrent.futures.ThreadPoolExecutor` 实现多线程任务
- 使用 `Pillow` 库进行图片处理
- 使用 `hashlib` 进行文件哈希计算
- 模块化设计，便于扩展与维护
---
## 注意事项
- 图片转换仅支持常见格式（如 PNG、JPG、WEBP）
- 哈希计算适合用于文件校验或去重
- 重命名操作不可逆，建议先备份
- 多线程处理时注意资源占用情况

