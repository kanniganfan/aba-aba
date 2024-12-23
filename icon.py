from PIL import Image, ImageDraw, ImageFont
import os

def create_icon():
    # 创建一个 256x256 的图像，带透明背景
    img = Image.new('RGBA', (256, 256), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 绘制圆形背景
    draw.ellipse([20, 20, 236, 236], fill='#4CAF50')
    
    # 添加文字
    try:
        font = ImageFont.truetype("simhei.ttf", 120)  # 使用系统字体
    except:
        font = ImageFont.load_default()
    
    # 绘制"阿"字
    draw.text((70, 70), "阿", font=font, fill='white')
    
    # 保存为 ICO 文件
    img.save('icon.ico', format='ICO', sizes=[(256, 256)])

if __name__ == '__main__':
    create_icon()
