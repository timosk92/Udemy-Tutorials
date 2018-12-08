'''
Udemy Tutorial: Artist friendly Programming
'''
from maya import cmds

SUFFIXES = {
"mesh":"geo",
"joint":"jnt",
"camera":None
}

DEFAULT_SUFFIX= "grp"



def rename():
    selection = cmds.ls(sl=True)

    if len(selection) == 0:
        selection = cmds.ls(dag=True, long=True)


    selection.sort(key=len, reverse = True)


    for obj in selection:
        shortName = obj.split(" | ") [-1]
        'Split and get the last section of the full path name'


        children =cmds.listRelatives(obj, children=True, fullPath=True) or []

        if len(children) == 1:
            child = children[0]
            objType = cmds.objectType(child)
        else:
            objType = cmds.objectType(obj)

        suffix = SUFFIXES.get(objType,DEFAULT_SUFFIX)
        "get the object type from the suffix dict, if you cant get default"

        if not suffix:
            continue

        if obj.endswith(suffix):
            continue


        newName = shortName + "_" + suffix
        cmds.rename (obj, newName)
