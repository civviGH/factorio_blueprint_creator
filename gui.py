import appJar
import os
from create_string import *

blueprint_app = appJar.gui()

selected_image = ""
is_running = False
blueprint_string = ""

# dialog for selecting image to work with
def openFileFunction(button):
    global selected_image
    selected_image = blueprint_app.openBox(title="Select image", dirName="img", fileTypes=[("images", "*.png"), ("images", "*.jpg")])
    blueprint_app.setLabel("filename", selected_image)
    selected_image = selected_image.split("/")[-1].split(".")[0]
    return 0

# put all .dict files in configs folder into to optionbox
def findAllConfigurations():
    options = []
    for filename in os.listdir("configs"):
        if filename.endswith(".dict"):
            options.append(filename.split(".")[0])
    return options

def debugging(button):
    print(blueprint_app.getEntry("Width of blueprint"))

def getAppjarColor(color):
    appjar_color = "#"
    for part in color.strip("()").split(","):
        hex_repr = hex(int(part))[2:]
        if len(hex_repr) == 1:
            hex_repr = "0" + hex_repr
        appjar_color = appjar_color + hex_repr
    return appjar_color

def fillTabs():
    tab_nr = 1
    for filename in os.listdir("configs"):
        if filename.endswith(".dict"):
            blueprint_app.startTab(filename.split(".")[0])
            with open("configs/" + filename, "r") as c:
                for line in c:
                    line_info = line.split(":")
                    entity_name = line_info[0].strip()
                    entity_color = line_info[1].strip()
                    appjar_color = getAppjarColor(entity_color)
                    blueprint_app.addLabel(entity_name + str(tab_nr), entity_name)
                    blueprint_app.setLabelBg(entity_name + str(tab_nr), appjar_color)
            tab_nr = tab_nr + 1
            blueprint_app.stopTab()

def startCreatingBlueprint():
    global is_running
    global selected_image
    global blueprint_string
    if is_running:
        return None
    # deactive button
    is_running = True
    # get active tab and load config
    config_name = blueprint_app.getTabbedFrameSelectedTab("colors")
    colors = getConfig(config_name)
    try:
        img_size = int(blueprint_app.getEntry("Width of blueprint"))
    except:
        img_size = 100
    img_resized = resizeImage(selected_image, img_size)
    img_width = img_resized.size[0]
    img_pixels = img_resized.load()
    bg_color = img_pixels[0, 0][0:3]
    matched_colors = {}
    check_for_bg_color = False

    bp = Blueprint()
    for x in range(img_width):
        blueprint_app.setMeter("progress", int((float(x+1)/img_width) * 100.0))
        #print("{}%".format((float(x+1)/img_width) * 100.0))
        for y in range(img_resized.size[1]):
            pixel_color = img_pixels[x, y][0:3]
            if (check_for_bg_color):
                if pixel_color == bg_color:
                    continue
            if pixel_color in matched_colors:
                rtn_code = bp.addEntity(matched_colors[pixel_color]["name"], (x,y), matched_colors[pixel_color]["type"])
            else:
                minimal_distance = 9999999
                nearest_color = ""
                for key,value in colors.items():
                    #distance = naiveColorDistance(key, pixel_color)
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
    blueprint_string = bp.getBlueprintString()

    is_running = False

def toClipboard():
    global blueprint_string
    w = Tk()
    w.withdraw()
    w.clipboard_clear()
    w.clipboard_append(blueprint_string)
    w.update()
    w.destroy()

def closeApp():
    global is_running
    if is_running:
        return
    blueprint_app.stop()

# basic startup
blueprint_app.setSize(800, 600)
blueprint_app.setTitle("Blueprint art creator")
blueprint_app.setResizable(canResize=False)
blueprint_app.setLocation("CENTER")

# regarding the grid
blueprint_app.setSticky("news")

# widgets
blueprint_app.addButtons(["Select image"], openFileFunction, 0, 0)
blueprint_app.addLabel("filename", "", 1, 0)
blueprint_app.addLabelNumericEntry("Width of blueprint", 2, 0)
blueprint_app.startTabbedFrame("colors", 0, 1, 1, 9)
fillTabs()
blueprint_app.stopTabbedFrame()
blueprint_app.addMeter("progress", 9, 0, 2)
blueprint_app.setMeterFill("progress", "green")
blueprint_app.setPadding([10, 10])
blueprint_app.addButtons(["Start"], startCreatingBlueprint, 10, 0)
blueprint_app.addButtons(["to Clipboard"], toClipboard, 10, 1)
blueprint_app.addButtons(["Close"], closeApp)

# startup logic
#blueprint_app.setStartFunction(fillListBox)

blueprint_app.go()
