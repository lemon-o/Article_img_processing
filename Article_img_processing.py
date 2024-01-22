import os
from PIL import Image, ImageFilter, ImageEnhance

def process_all_images_in_folder(input_folder, output_folder):
    # 获取脚本所在的文件夹路径
    input_folder = os.path.dirname(os.path.realpath(__file__))
    # 遍历目录中的所有文件
    for filename in os.listdir(input_folder):
        file_path = os.path.join(input_folder, filename)
        # 筛选出图片文件（假定为常见的图片格式，可根据实际情况扩展）
        if os.path.isfile(file_path) and filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            process_image(file_path, output_folder)

def process_image(input_path, output_folder):
    # 打开图片
    img = Image.open(input_path)
    # 将图片宽度改为820，高度随比例改变
    target_width = 820
    w_percent = target_width / float(img.size[0])
    target_height = int(float(img.size[1]) * float(w_percent))
    img = img.resize((target_width, target_height), Image.LANCZOS)  # 或者使用 Image.BICUBIC
    # 将画布大小改为：宽度=图片宽度+192 高度=图片高度+150
    canvas_width = target_width + 192
    canvas_height = target_height + 150
    canvas = Image.new('RGBA', (canvas_width, canvas_height), (0, 0, 0, 0))
    # 计算图片在画布中的位置
    img_position = ((canvas_width - target_width) // 2, (canvas_height - target_height) // 2)
    # 移动img，相对于img2，x和y分别增加5
    img_new_position = (img_position[0] + 5, img_position[1] + 5)
    # 创建一张与原图相同的图片，作为img2
    img2 = img.copy()
    # 创建一个带有透明度通道的版本
    img_with_alpha = img.convert("RGBA")
    # 设置透明度（这里设置为半透明，你可以根据需要调整）
    alpha = 80  # 0 表示完全透明，255 表示完全不透明
    img_with_alpha.putalpha(alpha)
    # 将图像的亮度调整为最低
    enhancer = ImageEnhance.Brightness(img_with_alpha)
    dark_img = enhancer.enhance(0.0)  # 0.0 表示最低亮度
    # 将图片合成到画布中间位置
    canvas.paste(dark_img, img_new_position)
    # 添加高斯模糊效果
    canvas = canvas.filter(ImageFilter.GaussianBlur(radius=10))
    canvas.paste(img2, img_position)  
    # 确保 output 文件夹存在，如果不存在则创建
    output_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), "output")
    os.makedirs(output_folder, exist_ok=True) 
    # 将图片存储为 png 格式，保存到 output 文件夹中
    output_path = os.path.join(output_folder, f"output_{os.path.splitext(os.path.basename(input_path))[0]}.png")
    canvas.save(output_path, format='PNG')
    print(f"处理完成：{os.path.basename(output_path)}")

if __name__ == "__main__":
    # 处理当前脚本所在目录中的所有图片文件，保存到 output 文件夹中
    process_all_images_in_folder(os.path.dirname(os.path.realpath(__file__)), "output")
