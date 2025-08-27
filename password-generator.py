import random
import string


def generate_password(length=12):
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(chars) for _ in range(length))


if __name__ == "__main__":
    print("生成的密码：", generate_password())
