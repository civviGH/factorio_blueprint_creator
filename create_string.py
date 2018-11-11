from bluestring_builder import *
import pickle
from PIL import Image

# import shortest range dict
print("Loading dictionary with shortest color ranges...")
with open("color_coding_ranges.txt","rb") as f:
    shortest_range = pickle.load(f)
print("done")

# resize image to wanted size
print("Loading image and resizing it...")
wanted_size = 100
img = Image.open("pikachu.png")
wpercent = (wanted_size/float(img.size[0]))
hsize = int((float(img.size[1])*float(wpercent)))
img_sized = img.resize((wanted_size,hsize), Image.ANTIALIAS)
img_pixels = img_sized.load()
print("done")

# iterate over pixels from image, add entity of right color
print("Creating blueprint from image data...")
bp = Blueprint()
image_width = img_sized.size[0]
for x in range(img_sized.size[0]):
    print("{}%".format((float(x+1)/image_width) * 100.0))
    for y in range(img_sized.size[1]):
        pixel_color = img_pixels[x, y][0:3]
        if pixel_color == (0,0,0):
            continue
        rtn_code = bp.addEntity(shortest_range[pixel_color], (x,y), "tile")
        if rtn_code != 0:
            print(rtn_code)
print("done. Here is your blueprint string:")
finished_blueprint = bp.getBlueprintString()
print(finished_blueprint)
with open("blueprint" , "w") as f:
    f.write(finished_blueprint)
