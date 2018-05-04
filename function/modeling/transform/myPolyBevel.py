import pymel.core as pm
import math
from functools import partial


def myPolyBevel(*args):
    Main()

class Main():   
    def __init__(self):            
        self.myRatio = math.sqrt(2) * 0.5
        self.showUI()
        
    # called by chamfer
    def chamferOn(self,*args):        
        pm.setAttr( self.myBevel.name()+".chamfer", 1 )  
    
    def chamferOff(self,*args):
        pm.setAttr( self.myBevel.name()+".chamfer", 0 ) 

    # called by convert
    def convertOn(self,*args):
        self.myRatio = math.sqrt(2) * 0.5
        self.myOffset()
    
    def convertOff(self,*args):
        self.myRatio = 1.0
        self.myOffset()
        
    def myOffset(self,*args): 
        temp =  pm.floatSliderGrp( self.myOffsetSlider, query = True, value = True ) * self.myRatio
        pm.setAttr( self.myBevel.name()+".offset", temp )
    
    def showUI(self,*args):   
       
        if pm.selected():
            newBevel = pm.polyBevel3( pm.selected(), offset = 0.1 * self.myRatio, segments = 2, smoothingAngle  = 30, chamfer = 1 )
            self.myBevel = newBevel[0]
            
            # UI  
            if pm.window('Bevel', exists = True):
                pm.deleteUI('Bevel')                 
            self.bevelWindow =  pm.window('Bevel')
            self.bevelLayout = pm.columnLayout()
            
            self.myConvert = pm.checkBoxGrp( numberOfCheckBoxes = 1, label = '', label1 = 'Convert', value1 = 1, 
                                            onCommand = partial(self.convertOn), offCommand = partial(self.convertOff) )            
            self.myOffsetSlider = pm.floatSliderGrp( label='Offset', field = True,
                                                    minValue = 0.0, maxValue = 5.0,
                                                    fieldMinValue = 0.0, fieldMaxValue = 100.0,
                                                    value = 0.1, step = 0.001,
                                                    dragCommand = partial(self.myOffset), changeCommand = partial(self.myOffset) )
            pm.attrControlGrp( attribute = self.myBevel.segments )
            pm.attrControlGrp( attribute = self.myBevel.depth )
            pm.attrEnumOptionMenuGrp(   label = 'Mitering',attribute = self.myBevel.mitering,
                                        enumeratedItem = [(0,'Auto'), (1,'Uniform'), (2,'Patch'), (3,'Radial'), (4, 'None')] )                          
            pm.attrEnumOptionMenuGrp(   label = 'Miter Along', attribute = self.myBevel.miterAlong,
                                        enumeratedItem = [(0,'Auto'), (1,'Center'), (2,'Edge'), (3,'Hard Edge')] )                             
            self.myChamfer = pm.checkBoxGrp( numberOfCheckBoxes = 1, label = '', label1 = 'Chamfer', value1 = 1, 
                                            onCommand = partial(self.chamferOn), offCommand = partial(self.chamferOff) )                                         
            pm.showWindow('Bevel') 
        