from PIL import Image, ImageEnhance, ImageFilter, ImageDraw, ImageFont
import os

path = './unedited_images'
pathOut = './edited_images'


for filename in os.listdir(path):
    img = Image.open(f"{path}/{filename}")
    edit = img.filter(ImageFilter.SHARPEN).convert('RGB')
    enhancer = ImageEnhance.Brightness(edit)
    edit = enhancer.enhance(1.2)
    font = ImageFont.truetype("/Library/Fonts/Arial.ttf", 70)
    draw = ImageDraw.Draw(edit)
    draw.text((10, 10), "Isha", font=font, fill="red")
    

    clean_name = os.path.splitext(filename)[0]
    edit.save(f'{pathOut}/{clean_name}_edited.jpg')


