import maya.cmds as cmds

def fixReverse():
    cmds.undoInfo(ock = 1)
    sel = cmds.ls(sl=1)
    selAll = cmds.filterExpand(sel,sm=12)
    for sel_child in selAll:
        cmds.select(sel_child)
        fixReverseDo(sel_child)
    cmds.select(sel,r=1)
    cmds.undoInfo(cck = 1)

def dotProduct(vecA,vecB):
    return vecA[0]*vecB[0] + vecA[1]*vecB[1] + vecA[2]*vecB[2]

def fixReverseDo(sel_child):
    selShape = sel_child
    if len(selShape) == 0:
        print("Nothing Selected!")
    else:
        node_CPOM = cmds.createNode('closestPointOnMesh')
        selShape_worldMesh = selShape + '.worldMesh[0]'
        selShape_worldMatrix = selShape + '.worldMatrix[0]'
        node_CPOM_inMesh = node_CPOM + '.inMesh'
        node_CPOM_inPosition = node_CPOM + '.inPosition'
        node_CPOM_inputMatrix = node_CPOM + ".inputMatrix"
        node_CPOM_result_normal = node_CPOM + ".result.normal"
        node_CPOM_outPosition = node_CPOM + ".position"
        persp_translate = "persp.translate"

        cmds.connectAttr(selShape_worldMesh, node_CPOM_inMesh ,force=1)
        cmds.connectAttr(persp_translate, node_CPOM_inPosition ,force=1)
        cmds.connectAttr(selShape_worldMatrix, node_CPOM_inputMatrix ,force=1)

        vec_persp_pos = cmds.getAttr(persp_translate)
        vec_closestPoint_pos = cmds.getAttr(node_CPOM_outPosition)
        vec_closestPoint_normal = cmds.getAttr(node_CPOM_result_normal)
        vec_persp_closestPoint = [vec_persp_pos[0][0] - vec_closestPoint_pos[0][0],
                                vec_persp_pos[0][1] - vec_closestPoint_pos[0][1],
                                vec_persp_pos[0][2] - vec_closestPoint_pos[0][2]]
        dotProductResult = dotProduct(vec_persp_closestPoint,vec_closestPoint_normal[0])
        if dotProductResult<0:
            cmds.polyNormal(selShape,normalMode=0,userNormalMode=1,ch=1)
        cmds.delete(node_CPOM)
