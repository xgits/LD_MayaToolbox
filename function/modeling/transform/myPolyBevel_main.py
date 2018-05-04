import pymel.core as pm
import math
import sys
import os
import maya.mel

#add work path

import myPolyBevel

#UI  
class myPolyBevel_main():   
    def __init__(self):               
        self.showUI()
        
    def showUI(self):
        if pm.window('Star', exists = True):
            pm.deleteUI('Star')
        with pm.window('Star'):
            with pm.gridLayout( cellWidthHeight = (40,40), numberOfColumns = 5 ):
                 pm.button('Bevel', command = myPolyBevel.myPolyBevel)
        pm.showWindow()

myPolyBevel_main() 
       
#delete work path
#sys.path.remove(modulePath)
