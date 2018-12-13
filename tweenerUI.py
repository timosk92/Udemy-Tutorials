from maya import cmds

def tween(percentage, obj=None, attrs=None,selection=True):

    #If obj is not given and selection is set to false Erorr
    if not obj and not selection:
        raise ValueError("No object to tween")
    #no obj specified get first one
    if not obj:
        obj = cmds.ls(selection=True)[0]

    if not attrs:
        attrs = cmds.listAttr(obj,keyable=True)

    currentTime= cmds.currentTime(query=True)


    for attr in attrs:
        #construct the full name of the attribute
        attrFull = "%s.%s" % (obj,attr)


        keyframes = cmds.keyframe(attrFull, query=True)
        #If there are no keys
        if not keyframes:
            continue


        previousKeyframes = []

        for frame in keyframes:
            if frame <currentTime:
                previousKeyframes.append(frame)

        laterKeyframes = [frame for frame in keyframes if frame > currentTime]

        if not previousKeyframes and not laterKeyframes:
            continue

        if previousKeyframes:
            previousFrame = max(previousKeyframes)
        else:
            previousFrame = None

        nextFrame = min(laterKeyframes) if laterKeyframes else None


        if not previousFrame or not nextFrame:
            continue

        previousValue = cmds.getAttr(attrFull, time=previousFrame)
        nextValue = cmds.getAttr(attrFull, time=nextFrame)

        difference = nextValue - previousValue
        weightedDifference = (difference * percentage) / 100.0
        currentValue = previousValue +weightedDifference

        cmds.setKeyframe(attrFull, time=currentTime, value = currentValue)
    return attrFull


def deleteKey(obj=None, attrs=None,selection=True):

    #If obj is not given and selection is set to false Erorr
    if not obj and not selection:
        raise ValueError("No object to tween")
    #no obj specified get first one
    if not obj:
        obj = cmds.ls(selection=True)[0]

    if not attrs:
        attrs = cmds.listAttr(obj,keyable=True)

    currentTime= cmds.currentTime(query=True)


    for attr in attrs:
        #construct the full name of the attribute
        attrFull = "%s.%s" % (obj,attr)

    print attrFull
    cmds.cutKey(attrFull, time=(currentTime,currentTime))


class tweenUI(object):

    windowName = "TweenerUI"
    def show(self):

        if cmds.window(self.windowName, query=True, exists=True):
            cmds.deleteUI(self.windowName)

        cmds.window(self.windowName)

        self.buildUI()
        cmds.showWindow()
    def buildUI(self):
        column =cmds.columnLayout()
        cmds.text("Use the slider to set tween amount")

        row = cmds.rowLayout(numberOfColumns=2)
        self.slider = cmds.floatSlider(min=0,max=100, value = 50, step=1,changeCommand=tween)

        cmds.button(label="reset",command=self.reset)
        cmds.setParent(column)
        cmds.button(label='close',command = self.close)

    def reset(self,*args):
        print "resetting...."
        cmds.floatSlider(self.slider, edit = True, value=50)
        deleteKey()

    def close(self,*args):
        cmds.deleteUI(self.windowName)
