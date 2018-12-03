from bluestring_builder import *
import pickle
from PIL import Image, ImageFilter
import sys
from tkinter import Tk
import math
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000
import os.path

def getConfig(filename):
    colors = {}
    with open("configs/" + filename + ".dict", "r") as f:
        for line in f:
            foo = line.split(":")
            p0 = foo[0].strip()
            p1 = eval(foo[1].strip())
            p2 = foo[2].strip()
            toAdd = {}
            toAdd["name"] = p0
            toAdd["type"] = p2
            colors[p1] = toAdd
    return colors

def resizeImage(filename, wanted_size = 50):
    filepath = "img/" + filename
    if (os.path.isfile(filepath + ".jpg")):
        filepath = filepath + ".jpg"
    else:
        filepath = filepath + ".png"
    img = Image.open(filepath)
    wpercent = (wanted_size/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img_sized = img.resize((wanted_size,hsize), Image.LANCZOS)
    #
    img_sized = img_sized.filter(ImageFilter.MedianFilter)
    #
    #img_sized = img.resize((wanted_size,hsize), Image.ANTIALIAS)
    img_sized.save("img/glu_sized.png", quality=100)
    return(img_sized)

def colorDistance(c1, c2):
    co1 = list(c1)
    co2 = list(c2)
    for i in range(3):
        co1[i] = co1[i] / 255.0
        co2[i] = co2[i] / 255.0
    c1_rgb = sRGBColor(co1[0], co1[1], co1[2])
    c2_rgb = sRGBColor(co2[0], co2[1], co2[2])
    c1_lab = convert_color(c1_rgb, LabColor)
    c2_lab = convert_color(c2_rgb, LabColor)
    delta_e = delta_e_cie2000(c1_lab, c2_lab)
    return delta_e

def naiveColorDistance(c1, c2):
    distance = math.sqrt((c1[0]-c2[0])**2+(c1[1]-c2[1])**2+(c1[2]-c2[2])**2)
    return distance

def tintedColorDistance(c1, c2):
    co2 = list(c2)
    for i in range(3):
        co2[i] = (co2[i] + 255)/2
    co2 = tuple(c2)
    distance = math.sqrt((c1[0]-c2[0])**2+(c1[1]-c2[1])**2+(c1[2]-c2[2])**2)
    return distance

def foobar():
    config_name = sys.argv[1]
    image_name = sys.argv[2]
    if len(sys.argv) > 3:
        image_size = int(sys.argv[3])
    else:
        image_size = 50

    colors = getConfig(config_name)
    img_sized = resizeImage(image_name, image_size)
    img_width = img_sized.size[0]
    img_pixels = img_sized.load()

    # get background color from upper leftmost tile
    bg_color = img_pixels[0, 0][0:3]
    # emtpy dict with colors we can match
    matched_colors = {}

    print("Creating blueprint from image data...")
    bp = Blueprint()
    for x in range(img_width):
        print("{}%".format((float(x+1)/img_width) * 100.0))
        for y in range(img_sized.size[1]):
            pixel_color = img_pixels[x, y][0:3]
            if pixel_color == bg_color:
                continue
            if pixel_color in matched_colors:
                rtn_code = bp.addEntity(matched_colors[pixel_color]["name"], (x,y), matched_colors[pixel_color]["type"])
            else:
                minimal_distance = 9999999
                nearest_color = ""
                for key,value in colors.iteritems():
                    distance = colorDistance(key, pixel_color)
                    if distance < minimal_distance:
                        minimal_distance = distance
                        nearest_color = key
                matched_colors[nearest_color] = {}
                matched_colors[nearest_color]["name"] = colors[nearest_color]["name"]
                matched_colors[nearest_color]["type"] = colors[nearest_color]["type"]
                rtn_code = bp.addEntity(colors[nearest_color]["name"], (x,y), colors[nearest_color]["type"])
            if rtn_code != 0:
                print(rtn_code)
    print("done")
    finished_blueprint = bp.getBlueprintString()

    # get blueprint in clipboard
    w = Tk()
    w.withdraw()
    w.clipboard_clear()
    w.clipboard_append(finished_blueprint)
    w.update()
    w.destroy()

    with open("blueprint" , "w") as f:
        f.write(finished_blueprint)

if __name__ == "__main__":
    foobar()
