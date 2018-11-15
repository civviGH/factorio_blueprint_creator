import json
import zlib
import base64
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000

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

class Blueprint:

    def __init__(self):
        self.__lowest_entity_id = 0
        self.__bluestring_json = {}
        self.__bluestring_json["blueprint"] = {}
        self.__bluestring_json["blueprint"]["item"] = "blueprint"
        self.__bluestring_json["blueprint"]["label"] = "test blueprint"
        self.__bluestring_json["blueprint"]["version"] = 68722819072
        self.__bluestring_json["blueprint"]["entities"] = []
        self.__bluestring_json["blueprint"]["tiles"] = []
        self.__bluestring_json["blueprint"]["icons"] = []
        iconsDict = {}
        iconsDict["index"] = 1
        signal = {}
        signal["type"] = "item"
        signal["name"] = "fast-transport-belt"
        iconsDict["signal"] = signal
        self.__bluestring_json["blueprint"]["icons"].append(iconsDict)
        self.__bluestring_json["blueprint"]["icons"].append


    def addEntity(self, objectName, position, eType):
        entityToAdd = {}
        entityToAdd["name"] = objectName
        entityToAdd["position"] = {}
        entityToAdd["position"]["x"] = position[0]
        entityToAdd["position"]["y"] = position[1]
        if eType == "entity":
            entityToAdd["entity_number"] = self.__lowest_entity_id
            self.__lowest_entity_id = self.__lowest_entity_id + 1
            entityToAdd["direction"] = 2
            self.__bluestring_json["blueprint"]["entities"].append(entityToAdd)
        elif eType == "tile":
            self.__bluestring_json["blueprint"]["tiles"].append(entityToAdd)
        else:
            return "uknown entity type for blueprint."
        return 0

    def getBlueprintString(self):
        stringedBlueprint = json.dumps(self.__bluestring_json)
        compressedBlueprint = zlib.compress(stringedBlueprint)
        encodedBlueprint = base64.b64encode(compressedBlueprint)
        encodedBlueprint = "0" + encodedBlueprint
        return encodedBlueprint

    def getJsonString(self):
        return json.dumps(self.__bluestring_json)
