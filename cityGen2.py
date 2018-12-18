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
    def __init__(self,sizeX,sizeY,startX=0,startY=0,highway=True,density = 3,square=2):
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.startX = startX
        self.startY = startY
        self.highway = highway
        self.density = density
        self.sqaure=square
        #urban sprawl attribute/
    def create(self):
        if self.highway == True:
            self.startY += -1
            self.startX += -1
        toggleX = 0
        toggleY = 0
        #populate
        for y in range(self.sizeY):
            print y
            if toggleY == self.sqaure:
                toggleY =0
            else:
                toggleX = 0
                toggleY += 1
                for x in range(self.sizeX):
                    if toggleX == self.sqaure:
                        toggleX =0
                    else:
                        myBuilding = Building(self.density)
                        myBuilding.create()
                        myBuilding.moveBuilding(self.startX+(x+0.5),0.5,self.startY+(y+0.5))
                        myBuilding.changecolour()
                        toggleX += 1


        if self.highway==True:
            for x in range(self.sizeX):
                freeway(90).create((self.sizeX-x)+self.startX,(self.sizeY)+self.startY)
                freeway(90).create((self.sizeX-x)+self.startX,self.startY)
            for y in range(self.sizeY+1):
                freeway(0).create((self.sizeX+1)+self.startX,(self.sizeY-y)+self.startY)
                freeway(0).create(self.startX,(self.sizeY-y)+self.startY)
            freeway(45).create(self.sizeX+self.startX+1,self.sizeY+self.startY+1)
            freeway(45).create(self.startX,self.sizeY+self.startY+1)
            freeway(45).create(self.sizeX+self.startX+1,self.startY)
            freeway(45).create(self.startX,self.startY)

def cityBuild(*args):
    #make plane, change shape here
    citySize = 100
    ground = cmds.polyPlane(w=citySize,h=citySize,n="ground")
    cmds.setAttr("lambert1.color", 0.0267, 0.0267, 0.0267,type="double3")
    cmds.move(citySize / 2, 0, citySize / 2)

    #make groups
    cmds.group( em = True, n = "gen_Buildings")
    cmds.group( em = True, n = "gen_Highways")
    cmds.group( em = True, n = "gen_Water")

    city(20,20,42,41,True,2).create()
    city(20,20,62,40,False,1).create()
    #for x in range(3):
    #    city(10,10,10 * x,0,True,8).create()
    #for x in range(3):
    #    city(10,10,10 * x,10,True,4).create()
    for x in range(30,40):
        for y in range (1,101):
            water(x,y).create()
    for y in range(0,10):
        print y
        cmds.select('ground.f['+str((y*9) + 3)+']' , r=True)
        cmds.delete()


class water(object):
    def __init__(self,placeX=0,placeY=0):
        self.placeX = placeX
        self.placeY = placeY
    def create(self):
        self.mesh = cmds.polyPlane(w=1,h=1,sx=1,sy=1,n="Water")
        cmds.move(self.placeX+0.5,0,self.placeY+0.5)
        if not cmds.objExists('waterShader'):
            cmds.shadingNode('blinn', asShader=True,n="waterShader")
        cmds.select(self.mesh)
        cmds.hyperShade(a='waterShader')
        cmds.setAttr("waterShader.color", 0.084168, 0.277934, 0.504,type="double3")
        cmds.setAttr("waterShader.transparency", 0.258741, 0.258741, 0.258741,type="double3")
        cmds.parent( self.mesh, 'gen_Water' )

class freeway(object):
    freewayCount = 0
    def __init__(self,rotation):

        self.rotate = rotation
        mesh = None
        freeway.freewayCount += 1
        self.freewayName = "Freeway_" + str(self.freewayCount)
    def create(self,placeX=0,placeY=0):
        self.mesh = cmds.polyCube(w=1,h=1,d=1,name=self.freewayName)
        cmds.polyMoveVertex("Freeway_" + str(self.freewayCount)+".vtx[0:1]", tz =-0.25)
        cmds.polyMoveVertex("Freeway_" + str(self.freewayCount)+".vtx[6:7]", tz =0.25)
        cmds.setAttr(("Freeway_" + str(self.freewayCount)+".ry"),self.rotate)
        cmds.setAttr(("Freeway_" + str(self.freewayCount)+".translateY"),0.5)
        cmds.setAttr(("Freeway_" + str(self.freewayCount)+".translateZ"),placeX-0.5)
        cmds.setAttr(("Freeway_" + str(self.freewayCount)+".translateX"),placeY-0.5)
        cmds.parent( self.mesh, 'gen_Highways' )

class Building(object):
    mesh=None
    buildingCount = 0
    def __init__(self,density):
        self.height = random.randint(3,7) * density
        print density
        Building.buildingCount +=1
        self.buildingName = "Building_" + str(self.buildingCount)


    def create(self):
        self.mesh = cmds.polyCube(h=self.height,sx=2)
        cmds.parent( self.mesh, 'gen_Buildings' )
        for x in range(1,3):
            pass

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

class park(object):
    pass

class bridge(object):
    mesh=None
    def __init__():
        self.rotation
    def create():
        self.mesh = cmds.polyCube(1,10,1)
