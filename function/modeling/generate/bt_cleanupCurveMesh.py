# Author:		Steven T. L. Roselle
#
# Created:        ( 04/01/15 )

from pymel.core import *
import maya.cmds as cmds


def bt_cleanupCurveMesh():
        
    instanceNode = ''
    extrudeNode = ''
    
    select(filterExpand(sm=12),r=1)
    select(listRelatives( parent=True))
    meshes = ls(sl=1)    
    
    if (meshes.__len__()):
        
        for mesh in meshes:        

            if (attributeQuery ('taper', exists=1, node=mesh)):
                extrudeNode = (listConnections (mesh+'.taper'))
                instanceNode = (listConnections (extrudeNode[0]+'.path'))
                        
            #delete remaining history and constraints
            delete (mesh, ch=1)
            delete (mesh, constraints=1)      
            
            if (attributeQuery ('width', exists=1, node=mesh)):
                delete(listConnections (mesh+'.width'))
                deleteAttr (mesh+".width")
            if (attributeQuery ('orientation', exists=1, node=mesh)):
                delete(listConnections (mesh+'.orientation'))
                deleteAttr (mesh+".orientation")
                 
            if (attributeQuery ('curvature', exists=1, node=mesh)):
                deleteAttr (mesh+".curvature")
            if (attributeQuery ('taper', exists=1, node=mesh)):
                deleteAttr (mesh+".taper")
            if (attributeQuery ('twist', exists=1, node=mesh)):
                deleteAttr (mesh+".twist")
            if (attributeQuery ('lengthDivisionSpacing', exists=1, node=mesh)):
                deleteAttr (mesh+'.lengthDivisionSpacing') 
            if (attributeQuery ('lengthDivisions', exists=1, node=mesh)):
                deleteAttr (mesh+".lengthDivisions")                               
            if (attributeQuery ('widthDivisions', exists=1, node=mesh)):
                deleteAttr (mesh+".widthDivisions")  
                
            if (objExists (instanceNode)):
                delete (instanceNode)
                
    else:
        warning ('No meshes selected.\n')
 
        
bt_cleanupCurveMesh()



