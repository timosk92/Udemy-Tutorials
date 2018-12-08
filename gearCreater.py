from maya import cmds

def createGear(teeth=10,length =0.3):
    """
    This function will create a gear with given parameters
    ARG:Teeth, length
    RETURNS: Tuple of constructor,transform and extrude nodes
    """
    spans = teeth * 2

    transform, constructor = cmds.polyPipe(subdivisionsAxis=spans)

    sideFaces = range(spans*2,spans*3,2)

    cmds.select(clear=True)

    for face in sideFaces:
        cmds.select("%s.f[%s]" % (transform,face),add = True)

    extrude = cmds.polyExtrudeFacet(localTranslateZ=length)[0]
    return constructor,transform,extrude


def changeTeeth(constructor,extrude, teeth=10, length=0.3):
    spans = teeth*2
    cmds.polyPipe(constructor, edit=True,subdivisionsAxis=spans)

    sideFaces = range(spans*2,spans*3,2)
    faceNames = []

    for face in faces:
        faceNames = "f[%s]" % (face)
        faceName.append(facesNames)

    cmds.setAttr('%s.inputComponent' % (extrude)), len(faceNames)