"""
Adapted from https://github.com/stevenquinn/CityGen
"""


import maya.cmds as cmds
import random
from functools import partial
import math

def main():
    createUI()

class createUI(object):

    windowName="City Builder - Tim Kelly 2018"

    def show(self):

        if cmds.window(self.windowName, query=True, exists=True):
            cmds.deleteUI(self.windowName)

        window = cmds.window(self.windowName)

        self.buildUI()
        cmds.showWindow(window)

    def buildUI(self):
        cmds.columnLayout( columnAttach=('both', 5), rowSpacing=10, columnWidth=250)
        cmds.button(label = "Generate", command = partial(cityBuild))

class city(object):
    def __init__(self,sizeX,sizeY,startX=0,startY=0):
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.startX = startX
        self.startY = startY
        #urban sprawl attribute
    def create(self):
        toggleX = True
        toggleY = True
        #populate
        for y in range(self.sizeY):
            if not toggleY:
                toggleY=True
            else:
                for x in range(self.sizeX):
                    if not toggleX:
                        toggleX=True
                    else:
                        myBuilding = Building(1,1,1)
                        myBuilding.create()
                        myBuilding.moveBuilding(self.startX+(x+0.5),0.5,self.startY+(y+0.5))
                        myBuilding.changecolour()
                        toggleX = False
                        toggleY = False


def cityBuild(*args):
    #make plane, change shape here
    citySize = 100
    cmds.polyPlane(w=citySize,h=citySize,n="ground")
    cmds.setAttr("lambert1.color", 0.0267, 0.0267, 0.0267,type="double3")
    cmds.move(citySize / 2, 0, citySize / 2)

    #make groups
    cmds.group( em = True, n = "gen_buildings")
    city(10,10).create()
    freeway().create()

def riverBuild():
    pass

class freeway(object):
    def __init__(rotation):
        self.rotate = rotation
    def create(self):
        cmds.polyCube(0.5,1,1)


class Building(object):
    mesh=None
    buildingCount = 0
    def __init__(self,inWidth=0,inHeight=0,inDepth=0):
        self.width = inWidth
        self.height = random.randint(3,7) * 2
        self.depth = inDepth
        Building.buildingCount +=1
        self.buildingName = "Building_" + str(self.buildingCount)


    def create(self):
        self.mesh = cmds.polyCube(h=self.height)
        print str(self.buildingName)


    def moveBuilding(self,moveX=0,moveY=0,moveZ=0):
        cmds.select(self.mesh)
        cmds.move(moveX,self.height/2,moveZ)
        cmds.select( cl=True)

    def changecolour(self):
        if not cmds.objExists('BuildingShader'):
            print "Made surface"
            cmds.shadingNode('lambert', asShader=True,n="BuildingShader")

        cmds.select(self.mesh)
        cmds.hyperShade(a='BuildingShader')
        cmds.setAttr("BuildingShader.color", 0.204545, 0.204545, 0.204545,type="double3")

    def addExtras(self):
        pass
