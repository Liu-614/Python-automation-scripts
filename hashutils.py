import hashlib

def compute_file_hash(file_path, algorithm='md5'):
    """计算文件的哈希值，支持 md5/sha1/sha256"""
    hash_func = getattr(hashlib, algorithm)()
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            hash_func.update(chunk)
    return hash_func.hexdigest()
