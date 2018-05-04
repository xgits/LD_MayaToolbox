import maya.cmds as cmds
import maya.mel as mel
import maya.api.OpenMaya as om2

def selectUVEdgeBorder():
    try:
        finalborder = []
        sel = cmds.ls(sl=1,o=1)
        sel = sel[0]+".map[*]"
        cmds.select(sel)
        mel.eval("polySelectBorderShell 1;")
        uvborder = cmds.ls(sl=1)
        uvborder = cmds.polyListComponentConversion(uvborder,te=1,internal=1)
        uvborder = cmds.ls(uvborder,fl=1)
        for border in uvborder:
            borderuv = cmds.polyListComponentConversion(border,tuv=1)
            borderuv = cmds.ls(borderuv,fl=1)
            if len(borderuv) > 2:
                finalborder.append(border)
        return finalborder
    except:
        print("TIP: There is no selection, select something first!")

def makeUVdic(sel):
    edge2uv = {}
    for edge in sel:
        uv = cmds.polyListComponentConversion(edge,tuv=1)
        uv = cmds.ls(uv,fl=1)
        edge2uv[edge] = uv
    return edge2uv
def morphToUV(baseobj):
    cmds.select(baseobj,r=1)
    uvborder = selectUVEdgeBorder()
    bordervertices = cmds.polyListComponentConversion(uvborder,tv=1)
    cmds.polySplitVertex(bordervertices)

    baseobj = cmds.ls(sl=1,o=1)
    basevertices = cmds.polyListComponentConversion(baseobj,tv=1)
    basevertices = cmds.ls(basevertices,fl=1)
    for i in basevertices:
        baseuv = cmds.polyListComponentConversion(i,tuv=1)
        uvpos = cmds.polyEditUV(baseuv,q=1)
        cmds.xform(i, t=(uvpos[0], uvpos[1],0 ),ws=1 )

def main():
    baseobj = cmds.ls(sl=1)
    morphToUV(baseobj[0])

    vertexes = cmds.polyListComponentConversion(baseobj,tv=1)
    uvs = cmds.polyListComponentConversion(baseobj,tuv=1)
    cmds.polyMergeVertex(vertexes,d=0.0001)
    cmds.polyMergeUV(uvs,d=0.001)
    
    cmds.polySoftEdge(baseobj,a=180,ch=1)
    f_command("Select Hard Edges")
    borderEdges = cmds.ls(sl=1)
    borderVerts = cmds.polyListComponentConversion(borderEdges,fe=1,tv=1) 
    borderEdges_usi = cmds.polyEvaluate(borderEdges,usi=1)
    for i in borderVerts:
        getMeshVtxPos(i)
def vertexOm2(vtxName):
    """
    Using Maya Python API 2.0
    """
    #_ Get vertex number and object having that vertex
    testVtx =re.search('(?<=\[)(?P<vtxNum>[\d]+)(?=\])', str(vtxName))
    if testVtx:
        vtxNum =int(testVtx.group('vtxNum'))
        vtxObj =vtxName.split('.')[0]
    else:
        return
    #___________Selection___________
    # 1 # Query the selection list
    selectionLs = om2.MGlobal.getActiveSelectionList()
    # 2 # Get the dag path of the first item in the selection list
    selObj = selectionLs.getDagPath(0)
    #___________Query vertex position ___________
    # create a Mesh functionset from our dag object
    mItVtx =MItMeshVertex(selObj)
    vtxPos=[]
    while not mItVtx.isDone():
        if mItVtx.index() == vtxNum:
            point =MPoint()
            point =mItVtx.position(MSpace.kWorld)
            vtxPos =[round(point.x, 5), round(point.y, 5), round(point.z, 5)]
            break
        mItVtx.next()
    return vtxPos
    
def getMeshVtxPos(vtxName):


    #_ Get Api MDagPath for object
    activList =MSelectionList()
    activList.add(vtxObj)
    pathDg =MDagPath()
    activList.getDagPath(0, pathDg)

    #_ Iterate over all the mesh vertices and get position of required vtx


    #_ Print or return your vtx position
    print [vtxPos]

#For Example
getMeshVtxPos('pSphere1.vtx[60]')
if __name__ =='__main__':
    vertexOm2(vtxName)
