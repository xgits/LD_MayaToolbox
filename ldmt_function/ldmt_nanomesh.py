import os
import math
from ldmt_function.ldmt_loadUIFile import get_maya_window, load_ui_type
import maya.OpenMayaUI as omui
from ldmt_core import ldmt_cmds as ld
from functools import partial
import maya.cmds as cmds
import maya.mel as mel

try:
    from PySide2.QtCore import * 
    from PySide2.QtGui import * 
    from PySide2.QtWidgets import *
    from PySide2.QtUiTools import *
    from PySide2 import __version__
    from shiboken2 import wrapInstance 
except ImportError:
    from PySide.QtCore import * 
    from PySide.QtGui import * 
    from PySide.QtUiTools import *
    from PySide import __version__
    from shiboken import wrapInstance 

import maya.OpenMaya as om
import maya.api.OpenMaya as om2
import random
import ast

LDMTPATH = ld.getPath('LDMT')
ldmt_uifile = LDMTPATH + '/ldmt_ui/ldmt_nanomesh.ui'
ldmt_list_form, ldmt_list_base = load_ui_type(ldmt_uifile)
ldmt_window_name = 'ldmt_nanomesh'
ldmt_button_name = 'btn_'+ldmt_window_name.split('_')[1]
'''
#UI
'''
class ldmt_cls(ldmt_list_form, ldmt_list_base):
    def __init__(self, parent = get_maya_window()):
        super(ldmt_cls, self).__init__(parent)
        self.window_name = 'ldmt_nanomesh'
        self.setupUi(self)
        self.move(QCursor.pos() + QPoint(20,20))
        # update status bar so it's not only show in help line window.
        self.setupBtn()
        self.statusbar.showMessage(ld.tag())
        self.installStartBar()
    def setupBtn(self):
        self.btn_setNanoMesh.clicked.connect(self.setNanoMesh)
        self.btn_setTargetVerts.clicked.connect(self.setTargetVerts)
        self.btn_setTargetFaces.clicked.connect(self.setTargetFaces)
        self.btn_selectNanoMesh.clicked.connect(self.selectNanoMesh)
        self.btn_selectTargetVerts.clicked.connect(self.selectTargetVerts)
        self.btn_selectTargetFaces.clicked.connect(self.selectTargetFaces)
        self.btn_copyToVerts.clicked.connect(self.copyToVerts)
        self.btn_copyToVertsMethod2.clicked.connect(self.copyToVertsMethod2)
        self.btn_copyToFaces.clicked.connect(self.copyToFaces)
        self.btn_clearAll.clicked.connect(self.clearAll)
    def setNanoMesh(self):
        selection = cmds.ls(sl=1,o=1)
        sel = []
        for i in selection:
            if cmds.objectType(i)=="transform":
                sel.append(i)
        if sel != []:
            self.btn_selectNanoMesh.setText(str(sel))
        else:
            self.btn_selectNanoMesh.setText('...')

    def setTargetVerts(self):
        sel = cmds.ls(sl=1)
        try:
            selType = sel[0].split('.')[1][0] 
            if selType == 'v':
                self.btn_selectTargetVerts.setText(str(sel))
            else:
                ld.msg("Please select verts!")
        except:
            self.btn_selectTargetVerts.setText('...')
            ld.msg("Please select verts!")

    def setTargetFaces(self):
        sel = cmds.ls(sl=1)
        try:
            selType = sel[0].split('.')[1][0] 
            if selType == 'f':
                self.btn_selectTargetFaces.setText(str(sel))
            else:
                ld.msg("Please select faces!")
        except:
            self.btn_selectTargetFaces.setText('...')
            ld.msg("Please select faces!")
    def selectSetObjects(self,sel):
        if sel != '...':
            sel = ast.literal_eval(sel)
            cmds.select(sel,r=1)
        else:
            ld.msg('Nothing selected')
    def selectNanoMesh(self):
        sel = self.btn_selectNanoMesh.text()
        self.selectSetObjects(sel)

    def selectTargetVerts(self):
        sel = self.btn_selectTargetVerts.text()
        self.selectSetObjects(sel)

    def selectTargetFaces(self):
        sel = self.btn_selectTargetFaces.text()
        self.selectSetObjects(sel)
    def copyToVerts(self):
        cmds.undoInfo(ock = 1)
        nanoMeshes = self.btn_selectNanoMesh.text()
        nanoMeshes = ast.literal_eval(nanoMeshes)
        targetPoints = self.btn_selectTargetVerts.text()
        targetPoints = ast.literal_eval(targetPoints)
        targetPoints = cmds.ls(targetPoints,fl=1)
        self.copy2Vertex_normal_exec(nanoMeshes,targetPoints)
        cmds.undoInfo(cck = 1)
    def copy2Vertex_normal_exec(self,sel,points):
        targetObj = points[0].split('.')[0]
        targetList = om2.MSelectionList()
        targetList.add(targetObj)
        targetPath = targetList.getDagPath(0)
        targetVtxIt = om2.MItMeshVertex(targetPath)
        targetFaceIt = om2.MItMeshPolygon(targetPath)
        faceId_area = {}
        vtxId_faceId = {} 
        pointsId = []
        relatedFacesId = []
        vtxid_avgArea = {}
        avgAreaAll = 0
        avgAreaSum = 0
        for i in points:
            pointsId.append(int(i.split('[')[1][:-1]))

        while not targetVtxIt.isDone():
            index = targetVtxIt.index()
            if index in pointsId:
                faceIds = targetVtxIt.getConnectedFaces()
                vtxId_faceId[index]=list(faceIds)
                relatedFacesId = relatedFacesId + (list(faceIds))
            targetVtxIt.next()
            
        while not targetFaceIt.isDone():
            index = targetFaceIt.index()
            if index in relatedFacesId:
                area = targetFaceIt.getArea()
                faceId_area[index]=area
            targetFaceIt.next(None)
        for vtxid in vtxId_faceId:
            areaSum=0
            for faceid in vtxId_faceId[vtxid]:
                areaSum = areaSum + faceId_area[faceid]
            avgArea = areaSum / len(vtxId_faceId[vtxid])
            
            vtxid_avgArea[vtxid]=avgArea
        for vtxid in vtxid_avgArea:
            avgAreaSum = avgAreaSum + vtxid_avgArea[vtxid]
            
        avgAreaAll = avgAreaSum / len(vtxid_avgArea)

        for i in sel:
            pivotWSPos = cmds.xform(i,ws=1,q=1,piv=1)
            cmds.move(0,0,0,i,rpr=1)
            cmds.makeIdentity(i,apply=True, t=1, r=1, s=1, n=0)
            cmds.move(pivotWSPos[0],pivotWSPos[1],pivotWSPos[2],i,rpr=1)

        if cmds.objectType(sel[0]) == "transform":
            for point in points:
                pointId = int(point.split('[')[1][:-1])
                objToInstance = int(random.random()*len(sel))
                newInstance = cmds.instance(sel[objToInstance])
                position = cmds.pointPosition(point, w=1)
                normal = cmds.polyNormalPerVertex(point,q=1,xyz=1)
                self.copy2Vertex_normal_moveAlign(newInstance,normal,position)
                scaleValue = vtxid_avgArea[pointId]/avgAreaAll
                cmds.scale(scaleValue,scaleValue,scaleValue,newInstance, r=1)
        else:
            print("Select Object First!")
    def copy2Vertex_normal_moveAlign(self,newInstance,normal,position):
        normalVec = om2.MVector((normal[0],normal[1],normal[2]))
        positionVec = om2.MVector(position)
        yVec = om2.MVector((0,1,0))
        tangent1 = normalVec^yVec
        tangent1.normalize()
        if tangent1.length() == 0:
            tangent1= om2.MVector((1,0,0))
        tangent2 = normalVec^tangent1

        matrixM = om2.MMatrix((\
                            (tangent2.x, tangent2.y, tangent2.z,0),\
                            (normalVec.x,normalVec.y,normalVec.z,0),\
                            (tangent1.x,tangent1.y,tangent1.z,0),\
                            (positionVec.x,positionVec.y,positionVec.z,1)\
                            ))

        cmds.xform(newInstance,ws=1,m=matrixM)
    def copyToVertsMethod2(self):
        cmds.undoInfo(ock = 1)
        nanoMeshes = self.btn_selectNanoMesh.text()
        nanoMeshes = ast.literal_eval(nanoMeshes)
        targetPoints = self.btn_selectTargetVerts.text()
        targetPoints = ast.literal_eval(targetPoints)
        targetPoints = cmds.ls(targetPoints,fl=1)
        targetMesh = targetPoints[0].split('.')[0]
        cmds.select(targetMesh,r=1)
        cmds.makeIdentity(targetMesh,apply=True, t=1, r=1, s=1, n=0)
        self.copy2VertexPy(nanoMeshes,targetPoints)
        cmds.undoInfo(cck = 1)
    def copy2VertexPy(self,sel,points):
        if not len(sel) >= 1:
            raise RuntimeError("Select at least one object first.")
        targetMesh = cmds.ls(points,o=1)
        targetMesh = targetMesh[0]
        sizeOfTobeInstanced = len(sel)

        for objIndex in range(sizeOfTobeInstanced):
            eachObj = sel[objIndex]
            cmds.select(eachObj,r=1)
            pivotWSPos = cmds.xform(ws=1,q=1,piv=1)
            cmds.move(0,0,0,eachObj,rpr=1)
            mel.eval("FreezeTransformations")
            cmds.move(pivotWSPos[0],pivotWSPos[1],pivotWSPos[2],eachObj,rpr=1)

        vertBinormals, vertTangents, vertNormals, vertPoints = self.getPosNormalTangents(targetMesh)

        for i in points:
            vertid = int(str(i).split('[')[1][:-1])
            objToInstance = random.randrange(0,sizeOfTobeInstanced)
            newInstance = cmds.instance(sel[objToInstance])
            mat = self.vectorsToMatrix(vertBinormals[vertid], vertTangents[vertid], vertNormals[vertid], vertPoints[vertid])
            cmds.xform(newInstance, m=mat)

    def getPosNormalTangents(self, mesh, normalize=True):
        """ Prototype/Snippet to get vertex tangents from a mesh """
        selList = om.MSelectionList()
        selList.add(mesh)
        path = om.MDagPath()
        selList.getDagPath(0, path)
        path.extendToShape()
        fnMesh = om.MFnMesh(path)
        tangents = om.MFloatVectorArray()
        binormals = om.MFloatVectorArray()
        
        fnMesh.getTangents(tangents)
        fnMesh.getBinormals(binormals)
        itMeshVertex = om.MItMeshVertex(path)
        
        vertBinormals = om.MFloatVectorArray()
        vertBinormals.setLength(fnMesh.numVertices())
        
        vertTangents = om.MFloatVectorArray()
        vertTangents.setLength(fnMesh.numVertices())
        
        vertNormals = om.MFloatVectorArray()
        vertNormals.setLength(fnMesh.numVertices())
        
        vertId = 0
        connectedFaceIds = om.MIntArray()
        
        # For each vertex get the connected faces
        # For each of those faces get the 'tangentId' to get the tangent and binormal stored above
        # Use that to calculate the normal
        while(not itMeshVertex.isDone()):
            
            itMeshVertex.getConnectedFaces(connectedFaceIds)
            tangent = om.MFloatVector()
            binormal = om.MFloatVector()
            for x in xrange(connectedFaceIds.length()):
                faceId = connectedFaceIds[x]
                tangentId = fnMesh.getTangentId(faceId, vertId)
                binormal += binormals[tangentId]
                tangent += tangents[tangentId]
                
            binormal /= connectedFaceIds.length()
            tangent /= connectedFaceIds.length()
            
            if normalize:
                binormal.normalize()
                tangent.normalize()
            
            normal = tangent ^ binormal
            if normalize:
                normal.normalize()
            
            # Put the data in the vertArrays
            vertTangents.set(tangent, vertId)
            vertBinormals.set(binormal, vertId)
            vertNormals.set(normal, vertId)
            
            vertId += 1
            itMeshVertex.next()
            
        vertPoints = om.MPointArray()
        fnMesh.getPoints(vertPoints)
            
        return vertBinormals, vertTangents, vertNormals, vertPoints
    def vectorsToMatrix(self, binormal=(1, 0, 0), tangent=(0, 1, 0), normal=(0, 0, 1), pos=(0, 0, 0), asApi=False):
        """ Function to convert an orthogonal basis defined from seperate vectors + position to a matrix """
        def _parseAPI(vec):
            if isinstance(vec, (om.MVector, om.MFloatVector, om.MPoint, om.MFloatPoint)):
                vec = [vec(x) for x in xrange(3)]
            return vec
        binormal = _parseAPI(binormal)    
        tangent = _parseAPI(tangent)
        normal = _parseAPI(normal)
        pos = _parseAPI(pos)

        if asApi:
            matrix = om.MMatrix()
            for x in xrange(3):
                om.MScriptUtil.setDoubleArray(matrix[0], x, binormal[x])
                om.MScriptUtil.setDoubleArray(matrix[1], x, tangent[x])
                om.MScriptUtil.setDoubleArray(matrix[2], x, normal[x])
                om.MScriptUtil.setDoubleArray(matrix[3], x, pos[x])
            return matrix

        else:
            return [binormal[0], binormal[1], binormal[2], 0,
                    tangent[0],  tangent[1],  tangent[2],  0,
                    normal[0],   normal[1],   normal[2],   0,
                    pos[0],      pos[1],      pos[2],      1]
    def copyToFaces(self):
        cmds.undoInfo(ock = 1)
        nanoMeshes = self.btn_selectNanoMesh.text()
        nanoMeshes = ast.literal_eval(nanoMeshes)
        targetFaces = self.btn_selectTargetFaces.text()
        targetFaces = ast.literal_eval(targetFaces)
        targetFaces = cmds.ls(targetFaces,fl=1)
        targetMesh = targetFaces[0].split('.')[0]
        cmds.select(targetMesh,r=1)
        cmds.makeIdentity(targetMesh,apply=True, t=1, r=1, s=1, n=0)
        self.copyToFaces_exec(nanoMeshes,targetFaces)
        cmds.undoInfo(cck = 1)
    def copyToFaces_exec(self,sel,faces):
        targetObj = faces[0].split('.')[0]
        targetList = om2.MSelectionList()
        targetList.add(targetObj)
        targetPath = targetList.getDagPath(0)
        targetFaceIt = om2.MItMeshPolygon(targetPath)
        faceid_center = {}
        faceid_normal = {}
        faceid_area = {}
        facesId = []
        avgArea = 0
        avgAreaSum = 0
        for i in faces:
            facesId.append(int(i.split('[')[1][:-1]))
            
        while not targetFaceIt.isDone():
            index = targetFaceIt.index()
            area = targetFaceIt.getArea()
            center = targetFaceIt.center(space=2)
            normal = targetFaceIt.getNormal(space=2)
            faceid_center[index] = center
            faceid_normal[index] = normal
            faceid_area[index]=area
            targetFaceIt.next(None)

        for faceid in faceid_area:
            avgAreaSum = avgAreaSum + faceid_area[faceid]
            
        avgArea = avgAreaSum / len(faceid_area)

        for i in sel:
            pivotWSPos = cmds.xform(i,ws=1,q=1,piv=1)
            cmds.move(0,0,0,i,rpr=1)
            cmds.makeIdentity(i,apply=True, t=1, r=1, s=1, n=0)
            cmds.move(pivotWSPos[0],pivotWSPos[1],pivotWSPos[2],i,rpr=1)

        if cmds.objectType(sel[0]) == "transform":
            for face in faces:
                faceid = int(face.split('[')[1][:-1])
                objToInstance = int(random.random()*len(sel))
                newInstance = cmds.instance(sel[objToInstance])
                position = faceid_center[faceid]
                normal = faceid_normal[faceid]
                self.copy2Vertex_normal_moveAlign(newInstance,normal,position)

                scaleValue = faceid_area[faceid]/avgArea
                cmds.scale(scaleValue,scaleValue,scaleValue,newInstance, r=1)
        else:
            print("Select Object First!")
    def clearAll(self):
        self.btn_selectNanoMesh.setText('...')
        self.btn_selectTargetFaces.setText('...')
        self.btn_selectTargetVerts.setText('...')
    def installStartBar(self):
        allQWidgets = self.findChildren(QWidget)
        for i in allQWidgets:
            i.installEventFilter(self)

    def eventFilter(self, obj, event ):
        '''Connect signals on mouse over''' 
        if event.type() == QEvent.Enter:
            self.oldMessage = ld.tag()
            self.statusbar.showMessage(' '+obj.statusTip(),0) 
        elif event.type() == QEvent.Leave:
            self.statusbar.showMessage(' '+self.oldMessage, 0)
            pass 
            event.accept()
        return False 
    def closeEvent(self,event):
        ld.turnToolBtnOff(self,ldmt_button_name)
        cmds.deleteUI(ldmt_window_name)

def ldmt_show():
    if cmds.window(ldmt_window_name,ex=1):
        if cmds.window(ldmt_window_name,q=1,vis=1):
            cmds.window(ldmt_window_name,e=1,vis=0)
        else:
            cmds.window(ldmt_window_name,e=1,vis=1)
    else:
        ui = ldmt_cls()
        ui.show()

if __name__ == '__main__':
    ldmt_show()