import os
import argparse
from concurrent.futures import ThreadPoolExecutor
from utils.hashutils import compute_file_hash
from utils.imageutils import convert_image
from utils.renameutils import batch_rename

def main():
    parser = argparse.ArgumentParser(description="多功能文件处理工具")
    subparsers = parser.add_subparsers(dest='command', required=True)

    # 重命名子命令
    rename_parser = subparsers.add_parser('rename', help='批量重命名文件')
    rename_parser.add_argument('--path', required=True, help='文件目录路径')
    rename_parser.add_argument('--pattern', help='正则表达式匹配模式')
    rename_parser.add_argument('--replacement', help='替换内容')
    rename_parser.add_argument('--prefix', help='文件名前缀')
    rename_parser.add_argument('--start', type=int, default=1, help='序号起始值')

    # 图片格式转换子命令
    convert_parser = subparsers.add_parser('convert', help='图片格式转换')
    convert_parser.add_argument('--path', required=True, help='文件目录路径')
    convert_parser.add_argument('--fromext', required=True, help='源扩展名（如 png）')
    convert_parser.add_argument('--toext', required=True, help='目标扩展名（如 jpg）')
    convert_parser.add_argument('--quality', type=int, default=85, help='压缩质量（1-100）')

    # 哈希计算子命令
    hash_parser = subparsers.add_parser('hash', help='计算文件哈希值')
    hash_parser.add_argument('--path', required=True, help='文件路径')
    hash_parser.add_argument('--algo', choices=['md5', 'sha1', 'sha256'], default='md5', help='哈希算法')

    args = parser.parse_args()

    if args.command == 'rename':
        batch_rename(args.path, args.pattern, args.replacement, args.prefix, args.start)
    elif args.command == 'convert':
        files = [f for f in os.listdir(args.path) if f.endswith(f'.{args.fromext}')]
        with ThreadPoolExecutor() as executor:
            for f in files:
                executor.submit(convert_image, os.path.join(args.path, f), args.toext, args.quality)
    elif args.command == 'hash':
        print(f"{args.algo.upper()}: {compute_file_hash(args.path, args.algo)}")

if __name__ == '__main__':
    main()
