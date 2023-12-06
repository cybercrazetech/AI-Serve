from PIL import Image
import os
'''
image = Image.open("emotions/normal.png")
width, height = image.size
print(width, height)
'''

images = [file for file in os.listdir() if file.endswith(('jpeg', 'png', 'jpg'))]
for image in images:
    img = Image.open(image)
    img.thumbnail((200,200))
    img.save(image, optimize=True, quality=40)
