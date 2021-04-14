from PIL import Image
import os, sys

path = "../data/cleaned/images/"
out = "./resized/"
dirs = os.listdir(path)

def resize(width, height):
    i = 0
    for item in dirs:
        if os.path.isfile(path + item):
            try:
                im = Image.open(path + item)
                f, e = os.path.splitext(path + item)
                imResize = im.resize((width, height), Image.ANTIALIAS)
                imResize.save(out + item, 'JPEG', quality=90)
                i+=1
                print(i)
            except Exception as e:
                print(e)


resize(512, 512)
