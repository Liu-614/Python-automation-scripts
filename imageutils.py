from PIL import Image
import os

def convert_image(input_path, target_ext='jpg', quality=85):
    """转换图片格式并压缩质量"""
    try:
        img = Image.open(input_path)
        base = os.path.splitext(input_path)[0]
        output_path = f"{base}.{target_ext}"
        img.save(output_path, quality=quality)
        print(f"✅ 转换完成: {output_path}")
    except Exception as e:
        print(f"❌ 转换失败: {input_path} | 错误: {e}")
