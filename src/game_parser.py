#!/usr/bin/python3

import sys

sys.path.append("src/")
from util_classes import *


def clean_laser_string(laserString):
    keep = False
    retval = ""
    for char in laserString:
        if char == "<":
            keep = True
        if char == ">":
            keep = False
        if keep:
            retval += char

    return retval


def make_laser_pos_list(laserString):
    laserList = ["" for i in range(50)]
    listIdx = 0
    start = 2
    stop = 1
    for char in laserString[2:]:
        stop += 1
        if char == "|":
            laserList[listIdx] += laserString[start + 1 : stop]
            listIdx += 1
            start = stop
    print(laserList)



def set_laser(laser, laserString):
    pass


def parse_lasers(laserString, info):
    laserString = clean_laser_string(laserString)
    laserPosList = make_laser_pos_list(laserString)
    start = 1
    stop = 1

    #for laser, laserPos, in info.lasers, laserPosList:
    return info

def set_properties(info, attrName, attrVal):
    if attrName == "id":
        info.playerID = attrVal
    elif attrName == "x":
        info.x = float(attrVal)
    elif attrName == "y":
        info.y = float(attrVal)
        
    return info


def parse_attribute(info, attrString):
    startIdx = 0
    attrName = None
    attrVal = None

    for i in range(len(attrString)):
        if attrString[i] == "<":
            attrName = attrString[startIdx + 1 : i]
            startIdx = i
        if attrString[i] == ">":
            attrVal = attrString[startIdx + 1 : i]
        
        if attrName and attrVal:
            info = set_properties(info, attrName, attrVal)
            attrName = None
            attrVal = None

    return info


def divide_string(infoString):
    attributeCount = 0
    shipString = ""
    laserString = ""
    
    for i in range(len(infoString)):
        if infoString[i] == "$":
            attributeCount += 1

        if attributeCount <= 3:
            shipString += infoString[i]
        else:
            laserString += infoString[i]
#    print(shipString)
#    print(laserString)
    shipString += "$"
    laserString += "$"

    return shipString, laserString


def parse_info_string(infoString, info):
    if infoString == "stop":
        exit()
   
    shipString, laserString = divide_string(infoString)
    startAttribute = 0

    for i in range(1, len(shipString)):
        if shipString[i] == "$":
            info = parse_attribute(info, shipString[startAttribute : i])
            startAttribute = i

    info = parse_lasers(laserString, info)

    return info
