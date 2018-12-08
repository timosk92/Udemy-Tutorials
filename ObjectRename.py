###
##Udemy Tutorial: Artist friendly Programming
###
from maya import cmds

SUFFIXES = {
"mesh":"geo",
"joint":"jnt",
"camera":None,
"ambientLight":"lgt"
}

DEFAULT_SUFFIX= "grp"



def rename(selection = False):
    """
    Renames objects by adding suffixes based on the object type
    Args:
        selection (bool): Whether we should use the selection or not. Defaults to False
    Raises:
        RuntimeError: If nothing is selected
    Returns:
        list: A list of all the objects renamed
    """
    objects = cmds.ls(selection=selection, dag=True)

    if selection and not objects:
        raise RuntimeError("Nothing Selected")

    objects.sort(key=len, reverse = True)


    for obj in objects:
        shortName = obj.split("|") [-1]
        #Split and get the last section of the full path name


        children =cmds.listRelatives(obj, children=True, fullPath=True) or []

        if len(children) == 1:
            child = children[0]
            objType = cmds.objectType(child)
        else:
            objType = cmds.objectType(obj)

        suffix = SUFFIXES.get(objType,DEFAULT_SUFFIX)
        #get the object type from the suffix dict, if you cant get default

        if not suffix:
            continue

        if shortName.endswith('_'+ suffix):
            continue


        newName = "%s_%s" % (shortName,suffix)
        cmds.rename (obj, newName)

        index = objects.index(obj)
        objects[index] = obj.replace(shortName,newName)
    return objects
