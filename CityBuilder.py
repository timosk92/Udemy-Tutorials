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
        self.square=square
        #urban sprawl attribute/
    def create(self):
        if self.highway == True:
            self.startY += -1
            self.startX += -1
        toggleX = 0
        toggleY = 0
        #populate
        for x in range(self.sizeX):
            if toggleY == self.square:
                toggleY =0
            else:
                toggleX = 0
                toggleY += 1
                for y in range(self.sizeY):
                    if toggleX == self.square:
                        toggleX =0
                    else:
                        myBuilding = Building(self.density)
                        myBuilding.create()
                        myBuilding.moveBuilding(self.startX+x+0.5,0.5,self.startY+y+1.5)
                        myBuilding.changecolour()
                        toggleX += 1


        if self.highway==True:
            for x in range(self.sizeX):
                #West
                freeway(0).create((self.sizeX-x)+self.startX,(self.sizeY)+self.startY+2)
                freeway(0).create((self.sizeX-x)+self.startX,self.startY+1)
            for y in range(self.sizeY):
                freeway(90).create((self.sizeX)+self.startX+1,(self.sizeY-y)+self.startY+1)
                freeway(90).create(self.startX,(self.sizeY-y)+self.startY+1)
            freeway(45).create(self.sizeX+self.startX+1,self.sizeY+self.startY+2)
            freeway(45).create(self.startX,self.sizeY+self.startY+2)
            freeway(45).create(self.sizeX+self.startX+1,self.startY+1)
            freeway(45).create(self.startX,self.startY+1)


def cityBuild(*args):
    #make plane, change shape here
    citySize = 100
    ground = cmds.polyPlane(w=citySize,h=citySize,n="ground")
    cmds.setAttr("lambert1.color", 0.0067, 0.0067, 0.0067,type="double3")
    cmds.move(citySize / 2, 0, citySize / 2)

    #make groups
    cmds.group( em = True, n = "gen_Buildings")
    cmds.group( em = True, n = "gen_Highways")
    cmds.group( em = True, n = "gen_Water")

    city(20, 20, 42, 41, True, 2, 2).create()
    city(20, 20, 72, 41, True, 1, 3).create()
    city(20, 20, 50, 20, True, 4, 2).create()
    #for x in range(3):
    #    city(10,10,10 * x,0,True,8).create()
    #for x in range(3):
    #    city(10,10,10 * x,10,True,4).create()
    for x in range(30,40):
        for y in range (0,100):
            water(x,y).create()
    for y in range(0,10):
        cmds.select('ground.f['+str((y*9) + 3)+']' , r=True)
        cmds.delete()
    tiles = []
    for x in range(1,water.waterCount+1):
        tiles.append("Water"+str(x))
    cmds.polyUnite(*tiles, n='result')
    cmds.delete("result", constructionHistory=True)
    bridge(0).create(35, 4, 1.4)
    park().create()
    park().movePark(71, 20)


class water(object):
    waterCount = 0
    def __init__(self,placeX=0,placeY=0):
        water.waterCount +=1
        self.waterName = "Water" + str(self.waterCount)
        self.placeX = placeX
        self.placeY = placeY
    def create(self):
        self.mesh = cmds.polyPlane(w=1,h=1,sx=1,sy=1,n="Water"+str(water.waterCount))
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
        self.mesh = cmds.polyCube(w=1,h=1, d=1, name=self.freewayName, sx=3)
        cmds.polyMoveVertex("Freeway_" + str(self.freewayCount) + ".vtx[0:3]", tz=-0.25)
        cmds.polyMoveVertex("Freeway_" + str(self.freewayCount) + ".vtx[12:15]", tz=0.25)
        cmds.polyMoveVertex("Freeway_" + str(self.freewayCount) + ".vtx[0:3]", ty=0.5)
        cmds.polyMoveVertex("Freeway_" + str(self.freewayCount) + ".vtx[12:15]", ty=0.5)
        cmds.polyExtrudeFacet("Freeway_" + str(self.freewayCount) + ".f[9]")
        cmds.polyExtrudeFacet("Freeway_" + str(self.freewayCount) + ".f[11]")
        cmds.polyMoveVertex("Freeway_" + str(self.freewayCount) + ".vtx[0:3]", ty=0.25)
        cmds.polyMoveVertex("Freeway_" + str(self.freewayCount) + ".vtx[12:15]", ty=0.25)
        cmds.polyMoveVertex("Freeway_" + str(self.freewayCount), ty=0.25)
        cmds.polyMoveVertex("Freeway_" + str(self.freewayCount) + ".vtx[16:23]", ty=-0.25)
        cmds.setAttr(("Freeway_" + str(self.freewayCount)+".ry"),self.rotate)
        cmds.setAttr(("Freeway_" + str(self.freewayCount)+".translateZ"),placeY-0.5)
        cmds.setAttr(("Freeway_" + str(self.freewayCount)+".translateX"),placeX-0.5)
        cmds.parent( self.mesh, 'gen_Highways' )


class Building(object):
    mesh = None
    buildingCount = 0

    def __init__(self,density):
        self.height = random.randint(3,7) * density
        Building.buildingCount +=1
        self.buildingName = "Building_" + str(self.buildingCount)


    def create(self):
        self.mesh = cmds.polyCube(h=self.height,sy=2)
        cmds.parent( self.mesh, 'gen_Buildings' )
        for x in range(1,3):
            pass

    def moveBuilding(self,moveX=0,moveY=0,moveZ=0):
        cmds.select(self.mesh)
        cmds.move(moveX,self.height/2,moveZ)
        cmds.select(cl=True)

    def changecolour(self):
        if not cmds.objExists('BuildingShader'):
            cmds.shadingNode('lambert', asShader=True,n="BuildingShader")

        cmds.select(self.mesh)
        cmds.hyperShade(a='BuildingShader')
        cmds.setAttr("BuildingShader.color", 0.204545, 0.204545, 0.204545,type="double3")

    def addExtras(self):
        pass


class park(object):
    mesh = None

    def __init__(self):
        pass

    def create(self):
        self.mesh = cmds.polyCube(d=5, w=5, h=1, n="Park")

    def movePark(self, placeX=0, placeY=0):
        cmds.select(self.mesh)
        cmds.move(placeX, 0, placeY)
        cmds.select(cl=True)

class bridge(object):
    mesh=None
    def __init__(self, rotation=0):
        self.rotation = rotation

    def create(self,placeX=0, placeY=0, placeZ=0):
        cmds.polyCube(d=3, w=10, h=0.2, n="Bridge", sx=7, sy=3, sz=3)
        #top posts
        cmds.polyExtrudeFacet("Bridge.f[22]")
        cmds.polyExtrudeFacet("Bridge.f[26]")
        cmds.polyExtrudeFacet("Bridge.f[40]")
        cmds.polyExtrudeFacet("Bridge.f[36]")
        cmds.polyMoveVertex("Bridge.vtx[104:119]", ty=3.5)
        #Bottom posts
        cmds.polyExtrudeFacet("Bridge.f[64]")
        cmds.polyExtrudeFacet("Bridge.f[68]")
        cmds.polyExtrudeFacet("Bridge.f[78]")
        cmds.polyExtrudeFacet("Bridge.f[82]")
        cmds.polyMoveVertex("Bridge.vtx[120:135]", ty=-2)
        #ramps
        cmds.polyExtrudeFacet("Bridge.f[93:101]")
        cmds.polyMoveVertex("Bridge.vtx[132:147]", ty=-2, tx=-7)
        cmds.polyExtrudeFacet("Bridge.f[84:92]")
        cmds.polyMoveVertex("Bridge.vtx[145:159]", ty=-2, tx=7)

        cmds.setAttr("Bridge.translateZ",placeY)
        cmds.setAttr("Bridge.translateX",placeX)
        cmds.setAttr("Bridge.translateY",placeZ)
        cmds.setAttr("Bridge.ry", self.rotation)
