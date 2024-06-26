# Function: Crop all image files in the directory input by the user, and perform cropping according to the set logic

from PIL import Image
import os


def crop_image(input_path):
    # 加载图像
    img = Image.open(input_path)

    # 原始和目标尺寸
    orig_width, orig_height = 2560, 1440
    target_width, target_height = 2462, 1385

    # 计算新图像的左上角坐标
    left = orig_width - target_width
    top = 0  # 从顶部开始

    # 定义裁剪框
    box = (left, top, left + target_width, top + target_height)

    # 裁剪图像
    cropped_img = img.crop(box)

    # 保存裁剪后的图像，覆盖原文件，保持原始格式和质量
    img_format = img.format if img.format else 'JPEG'  # 确保有一个默认格式
    cropped_img.save(input_path, format=img_format, quality=100)


def process_directory(directory):
    # 初始化计数器
    total_files = 0
    processed_files = 0

    # 先统计所有合适的文件数量
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                total_files += 1

    # 遍历目录中的所有文件和文件夹
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                # 直接覆盖原图片
                crop_image(file_path)
                processed_files += 1
                update_progress(processed_files / total_files)  # 更新进度
                print(f"Processed {file_path}")


def update_progress(progress):
    bar_length = 50  # 进度条长度
    block = int(round(bar_length * progress))
    text = "\r进度: [{0}] {1:.2f}%".format("#" * block + "-" * (bar_length - block), progress * 100)
    print(text, end="")


# 示例用法（包含进度）
def main():
    directory = input("请输入要处理的文件夹路径: ")
    process_directory(directory)
    update_progress(1)  # 100% 进度


# 调用 main 函数以运行程序
main()
