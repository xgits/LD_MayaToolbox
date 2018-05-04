import maya.cmds as cmds
def remove_namespaces(node):

    try:
        # Note rsplit instead of split

        namespace, name = node.rsplit(":", 1)
    except:
        namespace, name = None, node

    if namespace:
        try:
            cmds.rename(node, name)
        except RuntimeError:
            # Can't remove namespaces from read-only nodes
            # E.g. namespaces embedded in references
            pass

def remove_namespaces_from_selection():
    for node in cmds.ls(sl=1):
        # Remove namespaces of all children first
        for descendent in cmds.listRelatives(node, allDescendents=True):
            remove_namespaces(descendent)

        # Finally, remove namespace from current selection
        remove_namespaces(node)


remove_namespaces_from_selection()