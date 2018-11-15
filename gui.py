import appJar
import os
import bluestring_builder

blueprint_app = appJar.gui()

selected_image = ""

# dialog for selecting image to work with
def openFileFunction(button):
    selected_image = blueprint_app.openBox(title="Select image", dirName="img", fileTypes=[("images", "*.png"), ("images", "*.jpg")])
    blueprint_app.setLabel("filename", selected_image)
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
blueprint_app.setPadding([10, 10])
blueprint_app.addButtons(["Start"], None, 10, 0)
blueprint_app.addButtons(["to Clipboard"], None, 10, 1)
blueprint_app.addButtons(["DEBUG"], debugging)

# startup logic
#blueprint_app.setStartFunction(fillListBox)

blueprint_app.go()
