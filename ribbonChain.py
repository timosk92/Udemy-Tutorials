'''
Flexible Ribbon Script
Written by Timothy Kelly
'''

import maya.cmds as cmds


class createRibbon(object):

    def __init__(self,diameter=1,placeX=0, placeY=0, placeZ=0):
        self.diameter = diameter
        self.placeX = placeX
        self.placeY = placeY
        self.placeZ = placeZ

    def create(self):
        joints = []
        cmds.circle(n="Bottom", nr=(0, 1, 0), c=(self.placeX, self.placeY, self.placeZ), r=5)
        cmds.circle(n="Middle", nr=(0, 1, 0), c=(self.placeX, self.placeY + 24 / 2, self.placeZ), r=5)
        cmds.circle(n="Top", nr=(0, 1, 0), c=(self.placeX, self.placeY+24, self.placeZ), r=5)
        cmds.select(d=True)
        for x in range(0, 9):
            joint = cmds.joint(n="spine_JNT_" + str(x), p=(x, 0, 0))
            joints.append(joint)
        for joint in joints:
            cmds.setAttr((joint + ".translateX"),3)
        cmds.setAttr("spine_JNT_0.translateX", 0)
        cmds.setAttr("spine_JNT_0.jointOrientZ", 90)
        for x in range(0, 3):
            cmds.select(d=True)
            cmds.joint(n="CTL_JNT_0"+str(x), p=(0, 12 * x, 0))
        cmds.curve(d=1, n="ribbon1", p=([-0.3, 0, 0], [-0.3, 3, 0], [-0.3, 6, 0], [-0.3, 9, 0], [-0.3, 12, 0], [-0.3, 15, 0], [-0.3, 18, 0], [-0.3, 21, 0], [-0.3, 24, 0]))
        cmds.curve(d=1, n="ribbon2", p=([0.3, 0, 0], [0.3, 3, 0], [0.3, 6, 0], [0.3, 9, 0], [0.3, 12, 0], [0.3, 15, 0], [0.3, 18, 0], [0.3, 21, 0], [0.3, 24, 0]))
        cmds.select('ribbon1')
        cmds.select('ribbon2', add=True)
        cmds.loft('ribbon1', 'ribbon2', rn=0, po=0, rsn=True, n="ribbonMesh")
        cmds.rebuildSurface(rt=0, dir=2, su=16, sv=1)
        cmds.createHair(9,1)