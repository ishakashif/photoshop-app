from PIL import Image, ImageEnhance, ImageFilter
import os

path - './unedited_images'
pathOut = './edited_images'

for filename in os.listdir(path):
    