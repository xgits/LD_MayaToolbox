import maya.cmds as cmds
import maya.mel as mm
import colorsys
import math
from collections import deque
global dQ
global gbType
dQ = '\"'
gbType = 1
groomKits = 1
# 0 is demo 1 is license 2 is gb exclusive 4 is testing


def groomBoyDemo():

    if not gbType == 4:
        init = initialChecks()    
        if not init:
            return
    GBCallgroomBoy()

def initialChecks():
    
    ss = True
    if not cmds.window('gbWin', exists = True):
        if gbType == 1:
            licenseValid = licenseCheckGB()
        elif gbType == 2:
            licenseValid = licenseCheckGB()
            ss = verifySessionFiles()
        else:            
            ss = verifySessionFiles()
    if not ss:
        return False
    else:
        return True        

def GBCallgroomBoy():

    if gbDebugCheck() or gbType == 4:
#        print 'change work for debug'
#        scriptEditorWork()
        scriptEditorDebug()
    
    else:          
        scriptEditorWork()
    gbAutoRefresh()

    origSelect = cmds.ls(sl = True)
    cmds.flushUndo()
    newNode = False
    addChar = False
    charEnable = False
    scalpMesh = [] 
    networkNodes = cmds.ls(type = 'network')
    if not 'gbNode' in networkNodes:
        newNode = True
        addChar = True
    if not newNode:
        scalpMesh = getCharNodes()
#        print scalpMesh
    if len(scalpMesh) == 0:
        addChar = True
    else:
        charEnable = True
        
    iconPath = assignPathToIcons()
                
    if cmds.window('gbWin', exists = True):
        cmds.deleteUI('gbWin')
    if gbType == 0:
        titleName = 'Groomboy Demo'
    elif gbType == 2:
        titleName = 'Groomboy Exclusive'
    else:
        titleName = 'Groomboy'                
    cmds.window('gbWin', retain = True, rtf = True, width = 300, title = titleName)
    
    cmds.menuBarLayout('gbMenuBar')
    cmds.menu('selCharMenu',label = 'Scalp Mesh', enable = charEnable)
    cmds.radioMenuItemCollection('charRadio')
    for scalp in scalpMesh:
        cmds.menuItem(scalp + '_radio', label = cmds.getAttr(scalp + '.displayName'), cl = 'charRadio', c = 'charSelected()', radioButton = False )
    cmds.menuItem('scalpMeshDivider', d = True, p = 'selCharMenu')        
    cmds.menuItem('addNewMeshMenu', label = 'Add New Scalp Mesh', p = 'selCharMenu' , c = 'menuNewChar()')
    
    if not gbType == 1:
        cmds.menu(label = 'Buy License')
        cmds.menuItem(label = 'Generate License Key', c = 'createLicenseKeyGB()' )
        cmds.menuItem(label = 'Purchase', c = 'gbPurchaseMenu()')
        cmds.setParent('..')
    
    cmds.menu(label = 'Help', helpMenu = True)
    cmds.menuItem(label = 'Documentation', command = 'gbDocumentation()')
    cmds.menuItem(label = 'Video Tutorials / Tips', command = 'gbVideoTuts()')
    cmds.menuItem(label = 'About Groomboy', command = 'aboutUs()')
    cmds.setParent('..')

    if groomKits == 1:
        cmds.menu(label = 'Groom Kits')
#    cmds.menuItem(label = 'Clump Mesh Generator Kit', c = 'launchClumpMeshGenKit()')
        cmds.menuItem(label = 'Mesh Strips Generator Kit', c = 'launchMeshStripGenKit()')
    
    cL0 = cmds.columnLayout('cL0Layout', adj = True)
    cL1 = cmds.columnLayout('cL1Layout', adj = True)
    
#    Edit Base Mesh
    cmds.button('editBaseMeshBtn', label = 'Edit Mesh', vis = False, p = 'cL1Layout',  c = 'dropEditBaseMesh()')
    cmds.frameLayout('editBaseMeshFrame',p = 'cL1Layout', label = 'Edit Mesh', vis = False, cll = True, cl = True, cc = 'editBaseMeshOnCollapse()')
    cmds.columnLayout('editBaseMeshCL',adj = True, p = 'editBaseMeshFrame')
    cmds.radioButtonGrp('selectUpdateMeshRadio', cw2 = [125,125] , labelArray2 = ['Scalp Mesh', 'Volume Mesh'], numberOfRadioButtons = 2, cc = 'updateMeshSelected()', vis = True,sl = 2)
    cmds.button('tweakMeshBtn', label = 'Enter Tweak Mode', c = 'enterTweakMesh(\'\')')
    cmds.button('updateBaseMeshBtn', label = 'Update Base Mesh', c = 'execUpdateMesh()', vis = False)
    cmds.button('polySmoothVolMeshBtn', label = 'Poly Smooth Volume Mesh',vis = False,  c = 'polySmoothVolUpdate()')
    cmds.button('cancelUpdateBtn', label = 'Cancel and Revert Back', c = 'cancelUpdateBaseMesh()')
    cmds.text('editMeshOperation', label = '', vis = False)
    cmds.progressBar('editMeshFrameProgress', vis = False,width = 300) 


#    Handy Tools    
    cmds.frameLayout('commonFrame',p = 'cL1Layout', label = 'Handy Tools', vis = False, cc = 'handyToolsCollapse()', ec = 'handyToolsExpand()', cll = True, cl = True)
    
    cmds.columnLayout('handyToolsMainLyt', adj = True, p = 'commonFrame')
    cmds.button('bkpResBtn', label = 'Backup and Restore', vis = charEnable, c = 'backupRestoreGB()')
    cmds.button('showHideBtn', label = 'Show / Hide Elements', vis = charEnable, c = 'showHideUI()')
#    cmds.button('refGBBtn', label = 'Refresh GB Database', vis = charEnable, c = 'refreshGBDatabase()')
    
    cmds.frameLayout('htCurvesFrame', p = 'handyToolsMainLyt', label = 'Curves', cll = True, cl = True)
    cmds.rowLayout('r1', p = 'htCurvesFrame',  nc = 7)
    cmds.button(label = 'Rebuild',c = 'rebuildSelected()')
    cmds.text(label = 'CVs')
    cmds.intField('rbCVField', ann = 'Ctrl + LMB to Slide',w = 50, v = 15, s = 1, min = 4, max = 50)
    cmds.checkBox('check01', label = '0 to 1', v = True)
    cmds.button(label = 'CV Range ?', c = 'checkCVRange()')
    cmds.intField('minCV', ed = False,w = 25, en = False)
    cmds.intField('maxCV', ed = False,w = 25, en = False)
    cmds.setParent('htCurvesFrame')
    cmds.button(label = 'Set Pivot to Root CV',c = 'pivotToRoot()', p = 'htCurvesFrame')
    cmds.button(label = 'Tweak Mode', c = 'tweak()', p = 'htCurvesFrame')
    cmds.button(label = 'Snap Root CV to closest vertex', c = 'snapSelectedToNearestVertex()', p = 'htCurvesFrame')
    cmds.button(label = 'Repositon Curves to Active Mesh', c = 'repositionCurvesToActiveMesh()', p = 'htCurvesFrame')
#    cmds.button(label = 'Snap Selected Curves back to Mesh', c = 'snapSuperCurvesBackToMesh(\'fromUI\')', p = 'htCurvesFrame')
    cmds.button(label = 'Snap Selected Curves back to Scalp Mesh', c = 'touchCurvesToMesh()', p = 'htCurvesFrame')
    cmds.button(label = 'Snap Selected Curves back to Volume Mesh', c = 'touchCurvesToMesh(\'volumeMesh\')', p = 'htCurvesFrame')
    cmds.button(label = 'Convert Remaining Strokes to Super Curves', c = 'pfxToCurvesFromUI(\'handyTools\')')
    cmds.button(label = 'Scale Curvature on Selected Curves', c = 'launchScaleCurvature()', p = 'htCurvesFrame')
    cmds.button(label = 'Step Curves Tool', c = 'stepCurvesTool()', p = 'htCurvesFrame')
#    cmds.button(label = 'Assign Preview Hair System', c = 'gbHairPreviewSystem()', p = 'htCurvesFrame')
    
    cmds.frameLayout('htMeshFrame',  p = 'handyToolsMainLyt', label = 'Poly Mesh', cll = True, cl = True)
    cmds.button('htSculptGeoBtn', label = 'Edit Using Sculpt Geometry Tool', c = 'handyToolsSculptGeo()', p = 'htMeshFrame')
    cmds.rowLayout('htSculptGeoMaxDispLyt', vis = False, nc = 2)
    cmds.text('htSculptGeoMaxDispText', label = '           Max Displacement:', vis = False, p = 'htSculptGeoMaxDispLyt')
    cmds.floatField('htSculptGeoMaxDispFloat', v = 1.0, min = 0.01, pre = 2, step = .01, vis = False, p = 'htSculptGeoMaxDispLyt')
    cmds.floatField('htSculptGeoMaxDispFloat', edit = True, cc = 'sculptGeoMaxDispUpdate()', ec = 'sculptGeoMaxDispUpdate()', dc = 'sculptGeoMaxDispUpdate()')
    cmds.rowLayout('htDisplayMeshLyt', nc = 2, p  = 'htMeshFrame')
    cmds.text('htDisplayMeshText', label = 'Set Offset % for Display Mesh', p = 'htDisplayMeshLyt')
    cmds.floatField('htDisplayMeshFloat', v = 1.5, min = 0.01, max = 5.0, pre = 2, cc = 'handyRefreshDisplayMesh()', p = 'htDisplayMeshLyt')

#    Add Character Mesh    
    
    cmds.iconTextButton('addScalpBtnICON', label = 'Create Groomboy Character Setup', w = 250, h = 182, style = 'iconAndTextVertical', vis = addChar, c = 'enterScalpDP()', p = cL0 )
    cmds.iconTextButton('addScalpBtnICON', edit = True, i = iconPath + 'charSetup.jpg')

    cmds.textField('addScalpText', tx = autoGBDisplayName(), aie = True, rfc = 'clearText()' , vis = False, ec = 'onCharMeshUpdate()', p = cL0) 

    cmds.button('cancelAddNewCharacterBtn', vis = addChar, label = 'Cancel Character Setup', c = 'cancelAddNewChar()', p = cL0)
    cmds.button('confirmScalpText', vis = False, label = 'Continue', c = 'onCharMeshUpdate()', p = cL0)
    cmds.columnLayout('volumeMeshLT', p = cL0, adj = True, vis = False)
    cmds.columnLayout('askDrawMeshLayout', p = cL0, adj = True, vis = False)
    
    cmds.text(label = '', p = 'cL1Layout')
        
#    Tabs    
    cmds.tabLayout('mainTabs', en = False,  p = cL1, vis = False)

    child1 = cmds.columnLayout(adj = True, p = 'mainTabs')
#    Radio Buttons        
    collection1 = cmds.radioCollection()
    rb1 = cmds.radioButton('onGridRadio', label = 'on UV Grid', vis = False, en = False, onc = 'drawOnGrid()')
    rb2 = cmds.radioButton('onCharRadio', label = 'on Character', vis = False, onc = 'drawOnChar(True)',select = True)
    cmds.setParent( child1 )

    cmds.columnLayout('uvTool', adj = True,vis = False, p = child1)
#     Start Drawing Button    
    cmds.button('startDrawBtn' , label = 'Start Drawing', c = 'startDraw()', p = child1, vis = False)
#    Drawing Tools Frame    
    cmds.frameLayout('uvDrawFrame', label = 'Drawing Tools',vis = False, p = child1, cll = True, cl = False,cc = 'toggleStartbtn()')
    cmds.rowLayout(nc = 3)
    cmds.checkBox('reflowChk', label = 'Reflow Mode', onc = 'enterReflowMode()', ofc = 'exitReflowMode()')
    cmds.text(label = '   Threshold %')
    cmds.floatField('reflowThres', v = 0.04, w = 35, pre = 2, s = 0.01, min = 0.01, max = 0.1)
    cmds.setParent('..')
    
    cmds.button('switchMeshBtn', label = 'Switch to Volume Mesh for Drawing', c = 'switchMeshToDraw()')
    cmds.rowLayout(nc = 3)
    cmds.checkBox('checkPFXRebuild', label = 'Auto Rebuild', v = True)
    cmds.text(label = 'CVs')
    cmds.intField('cvPFXRebuild', v = 10,w = 25,s = 1, min = 4, max = 50)
    cmds.setParent('..')
    cmds.rowLayout(nc = 3)
    cmds.checkBox('checkPFXSmooth', label = 'Auto Smooth', v = True)
    cmds.text(label = 'Smoothness')
    cmds.intField('smPFXSmooth', v = 1,w = 25,s = 1, min = 1, max = 10)
    cmds.setParent('..')
    
    cmds.rowLayout(nc = 3)
    cmds.checkBox('checkAutoSnapVtx', label = 'Auto Snap To Closest Vertex', v = False)
    cmds.text(label = 'Threshold %')
    cmds.floatField('drawAutoSnapThres', v = 5.0, w = 35, pre = 2, s = 0.1, min = 0.01, max = 20.0)
    cmds.setParent('..')
    
    cmds.checkBox('autoConvertToManualChk', label = 'Auto Convert to Freeform Curves')
    cmds.checkBox('autoConvertToRoughChk', label = 'Auto Convert to Rough Marking Curves')
    
    cmds.button('convertPFXToCrvBtn', label = 'Convert Strokes to Curves', c = 'pfxToCurvesFromUI(\'startDraw\')')
    
#    Curve Manipulation for Grid and Character
    cmds.frameLayout('gridCM', label = 'Curve Manipulation on Grid',  cll = True, cl = True, vis = False, p = child1)
    cmds.button('mapG2CBtn', label = 'Swap Curves between Character and UV Grid', c = 'swapCurvesBetweenMeshAndUVGrid()' , en = True)
    cmds.setParent('..')
    cmds.setParent(child1)

    cmds.frameLayout('charCM', label = 'Curve Mainipulation on Character', ec = 'checkGrid()', vis = False, cll = True, cl = True)
#    cmds.button('mapC2GBtn', label = 'Swap Curves between Character and UV Grid', c = 'swapCurvesBetweenMeshAndUVGrid()' , en = True)
    
    cmds.button(label = 'Add Super Curves for Interpolation', c = 'addSuperCurves()')
    cmds.button(label = 'Convert to Freeform curves', c = 'convertToFreeform()')
    cmds.button(label = 'Mirror Selected Super Curves', c = 'mirrorSelectedSuperCurves()')
    cmds.radioButtonGrp('mirrorSuperCurvesAxisRadio', cw3 = [90,90,90], labelArray3 = ['X', 'Y', 'Z'], numberOfRadioButtons = 3, sl = 1)
    
    cmds.frameLayout('interpolationFrame', label = 'Interpolation', cll = True, cl = True, p = child1)
    cmds.button('ipolPerSuperBtn', label = 'Create Interpolation Curves per Super Curve', c = 'createIpolPerSuper()', p = 'interpolationFrame')
#    cmds.rowLayout('runInterRowLyt', nc = 2, columnAlign2 = ['left', 'right'], ad2 = 2,  p = 'interpolationFrame')
#    cmds.intField('interPercentField', w = 30, v = 100, step = 5, min = 1, max = 100, cc = 'interPercentChanged()', ec = 'interPercentChanged()', p = 'runInterRowLyt')
    cmds.button('interCharBtn', label = 'Run Interpolation On Selected Area', c = 'charInterpolationSelectedFaces()',en = False, p = 'interpolationFrame')
#    cmds.button('interCharBtn', c = 'charInterpolationSelectedFaces()', en = False, p = 'runInterRowLyt')
#    cmds.button('interCharBtn', edit = True, label = 'get()')
#    interPercentChanged()
    cmds.button('removeInterBtn', label = 'Remove Interpolation From Selected Area', c = 'removeInterpolationFromSelected()', p = 'interpolationFrame')
    cmds.button('upIP', label = 'Update Interpolation', c = 'checkSuperAndIpolForUpdate()' , en = True, p = 'interpolationFrame')
    cmds.popupMenu(parent = 'interpolationFrame', mm = True, b = 3)
    cmds.menuItem(label = 'Load Previous Selection', rp = 'N', c = 'loadPreviousSelectionForIpol()')
    cmds.menuItem(label = 'Vertex Paint Selection', rp = 'W', c = 'loadPaintForIpol(\'Point\')')
    cmds.menuItem(label = 'Face Paint Selection', rp = 'E', c = 'loadPaintForIpol(\'Facet\')')
    cmds.menuItem(label = 'Select Vertices of all Ipol', rp = 'S', c = 'selectVerticesAllIpol()')
    
    
    cmds.setParent(child1)
    child2 = adjustVolTabUI()
    
    cmds.tabLayout( 'mainTabs', edit=True, tabLabel=((child1, '    Draw Guides    '), (child2, '    Assign Volume    ')) )        

    cmds.tabLayout( 'mainTabs', edit = True, cc = 'tabSelectChange()')


    cmds.columnLayout('gbProgressBarLyt', adj = True, p = 'cL0Layout')
    cmds.text('gbProgressBarText', vis = False)
    cmds.progressBar('gbProgressBar', vis = False, width = 300)

    cmds.rowLayout('gbMessageLayout', nc = 2, p = 'gbProgressBarLyt')
    cmds.text('gbMessageStatusColor', h = 20, label = '   ', vis = False, p = 'gbMessageLayout')
    cmds.text('gbMessageStatusText', font = 'obliqueLabelFont', vis = False, p = 'gbMessageLayout')
    cmds.showWindow()
    
    if cmds.textField('addScalpText', q = True, vis = True):
        cmds.setFocus('addScalpText')
        cmds.button('confirmScalpText', edit = True, vis = True)
        reportGBMessage('Press Enter to Continue', False, False, 'blue')
    
    if origSelect:
        cmds.select(origSelect, r = True)
    
    if len(scalpMesh) > 0:
        resumeLastGBNode()        

    
def adjustVolTabUI():
#    Adjust Volume Mesh Tab    
    child2 = cmds.columnLayout(adj = True, p = 'mainTabs')
    cmds.columnLayout('graphInitLyt', adj = True, p = child2)
    cmds.button('useIpolCurves', label = 'Use Interpolated Curves', c = 'ipolCurvesForVolume()', p = 'graphInitLyt')
    cmds.button('useFreeformCurvesBtn', label = 'Use Freeform Curves', c = 'freeFormCurvesForVolume()', p = 'graphInitLyt')
#    cmds.button('useSelectedCurves', label = 'Use Selected Curves', c = 'curvesForVolume()', p = 'graphInitLyt')
#    cmds.button('selGraphCurvesBtn', label = 'Select Graph Curves', vis = False, c = 'selectGraphCurves()', p = 'graphInitLyt')
    cmds.button('continueToGraphBtn', label = 'Continue', vis = False, c = 'continueForGraph()', p = 'graphInitLyt')
    cmds.progressBar('progressCurveMapping', vis = False, width = 300, p = 'graphInitLyt')

    cmds.columnLayout('adjVolLayout',adj = True, vis = False, p = child2)
    cmds.button(label = 'Quick Update the Volume Mesh',c = 'updateTargetMesh()', p = 'adjVolLayout')
    cmds.canvas('whiteCanvas', vis = False, rgbValue = (1, 1, 1),  height = 5)
    cmds.gradientControlNoAttr( 'defaultColorGraph', asString = '0,0,3,1,1,3', h = 100, p = 'adjVolLayout')
    cmds.popupMenu(b = 3)
    cmds.menuItem(label = 'Load Preset', c = 'loadPresetFromGraph(\'defaultColorGraph\')')
    cmds.menuItem(label = 'Save Preset', c = 'savePreset(\'defaultColorGraph\')')
    cmds.button(label = 'Auto Resize', c = 'autoResize()', p = 'adjVolLayout')
    cmds.intSliderGrp('globalScaleSlider', field = True, label = 'Global Scale %', minValue = -100, maxValue = 100, fieldMinValue = -100, fieldMaxValue = 500, value = 0, fs = 5, ss = 5) 
    cmds.intSliderGrp('globalScaleSlider', edit = True, dc = 'globalSliderChange()', cc = 'globalSliderChange()\nautoResize()')
    
    cmds.intSliderGrp('globalRandomSlider', field = True, label = 'Global Randomness %', minValue = 0, maxValue = 100, value = 0)
    cmds.intSliderGrp('globalRandomSlider', edit = True, dc = 'globalSliderChange()', cc = 'globalSliderChange()\nautoResize()')
    
    cmds.checkBox('regionGraphInteractiveBtn', vis = False, label = 'Interactive Tweak Mode for Updating Graphs', onc = 'interactiveRegionGraphUpdateON()', ofc = 'interactiveRegionGraphUpdateOFF()')
    cmds.button('loadGraphFromControlBtn', label = 'Copy Graph', vis = False, c = 'loadGraphFromSelControl()', p = 'adjVolLayout')
    cmds.button('updateGraphOnRegionBtn', label = 'Paste Graph', vis = False, c = 'regionUpdateGraphToSelControl(\'manual\')', p = 'adjVolLayout')
    cmds.setParent('adjVolLayout')

    cmds.columnLayout('updateCurvesLayout', adj = True, vis = False)
    cmds.button('Enter Tweak Mode', p = 'updateCurvesLayout')
    cmds.button('Update Selected Curves', p = 'updateCurvesLayout')
    cmds.setParent('updateCurvesLayout')
    
    
#    Restore Back + Edit Curves
    cmds.frameLayout('editCurves', label = 'Add/Remove Curves', cll= True, cl = True, ec = 'addIpolFromGraphUI()', p = 'adjVolLayout')
    cmds.button('addIpolCurvesForGraphBtn', label = 'Add Interpolated Curves', c = 'addIpolFrmGraphPage()', vis = False)
    cmds.button('addCurvesForGraphBtn', label = 'Add Selected Curves', c = 'addSelectedCurvesForGraph()')
    cmds.button('removeCurvesFromGraphBtn', label = 'Remove Selected Curves', c = 'removeSelectedCurvesFromGraph()')
    cmds.setParent('editCurves')
#    Localized Control
    cmds.frameLayout('localizedControlFrame', label = 'Localized Control of Graph', cll = True, cl = True, p = 'adjVolLayout')
    cmds.button('colorGraphControlBtn', label = 'Texture based Control', c = 'colorBasedGraphSelected()')
    cmds.button('regionGraphControlBtn', label = 'Region based control', c = 'regionBasedGraphSelected()')
    
#    Color Graphs    
    cmds.button('addColorGraphBtn', label = 'Add Color Based Graphs', vis = False, c = 'addColorGraphs()', p = 'adjVolLayout')
    cmds.frameLayout('colorGraphFrame', vis = False, label = 'Assign Texture', cll = True, cl = True, ec = 'newTextureRadioBtn()', p = 'adjVolLayout')
    cmds.columnLayout('addColorOptionsLyt', vis = False, adj = True, p = 'colorGraphFrame' )
    cmds.text('colorGraphDesc', label = 'Method for assigning texture', p = 'addColorOptionsLyt')
    cmds.radioButtonGrp('newTextureRadio', vr = True, cw3 = [125,125,125] , labelArray3 = ['3D Paint', 'Image File Path', 'Select from HyperShade'], numberOfRadioButtons = 3, sl = 1, p = 'addColorOptionsLyt')
    cmds.radioButtonGrp('newTextureRadio', edit = True, cc1 = 'paint3DSelected()', cc2 = 'imageFilePathSelected()', cc3 = 'hypershadeSelected()')
    cmds.button('enter3DPaintToolBtn', vis = False, label = 'Enter 3D Paint Tool', c = 'launch3DPaint()')
    cmds.rowLayout('filePathLayout',ct2 =['left','right'], ad2 = 2, vis = False, nc = 2)
    cmds.button('browseFileBtn', label = 'Browse', c = 'browseFilePathSelected(\'browse\')', p = 'filePathLayout')
    cmds.textField('texturefilePathTextField', tx = 'Paste Here Path for Image File', aie = True, ec = 'browseFilePathSelected(\'paste\')', rfc = 'fileTextFieldFocus()', p = 'filePathLayout')
    cmds.setParent('..')
    cmds.button('launchHSBtn', label = 'Open HyperShade Window', vis = False, c = 'launchHSWindow()')
    cmds.button('useSelectedTextureBtn', label = 'Use Selected 2D Texture Node', vis = False, c = 'useSelectedTextureFromHS()')
    cmds.setParent('colorGraphFrame')

    cmds.columnLayout('rgbGraphsColumn', vis = False, adj = True, p = 'adjVolLayout')
    
    cmds.button('editUsing3DPaintBtn', label = 'Edit Texture', vis = True, c = 'editUsing3DPaintOrAE()', p = 'rgbGraphsColumn')

    cmds.frameLayout('redGraphFrameLyt', label = 'Red Graph', cll = True, cl = True, p = 'rgbGraphsColumn')
    cmds.canvas(rgbValue = (1, 0, 0), height = 5, p = 'redGraphFrameLyt')
    cmds.gradientControlNoAttr( 'rgbGraphControl0', asString = '0,0,3,1,1,3',   h = 100, p = 'redGraphFrameLyt')
    cmds.popupMenu(b = 3)
    cmds.menuItem(label = 'Load Preset', c = 'loadPresetFromGraph(\'rgbGraphControl0\')')
    cmds.menuItem(label = 'Save Preset', c = 'savePreset(\'rgbGraphControl0\')')
    
    cmds.frameLayout('greenGraphFrameLyt', label = 'Green Graph', cll = True, cl = True, p = 'rgbGraphsColumn')
    cmds.canvas(rgbValue = (0, 1, 0),height = 5, p = 'greenGraphFrameLyt')
    cmds.gradientControlNoAttr( 'rgbGraphControl1',asString = '0,0,3,1,1,3',  h = 100, p = 'greenGraphFrameLyt')
    cmds.popupMenu(b = 3)
    cmds.menuItem(label = 'Load Preset', c = 'loadPresetFromGraph(\'rgbGraphControl1\')')
    cmds.menuItem(label = 'Save Preset', c = 'savePreset(\'rgbGraphControl1\')')
    
    cmds.frameLayout('blueGraphFrameLyt', label = 'Blue Graph', cll = True, cl = True, p = 'rgbGraphsColumn')
    cmds.canvas(rgbValue = (0, 0, 1), height = 5, p = 'blueGraphFrameLyt')
    cmds.gradientControlNoAttr('rgbGraphControl2', asString = '0,0,3,1,1,3', h = 100, p = 'blueGraphFrameLyt')
    cmds.popupMenu(b = 3)
    cmds.menuItem(label = 'Load Preset', c = 'loadPresetFromGraph(\'rgbGraphControl2\')')
    cmds.menuItem(label = 'Save Preset', c = 'savePreset(\'rgbGraphControl2\')')
    cmds.setParent('adjVolLayout')
    
#    Region based graphs
    cmds.frameLayout('regionBasedGraphFrame', vis = False, label = 'Region Based Graphs', cll = True, cl = True,p = 'adjVolLayout')
    cmds.button('paintRegionControlBtn', label = 'Paint Region Controllers', c = 'paintRegionControlExec()')   
    cmds.button('moveRegionControlBtn', label = 'Move Region Controller', c = 'moveRegionControlExec()')
    cmds.button('showhideRegionControlBtn', label = 'Mirror Selected Region Controllers', c = 'mirrorRegionCtrls()')
    cmds.radioButtonGrp('mirrorRegionCtrlAxisRadio', cw3 = [90,90,90], labelArray3 = ['X', 'Y', 'Z'], numberOfRadioButtons = 3, sl = 1, p = 'regionBasedGraphFrame')
    
#    cmds.frameLayout('groomKitsFrame', label = 'Groom Kits', vis = True, cll = True, cl = True, p = 'adjVolLayout')
#    cmds.button('launchClumpMeshBtn', label = 'Launch Clump Mesh Groomkit', c = 'launchClumpMeshKit()',  p = 'groomKitsFrame')
    return child2
    

#     Update Character Mesh 

def resumeLastGBNode():
    
    currNode = cmds.getAttr('gbNode.currentGBNode')
    cmds.menuItem(currNode + '_radio', edit = True, radioButton = True)
    charSelected()
    
def gbAutoRefresh():
    
    jobExists = False
    allJobs = cmds.scriptJob(lj = True)
    for job in allJobs:
        if 'restartGroomBoy' in job:
#            print job
            jobExists = True
    if not jobExists:                    
#        cmds.scriptJob(e = ['NewSceneOpened','groomBoy()'])
        cmds.scriptJob(e = ['SceneOpened','restartGroomBoy()'])    

            
#            cmds.scriptJob(attributeChange = ['gbNode.autoRefresh', 'groomBoy()'], runOnce = True)
            
    
def restartGroomBoy():
    
    if cmds.window('gbWin', exists = True):
        GBCallgroomBoy()
    elif cmds.objExists('gbNode'):
        GBCallgroomBoy()
    
#    print 'restart'
    if cmds.window('groomKitMeshStripWin', exists = True) or cmds.objExists('meshGenGBNode'):
#        print 'here'
        launchMeshStripGenKit()                    
        
def updateCharList():
    
    scalpMesh = []
    scalpMesh = getCharNodes()
#    cmds.menu('selCharMenu', edit = True, dai = True)

    if cmds.radioMenuItemCollection('charRadio', q = True, exists = True):
        allMI = cmds.lsUI(mi = True)
        for mi in allMI:
            if cmds.menuItem(mi, q = True, collection = True) == 'charRadio':
#                print mi
                cmds.deleteUI(mi)
        cmds.deleteUI('charRadio', ric = True)
    cmds.radioMenuItemCollection('charRadio', p = 'selCharMenu')
    for scalp in scalpMesh:
        cmds.menuItem(scalp + '_radio', label = cmds.getAttr(scalp + '.displayName'), c = 'charSelected()', radioButton = False, p = 'charRadio')
    cmds.menuItem(d = True)        
    cmds.menuItem(label = 'Add New Scalp Mesh', c = 'menuNewChar()')
    cmds.setParent('selCharMenu')

def clearText():

    return
    stopGBUndo()
    cmds.undoInfo(swf = False)
    cmds.textField('addScalpText', edit = True, tx = '')
    cmds.undoInfo(swf = True)
    startGBUndo()

def enterScalpDP():
    
    stopGBUndo()
    gbNodeInit()
    sel = cmds.ls(sl = True)
    if len(sel) > 0:
        if not cmds.ls(cmds.listRelatives(sel[0], s = True), type = 'mesh'):
#            print 'seleee', sel
            reportGBMessage('No Poly Mesh Selected', True, True, 'red')                                            
#            raise RuntimeError, 'No Poly Mesh Selected' 
    else:
        reportGBMessage('Nothing Selected', True, True, 'red')
#        raise RuntimeError, 'Nothing Selected'
    
    cmds.undoInfo(swf = False)        
    if gbType == 0:
        verifyForTESTVERSION(sel[0],True)
#    verifyScalpMesh(sel[0])
    
    scalpMesh = cmds.duplicate(sel[0], name = sel[0] + '_GB', rc = True, rr = True)[0]
#    scalpMesh = removeNameSpaceGB(scalpMesh)
        
    cmds.setAttr(sel[0] + '.visibility', False)
    cmds.select(scalpMesh, r = True)
    
    unlockXform(scalpMesh)        
    cmds.textField('addScalpText', edit = True, tx = autoGBDisplayName(), vis = True)
    cmds.setFocus('addScalpText')
    cmds.button('confirmScalpText', edit = True, vis = True)
    reportGBMessage('Press Enter to Continue', False, False, 'blue')
#    cmds.button('addScalpBtn' , edit = True, vis = False)
    cmds.iconTextButton('addScalpBtnICON', edit = True, vis = False)
    
    cmds.undoInfo(swf = True)
    startGBUndo()

# removeNameSpaceGB('asds:asdsd3r3')

def removeNameSpaceGB(meshName):
    
    if ':' in meshName:
        ind = meshName.index[':']
        return meshName[ind:]
        
        

def unlockXform(mesh):

    cmds.setAttr(mesh + '.tx', lock = False)
    cmds.setAttr(mesh + '.ty', lock = False)
    cmds.setAttr(mesh + '.tz', lock = False)
    cmds.setAttr(mesh + '.rx', lock = False)
    cmds.setAttr(mesh + '.ry', lock = False)
    cmds.setAttr(mesh + '.rz', lock = False)
    cmds.setAttr(mesh + '.sx', lock = False)
    cmds.setAttr(mesh + '.sy', lock = False)
    cmds.setAttr(mesh + '.sz', lock = False)    
    
    
def menuNewChar():
    
    stopGBUndo()
    killAllGBJobs()
    killPFXJob()
    charNodes = getCharNodes()
    
    if charNodes:
        for char in charNodes:
            cmds.setAttr(cmds.getAttr(char + '.mainGroup') + '.visibility', False)
    cmds.iconTextButton('addScalpBtnICON', edit = True, vis = True)
    
#    cmds.button('addScalpBtn' , edit = True, vis = True)
    cmds.textField('addScalpText', edit = True, tx = autoGBDisplayName())
    cmds.setFocus('addScalpText')
#    reportGBMessage('Press Enter to Continue', False, False, 'blue')
    cmds.button('cancelAddNewCharacterBtn', edit = True, vis = True)
    cmds.columnLayout('cL1Layout', edit = True, vis = False)
    if cmds.columnLayout('volumeMeshLT', q = True, exists = True):
        cmds.columnLayout('volumeMeshLT', edit = True, vis = False)
    if cmds.columnLayout('askDrawMeshLayout', q = True, exists = True):
        cmds.columnLayout('askDrawMeshLayout', edit = True, vis = False)
    startGBUndo()

def volMeshCreate():
    
    iconPath = assignPathToIcons()
    updateMeshStripsUIForGB()
    vml = 'volumeMeshLT'
    cmds.columnLayout('volumeMeshLT', edit = True, cal = 'center', vis = True)

    if not 'volRadio1' in cmds.lsUI(type = ['control']):
        cmds.text(label = 'Volume / Target Mesh Definition', fn = 'boldLabelFont', p = vml)
        
        
        cmds.radioButtonGrp('volRadio1', cw2 = [125,125] , labelArray2 = ['Existing Mesh', 'Create a New Mesh'], numberOfRadioButtons = 2, on1 = 'useExistVol()', on2 = 'createVol()', p = vml)
        cmds.iconTextRadioCollection( 'createVolRadioICON', p = vml )
        cmds.rowLayout('defaultSmartRowLayout', vis = False, nc = 2, p = vml)
        cmds.iconTextRadioButton('defaultVolRadioIcon', w = 125,h = 180, st = 'iconAndTextVertical', onc = 'defaultVol()', label = 'Default Volume Mesh',  p = 'defaultSmartRowLayout')
        cmds.iconTextRadioButton('smartVolRadioIcon', w = 125, h = 180, st = 'iconAndTextVertical', onc = 'smartVol()', label = 'Smart Volume Mesh',  p = 'defaultSmartRowLayout')        
        cmds.iconTextRadioButton('defaultVolRadioIcon', edit = True, i = iconPath + 'defaultVolMesh.jpg')
        cmds.iconTextRadioButton('smartVolRadioIcon', edit = True, i = iconPath + 'smartVolMesh.jpg')
#        cmds.radioButtonGrp('createVolRadio', cw2 = [125,125] , labelArray2 = ['Default Volume Mesh', 'Smart Volume Mesh'], numberOfRadioButtons = 2,on1 = 'defaultVol()', on2 = 'smartVol()', vis = False, p = vml)
#        cmds.image('defaultVolImage', i = iconPath + 'defaultVolMesh.jpg', vis = False, p = vml)     
#        cmds.image('smartVolImage', i = iconPath + 'smartVolMesh.jpg', vis = False, p = vml)        
        cmds.button('selExistVolBtn', label = 'Use Selected as Volume / Target Mesh', vis = False, c = 'selectExistVol()' , p = vml)
        
        cmds.rowLayout('defaultVolThicknessLyt', vis = False, nc = 2, p = vml)
        cmds.text(label = '                   Volume Percentage: ', p = 'defaultVolThicknessLyt')
        cmds.floatField('defaultThicknessField', v = 10, min = 0.1, pre = 1, step = .1, cc = 'defaultVolCreate()', enterCommand = 'defaultVolCreate()', p = 'defaultVolThicknessLyt')
        
        
#        cmds.floatFieldGrp('defaultVolText', label = 'Fur Thickness', vis = False, v1 = 1, p = vml)
        cmds.button('defaultVolBtn', label = 'Create Volume Mesh', c = 'defaultVolCreate()', vis = False, p = vml)
        cmds.button('cancelDefaultVolBtn', label = 'Cancel and Go Back', c = 'cancelDefaultVol()', vis = False, p = vml)
        cmds.button('confirmDefaultVolBtn', label = 'Confirm Volume Mesh', c = 'confirmDefaultVol()', vis = False, p = vml)
        cmds.button('smartVolSelBtn', label = 'Create Using Smart Volume Mesh', c = 'enterSmartVol()', vis = False, p = vml)
        smartVL = cmds.columnLayout('smartVolLayout', adj = True, vis = False, p = vml)
#        cmds.button('addBulge', label = 'Add Bulges', c = 'addBulge()',  p = smartVL)
                    
        cmds.button('paintBulge', label = 'Paint Bulges', c = 'paintBulge()',  p = smartVL)
                      
        cmds.button('bulgeOptionsBtn', label = 'Bulge Options', c = 'bulgeOptionsPress()', p = smartVL)
        
        cmds.frameLayout('bulgeOptionsFrame', label = 'Bulge Options', vis = False, cll = True, cl = False, cc = 'bulgeOptionsFrameCollapse()', p = smartVL)
        cmds.radioButtonGrp('mirrorAxisRadio', cw3 = [90,90,90], labelArray3 = ['X', 'Y', 'Z'], numberOfRadioButtons = 3,sl = 1, p = 'bulgeOptionsFrame')

        cmds.button('mirrorBtn', label = 'Mirror Selected Bulges', c = 'mirrorSelected()',p = 'bulgeOptionsFrame')
        cmds.button('addBulgeBtn', label = 'Add Bulges at Selected References', c = 'addBulgesAtReferences()', p = 'bulgeOptionsFrame') 
        cmds.rowLayout('bulgeSizeRowLayout', nc = 2, p = 'bulgeOptionsFrame')
        cmds.text(label = '                 Default Bulge Size: ', p = 'bulgeSizeRowLayout')
        cmds.floatField('defaultBulgeSize', v = 1.0, min = 0.001, pre = 2, step = .01, p = 'bulgeSizeRowLayout')

        
        cmds.checkBox('autoUpdateSmartVolChk', label = 'Auto Update Smart Volume Mesh', cc = 'autoUpdateSmartVol()', v = True, p = smartVL)
        cmds.button('createSmartVol', label = 'Update Volume Mesh', c = 'createSmartVol()', p = smartVL)
        cmds.button('smartVolCancelBtn', label = 'Cancel Smart Vol and Go Back', c = 'cancelSmartVol()', p = smartVL)
        cmds.button('smartVolConfirmBtn', label = 'Confirm Volume Mesh', c = 'confirmSmartVol()', p = smartVL)
        
        
        cmds.text('askDrawText', label = 'Select Mesh to Draw Curves' , p = 'askDrawMeshLayout')
            
#        cmds.radioButtonGrp('radioDrawMesh', cw2 = [125,125] , labelArray2 = ['Scalp Mesh', 'Volume Mesh'], numberOfRadioButtons = 2, on1 = 'drawScalpRadio()', on2 = 'drawVolRadio()', p = 'askDrawMeshLayout',sl = 1)
#        cmds.image('drawScalpIcon', i = iconPath + 'drawOnScalp.jpg', vis = False, p = 'askDrawMeshLayout')
#        cmds.image('drawVolIcon', i = iconPath + 'drawOnVol.jpg'vis = False, p = 'askDrawMeshLayout')
        
        cmds.iconTextRadioCollection( 'radioDrawMeshICON', p = 'askDrawMeshLayout')
        cmds.rowLayout('rl', nc = 2, p = 'askDrawMeshLayout')
        cmds.iconTextRadioButton('scalpMeshDrawICON', w = 125, h = 180, sl = True, i = iconPath + 'drawOnScalp.jpg', l = 'Scalp Mesh', style = 'iconAndTextVertical', p = 'rl')
        cmds.iconTextRadioButton('volMeshDrawICON', w = 125, h = 180, i = iconPath + 'drawOnVolume.jpg', l = 'Volume Mesh', style = 'iconAndTextVertical', p = 'rl')
        
        cmds.button('selectDrawMeshBtn', label = 'Confirm to Draw Curves on', c = 'drawMeshSelected()', p = 'askDrawMeshLayout')
    else:
        cmds.radioButtonGrp('volRadio1', edit = True, sl = 1, en = True)
        useExistVol()        
        
    
#    cmds.setParent(vml)
#    noUVGrid()

    
def useExistVol():
    
    stopGBUndo()
#    print 'exist'
    cmds.button('gbWin|gbMenuBar|cL0Layout|volumeMeshLT|selExistVolBtn', edit = True, vis = True)
    cmds.rowLayout('gbWin|gbMenuBar|cL0Layout|volumeMeshLT|defaultSmartRowLayout', edit = True, vis = False)            
#    cmds.radioButtonGrp('gbWin|gbMenuBar|cL0Layout|volumeMeshLT|createVolRadio', edit = True, vis = False)
    cmds.button('gbWin|gbMenuBar|cL0Layout|volumeMeshLT|smartVolSelBtn', edit = True, vis = False)
    cmds.rowLayout('gbWin|gbMenuBar|cL0Layout|volumeMeshLT|defaultVolThicknessLyt', edit = True, vis = False)        
#    cmds.floatFieldGrp('gbWin|gbMenuBar|cL0Layout|volumeMeshLT|defaultVolText', edit = True, vis = False)
    cmds.button('gbWin|gbMenuBar|cL0Layout|volumeMeshLT|defaultVolBtn', edit = True, vis = False)
    
    cmds.button('cancelDefaultVolBtn', edit = True, vis = False)
    cmds.button('confirmDefaultVolBtn',edit = True, vis = False)
    
    cmds.columnLayout('smartVolLayout', edit = True, vis = False)
    
    startGBUndo()

    
def createVol():
    stopGBUndo()
#    print 'create'
#    cmds.radioButtonGrp('gbWin|gbMenuBar|cL0Layout|volumeMeshLT|createVolRadio', edit = True, vis = True, en = True)
    cmds.rowLayout('gbWin|gbMenuBar|cL0Layout|volumeMeshLT|defaultSmartRowLayout', edit = True, vis = True, en = True)
    cmds.columnLayout('smartVolLayout', edit = True, vis = False)
    if cmds.iconTextRadioButton('defaultVolRadioIcon', q = True, select = True):
        defaultVol()
        
    if cmds.iconTextRadioButton('smartVolRadioIcon', q = True, select = True):
        smartVol()
        
    cmds.button('gbWin|gbMenuBar|cL0Layout|volumeMeshLT|selExistVolBtn', edit = True, vis = False)
    cmds.button('gbWin|gbMenuBar|cL0Layout|volumeMeshLT|defaultVolBtn', edit = True, vis = False)
    startGBUndo()

def defaultVol():
    
    stopGBUndo()
#    print 'default'
    currNode = cmds.getAttr('gbNode.currentGBNode')
    
    cmds.rowLayout('gbWin|gbMenuBar|cL0Layout|volumeMeshLT|defaultVolThicknessLyt', edit = True, vis = True)
    cmds.floatField('gbWin|gbMenuBar|cL0Layout|volumeMeshLT|defaultVolThicknessLyt|defaultThicknessField', e = True, v = 10.0)
    defaultVolCreate()
    previewDefaultVol()
#    cmds.image('gbWin|gbMenuBar|cL0Layout|volumeMeshLT|defaultVolImage', edit = True, vis = True)
#    cmds.image('gbWin|gbMenuBar|cL0Layout|volumeMeshLT|smartVolImage', edit = True, vis = False)
#    cmds.floatFieldGrp('gbWin|gbMenuBar|cL0Layout|volumeMeshLT|defaultVolText', edit = True, vis = True)
#    cmds.button('gbWin|gbMenuBar|cL0Layout|volumeMeshLT|defaultVolBtn', edit = True, vis = True)
    cmds.button('gbWin|gbMenuBar|cL0Layout|volumeMeshLT|smartVolSelBtn', edit = True, vis = False)
    cmds.setAttr(currNode + '.lastState', 'defaultVol', type = 'string')
    startGBUndo()

def selectExistVol():
    
    stopGBUndo()
    import cPickle as Pickle
    sel = cmds.ls(sl = True) 
    currNode = cmds.getAttr('gbNode.currentGBNode')  
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    match = False
    smoothNode = ''
    if len(sel) > 0:
        if not cmds.ls(cmds.listRelatives(sel[0], s = True), type = 'mesh'):
            reportGBMessage('No Poly Mesh Selected', True, True, 'red')
#            raise RuntimeError, 'No Poly Mesh Selected'
        elif(sel[0] == cmds.getAttr(currNode + '.scalpMesh')):
            reportGBMessage('That is the Scalp Mesh, Please select Volume Mesh', True, True, 'red')
#            print 'same as scalp'
#            raise RuntimeError, 'Thats the Scalp Mesh, Please select Volume Mesh'
        
        dupVolume = cmds.duplicate(sel[0], name = sel[0] + '_GB', rc = True, rr = True)[0]
        cmds.select(dupVolume, r = True)
        cmds.setAttr(sel[0] + '.visibility', False)
        
        sel[0] = dupVolume
        cmds.delete(sel[0], ch = True)
        cmds.makeIdentity(sel[0], apply = True)
#        allowedSmoothValuesString = cmds.getAttr(currNode + '.allowedSmoothValues')
#        allowedSmoothValues = []
#        if allowedSmoothValuesString:
        cmds.undoInfo(swf = False)
        if cmds.polyEvaluate(scalpMesh,v = True, f = True) == cmds.polyEvaluate(sel[0], v = True, f = True):
            cmds.polyTransfer(sel[0], uv = 1, ao = scalpMesh)
            cmds.delete(sel[0], ch = True)
            cmds.setAttr(currNode + '.currSmoothLevel', 0)
        
        else:
            currSmoothLevel = isSelectedMeshValid(sel[0])
            if currSmoothLevel == -1:
                cmds.undoInfo(swf = True)
                reportGBMessage('Selected Mesh Topology should match that of Scalp Mesh, or Smooth of Scalp Mesh (upto divisions = 2)', True, True, 'red')
#                raise RuntimeError, 'Selected Mesh Topology should match that of Scalp Mesh, or Smooth of Scalp Mesh (upto divisions = 2)'
            else:
                cmds.setAttr(currNode + '.currSmoothLevel', i)
                cmds.polyTransfer(sel[0], uv = 1, ao = scalpMesh)
                cmds.delete(sel[0], ch = True)
        
    else:
         reportGBMessage('Nothing Selected', True, True, 'red')       
#        raise RuntimeError, 'Nothing Selected'
            
    volMesh = sel[0]
    currNode = cmds.getAttr('gbNode.currentGBNode')
    cmds.setAttr(currNode + '.volumeMesh', volMesh, type = 'string')
    cmds.select(volMesh, cl = True)
    assignVolumeMeshShader(volMesh)
    
    if volMesh not in cmds.listRelatives(cmds.getAttr(currNode + '.mainGroup'),c = True):
        cmds.parent(volMesh, cmds.getAttr(currNode + '.mainGroup'))
    cmds.columnLayout('volumeMeshLT', edit = True, vis = False)
    
    cmds.columnLayout('askDrawMeshLayout', edit = True, vis = True)
    cmds.setAttr(currNode + '.lastState', 'askDraw', type = 'string')
    cmds.undoInfo(swf = True)
    
    startGBUndo()

def assignVolumeMeshShader(volumeMesh):
    
    shaderNames= getShaderNames()
    volumeShader = shaderNames[2]
    volumeShaderSG = shaderNames[3]
    
    if not cmds.objExists(volumeShader):
        cmds.shadingNode('lambert', name = volumeShader, asShader = True)
        cmds.setAttr(volumeShader + '.transparency', 0.75, 0.75, 0.75, type = 'double3')
        cmds.select(cl = True)
    if not cmds.objExists(volumeShaderSG):
        cmds.sets(name = volumeShaderSG, renderable = True,  noSurfaceShader = True)
        cmds.connectAttr(volumeShader + '.outColor', volumeShaderSG + '.surfaceShader', f = True)
    cmds.sets(volumeMesh, forceElement = volumeShaderSG)
    
    
def volumePercentByDistance(per,obj):
    
    bbox1 = cmds.xform(obj, q = True, bb = True)
    bbox2 = cmds.exactWorldBoundingBox(obj)
    if any(t == 0.0 for t in bbox1):
        bbox = bbox2
    elif any(t == 0.0 for t in bbox2):
        bbox = bbox1
    else:
        bbox = bbox1
    centerX = (bbox[3] - bbox[0])/2.0  + bbox[0]       
    centerZ = (bbox[5] - bbox[2])/2.0  + bbox[2]      
#    print 'BBB', bbox
#    dx = abs(bbox[0] - bbox[3])/2.0
    dy = abs(bbox[1] - bbox[4])/2.0
#    dz = abs(bbox[2] - bbox[5])/2.0
    
    scalpMesh = obj    
#    currNode = cmds.getAttr('gbNode.currentGBNode')
#    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    totalV = cmds.polyEvaluate(scalpMesh, v = True)
    if totalV < 100:
        max = 50
    else:        
        max = 100
    gap = int(round(totalV / max))
    
        
    pos = []
    if gap == 0:
        for i in range(0, totalV):
            pos.append(cmds.xform(scalpMesh + '.vtx[' + str(i) + ']', q = True, ws = True, t = True))
    else:        
        for i in range(0, totalV, gap):
            pos.append(cmds.xform(scalpMesh + '.vtx[' + str(i) + ']', q = True, ws = True, t = True))
#        print pos[-1]
    
#    print 'center', centerX, centerZ
    sumMinX = [x[0] for x in pos if x[0] < centerX]
    minX = sum(sumMinX)/float(len(sumMinX))
    
    sumMaxX = [x[0] for x in pos if x[0] > centerX]
    maxX = sum(sumMaxX)/float(len(sumMaxX))
    
    sumMinZ = [x[2] for x in pos if x[2] < centerZ]
    minZ = sum(sumMinZ)/float(len(sumMinZ))
    
    sumMaxZ = [x[2] for x in pos if x[2] > centerZ]
    maxZ = sum(sumMaxZ)/float(len(sumMaxZ))
    
       
    dx = abs(maxX - minX)/2.0
    dz = abs(maxZ - minZ)/2.0

    
    d = ((dx + dy + dz)/3) * (per/100.0)

    if d == 0.0:
        d = 0.0001
    
#    print 'minmax', minX, maxX, minZ, maxZ
    
#    print dx, dy, dz, d

    return d
    
def defaultVolCreate():
    
    stopGBUndo()
    currNode = cmds.getAttr('gbNode.currentGBNode')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')     
    cmds.undoInfo(swf = False)
    dispPer = cmds.floatField('gbWin|gbMenuBar|cL0Layout|volumeMeshLT|defaultVolThicknessLyt|defaultThicknessField', q = True, v = True)

    disp = volumePercentByDistance(dispPer,scalpMesh)
    
    currVol = cmds.getAttr(currNode + '.volumeMesh')
    if currVol is not None:
        if cmds.objExists(currVol):
            cmds.delete(currVol)
    
       
    volMesh = cmds.duplicate(scalpMesh, name = 'volumeMesh_' + cmds.getAttr(currNode + '.scalpMesh'),rr = True)[0]
    cmds.select(cl = True)
    
    handleToolSettings()
    
    cmds.setAttr(volMesh + '.visibility', False)
    whichMode = ''
    tempDup = cmds.duplicate(scalpMesh, name = 'tempDup', rr = True)[0]
    cmds.select(tempDup, r = True)
    bbY1 = cmds.exactWorldBoundingBox(tempDup)[4]
    bbZ1 = cmds.exactWorldBoundingBox(tempDup)[5]
    mm.eval('artPuttyToolScript 3;')
    mm.eval('resetTool artPuttyContext;')
    cmds.artPuttyCtx('artPuttyContext', e = True, mtm = 'pull', sao = 'additive')
    mm.eval('artPuttyCtx -e -maxdisp ' + str(disp) + '`currentCtx`;')
    mm.eval('artPuttyCtx -e -clear `currentCtx`;')
    cmds.setToolTo('selectSuperContext')
    bbY2 = cmds.exactWorldBoundingBox(tempDup)[4]
    bbZ2 = cmds.exactWorldBoundingBox(tempDup)[5]
#    print bbY2, bbY1

    if bbZ2 > bbZ1:
        whichMode = 'pull'
#        print 'pull'
    else:
        whichMode = 'push'
#        print 'push'
    cmds.delete(tempDup)
#    whichMode = 'pull'
    cmds.select(volMesh, r = True)
    mm.eval('artPuttyToolScript 3;')
    mm.eval('resetTool artPuttyContext;')
    cmds.artPuttyCtx('artPuttyContext', e = True, sao = 'additive', mtm = whichMode)
    mm.eval('artPuttyCtx -e -maxdisp ' + str(disp) + '`currentCtx`;')
    mm.eval('artPuttyCtx -e -clear `currentCtx`;')
    cmds.setToolTo('selectSuperContext')

    cmds.button('cancelDefaultVolBtn', edit = True, vis = True)
    cmds.button('confirmDefaultVolBtn', edit = True, vis = True)
    cmds.radioButtonGrp('volRadio1', edit = True, en = False)
#    cmds.radioButtonGrp('createVolRadio', edit = True, en = False)
    cmds.rowLayout('gbWin|gbMenuBar|cL0Layout|volumeMeshLT|defaultSmartRowLayout', edit = True, en = False)
    cmds.setAttr(currNode + '.volumeMesh', volMesh , type = 'string')
    cmds.setAttr(volMesh + '.visibility', True)
    loc = cmds.toolPropertyWindow(q = True, loc = True)
    if loc:
        mm.eval('ToggleToolSettings;')
    assignVolumeMeshShader(volMesh)
    setVolMeshReference()
    cmds.select(volMesh, cl = True)
    
#    cmds.undoInfo(swf = True)
    startGBUndo()

def previewDefaultVol():
    
#    cmds.button('cancelDefaultVolBtn', edit = True, vis = False)
#    cmds.button('confirmDefaultVolBtn', edit = True, vis = False)
    cmds.radioButtonGrp('volRadio1', edit = True, en = True)
    cmds.rowLayout('gbWin|gbMenuBar|cL0Layout|volumeMeshLT|defaultSmartRowLayout', edit = True, en = True)
    
def handleToolSettings():
    
    
    defaultDocks = ['Channel Box', 'Channel Box / Layer Editor' , 'Layer Editor', 'Attribute Editor']
    dockControls = cmds.lsUI(type = 'dockControl')
    if not dockControls:
        return
    for dc in dockControls:
        if cmds.dockControl(dc, q = True, label = True) == 'Tool Settings':
            if not cmds.dockControl(dc, q = True, fl = True):
#                print 'docked'
                cmds.dockControl(dc, edit = True, fl = True, vis = False)
                for each in dockControls:
                    if cmds.dockControl(each, q = True, label = True) in defaultDocks:
                        cmds.dockControl(each, edit = True, vis = False)
            cmds.dockControl(dc, edit = True, vis = False)
            

def cancelDefaultVol():
    
    stopGBUndo()
    cmds.undoInfo(swf = False)
    cmds.radioButtonGrp('volRadio1', edit = True, en = True)
#    cmds.radioButtonGrp('createVolRadio', edit = True, en = True)
    cmds.rowLayout('gbWin|gbMenuBar|cL0Layout|volumeMeshLT|defaultSmartRowLayout', edit = True, en = True)
    cmds.button('cancelDefaultVolBtn', edit = True, vis = False)
    cmds.button('confirmDefaultVolBtn', edit = True, vis = False)
    cmds.rowLayout('gbWin|gbMenuBar|cL0Layout|volumeMeshLT|defaultVolThicknessLyt',edit = True, vis = False)
#    cmds.floatFieldGrp('gbWin|gbMenuBar|cL0Layout|volumeMeshLT|defaultVolText', edit = True, vis = False)
    cmds.button('gbWin|gbMenuBar|cL0Layout|volumeMeshLT|selExistVolBtn', edit = True, vis = False)
    cmds.button('gbWin|gbMenuBar|cL0Layout|volumeMeshLT|defaultVolBtn', edit = True, vis = False)
    currNode = cmds.getAttr('gbNode.currentGBNode')
    cmds.delete(cmds.getAttr(currNode + '.volumeMesh'))
    cmds.setAttr(currNode + '.volumeMesh','',type = 'string')
    cmds.undoInfo(swf = True)
    startGBUndo()
    
def confirmDefaultVol():
    
    stopGBUndo()
    cmds.undoInfo(swf = False)
#    cmds.columnLayout('volumeMeshLT', edit = True, vis = False)
#    cmds.columnLayout('cL1Layout', edit = True, vis = True)
    cmds.columnLayout('volumeMeshLT', edit = True, vis = False)
    cmds.columnLayout('askDrawMeshLayout', edit = True, vis = True)
    currNode = cmds.getAttr('gbNode.currentGBNode')
    cmds.setAttr(currNode + '.lastState', 'askDraw', type = 'string')
    cmds.setAttr(currNode + '.currSmoothLevel', 0)
#    noUVGrid()
#    currNode = cmds.getAttr('gbNode.currentGBNode')
#    cmds.setAttr(currNode + '.lastState', 'onChar', type = 'string')
    cmds.undoInfo(swf = True)
    startGBUndo()
      
    
def smartVol():
#    print 'smart'
    cmds.rowLayout('gbWin|gbMenuBar|cL0Layout|volumeMeshLT|defaultVolThicknessLyt',edit = True, vis = False)
    
#    cmds.floatFieldGrp('gbWin|gbMenuBar|cL0Layout|volumeMeshLT|defaultVolText', edit = True, vis = False)
    cmds.button('gbWin|gbMenuBar|cL0Layout|volumeMeshLT|selExistVolBtn', edit = True, vis = False)
    cmds.button('gbWin|gbMenuBar|cL0Layout|volumeMeshLT|defaultVolBtn', edit = True, vis = False)
    cmds.button('gbWin|gbMenuBar|cL0Layout|volumeMeshLT|smartVolSelBtn', edit = True, vis = True)
#    cmds.image('gbWin|gbMenuBar|cL0Layout|volumeMeshLT|defaultVolImage', edit = True, vis = False)
#    cmds.image('gbWin|gbMenuBar|cL0Layout|volumeMeshLT|smartVolImage', edit = True, vis = True)
    cmds.button('cancelDefaultVolBtn', edit = True, vis = False)
    cmds.button('confirmDefaultVolBtn', edit = True, vis = False)
    refreshVolMeshCreation()
    
    currNode = cmds.getAttr('gbNode.currentGBNode')
    cmds.setAttr(currNode + '.lastState', 'smartVol', type = 'string')

def refreshVolMeshCreation():
    
    currNode = cmds.getAttr('gbNode.currentGBNode')
    volumeMesh = cmds.getAttr(currNode + '.volumeMesh')
    if volumeMesh:
        cmds.setAttr(currNode + '.volumeMesh', '', type = 'string')
        if cmds.objExists(volumeMesh):
            cmds.delete(volumeMesh)
            
def enterSmartVol():
    cmds.radioButtonGrp('volRadio1', edit = True, en = False)
#    cmds.radioButtonGrp('createVolRadio', edit = True, en = False)
    cmds.rowLayout('gbWin|gbMenuBar|cL0Layout|volumeMeshLT|defaultSmartRowLayout', edit = True, en = False)
    cmds.columnLayout('smartVolLayout', edit = True, vis = True)
    cmds.button('gbWin|gbMenuBar|cL0Layout|volumeMeshLT|smartVolSelBtn', edit = True, vis = False)
    currNode = cmds.getAttr('gbNode.currentGBNode')
#    createSMVNode()
    cmds.setAttr(currNode + '.lastState', 'smartVol', type = 'string')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    cmds.setAttr(scalpMesh + '.visibility', False)
    if not cmds.objExists('smartVolMesh_' + scalpMesh):
        cmds.button('gbWin|gbMenuBar|cL0Layout|volumeMeshLT|smartVolLayout|smartVolConfirmBtn', edit = True, vis = False)
    
    smartVolGrp = 'smartVolumeGrp_' + scalpMesh
    bulgeGrp = 'bulges_' + scalpMesh

    if not cmds.objExists(smartVolGrp):
        cmds.group(name = smartVolGrp, em = True)
        cmds.addAttr(smartVolGrp, ln = 'usedBulges', dt = 'string')
        dupScalp = cmds.duplicate(scalpMesh, name = scalpMesh + '_dupScalp',rr = True)
        cmds.parent(dupScalp,smartVolGrp)
        cmds.group(name = bulgeGrp, em = True, parent = smartVolGrp)
        cmds.setAttr(scalpMesh + '.visibility', False)
        cmds.setAttr(dupScalp[0] + '.visibility', True)
        
        
def addBulge():
    
    historyDelete = []
    
    faceList = []
    sel = cmds.ls(sl = True, fl = True, st = True)
    selFaceOnly = cmds.ls(sl = True, fl = True)
    currNode = cmds.getAttr('gbNode.currentGBNode')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    
    if not len(sel):
#        print 'zero'
        reportGBMessage('No Poly Faces Selected', True, True, 'red')
#        raise RuntimeError, 'No Poly Faces Selected'
    

    
    
    for s in range(0,len(sel),2):
#        print s
        a = sel[s].split('.')[0]
        b = sel[s+1]
#        print a,b
        if a == (scalpMesh + '_dupScalp') and b == 'float3':
            faceList.append(sel[s])
        if len(sel) == 2:
            break

    if not len(faceList):
        reportGBMessage('No Poly Faces Selected', True, True, 'red')
#        print sel
#        raise RuntimeError, 'No Poly Faces Selected'
    
    charCPNode = createCPNode(scalpMesh)
    historyDelete.append(charCPNode)    
    
#    charCPNode = cmds.getAttr(currNode + '.scalpMeshCPNode')
#    scalpFoll = cmds.getAttr(currNode + '.scalpMeshFollicle')

    scalpFoll = createFollicle('scalpMesh')
    historyDelete.append(scalpFoll)
    
    scalpFollShp = cmds.listRelatives(scalpFoll, s = True)[0]

    smartVolGrp = 'smartVolumeGrp_' + scalpMesh
    bulgeGrp = 'bulges_' + scalpMesh
    if not cmds.objExists(bulgeGrp):
        cmds.group(name = bulgeGrp, em = True, parent = smartVolGrp)
        
    if not cmds.objExists(smartVolGrp):
        cmds.group(name = smartVolGrp, em = True)
#        cmds.addAttr(smartVolGrp, ln = 'usedBulges', dt = 'string')
        dupScalp = cmds.duplicate(scalpMesh, rr = True, name = scalpMesh + '_dupScalp')
        cmds.parent(dupScalp,smartVolGrp)
        cmds.group(name = bulgeGrp, em = True, parent = smartVolGrp)

    if 'artSelectC' or 'selectSuperContext' in cmds.currentCtx():
        posF = []
        posF4 = cmds.xform(selFaceOnly, q = True, ws = True, t = True)
        for i in range(0,3):
            posF.append(0)
            for j in range(i,len(posF4),3):
                posF[i] = posF[i] + (posF4[j]/(len(posF4)/3))
        cmds.setAttr(charCPNode + '.ip', posF[0], posF[1], posF[2])
        cpFace = scalpMesh + '_dupScalp' + '.f[' + str(cmds.getAttr(charCPNode + '.f')) + ']'
        del faceList[:]
        faceList.append(cpFace)
        
    bulge = createTemplateBulge()
    posF = []
    for face in faceList:
        faceID = face.split('[')[1].split(']')[0]
        bulgeName = scalpMesh + '_bulge_' + str(faceID)
        bulgeJoint = scalpMesh + '_bulgeJoint_' + str(faceID)
        if cmds.objExists(bulgeName):
            continue
        posF = []
        posF4 = cmds.xform(face, q = True, ws = True, t = True)
        for i in range(0,3):
            posF.append(0)
            for j in range(i,len(posF4),3):
                posF[i] = posF[i] + (posF4[j]/(len(posF4)/3))
#        cmds.select(cl = True)
#        bj = cmds.joint(p = (posF[0], posF[1], posF[2]), name = bulgeJoint)
#        cmds.parent(bj, bulgeJointGrp)
        cmds.setAttr(charCPNode + '.ip', posF[0], posF[1], posF[2])
#        uValue = cmds.getAttr(charCPNode + '.u')        
#        vValue = cmds.getAttr(charCPNode + '.v')
#        print uValue
#        print vValue
        cmds.setAttr(scalpFollShp + '.parameterU', cmds.getAttr(charCPNode + '.u'))
        cmds.setAttr(scalpFollShp + '.parameterV', cmds.getAttr(charCPNode + '.v'))
        
#        cmds.setAttr(scalpFollShp + '.parameterU', .25)
#        cmds.setAttr(scalpFollShp + '.parameterV', .25)
            
        bulgeDup = cmds.duplicate(bulge, name =  bulgeName, rr = True)[0]
        pc = cmds.parentConstraint(scalpFoll, bulgeDup)
        cmds.delete(pc)
        cmds.parent(bulgeDup, bulgeGrp)
        defaultBulgeScale = cmds.floatField('defaultBulgeSize', q = True, v = True)
        cmds.scale( defaultBulgeScale, defaultBulgeScale, defaultBulgeScale,bulgeDup, xyz = True, a = True)
        
            
#        cmds.setAttr(bulgeDup + '.prevScale', 1.0)
    
    cmds.delete(bulge)
    cmds.scriptJob(ac = [bulgeDup + '.scaleZ', 'createSmartVol(\'auto\')'])
    for h in historyDelete:
        if cmds.objExists(h):
            cmds.delete(h)       

    bulgeGrpChildren = cmds.listRelatives(bulgeGrp, c = True)
    if len(bulgeGrpChildren) > 3:
#        print 'here'
        if cmds.checkBox('autoUpdateSmartVolChk', q = True, v = True):
            createSmartVol()
#        print 'aaa'

        cmds.select(scalpMesh + '_dupScalp', r = True)
        cmds.setToolTo('artSelectContext')
        cmds.evalDeferred('paintBulge()')


def paintBulge():
    
#    print 'enter paint bulge'
    currNode = cmds.getAttr('gbNode.currentGBNode')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    smartVolGrp = 'smartVolumeGrp_' + scalpMesh
    smartVolMesh = 'smartVolMesh_' + scalpMesh
    if cmds.objExists(smartVolMesh):
        if smartVolGrp in cmds.listRelatives(smartVolMesh, p = True):
            cmds.setAttr(smartVolMesh + '.visibility', True)
    cmds.setAttr(scalpMesh + '.visibility', False)
    cmds.select(scalpMesh + '_dupScalp', r = True)
    cmds.softSelect(edit = True, sse = 0)    

    
    cmds.setToolTo('artSelectContext')
    loc = cmds.toolPropertyWindow(q = True, loc = True)
    if loc:
        mm.eval('ToggleToolSettings;')
    cmds.resetTool(cmds.currentCtx())
    mm.eval('setComponentPickMask ' + dQ + 'Facet' + dQ + ' true;')
    fieldLayout = 'MayaWindow|MainToolSettingsLayout|tabLayout1|artSelect|artSelectStrokeFrame|columnLayout4|columnLayout5'
    if cmds.columnLayout(fieldLayout, q = True, exists = True):
        cmds.columnLayout(fieldLayout, e = True, vis = False)
    cmds.artSelectCtx('artSelectContext', e = True, asc = 'python('+ dQ + 'addBulge()'+ dQ + ');')
    cmds.artSelectCtx('artSelectContext', e = True, addselection = False)
    cmds.scriptJob( e = ['ToolChanged','resetArtSelectTool()'], runOnce = True)
    loc = cmds.toolPropertyWindow(q = True, loc = True)
    if loc:
        mm.eval('ToggleToolSettings;')

#    print '>>>>>', cmds.currentCtx()
    
def resetArtSelectTool():
    
#    print 'RESET TOOL'
#    if not cmds.currentCtx() == 'artSelectContext':
#        cmds.setToolTo('artSelectContext')
    cmds.artSelectCtx('artSelectContext', e = True, asc = '')
    fieldLayout = 'MayaWindow|MainToolSettingsLayout|tabLayout1|artSelect|artSelectStrokeFrame|columnLayout4|columnLayout5'
    if cmds.columnLayout(fieldLayout, q = True, exists = True):
        cmds.columnLayout(fieldLayout, e = True, vis = True)

    cmds.resetTool( 'artSelectContext' )

    cmds.setToolTo('selectSuperContext')
    mm.eval('changeSelectMode -object')
    
def paintBulgeOnFace():
    
    currNode = cmds.getAttr('gbNode.currentGBNode')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    selList = []
    selList = cmds.ls(sl = True, fl = True)
    if not selList:
        return
    else:
        selFirstItem = selList[0]
        if not selFirstItem.split['.f['][0] == scalpMesh:
            return
        else:
            posF = []
            posF4 = cmds.xform(selList, q = True, ws = True, t = True)
            for i in range(0,3):
                posF.append(0)
                for j in range(i,len(posF4),3):
                    posF[i] = posF[i] + (posF4[j]/(len(posF4)/3))
                    
def createTemplateBulge():

    bulge = cmds.polySphere(sx = 8, sy = 8)[0]
    assignBulgeShader(bulge)
    cmds.rotate('90deg',  bulge, x = True)
    cmds.delete(bulge + '.f[0:23]', bulge + '.f[48:55]')
    cmds.displaySmoothness(bulge, divisionsU = 3, divisionsV = 3, pointsWire = 16, pointsShaded = 4, polygonObject = 3)
    cmds.makeIdentity(bulge, apply = True)

    return bulge
    
def assignBulgeShader(bulge):
    
    bulgeShader = 'gbBulgeShader'
    bulgeShaderSG = 'gbBulgeShaderSG'
    if not cmds.objExists(bulgeShader):
        cmds.shadingNode('lambert', name = bulgeShader, asShader = True)
        cmds.setAttr(bulgeShader + '.color', 1,0,0, type = 'double3')
        cmds.select(cl = True)
    if not cmds.objExists(bulgeShaderSG):
        cmds.sets(name = bulgeShaderSG, renderable = True,  noSurfaceShader = True)
        cmds.connectAttr(bulgeShader + '.outColor', bulgeShaderSG + '.surfaceShader', f = True)
    cmds.sets(bulge, forceElement = bulgeShaderSG)        
    
def addBulgesAtReferences():
    
    historyDelete = []
    currNode = cmds.getAttr('gbNode.currentGBNode')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    selection = cmds.ls(sl = True)
    selWithType = cmds.ls(sl = True,st = True)
    if not selection:
        reportGBMessage('Please select Reference Bulges or Objects Closer to Character', True, True, 'red')
    
    charCPNode = createCPNode(scalpMesh)         
    historyDelete.append(charCPNode)    
    
    locator = cmds.spaceLocator()[0]
    historyDelete.append(locator)    
    
    scalpFoll = createFollicle('scalpMesh')
    historyDelete.append(scalpFoll)
    scalpFollShp = cmds.listRelatives(scalpFoll, s = True)[0]
    cmds.select(cl = True)
    
    smartVolGrp = 'smartVolumeGrp_' + scalpMesh
    bulgeGrp = 'bulges_' + scalpMesh
    if not cmds.objExists(bulgeGrp):
        cmds.group(name = bulgeGrp, em = True, parent = smartVolGrp)
        
    if not cmds.objExists(smartVolGrp):
        cmds.group(name = smartVolGrp, em = True)
#        cmds.addAttr(smartVolGrp, ln = 'usedBulges', dt = 'string')
        dupScalp = cmds.duplicate(scalpMesh, rr = True, name = scalpMesh + '_dupScalp')
        cmds.parent(dupScalp,smartVolGrp)
        cmds.group(name = bulgeGrp, em = True, parent = smartVolGrp)
    
    
    for obj in selection:
        showType = cmds.ls(obj, st = True)
        if showType[1] == 'float3' and scalpMesh + '_dupScalp' in obj:
            cmds.select(obj,r = True)
            addBulge()
        else:       
            scaleZ = cmds.floatField('defaultBulgeSize', q = True, v = True)     

            if cmds.objectType(relatives[0], isType='mesh'):
                check = isValidBulge(obj)
                if check:
                    scaleZ = check
            
            pc = cmds.pointConstraint(obj, locator, mo = 0)
            cmds.delete(pc)
            locPos = cmds.xform(locator, q = True, ws = True, t = True)
            cmds.setAttr(charCPNode + '.ip', locPos[0], locPos[1], locPos[2])
            faceID = cmds.getAttr(charCPNode + '.f')
            cpFace = scalpMesh + '_dupScalp' + '.f[' + str(faceID) + ']'
            bulgeName = scalpMesh + '_bulge_' + str(faceID)
            if cmds.objExists(bulgeName):
                continue
            cmds.setAttr(scalpFollShp + '.parameterU', cmds.getAttr(charCPNode + '.u'))
            cmds.setAttr(scalpFollShp + '.parameterV', cmds.getAttr(charCPNode + '.v'))

            bulge = createTemplateBulge()
            bulgeDup = cmds.duplicate(bulge, name =  bulgeName, rr = True)[0]
            
            pc = cmds.parentConstraint(scalpFoll, bulgeDup)
            cmds.delete(pc)
            cmds.parent(bulgeDup, bulgeGrp)
            
            cmds.scale( scaleZ, scaleZ, scaleZ,bulgeDup, xyz = True, a = True)
            
            cmds.delete(bulge)
            cmds.scriptJob(ac = [bulgeDup + '.scaleZ', 'createSmartVol(\'auto\')'])
            
    
    for h in historyDelete:
        if cmds.objExists(h):
            cmds.delete(h)       
    

    bulgeGrpChildren = cmds.listRelatives(bulgeGrp, c = True)
    if len(bulgeGrpChildren) > 3:
        if cmds.checkBox('autoUpdateSmartVolChk', q = True, v = True):
            createSmartVol()            
            
                                
            
                    

def isValidBulge(obj):
    
    valid = {'uvcoord': 44, 'edge': 64, 'vertex': 33, 'face': 32}
    
    if cmds.polyEvaluate(obj, v = True, e = True, f = True, uv = True) == valid and 'bulge' in obj:
        scaleZ = cmds.getAttr(obj + '.scaleZ')
        return scaleZ
    else:
        return False        
    
def bulgeOptionsPress():
    cmds.button('bulgeOptionsBtn', edit = True, vis = False)
    cmds.frameLayout('bulgeOptionsFrame', edit = True, vis = True)
    cmds.frameLayout('bulgeOptionsFrame', edit = True, cl = False)

    
def bulgeOptionsFrameCollapse():
    cmds.button('bulgeOptionsBtn', edit = True, vis = True)
    cmds.frameLayout('bulgeOptionsFrame', edit = True, vis = False)

def mirrorSelected():
    
    historyDelete = []
    axisID = cmds.radioButtonGrp('mirrorAxisRadio', q = True, sl = True)
    mirrorDict = {1:'X', 2:'Y', 3:'Z'}
    axis = mirrorDict[axisID]
    
    selObj = cmds.ls(sl = True)
    
    currNode = cmds.getAttr('gbNode.currentGBNode')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    
    charCPNode = createCPNode(scalpMesh)
    historyDelete.append(charCPNode)
#    charCPNode = cmds.getAttr(currNode + '.scalpMeshCPNode')
    center = cmds.objectCenter(scalpMesh, gl = True)

    bulgeObj = [s for s in selObj if scalpMesh + '_bulge_' in s]
    if not bulgeObj:
        reportGBMessage('No Bulges Selected', True, True, 'red')
#        raise RuntimeError, 'Select Bulges'
    tempMirrorScalpDup = scalpMesh + '_MirrorDup'
    tempMirrorGrp = scalpMesh + '_MirrorGrp'
    if cmds.objExists(tempMirrorScalpDup):
        cmds.delete(tempMirrorScalpDup)
    else:
        cmds.duplicate(scalpMesh, name = tempMirrorScalpDup, rr = True)
    if cmds.objExists(tempMirrorGrp):
        cmds.delete(tempMirrorGrp)
    else:
        cmds.group(tempMirrorScalpDup, name = tempMirrorGrp)
        
    cmds.delete(tempMirrorScalpDup)
    cmds.xform(tempMirrorGrp, cp = True)
    
    for bulge in bulgeObj:
        bulgeDup = cmds.duplicate(bulge, name = bulge + '_DUP', rr = True)
        cmds.select(cl = True)
        cmds.parent(bulgeDup, tempMirrorGrp)

    command = 'scale -a -1 -1 -1 -scale' + axis + ' ' + tempMirrorGrp
    mm.eval(command)
    
    newBulge = cmds.listRelatives(tempMirrorGrp, c = True)
    for bulge in newBulge:
#        print bulge
        bPos = cmds.xform(bulge, q = True, ws = True, t = True)
        cmds.setAttr(charCPNode + '.ip', bPos[0], bPos[1], bPos[2])
        face = cmds.getAttr(charCPNode + '.f')
#        print face
        newBulgeName = scalpMesh + '_bulge_' + str(face)
        if cmds.objExists(newBulgeName):
            cmds.delete(newBulgeName)
        cmds.rename(bulge, newBulgeName)
        cmds.parent(newBulgeName, 'bulges_' + scalpMesh)
        cmds.scriptJob(ac = [newBulgeName + '.scaleZ', 'createSmartVol(\'auto\')'])
    cmds.delete(tempMirrorGrp)
    cmds.delete(historyDelete)
    bulgeGrpChildren = cmds.listRelatives('bulges_' + scalpMesh)
    if len(bulgeGrpChildren) > 3:
        if cmds.checkBox('autoUpdateSmartVolChk',q = True, v = True):
            createSmartVol()

    for h in historyDelete:
        if cmds.objExists(h):
            cmds.delete(h)        

    cmds.select(selObj, r = True)
        

def cancelSmartVol():
    cmds.radioButtonGrp('volRadio1', edit = True, en = True)
#    cmds.radioButtonGrp('createVolRadio', edit = True, en = True)
    cmds.rowLayout('gbWin|gbMenuBar|cL0Layout|volumeMeshLT|defaultSmartRowLayout', edit = True, en = True)
    cmds.button('gbWin|gbMenuBar|cL0Layout|volumeMeshLT|smartVolSelBtn', edit = True, en = True, vis = True)
    
    cmds.columnLayout('smartVolLayout', edit = True, vis = False)
    currNode = cmds.getAttr('gbNode.currentGBNode')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    if cmds.objExists('smartVolumeGrp_' + scalpMesh):
        cmds.delete('smartVolumeGrp_' + scalpMesh)
    cmds.setAttr(scalpMesh + '.visibility', True)
    allJobs = cmds.scriptJob(lj = True)
    for job in allJobs:
        if 'createSmartVol' in job:
            cmds.scriptJob(kill = int(job.split(':')[0]))
            
def createSmartVol(mode = 'manual'):
    
    import os
    if mode == 'auto':
#        print 'first'
        if not cmds.checkBox('autoUpdateSmartVolChk', q = True, v = True):
#            print 'seconds'
            return
    historyDelete = []
    targetsAdded = []
    ctx = cmds.currentCtx()
    currNode = cmds.getAttr('gbNode.currentGBNode')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    smartVolBase = scalpMesh + '_dupScalp'
    if cmds.objExists(smartVolBase):
        smartVolBaseShp = cmds.listRelatives(smartVolBase, s = True)
    
    bulgeGrp = 'bulges_' + scalpMesh
    smartVolGrp = 'smartVolumeGrp_' + scalpMesh
    smartVolMesh = 'smartVolMesh_' + scalpMesh
    
    if not cmds.objExists(bulgeGrp):
        reportGBMessage('Please Add at least 3 Bulges', True, True, 'red')                
#        raise RuntimeError, 'Please Add at least 3 Bulges'

    bulges = cmds.listRelatives(bulgeGrp, c = True)
    if len(bulges) < 3:
        reportGBMessage('Please Add at least 3 Bulges', True, True, 'red')  
#        raise RuntimeError, 'Please Add at least 3 Bulges'
    
    cmds.undoInfo(swf = False)
    currentBulgesTmp = bulges
    
    bulgeTargetGrp = 'targets_smartVolume_' + scalpMesh
    historyDelete.append(bulgeTargetGrp)
    if not cmds.objExists(bulgeTargetGrp):
#        print 'entered'
        cmds.group(name = bulgeTargetGrp, em = True, parent = smartVolGrp)
        cmds.setAttr(bulgeTargetGrp + '.visibility', False)
    
    bulgeJointGrp = 'bulgeJoints_' + scalpMesh
    historyDelete.append(bulgeJointGrp)
    
    if not cmds.objExists(bulgeJointGrp):
        cmds.group(name = bulgeJointGrp, em = True, parent = smartVolGrp)
        cmds.setAttr(bulgeJointGrp + '.visibility', False)
    
    if not cmds.objExists(smartVolMesh):
        smartVolMesh = cmds.duplicate(smartVolBase, name = smartVolMesh, rr = True)[0]

    smartVolMeshShp = cmds.listRelatives(smartVolMesh, s = True)
    cmds.button('gbWin|gbMenuBar|cL0Layout|volumeMeshLT|smartVolLayout|smartVolConfirmBtn', edit = True, vis = True)
    cmds.setAttr(smartVolMesh + '.visibility', False)
    
    smartVolBSList = cmds.listConnections(cmds.listRelatives(smartVolMesh, s = True)[0], type = 'blendShape')
    if smartVolBSList:
        cmds.delete(smartVolBSList)
    
    smartVolBS = cmds.blendShape(smartVolMesh, name = 'smartVolBS_' + scalpMesh, origin = 'world')[0]
#    historyDelete.append(smartVolBS)
    cmds.setAttr(smartVolBS + '.envelope', 0)
    if cmds.objExists(bulgeGrp):
        currentBulges = cmds.listRelatives(bulgeGrp, c = True)
    
    handleToolSettings()    
    totalTargets = 0
    whichMode = ''
    for bulge in currentBulges:
        
        faceID = bulge.split(scalpMesh + '_bulge_')[1]
        bulgeJoint = scalpMesh + '_bulgeJoint_' + str(faceID)
        facePos = cmds.xform(bulge, q = True, ws = True, t = True)
        cmds.select(cl = True)
        if cmds.objExists(bulgeJoint):
            cmds.delete(bulgeJoint)
        cmds.joint(p = (facePos[0], facePos[1], facePos[2]), name = bulgeJoint)
        
        cmds.parent(bulgeJoint, bulgeJointGrp)
        bulgeTarget = 'bulgeTarget_' + bulge
        
        if cmds.objExists(bulgeTarget):
            cmds.delete(bulgeTarget)
        bulgeTarget = cmds.duplicate(smartVolBase, name = bulgeTarget, rr = True)[0]
        
        if whichMode == '':
            tempDup = cmds.duplicate(smartVolBase, name = 'tempDup', rr = True)[0]
            cmds.select(tempDup, r = True)
            bbY1 = cmds.exactWorldBoundingBox(tempDup)[5]
            mm.eval('artPuttyToolScript 3;')
            mm.eval('resetTool artPuttyContext;')
            cmds.artPuttyCtx('artPuttyContext', e = True, mtm = 'pull', sao = 'additive')
            mm.eval('artPuttyCtx -e -maxdisp ' + str(abs(cmds.getAttr(bulge + '.scaleZ'))) + '`currentCtx`;')
            mm.eval('artPuttyCtx -e -clear `currentCtx`;')
            cmds.setToolTo('selectSuperContext')
            bbY2 = cmds.exactWorldBoundingBox(tempDup)[5]
#            print bbY2, bbY1

            if bbY2 > bbY1:
                whichMode = 'pull'
            else:
                whichMode = 'push'

            cmds.delete(tempDup)
            
        cmds.setAttr(bulgeTarget + '.visibility', False)
        cmds.parent(bulgeTarget, bulgeTargetGrp)
        cmds.select(bulgeTarget, r = True)
        mm.eval('artPuttyToolScript 3;')
        mm.eval('resetTool artPuttyContext;')
        cmds.artPuttyCtx('artPuttyContext', e = True, sao = 'additive', mtm = whichMode)
        mm.eval('artPuttyCtx -e -maxdisp ' + str(abs(cmds.getAttr(bulge + '.scaleZ'))) + '`currentCtx`;')
        mm.eval('artPuttyCtx -e -clear `currentCtx`;')
        cmds.setToolTo('selectSuperContext')
        cmds.blendShape(smartVolBS, edit = True, t = (smartVolMesh, totalTargets, bulgeTarget, 1.0))
        cmds.setAttr(smartVolBS + '.' + bulgeTarget, 1.0)
        targetsAdded.append(totalTargets)
        totalTargets = totalTargets + 1


    clustName = mm.eval('findRelatedSkinCluster(' + dQ + smartVolBase + dQ + ');')
    if clustName:
        cmds.skinCluster(clustName, edit = True, ub = True)
    tempGBNode = cmds.getAttr('gbNode.tempGBNode')   
    jointList = cmds.listRelatives(bulgeJointGrp, c = True)
    cmds.select(jointList, smartVolBase)
    clustName = cmds.skinCluster(name = tempGBNode, dr = 10.0, mi = 4, omi = False, tsb = True, sm = 0 )[0]
#    historyDelete.append(clustName)
    cmds.select(smartVolBase, r = True)
    yldSkin(smartVolBase, jointList, [])
    
#    totalV = cmds.polyEvaluate(smartVolBase, v = True)
#    skinPer = []
#    for v in range(totalV):
#        vtx = smartVolBase + '.vtx[' + str(v) + ']'
#        skinPer = cmds.skinPercent( clustName, vtx, v = True, q = True)
#        for z in range(0, len(skinPer)):
#            cmds.setAttr(smartVolBS+ '.inputTarget[0].inputTargetGroup[' + str(z) + '].targetWeights[' + str(v) + ']', skinPer[z])
     
    projPath = cmds.workspace(q = True, rd  = True)
    tmpPath = os.path.normpath(projPath)
    tmpFile = 'tempGBFile.xml'
    tmpPathN = tmpPath + tmpFile
    
    jList = cmds.skinCluster(tempGBNode, q = True, inf = True)
    bList = cmds.blendShape(smartVolBS, q = True, target = True)
    
    for j in range(len(jList)):
        id = '_' + jList[j].split('_')[-1]
        for b in range(len(bList)):
            if id in bList[b]:
                cmds.rename(jList[j], bList[b])
        
        
    cmds.deformerWeights (tmpFile, path = projPath, ex = True, deformer = tempGBNode)
#    print('\n')
    cmds.deformerWeights(tmpFile, path = projPath,  im = True, method = 'index', deformer = smartVolBS)        
    
    gbos = cmds.about(os = True)
    plus = '\\'
    if gbos == 'nt' or gbos == 'win64':
        plus = '\\'
    else:
        plus = '/'
    
    toRemove = tmpPath + plus + tmpFile        
#    print toRemove
    os.remove(toRemove)
                
    cmds.setAttr(smartVolBS + '.envelope', 1)
    cmds.setAttr(smartVolMesh + '.visibility', True)

    cmds.delete(historyDelete)
    cmds.delete(smartVolBase, ch = True)
    cmds.delete(smartVolMesh, ch = True)
    
    loc = cmds.toolPropertyWindow(q = True, loc = True)
    if loc:
        mm.eval('ToggleToolSettings;')
    cmds.setAttr(smartVolMesh + '.overrideEnabled', 1)
    cmds.setAttr(smartVolMesh + '.overrideDisplayType', 2)    
    assignVolumeMeshShader(smartVolMesh)
    loc = cmds.toolPropertyWindow(q = True, loc = True)
    if loc:
        mm.eval('ToggleToolSettings;')
            
#    cmds.setToolTo(ctx)
    cmds.undoInfo(swf = True)
    
def confirmSmartVol():
    currNode = cmds.getAttr('gbNode.currentGBNode')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    volMesh = 'smartVolMesh_' + scalpMesh
    newName = scalpMesh + '_volumeMesh'
    if cmds.objExists(newName):
        cmds.delete(newName)
    cmds.rename(volMesh, newName)
    cmds.setAttr(currNode + '.volumeMesh', newName, type = 'string')
    cmds.parent(newName, cmds.getAttr(currNode + '.mainGroup'))
    cmds.setAttr('smartVolumeGrp_' + scalpMesh + '.visibility', False)
    cmds.setAttr(scalpMesh + '.visibility', True)
    cmds.setAttr(currNode + '.currSmoothLevel', 0)
#    cmds.delete('targets_smartVolume_' + scalpMesh, 'bulgeJoints_' + scalpMesh)
    allJobs = cmds.scriptJob(lj = True)
    for job in allJobs:
        if 'createSmartVol' in job:
            cmds.scriptJob(kill = int(job.split(':')[0]))
    cmds.setToolTo('selectSuperContext')           
    doneWithVolumeMesh()

def smoothBlendWeights(targetList):
    mm.eval('artAttrBlendShapeToolScript 3;')
    mm.eval('artAttrPaintOperation artAttrCtx Smooth;')
    mm.eval('artAttrCtx -e -colorfeedback false `currentCtx`;')
    mm.eval('artAttrCtx -e -opacity 0.8 `currentCtx`;')
    for j in range(0,len(targetList)):
        mm.eval('artBlendShapeSelectTarget artAttrCtx ' + dQ + targetList[j] + dQ + ';')
        mm.eval('artAttrCtx -e -clear `currentCtx`;')
    mm.eval('artAttrCtx -e -colorfeedback true `currentCtx`;')        
    cmds.setToolTo('selectSuperContext')

def doneWithVolumeMesh():
    
    cmds.columnLayout('volumeMeshLT', edit = True, vis = False)

    cmds.columnLayout('askDrawMeshLayout', edit = True, vis = True)
    currNode = cmds.getAttr('gbNode.currentGBNode')
    cmds.setAttr(currNode + '.lastState', 'askDraw', type = 'string')
    
#    cmds.columnLayout('volumeMeshLT', edit = True, vis = False)
#    cmds.columnLayout('cL0Layout', edit = True, vis = True)
#    cmds.columnLayout('cL1Layout', edit = True, vis = True)
#    noUVGrid()
#    currNode = cmds.getAttr('gbNode.currentGBNode')
#    cmds.setAttr(currNode + '.lastState', 'onChar', type = 'string')

def smoothSkinSMV(jointList):
    
    mm.eval('artAttrSkinToolScript 3;')
    mm.eval('artAttrPaintOperation artAttrSkinPaintCtx Smooth;') 
    mm.eval('artAttrSkinPaintCtx -e -colorfeedback false `currentCtx`;')
    mm.eval('artAttrSkinPaintCtx -e -opacity 0.8 `currentCtx`;')
#    cmds.progressBar('progress3DIpol', edit = True, max = len(jointList)-1, vis = True)
    for j in range(0,len(jointList)):
        if j > 0:
            mm.eval('artSkinInflListChanging ' + jointList[j-1] + ' 0;')
        mm.eval('artSkinInflListChanging ' + jointList[j] + ' 1;')
        mm.eval('artSkinInflListChanged artAttrSkinPaintCtx;')
        mm.eval('artAttrSkinPaintCtx -e -clear `currentCtx`;')
    mm.eval('artAttrSkinPaintCtx -e -colorfeedback true `currentCtx`;')        
    cmds.setToolTo('selectSuperContext')
#    cmds.refresh(su = False)   
 
def verifyDPName(dpName):
   
    
    scalpMesh = [] 
    networkNodes = cmds.ls(type = 'network')
    if 'gbNode' in networkNodes:
        networkNodes.remove('gbNode')
    else:
        return
           
    if networkNodes:
        for each in networkNodes:
            if cmds.attributeQuery('parent', node = each, exists = True):
                if cmds.getAttr(each + '.parent') == 'gbNode':
                    if cmds.getAttr(each + '.displayName') == dpName:
                        reportGBMessage('Please use different name, as it is already assigned', True, True, 'red')
#                        raise RuntimeError, 'Please use different name, as it is already assigned'
                        
def verifyScalpMesh(mesh):
   
    
    scalpMesh = [] 
    networkNodes = cmds.ls(type = 'network')
    if 'gbNode' in networkNodes:
        networkNodes.remove('gbNode')
    else:
        return
#each = networkNodes[0]           
    if networkNodes:
        for each in networkNodes:
            if cmds.attributeQuery('parent', node = each, exists = True):
                if cmds.getAttr(each + '.parent') == 'gbNode':
                    if cmds.getAttr(each + '.scalpMesh') == mesh:
                        reportGBMessage('Please use different mesh as Scalp, as it is already assigned', True, True, 'red')
#                        raise RuntimeError, 'Please use different mesh as Scalp, as it is already assigned'                        
                        
    
def cancelAddNewChar():
    
    option = cmds.confirmDialog( title='Cancel Character Setup', message='Are you sure you do not want to continue with this Character?', button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No' )
    if option == 'Yes':
        cancelAndCleanupNewChar()
        
def cancelAndCleanupNewChar():
            
    stopGBUndo()    
#    cmds.undoInfo(swf = False)
    if cmds.textField('addScalpText', q = True, vis = True):
        GBCallgroomBoy()
        return
    if not cmds.objExists('gbNode'):
        return
            
    currNode = cmds.getAttr('gbNode.currentGBNode')

    if currNode:
        scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
        cmds.parent(scalpMesh, world = True)
        cmds.setAttr(scalpMesh + '.visibility', True)

        shaderNames = getShaderNames()
        for shader in shaderNames:
            if cmds.objExists(shader):
                cmds.delete(shader)
        dispLayers = cmds.ls(type = 'displayLayer')
        if dispLayers:
            currDispLayer = scalpMesh + '_charInterpolation_Curves'
            if currDispLayer in dispLayers:
                cmds.delete(currDispLayer)
        cmds.delete(cmds.getAttr(currNode + '.mainGroup'))
        cmds.delete(currNode)
        if cmds.objExists('initialShadingGroup'):
            cmds.sets(scalpMesh, forceElement = 'initialShadingGroup')    
#        if not cmds.getAttr(currNode + '.drawMesh'):
#           cmds.delete(currNode)
        radio = scalpMesh + 'radio'
        all = cmds.lsUI(mi = True)
        for a in all:
            if radio in a:
                cmds.deleteUI(radio)


    removeGBConnectedMeshStripSetup()    
    
    allChars = getCharNodes()                        
    if allChars:
        cmds.setAttr('gbNode.currentGBNode', allChars[0], type = 'string')
        cmds.setAttr('gbNode.activeMesh', cmds.getAttr(allChars[0] + '.drawMesh'), type = 'string')
    
    cmds.undoInfo(swf = True)
    
    GBCallgroomBoy()
    startGBUndo()
    

def removeGBConnectedMeshStripSetup():
    
    meshStripNodes = getMeshStripNodes('gb')
    if meshStripNodes:
        for msNode in meshStripNodes:
            connGB = cmds.getAttr(msNode + '.connectedGBNode')
            currNode = cmds.getAttr('gbNode.currentGBNode')
            if connGB == currNode:
                msGrp = cmds.getAttr(msNode + '.msGrp')
#                print 'deleting ', msGrp, msNode
                cmds.delete(msGrp)
                cmds.delete(msNode)
                menuNewMeshStripSetup() 
                cleanupAbortedMSNodes()
                break

def onCharMeshUpdate():
    
    cmds.undoInfo(swf = False)

    dpName = cmds.textField('addScalpText', q = True, tx = True)
    if not mm.eval('isValidObjectName(' + dQ + dpName + dQ +');'):
        cmds.textField('addScalpText', edit = True, tx = '')
        reportGBMessage('Please use naming as per Maya conventions', True, True, 'red')
#        raise RuntimeError, 'Please use naming as per Maya conventions'
    verifyDPName(dpName)
    mesh = cmds.ls(sl = True)[0]
    verifyScalpMesh(mesh)
    
    cmds.textField('addScalpText', edit = True, vis = False)
    cmds.button('confirmScalpText', edit = True, vis = False)
    resetGBStatus()
#    cmds.button('cancelAddNewCharacterBtn',edit = True, vis = True)
    
    cmds.makeIdentity(mesh, apply = True)
    nwNode = cmds.createNode('network', ss = True, name = 'gb_' + mesh)
    
    cmds.addAttr(nwNode, ln = 'parent', sn = 'pr', dt = 'string')
    cmds.setAttr(nwNode + '.parent', 'gbNode', type = 'string')
    
    cmds.addAttr(nwNode, ln = 'displayName', sn = 'dp', dt = 'string')
    cmds.setAttr(nwNode + '.displayName', dpName, type = 'string')
    
    cmds.addAttr(nwNode, ln = 'scalpMesh', sn = 'sm', dt = 'string')
    cmds.setAttr(nwNode + '.scalpMesh', mesh, type = 'string')
    
    cmds.addAttr(nwNode, ln = 'volumeMesh', dt = 'string')
    cmds.addAttr(nwNode, ln = 'drawMesh', dt = 'string')
    
    cmds.addAttr(nwNode, ln = 'uvGridCreated', sn = 'uvGridC', attributeType = 'bool', dv = False)
    cmds.addAttr(nwNode, ln = 'uvGrid', sn = 'uvGrid', dt = 'string')
    
    cmds.menu('selCharMenu', edit = True, enable = True)
    cmds.menuItem(nwNode + '_radio', label = dpName, ia = '', radioButton = True, cl = 'charRadio', c = 'charSelected()', p = 'selCharMenu')
    
    
    
    cmds.setAttr('gbNode.currentGBNode', nwNode, type = 'string')
    cmds.setAttr('gbNode.activeMesh', mesh, type = 'string')
    
    cmds.addAttr(nwNode, ln = 'mainGroup', dt = 'string')
    cmds.addAttr(nwNode, ln = 'baseMeshGroup', dt = 'string')
    
    cmds.addAttr(nwNode, ln = 'scalpMeshFollicle', dt = 'string')
    cmds.addAttr(nwNode, ln = 'volumeMeshFollicle', dt = 'string')
    cmds.addAttr(nwNode, ln = 'drawMeshFollicle', dt = 'string')
    
    cmds.addAttr(nwNode, ln = 'closestPointNode', dt = 'string')
    cmds.addAttr(nwNode, ln = 'scalpMeshCPNode', dt = 'string')
    cmds.addAttr(nwNode, ln = 'volumeMeshCPNode', dt = 'string')
    cmds.addAttr(nwNode, ln = 'drawMeshCPNode', dt = 'string')

    cmds.addAttr(nwNode, ln = 'lastState', dt = 'string')
    cmds.addAttr(nwNode, ln = 'lastStateAttrF1', at = 'float')
    
    cmds.addAttr(nwNode, ln = 'curveList4Graph', dt = 'string')
    cmds.addAttr(nwNode, ln = 'origCurveCVpos', dt = 'string')
    cmds.addAttr(nwNode, ln = 'closestPointPos', dt = 'string')
    cmds.addAttr(nwNode, ln = 'dVector', dt = 'string')
    cmds.addAttr(nwNode, ln = 'cvUV', dt = 'string')
    cmds.addAttr(nwNode, ln = 'cvCountL', dt = 'string')    
    
    cmds.addAttr(nwNode, ln = 'whichMesh', dt = 'string')
    
    cmds.addAttr(nwNode, ln = 'superCurves3D', dt = 'string')
    cmds.addAttr(nwNode, ln = 'superCurvesPos', dt = 'string')
    cmds.addAttr(nwNode, ln = 'ipolVertices3D', dt = 'string')
    
    cmds.addAttr(nwNode, ln = 'curveFaces', dt = 'string')
    cmds.addAttr(nwNode, ln = 'removedIpolFromGraph', dt = 'string')
    cmds.addAttr(nwNode, ln = 'toBeUpdatedIpol', dt = 'string')
    cmds.addAttr(nwNode, ln = 'isGraphRestored', attributeType = 'bool', dv = False)
    
    cmds.addAttr(nwNode, ln = 'tweakMesh', dt = 'string')
    cmds.addAttr(nwNode, ln = 'scalpMeshShape', dt = 'string')
    cmds.addAttr(nwNode, ln = 'volumeMeshShape', dt = 'string')
    cmds.addAttr(nwNode, ln = 'alteredVertices', dt = 'string')
    cmds.addAttr(nwNode, ln = 'penetratedVertices', dt = 'string')
    cmds.addAttr(nwNode, ln = 'useIpolForGraph', attributeType = 'bool', dv = False) 
    
    cmds.addAttr(nwNode, ln = 'allowedSmoothValues', dt = 'string')
    cmds.addAttr(nwNode , ln = 'currSmoothLevel', attributeType = 'short', dv = 0)
    cmds.addAttr(nwNode , ln = 'paintOnMesh', dt = 'string')
    
    cmds.addAttr(nwNode, ln = 'currentLocalControl', dt = 'string')
    cmds.addAttr(nwNode, ln = 'regionCtrlName', dt = 'string')
    cmds.addAttr(nwNode, ln = 'regionCtrlGraph', dt = 'string')
    cmds.addAttr(nwNode, ln = 'lastRegionCtrl', dt = 'string')
    cmds.addAttr(nwNode, ln = 'regionCtrlCurves', dt = 'string')
    cmds.addAttr(nwNode, ln = 'regionPerList', dt = 'string')
    cmds.addAttr(nwNode, ln = 'regionEdited', dt = 'string')
    cmds.addAttr(nwNode, ln = 'regionAdded', dt = 'string')
    cmds.addAttr(nwNode, ln = 'regionMoved', dt = 'string')
        
    cmds.addAttr(nwNode, ln = 'scalpSuperCurves', dt = 'string')
    cmds.addAttr(nwNode, ln = 'scalpSuperCurvesPos', dt = 'string')
    cmds.addAttr(nwNode, ln = 'volumeSuperCurves', dt = 'string')
    cmds.addAttr(nwNode, ln = 'volumeSuperCurvesPos', dt = 'string')
    
    cmds.addAttr(nwNode, ln = 'switchBackSuperCurves', attributeType = 'bool', dv = False) 
    cmds.addAttr(nwNode, ln = 'meshNotUpdated', attributeType = 'bool', dv = False) 
    
    cmds.addAttr(nwNode, ln = 'lastBunchName', dt = 'string')
    
    cmds.addAttr(nwNode, ln = 'rgbGraphs', dt = 'string')
    cmds.addAttr(nwNode, ln = 'defaultGraph',  dt = 'string')
    cmds.setAttr(nwNode + '.defaultGraph', '0,0,3,1,1,3', type = 'string')
    
    cmds.addAttr(nwNode, ln = 'volumeResizePos', dt = 'string')
    cmds.addAttr(nwNode, ln = 'toBeResize', dt = 'string')
    
    cmds.addAttr(nwNode, ln = 'rgbInfo', dt = 'string')
    cmds.addAttr(nwNode, ln = 'rgbPerList', dt = 'string')
    cmds.addAttr(nwNode, ln = 'rgbCurves', dt = 'string')
    cmds.addAttr(nwNode, ln = 'texPathTime', dt = 'string')
    
    cmds.addAttr(nwNode, ln = 'tempData', dt = 'string')
    
    cmds.addAttr(nwNode, ln = 'superCurvesRF', dt = 'string')
    cmds.addAttr(nwNode, ln = 'superCurvesPosRF', dt = 'string')
    cmds.addAttr(nwNode, ln = 'superMeshFacesRF', dt = 'string')
    
    cmds.addAttr(nwNode, ln = 'manualCurves', dt = 'string')
    cmds.addAttr(nwNode, ln = 'manualCurvesPos', dt = 'string')
    cmds.addAttr(nwNode, ln = 'useManualForGraph', attributeType = 'bool', dv = False) 
    
    cmds.addAttr(nwNode , ln = 'displayMeshOffset', attributeType = 'float', dv = 1.5)
    
    cmds.addAttr(nwNode, ln = 'clumpMesh', dt = 'string')
    
    cmds.addAttr(nwNode, ln = 'ips', dt = 'string')
    
    cmds.addAttr(nwNode, ln = 'clumpCurves', dt = 'string')
    cmds.addAttr(nwNode, ln = 'clumpCurvesFlatPos', dt = 'string')
    
    cmds.addAttr(nwNode, ln = 'clumpSurfaces', dt = 'string')
    cmds.addAttr(nwNode, ln = 'clumpVertices', dt = 'string')
    cmds.addAttr(nwNode, ln = 'clumpBasePos', dt = 'string')
    cmds.addAttr(nwNode, ln = 'clumpScaleGraph', dt = 'string')
    cmds.addAttr(nwNode, ln = 'clumpFlatness', dt = 'string')
    cmds.addAttr(nwNode, ln = 'clumpSectionsU', dt = 'string')
    cmds.addAttr(nwNode, ln = 'clumpSpansV', dt = 'string')
    
    
    cmds.addAttr(nwNode, ln = 'performIPS', attributeType = 'bool', dv = False)     
    cmds.addAttr(nwNode, ln = 'lastIpolSelection', dt = 'string')
    cmds.addAttr(nwNode, ln = 'existIPS', dt = 'string')
    
    cmds.addAttr(nwNode, ln = 'clumpDB', dt = 'string')
    cmds.addAttr(nwNode, ln = 'toBeUpdatedClumps', dt = 'string')
    
    
    
    
    
    mainGrp = cmds.group(n = dpName + '_Main_Group', em = True)
#    cmds.group(name = 'ScalpMesh_' + mesh, em = True, parent = mainGrp)
    cmds.select(mesh, r = True)
    cmds.setAttr(nwNode + '.mainGroup', mainGrp, type = 'string')
#    meshShape = cmds.listRelatives(mesh, s = True)[0]
    
#    selCharShp = cmds.listRelatives(mesh, s = True)[0]
#    charCPNode = cmds.createNode('closestPointOnMesh')
#    cmds.connectAttr(selCharShp+'.worldMatrix',charCPNode+'.inputMatrix')
#    cmds.connectAttr(selCharShp+'.worldMesh',charCPNode+'.inMesh')
#    cmds.setAttr(nwNode + '.closestPointNode', charCPNode, type = 'string')
#    cmds.setAttr(nwNode + '.scalpMeshCPNode', charCPNode, type = 'string')
    cmds.parent(mesh, mainGrp)
    
    baseMeshGrp = 'baseMesh_' + mesh
    cmds.group(name = baseMeshGrp, em = True, parent = mainGrp)
    cmds.setAttr(nwNode + '.baseMeshGroup', baseMeshGrp , type = 'string')
#    createFollicle('scalpMesh')
    updateMainGroupVisibility()
#    createUVGrid()
    volMeshCreate()
    cmds.button('bkpResBtn' , edit = True, vis = True)
    cmds.button('showHideBtn' , edit = True, vis = True)
    
    
    
    cmds.undoInfo(swf = True)
    
def createCPNode(obj):
    
    objShp = cmds.listRelatives(obj, s = True)[0]
    cpNode = cmds.createNode('closestPointOnMesh',ss = True)
    cmds.connectAttr(objShp+'.worldMatrix', cpNode + '.inputMatrix')
    cmds.connectAttr(objShp+'.worldMesh', cpNode + '.inMesh')
    return cpNode

    
def gbNodeInit():
    
    if cmds.objExists('gbNode'):
        return
    sel = cmds.ls(sl = True)        
    cmds.createNode('network', n = 'gbNode')
    cmds.addAttr('gbNode' , ln = 'rebuildCVs', sn = 'rbCV', attributeType = 'short', dv = 10)
    cmds.addAttr('gbNode' , ln = 'rebuildP01', sn = 'rbP01', attributeType = 'bool', dv = True)
    cmds.addAttr('gbNode' , ln = 'currentGBNode', sn = 'curGB', dt = 'string')
    cmds.addAttr('gbNode' , ln = 'activeMesh', sn = 'actMesh', dt = 'string')
    cmds.addAttr('gbNode' , ln = 'maxCV', at = 'byte')
    cmds.addAttr('gbNode' , ln = 'concaveCheck', attributeType = 'bool', dv = False)
    cmds.addAttr('gbNode' , ln = 'minimumSuperCurves', attributeType = 'short', dv = 6)
    cmds.addAttr('gbNode' , ln = 'displayMeshOffset', attributeType = 'float', dv = 1.5)
    cmds.addAttr('gbNode' , ln = 'pathForIcons', dt = 'string')
    cmds.addAttr('gbNode' , ln = 'tempGBNode', dt = 'string')
    cmds.setAttr('gbNode.maxCV', 0)  
    cmds.setAttr('gbNode.tempGBNode', 'tempGBNode', type = 'string')  
    if sel:
        cmds.select(sel, r = True)

def getCharNodes():
    
    scalpMesh = [] 
    networkNodes = cmds.ls(type = 'network')
    if 'gbNode' in networkNodes:
        networkNodes.remove('gbNode')
    
    if not len(networkNodes) == 0:
        for each in networkNodes:
            if cmds.attributeQuery('parent', node = each, exists = True):
                scalpMesh.append(each)
    return scalpMesh



def charSelected():
    
    stopGBUndo()
    scalp = getCharNodes()
    recallStripVtx('charselected')
    

#    print scalp
    for s in scalp:
        if cmds.menuItem(s + '_radio', q = True, radioButton = True):
            selectedScalp = s
#    print '>>>>>>>>>> ', selectedScalp
    
    checkForTempGBNode()
    insertRemoveCharMenu()
    
    cmds.setAttr('gbNode.currentGBNode', selectedScalp, type = 'string')
    showDisplayScalpMesh()
    if cmds.getAttr(selectedScalp + '.meshNotUpdated'):
        revertFromMeshShapes('scalpMesh', 'volumeMesh')
        cmds.setAttr(selectedScalp + '.meshNotUpdated', False)
    
    lastState = cmds.getAttr(selectedScalp + '.lastState')
    
    if lastState == 'defaultVol' or lastState == None:
#        print 'herere'
        cmds.columnLayout('cL1Layout', edit = True, vis = False)
        volumeMeshUIRestore()
        volMeshCreate()
        cmds.radioButtonGrp('volRadio1', edit = True, sl = 2)
        createVol()
#        cmds.radioButtonGrp('createVolRadio', edit = True, sl = 1)
        cmds.iconTextRadioButton('defaultVolRadioIcon',edit = True, sl = True)
        defaultVol()
        
    elif lastState == 'smartVol':
        cmds.columnLayout('cL1Layout', edit = True, vis = False)
        volumeMeshUIRestore()
        volMeshCreate()
        cmds.radioButtonGrp('volRadio1', edit = True, sl = 2)
        createVol()
#        cmds.radioButtonGrp('createVolRadio', edit = True, sl = 2)
        cmds.iconTextRadioButton('smartVolRadioIcon',edit = True, sl = True)
        enterSmartVol()
        
    elif lastState == 'askDraw':
#        print 'askkkk'
        cmds.columnLayout('cL1Layout', edit = True, vis = False)
        volumeMeshUIRestore()
        volMeshCreate()
        cmds.columnLayout('volumeMeshLT', edit = True, vis = False)
        cmds.columnLayout('askDrawMeshLayout', edit = True, vis = True)
            
    
    elif lastState == 'onChar':
        cmds.columnLayout('cL0Layout', edit = True, vis = True)
        cmds.columnLayout('cL1Layout', edit = True, vis = True)
        
        cmds.button('editBaseMeshBtn', edit = True, vis = True)

        cmds.tabLayout('mainTabs', edit = True, sti = 1)
        noUVGrid()
        cmds.radioButton('onCharRadio', edit = True, select = True)
        cmds.frameLayout('commonFrame', edit = True, vis = True)
        drawOnChar(True)
        
    elif lastState == 'onGrid':
        cmds.columnLayout('cL0Layout', edit = True, vis = True)
        cmds.columnLayout('cL1Layout', edit = True, vis = True)
        
        cmds.button('editBaseMeshBtn', edit = True, vis = True)
        
        cmds.tabLayout('mainTabs', edit = True, sti = 1)
        noUVGrid()
        cmds.radioButton('onGridRadio', edit = True, select = True)
        cmds.frameLayout('commonFrame', edit = True, vis = True)
        drawOnGrid()
        
    elif lastState == 'graphInit':
        cmds.columnLayout('cL0Layout', edit = True, vis = True)
        cmds.columnLayout('cL1Layout', edit = True, vis = True)
        cmds.frameLayout('commonFrame', edit = True, vis = True)
        cmds.button('editBaseMeshBtn', edit = True, vis = True)
        
        cmds.tabLayout('mainTabs', edit = True, sti = 2)
        showGraphInit()
#        cmds.columnLayout('graphInitLyt', edit = True, vis = True)
#       cmds.columnLayout('adjVolLayout', edit = True, vis = False)
    
    elif lastState == 'graphPage':

        cmds.columnLayout('cL0Layout', edit = True, vis = True)
        cmds.columnLayout('cL1Layout', edit = True, vis = True)
        cmds.frameLayout('commonFrame', edit = True, vis = True)
        cmds.button('editBaseMeshBtn', edit = True, vis = True)
        
        cmds.tabLayout('mainTabs', edit = True, sti = 2)
#        continueForGraph()
        currLocalControl = cmds.getAttr(selectedScalp + '.currentLocalControl')
#        print 'currlocal', currLocalControl
#        if currLocalControl == 'region':
#            regionBasedGraphSelected()
#        elif currLocalControl == 'color':
#            print 'color registered'
#            colorBasedGraphSelected()
#        elif currLocalControl == None:
    
        if currLocalControl == None:           
#            print 'no local control'
            cmds.frameLayout('localizedControlFrame', edit = True, vis = True)
            cmds.button('addColorGraphBtn', edit = True, vis = False)
            cmds.frameLayout('colorGraphFrame', edit = True, vis = False)
            cmds.columnLayout('rgbGraphsColumn', edit = True, vis = False)
            cmds.button('colorGraphControlBtn', edit = True, en = True)
            cmds.button('regionGraphControlBtn', edit = True, en = True)
            cmds.canvas('whiteCanvas', edit = True, vis = False)
            cmds.button('loadGraphFromControlBtn', edit = True, vis = False)
            cmds.button('updateGraphOnRegionBtn', edit = True, vis = False)
            
            cmds.gradientControlNoAttr('defaultColorGraph', edit = True, asString = cmds.getAttr(selectedScalp + '.defaultGraph'))
#        cmds.columnLayout('graphInitLyt', edit = True, vis = False)
#       cmds.columnLayout('adjVolLayout', edit = True, vis = True)

        
    if cmds.getAttr(selectedScalp + '.volumeMesh'): 
        reassignShaders()
    updateMainGroupVisibility()
    updateMeshStripsSetup()
    gbCloseup(cmds.getAttr(selectedScalp + '.scalpMesh'))
    startGBUndo()
    
def gbCloseup(mesh):

    sel = cmds.ls(sl = True)        
    cmds.select(mesh, r = True)
    cmds.viewFit()
    cmds.select(cl = True)
    if len(sel) > 0:
        cmds.select(sel, r = True)
        
def drawMeshSelected():
    
    stopGBUndo()
    currNode = cmds.getAttr('gbNode.currentGBNode')
    cmds.frameLayout('commonFrame', edit = True, vis = True)
#    select = cmds.radioButtonGrp('radioDrawMesh', q = True, sl = True)
    radio = cmds.iconTextRadioCollection( 'radioDrawMeshICON' , q = True, sl = True )
    if 'scalp' in radio:
        select = 1
    else:
        select = 2        
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    volMesh = cmds.getAttr(currNode + '.volumeMesh')
    if select == 1:
        cmds.setAttr(currNode + '.drawMesh', scalpMesh, type = 'string')
        sel = 'scalpMesh'
        cmds.setAttr(currNode + '.whichMesh', sel, type = 'string')
    else:
        cmds.setAttr(currNode + '.drawMesh', volMesh, type = 'string')
        sel = 'volumeMesh'
        cmds.setAttr(currNode + '.whichMesh', sel, type = 'string')
        
#    volMesh = cmds.getAttr(currNode + '.volumeMesh')

    drawMesh = cmds.getAttr(currNode + '.drawMesh')
#    drawMesh = cmds.getAttr(currNode + '.scalpMesh')
    cmds.setAttr(currNode + '.paintOnMesh', drawMesh, type = 'string')
#    baseMeshGrp = 'baseMesh_' + drawMesh
    baseMeshGrp = 'baseMesh_' + scalpMesh
#    cmds.group(name = baseMeshGrp, em = True, parent = cmds.getAttr(currNode + '.mainGroup'))
    if cmds.objExists('baseMesh_' + cmds.getAttr(currNode + '.scalpMesh')):
        cmds.rename('baseMesh_' + cmds.getAttr(currNode + '.scalpMesh'), baseMeshGrp)
    cmds.setAttr(currNode + '.baseMeshGroup', baseMeshGrp, type = 'string')
    
#    createFollicle('volumeMesh')
#    cmds.setAttr(currNode + '.drawMeshFollicle', cmds.getAttr(currNode + '.' + sel + 'Follicle'), type = 'string')
    
#    volMeshShp = cmds.listRelatives(cmds.getAttr(currNode + '.volumeMesh'), s = True)[0]
#    volCPNode = cmds.createNode('closestPointOnMesh')
#    cmds.connectAttr(volMeshShp+'.worldMatrix',volCPNode+'.inputMatrix')
#    cmds.connectAttr(volMeshShp+'.worldMesh',volCPNode+'.inMesh')
#    cmds.setAttr(currNode + '.volumeMeshCPNode', volCPNode, type = 'string')
#    cmds.setAttr(currNode + '.drawMeshCPNode', cmds.getAttr(currNode + '.' + sel + 'CPNode'), type = 'string')
    
    if cmds.radioButtonGrp('volRadio1', q = True, sl = True) == 1:
        checkPenetrations(scalpMesh, volMesh)
    storeMeshShapes()
    cmds.button('cancelAddNewCharacterBtn',edit = True, vis = False)
    cmds.columnLayout('askDrawMeshLayout', edit = True, vis = False)
    cmds.columnLayout('cL0Layout', edit = True, vis = True)
    cmds.columnLayout('cL1Layout', edit = True, vis = True)
    cmds.tabLayout('mainTabs', edit = True, sti = 1)
    noUVGrid()

    cmds.radioButton('onCharRadio', edit = True, select = True)
    drawOnChar(True)
    cmds.button('editBaseMeshBtn', edit = True, vis = True)
    
    
    scalpDISP = scalpMesh + '_DISPLAY'
#    volDISP = volMesh + '_DISPLAY'
    if cmds.objExists(scalpDISP):
        cmds.delete(scalpDISP)
#    if cmds.objExists(volDISP):
#        cmds.delete(volDISP)            
    cmds.duplicate(scalpMesh, rr = True, rc = True, name = scalpDISP)

    resizeDISPMesh(scalpDISP)
    cmds.setAttr(scalpMesh + '.visibility', False)
    setVolMeshReference()
    reassignShaders()
#    cmds.setAttr(volMesh + '.visibility', False)
#    gbCloseup(scalpMesh)
    hideToolSettings()

    insertRemoveCharMenu()
    startGBUndo()
    startDraw()
    
def createFreshDISPMesh():
    
    currNode = cmds.getAttr('gbNode.currentGBNode')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    scalpDISP = scalpMesh + '_DISPLAY'
    if cmds.objExists(scalpDISP):
        cmds.delete(scalpDISP)
    cmds.duplicate(scalpMesh, rr = True, rc = True, name = scalpDISP)
#    resizeDISPMesh(scalpDISP)
    
    
def resizeDISPMesh(mesh):
    
    currNode = cmds.getAttr('gbNode.currentGBNode')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    mainGroup = cmds.getAttr(currNode + '.mainGroup')
    if mesh == scalpMesh + '_DISPLAY':
        cmds.delete(mesh)
        cmds.duplicate(scalpMesh, rr = True, rc = True, name = mesh)
        
    cmds.setAttr(mesh + '.visibility', False)
    if cmds.attributeQuery('displayMeshOffset', node = currNode, exists = True):
        dispPer = cmds.getAttr(currNode + '.displayMeshOffset')
    else:
        dispPer = cmds.getAttr('gbNode.displayMeshOffset')
              
    disp = volumePercentByDistance(dispPer,mesh)
#    print 'dispppp', disp
    whichMode = ''
    tempDup = cmds.duplicate(mesh, name = 'tempDup', rr = True)[0]
    cmds.select(tempDup, r = True)
#    bbox1 = cmds.exactWorldBoundingBox(tempDup) 
#    bbY1 = bbox1[4]
    tempDupShape = cmds.listRelatives(tempDup, s = True)[0]
    
    bbY1 = cmds.getAttr(tempDupShape + '.boundingBoxMaxZ')
#    bbY1min = bbox1[1]
    mm.eval('artPuttyToolScript 3;')
    mm.eval('resetTool artPuttyContext;')
    cmds.artPuttyCtx('artPuttyContext', e = True, mtm = 'pull', sao = 'additive')
    mm.eval('artPuttyCtx -e -maxdisp ' + str(disp) + '`currentCtx`;')
    mm.eval('artPuttyCtx -e -clear `currentCtx`;')
    cmds.setToolTo('selectSuperContext')
#    bbox2 = cmds.exactWorldBoundingBox(tempDup) 
#    bbY2 = bbox2[4]
    bbY2 = cmds.getAttr(tempDupShape + '.boundingBoxMaxZ')
#    bbY2min = bbox2[1]
#    print bbox2
#    print bbox1
#    print bbY2
#    print bbY1
#    print bbY2, bbY1

    if bbY2 < bbY1:
        whichMode = 'pull'
    else:
        whichMode = 'push'
    cmds.delete(tempDup)
        
    cmds.select(mesh, r = True)
    mm.eval('artPuttyToolScript 3;')
    mm.eval('resetTool artPuttyContext;')
    cmds.artPuttyCtx('artPuttyContext', e = True, sao = 'additive', mtm = whichMode)
    mm.eval('artPuttyCtx -e -maxdisp ' + str(disp) + '`currentCtx`;')
    mm.eval('artPuttyCtx -e -clear `currentCtx`;')
    cmds.setToolTo('selectSuperContext')
    if cmds.button('editBaseMeshBtn', q = True, vis = True):
        cmds.setAttr(mesh + '.visibility', True)
        
#    print 'DISPPP'

    
def volumeMeshUIRestore():
    
    iconPath = assignPathToIcons()
    
    cmds.columnLayout('cL0Layout', edit = True, vis = True)
    cmds.button('cancelAddNewCharacterBtn', edit = True, vis = True)
#    cmds.columnLayout('cL1Layout', edit = True, vis = True)
    cmds.iconTextButton('addScalpBtnICON', edit = True, i = iconPath + 'charSetup.jpg', vis = False)
#    cmds.button('addScalpBtn' , edit = True, vis = False)
    cmds.textField('addScalpText', edit = True, vis = False)
#    cmds.button('cancelAddNewCharacterBtn', edit = True, vis = False)
    cmds.columnLayout('volumeMeshLT', edit = True, vis = True)
    
    
def updateMainGroupVisibility():
    
    scalp = getCharNodes()
    currNode = cmds.getAttr('gbNode.currentGBNode')
    mainGrp = cmds.getAttr(currNode + '.mainGroup')
    mesh = cmds.getAttr(currNode + '.scalpMesh')
    

    cmds.setAttr(mainGrp + '.visibility', True)

    meshDISP = mesh + '_DISPLAY'
    if cmds.objExists(meshDISP):
        cmds.setAttr(meshDISP + '.visibility', True)
        cmds.setAttr(mesh + '.visibility', False)
    else:
        cmds.setAttr(mesh + '.visibility', True)
    lastState =  cmds.getAttr(currNode + '.lastState')   
    
    if lastState == 'graphPage':
        cmds.setAttr(meshDISP + '.visibility', False)
        cmds.setAttr(mesh + '.visibility', True)
    
    elif not lastState == 'smartVol' and not lastState == 'graphPage':
        if cmds.objExists(meshDISP):
            cmds.setAttr(meshDISP + '.visibility', True)
        else:
            cmds.setAttr(mesh + '.visibility', True)

    elif lastState == 'smartVol':    
        cmds.setAttr(mesh + '.visibility', False)

    for each in scalp:
        if not currNode == each:
#            print each
            cmds.setAttr(cmds.getAttr(each + '.mainGroup') + '.visibility', False)
#            cmds.setAttr(cmds.getAttr(each + '.scalpMesh') + '.visibility', False)
    

#    cmds.select(mesh, r = True)
#    cmds.viewFit()
#    cmds.select(cl = True)

def updateMeshStripsSetup():

    updateMeshStripsVisibility()
    updateMeshStripsUIForGB()    
    
            
def updateMeshStripsVisibility():
    
    meshStripNodes = getMeshStripNodes()
    if meshStripNodes:
        for msNode in meshStripNodes:
            msGrp = cmds.getAttr(msNode + '.msGrp')
            cmds.setAttr(msGrp + '.visibility', False)
    
                
def updateMeshStripsUIForGB():
    
    meshStripNodes = getMeshStripNodes('gb')
    currNode = cmds.getAttr('gbNode.currentGBNode') 
    gbFound = False
#    msNode = meshStripNodes[0]
    for msNode in meshStripNodes:
        connGB = cmds.getAttr(msNode + '.connectedGBNode')
        if connGB == currNode:
#            print 'setting at 2328'
            
            cmds.setAttr('meshGenGBNode.currentMeshStripNode', msNode, type = 'string')
            meshStripControlsUIShow()
            gbFound = True
    if not gbFound:
#        print 'gb not found'
        if cmds.columnLayout('meshStripL1', exists = True):
            cmds.columnLayout('meshStripL1', edit = True, vis = False)            
    
    custMeshStripNodes = getMeshStripNodes()

    for msNode in custMeshStripNodes:
        cmds.menuItem(msNode + '_radio', edit = True, rb = False)            
    

            
def drawOnGrid():
    
    stopGBUndo()
    cmds.setToolTo('selectSuperContext')
    
    cmds.frameLayout('charCM', e = True,vis = False)
    cmds.frameLayout('interpolationFrame', e = True, vis = False)
    cmds.frameLayout('gridCM', e = True,vis = True)
    cmds.button('startDrawBtn', e = True, vis = True)
    cmds.frameLayout('uvDrawFrame', e = True, vis = False)
    currGB = cmds.getAttr('gbNode.currentGBNode')
    uvName = cmds.getAttr(currGB + '.uvGrid')
    cmds.setAttr(uvName + '.visibility', True)
    cmds.setAttr('gbNode.activeMesh', uvName, type = 'string')
    
    gbCloseup(uvName)
#    sel = cmds.ls(sl = True)
#    cmds.select(uvName, r = True)
#    cmds.viewFit()
#    cmds.select(cl = True)
#    if len(sel) > 0:
#        cmds.select(sel, r = True)
    cmds.setAttr(currGB + '.lastState', 'onGrid', type = 'string')        
    startGBUndo()
    startDraw()

def hideToolSettings():
    
    loc = cmds.toolPropertyWindow(q = True, loc = True)
    if loc:
        mm.eval('ToggleToolSettings;')
        
        
def drawOnChar(closeUp = False):
    
    stopGBUndo()
#    from random import randrange as rr
#    print 'aaaaa', closeUp
    cmds.setToolTo('selectSuperContext')
    hideToolSettings()
    cmds.frameLayout('gridCM', e = True,vis = False)
    cmds.frameLayout('charCM', e = True,vis = True)
    cmds.frameLayout('interpolationFrame', e = True, vis = True)
    cmds.button('startDrawBtn', e = True, vis = True)
    cmds.frameLayout('uvDrawFrame', e = True, vis = False)
    currGB = cmds.getAttr('gbNode.currentGBNode')
    lastState = cmds.getAttr(currGB + '.lastState')
    if lastState == 'onGrid':
        autoTransferGridToChar()
    
#    scalpMesh= cmds.getAttr(currGB + '.scalpMesh')
    scalpMesh= cmds.getAttr(currGB + '.drawMesh')
#    uvName = cmds.getAttr(currGB + '.uvGrid')
#    cmds.setAttr(uvName + '.visibility', False)
    paintMesh = cmds.getAttr(currGB + '.paintOnMesh')
    cmds.setAttr('gbNode.activeMesh', paintMesh, type = 'string')
#    allV = cmds.polyEvaluate(scalpMesh, v = True)

#    vList = []
#    for i in range(0,10):
#        vList.append(scalpMesh + '.vtx[' + str(rr(0,allV)) + ']')
#    cmds.select(vList, r = True)
#    closeUp = False
    if closeUp:
        gbCloseup(scalpMesh)

    cmds.setAttr(currGB + '.lastState', 'onChar', type = 'string')   
#    print 'hiding tool'     
    startGBUndo()
#    startDraw()
        
def aboutUs():
    
    import webbrowser

    webbrowser.open('http://www.groomboy.com')
    
def startDraw():
    
#    print 'entered start draw'
    stopGBUndo()
    changeSwitchBtnLabel()
    cmds.button('startDrawBtn', e = True, vis = False)
    cmds.frameLayout('uvDrawFrame', e = True, vis = True,cl = False)
#    cmds.frameLayout('charCM', e = True, cl = True)
#    cmds.frameLayout('interpolationFrame', e = True, cl = True)
#    cmds.frameLayout('gridCM', e = True, cl = True)
    currMesh = cmds.getAttr('gbNode.activeMesh')
    cmds.select(currMesh, r = True)
#    cmds.viewFit()
    mm.eval('MakePaintable;')
    vers = int(cmds.about(version = True))
    if not cmds.currentCtx() == 'dynWireCtx1':
        mainPath = mm.eval('getenv ' + dQ + 'MAYA_LOCATION' + dQ)
        if vers > 2016:
            brushLoc = mainPath + '/Examples/Paint_Effects/Pens/ballpointRough.mel'
        else:
            brushLoc =  mainPath + '/brushes/pens/ballpointRough.mel'
        mm.eval('copyBrushToSelected ' + dQ + brushLoc + dQ)
    cmds.select(cl = True)
    loc = cmds.toolPropertyWindow(q = True, loc = True)
    if loc:
        mm.eval('ToggleToolSettings;')        
    
    cmds.scriptJob(event = ['DagObjectCreated', 'pfxToCurves()'], compressUndo = True)
    cmds.scriptJob(event =  ['ToolChanged', 'killPFXJob()'] , runOnce = True)
    startGBUndo()
    
def changeSwitchBtnLabel():
    
    currNode = cmds.getAttr('gbNode.currentGBNode')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    paintMesh = cmds.getAttr(currNode + '.paintOnMesh')
    if paintMesh == scalpMesh:
        cmds.button('switchMeshBtn', edit = True, label = 'Switch to Volume Mesh for Drawing')
    else:
        cmds.button('switchMeshBtn', edit = True, label = 'Switch to Scalp Mesh for Drawing')
    
    
def switchMeshToDraw():
    
    stopGBUndo()
    currNode = cmds.getAttr('gbNode.currentGBNode')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    volMesh = cmds.getAttr(currNode + '.volumeMesh')
    paintMesh = cmds.getAttr(currNode + '.paintOnMesh')
    if paintMesh == scalpMesh:
        paintMesh = volMesh
        cmds.button('switchMeshBtn', edit = True, label = 'Switch to Scalp Mesh for Drawing')
    else:
        paintMesh = scalpMesh
        cmds.button('switchMeshBtn', edit = True, label = 'Switch to Volume Mesh for Drawing')
    cmds.undoInfo(swf = False)        
    killPFXJobOnly()
    switchCurvesToOtherMesh()
    cmds.setAttr(currNode + '.paintOnMesh', paintMesh, type = 'string')
    cmds.setAttr('gbNode.activeMesh', paintMesh, type = 'string')
    cmds.undoInfo(swf = True)
    startDraw()
    startGBUndo()
        
def killPFXJobOnly():
    all = cmds.scriptJob(lj = True)
    for a in all:
        if 'pfxToCurves' in a:
            cmds.scriptJob(kill = int(a.split(':')[0]))
    
#    pfxToCurvesFromUI('postDraw')            
          
            
def switchCurvesToOtherMesh():
    
    import cPickle as Pickle
    currNode = cmds.getAttr('gbNode.currentGBNode')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    volMesh = cmds.getAttr(currNode + '.volumeMesh')
    paintMesh = cmds.getAttr(currNode + '.paintOnMesh')

    if paintMesh == scalpMesh:
        currMesh = 'scalpMesh'
        nextMesh = 'volumeMesh'
    else:
        currMesh = 'volumeMesh'
        nextMesh = 'scalpMesh'

    baseMeshGrp = cmds.getAttr(currNode + '.baseMeshGroup')
    baseMeshGrpChildren = cmds.listRelatives(baseMeshGrp, c = True)
    superGrp = 'superCurves_charInterpolation_' + scalpMesh
    if not baseMeshGrpChildren:
        return
    if not superGrp in baseMeshGrpChildren:
        return
    superGrpChildren = []
    superGrpChildren = cmds.listRelatives(superGrp, c = True)
    if not superGrpChildren:
        return
    
    scalpSuperCurvesString = cmds.getAttr(currNode + '.scalpSuperCurves')
    scalpSuperCurvesPosString = cmds.getAttr(currNode + '.scalpSuperCurvesPos')
    volumeSuperCurvesString = cmds.getAttr(currNode + '.volumeSuperCurves')
    volumeSuperCurvesPosString = cmds.getAttr(currNode + '.volumeSuperCurvesPos')
    
    scalpSuperCurves = []
    scalpSuperCurvesPos = []
    volumeSuperCurves = []
    volumeSuperCurvesPos = []
    
    if scalpSuperCurvesString:
        scalpSuperCurves = Pickle.loads(str(scalpSuperCurvesString))
        scalpSuperCurvesPos = Pickle.loads(str(scalpSuperCurvesPosString))
    if volumeSuperCurvesString:
        volumeSuperCurves = Pickle.loads(str(volumeSuperCurvesString))
        volumeSuperCurvesPos = Pickle.loads(str(volumeSuperCurvesPosString))
    
    if currMesh == 'scalpMesh':
        currSuperCurves = scalpSuperCurves
        currSuperCurvesPos = scalpSuperCurvesPos
        nextSuperCurves = volumeSuperCurves
        nextSuperCurvesPos = volumeSuperCurvesPos
    else:
        currSuperCurves = volumeSuperCurves
        currSuperCurvesPos = volumeSuperCurvesPos
        nextSuperCurves = scalpSuperCurves
        nextSuperCurvesPos = scalpSuperCurvesPos
    
    actualSuperCurves = superGrpChildren
    
    addSups = list(set(actualSuperCurves) - set(currSuperCurves))
    remSups = list(set(currSuperCurves) - set(actualSuperCurves))
    
    commonSups = list(set(actualSuperCurves) & set(currSuperCurves))
    if commonSups:
        cmds.makeIdentity(commonSups, apply = True)
        for sup in commonSups:
            currPos = currSuperCurvesPos[currSuperCurves.index(sup)]
            sp = cmds.getAttr(sup +'.spans')
            dg = cmds.getAttr(sup +'.degree') 
            ncv = sp + dg
            if not ncv == len(currPos):
                addSups.append(sup)
                remSups.append(sup)
                continue
            
            for cv in range(ncv):
                actualPos = cmds.xform(sup + '.cv[' + str(cv) + ']', q = True, ws = True, t = True)
                if max([abs(a - b) for a, b in zip(actualPos, currPos[cv])]) > 0.01:
                    addSups.append(sup)
                    remSups.append(sup)
                    break
    
    if remSups:
        
        remIndexList = []
        currDelCurve = []
        currDelPos = []
        nextDelPos = []
        
        for rem in remSups:
            remIndexList.append(currSuperCurves.index(rem))
        
        remIndexList.sort(reverse = True)    

        for x in remIndexList:
            currSuperCurves.pop(x)
            nextSuperCurves.pop(x)
            currSuperCurvesPos.pop(x)
            nextSuperCurvesPos.pop(x)
    
    
    if addSups:
        
        historyDelete = []
        currMeshCPNode = createCPNode(cmds.getAttr(currNode + '.' + currMesh))
        historyDelete.append(currMeshCPNode)
        nextMeshFoll = createFollicle(nextMesh)
        nextMeshFollShp = cmds.listRelatives(nextMeshFoll, s = True)[0]
        historyDelete.append(nextMeshFoll)
        
        zeroDistFound = False
        zeroPos = [0.0,0.0,0.0]
        
        for sup in addSups:
            currSuperCurves.append(sup)
            nextSuperCurves.append(sup)
            cmds.makeIdentity(sup, apply = True)
            sp = cmds.getAttr(sup + '.spans')
            dg = cmds.getAttr(sup +'.degree') 
            ncv = sp + dg
            actualPos = []
            projPos = []
            cvDeleted = False
#            print 'sup ', sup
            cv = 0        
            while cv < ncv:
#                print 'cv ', cv
                actualPosCV = cmds.xform(sup + '.cv[' + str(cv) + ']', q = True, ws = True, t = True)
                actualPos.append(actualPosCV)
                cmds.setAttr(currMeshCPNode + '.ip', actualPosCV[0], actualPosCV[1], actualPosCV[2])
                cU = cmds.getAttr(currMeshCPNode + '.u')
                cV = cmds.getAttr(currMeshCPNode + '.v')
                cmds.setAttr(nextMeshFollShp + '.parameterU', cU)
                cmds.setAttr(nextMeshFollShp + '.parameterV', cV)
                projPosCV = cmds.xform(nextMeshFoll, q = True, ws = True, t = True)
                
                
                if not zeroDistFound:
                    if -0.25 <= projPosCV[0] <= 0.25 and -0.25 <= projPosCV[1] <= 0.25 and -0.25 <= projPosCV[2] <= 0.25:
                        zeroDistFound =  True
                        zeroPos = projPosCV
                
                if projPosCV == zeroPos:
                    ncv = ncv - 1
                    cmds.delete(sup + '.cv[' + str(cv) + ']')
                    cvDeleted = True
                    
                else:
                    projPos.append(projPosCV)
                    cmds.xform(sup + '.cv[' + str(cv) + ']', ws = True, t = projPosCV)
                    cv = cv + 1
            
            if cvDeleted:
                projPos = []
                cmds.rebuildCurve(sup, ch = True, s = sp, d = dg)
                cmds.delete(sup, ch = True)
                for cv in range(sp+dg):
                    projPos.append(cmds.xform(sup + '.cv[' + str(cv) + ']', q = True, ws = True, t = True))
            
            
            currSuperCurvesPos.append(actualPos)
            nextSuperCurvesPos.append(projPos)
            cmds.xform(sup, piv =  actualPos[0])
        
        for h in historyDelete:
            if cmds.objExists(h):
                cmds.delete(h)        
    
    properSups = list(set(commonSups) - set(addSups))
    for sup in properSups:
        nextPos = nextSuperCurvesPos[nextSuperCurves.index(sup)]
        for cv in range(len(nextPos)):
            cmds.xform(sup + '.cv[' + str(cv) + ']', ws = True, t = nextPos[cv])
        cmds.xform(sup, piv = nextPos[0])
    
    
    if currMesh == 'scalpMesh':
        scalpSuperCurvesString = Pickle.dumps(currSuperCurves)
        scalpSuperCurvesPosString = Pickle.dumps(currSuperCurvesPos)
        volumeSuperCurvesString = Pickle.dumps(nextSuperCurves)
        volumeSuperCurvesPosString = Pickle.dumps(nextSuperCurvesPos)
    else:
        scalpSuperCurvesString = Pickle.dumps(nextSuperCurves)
        scalpSuperCurvesPosString = Pickle.dumps(nextSuperCurvesPos)
        volumeSuperCurvesString = Pickle.dumps(currSuperCurves)
        volumeSuperCurvesPosString = Pickle.dumps(currSuperCurvesPos)
        
    
        
    cmds.setAttr(currNode + '.scalpSuperCurves', scalpSuperCurvesString, type = 'string')   
    cmds.setAttr(currNode + '.scalpSuperCurvesPos', scalpSuperCurvesPosString, type = 'string')   
    cmds.setAttr(currNode + '.volumeSuperCurves', volumeSuperCurvesString, type = 'string')   
    cmds.setAttr(currNode + '.volumeSuperCurvesPos', volumeSuperCurvesPosString, type = 'string')   
    
    

def switchCurvesScalpToVol():
    
    currNode = cmds.getAttr('gbNode.currentGBNode')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    baseMeshGrp = cmds.getAttr(currNode + '.baseMeshGroup')
    superGrp = 'superCurves_charInterpolation_' + scalpMesh
    

def switchCurvesScalpToVol():
    
    currNode = cmds.getAttr('gbNode.currentGBNode')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    volMesh = cmds.getAttr(currNode + '.volumeMesh')
    paintMesh = cmds.getAttr(currNode + '.paintOnMesh')
    

def killPFXJob():

    all = cmds.scriptJob(lj = True)
    for a in all:
        if 'pfxToCurves' in a:
            cmds.scriptJob(kill = int(a.split(':')[0]))

    if cmds.checkBox('reflowChk', q = True, v = True):
        reflowCleanup()
        cmds.checkBox('reflowChk', edit = True, v = False)
        
           
    cmds.button('startDrawBtn', e = True, vis = True)
    cmds.frameLayout('uvDrawFrame', e = True, vis = False)    

    cmds.select(cl = True)
    cmds.evalDeferred('cmds.setToolTo(\'CreatePolySphereCtx\')')
    cmds.evalDeferred('cmds.setToolTo(\'selectSuperContext\')', lp = True)
    
    pfxToCurvesFromUI('postDraw')

def pfxToCurves():
    
    currNode = cmds.getAttr('gbNode.currentGBNode')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    baseMesh = cmds.getAttr(currNode + '.drawMesh')
    baseMeshGrp = cmds.getAttr(currNode + '.baseMeshGroup')
    if cmds.currentCtx() == 'dynWireCtx1':
        new = cmds.ls(sl = True)
        if not new:
            return
        whichNode= cmds.ls(cmds.listRelatives(new, s = True)[0], st = True)[1]
        if whichNode == 'stroke':
            newStroke = new[0]    
            cmds.select(newStroke, r = True)
#            return
            mm.eval('doPaintEffectsToCurve( 1);')
            st = cmds.listRelatives(newStroke, s = True)[0]
            c = cmds.listConnections(st, et = True, t = 'nurbsCurve')[0]
            if cmds.checkBox('checkPFXRebuild' , q = True, v = True):
                cv = cmds.intField('cvPFXRebuild', q = True, v = True)
                cmds.rebuildCurve(c, ch = True, s = cv - cmds.getAttr(c + '.degree'), rt = 0, rpo = True, kr = 0)
                
            g = str(cmds.listRelatives(c, f = True)).split('|')
            cmds.delete(c, ch = True)
            scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
            actMesh = cmds.getAttr('gbNode.activeMesh')
#            curveGrp = 'handDrawnCurvesOn_' + actMesh
            
                
            if cmds.radioButton('onGridRadio', q = True, select = True):
                curveGrp = 'handDrawnCurvesOn_' + actMesh
                prnt = actMesh
            else:
#                curveGrp = 'superCurves_charInterpolation_' + baseMesh
                curveGrp = 'superCurves_charInterpolation_' + scalpMesh
                prnt = baseMeshGrp
            if not cmds.objExists(curveGrp):
                cmds.group(name = curveGrp, em = True,parent = prnt)
            cmds.parent(c, curveGrp)
            
            newX = [x for x in cmds.listRelatives(curveGrp, c = True) if actMesh + '_curve' in x]
            if newX:
                newC = newX[-1]
            else:
                newC = actMesh + '_' + c
            
            if cmds.objExists(newC):
                while cmds.objExists(newC):
                    newC = actMesh + '_curve' + str(int(newC.split(actMesh + '_curve')[1])+1)
                cmds.rename(c,newC)
            else:
                cmds.rename(c,newC)
            
            if cmds.checkBox('checkAutoSnapVtx', q = True, v = True):
                cmds.select(newC, r = True)
                snapSelectedToNearestVertex()
            
            if cmds.checkBox('checkPFXSmooth', q = True, v = True):
                sm = cmds.intField('smPFXSmooth', q = True, v = True)
                cmds.smoothCurve(newC + '.cv[*]', s = sm)

            cmds.select(newC, r = True)                                
            pivotToRoot()
            finalShp = cmds.listRelatives(newC, s = True)[0]
            cmds.setAttr(finalShp + '.overrideEnabled', True)
            cmds.setAttr(finalShp + '.overrideColor', 13)
            cmds.delete(newStroke, g[1])
            
            if cmds.checkBox('reflowChk', q = True, v = True):
                execReflowMode(newC)
    
            if cmds.checkBox('autoConvertToManualChk', q = True, v = True):
                convertToFreeform()
            if cmds.checkBox('autoConvertToRoughChk',  q = True, v = True):
                convertToRoughCurves()

            pfxToCurvesFromUI('postDraw')
            cmds.select(cl = True)       
            
    
def pfxToCurvesFromUI(source):
    
    selection = []
    if source == 'handyTools':
        selection = cmds.ls(sl = True)
        if not selection:
            reportGBMessage('Please select PFX Strokes', True, True, 'red')
    else:
        allObjects = [cmds.listRelatives(p, p = True)[0] for p in cmds.ls(type = 'stroke')]
        if not allObjects:
            if source == 'postDraw':
                return
            reportGBMessage('No strokes detected, Please use Handy Tools > Curves > Convert PFX to Curves', False, False, 'yellow')
        for obj in allObjects:
           if cmds.listRelatives(obj, allParents = True) is None and 'strokeBallpointRough' in obj:
               selection.append(obj)

    
    if not selection:
        return
                    
    currNode = cmds.getAttr('gbNode.currentGBNode')
    baseMesh = cmds.getAttr(currNode + '.drawMesh')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    baseMeshGrp = cmds.getAttr(currNode + '.baseMeshGroup')
    for new in selection:
        shp = cmds.listRelatives(new, s = True)
        shpN = ''
        if shp:
            shpN = shp[0]
        if not shpN:
            continue
        whichNode = cmds.ls(shpN, st = True)[1]
        if whichNode == 'stroke':
            newStroke = new
            cmds.select(newStroke, r = True)
#            return
            mm.eval('doPaintEffectsToCurve( 1);')
            st = cmds.listRelatives(newStroke, s = True)[0]
            c = cmds.listConnections(st, et = True, t = 'nurbsCurve')[0]
            if cmds.checkBox('checkPFXRebuild' , q = True, v = True):
                cv = cmds.intField('cvPFXRebuild', q = True, v = True)
                cmds.rebuildCurve(c, ch = True, s = cv - cmds.getAttr(c + '.degree'), rt = 0, rpo = True, kr = 0)
                
            g = str(cmds.listRelatives(c, f = True)).split('|')
            cmds.delete(c, ch = True)
            scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
            actMesh = cmds.getAttr('gbNode.activeMesh')
#            curveGrp = 'handDrawnCurvesOn_' + actMesh

            if cmds.radioButton('onGridRadio', q = True, select = True):
                curveGrp = 'handDrawnCurvesOn_' + actMesh
                prnt = actMesh
            else:
#                curveGrp = 'superCurves_charInterpolation_' + baseMesh
                curveGrp = 'superCurves_charInterpolation_' + scalpMesh    
                prnt = baseMeshGrp
            if not cmds.objExists(curveGrp):
                cmds.group(name = curveGrp, em = True,parent = prnt)
            cmds.parent(c, curveGrp)
            
            newX = [x for x in cmds.listRelatives(curveGrp, c = True) if actMesh + '_curve' in x]
            if newX:
                newC = newX[-1]
            else:
                newC = actMesh + '_' + c
            
            if cmds.objExists(newC):
                while cmds.objExists(newC):
                    newC = actMesh + '_curve' + str(int(newC.split(actMesh + '_curve')[1])+1)
                cmds.rename(c,newC)
            else:
                cmds.rename(c,newC)
            
            if cmds.checkBox('checkAutoSnapVtx', q = True, v = True):
                cmds.select(newC, r = True)
                snapSelectedToNearestVertex()
                                
            if cmds.checkBox('checkPFXSmooth', q = True, v = True):
                sm = cmds.intField('smPFXSmooth', q = True, v = True)
                cmds.smoothCurve(newC + '.cv[*]', s = sm)
            
            cmds.select(newC, r = True)                                  
            pivotToRoot()
            finalShp = cmds.listRelatives(newC, s = True)[0]
            cmds.setAttr(finalShp + '.overrideEnabled', True)
            cmds.setAttr(finalShp + '.overrideColor', 13)
            cmds.delete(newStroke, g[1])
            
            if cmds.checkBox('reflowChk', q = True, v = True):
                execReflowMode(newC)
            
            if cmds.checkBox('autoConvertToManualChk', q = True, v = True):
                convertToFreeform()                
            
            if cmds.checkBox('autoConvertToRoughChk',  q = True, v = True):
                convertToRoughCurves()                
    
    
def toggleStartbtn():

    stopGBUndo()
    cmds.frameLayout('uvDrawFrame', e = True, vis = False)
    cmds.button('startDrawBtn', e = True, vis = True)
    cmds.setToolTo('selectSuperContext')
    startGBUndo()
    
def checkGrid():
    
    stopGBUndo()
    cmds.setToolTo('selectSuperContext')
    startGBUndo()
#    cmds.progressBar('progress3DIpol', edit = True, vis = False)
#    if not cmds.button('uvGridBtn',q = True, vis = True):
#        cmds.button('firstUVCBtn', edit = True, vis = False)
        
def firstUVGrid(option):

    cmds.tabLayout('mainTabs', edit = True, en = True,vis = True)
    cmds.button('startDrawBtn', edit = True, vis = True)
#    cmds.button('uvGridBtn', edit = True, vis = False)
#    cmds.button('firstUVCBtn', edit = True, vis = False)
#    cmds.button('mapC2GBtn', edit = True, en = True)
    cmds.button('interCharBtn', edit = True, en = True)
    cmds.radioButton('onGridRadio', edit = True, en = True)
    if option == 'draw':
        cmds.radioButton('onGridRadio', edit = True, select = True)
        cmds.frameLayout('charCM', e = True,vis = False)
        cmds.frameLayout('interpolationFrame', e = True, vis = False)
        cmds.frameLayout('gridCM', e = True,vis = True)
        
    currScalp = cmds.getAttr('gbNode.currentGBNode')
    if not cmds.getAttr(currScalp + '.uvGridCreated'):
        createUVGrid()
        cmds.setAttr(currScalp + '.uvGridCreated', True)
    

def noUVGrid():
    
    cmds.tabLayout('mainTabs', edit = True, en = True,vis = True)
    cmds.button('startDrawBtn', edit = True, vis = True)
    cmds.frameLayout('charCM', edit = True,vis = True)
    cmds.frameLayout('interpolationFrame', e = True, vis = True)
#    cmds.button('uvGridBtn', edit = True, vis = True)
#    cmds.button('firstUVCBtn', edit = True, vis = True)
#    cmds.button('mapC2GBtn', edit = True, en = True)
    cmds.button('interCharBtn', edit = True, en = True)
    cmds.radioButton('onGridRadio', edit = True, en = True)
    cmds.radioButton('onCharRadio', edit = True, en = True, select = True)
    cmds.frameLayout('gridCM', e = True,vis = False)
    cmds.button('cancelAddNewCharacterBtn', edit = True, vis = False)
    cmds.columnLayout('volumeMeshLT', edit = True, vis = False)

#    Useful Tools Procedures

def rebuildSelected():
    
    stopGBUndo()
    selCurves = cmds.ls(sl = True)

    if not selCurves:
        reportGBMessage('No Curves Selected', True, True, 'red')
#        raise RuntimeError, 'Nothing Selected'
    
    cv = cmds.intField('rbCVField', q = True, v = True)
    ch01 = cmds.checkBox('check01', q = True, v = True)
    cmds.setAttr('gbNode.rbCV', cv)
    cmds.setAttr('gbNode.rbP01', ch01)
    kr01 = 0 if ch01 == True else 1
        
    for sel in selCurves:
        selShp = cmds.listRelatives(sel, s = True)
        if not cmds.nodeType(selShp) == 'nurbsCurve':
            selCurves.remove(sel)
        else:
            try:
                cHist = True if cmds.listConnections(selShp, source = True, destination = False) else False
                cmds.rebuildCurve(sel, ch = cHist, s = (cv - cmds.getAttr(sel + '.degree')), rt = 0, rpo = True, kr = kr01)
            except RuntimeError as re:
                reportGBMessage(sel + ' is an Invalid Curve for Rebuild', False, True, 'red')
#                print sel + ' is an Invalid Curve for Rebuild' 
            
    if not selCurves:
        reportGBMessage('No Curves were Selected', True, True, 'red')
#        raise RuntimeError, 'No Curves were Selected'
    startGBUndo()

def checkCVRange():
    
    selCurves = cmds.ls(sl = True)
    cvList = []
    append = cvList.append
    if not selCurves:
        reportGBMessage('No Curves were Selected', True, True, 'red')
#        raise RuntimeError, 'Nothing Selected'
    
    for sel in selCurves:
        selShp = cmds.listRelatives(sel, s = True)
        if not cmds.nodeType(selShp) == 'nurbsCurve':
            selCurves.remove(sel)
        else:
            cv = cmds.getAttr(sel + '.spans') + cmds.getAttr(sel + '.degree')
            append(cv)
            
    if not selCurves:
        reportGBMessage('No Curves were Selected', True, True, 'red')            
#        raise RuntimeError, 'No Curves were Selected'
    
    cmds.intField('minCV', edit = True, en = True, v = min(cvList), ann = str(selCurves[cvList.index(min(cvList))]))
    cmds.intField('maxCV', edit = True, en = True, v = max(cvList), ann = str(selCurves[cvList.index(max(cvList))]))       

def pivotToRoot():
    
    stopGBUndo()

    selCurves = cmds.ls(sl = True)

    if not selCurves:
        reportGBMessage('No Curves were Selected', True, True, 'red')
#        raise RuntimeError, 'Nothing Selected'
    
    for sel in selCurves:
        selShp = cmds.listRelatives(sel, s = True)
        if not cmds.nodeType(selShp) == 'nurbsCurve':
            selCurves.remove(sel)
        else:
            cmds.xform(sel, piv = cmds.xform(sel + '.cv[0]', q = True, ws = True, t = True))
            
    startGBUndo()            


# Tweak Mode

def tweak():
    
    stopGBUndo()
    
    sel = cmds.ls(sl = True)[0]
#    cmds.selectMode(component=True )
#    mm.eval('changeSelectMode -component;')
    cmds.selectType( cv=True )
    mm.eval('manipMoveContext -edit -mode 6 Move;')
    cmds.scriptJob(e = ['SelectionChanged', 'slideCV()'], kws = True, cu = True)
    cmds.scriptJob(e = ['SelectModeChanged', 'killTweak()'], ro = True, kws = True)
    
    startGBUndo()
    
def killTweak():
    all = cmds.scriptJob(lj = True)
    for a in all:
        if 'slideCV' in a:
            cmds.scriptJob(kill = int(a.split(':')[0]))
    mm.eval('manipMoveContext -edit -mode 2 Move;')
    selChar = cmds.getAttr(cmds.getAttr('gbNode.currentGBNode') + '.scalpMesh') + '_DISPLAY'
    cmds.setAttr(selChar + '.overrideEnabled', 1)
    cmds.setAttr(selChar + '.overrideDisplayType', 0)
    
def slideCV():
#    print 'slide'
#    mm.eval('manipMoveContext -edit -mode 6 Move;')
    currNode = cmds.getAttr('gbNode.currentGBNode')
#    selChar = cmds.getAttr(currNode + '.scalpMesh')
    selChar = cmds.getAttr(currNode + '.paintOnMesh')
        
    selCharShp = cmds.listRelatives(selChar, s = True)[0]
    
#    existCPnode = cmds.getAttr(currNode + '.drawMeshCPNode')
    
    
    cvList = cmds.ls(sl = True, fl = True)
    if cvList:
        cv = cvList[0]
    else:
#        cmds.delete(charCPNode)
        return        
#    print cv
    cmds.setAttr(selChar + '_DISPLAY.overrideEnabled', 1)
    cmds.setAttr(selChar + '_DISPLAY.overrideDisplayType', 2)
    
    cvPos = cmds.xform(cv , q = True, ws = True, t = True)
    charCPNode = createCPNode(selChar)
    cmds.setAttr(charCPNode + '.ip', cvPos[0], cvPos[1], cvPos[2])
    faceID = cmds.getAttr(charCPNode + '.f')
    normal = list(cmds.getAttr(charCPNode + '.n')[0])
#    print normal
    face = selChar + '.f[' + str(faceID) + ']'
#    print face
#    cmds.select(cv, r = True)
    cmds.manipMoveContext('Move', edit = True, alignAlong = normal)

#    cvPos = cmds.xform(cv , q = True, ws = True, t = True)
#    cmds.setAttr(charCPNode + '.ip', cvPos[0], cvPos[1], cvPos[2])
#    newPos = cmds.xform(cv, ws = True, t = list(cmds.getAttr(charCPNode + '.p')[0]))
#    cmds.evalDeferred('cmds.select(' + cv + ', r = True)')   
    cmds.delete(charCPNode)

def enterSculptGeoTool():
    
    mm.eval('SculptGeometryToolOptions;')
    cmds.artPuttyCtx(cmds.currentCtx(), edit = True, mtm = 'pull')

def sculptGeoMaxDispUpdate():
    
    ctx = cmds.currentCtx()
    if not 'artPuttyContext' in ctx:
        return
    v = cmds.floatField('htSculptGeoMaxDispFloat', q = True, v = True)
    cmds.artPuttyCtx(ctx, edit = True, maxdisp = v)      


# Create UV Grid
def createUVGrid():
    
    from collections import deque 
    
    
    currNode = cmds.getAttr('gbNode.currentGBNode')
    selChar = cmds.getAttr(currNode + '.scalpMesh')

#    cmds.makeIdentity(selChar, apply = True)

    xmax = cmds.exactWorldBoundingBox(selChar)[3]
        
    pieceList = []
    parts = []
    borderParts = []
    
    planeWidth = int(xmax * 2)
    pName = cmds.nurbsPlane(ax = (0,1,0), w = planeWidth, n = 'UVGrid_' + selChar)
    planeName = pName
    cmds.setAttr(pName[0] + '.visibility', False)
    cmds.parent(pName[0], cmds.getAttr(currNode + '.mainGroup'))
    cmds.setAttr(currNode + '.uvGrid', planeName[0], type = 'string')
    cmds.setAttr('gbNode.activeMesh', planeName[0], type = 'string')
    cmds.setAttr( pName[0] + '.ty',lock = True)

    selCharShp = cmds.listRelatives(selChar, s = True)[0]
    
    
        
    obj = cmds.duplicate(selChar,rc = True)[0]    
    queue = deque ([obj])
    pieceList = []
    
    cmds.setToolTo('selectSuperContext')
    while len(queue) != 0:
        pop = queue.pop()
        nof = cmds.polyEvaluate(pop, f = True)
        cmds.select(pop + '.map[0]',  replace = True)
        mm.eval('polySelectBorderShell 0')
        mm.eval('PolySelectConvert 1')
        x = len(cmds.ls(sl = True, fl = True))
        if x!= nof:
            cmds.polyChipOff(ch = 0, dup = 0, kft = 1)
            parts = cmds.polySeparate(pop, ch = 0)
            for part in parts:
                cmds.select(part, replace = True)
                cmds.polyChipOff(ch = 0, dup = 0, kft = 1)
                queue.append(part)
        else:
            pieceList.append(pop)
    
    
    firstGrp = cmds.group(name = 'polyClubGrp', em = True)
    shellGrp = cmds.group(name = 'shellGrp_' + selChar, em = True)
    cmds.parent(shellGrp, planeName[0])
    
    for piece in pieceList:
        cmds.parent(piece, firstGrp)

    
    
    pBar = False
    if len(pieceList)>1:       
        pBar = True
    if pBar:        
        cmds.text('gbProgressBarText', edit = True, vis = True, label = 'Creating UV Grid') 
        cmds.progressBar('gbProgressBar', edit = True, pr = 0, max = len(pieceList)-1, vis = True)
    
    for piece in pieceList:
        totalM = cmds.polyEvaluate(piece, uv = True)
        cmds.select(piece + '.map[0:' + str(totalM-1) + ']', r = True)
        mm.eval('polySelectBorderShell 1')
        mm.eval('PolySelectConvert 3;')
        borderV = cmds.ls(sl = True, fl = True)
        border = 0
        pS = cmds.listRelatives(piece, s = True)[0]
        for v in borderV:
            maps = cmds.polyListComponentConversion(v, toUV = True)
            if ':' in maps[0] or len(maps)>1:
                border = 1
                break
        singlePiece = 0
        
        if border == 1:
            mm.eval('PolySelectConvert 1')
            bf = len(cmds.ls(sl = True, fl = True))
            pieceF = cmds.polyEvaluate(piece, f = True)
            nonBorderF = pieceF - bf
            
            if bf == pieceF:
                singlePiece = 1
                cmds.select(piece, r = True)
                cmds.polyChipOff(ch = False, kft = False, dup = False)
                xformShell(piece)
                cmds.parent(piece, shellGrp)
#                print 'singlePiece'
                continue
                
            cmds.polyChipOff(ch = True, kft = True, dup = False) 
            parts = cmds.polySeparate(pS, rs = True,ch = False)

            borderParts = []
            for part in parts:
                for v in range(0,(cmds.polyEvaluate(part,v= True)-1)):
                    cmaps = cmds.polyListComponentConversion(part + '.vtx[' + str(v) + ']', fv = True, tuv = True)
                    if ':' in cmaps[0] or len(cmaps) > 1:
                        cmds.select(part, r = True)
                        cmds.polyChipOff(ch = False, kft = False, dup = False)
                        continue
            
            for p in parts:
                xformShell(p)
            
           
            newPiece = cmds.polyUnite(piece)[0]
            cmds.delete(piece)
            newPieceShp = cmds.listRelatives(newPiece, s = True)[0]
#            cmds.polyMergeVertex(newPiece, d = 0, am = True, ch = False)
            sNode = cmds.shadingNode('lambert', asShader = True)
            sgNode = cmds.sets(renderable = True, noSurfaceShader = True, empty = True, name = sNode+'SG')
            cmds.connectAttr(sNode + '.outColor', sgNode + '.surfaceShader',force = True)
            cmds.sets(newPieceShp, edit = True, forceElement = sgNode)
            lockXform(newPiece)
            cmds.parent(newPiece, shellGrp)

        elif border == 0 or len(pieceList) == 1:
            singlePiece = 1
            xformShell(piece)
            cmds.parent(piece, shellGrp)
    
        if pBar:              
            cmds.progressBar('gbProgressBar', edit = True, s = 1)

    if singlePiece == 0:
        if cmds.objExists(obj):
            cmds.delete(obj)
            
    for each in (cmds.listRelatives(shellGrp, c = True)):
        each = cmds.rename(each, 'uvShell_' + selChar + '_1')
        cmds.select(each, replace = True)
        cmds.polyMergeVertex(each, d = 0.001, am = True, ch = False)
        cmds.polyMergeUV(each, ch = False)
        cmds.select(cl = True)
    cmds.setAttr(currNode + '.uvGridCreated', True)

    if cmds.objExists(firstGrp):
        cmds.delete(firstGrp)
    

    xshift = xmax * 2.25
    cmds.xform(planeName, a = True, t = [xshift, 0 , 0])
        
    if pBar:
        cmds.text('gbProgressBarText', edit = True, vis = False)
        cmds.progressBar('gbProgressBar', edit = True, vis = False)
        cmds.progressBar('gbProgressBar', edit = True, pr = 0)
           

def xformShell(poly):
    pc = poly        
    selChar = cmds.getAttr('gbNode.activeMesh')
    currNode = cmds.getAttr('gbNode.currentGBNode')
    planeName = cmds.getAttr(currNode + '.uvGrid')
#    piece = cmds.rename(pc, selChar + '_uvShell_1')
    piece = pc
    vPiece = cmds.polyEvaluate(piece, v = True)
    for v in range(0,vPiece):
        mapID = cmds.polyListComponentConversion(piece + '.vtx[' + str(v) + ']', fv = True, tuv = True)
        uv = cmds.polyEditUV(mapID,q = True)
        cpU = round(uv[0], 6)
        cpV = round(uv[1], 6)
        newXYZ = cmds.pointOnSurface( planeName , u= cpU, v= cpV, position=True)
        cmds.xform(piece + '.vtx[' + str(v) + ']', ws = True, t = tuple(newXYZ))
        lockXform(piece)
    cmds.polySetToFaceNormal(piece)
                                                
def lockXform(piece):
    cmds.setAttr(piece + '.tx', lock = True)
    cmds.setAttr(piece + '.ty', lock = True)
    cmds.setAttr(piece + '.tz', lock = True)
    cmds.setAttr(piece + '.rx', lock = True)
    cmds.setAttr(piece + '.ry', lock = True)
    cmds.setAttr(piece + '.rz', lock = True)
    cmds.setAttr(piece + '.sx', lock = True)
    cmds.setAttr(piece + '.sy', lock = True)
    cmds.setAttr(piece + '.sz', lock = True)    

def createFollicle(whichMesh):
    
    currNode = cmds.getAttr('gbNode.currentGBNode')
    baseMeshGrp = cmds.getAttr(currNode + '.baseMeshGroup')
    
    mesh = cmds.getAttr(currNode + '.' + whichMesh)
    
    meshShp = cmds.listRelatives(mesh, s = True)[0]
    follT = cmds.createNode('transform' , name = mesh + 'follicle', parent = baseMeshGrp)
    follShp = cmds.createNode('follicle', name = follT + 'Shp', parent = follT)
    uv = cmds.polyEditUV( mesh + '.map[0]', query=True )
    cmds.connectAttr(meshShp + '.worldMatrix[0]', follShp + '.inputWorldMatrix')
    cmds.connectAttr(meshShp + '.worldMesh[0]', follShp + '.inputMesh')
    cmds.connectAttr(follShp + '.outRotate', follT + '.rotate')
    cmds.connectAttr(follShp + '.outTranslate', follT + '.translate')    
    cmds.setAttr(follShp + '.parameterU', uv[0])
    cmds.setAttr(follShp + '.parameterV', uv[1])
    cmds.setAttr(follT + '.visibility', False)
    cmds.setAttr(currNode + '.' + whichMesh + 'Follicle', follT, type = 'string')
    
    return follT

def createFollicleOtherMesh(mesh):
    
        
    meshShp = cmds.listRelatives(mesh, s = True)[0]
    follT = cmds.createNode('transform' , name = mesh + '_follicle')
    follShp = cmds.createNode('follicle', name = follT + 'Shp', parent = follT)
    uv = cmds.polyEditUV( mesh + '.map[0]', query=True )
    cmds.connectAttr(meshShp + '.worldMatrix[0]', follShp + '.inputWorldMatrix')
    cmds.connectAttr(meshShp + '.worldMesh[0]', follShp + '.inputMesh')
    cmds.connectAttr(follShp + '.outRotate', follT + '.rotate')
    cmds.connectAttr(follShp + '.outTranslate', follT + '.translate')    
    cmds.setAttr(follShp + '.parameterU', uv[0])
    cmds.setAttr(follShp + '.parameterV', uv[1])
    cmds.setAttr(follT + '.visibility', False)
    
    return follT


def createFollicleHAIR(whichMesh):
    
    
    currNode = cmds.getAttr('gbNode.currentGBNode')
    poly = cmds.getAttr(currNode + '.' + whichMesh)
    
    dupBaseMesh = poly
    cmds.select (dupBaseMesh + '.f[0]', r = True)
    mm.eval('createHair 8 8 10 0 0 0 0 5 0 2 2 2;')
    baseMeshGrp = cmds.getAttr(currNode + '.baseMeshGroup')

    dupBaseShp = cmds.listRelatives(dupBaseMesh, s = True)[0]
    follName = cmds.listConnections(dupBaseShp, t = 'follicle', et = True)
    follShp = cmds.listRelatives(follName[0], s = True)
    hairSys = cmds.listConnections(follShp[0], t = 'hairSystem', et = True)
    cmds.delete(hairSys[0])
    bothCurves = cmds.listConnections(follShp[0], t = 'nurbsCurve', et = True)
    cmds.delete(bothCurves[0])
    curvGrp = cmds.listRelatives(bothCurves[1], p = True)
    cmds.delete(curvGrp[0])
    cmds.hide(follName[0])
    follGrp = cmds.listRelatives(follName[0], p = True)
    cmds.parent(follGrp, baseMeshGrp)
    cmds.rename(follGrp, 'hairFollicle_' + poly)
    cmds.setAttr(currNode + '.' + whichMesh + 'Follicle', follName[0], type = 'string')
    return follName[0]
    
def createCPSNode(obj):
    
    objShp = cmds.listRelatives(obj, s = True)[0]
    cpsNode = cmds.createNode('closestPointOnSurface', ss = True)
    cmds.connectAttr(objShp + '.worldSpace', cpsNode + '.inputSurface')
    return cpsNode

def swapCurvesBetweenMeshAndUVGrid():
    
    stopGBUndo()
    currNode = cmds.getAttr('gbNode.currentGBNode')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    selList = cmds.ls(os = True)
    
    uvGrid = cmds.getAttr(currNode + '.uvGrid')
    gridCPNode = createCPSNode(uvGrid)
    historyDelete.append(gridCPNode)
    selCurves = [crv for crv in selList if cmds.ls(cmds.listRelatives(crv, s = True), et = 'nurbsCurve')]
    if not selCurves:
        reportGBMessage('Please Select Curves to Swap', True, True, 'red')
    
    
    historyDelete = []
    
    charCPNode = createCPNode(scalpMesh)
    historyDelete.append(charCPNode)
    
    testCrv = selCurves[0]
    rootPos = cmds.pointPosition(testCrv + '.cv[0]')
    cmds.setAttr(charCPNode + '.ip', rootPos[0], rootPos[1], rootPos[2])
    charDist = distance3d(rootPos, list(cmds.getAttr(charCPNode + '.p')[0]))
    
    cmds.setAttr(gridCPNode + '.ip', rootPos[0], rootPos[1], rootPos[2])
    gridDist = distance3d(rootPos, list(cmds.getAttr(gridCPNode + '.p')[0]))
    
    charToGrid = False
    if charDist <= gridDist:
        charToGrid = True
        
    threshold = 1.0
    finalCurves = []
    for crv in selCurves:
        rootPos = cmds.pointPosition(crv + '.cv[0]')
        
        if charToGrid:
            cmds.setAttr(charCPNode + '.ip', rootPos[0], rootPos[1], rootPos[2])
            charDist = distance3d(rootPos, list(cmds.getAttr(charCPNode + '.p')[0]))
            if charDist > threshold:
                reportGBMessage(crv + ' Skipped as far from Character Mesh', False, False, 'yellow')
#                raise RuntimeWarning, crv + ' Skipped as far from Character Mesh'
                continue
            else:
                finalCurves.append(crv)                
        else:    
            cmds.setAttr(gridCPNode + '.ip', rootPos[0], rootPos[1], rootPos[2])
            gridDist = distance3d(rootPos, list(cmds.getAttr(gridCPNode + '.p')[0]))
            if gridDist > threshold:
                reportGBMessage(crv + ' Skipped as far from UV Grid', False, False, 'yellow')                
#                raise RuntimeWarning, crv + ' Skipped as far from UV Grid'
                continue
            else:
                finalCurves.append(crv)                
     
    cmds.select(finalCurves, r = True)
    cmds.undoInfo(swf = False)
    if charToGrid:
        mapCharGrid(1)
    else:
        autoMap(1)         
    
    for h in historyDelete:
        if cmds.objExists(h):
            cmds.delete(h)
                    
    cmds.undoInfo(swf = True)                
    startGBUndo()
     

    
# Auto Map from Grid to Character

def autoMap(ip):
    
    curvePosBake = []
    sourceUV = []
    sourceCharVtx = []
    sourceCharMap = []
    uvPos = []
    restCurvePos = []
    toBeJoinedList = []
    xList = []
    todelete = []
    origCurves = []
    origCurveBakePos = []
    gCurves = []
    historyDelete = []


    currNode = cmds.getAttr('gbNode.currentGBNode')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    
#    gCur = cmds.ls(sl = True)
    gCur = cmds.listRelatives(cmds.listRelatives(cmds.ls(sl = True), ad = True, typ = 'nurbsCurve'), p = True)
    if not gCur:
        cmds.undoInfo(swf = True)
        reportGBMessage('No Curves Selected', True, True, 'red')
#        raise RuntimeError, 'No Curves Selected'
    
    if cmds.getAttr(currNode + '.paintOnMesh') == cmds.getAttr(currNode + '.volumeMesh'):
        switchCurvesToOtherMesh()
        cmds.setAttr(currNode + '.paintOnMesh', cmds.getAttr(currNode + '.scalpMesh'), type = 'string')
    
    selChar = cmds.getAttr(currNode + '.paintOnMesh')
        
    baseMeshGrp = cmds.getAttr(currNode + '.baseMeshGroup')
    for g in range(0, len(gCur)):
        if cmds.ls(cmds.listRelatives(gCur[g], s = True), et = 'nurbsCurve'):
            if ip == 1:
                if not cmds.objExists('superCurves_charInterpolation_' + scalpMesh):
                    cmds.group(em = True, name = 'superCurves_charInterpolation_' + scalpMesh, parent = baseMeshGrp)
                cmds.parent(gCur[g], 'superCurves_charInterpolation_' + scalpMesh)
                gCurves.append(gCur[g])
            else:
                gCurves.append(gCur[g])
                
    gCurvesDup = []
    for g in gCurves:
        gCurvesDup.append(g)
    
    pName = cmds.getAttr(currNode + '.uvGrid')
    planeName = pName
    charFoll = createFollicleOtherMesh(selChar)
    historyDelete.append(charFoll)
    
    pRel = cmds.listRelatives(pName, s= True)
    checkCP = cmds.listConnections(pRel[0], type = 'closestPointOnSurface')
    if not checkCP:
        cPMNode = cmds.createNode('closestPointOnSurface')
        cmds.connectAttr(pRel[0]+ '.worldSpace', cPMNode + '.inputSurface')
    else:
        cPMNode = checkCP[0]
    
    historyDelete.append(cPMNode)

    originLoc = cmds.spaceLocator(n = 'originLoc')
    tempLoc = cmds.spaceLocator(n = 'tempLoc')
    rLoc = cmds.spaceLocator(n = 'rLoc')[0]
    sourceCurve = cmds.curve( p = [[0,0,0],[0,0,0]], d = 1, n = 'sourceCurve')
    destCurve = cmds.curve( p = [[0,0,0],[0,0,0]], d = 1, n = 'destCurve')
    tempCurve = cmds.curve( p = [[0,0,0],[0,0,0]], d = 1, n = 'tempCurve')

    selCharShp = cmds.listRelatives(selChar, s = True)[0]
    charCPnode = createCPNode(selChar)
    historyDelete.append(charCPnode)
    
    shellGrp = cmds.listRelatives(planeName, c = True)[1]
    allpShells = cmds.listRelatives(shellGrp, c = True)
    
    shellCPNodesList = cpNodesForAllShells()
    for shellN in shellCPNodesList:
        historyDelete.append(shellN)
    
    dqshellCPNodesList = deque(shellCPNodesList)
    dqallpShells = deque(allpShells)
    
    
    for eachC in gCurves:
        
        if eachC.count('_restPart') == 5:
            
            xList = []
            eC = eachC.split('_restPart')[0]
            
            todelete = []
            for tt in toBeJoinedList:
                for ttt in tt:
                    if eC in ttt:
                        if not eC == ttt:
                            todelete.append(ttt)
                        xList.append(tt)
                        
            for x in xList:
                if xList.count(x) == 2:
                    xList.remove(x)
            
            for x in xList:
                toBeJoinedList.pop(toBeJoinedList.index(x))
            
            todel = set(todelete)

            for d in todel:
                if cmds.objExists(d):
                    cmds.delete(d)
            
            ind = origCurves.index(eC)
            bakePos = origCurveBakePos[ind]
            ncvOnly = cmds.getAttr(eC + '.spans') + cmds.getAttr(eC + '.degree')

            if ncvOnly < 5:
                cmds.delete(eC)
                cmds.curve(n = eC, p = bakePos)
            else:
                cmds.curve(eC, r = True, p = bakePos)

            if not cmds.objExists('unableToMap'):
                cmds.group(n = 'unableToMap', em = True)
                cmds.setAttr('unableToMap.visibility', False)

            cmds.parent(eC, 'unableToMap')
                
            continue
            
        if 'ipolCrv_' in eachC:           
            eachCShp = cmds.listRelatives(eachC,s = True)
            blndNode = cmds.listConnections(eachCShp, et  = 1, t = 'blendShape')
            if blndNode is not None:
                blndCurves = cmds.ls(cmds.listConnections(blndNode, et = 1, t = 'nurbsCurve'),fl = True)
                if len(blndCurves) > 0:
                    if eachC in blndCurves:
                        blndCurves.remove(eachC)
                    if len(blndCurves) > 0:
                        cmds.delete(blndCurves)
                
        
        cmds.delete(eachC, ch = True)

        sp = cmds.getAttr(eachC +'.spans')
        dg = cmds.getAttr(eachC +'.degree') 
        ncv = sp + dg
        curvePosBake = []
        for i in range(0,ncv):
            curvePosBake.append(cmds.xform(eachC + '.cv[' + str(i) + ']', q = True, ws = True, t = True))
        for cv in range(0,ncv):
            cvXYZ = []
            cvXYZ = cmds.xform(eachC + '.cv[' + str(cv) + ']', q = True, ws = True, t = True)
            
            if cv == 0:
                rootXYZ = cvXYZ
            
                           
            cmds.setAttr(cPMNode+'.ip',cvXYZ[0],cvXYZ[1],cvXYZ[2])
            cpU = cmds.getAttr(cPMNode+'.u')
            cpV = cmds.getAttr(cPMNode+'.v')

            cmds.setAttr(charFoll+ '.parameterU',cpU)
            cmds.setAttr(charFoll + '.parameterV',cpV)
            fcXYZ = cmds.xform(charFoll, q = True, ws = True, t = True) 
            
            if fcXYZ[0] == 0 and fcXYZ[1] == 0:

                for n in range(0,len(dqshellCPNodesList)):
                    cmds.setAttr((dqshellCPNodesList[n] + '.ip'),rootXYZ[0], rootXYZ[1], rootXYZ[2])
                    tupleP = cmds.getAttr(dqshellCPNodesList[n]+ '.p')
                    dX = abs(round((rootXYZ[0] - tupleP[0][0]),4))
                    dZ = abs(round((rootXYZ[2] - tupleP[0][2]),4))
                    onShell = 0
                    if (dX+dZ) <= 0.1:
                        onShell = 1
                        distXZ = dX+dZ
                        shell = dqallpShells[n]
                        shellCPNode = dqshellCPNodesList[n]
                        if n!= 0:
                            dqallpShells.rotate(-n)
                            dqshellCPNodesList.rotate(-n)
                        break
                closeDist = 10000
                if onShell == 0:
                    for n in range(0,len(dqshellCPNodesList)):
                        cmds.setAttr((dqshellCPNodesList[n] + '.ip'),rootXYZ[0], rootXYZ[1], rootXYZ[2])
                        tupleP = cmds.getAttr(dqshellCPNodesList[n]+ '.p')
                        dX1 = abs(round((rootXYZ[0] - tupleP[0][0]),4))
                        dZ1 = abs(round((rootXYZ[2] - tupleP[0][2]),4))
                        
                        if (dX1+dZ1) < closeDist:
                            closeDist = dX1+dZ1
                            shell = dqallpShells[n]
                            shellCPNode = dqshellCPNodesList[n]
                            
                closestXYZ = cmds.getAttr(shellCPNode + '.p')
                dXC = abs(round((cvXYZ[0] - closestXYZ[0][0]),5))
                dZC = abs(round((cvXYZ[2] - closestXYZ[0][2]),5))
                
                
                if (dXC+dZC) <= 0.01:

                    cpUC = cmds.getAttr(shellCPNode+'.u')
                    cpVC = cmds.getAttr(shellCPNode+'.v')
                    cmds.setAttr(charFoll+ '.parameterU',cpUC)
                    cmds.setAttr(charFoll + '.parameterV',cpVC)
                    fcXYZ = cmds.xform(charFoll, q = True, ws = True, t = True)
                    cmds.xform(eachC + '.cv[' + str(cv) + ']', ws = True, t = tuple(fcXYZ))
                    if cv == 0 and '_restPart' not in eachC:
                        cmds.xform(eachC, piv = fcXYZ)
                    continue 
                
                cmds.setAttr(shellCPNode + '.ip', cvXYZ[0],cvXYZ[1],cvXYZ[2])
                
                sourceShell0U = cmds.getAttr(shellCPNode + '.u')
                sourceShell0V = cmds.getAttr(shellCPNode + '.v')
                faceId = cmds.getAttr(shellCPNode + '.f')

                sourceShellVtxId0 = getClosestVtx(shell, faceId, cvXYZ) 
                faceToEdges = cmds.ls(cmds.polyListComponentConversion(shell + '.f[' + str(faceId) + ']', ff = True, te = True),fl = True)

                cmds.select(faceToEdges, r = True)
                mm.eval('ConvertSelectionToShellBorder')
                
                borderEdges = cmds.ls(sl = True, fl = True)
                if len(borderEdges) == 0:
                    if eachC.count('_restPart') > 0:
                        xList = []
                        eC = eachC.split('_restPart')[0]
                    else:
                        eC = eachC
                        
                    todelete = []
                    for tt in toBeJoinedList:
                        for ttt in tt:
                            if eC in ttt:
                                if not eC == ttt:
                                    todelete.append(ttt)
                                xList.append(tt)

                    
                    for x in xList:
                        if xList.count(x) == 2:
                            xList.remove(x)

                        
                    for x in xList:
                        toBeJoinedList.pop(toBeJoinedList.index(x))

                        
                    todel = set(todelete)

                    for d in todel:
                        if cmds.objExists(d):
                           cmds.delete(d)
                    
                    if eC == eachC:
                        bakePos = curvePosBake
                    else:    
                        ind = origCurves.index(eC)
                        bakePos = origCurveBakePos[ind]

                    if cmds.objExists(eC):
                        cmds.delete(eC)
                    newCurve = cmds.curve(p = bakePos)
                    cmds.rename(newCurve, eC)
                    
                    if not cmds.objExists('unableToMap'):
                        cmds.group(n = 'unableToMap', em = True)
                        cmds.setAttr('unableToMap.visibility', False)
                       
                    cmds.delete(eC, ch = True)
                    cmds.parent(eC, 'unableToMap')
                    break
                    

                cmds.select(cl = True)
                faceEdges = faceToEdges
                
                faceToEdges = []
                for e in range(0, len(faceEdges)):
                    for f in range(0, len(borderEdges)):
                        if faceEdges[e] == borderEdges[f]:
                            faceToEdges.append(faceEdges[e])
                            
                
                gotEdge = 0
                if len(faceToEdges) == 0:
                    connEdges = cmds.ls(cmds.polyListComponentConversion(sourceShellVtxId0, fv = True, te = True),fl = True)
                    for conn in connEdges:
                        if conn in borderEdges:
                            shellSourceEdge = conn
                    gotEdge = 1

                if len(faceToEdges) == 1:
                    gotEdge = 1
                    shellSourceEdge = faceToEdges[0]
                else:
                    if cv > 0:
                        lastCVPos = curvePosBake[cv-1]
                        
                        A = [lastCVPos[0], lastCVPos[2]]
                        B = [cvXYZ[0], cvXYZ[2]]
                        for edge in faceToEdges:
                            
                            edgePos = cmds.xform(edge, q = True, ws = True, t = True)
                            C = [edgePos[0], edgePos[2]]
                            D = [edgePos[3], edgePos[5]]
                            
                            result = inter(A,B,C,D)
                            if result is True:
                                gotEdge = 1
                                shellSourceEdge = edge
                                break
                                
                    if gotEdge == 0 or cv == 0:
                        distCDB = []
                        B = [cvXYZ[0], cvXYZ[2]]
                        if len(faceToEdges) > 1:
                            for edge in faceToEdges:
                                edgePos = cmds.xform(edge, q = True, ws = True, t = True)
                                C = [edgePos[0], edgePos[2]]
                                D = [edgePos[3], edgePos[5]]
                                distCB = distance(C,B)
                                distDB = distance(D,B)
                                distCDB.append(distCB + distDB)                        
                            minDist = max(distCDB)
                            minPos = [i for i, j in enumerate(distCDB) if j == minDist]
                            shellSourceEdge = faceToEdges[minPos[0]]
                        else:
                            if gotEdge == 0:
                                shellSourceEdge =  faceToEdges[0]                   
                
                sourceEdgeToVtx = cmds.ls(cmds.polyListComponentConversion(shellSourceEdge, fe = True, tv = True),fl = True)
                sourceUV = []
                sourceCharVtx = []
                sourceCharMap = []
                sourceShellVtx = sourceEdgeToVtx
                fallback = 0
                edgeOnChar = []
                for i in range(0,2):
                    sourceUV.append(cmds.polyEditUV(cmds.ls(cmds.polyListComponentConversion(sourceShellVtx[i], fv = True, tuv = True),fl = True), q = True))
                    sourceUV[i] = list(set(sourceUV[i]))
                    if len(sourceUV[i])<2:
                        fallback = 1
                        break
                    else:

                        cmds.setAttr(charFoll+ '.parameterU',sourceUV[i][0])
                        cmds.setAttr(charFoll + '.parameterV',sourceUV[i][1])
                        cXYZ = cmds.xform(charFoll, q = True, ws = True, t = True)
                        cmds.setAttr(charCPnode + '.ip', cXYZ[0], cXYZ[1], cXYZ[2])

                        closesCharVtx = getClosestVtx(selChar, cmds.getAttr(charCPnode + '.f'),cXYZ)
                        sourceCharVtx.append(closesCharVtx)
                        sourceCharMap.append(cmds.ls(cmds.polyListComponentConversion(sourceCharVtx[i], fv = True, tuv = True),fl = True))
                
                
                if fallback == 0:
                    edgeOnChar = cmds.polyListComponentConversion(sourceCharVtx, fv = True, te = True,internal = True)
                
                mapUVRemove = []
                if len(edgeOnChar) == 0 or fallback == 1:
                    fallback = 1
                else:
                    edgeToMapOnChar = cmds.ls(cmds.polyListComponentConversion(edgeOnChar, fe = True, tuv = True),fl = True)
                
                
                    mapToUVChar = []
                    for map in edgeToMapOnChar:
                        mapToUVChar.append(cmds.polyEditUV(map, query = True))
                    
                                
                    mapUVRemove = []
                    edgetomapRemove = []
                    for uv in range(0, len(mapToUVChar)):
                        if mapToUVChar[uv] in sourceUV:
                            mapUVRemove.append(mapToUVChar[uv])
                            edgetomapRemove.append(edgeToMapOnChar[uv])
                        
                if len(mapUVRemove) < 2 or fallback == 1:

                    if eachC.count('_restPart') > 0:
                        xList = []
                        eC = eachC.split('_restPart')[0]
                    else:
                        eC = eachC
                        
                    todelete = []
                    for tt in toBeJoinedList:
                        for ttt in tt:
                            if eC in ttt:
                                if not eC == ttt:
                                    todelete.append(ttt)
                                xList.append(tt)

                    
                    for x in xList:
                        if xList.count(x) == 2:
                            xList.remove(x)

                        
                    for x in xList:
                        toBeJoinedList.pop(toBeJoinedList.index(x))

                        
                    todel = set(todelete)

                    for d in todel:
                        if cmds.objExists(d):
                           cmds.delete(d)
                    
                    if eC == eachC:
                        bakePos = curvePosBake
                    else:    
                        ind = origCurves.index(eC)
                        bakePos = origCurveBakePos[ind]

                    if cmds.objExists(eC):
                        cmds.delete(eC)
                    newCurve = cmds.curve(p = bakePos)
                    cmds.rename(newCurve, eC)
                    
                    if not cmds.objExists('unableToMap'):
                        cmds.group(n = 'unableToMap', em = True)
                        cmds.setAttr('unableToMap.visibility', False)
                    cmds.delete(eC, ch = True)

                    cmds.parent(eC, 'unableToMap')
                        
                    break
                    
                for p in range(0,2):

                    mapToUVChar.remove(mapUVRemove[p])
                    edgeToMapOnChar.remove(edgetomapRemove[p])
                
                if len(edgeToMapOnChar) == 1:
                    for sv in range(0,2):
                        v2m = cmds.ls(cmds.polyListComponentConversion(sourceCharVtx[sv], fv = True, tuv = True),fl = True)
                        if len(v2m) == 1:
                            edgeToMapOnChar.append(v2m)
                            mapToUVChar.append(cmds.polyEditUV(v2m,query = True))
                
                if len(edgeToMapOnChar) == 0:
                    if eachC.count('_restPart') > 0:
                        xList = []
                        eC = eachC.split('_restPart')[0]
                    else:
                        eC = eachC
                        
                    todelete = []
                    for tt in toBeJoinedList:
                        for ttt in tt:
                            if eC in ttt:
                                if not eC == ttt:
                                    todelete.append(ttt)
                                xList.append(tt)

                    
                    for x in xList:
                        if xList.count(x) == 2:
                            xList.remove(x)

                        
                    for x in xList:
                        toBeJoinedList.pop(toBeJoinedList.index(x))

                        
                    todel = set(todelete)

                    for d in todel:
                        if cmds.objExists(d):
                           cmds.delete(d)
                    
                    if eC == eachC:
                        bakePos = curvePosBake
                    else:    
                        ind = origCurves.index(eC)
                        bakePos = origCurveBakePos[ind]

                    if cmds.objExists(eC):
                        cmds.delete(eC)
                    newCurve = cmds.curve(p = bakePos)
                    cmds.rename(newCurve, eC)
                    
                    if not cmds.objExists('unableToMap'):
                        cmds.group(n = 'unableToMap', em = True)
                        cmds.setAttr('unableToMap.visibility', False)
                    cmds.delete(eC, ch = True)

                    cmds.parent(eC, 'unableToMap')
                        
                    break
                            
                    
                vtxCheck = cmds.polyListComponentConversion(edgeToMapOnChar[0], fuv = True, tv = True)
                

                if vtxCheck[0] == sourceCharVtx[0]:
                    destUVPos = mapToUVChar
                elif vtxCheck[0] == sourceCharVtx[1]:
                    mapToUVChar.reverse()
                    destUVPos = mapToUVChar
                
                srcXYZ0 = cmds.pointOnSurface(planeName, u = sourceUV[0][0], v = sourceUV[0][1], position = True)
                srcXYZ1 = cmds.pointOnSurface(planeName, u = sourceUV[1][0], v = sourceUV[1][1], position = True)                    
                
                cmds.xform(sourceCurve + '.cv[0]', ws = True, t = srcXYZ0)
                cmds.xform(sourceCurve + '.cv[1]', ws = True, t = srcXYZ1)
                cmds.xform(sourceCurve, ws = True, rp = srcXYZ0, sp = srcXYZ0)

                destXYZ0 = cmds.pointOnSurface(planeName, u = destUVPos[0][0], v = destUVPos[0][1], position = True)
                destXYZ1 = cmds.pointOnSurface(planeName, u = destUVPos[1][0], v = destUVPos[1][1], position = True)
                
                cmds.xform(destCurve + '.cv[0]', ws = True, t = destXYZ0)
                cmds.xform(destCurve + '.cv[1]', ws = True, t = destXYZ1)
                cmds.xform(destCurve, ws = True, rp = destXYZ0,sp = destXYZ0)
                
                cmds.xform(tempLoc, ws = True, t = destXYZ0)
                
                
                restCurvePos = []
                
                for c in range(cv,ncv):
                    cvPos = cmds.xform(eachC + '.cv[' + str(c) + ']', q = True, ws = True, t = True)
                    restCurvePos.append(cvPos)
                
                if ncv-cv <=4:
                    degree = ncv - cv - 1
                else:
                    degree = 3 
                    
                restCurve = cmds.curve(p = restCurvePos, d = degree, n = 'restCurve')
                cmds.xform(restCurve, ws = True, rp = restCurvePos[0], sp = restCurvePos[0])
                
                
                cmds.parent(restCurve, sourceCurve)

                
                pCs = cmds.pointConstraint(originLoc, sourceCurve, mo = 0)
                cmds.delete(pCs)
                pCd = cmds.pointConstraint(originLoc, destCurve, mo = 0)
                cmds.delete(pCd)
                
                
                srcCV1Pos = cmds.xform(sourceCurve + '.cv[1]',q = True, ws = True, t = True)
                destCV1Pos = cmds.xform(destCurve + '.cv[1]',q = True, ws = True, t = True)
               
                
                rot = cmds.angleBetween(euler = True, v1 = tuple(srcCV1Pos), v2 = tuple(destCV1Pos))
                cmds.xform(sourceCurve, ws = True, ro = rot)
            
                pC = cmds.pointConstraint(tempLoc, sourceCurve, mo = 0)
                cmds.delete(pC)
                reversed = 0
                for j in range(0,ncv-cv):

                    origXYZ = cmds.xform(eachC + '.cv[' + str(j+cv) + ']', q = True, ws = True, t = True)
                    cmds.setAttr((shellCPNode + '.ip'),origXYZ[0], origXYZ[1], origXYZ[2])
                    tupleP = cmds.getAttr(shellCPNode + '.p')
                    dX = abs(round((origXYZ[0] - tupleP[0][0]),7))
                    dZ = abs(round((origXYZ[2] - tupleP[0][2]),7))
                  
                    if (dX+dZ) == 0.0:
                        
                        cpUj = cmds.getAttr(shellCPNode+'.u')
                        cpVj = cmds.getAttr(shellCPNode+'.v')
                    else:
       
                        jXYZ = cmds.xform(restCurve + '.cv[' + str(j) + ']', q = True, ws = True, t = True)
                        cmds.setAttr(cPMNode+'.ip',jXYZ[0],jXYZ[1],jXYZ[2])
                        cpUj = cmds.getAttr(cPMNode+'.u')
                        cpVj = cmds.getAttr(cPMNode+'.v')
                    cmds.setAttr(charFoll + '.parameterU',cpUj)
                    cmds.setAttr(charFoll + '.parameterV',cpVj)
                    fcXYZj = cmds.xform(charFoll, q = True, ws = True, t = True)
                    
                    if fcXYZj[0] == 0 and fcXYZj[1] == 0:
                        
                        againRestCurvePos =  []                        
                        for m in range(j,ncv-cv):
                            posM = cmds.xform(restCurve + '.cv[' + str(m) + ']', q = True, ws = True, t = True)
                            againRestCurvePos.append(posM)
                        if ncv-cv-j <= 4:
                            degree = ncv - cv - j - 1
                        else:
                            degree = 3
                            
                        if degree == 0:
                            degree = 1
                        
                        if len(againRestCurvePos) == 1:
                            againRestCurvePos.append(againRestCurvePos[0])
                            againRestCurvePos.append(againRestCurvePos[0])
                        
                        if not '_restPart' in eachC:
                            origCurves.append(eachC)
                            origCurveBakePos.append(curvePosBake)    
                        againRestCurve = cmds.curve(p = againRestCurvePos, d = degree, n = eachC + '_restPart')
                        cmds.xform(againRestCurve, ws = True, rp = againRestCurvePos[0], sp = againRestCurvePos[0])

                        cmds.delete(eachC + '.cv[' + str(j+cv) + ':' + str(ncv-1) + ']' )
                        
                        gCurves.append(againRestCurve)
                        toBeJoinedList.append([eachC, againRestCurve])
                        break
                            
                    cmds.xform(eachC + '.cv[' + str(j+cv) + ']', ws = True, t = tuple(fcXYZj))

                cmds.delete(restCurve)
                cmds.delete(sourceCurve,ch = True)
                cmds.makeIdentity(sourceCurve, apply = True)
                    
                break
                
            cmds.xform(eachC + '.cv[' + str(cv) + ']', ws = True, t = tuple(fcXYZ))
            if cv == 0 and '_restPart' not in eachC:
                cmds.xform(eachC,piv = fcXYZ)
    cmds.delete(originLoc, tempLoc, sourceCurve, destCurve, rLoc,tempCurve)
         
    
    for o in range(len(toBeJoinedList)-1,-1,-1):

        mainCurve = toBeJoinedList[o][0]
        curvePart = toBeJoinedList[o][1]

        sp = cmds.getAttr(curvePart +'.spans')
        dg = cmds.getAttr(curvePart +'.degree') 
        ncvPart = sp + dg
        spM = cmds.getAttr(mainCurve +'.spans')
        dgM = cmds.getAttr(mainCurve +'.degree')
        ncvM = spM + dgM
        if ncvM == 0:
            if '_restPart' in mainCurve:
                if ncvPart > 0:
                    toBeJoinedList[o][0] = ''
                    for t in range(0,len(toBeJoinedList)):
                        for tt in range(0,len(toBeJoinedList[t])):
                            if toBeJoinedList[t][tt] == mainCurve:
                                toBeJoinedList[t][tt] = curvePart

                    cmds.delete(mainCurve)
                    continue
                else:
                    continue
            else:
                cmds.delete(mainCurve)
                cmds.rename(curvePart, mainCurve)
                continue
        if ncvPart == 0:
#            print 'zero curve'
            continue
        if ncvM < 4:
            rootM = cmds.xform(mainCurve + '.cv[' + str(ncvM-1) + ']', q = True, ws = True, t = True)
            for q in range(ncvM, 4):
                cmds.curve(mainCurve, a = True, p = rootM)
        for p in range(0,ncvPart):
                
            pPos = cmds.xform(curvePart + '.cv[' + str(p) + ']', q = True, ws = True, t = True)
            cmds.curve(mainCurve, a = True, p = pPos)
            if '_restPart' not in mainCurve:
                cmds.xform(mainCurve, piv = (cmds.xform(mainCurve + '.cv[0]', q = True, ws = True, t = True)))
        cmds.delete(curvePart)
    
    for h in historyDelete:
        if cmds.objExists(h):
            cmds.delete(h)
               
    oddCurvesCheck(gCurvesDup)
    cmds.undoInfo(swf = True)
    
def oddCurvesCheck(curveGrp):
    
    unableGrp = []
    if cmds.objExists('unableToMap'):
        unableGrp = cmds.ls(cmds.listRelatives('unableToMap', c = True),fl = True)
        
        
    for crv in curveGrp:
        if len(unableGrp) > 0:
            if crv in unableGrp:
                continue
        if not cmds.objExists(crv):
            continue
        s = cmds.getAttr(crv + '.spans')
        d = cmds.getAttr(crv + '.degree')
        n = s + d
        dist = []
        allPos = []
        for c in range(0,n):
            allPos.append(cmds.xform(crv + '.cv[' + str(c) + ']', q = True, ws = True, t = True))
        for c in range(0,n-1):
            dist.append(distance3d(allPos[c], allPos[c+1]))
#        print 'len ', len(dist)
        if len(dist) == 0:
            continue
        avg = sum(dist) / float(len(dist))           
        maxmax = dist.index(max(dist))
        if maxmax > 0 and maxmax < n-2:
            if (dist[maxmax] - dist[maxmax-1]) > (avg * 1.5) and (dist[maxmax] - dist[maxmax+1]) > (avg * 1.5):
#                print crv
                if not cmds.objExists('unableToMap'):
                    cmds.group(n = 'unableToMap', em = True)
                    cmds.setAttr('unableToMap.visibility', False)
#                print '1467'                    
                cmds.parent(crv, 'unableToMap')
                continue

        indList = []
        for d in range(0,len(dist)):
            if dist[d] > avg * 2:
                indList.append(d)
        deleteInd = []
    

        if len(indList) > 0:
            for maxInd in indList:
                if maxInd == 0:
                    deleteInd.append(maxInd)
                elif maxInd == n-2:
                    deleteInd.append(maxInd+1)
                else:
                    if dist[maxInd+1] > dist[maxInd]:
                        deleteInd.append(maxInd+1)
                    else:
                        deleteInd.append(maxInd+0)
                        
            if len(deleteInd) == 1:
                if not deleteInd[0] == 0 or deleteInd[0] == n-1:
                    if not cmds.objExists('unableToMap'):
                        cmds.group(n = 'unableToMap', em = True)
                        cmds.setAttr('unableToMap.visibility', False)
#                    print '1495'
                    cmds.parent(crv, 'unableToMap')
                    continue
                    
            delInd = list(set(deleteInd))
#            print  crv , ' ', delInd                       
            for dl in range(len(delInd)-1,-1,-1):
                cmds.delete(crv + '.cv[' + str(delInd[dl]) + ']')
            cmds.xform(crv, piv = (cmds.xform(crv + '.cv[0]', q = True, ws = True, t = True)))
            
                
def cpNodesForAllShells():
    
    
    planeName = cmds.getAttr(cmds.getAttr('gbNode.currentGBNode') + '.uvGrid')
    shellGrp = cmds.listRelatives(planeName, c = True)[1]
    allpShells = cmds.listRelatives(shellGrp, c = True)
    shellCPNodesList = []
    shellCPnode = ''

    for shell in allpShells:
        shellShp = cmds.listRelatives(shell, s = True)[0]
        existCPnode = cmds.listConnections( shellShp, type = 'closestPointOnMesh' , exactType = 1 )
        if existCPnode is None:
            shellCPnode = cmds.createNode('closestPointOnMesh')
            cmds.connectAttr(shellShp+'.worldMatrix',shellCPnode+'.inputMatrix')
            cmds.connectAttr(shellShp+'.worldMesh',shellCPnode+'.inMesh')
        else:
            shellCPnode = existCPnode[0]
        shellCPNodesList.append(shellCPnode)
        
    return shellCPNodesList
    
def distance3d(p0, p1):
    return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2 + (p0[2] - p1[2])**2)
    

# Map Curves from Character to Grid Section

def mapCharGrid(ip):
    
    
    historyDelete = []
    
    currNode = cmds.getAttr('gbNode.currentGBNode')
    
    gCur = cmds.listRelatives(cmds.listRelatives(cmds.ls(sl = True), ad = True, typ = 'nurbsCurve'), p = True)
    if not gCur:
        cmds.undoInfo(swf = True)
        reportGBMessage('No Curves Selected', True, True, 'red')

    if cmds.getAttr(currNode + '.paintOnMesh') == cmds.getAttr(currNode + '.volumeMesh'):
        switchCurvesToOtherMesh()
        cmds.setAttr(currNode + '.paintOnMesh', cmds.getAttr(currNode + '.scalpMesh'), type = 'string')
    

            
    charFoll = createFollicle(cmds.getAttr(currNode + '.whichMesh'))
    historyDelete.append(charFoll)
    planeName = []
    uvGridName = cmds.getAttr(currNode + '.uvGrid')
    planeName.append(uvGridName)
    selChar = cmds.getAttr(currNode + '.paintOnMesh')
    curvePosBake = []
    charFaceID = []
    shellFaceID = []
    join2DList = []
    join2DListUVList = []
    sourceUV = [[],[]]
    destUV = [[],[]]
    charUVList = []
    shellFaceUVList = []
    orig3dCurves = []
    orig3dCurveBakePos = []
    gCurves = []
    
    
    
    for g in range(0, len(gCur)):
        if cmds.ls(cmds.listRelatives(gCur[g], s = True), et = 'nurbsCurve'):
            if ip == 1:
                if not cmds.objExists('mapFromChar_' + selChar):
                    cmds.group(em = True, name = 'mapFromChar_' + selChar, parent = uvGridName)
                cmds.parent(gCur[g], 'mapFromChar_' + selChar)
                gCurves.append(gCur[g])
            else:
                gCurves.append(gCur[g])
    gCopy = []            
    for g in gCurves:
        gCopy.append(g)
    
    originLoc = cmds.spaceLocator(n = 'originLoc')
    tempLoc = cmds.spaceLocator(n = 'tempLoc')
    sourceCurve = cmds.curve( p = [[0,0,0],[0,0,0]], d = 1, n = 'sourceCurve')
    destCurve = cmds.curve( p = [[0,0,0],[0,0,0]], d = 1, n = 'destCurve')
    
    selCharShp = cmds.listRelatives(selChar, s = True)[0]
    charCPnode = createCPNode(selChar)
    historyDelete.append(charCPnode)   
    
    shellGrp = cmds.listRelatives(planeName[0], c = True)[1]
    allpShells = cmds.listRelatives(shellGrp, c = True)
    
    shellCPNodesList = cpNodesForAllShells()
    for shellN in shellCPNodesList:
        historyDelete.append(shellN)
    
    dqshellCPNodesList = deque(shellCPNodesList)
    dqallpShells = deque(allpShells)
    
    join2DListUVList = []
    edgeList = []

    for eachC in gCurves:
        
        cmds.delete(eachC, ch = True)
        newLength = int((round(cmds.arclen(eachC))+1))
        sp = cmds.getAttr(eachC +'.spans')
        dg = cmds.getAttr(eachC +'.degree') 
        ncv = sp + dg

        if ncv < newLength:
            cmds.rebuildCurve(eachC, ch = False, s = newLength)
            ncv = int(newLength)
        curvePosBake = []
        for i in range(0,ncv):
            curvePosBake.append(cmds.xform(eachC + '.cv[' + str(i) + ']', q = True, ws = True, t = True))
        
        root3dPos = curvePosBake[0]
        cmds.xform(eachC, ws = True, rp = root3dPos, sp = root3dPos)
        cmds.setAttr(charCPnode + '.ip', root3dPos[0], root3dPos[1], root3dPos[2])
        cpU = cmds.getAttr(charCPnode+'.u')
        cpV = cmds.getAttr(charCPnode+'.v')
        charFaceID = []
        charFaceID.append(cmds.getAttr(charCPnode + '.f'))
        rootXYZ = cmds.pointOnSurface(planeName[0], u = cpU, v = cpV, position = True)
        cmds.xform(eachC + '.cv[0]', ws = True, t = rootXYZ)
        cmds.xform(eachC, piv = rootXYZ)
        
        for n in range(0,len(dqshellCPNodesList)):
            cmds.setAttr((dqshellCPNodesList[n] + '.ip'),rootXYZ[0], rootXYZ[1], rootXYZ[2])
            tupleP = cmds.getAttr(dqshellCPNodesList[n]+ '.p')
            dX = abs(round((rootXYZ[0] - tupleP[0][0]),4))
            dZ = abs(round((rootXYZ[2] - tupleP[0][2]),4))
            onShell = 0
            if (dX+dZ) <= 0.1:
                onShell = 1
                distXZ = dX+dZ
                shell = dqallpShells[n]
                shellCPNode = dqshellCPNodesList[n]
                if n!= 0:
                    dqallpShells.rotate(-n)
                    dqshellCPNodesList.rotate(-n)
                break

        cmds.setAttr(shellCPNode + '.ip', rootXYZ[0], rootXYZ[1], rootXYZ[2])
        shellFaceID = []
        shellFaceID.append(cmds.getAttr(shellCPNode + '.f'))
        over = 0
        for cv in range(1,ncv):
            over = 0

            charCVPos = cmds.xform(eachC + '.cv[' + str(cv) + ']', q = True, ws = True, t = True)
            cmds.setAttr(charCPnode + '.ip', charCVPos[0], charCVPos[1], charCVPos[2])
            cpU = cmds.getAttr(charCPnode+'.u')
            cpV = cmds.getAttr(charCPnode+'.v')
            cpU = 1.0 if cpU > 1.0 else cpU
            cpV = 1.0 if cpV > 1.0 else cpV
            charFaceID.append(cmds.getAttr(charCPnode + '.f'))

            curCV = cmds.pointOnSurface(planeName[0], u = cpU, v = cpV, position = True)
            cmds.setAttr(shellCPNode + '.ip', curCV[0], curCV[1], curCV[2])

            tupleP = cmds.getAttr(shellCPNode + '.p')
            shellFaceID.append(cmds.getAttr(shellCPNode + '.f'))
            
            dX = abs(round((curCV[0] - tupleP[0][0]),7))
            dZ = abs(round((curCV[2] - tupleP[0][2]),7))
            distFromShell = dX + dZ
            
            prevFace = shellFaceID[-2]
            curFace = shellFaceID[-1]
            
            inFlow = 0
            if distFromShell <= 0.001:
                if prevFace == curFace:
                    inFlow = 1
                else:
                    prevVtx = cmds.ls(cmds.polyListComponentConversion(shell + '.f[' + str(prevFace) + ']', ff = True, tv = True),fl = True)
                    currVtx = cmds.ls(cmds.polyListComponentConversion(shell + '.f[' + str(curFace) + ']', ff = True, tv = True),fl = True)
                    for vtx in prevVtx:
                        if vtx in currVtx:
                            inFlow = 1

                            break
                        
            if inFlow == 1:
                cmds.xform(eachC + '.cv[' + str(cv) + ']', ws = True, t = curCV)
                if cv == 0:
                    cmds.xform(eachC, piv = curCV)
                continue
            else:
                charCommonEdge = cmds.polyListComponentConversion(selChar + '.f[' + str(charFaceID[-2]) + ']', selChar + '.f[' + str(charFaceID[-1]) + ']', ff = True, te = True, internal = True)
                if len(charCommonEdge) == 0:
                    if cmds.getAttr(eachC + '.ra', l = True):
                        if '_2dPART' in eachC:
                            
                            xList = []
                            eC = eachC.split('_2dPART')[0]
                            todelete = []
                            for tt in join2DList:
                                for ttt in tt:
                                    if eC in ttt:
                                        if not eC == ttt:
                                            todelete.append(ttt)
                                        xList.append(tt)
                            
                            for x in xList:
                                if xList.count(x) == 2:
                                    xList.remove(x)
                            
                            for x in xList:
                                indx = join2DList.index(x)
                                join2DList.pop(indx)
                                join2DListUVList.pop(indx)
                                edgeList.pop(indx)
                                
                            todel = set(todelete)
                            for d in todel:
                                if cmds.objExists(d):
                                    cmds.delete(d)
                            
                            ind = orig3dCurves.index(eC)
                            bakePos = orig3dCurveBakePos[ind]
                        
                            cmds.delete(eC)
                            cmds.curve(n = eC, p = bakePos)
                        else:
                            eC = eachC
                            cmds.delete(eC)
                            cmds.curve(n = eC, p = curvePosBake)
                        
                        if not cmds.objExists('unableToMap'):
                            cmds.group(n = 'unableToMap', em = True)
                            cmds.setAttr('unableToMap.visibility', False)
                        cmds.parent(eC, 'unableToMap')
                        break

                        
                    else:
                        for i in range(0, ncv):
                            cmds.xform(eachC + '.cv[' + str(i) + ']',ws= True, t = curvePosBake[i])
                        uPara = (1.0 / ncv) 
                        tmp = cv-1
                        uPara = uPara * tmp * 1.0
                        minU = uPara - 0.1
                        if minU < 0.0:
                            minU = 0.0
                        maxU = uPara + 0.1
                        if maxU > 1.0:
                            maxU = 1.0
                        cmds.rebuildCurve(eachC, ch = False, kcp = True, rpo = True, rt = 0, end = 1, kr = 0, s = 4, kep = True, kt = False)
                        cmds.insertKnotCurve(eachC , p = (minU, maxU), nk = 50, ch = False, ib = True, rpo = True)
                        cmds.setAttr(eachC + '.ra', l = True)
                        gCurves.append(eachC)
                        break
                    continue
                else:
                    mapID = cmds.ls(cmds.polyListComponentConversion(charCommonEdge, fe = True, tuv = True),fl = True)
                    edgeToVtx = cmds.ls(cmds.polyListComponentConversion(charCommonEdge, fe = True, tv = True),fl = True)
                    charUVList = []
                    for map in mapID:
                        uvChk = cmds.polyEditUV(map, query = True)
                        charUVList.append(uvChk)
                    
                    shellFaceMapID = cmds.ls(cmds.polyListComponentConversion(shell + '.f[' + str(prevFace) + ']', ff = True, tuv = True),fl = True)
                    shellFaceUVList = []
                    for sf in shellFaceMapID:
                        shellFaceUVList.append(cmds.polyEditUV(sf, query = True))
                     
                    sourceUV = []
                    destUV = []
                    for j in range(0,len(shellFaceUVList)):
                        for k in range(0,len(charUVList)):
                            if shellFaceUVList[j] == charUVList[k]:
                                sourceUV.append(charUVList[k])
                                charUVList.pop(k)
                                break

                    if len(sourceUV) <= 1 or len(charUVList) < 2:
                        
                        if cmds.getAttr(eachC + '.ra', l = True):
                                                
                            if '_2dPART' in eachC:
        
                                xList = []
                                eC = eachC.split('_2dPART')[0]
                                todelete = []
                                for tt in join2DList:
                                    for ttt in tt:
                                        if eC in ttt:
                                            if not eC == ttt:
                                                todelete.append(ttt)
                                            xList.append(tt)
                                
                                for x in xList:
                                    if xList.count(x) == 2:
                                        xList.remove(x)
                                
                                for x in xList:
                                    indx = join2DList.index(x)
                                    join2DList.pop(indx)
                                    join2DListUVList.pop(indx)
                                    edgeList.pop(indx)
                                    
                                
                                todel = set(todelete)
                                for d in todel:
                                    if cmds.objExists(d):
                                        cmds.delete(d)
                                
                                ind = orig3dCurves.index(eC)
                                bakePos = orig3dCurveBakePos[ind]
                                cmds.delete(eC)
                                cmds.curve(n = eC, p = bakePos)
                            else:
                                eC = eachC
                                cmds.delete(eC)
                                cmds.curve(n = eC, p = curvePosBake)
                            
                            if not cmds.objExists('unableToMap'):
                                cmds.group(n = 'unableToMap', em = True)
                                cmds.setAttr('unableToMap.visibility', False)
                            cmds.parent(eC, 'unableToMap')
                            break
    
                            
                        else:
                            for i in range(0, ncv):
                                cmds.xform(eachC + '.cv[' + str(i) + ']',ws= True, t = curvePosBake[i])
                            uPara = (1.0 / ncv) 
                            tmp = cv-1
                            uPara = uPara * tmp * 1.0
                            minU = uPara - 0.1
                            if minU < 0.0:
                                minU = 0.0
                            maxU = uPara + 0.1
                            if maxU > 1.0:
                                maxU = 1.0
                            cmds.rebuildCurve(eachC, ch = False, kcp = True, rpo = True, rt = 0, end = 1, kr = 0, s = 4, kep = True, kt = False)
                            cmds.insertKnotCurve(eachC , p = (minU, maxU), nk = 100, ch = False, ib = True, rpo = False)
                            cmds.setAttr(eachC + '.ra', l = True)
                            gCurves.append(eachC)
                            break
                        continue

                    sourceUV[0] = [1.0 if c > 1.0 else c for c in sourceUV[0]]
                    cmds.setAttr(charFoll+ '.parameterU',sourceUV[0][0])
                    cmds.setAttr(charFoll + '.parameterV',sourceUV[0][1])
                    cXYZ = cmds.xform(charFoll, q = True, ws = True, t = True)
                    cmds.setAttr(charCPnode + '.ip', cXYZ[0], cXYZ[1], cXYZ[2])
                    v1 = getClosestVtx(selChar, cmds.getAttr(charCPnode + '.f'),cXYZ)
                    
                    cmds.setAttr(charFoll+ '.parameterU',charUVList[0][0])
                    cmds.setAttr(charFoll + '.parameterV',charUVList[0][1])
                    cXYZ = cmds.xform(charFoll, q = True, ws = True, t = True)
                    cmds.setAttr(charCPnode + '.ip', cXYZ[0], cXYZ[1], cXYZ[2])
                    v2 = getClosestVtx(selChar, cmds.getAttr(charCPnode + '.f'),cXYZ)
                    
                    if v1 == v2:
                        destUV.append(charUVList[0])
                        destUV.append(charUVList[1])
                    else:
                        destUV.append(charUVList[1])
                        destUV.append(charUVList[0])                        
                        
                    nextCurve = cmds.duplicate(eachC, n = eachC + '_2dPART', rc = True)[0]
                    if not '_restPart' in eachC:
                            orig3dCurves.append(eachC)
                            orig3dCurveBakePos.append(curvePosBake)
                            
                    cmds.delete(eachC + '.cv[' + str(cv) + ':' + str(ncv) + ']')
                    spDel = cmds.getAttr(eachC + '.spans')
                    dgDel = cmds.getAttr(eachC + '.degree')
                    ncvDel = spDel + dgDel
                    if ncvDel < 4:
                        for n in range(ncvDel,5):
                            cmds.curve(eachC, a = True, p = (cmds.xform(eachC + '.cv[' + str(ncvDel) + ']', q = True, ws = True, t = True)))    
                    
                    
                    cmds.delete(nextCurve + '.cv[0:' + str(cv-1) + ']')

                    spN = cmds.getAttr(nextCurve +'.spans')
                    dgN = cmds.getAttr(nextCurve +'.degree')
                    ncvN = spN + dgN
                    if ncvN < 4:
                        for n in range(ncvN,5):
                            cmds.curve(nextCurve, a = True, p = (cmds.xform(nextCurve + '.cv[' + str(ncvN) + ']', q = True, ws = True, t = True)))    
                    cmds.xform(nextCurve, ws = True, rp = curvePosBake[cv],sp = curvePosBake[cv])

                    gCurves.append(nextCurve)
                    edgeList.append(charCommonEdge)
                    join2DList.append([eachC,nextCurve])
                    join2DListUVList.append([sourceUV, destUV])

                    over = 1
                break
    
    
    for o in range(len(join2DList)-1,-1,-1):
        cmds.makeIdentity(destCurve, apply = True) 
        mainCurve = join2DList[o][0]
        curvePart = join2DList[o][1]
        sourceUV = join2DListUVList[o][0]
        destUV = join2DListUVList[o][1]
        newUV = []
        newUV = [1.0 if c > 1.0 else c for c in sourceUV[0]]
        srcXYZ0 = cmds.pointOnSurface(planeName[0], u = newUV[0], v = newUV[1], position = True)
        newUV = []
        newUV = [1.0 if c > 1.0 else c for c in sourceUV[1]]
        srcXYZ1 = cmds.pointOnSurface(planeName[0], u = newUV[0], v = newUV[1], position = True)                    
        
        cmds.xform(sourceCurve + '.cv[0]', ws = True, t = srcXYZ0)
        cmds.xform(sourceCurve + '.cv[1]', ws = True, t = srcXYZ1)
        cmds.xform(sourceCurve, ws = True, rp = srcXYZ0, sp = srcXYZ0)
        newUV = []
        newUV = [1.0 if c > 1.0 else c for c in destUV[0]]
        destXYZ0 = cmds.pointOnSurface(planeName[0], u = newUV[0], v = newUV[1], position = True)
        newUV = []
        newUV = [1.0 if c > 1.0 else c for c in destUV[1]]
        destXYZ1 = cmds.pointOnSurface(planeName[0], u = newUV[0], v = newUV[1], position = True)
        
        cmds.xform(destCurve + '.cv[0]', ws = True, t = destXYZ0)
        cmds.xform(destCurve + '.cv[1]', ws = True, t = destXYZ1)
        cmds.xform(destCurve, ws = True, rp = destXYZ0,sp = destXYZ0)
        
        cmds.select(curvePart, destCurve, r = True)
        mm.eval('CreateWrap;')
        cmds.select(cl = True)
        
        
        cmds.xform(tempLoc, ws = True, t = srcXYZ0)
        
        pCs = cmds.pointConstraint(originLoc, sourceCurve, mo = 0)
        cmds.delete(pCs)
        pCd = cmds.pointConstraint(originLoc, destCurve, mo = 0)
        cmds.delete(pCd)
        
        srcCV1Pos = cmds.xform(sourceCurve + '.cv[1]',q = True, ws = True, t = True)
        destCV1Pos = cmds.xform(destCurve + '.cv[1]',q = True, ws = True, t = True)
       
        
        rot = cmds.angleBetween(euler = True, v1 = tuple(destCV1Pos), v2 = tuple(srcCV1Pos))
        cmds.xform(destCurve, ws = True, ro = rot)

        pC = cmds.pointConstraint(tempLoc, destCurve, mo = 0)
        cmds.delete(pC)
        
        
        sp = cmds.getAttr(curvePart +'.spans')
        dg = cmds.getAttr(curvePart +'.degree') 
        ncvPart = sp + dg
        
        
        for p in range(0,ncvPart):
            pPos = cmds.xform(curvePart + '.cv[' + str(p) + ']', q = True, ws = True, t = True)
            cmds.curve(mainCurve, a = True, p = pPos)
            if not '_2dPART' in mainCurve:
                cmds.xform(mainCurve, piv = (cmds.xform(mainCurve + '.cv[0]', q = True, ws = True, t = True)))
                
        cmds.delete(curvePart)
        
                        
    
    cmds.delete(originLoc, tempLoc, sourceCurve, destCurve) 

    for h in historyDelete:
    	if cmds.objExists(h):
            cmds.delete(h)

    cmds.select(gCopy, r = True)
    cmds.undoInfo(swf = True)


def getClosestVtx(shell, faceId, cvXYZ):
    
    minDist = 100000
    vtxList = cmds.ls(cmds.polyListComponentConversion(shell + '.f[' + str(faceId) + ']', ff = True, tv = True),fl = True)
    dist3 = []
    for vtx in vtxList:
        vPos = cmds.xform(vtx, q = True, ws = True, t = True)
        dist3.append(distance3d(vPos, cvXYZ))
    closeV =  vtxList[dist3.index(min(dist3))]
    return closeV       

def ccw(A,B,C):
	return (C[1]-A[1])*(B[0]-A[0]) > (B[1]-A[1])*(C[0]-A[0])
	
def inter(A,B,C,D):
	return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)
	
def distance(p0, p1):
    return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)
    

def volSelectCurvesExec():

    # Adjust Volume - Second Tab    
    
    cmds.columnLayout('targetMeshLayout', edit = True, vis = True)
    cmds.button('volSelectCurves', edit = True, vis = False)
    
def partSel():
    cmds.button('scalpSel',edit = True, vis = True)
    cmds.radioButtonGrp('targetRadio2', edit = True, vis = False)
    cmds.button('existVolBtn', edit = True, vis = False)    
    cmds.button('newVolBtn', edit = True, vis = False)
    

def volSel():
    cmds.radioButtonGrp('targetRadio2', edit = True, vis = True)
    cmds.button('scalpSel',edit = True, vis = False)
    
def existVol():
    cmds.button('existVolBtn', edit = True, vis = True)    
    cmds.button('newVolBtn', edit = True, vis = False)            

def newVol():
    cmds.button('existVolBtn', edit = True, vis = False)    
    cmds.button('newVolBtn', edit = True, vis = True)            

def targetIsScalp():
    cmds.columnLayout('adjVolLayout', edit = True, vis = True)
    cmds.columnLayout('configLayout', edit = True, vis = False)

def targetIsExVolume():
    cmds.columnLayout('adjVolLayout', edit = True, vis = True)
    cmds.columnLayout('configLayout', edit = True, vis = False)

def targetIsNewVolume():
    cmds.columnLayout('adjVolLayout', edit = True, vis = True)
    cmds.columnLayout('configLayout', edit = True, vis = False)

def updateCurves():
    cmds.columnLayout('adjVolLayout', edit = True, vis = False)
    cmds.columnLayout('updateCurvesLayout', edit = True, vis = True)
    
def yldSkin(baseMesh, jointList, faceIDList):
    
    facetList = []
    currNode = cmds.getAttr('gbNode.currentGBNode')
#    baseMesh = cmds.getAttr(currNode + '.drawMesh')
    clustName = mm.eval('findRelatedSkinCluster(' + dQ + baseMesh + dQ + ');')    
    smoothBaseMesh = cmds.duplicate(baseMesh, name = 'highRes_' + baseMesh, rr = True)[0]
    faceList = []
#    cmds.polySmooth(smoothBaseMesh, dv = 1)
    for jnt in jointList:
        pos = cmds.xform(jnt, q = True, ws = True, t = True)
        if not faceIDList:
            fID = jnt.split('_')[-1]
            faceList.append(smoothBaseMesh + '.f[' + fID + ']')
        facetList.append(cmds.polyCreateFacet( p=[tuple(pos), tuple(pos), tuple(pos)] , ch = False)[0])
    
    if not faceList:
        faceList = [smoothBaseMesh + '.f[' + str(f) + ']' for f in faceIDList]
        
    faceList = cmds.polyListComponentConversion(cmds.polyListComponentConversion(faceList, ff = True, te = True), fe = True, tf = True)
    cmds.polySmooth(faceList, dv = 2)
    
    polyCloud = cmds.polyUnite(facetList, ch = False, name = 'pointCloud_' + smoothBaseMesh)[0]

    cmds.transferAttributes(polyCloud, smoothBaseMesh, transferPositions = True, nml = False, uvs = False, col = False, sampleSpace = 0)
    cmds.polyMergeVertex(smoothBaseMesh, d = 0.001)
    cmds.select(jointList, smoothBaseMesh, r = True)
    tempGBNode = cmds.getAttr('gbNode.tempGBNode')   
    yldClust = cmds.skinCluster(name = tempGBNode, dr = 10.0, mi = 1 , omi = True, tsb = True, sm = 0 )[0]

    cmds.copySkinWeights(ss = yldClust, ds = clustName, nm = True, ia = 'closestJoint', sa = 'closestPoint')
    cmds.delete(smoothBaseMesh, polyCloud)
    
def smoothSkin(jointList):
    
    mm.eval('artAttrSkinToolScript 3;')
    mm.eval('artAttrPaintOperation artAttrSkinPaintCtx Smooth;') 
    mm.eval('artAttrSkinPaintCtx -e -colorfeedback false `currentCtx`;')
    mm.eval('artAttrSkinPaintCtx -e -opacity .8 `currentCtx`;')
#    cmds.progressBar('progress3DIpol', edit = True, max = len(jointList)-1, vis = True)
    for j in range(0,len(jointList)):
        
#        cmds.refresh(su = True)        
        if j > 0:
            mm.eval('artSkinInflListChanging ' + jointList[j-1] + ' 0;')
        mm.eval('artSkinInflListChanging ' + jointList[j] + ' 1;')
        mm.eval('artSkinInflListChanged artAttrSkinPaintCtx;')
#        for i in range(0,5):
        mm.eval('artAttrSkinPaintCtx -e -clear `currentCtx`;')
#        cmds.progressBar('progress3DIpol', edit = True, s = 1)
#    cmds.progressBar('progress3DIpol', edit = True, vis = False)
    mm.eval('artAttrSkinPaintCtx -e -colorfeedback true `currentCtx`;')        
    cmds.setToolTo('selectSuperContext')
#    cmds.refresh(su = False)

def touchRotate(crv, p0, pA, pB):
    dA = [(c - d) for c, d in zip(pA,p0)] 
    dB = [(c - d) for c, d in zip(pB,p0)] 
    uA = mm.eval('unit <<' + str(dA[0]) + ',' + str(dA[1]) + ',' + str(dA[2]) + '>>')
    uB = mm.eval('unit <<' + str(dB[0]) + ',' + str(dB[1]) + ',' + str(dB[2]) + '>>')
    tRot = cmds.angleBetween(euler = True, v1=uA, v2=uB)
    cmds.rotate(tRot[0], tRot[1], tRot[2], crv, r = True)

def addSuperCurves():
    
    stopGBUndo()
#    print 'adddd'
    cmds.button('interCharBtn', edit = True, en = True)
    currNode = cmds.getAttr('gbNode.currentGBNode')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    selChar = cmds.getAttr(currNode + '.drawMesh')
    baseMeshGrp = cmds.getAttr(currNode + '.baseMeshGroup')
    baseMeshGrpChildren = cmds.listRelatives(baseMeshGrp, c = True)
#    super = cmds.ls(sl = True)
    super = cmds.listRelatives(cmds.listRelatives(cmds.ls(sl = True), ad = True, typ = 'nurbsCurve'), p = True)
    if not super:
        reportGBMessage('No Curves Selected', True, True, 'red')
#        raise RuntimeError, 'No Curves Selected'
 
#    superGrp = 'superCurves_charInterpolation_' + selChar
    superGrp = 'superCurves_charInterpolation_' + scalpMesh
    
    if baseMeshGrpChildren is None:
        cmds.group(name = superGrp, em = True, p = baseMeshGrp)
        
    else:
        if not superGrp in baseMeshGrpChildren:
            cmds.group(name = superGrp, em = True, p = baseMeshGrp)
    superChildren = []
    superChildren = cmds.listRelatives(superGrp, c = True)
    
    if not superChildren is None:
        newSups = list(set(super)-set(superChildren))
    else:
        newSups = super
    
    cmds.parent(newSups, superGrp)
    
    finalSups = cmds.listRelatives(superGrp, ad = True, typ = 'nurbsCurve')
    for sup in finalSups:
        cmds.setAttr(sup + '.overrideEnabled', True)
        cmds.setAttr(sup + '.overrideColor', 13)
    
    if not checkIfFFExists():
        deleteFFGroup()
    startGBUndo()

def deleteFFGroup():
    
    currNode = cmds.getAttr('gbNode.currentGBNode')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    baseMeshGrp = cmds.getAttr(currNode + '.baseMeshGroup')
    baseMeshGrpChildren = cmds.listRelatives(baseMeshGrp, c = True)
    i3DGrp = 'manualCurvesGrp_' + scalpMesh
    i3DGrpChildren = []
    if baseMeshGrpChildren:
        if i3DGrp in baseMeshGrpChildren:
            cmds.delete(i3DGrp)

def mirrorSelectedSuperCurves():
    
    stopGBUndo()
    currNode = cmds.getAttr('gbNode.currentGBNode')
    paintMesh = cmds.getAttr(currNode + '.paintOnMesh')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    selList = cmds.ls(sl = True)
    if not selList:
        reportGBMessage('No Curves Selected', True, True, 'red')
#        raise RuntimeError, 'Nothing Selected'
    baseMeshGrp = cmds.getAttr(currNode + '.baseMeshGroup')
    superGrp = 'superCurves_charInterpolation_' + scalpMesh
    baseMeshGrpChildren = cmds.listRelatives(baseMeshGrp, c = True)
    superGrpChildren = []
    if superGrp in baseMeshGrpChildren:
        superGrpChildren = cmds.listRelatives(superGrp, c = True)
    
    if not superGrpChildren:
        reportGBMessage('No Super Curves exist', True, True, 'red')
#        raise RuntimeError, 'No Super Curves exist'
        
    selSuper = []
    selSuper = [sel for sel in selList if sel in superGrpChildren]
    if not selSuper:
        reportGBMessage('Please select Super Curves', True, True, 'red')
#        raise RuntimeError, 'Please select Super Curves'

    historyDelete = []
    axisID = cmds.radioButtonGrp('mirrorSuperCurvesAxisRadio', q = True, sl = True)
    mirrorDict = {1:'X', 2:'Y', 3:'Z'}
    axis = mirrorDict[axisID]
    
    charCPNode = createCPNode(paintMesh)
    historyDelete.append(charCPNode)
    
    center = cmds.objectCenter(paintMesh, gl = True)
    tempMirrorScalpDup = paintMesh + '_MirrorDup'
    tempMirrorGrp = paintMesh + '_MirrorGrp'
    
    if cmds.objExists(tempMirrorScalpDup):
        cmds.delete(tempMirrorScalpDup)
    else:
        cmds.duplicate(paintMesh, name = tempMirrorScalpDup, rr = True)

    if cmds.objExists(tempMirrorGrp):
        cmds.delete(tempMirrorGrp)
    
    cmds.group(tempMirrorScalpDup, name = tempMirrorGrp)    
    
    cmds.delete(tempMirrorScalpDup)
    cmds.xform(tempMirrorGrp, cp = True)
    
    for sup in selSuper:
        supDup = cmds.duplicate(sup, rr = True)
        cmds.select(cl = True)
        cmds.parent(supDup, tempMirrorGrp)
        
    command = 'scale -a -1 -1 -1 -scale' + axis + ' ' + tempMirrorGrp
    mm.eval(command)
    
    newSups = cmds.listRelatives(tempMirrorGrp, c = True)
    cmds.select(newSups, r = True)
    addSuperCurves()
    cmds.select(newSups, r = True)
    snapSuperCurvesBackToMesh('internal')
    cmds.makeIdentity(newSups, apply = True)

    cmds.delete(tempMirrorGrp)
    for h in historyDelete:
        if cmds.objExists(h):
            cmds.delete(h)
    
    startGBUndo()
            

def snapSuperCurvesBackToMesh(mode):
    
    stopGBUndo()
    currNode = cmds.getAttr('gbNode.currentGBNode')
    paintMesh = cmds.getAttr(currNode + '.paintOnMesh')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
#    if paintMesh == scalpMesh:
#        paintMesh = scalpMesh + '_DISPLAY'
    selList = cmds.ls(sl = True)
    if not selList:
        reportGBMessage('No Curves Selected', True, True, 'red')
#        raise RuntimeError, 'Nothing Selected'
    baseMeshGrp = cmds.getAttr(currNode + '.baseMeshGroup')
    superGrp = 'superCurves_charInterpolation_' + scalpMesh
    baseMeshGrpChildren = cmds.listRelatives(baseMeshGrp, c = True)
    superGrpChildren = []
    if superGrp in baseMeshGrpChildren:
        superGrpChildren = cmds.listRelatives(superGrp, c = True)
    
    if not superGrpChildren:
        reportGBMessage('No Super Curves exist', True, True, 'red')
        
#        raise RuntimeError, 'No Super Curves exist'
        
    selSuper = []
    selSuper = [sel for sel in selList if sel in superGrpChildren]
    if not selSuper:
        reportGBMessage('Please select Super Curves', True, True, 'red')
#        raise RuntimeError, 'Please select Super Curves'
    
    historyDelete = []
    charCPNode = createCPNode(paintMesh)
    historyDelete.append(charCPNode)
    
    threshold = 0.75
    
    for sup in selSuper:
        rootPos = cmds.pointPosition(sup + '.cv[0]')
        cmds.setAttr(charCPNode + '.ip', rootPos[0], rootPos[1], rootPos[2])
        cpPos = list(cmds.getAttr(charCPNode + '.p')[0])
        if distance3d(rootPos, cpPos) > threshold:
            if mode == 'internal':
                cmds.delete(sup)
            reportGBMessage(str(sup) + ' skipped as it is not on mesh', False, True, 'yellow')
#            raise RuntimeWarning, str(sup) + ' skipped as it is not on mesh'                            
            continue
        sp = cmds.getAttr(sup + '.spans')
        dg = cmds.getAttr(sup + '.degree')
        ncv = sp + dg
        for cv in range(ncv):
            cvPos = cmds.pointPosition(sup + '.cv[' + str(cv) + ']')
            cmds.setAttr(charCPNode + '.ip', cvPos[0], cvPos[1], cvPos[2])
            cmds.xform(sup + '.cv[' + str(cv) + ']', ws = True, t = list(cmds.getAttr(charCPNode + '.p')[0]))
            
    cmds.delete(historyDelete)
    startGBUndo()
     
            

def interpolateOnFaces(vertices,clustName):
    
    import cPickle as Pickle
    import time
    historyDelete = []
    vtxSel = vertices
    cmds.select(cl = True)
    
    currNode = cmds.getAttr('gbNode.currentGBNode')
    superCurves = Pickle.loads(str(cmds.getAttr(currNode + '.superCurves3D')))
    ipolVertices = Pickle.loads(str(cmds.getAttr(currNode + '.ipolVertices3D')))
#    print 'interpolation vertices', vertices
    if not vertices:
        return
    
    vertices = list(set(vertices))
    toBeUpdatedIpol = []
    toBeUpdatedIpolString = cmds.getAttr(currNode + '.toBeUpdatedIpol')
    if toBeUpdatedIpolString:
        toBeUpdatedIpol = Pickle.loads(str(toBeUpdatedIpolString))
        
    curveList4Graph = []
    curveList4GraphString = cmds.getAttr(currNode + '.curveList4Graph')
    if curveList4GraphString:
        curveList4Graph = Pickle.loads(str(curveList4GraphString))
        
    
#    charFoll = createFollicle(cmds.getAttr(currNode + '.whichMesh'))
#    historyDelete.append(charFoll)
    
    charFoll = cmds.getAttr(currNode + '.drawMeshFollicle')
    charFollShp = cmds.listRelatives(charFoll , s = True)[0]
    planeName = []
    planeName.append(cmds.getAttr(currNode + '.uvGrid'))
    selChar = cmds.getAttr(currNode + '.scalpMesh')
#    selChar = cmds.getAttr(currNode + '.drawMesh')
    jointList = []
    
    
    superGrp = 'superCurves_charInterpolation_' + selChar
    
    notProper = []
    maxCV = cmds.getAttr('gbNode.maxCV')
    
    vtxLoc = cmds.group(empty = True)
    historyDelete.append(vtxLoc)
            
    selCharShp = cmds.listRelatives(selChar, s = True)[0]
    
    notInFlow = []
    charCPNode = cmds.getAttr(currNode + '.drawMeshCPNode')

    
    i3DGrp = 'charInterpolation_' + selChar
    
    
#    uv = [0,0]
    if len(vtxSel)>1:
#        cmds.progressBar('progress3DIpol', edit = True, max = len(vtxSel)-1, vis = True)
        cmds.text('gbProgressBarText', edit = True, vis = True, label = 'Performing Interpolation On ' + str(len(vtxSel)) + ' Vertices')
        cmds.progressBar('gbProgressBar', edit = True, pr = 0, max = len(vtxSel)-1, vis = True)
    step = len(vtxSel)
    totalIter = step
    percentCheck = [(per * totalIter) / 100 for per in range(0,100,10)]
    masterTime = time.time()      
    iter = 0
    checkTime = False
    firstLoop = False
    bgRGB = [0,1,1]
    flM = 0
    flS = 0
    loopEntered = False
    for vtx in vtxSel:
        if iter in percentCheck:
#            print iter
            checkTime = True
        else:
            checkTime = False            

        if checkTime:
            loopStart = time.time()
                
        iter = iter + 1
#        print vtx
        vtxID = vtx.split('[')[1].split(']')[0]
        for ipol in range(len(ipolVertices)):
            if vtxID in ipolVertices[ipol]:
                ipolVertices[ipol].remove(vtxID)
                
        iPolName = ('ipol3DCrv_' + selChar + 'vtx_' + vtxID)
        if curveList4Graph.count(iPolName):
#            print 'iPolName exists', iPolName
#            toBeIndex = curveList4Graph.index(iPolName)
#            if not toBeIndex in toBeUpdatedIpol:
#                toBeUpdatedIpol.append(toBeIndex)
            toBeUpdatedIpol.append(str(vtxID))
           
        
        if cmds.objExists(iPolName):
#            cmds.delete(cmds.blendShape(cmds.listConnections(cmds.listRelatives(iPolName,s = True)[0], type = 'blendShape')[0], q = True, t = True))
            cmds.delete(iPolName)

        posV = []
        posV = cmds.xform(vtx, q = True, ws = True, t = True)
        
#        posF = []
#        posF4 = cmds.xform(face, q = True, ws = True, t = True)
#        for i in range(0,3):
#            posF.append(0)
#            for j in range(i,len(posF4),3):
#                posF[i] = posF[i] + (posF4[j]/(len(posF4)/3))

    
        cmds.setAttr(charCPNode + '.ip', posV[0], posV[1], posV[2])
        
        cuV = cmds.getAttr(charCPNode + '.u')
        cvV = cmds.getAttr(charCPNode + '.v')
        cmds.setAttr(charFollShp + '.parameterU', cuV)
        cmds.setAttr(charFollShp + '.parameterV', cvV)
        jntList = cmds.skinCluster(clustName, inf = True , q = True)
#        vtx = cmds.ls(cmds.polyListComponentConversion(face, ff = True, tv = True),fl = True)
#        vtx0 = cmds.ls(cmds.polyListComponentConversion(face, ff = True, tv = True),fl = True)[0]
        skinList = []
        skinP = []
        '''
        for v in vtx:
            skinP.append(cmds.skinPercent(clustName, v, q = True, v = True))
        for i in range(0,len(jointList)):
            sk = 0.0
            for j in range(len(vtx)):
                sk = sk + skinP[j][i]
            skinList.append(sk / float(len(vtx)))
         '''
#        print skinList
#        print 'current vtx', vtx
        skinList = cmds.skinPercent(clustName, vtx , q = True, v = True)
#        print 'current clustname', clustName, skinList
        
        zipJS = zip(jntList, skinList)
        
        
        curvePos = []

        for cv in range(0, maxCV):
            curvePos.append(posV)
        iName = cmds.curve(p = curvePos, degree = 3, n = iPolName )
        cmds.xform(iName, piv = posV)
        cmds.makeIdentity(iName, apply = True)
        cmds.parent(iName,i3DGrp)
        
        
        iBlend = cmds.blendShape(iName, n = 'iBlend_' + iName)[0]
        avgLen = 0
        localBSList = []
        crvList = []
        wtList = []
        dupCurvesList = []
        
        for z in range(0, len(zipJS)):
            if zipJS[z][1] < 0.1:
                continue
            crv = zipJS[z][0].split('joint3D_')[1]
            ipolVertices[superCurves.index(crv)].append(vtxID)
            crvList.append(crv)
            sGrp = 'nullGrp_' + crv
            dupGrp = cmds.duplicate(sGrp, rr = True, rc = True)[0]
            p0 = cmds.xform(charFoll, q = True, ws = True, t = True)
            cmds.xform(dupGrp, ws = True, t = p0)
            dup = cmds.listRelatives(dupGrp, c = True)

#            cmds.xform(dupGrp, ws = True, ro = cmds.xform(charFoll, q = True, ws = True, ro = True))
            
#            if len(dup) > 1:
#                print dup
            dupCrv = crv + '_vtx_' + vtxID + '_copy'
#            print 'crv ', crv, 'grp ', sGrp, ' dupGrp ', dupGrp, 'dupCrv ', dupCrv
            cmds.rename(dup, dupCrv)
            cmds.ungroup(dupGrp, parent = i3DGrp)
            dupCurvesList.append(dupCrv)
            historyDelete.append(dupCrv)
#            cmds.delete(dupGrp)

            cmds.setAttr(dupCrv + '.visibility', False)
#            dupCrv = cmds.ls(sl = True)
#            charCPNode = 'closestPointOnMesh1'
#            p0 = cmds.xform(cmds.ls(sl = True), q = True, ws = True, t = True)
                         
            pA = cmds.pointOnCurve(dupCrv, pr = 0.2, p = True)
            cmds.setAttr(charCPNode + '.ip', pA[0], pA[1], pA[2])
            pB = list(cmds.getAttr(charCPNode + '.p')[0])
            dA = [(c - d) for c, d in zip(pA,p0)] 
            dB = [(c - d) for c, d in zip(pB,p0)] 
            uA = mm.eval('unit <<' + str(dA[0]) + ',' + str(dA[1]) + ',' + str(dA[2]) + '>>')
            uB = mm.eval('unit <<' + str(dB[0]) + ',' + str(dB[1]) + ',' + str(dB[2]) + '>>')
            tRot = cmds.angleBetween(euler = True, v1=uA, v2=uB)
            cmds.rotate(tRot[0], tRot[1], tRot[2], dupCrv, r = True)
            
#            localBSList.append(cmds.blendShape(crv,dupCrv, o = 'local',w = (0,1)))
            
#            sBlend = cmds.blendShape(dupCrv, n = 'sBlend_' + dupCrv)[0]
#            cmds.blendShape ( sBlend , t = (dupCrv, 0, crv, 1), e = True, tc = False, origin = 'local')            
#            cmds.setAttr((sBlend + '.' + crv),1.0)
            
            cmds.blendShape ( iBlend , t = (iName, z, dupCrv, 1), e = True, tc = False, origin = 'world')
            zWt = float(zipJS[z][1])
            wtList.append(zWt)            
            cmds.setAttr(iBlend + '.' + dupCrv, zWt)
            
#            avgLen = avgLen + distance3d(cmds.xform(iName + '.cv[0]', q = True, ws = True, t = True), cmds.xform(dupCrv + '.cv[' + str(maxCV-1)+ ']', q = True, ws = True, t = True))
#        avgLen = avgLen / float(len(dupCurvesList))
#        cmds.setAttr(iName + '.rotateAxisX', avgLen)            
        target = cmds.blendShape(iBlend, q = True, t = True)
        if len(target) == 1:
#            print 'bs = ', iBlend, ' target: ', target
            cmds.setAttr(iBlend + '.' + target[0], 1.0)

            
        allCVPos = []
        for i in range(0, maxCV):
            allCVPos.append(cmds.xform(iName + '.cv[' + str(i) + ']', q = True, ws = True, t = True))
        cmds.setAttr(iBlend + '.envelope', 0.0)
#        inflow = 1
        for i in range(0, maxCV):
            cmds.setAttr(charCPNode + '.ip', allCVPos[i][0],allCVPos[i][1], allCVPos[i][2])
            cmds.xform(iName + '.cv[' + str(i) + ']', ws = True, t = cmds.getAttr(charCPNode + '.p')[0])
        
        
#        iNameLen = distance3d(iNamePos0 , cmds.xform(iName + '.cv[' + str(maxCV-1)+ ']', q = True, ws = True, t = True))
#        sc = avgLen / float(iNameLen)
        cmds.xform(iName, ws = True, piv = cmds.xform(iName + '.cv[0]', q = True, ws = True, t = True))
#        cmds.setAttr(iName + '.rotateAxisY', iNameLen)
#        cmds.setAttr(iName + '.rotateAxisZ', sc)
#        cmds.xform(iName, s = [sc,sc,sc])
#        allCVPos = []
#        for i in range(0, maxCV):
#            allCVPos = cmds.xform(iName + '.cv[' + str(i) + ']', q = True, ws = True, t = True)
#            cmds.setAttr(charCPNode + '.ip', allCVPos[0],allCVPos[1], allCVPos[2])
#            cmds.xform(iName + '.cv[' + str(i) + ']', ws = True, t = cmds.getAttr(charCPNode + '.p')[0])
        
        cmds.delete(iName, ch = True)
        if cmds.objExists(iBlend):
            cmds.delete(iBlend)
#        for d in dupToMapList:
#            if cmds.objExists(d):
#                cmds.delete(d)
        for d in dupCurvesList:
            if cmds.objExists(d):
                cmds.delete(d)
        step = step - 1                
        cmds.text('gbProgressBarText', edit = True, label = 'Performing Interpolation : ' + str(step) + ' Curves Remaining')
        cmds.progressBar('gbProgressBar', edit = True, s = 1)
        
        if checkTime:
            timeRemaining = (time.time() - loopStart) * (totalIter - iter)
            trM, trS = divmod(timeRemaining, 60)
#            print bgRGB
    
            if not firstLoop and trS > 1.0:
                flM = trM
                flS = trS 
                firstLoop = True
        loopEntered = True            
        timeElapsed = time.time() - masterTime
        teM, teS = divmod(timeElapsed, 60)
        messageString = 'Time Remaining: ' + str('%02d' % trM) + ':' + str('%02d' % trS) + '\t' + 'Time Elapsed: ' + str('%02d' % teM) + ':' + str('%02d' % teS) 
#        reportGBMessage(messageString, False, False, 'blue')
        cmds.text('gbMessageStatusText', edit = True, vis = True,  label = '  ' + messageString)
#        bgRGB = list(mm.eval('hsv_to_rgb <<' + str(remapNew(0,0.333,0,totalIter,iter)) + ',1.0,' + str(remapNew(0.0,1.0,-1.0,1.0,math.sin(iter))) + '>>;'))
        bgRGB = list(mm.eval('hsv_to_rgb <<' + str(remapNew(0,0.333,0,totalIter,iter)) + ',1.0,1.0>>;'))
        cmds.text('gbMessageStatusColor',edit = True, vis = True, bgc = bgRGB)
        
        
    cmds.text('gbProgressBarText', edit = True, vis = False)
    cmds.progressBar('gbProgressBar', edit = True, vis = False)
    cmds.progressBar('gbProgressBar', edit = True, pr = 0)
    finalMessage = ''
    if loopEntered:
        finalMessage = 'Total Time Expected: ' + str('%02d' % flM) + ':' + str('%02d' % flS) + '\t' + 'Time Taken: ' + str('%02d' % teM) + ':' + str('%02d' % teS) 
    

    for h in historyDelete:
    	if cmds.objExists(h):
            cmds.delete(h)
    
    ipolVerticesString = Pickle.dumps(ipolVertices)
    cmds.setAttr(currNode + '.ipolVertices3D', ipolVerticesString, type = 'string')
    
    toBeUpdatedIpolString = Pickle.dumps(toBeUpdatedIpol)
    cmds.setAttr(currNode + '.toBeUpdatedIpol', toBeUpdatedIpolString, type = 'string')
    
    if notInFlow:
        cmds.warning(' Selected areas are not proper interpolated, as super curves are too big for that area ')
        cmds.select(notInFlow, r = True)

    if finalMessage:
        cmds.text('gbMessageStatusText', edit = True, vis = False, label = finalMessage)


def charInterpolationSelectedFaces():
    
    if not cmds.button('startDrawBtn', q = True, vis = True):
        killPFXJob()
    stopGBUndo()
    import cPickle as Pickle
    superCurves = []
    jointList = []
    nullGrpList = []
    
    cmds.undoInfo( swf = False )
    
    currNode = cmds.getAttr('gbNode.currentGBNode')
    baseMesh = cmds.getAttr(currNode + '.scalpMesh')  
    baseMeshDISP = baseMesh + '_DISPLAY'
    vtxSel = cmds.ls(sl = True, fl = True, type = 'float3')
    vtxSel = [v for v in vtxSel if v.split('.')[0] == baseMeshDISP]
    if not vtxSel:
        cmds.undoInfo( swf = True )
        reportGBMessage('Please select faces/vertices first of ScalpMesh', True, True, 'red')
#        raise RuntimeError, 'Please select faces/vertices first of ScalpMesh'
    
#    radioSel = cmds.radioButtonGrp('interpolRadio', q = True, sl = True)
#    if radioSel == 1:
#        mm.eval('polySelectBorderShell 0;')
#        vtxSel = cmds.ls(sl = True, fl = True, type = 'float3')

    
    if not cmds.objExists(currNode + '.lastIpolSelection'):
        cmds.addAttr(currNode, ln = 'lastIpolSelection', dt = 'string')
    
    cmds.setAttr(currNode + '.lastIpolSelection', Pickle.dumps(vtxSel), type = 'string')
                    
    vtxSel = cmds.ls(cmds.polyListComponentConversion(vtxSel, fe = True, ff = True, fv = True, tv = True),fl = True)
#    vtxSel = filterIpolSelection(vtxSel)
    vtxSel = [i.replace(baseMeshDISP, baseMesh) for i in vtxSel]
    cmds.setToolTo('selectSuperContext')
    cmds.select(cl = True)
    
    baseMeshGrp = cmds.getAttr(currNode + '.baseMeshGroup')
    i3DGrp = 'charInterpolation_' + baseMesh
    
    baseMeshGrpChildren = cmds.listRelatives(baseMeshGrp, c = True)

    historyDelete = []
 
    
    superGrp = 'superCurves_charInterpolation_' + baseMesh
    superCurves = []
    minimumSuperCurves = cmds.getAttr('gbNode.minimumSuperCurves')
    
    if superGrp in baseMeshGrpChildren:
        superCurves = cmds.listRelatives(cmds.listRelatives(superGrp, ad = True, typ = 'nurbsCurve'), p = True)
    
    if len(superCurves) < minimumSuperCurves:
        cmds.undoInfo( swf = True )
        reportGBMessage(' Please add at least ' + str(minimumSuperCurves) + ' Super Curves for Interpolation', True, True, 'red')
#        raise RuntimeError, ' Please add at least ' + str(minimumSuperCurves) + ' Super Curves for Interpolation'

    firstTime = 0
    i3DGrpChildren = []
    if not i3DGrp in baseMeshGrpChildren:
        cmds.group(name = i3DGrp, p = baseMeshGrp, em = True)
        firstTime = 1
    else:
        i3DGrpChildren = cmds.listRelatives(cmds.listRelatives(i3DGrp, ad = True, typ = 'nurbsCurve'), p = True)
        if i3DGrpChildren:
            checkAddRemoveSuperCurves('interpol')
   
    usedSuperCurvesString = cmds.getAttr(currNode + '.superCurves3D')
    usedSuperCurves = []
    if usedSuperCurvesString:
        usedSuperCurves = Pickle.loads(str(usedSuperCurvesString))
    else:
        firstTime = 1
    
    changeAgain = False
    if firstTime == 1:
        if cmds.getAttr(currNode + '.paintOnMesh') == cmds.getAttr(currNode + '.volumeMesh'):
            switchCurvesToOtherMesh()
            cmds.setAttr(currNode + '.paintOnMesh', cmds.getAttr(currNode + '.scalpMesh'), type = 'string')
            changeAgain = True
            
    maxCV = cmds.getAttr('gbNode.maxCV')
    if maxCV == 0:
        for crv in superCurves:
            ncv = cmds.getAttr(crv + '.spans') + cmds.getAttr(crv + '.degree')
            if ncv > maxCV:
                maxCV = ncv
        cmds.setAttr('gbNode.maxCV', maxCV)
    
    if firstTime == 1:
        superCurvesString = Pickle.dumps(superCurves)
        cmds.setAttr(currNode + '.superCurves3D', superCurvesString, type = 'string')
    
    if not (cmds.objExists(i3DGrp)):
        cmds.group(name = i3DGrp, p = baseMeshGrp, em = True)
    
    dispLayers = cmds.ls(type = 'displayLayer')
    
    if not baseMesh + '_charInterpolation_Curves'  in dispLayers:
        cmds.select(i3DGrp, r = True)
        dispLayer = cmds.createDisplayLayer(n = baseMesh + '_charInterpolation_Curves' )    
        cmds.setAttr(dispLayer + '.displayType', 2)
    
    ipolVerticesList = []
    ipolVerticesListString = cmds.getAttr(currNode + '.ipolVertices3D')
    if ipolVerticesListString:
        ipolVerticesList = Pickle.loads(str(ipolVerticesListString))
    
    
    if i3DGrpChildren:    
        vtxSel = [vtx for vtx in vtxSel if not 'ipol3DCrv_' + baseMesh + 'vtx_' + vtx.split(baseMesh + '.vtx[')[1].split(']')[0] in i3DGrpChildren]
    if not vtxSel:
        if changeAgain:
            switchCurvesToOtherMesh()
            cmds.setAttr(currNode + '.paintOnMesh', cmds.getAttr(currNode + '.volumeMesh'), type = 'string')
        cmds.undoInfo( swf = True )
        reportGBMessage('Interpolation is already performed on selected area', True, True, 'red')                
#        raise RuntimeError, 'Interpolation is already performed on selected area'
    
    charCPNode = createCPNode(baseMesh)
    historyDelete.append(charCPNode)
    cmds.setAttr(currNode + '.drawMeshCPNode', charCPNode, type = 'string')

    charFoll = createFollicle(cmds.getAttr(currNode + '.whichMesh'))
    historyDelete.append(charFoll)
    cmds.setAttr(currNode + '.drawMeshFollicle', charFoll, type = 'string')
    charFollShp = cmds.listRelatives(charFoll, s = True)[0]
 
    superCurvesPos = []        
    faceForDel = []        
    for crv in superCurves:

        cmds.rebuildCurve(crv , s = maxCV-3, degree = 3)
        cmds.delete(crv, ch = True)
        cmds.makeIdentity(crv, apply = True)
        superCurvesPos.append([cmds.xform(crv + '.cv[' + str(cv) + ']', q = True, ws = True, t = True) for cv in range(maxCV)])
        
        rootPos = cmds.xform(crv + '.cv[0]', q = True, ws = True, t = True)
        cmds.xform(crv, piv = rootPos)
        
        cmds.joint(p = (rootPos[0], rootPos[1], rootPos[2]), n = ('joint3D_' + crv))
        jName = cmds.ls(selection = True)[0]
        jointList.append(jName)
        cmds.setAttr(jName +'.visibility', False)
        historyDelete.append(jName)

        grp = cmds.group(name = 'nullGrp_' + crv, em = True, p = superGrp)
        historyDelete.append(grp)
        
        cmds.setAttr(charCPNode + '.ip', rootPos[0],  rootPos[1],  rootPos[2])
        cu = cmds.getAttr(charCPNode + '.u')
        cv = cmds.getAttr(charCPNode + '.v')
        faceForDel.append(cmds.getAttr(charCPNode + '.f'))
        cmds.setAttr(charFollShp + '.parameterU', cu)
        cmds.setAttr(charFollShp + '.parameterV', cv)
        prC = cmds.parentConstraint(charFoll, grp)
        cmds.delete(prC)
        cmds.parent(crv, grp)
        ipolVerticesList.append([])
    cmds.parent(jointList,superGrp)
    
    superCurvesPosString = Pickle.dumps(superCurvesPos)
    cmds.setAttr(currNode + '.superCurvesPos', superCurvesPosString, type = 'string')
        
    ipolVerticesString = Pickle.dumps(ipolVerticesList)
    cmds.setAttr(currNode + '.ipolVertices3D', ipolVerticesString, type = 'string')
        
    totalJointList = cmds.ls(cmds.listRelatives(superGrp, c = True),type = 'joint')
    clustName = mm.eval('findRelatedSkinCluster(' + dQ + baseMesh + dQ + ');')
    if clustName:
        cmds.delete(clustName)
    
    cmds.select(totalJointList, baseMesh)
    tempGBNode = cmds.getAttr('gbNode.tempGBNode')   
    clustName = cmds.skinCluster(name = tempGBNode, dr = 10.0, mi = 4, omi = False, tsb = True, sm = 0 )[0]
    yldSkin(baseMesh, totalJointList, faceForDel)
    cmds.select(cl = True)
        
    cmds.select(vtxSel, r = True)
#        print 'first time .. giving to interpolate'
#    print 'vtx for interpolation' , vtxSel

    interpolateOnFaces(vtxSel,clustName)
       
    cmds.skinCluster(clustName, edit = True, ub = True)
    for sup in superCurves:
        cmds.parent(sup, superGrp)
        
    for h in historyDelete:
    	if cmds.objExists(h):
            cmds.delete(h)
    
    if changeAgain:
        switchCurvesToOtherMesh()
        cmds.setAttr(currNode + '.paintOnMesh', cmds.getAttr(currNode + '.volumeMesh'), type = 'string')


    message = cmds.text('gbMessageStatusText', q = True, label = True)
    reportGBMessage(message, False, False, 'yellow')
    cmds.text('gbMessageStatusColor',edit = True, vis = True, bgc = [0.0,1.0,0.0])
    
    cmds.select(cl = True)
    cmds.undoInfo( swf = True )
    startGBUndo()
    
def removeInterpolationFromSelected(mode = 'manual'):
    
    if not cmds.button('startDrawBtn', q = True, vis = True):
        killPFXJob()
    stopGBUndo()
    import cPickle as Pickle
    
    currNode = cmds.getAttr('gbNode.currentGBNode')
    baseMesh = cmds.getAttr(currNode + '.scalpMesh')  
    scalpMeshDISP = baseMesh + '_DISPLAY'
    volumeMesh = cmds.getAttr(currNode + '.volumeMesh')
    vtxSel = cmds.ls(sl = True, fl = True, type = 'float3')
    vtxSel = [v for v in vtxSel if v.split('.')[0] == scalpMeshDISP or v.split('.')[0] == baseMesh or v.split('.')[0] == volumeMesh]
    if not vtxSel:
        reportGBMessage('Please select faces/vertices first of ' + scalpMeshDISP, True, True, 'red')
#        raise RuntimeError, 'Please select faces/vertices first of ' + scalpMeshDISP
    
    vtxSel = cmds.ls(cmds.polyListComponentConversion(vtxSel, ff = True, fv = True, tv = True),fl = True)
    cmds.select(cl = True)
    if scalpMeshDISP in vtxSel[0]:
        vtxSel = [i.replace(scalpMeshDISP, baseMesh) for i in vtxSel]
    elif volumeMesh in vtxSel[0]:
        vtxSel = [i.replace(volumeMesh, baseMesh) for i in vtxSel]
                
    baseMeshGrp = cmds.getAttr(currNode + '.baseMeshGroup')
    baseMeshGrpChildren = cmds.listRelatives(baseMeshGrp, c = True)
    i3DGrp = 'charInterpolation_' + baseMesh
    if baseMeshGrpChildren is None:
        reportGBMessage('Interpolation Does Not Exist', True, True, 'red')
#        raise RuntimeError, 'Interpolation Does Not Exist'
    i3DGrpChildren = []
    if baseMeshGrpChildren:
        if i3DGrp in baseMeshGrpChildren:
            i3DGrpChildren = cmds.listRelatives(cmds.listRelatives(i3DGrp, ad = True, typ = 'nurbsCurve'), p = True)
        else:
            reportGBMessage('Interpolation Does Not Exist', True, True, 'red')
#            raise RuntimeError, 'Interpolation Does Not Exist'
        if i3DGrpChildren is None:
#            print mode
            if mode == 'auto':
                return
            else:
                reportGBMessage('Interpolation Does Not Exist', True, True, 'red')
#            raise RuntimeError, 'Interpolation Does Not Exist'
        elif not i3DGrpChildren:
            reportGBMessage('Interpolation Does Not Exist', True, True, 'red')
#            raise RuntimeError, 'Interpolation Does Not Exist'
#    ipol3DCrv_pSphere1vtx_637    
    removeCurvesList = []
    removeVerticesList = []
    removeCurvesList = [crv for crv in i3DGrpChildren if baseMesh + '.vtx[' + crv.split('ipol3DCrv_' + baseMesh + 'vtx_')[1] + ']' in vtxSel]
    if not removeCurvesList and mode == 'manual':
        reportGBMessage('Interpolation Does Not Exist on Selected Area', True, True, 'red')
#        raise RuntimeError, 'Interpolation Does Not Exist on Selected Area'
    
#    $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    cmds.undoInfo( swf = False)
    origCurveCVpos = []
    closestPointPos = []
    dVector = []
    cvUV = []
    cvCountL = []
    curveFaces = []
    volumeResizePos = []
    
    removeIDList = []
    removedIpolCurves = []
    
    curveList4GraphString = cmds.getAttr(currNode + '.curveList4Graph')
    existList = []
    remVtxIDList = []
    rgbExists = False
    if curveList4GraphString: 
    
        existList = Pickle.loads(str(curveList4GraphString))
        
    if existList:
        remList = list(set(removeCurvesList) & set(existList))
        
        if remList:
            for crv in remList:
                removeIDList.append(existList.index(crv))

                if crv in i3DGrpChildren and 'ipol3DCrv_' + baseMesh + 'vtx_' in crv:
                    remVtxIDList.append(str(crv.split('ipol3DCrv_' + baseMesh + 'vtx_')[1]))
            
        
            origCurveCVpos = Pickle.loads(str(cmds.getAttr(currNode + '.origCurveCVpos')))
            closestPointPos = Pickle.loads(str(cmds.getAttr(currNode + '.closestPointPos')))
            dVector = Pickle.loads(str(cmds.getAttr(currNode + '.dVector')))
            cvUV = Pickle.loads(str(cmds.getAttr(currNode + '.cvUV')))
            cvCountL = Pickle.loads(str(cmds.getAttr(currNode + '.cvCountL')))
            curveFaces = Pickle.loads(str(cmds.getAttr(currNode + '.curveFaces')))
            rgbInfo = []
            rgbInfoString = cmds.getAttr(currNode + '.rgbInfo')
            if rgbInfoString:
                rgbInfo = Pickle.loads(str(rgbInfoString))
                rgbPerList = Pickle.loads(str(cmds.getAttr(currNode + '.rgbPerList')))
                rgbCurves = Pickle.loads(str(cmds.getAttr(currNode + '.rgbCurves')))
                rgbExists = True
                
            if cmds.getAttr(currNode + '.volumeResizePos'):
                volumeResizePos = Pickle.loads(str(cmds.getAttr(currNode + '.volumeResizePos')))
                
            
            
            toBeUpdatedIpol = []
            toBeUpdatedIpolString = cmds.getAttr(currNode + '.toBeUpdatedIpol')
            if toBeUpdatedIpolString:
                toBeUpdatedIpol = Pickle.loads(str(toBeUpdatedIpolString))
            if toBeUpdatedIpol:
                toBeUpdatedIpol = [x for y, x in enumerate(toBeUpdatedIpol) if y not in remVtxIDList]
                    
#                toBeUpdatedIpol = [x for y, x in enumerate(toBeUpdatedIpol) if y not in removeIDList]
                toBeUpdatedIpolString = Pickle.dumps(toBeUpdatedIpol)
                cmds.setAttr(currNode + '.toBeUpdatedIpol', toBeUpdatedIpolString, type = 'string')
                
            existList = [x for y, x in enumerate(existList) if y not in removeIDList]
            origCurveCVpos = [x for y, x in enumerate(origCurveCVpos) if y not in removeIDList]
            closestPointPos = [x for y, x in enumerate(closestPointPos) if y not in removeIDList]
            dVector = [x for y, x in enumerate(dVector) if y not in removeIDList]
            cvUV = [x for y, x in enumerate(cvUV) if y not in removeIDList]
            cvCountL = [x for y, x in enumerate(cvCountL) if y not in removeIDList]
            volumeResizePos = [x for y, x in enumerate(volumeResizePos) if y not in removeIDList]
            if rgbExists:
                rgbInfo = [x for y, x in enumerate(rgbInfo) if y not in removeIDList]
                rgbPerList = [x for y, x in enumerate(rgbPerList) if y not in removeIDList]
                
                for x in range(4):
                    for id in remVtxIDList:
                        if id in rgbCurves[x]:
                            rgbCurves[x].remove(id)
                            
                
                

                        
            for id in remVtxIDList:
                for cf in range(len(curveFaces)):
                    if id in curveFaces[cf]:
                        curveFaces[cf].remove(id)
            
            toBeResize = []
            if cmds.getAttr(currNode + '.toBeResize'):
                toBeResize = Pickle.loads(str(cmds.getAttr(currNode + '.toBeResize')))
                toBeResize = [x for x in toBeResize if x not in remVtxIDList]
#                for tbr in toBeResize:
#                    if not tbr.isdigit():
#                        print '5814', tbr
                toBeResizeString = Pickle.dumps(toBeResize)
                cmds.setAttr(currNode + '.toBeResize', toBeResizeString, type = 'string')
                
                
                        
                        
#            for id in removeIDList:
#                for cf in range(len(curveFaces)):
#                    if id in curveFaces[cf]:
#                        curveFaces[cf].remove(id)
                
    
            finalListString = Pickle.dumps(existList)
            origCurveCVposString = Pickle.dumps(origCurveCVpos)
            closestPointPosString = Pickle.dumps(closestPointPos)
            dVectorString = Pickle.dumps(dVector)
            cvUVString = Pickle.dumps(cvUV)
            cvCountLString = Pickle.dumps(cvCountL)
            curveFacesString = Pickle.dumps(curveFaces)
            removedIpolCurvesString = Pickle.dumps(removedIpolCurves)
            volumeResizePosString = Pickle.dumps(volumeResizePos)
            if rgbExists:
                rgbInfoString = Pickle.dumps(rgbInfo)
                rgbPerListString = Pickle.dumps(rgbPerList)
                rgbCurvesString = Pickle.dumps(rgbCurves)
            
            
            cmds.setAttr(currNode + '.curveList4Graph', finalListString, type = 'string')
            cmds.setAttr(currNode + '.origCurveCVpos', origCurveCVposString, type = 'string')
            cmds.setAttr(currNode + '.closestPointPos', closestPointPosString, type = 'string')
            cmds.setAttr(currNode + '.dVector', dVectorString, type = 'string')
            cmds.setAttr(currNode + '.cvUV', cvUVString, type = 'string')        
            cmds.setAttr(currNode + '.cvCountL', cvCountLString, type = 'string')
            cmds.setAttr(currNode + '.curveFaces', curveFacesString, type = 'string')
            cmds.setAttr(currNode + '.removedIpolFromGraph', removedIpolCurvesString, type = 'string')
            cmds.setAttr(currNode + '.volumeResizePos', volumeResizePosString, type = 'string')
            if rgbExists:
                cmds.setAttr(currNode + '.rgbInfo', rgbInfoString, type = 'string')
                cmds.setAttr(currNode + '.rgbPerList', rgbPerListString, type = 'string')
                cmds.setAttr(currNode + '.rgbCurves', rgbCurvesString, type = 'string')            
    
        
        

#    $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$    
        
    usedIpolVertices = Pickle.loads(str(cmds.getAttr(currNode + '.ipolVertices3D')))
    for supV in usedIpolVertices:
        for rc in removeCurvesList:
            vtxID = rc.split('ipol3DCrv_'  + baseMesh + 'vtx_')[1]
            if vtxID in supV:
                supV.remove(vtxID)
    ipolVerticesString = Pickle.dumps(usedIpolVertices)
    cmds.setAttr(currNode + '.ipolVertices3D', ipolVerticesString, type = 'string')
    
    if removeCurvesList:
        cmds.delete(removeCurvesList)
    
    if not checkIfIpolExists():
        if cmds.objExists(i3DGrp):
            cmds.delete(i3DGrp)
        dispLayers = cmds.ls(type = 'displayLayer')
        ipolLayer = baseMesh + '_charInterpolation_Curves'
        if ipolLayer in dispLayers:            
            cmds.delete(ipolLayer)
       
    cmds.undoInfo( swf = True)
    startGBUndo()
    
def checkSuperAndIpolForUpdate():
    
    if not cmds.button('startDrawBtn', q = True, vis = True):
        killPFXJob()
    stopGBUndo()
    import cPickle as Pickle
    
    currNode = cmds.getAttr('gbNode.currentGBNode')
    baseMesh = cmds.getAttr(currNode + '.scalpMesh')
    baseMeshGrp = cmds.getAttr(currNode + '.baseMeshGroup')
    minimumSuperCurves = cmds.getAttr('gbNode.minimumSuperCurves')
    baseMeshGrpChildren = cmds.listRelatives(baseMeshGrp, c = True)
    superGrp = 'superCurves_charInterpolation_' + baseMesh
    superCurves = []
    if superGrp in baseMeshGrpChildren:
        superCurves = cmds.listRelatives(cmds.listRelatives(superGrp, ad = True, typ = 'nurbsCurve'), p = True)
    
    i3DGrp = 'charInterpolation_' + baseMesh
    ipolCurves = []
    if i3DGrp in baseMeshGrpChildren: 
        ipolCurves = cmds.listRelatives(cmds.listRelatives(i3DGrp, ad = True, typ = 'nurbsCurve'), p = True)
        
        
    if not ipolCurves and not superCurves or len(superCurves) < minimumSuperCurves:
        reportGBMessage('Please add atleast ' + str(minimumSuperCurves) + ' Super Curves', True, True, 'red')
#        raise RuntimeError, 'Please add atleast ' + str(minimumSuperCurves) + ' Super Curves'
    
    if not ipolCurves and len(superCurves) >= minimumSuperCurves:
        reportGBMessage('Please select faces and perform Character Interpolation', True, True, 'red')
#        raise RuntimeError, 'Please select faces and perform Character Interpolation'
        
    if ipolCurves and len(superCurves) < minimumSuperCurves:
        cautionAddSuperCurves()
        return
    
    checkAddRemoveSuperCurves('manual')
    message = cmds.text('gbMessageStatusText', q = True, label = True)
    if message:
        reportGBMessage(message, False, False, 'yellow')
        cmds.text('gbMessageStatusColor',edit = True, vis = True, bgc = [0.0,1.0,0.0])   
    
    startGBUndo()
            
    
def cautionAddSuperCurves():
    
    currNode = cmds.getAttr('gbNode.currentGBNode')
    minimumSuperCurves = cmds.getAttr('gbNode.minimumSuperCurves')
    cmds.confirmDialog(title = 'Caution!', message = 'Current Interpolation does not reflect properly to available Super Curves. Please add atleast ' + str(minimumSuperCurves) + '  Super Curves', button = ['OK'])
    
        
def checkSuperAndIpolAllTime():
    
    import cPickle as Pickle
    
    currNode = cmds.getAttr('gbNode.currentGBNode')
    baseMesh = cmds.getAttr(currNode + '.scalpMesh')
    baseMeshGrp = cmds.getAttr(currNode + '.baseMeshGroup')
    baseMeshGrpChildren = cmds.listRelatives(baseMeshGrp, c = True)
    minimumSuperCurves = cmds.getAttr('gbNode.minimumSuperCurves')
    
    superGrp = 'superCurves_charInterpolation_' + baseMesh
    i3DGrp = 'charInterpolation_' + baseMesh
    
    superGrpChildren = []
    i3DGrpChildren = []
    
    if not baseMeshGrpChildren:
        return        
    if superGrp in baseMeshGrpChildren:
        superGrpChildren = cmds.listRelatives(cmds.listRelatives(superGrp, ad = True, typ = 'nurbsCurve'), p = True)
    i3DGrpChildren = []
    if i3DGrp in baseMeshGrpChildren:
        i3DGrpChildren = cmds.listRelatives(cmds.listRelatives(i3DGrp, ad = True, typ = 'nurbsCurve'), p = True)
    
    if superGrpChildren:        
        if len(superGrpChildren) < minimumSuperCurves:
            if i3DGrpChildren:
                cmds.warning('GroomBoy: Atleast ' + str(minimumSuperCurves) + ' Curves are needed to make current interpolation reliable')
            return
    
    if not i3DGrpChildren:
        return
    
    cmds.undoInfo( swf = False)
    if cmds.tabLayout('mainTabs', query = True, sti = True) == 2:
#        print 'from second tab'
        checkAddRemoveSuperCurves('adjVolTab')
    elif cmds.tabLayout('mainTabs', query = True, sti = True) == 1:
#        print '3'
        checkAddRemoveSuperCurves('auto')
    cmds.undoInfo( swf = True)        

def checkAddRemoveSuperCurves(mode):
    
    
    import cPickle as Pickle
    currNode = cmds.getAttr('gbNode.currentGBNode')
    baseMesh = cmds.getAttr(currNode + '.scalpMesh')
    changeAgain = False
    superGrp = 'superCurves_charInterpolation_' + baseMesh
    currentSups = cmds.listRelatives(cmds.listRelatives(superGrp, ad = True, typ = 'nurbsCurve'), p = True)
    if currentSups:
        if cmds.getAttr(currNode + '.paintOnMesh') == cmds.getAttr(currNode + '.volumeMesh'):
            switchCurvesToOtherMesh()
            cmds.setAttr(currNode + '.paintOnMesh', cmds.getAttr(currNode + '.scalpMesh'), type = 'string')
            changeAgain = True
        
    else:
        cmds.tabLayout('mainTabs', edit = True, sti = 1)
        cmds.evalDeferred('cmds.select(cl = True)')
        
        reportGBMessage('No Super Curves Exist. Current Interpolation is invalid', True, True,'red')     
        
    usedSups = []
    usedSupsPos = []
    usedSuperCurvesString = cmds.getAttr(currNode + '.superCurves3D')
    if usedSuperCurvesString:
        usedSups = Pickle.loads(str(usedSuperCurvesString))
        usedSupsPos = Pickle.loads(str(cmds.getAttr(currNode + '.superCurvesPos')))
        
    addSups = list(set(currentSups) - set(usedSups))
    remSups = list(set(usedSups) - set(currentSups))
#    print 'addSups', addSups
#    print 'remSups', remSups
    commonSups = list(set(currentSups) & set(usedSups))
    
    if commonSups:
        cmds.makeIdentity(commonSups, apply = True)
        for sup in commonSups:
            usedPos = usedSupsPos[usedSups.index(sup)]
            sp = cmds.getAttr(sup +'.spans')
            dg = cmds.getAttr(sup +'.degree') 
            ncv = sp + dg
            if not ncv == len(usedPos):
#                print 'edit1', sup
                addSups.append(sup)
                remSups.append(sup)
                continue
               
            for cv in range(ncv):
                currPos = cmds.xform(sup + '.cv[' + str(cv) + ']', q = True, ws = True, t = True)
                if max([abs(a - b) for a, b in zip(currPos, usedPos[cv])]) > 0.01:
#                if not  currPos == usedPos[cv]:
#                    print 'edit2', sup, usedSups.index(sup)
#                    print 'cv', cv
#                    print 'curr', currPos
#                    print 'used', usedPos[cv]
                    addSups.append(sup)
                    remSups.append(sup)
                    break
    
    
    if addSups or remSups:
        if mode == 'adjVolTab':
            cmds.tabLayout('mainTabs', edit = True, sti = 1)
            tabSelectChange()
            if changeAgain:
                switchCurvesToOtherMesh()
                cmds.setAttr(currNode + '.paintOnMesh', cmds.getAttr(currNode + '.volumeMesh'), type = 'string')
                changeAgain = False
#            askForUpdateInterpolation()
            option = cmds.confirmDialog( title='Update Interpolation Warning', message='Current Interpolation is not Updated. Would you like to Update?', button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No' )
            if option == 'Yes':
                updateCharInterpolation(currentSups, usedSups, addSups, remSups, mode)
                
                cmds.tabLayout('mainTabs', edit = True, sti = 2)
            else:
                return
                          
#            reportGBMessage('Current Interpolation does not reflect SuperCurves. Please Update Interpolation First', True, True, 'red')                
#            raise RuntimeError, 'Current Interpolation does not reflect SuperCurves. Please Update Interpolation First'
        else:                        
            updateCharInterpolation(currentSups, usedSups, addSups, remSups, mode)
#            createIpolPerSuper('auto')

        
        if changeAgain:
            switchCurvesToOtherMesh()
            cmds.setAttr(currNode + '.paintOnMesh', cmds.getAttr(currNode + '.volumeMesh'), type = 'string')
            changeAgain = False        
        
                 
                
    elif mode == 'manual':
        if changeAgain:
            switchCurvesToOtherMesh()
            cmds.setAttr(currNode + '.paintOnMesh', cmds.getAttr(currNode + '.volumeMesh'), type = 'string')
            changeAgain = False        
        reportGBMessage(' Interpolation Already Updated ', False, True, 'yellow')            
#        cmds.warning(' Interpolation Already Updated ')
    
#    if cmds.getAttr(currNode + '.performIPS'):
#        createIpolPerSuper('auto')
#    createIPSforClump()

def createIpolGrp():
    
    currNode = cmds.getAttr('gbNode.currentGBNode')
    baseMesh = cmds.getAttr(currNode + '.scalpMesh')
    baseMeshGrp = cmds.getAttr(currNode + '.baseMeshGroup')
    baseMeshGrpChildren = cmds.listRelatives(baseMeshGrp, c = True)
    i3DGrp = 'charInterpolation_' + baseMesh
    createIpol = False
    if baseMeshGrpChildren is None:
        createIpol = False
    if baseMeshGrpChildren:
        if not i3DGrp in baseMeshGrpChildren:
            createIpol = True
    if createIpol:
        cmds.group(name = i3DGrp, p = baseMeshGrp, em = True)
        dispLayers = cmds.ls(type = 'displayLayer')
    
        if not baseMesh + '_charInterpolation_Curves'  in dispLayers:
            cmds.select(i3DGrp, r = True)
            dispLayer = cmds.createDisplayLayer(n = baseMesh + '_charInterpolation_Curves' )    
            cmds.setAttr(dispLayer + '.displayType', 2)
                        
                    

        
def updateCharInterpolation(currentSups, usedSups, addSups, remSups, mode):
    
    import cPickle as Pickle
    currNode = cmds.getAttr('gbNode.currentGBNode')
    baseMesh = cmds.getAttr(currNode + '.scalpMesh')
    
    historyDelete = []
    maxCV = cmds.getAttr('gbNode.maxCV')
    superGrp = 'superCurves_charInterpolation_' + baseMesh
    
    extraForIPS = []
    extraForIPS = getVtxForIPS()
    if extraForIPS:
        extraForIPS = [baseMesh + '.vtx[' + vtx.split(baseMesh + '_DISPLAY.vtx[')[1].split(']')[0] + ']' for vtx in extraForIPS]
    
    i3DGrp = 'charInterpolation_' + baseMesh
    createIpolGrp()
    i3DGrpChildren = []
    i3DGrpChildren = cmds.listRelatives(i3DGrp, c = True)
#    print 'ipol curves', i3DGrpChildren
    if i3DGrpChildren:
        checkVertices = [baseMesh + '.vtx[' + i.split('ipol3DCrv_' + baseMesh + 'vtx_')[1] + ']' for i in i3DGrpChildren if 'ipol3DCrv_' in i]
    else:
        checkVertices = extraForIPS        
#    print 'check vertices', checkVertices
    usedIpolVerticesString = cmds.getAttr(currNode + '.ipolVertices3D') 
    usedIpolVertices = Pickle.loads(str(usedIpolVerticesString))
    finalVertices = []
    
    
    superCurvesPos = Pickle.loads(str(cmds.getAttr(currNode + '.superCurvesPos') ))
   
    if remSups:
#        print 'REMOVE', remSups
        remove = 1
        
        delCurve = []
        delVtx = []
        delPos = []
        
        
        for rem in remSups:
            curveIndex = usedSups.index(rem)
            delCurve.append(usedSups[curveIndex])
            delVtx.append(usedIpolVertices[curveIndex])
            delPos.append(superCurvesPos[curveIndex])
            for vtx in usedIpolVertices[curveIndex]:
                finalVertices.append(baseMesh + '.vtx[' + vtx + ']')
            
          
        for x in range(len(remSups)):
            usedSups.remove(delCurve[x])
            usedIpolVertices.remove(delVtx[x])
            superCurvesPos.remove(delPos[x])

    jointList = []
    add = 0
    
    if addSups:
#        print 'ADD', addSups
        add = 1
       
        
        for crv in addSups:
            usedSups.append(crv)
            
            usedIpolVertices.append([])
            
            
    charCPNode = createCPNode(baseMesh)
    cmds.setAttr(currNode + '.drawMeshCPNode', charCPNode, type = 'string')
    historyDelete.append(charCPNode)
    
    charFoll = createFollicle(cmds.getAttr(currNode + '.whichMesh'))
    cmds.setAttr(currNode + '.drawMeshFollicle',charFoll, type = 'string')
    charFollShp = cmds.listRelatives(charFoll, s = True)[0]
    historyDelete.append(charFoll)
    jointList = []
    faceForDel = []
    for crv in currentSups:
#        print 'currentSups', currentSups
        cmds.rebuildCurve(crv , s = maxCV-3, degree = 3)
        cmds.makeIdentity(crv, apply = True)
        rootPos = cmds.xform(crv + '.cv[0]', q = True, ws = True, t = True)
        cmds.xform(crv, piv = rootPos)
        
        cmds.joint(p = (rootPos[0], rootPos[1], rootPos[2]), n = ('joint3D_' + crv))
        jName = cmds.ls(selection = True)[0]
        jointList.append(jName)
        cmds.setAttr(jName +'.visibility', False)
        historyDelete.append(jName)
        
        grp = cmds.group(name = 'nullGrp_' + crv, em = True, p = superGrp)
        historyDelete.append(grp)
        
        cmds.setAttr(charCPNode + '.ip', rootPos[0],  rootPos[1],  rootPos[2])
        cu = cmds.getAttr(charCPNode + '.u')
        cv = cmds.getAttr(charCPNode + '.v')
        faceForDel.append(cmds.getAttr(charCPNode + '.f'))
        cmds.setAttr(charFollShp + '.parameterU', cu)
        cmds.setAttr(charFollShp + '.parameterV', cv)
        prC = cmds.parentConstraint(charFoll, grp)
        cmds.delete(prC)
        cmds.parent(crv, grp)
    cmds.parent(jointList,superGrp)
    
    
    clustName = ''
    totalJointList = cmds.ls(cmds.listRelatives(superGrp, c = True),type = 'joint')
    clustName = mm.eval('findRelatedSkinCluster(' + dQ + baseMesh + dQ + ');')
    if clustName:
        cmds.delete(clustName)
    
    cmds.select(totalJointList, baseMesh)
    tempGBNode = cmds.getAttr('gbNode.tempGBNode')   
    clustName = cmds.skinCluster(name = tempGBNode, dr = 10.0, mi = 4, omi = False, tsb = True, sm = 0 )[0]
    yldSkin(baseMesh, totalJointList,faceForDel)
    cmds.select(cl = True)

    if add == 1:
        skinList = []
        totalJointList = cmds.skinCluster(clustName, inf = True , q = True)

        for vtx in checkVertices:
#                vtx0 = cmds.ls(cmds.polyListComponentConversion(face, ff = True, tv = True),fl = True)[0]
            
            skinList = cmds.skinPercent(clustName, vtx , q = True, v = True)
            for super in addSups:
                if skinList[totalJointList.index('joint3D_' + super)] > 0.01:
                    finalVertices.append(vtx)
                    break
    
        
    superCurvesString = Pickle.dumps(currentSups)
    cmds.setAttr(currNode + '.superCurves3D', superCurvesString, type = 'string')

    ipolVerticesString = Pickle.dumps(usedIpolVertices)
    cmds.setAttr(currNode + '.ipolVertices3D', ipolVerticesString, type = 'string')
    
#    print len(finalVertices)
    
    if extraForIPS:
        finalVertices = list(set(finalVertices + extraForIPS))

    interpolateOnFaces(finalVertices, clustName)
    
    if clustName:
        cmds.skinCluster(clustName, edit = True, ub = True)

    superCurvesPos = []
    for sup in currentSups:
        cmds.parent(sup, superGrp)
        cmds.makeIdentity(sup, apply = True)
        superCurvesPos.append([cmds.xform(sup + '.cv[' + str(cv) + ']', q = True, ws = True, t = True) for cv in range(maxCV)])
    superCurvesPosString = Pickle.dumps(superCurvesPos)
    cmds.setAttr(currNode + '.superCurvesPos', superCurvesPosString, type = 'string')       
    
            
    for h in historyDelete:
    	if cmds.objExists(h):
            cmds.delete(h)    
    
#    message = cmds.text('gbMessageStatusText', q = True, label = True)
#    reportGBMessage(message, False, False, 'yellow')
#    cmds.text('gbMessageStatusColor',edit = True, vis = True, bgc = [0.0,1.0,0.0])
            

def getVtxForIPS():
    
    import cPickle as Pickle
    currNode = cmds.getAttr('gbNode.currentGBNode')
    if not cmds.objExists(currNode + '.performIPS'):
        return
    if not cmds.getAttr(currNode + '.performIPS'):
        return
    existIPS = []
    existIPSString = cmds.getAttr(currNode + '.existIPS')
    if existIPSString:
        existIPS = Pickle.loads(str(existIPSString))
    if existIPS:
#        print 'removing on', existIPS
        finalIPS = filterForExistingIpol(existIPS)
        if finalIPS:
            cmds.select(finalIPS, r = True)
            removeInterpolationFromSelected('auto')
    createIpolPerSuper('auto')
    existIPSString = cmds.getAttr(currNode + '.existIPS')
    if existIPSString:
        existIPS = Pickle.loads(str(existIPSString))
#    print 'giving back', existIPS        
    return existIPS        

def filterForExistingIpol(existIPS):
    
    currNode = cmds.getAttr('gbNode.currentGBNode')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    baseMeshGrp = cmds.getAttr(currNode + '.baseMeshGroup')
    baseMeshGrpChildren = cmds.listRelatives(baseMeshGrp, c = True)
    i3DGrp = 'charInterpolation_' + scalpMesh
    finalIPS = []
    i3DGrpChildren = []
    if baseMeshGrpChildren:
        if i3DGrp in baseMeshGrpChildren:
            i3DGrpChildren = cmds.listRelatives(cmds.listRelatives(i3DGrp, ad = True, typ = 'nurbsCurve'), p = True)
            for ips in existIPS:
                if 'ipol3DCrv_' + scalpMesh + 'vtx_' + ips.split(scalpMesh + '_DISPLAY.vtx[')[1].split(']')[0] in i3DGrpChildren:
                    finalIPS.append(ips)
    
    return finalIPS
            
def checkIfIpolExists():
    
    currNode = cmds.getAttr('gbNode.currentGBNode')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    baseMeshGrp = cmds.getAttr(currNode + '.baseMeshGroup')
    baseMeshGrpChildren = cmds.listRelatives(baseMeshGrp, c = True)
    i3DGrp = 'charInterpolation_' + scalpMesh
    i3DGrpChildren = []
    if baseMeshGrpChildren:
        if i3DGrp in baseMeshGrpChildren:
            i3DGrpChildren = cmds.listRelatives(cmds.listRelatives(i3DGrp, ad = True, typ = 'nurbsCurve'), p = True)
    if i3DGrpChildren:
        return True
    else:
        return False        
    
def checkIfFFExists():
    
    currNode = cmds.getAttr('gbNode.currentGBNode')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    baseMeshGrp = cmds.getAttr(currNode + '.baseMeshGroup')
    baseMeshGrpChildren = cmds.listRelatives(baseMeshGrp, c = True)
    i3DGrp = 'manualCurvesGrp_' + scalpMesh
    i3DGrpChildren = []
    if baseMeshGrpChildren:
        if i3DGrp in baseMeshGrpChildren:
            i3DGrpChildren = cmds.listRelatives(cmds.listRelatives(i3DGrp, ad = True, typ = 'nurbsCurve'), p = True)
    if i3DGrpChildren:
        return i3DGrpChildren
    else:
        return False           
    
def createIpolPerSuper(mode = 'manual'):
    
    stopGBUndo()
    import cPickle as Pickle
    currNode = cmds.getAttr('gbNode.currentGBNode')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    baseMeshGrp = cmds.getAttr(currNode + '.baseMeshGroup')
    baseMeshGrpChildren = cmds.listRelatives(baseMeshGrp, c = True)
        
    superGrp = 'superCurves_charInterpolation_' + scalpMesh
    
    if baseMeshGrpChildren:
        if not superGrp in baseMeshGrpChildren:
            if mode == 'auto':
                return []
            reportGBMessage('No Super Curves Exist', True, True, 'red')

    superGrpChildren = []    
    if cmds.objExists(superGrp):
        superGrpChildren = cmds.listRelatives(superGrp, c = True)      
    
    if not superGrpChildren:
        if mode == 'auto':
            return []
        reportGBMessage('No Super Curves Exist', True, True, 'red')
    
    cmds.setAttr(currNode + '.performIPS', True)
    scalpSuperCurvesPos = []
    scalpSuperCurvesPosString = cmds.getAttr(currNode + '.scalpSuperCurvesPos')
    if scalpSuperCurvesPosString:
        scalpSuperCurvesPos = Pickle.loads(str(scalpSuperCurvesPosString))    

    finalScalpPos = []
    if scalpSuperCurvesPos:
        finalScalpPos = [x[0] for x in scalpSuperCurvesPos]
    
    else:
        for sup in superGrpChildren:
            finalScalpPos.append(cmds.xform(sup + '.cv[0]', q = True, ws = True, t = True))
    vtxSel = []
    charCPNode = createCPNode(scalpMesh)
    scalpMeshDISP = scalpMesh + '_DISPLAY'
    for pos in finalScalpPos:
        cmds.setAttr(charCPNode + '.ip', pos[0], pos[1], pos[2])
        vtxID = cmds.getAttr(charCPNode + '.vt')
        vtxSel.append(scalpMeshDISP + '.vtx[' + str(vtxID) + ']')
    
#    cmds.select(vtxSel, r = True)
#    print vtxSel
    currentLastIpol = cmds.getAttr(currNode + '.lastIpolSelection')
#    removeExistingIpolPerSuper()
    existIPS = []
    existIPSString = cmds.getAttr(currNode + '.existIPS')

    if existIPSString:
        existIPS = Pickle.loads(str(existIPSString))
    if existIPS and mode == 'manual':
        cmds.select(existIPS, r = True)
        removeInterpolationFromSelected('auto')
#        print '??', existIPS

    existIPS = vtxSel        
#    print '!!', existIPS
    if not mode == 'auto':
        cmds.select(existIPS, r = True)
        charInterpolationSelectedFaces()
    
    cmds.delete(charCPNode)
    cmds.setAttr(currNode + '.existIPS', str(Pickle.dumps(existIPS)), type = 'string')
    if currentLastIpol:
        cmds.setAttr(currNode + '.lastIpolSelection', currentLastIpol, type = 'string')
    startGBUndo()
                    
                
                


# ---------------------------------------------------------------------------------------

# Graph Page Add - Remove
def addSelectedCurvesForGraph():
    
    stopGBUndo()
    killAllGBJobs()
    curveList = []
    if cmds.ls(sl = True):    
        curveList = cmds.listRelatives(cmds.listRelatives(cmds.ls(sl = True), ad = True, typ = 'nurbsCurve'), p = True)
    if not curveList:
        reportGBMessage('No Curves Selected', True, True, 'red')
#        raise RuntimeError, 'No Curves Selected'
#    print curveList, '<<< to add'
    cmds.select(curveList, r = True)
    touchCurvesToMesh()
    addCurvesForGraph(curveList, 'manual')
#    autoResize()
    updateMeshStripsForGBFFCUpdates([], curveList)
    updateMeshStripsForGBFFCUpdatesFromUI()
    autoResize()
#    checkManualAllTime()
    
#    if curveList:
#        regenerateClumpFF()
        
    startGBUndo()

def removeSelectedCurvesFromGraph():
    
    stopGBUndo()
    killAllGBJobs()
    curveList = []
    if cmds.ls(sl = True):
        curveList = cmds.listRelatives(cmds.listRelatives(cmds.ls(sl = True), ad = True, typ = 'nurbsCurve'), p = True)
    if not curveList:
        reportGBMessage('No Curves Selected', True, True, 'red')
#        raise RuntimeError, 'No Curves Selected'
    
    removeCurvesFromGraph('names', curveList)
    
    updateMeshStripsForGBFFCUpdates(curveList, [])
    updateMeshStripsForGBFFCUpdatesFromUI()
#    if curveList:
#        regenerateClumpFF()
        
    startGBUndo()
    
    
    
# Graph Init page add
def curvesForVolume():
    
    stopGBUndo()
    import cPickle as Pickle
    currNode = cmds.getAttr('gbNode.currentGBNode')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    
    lastState = cmds.getAttr(currNode + '.lastState')
    
    superGrp = 'superCurves_charInterpolation_' + scalpMesh
    superGrpChildren = []
    if cmds.objExists(superGrp):
        superGrpChildren = cmds.listRelatives(superGrp, c = True)    
    selected = cmds.ls(sl = True)
    if not selected:
        reportGBMessage('Nothing Selected', True, True, 'red')        
    
    curveList = cmds.listRelatives(cmds.listRelatives(selected, ad = True, typ = 'nurbsCurve'), p = True)
    if curveList:
        if superGrpChildren:
            curveList = [crv for crv in curveList if not crv in superGrpChildren]
    
    if not curveList:
        reportGBMessage('No Curves Selected', True, True, 'red')
#        raise RuntimeError, 'No Curves Selected'
#    s = Pickle.dumps(curveList)
#    cmds.setAttr(currNode + '.curveList4Graph', s, type = 'string')
    
    cmds.undoInfo(swf = False)
    cmds.setAttr(currNode + '.useManualForGraph', True)
    cmds.select(curveList, r = True)
    touchCurvesToMesh()
    addCurvesForGraph(curveList, 'manual')
    
    updateMeshStripsForGBFFCUpdates([], curveList)
    
    checkManualAllTime()
    
    cmds.button('continueToGraphBtn', edit = True, vis = True)
#    cmds.button('selGraphCurvesBtn', edit = True, vis = True)
#    cmds.undoInfo(swf = True)
    startGBUndo()
    
# Graph Init Page Ipol add
def ipolCurvesForVolume():
    
#    print 'ipolcurvesforvolume'
    stopGBUndo()
#    cmds.undoInfo(swf = False)
    import cPickle as Pickle
    currNode = cmds.getAttr('gbNode.currentGBNode')
#    baseMesh = cmds.getAttr(currNode + '.drawMesh')
    baseMesh = cmds.getAttr(currNode + '.scalpMesh')
    iPolGrp = 'charInterpolation_' + baseMesh
    if not cmds.objExists(iPolGrp):
        cmds.undoInfo(swf = True)
        reportGBMessage('No Interpolation Found', True, True, 'red')
#        raise RuntimeError, 'No Interpolation Found'
   
    grpChildren = cmds.listRelatives(iPolGrp, c = True)
    if not grpChildren:
        cmds.undoInfo(swf = True)
        reportGBMessage('No Interpolation Found', True, True, 'red')
    for child in grpChildren:
        if not cmds.nodeType(cmds.listRelatives(child, s = True)) == 'nurbsCurve':
            grpChildren.remove(child)
    if not grpChildren:
        cmds.undoInfo(swf = True)
        reportGBMessage('No Interpolation Found', True, True, 'red')
#        raise RuntimeError, 'No interpolation found'
        
    
    removedIpolFromGraph = []
    removedIpolFromGraphString = cmds.getAttr(currNode + '.removedIpolFromGraph')
    if removedIpolFromGraphString:
        removedIpolFromGraph = Pickle.loads(str(removedIpolFromGraphString))
        
    
    curveList = list(set(grpChildren) - set(removedIpolFromGraph))
    cmds.setAttr(currNode + '.useIpolForGraph', True)
    cmds.button('useIpolCurves', edit = True, vis = False)

    if curveList:
#        cmds.scriptJob(e = ['idle', 'addCurvesForGraph(curveList,\'ipol\')'], runOnce = True)
        addCurvesForGraph(curveList, 'ipol')
#        cmds.evalDeferred('addCurvesForGraph(curveList, \'ipol\')')
        if cmds.getAttr(currNode + '.lastState') == 'graphInit':
            cmds.button('continueToGraphBtn', edit = True, vis = True)

    
    cmds.undoInfo(swf = True)
    startGBUndo()
    
def loadBody():
    
    import cPickle as Pickle
    
    historyDelete = []
    
    currNode = cmds.getAttr('gbNode.currentGBNode')
    curveList = Pickle.loads(str(cmds.getAttr(currNode + '.curveList4Graph')))
        
    baseMesh = cmds.getAttr(currNode + '.paintOnMesh')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    if baseMesh == scalpMesh:
        
        attr = 'scalpMesh'
        targetAttr = 'volumeMesh'
#        print 'base is ', attr
#        print 'target is ', targetAttr
    else:
        attr = 'volumeMesh'
        targetAttr = 'scalpMesh'
#        print 'base is ', attr
#        print 'target is ', targetAttr

#    baseCPNode = cmds.getAttr(currNode + '.' + attr + 'CPNode')
#    targetCPNode = cmds.getAttr(currNode + '.' + targetAttr + 'CPNode')
    baseCPNode = createCPNode(baseMesh)
    historyDelete.append(baseCPNode)   
    targetCPNode = createCPNode(cmds.getAttr(currNode + '.' + targetAttr))
    historyDelete.append(targetCPNode)    
    targetFoll = createFollicle(targetAttr)
    historyDelete.append(targetFoll)
    targetFollShp = cmds.listRelatives(targetFoll, s = True)[0]
    
    
    origCurveCVpos = []
    closestPointPos = []
    distanceMax = []
    dVector = []
    cvCountL = []
    cv1 = []
    cp1 = []
    d1 = []
    dV = []
    uv1 = []
    cvUV = []
    
    
    for eachC in curveList:
        sp = cmds.getAttr(eachC +'.spans')
        dg = cmds.getAttr(eachC +'.degree') 
        ncv = sp + dg
        cvCountL.append(ncv)
        for cv in range(0,ncv):
            pos = cmds.xform((eachC + '.cv['+ str(cv) + ']'), query = True, ws = True, t = True)
            cmds.setAttr((baseCPNode + '.ip'),pos[0], pos[1], pos[2])
            cpU = cmds.getAttr(baseCPNode + '.u')
            cpV = cmds.getAttr(baseCPNode + '.v')
            if cv == 0:
                u0 = cpU
                v0 = cpV
            cmds.setAttr(targetFollShp + '.parameterU', cpU)
            cmds.setAttr(targetFollShp + '.parameterV', cpV)  
            cpPos = cmds.xform(targetFoll, q= True, ws = True, t = True)
            cmds.setAttr(targetCPNode + '.ip', cpPos[0], cpPos[1], cpPos[2])
            cpPos = list(cmds.getAttr(targetCPNode + '.p')[0])
            diffV = (cpPos[0] - pos[0], cpPos[1] - pos[1], cpPos[2] - pos[2])
            
            uv = (u0, v0)
            tpos = tuple(pos)
            tcpPos = tuple(cpPos)
  
            cv1.append(tpos)
            cp1.append(tcpPos)
            dV.append(diffV)
            
                
        origCurveCVpos.append(cv1)
        closestPointPos.append(cp1)
        dVector.append(dV)
        cvUV.append(uv)
        
            
        cv1 = []
        cp1 = []
        dV = []
        uv1 = []
    
    origCurveCVposString = Pickle.dumps(origCurveCVpos)
    closestPointPosString = Pickle.dumps(closestPointPos)
    dVectorString = Pickle.dumps(dVector)
    cvUVString = Pickle.dumps(cvUV)
    cvCountLString = Pickle.dumps(cvCountL)
    
#    print 'settting'
    cmds.setAttr(currNode + '.origCurveCVpos', origCurveCVposString, type = 'string')
    cmds.setAttr(currNode + '.closestPointPos', closestPointPosString, type = 'string')
    cmds.setAttr(currNode + '.dVector', dVectorString, type = 'string')
    cmds.setAttr(currNode + '.cvUV', cvUVString, type = 'string')        
    cmds.setAttr(currNode + '.cvCountL', cvCountLString, type = 'string')        
    
    for h in historyDelete:
        if cmds.objExists(h):
            cmds.delete(h)
        

def createManualCurvesGrp():
    
    currNode = cmds.getAttr('gbNode.currentGBNode')
    baseMeshGrp = cmds.getAttr(currNode + '.baseMeshGroup')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    manualGrp = 'manualCurvesGrp_' + scalpMesh
    baseMeshGrpChildren = cmds.listRelatives(baseMeshGrp, c = True)
    if not baseMeshGrpChildren:
        cmds.group(name = manualGrp, em = True, parent = baseMeshGrp)
    else:        
        if not manualGrp in baseMeshGrpChildren:
            cmds.group(name = manualGrp, em = True, parent = baseMeshGrp)
    return manualGrp    

def createRoughMarkingCurvesGrp():
    
    currNode = cmds.getAttr('gbNode.currentGBNode')
    baseMeshGrp = cmds.getAttr(currNode + '.baseMeshGroup')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    roughGrp = 'roughMarkingCurvesGrp_' + scalpMesh
    baseMeshGrpChildren = cmds.listRelatives(baseMeshGrp, c = True)
    if not baseMeshGrpChildren:
        cmds.group(name = roughGrp, em = True, parent = baseMeshGrp)
    else:        
        if not roughGrp in baseMeshGrpChildren:
            cmds.group(name = roughGrp, em = True, parent = baseMeshGrp)
    return roughGrp    
    
    
def addCurvesForGraph(curveList, mode):
    
    import cPickle as Pickle
    import time
    currNode = cmds.getAttr('gbNode.currentGBNode')
#    curveList = cmds.listRelatives(cmds.listRelatives(cmds.ls(sl = True), ad = True, typ = 'nurbsCurve'), p = True)
#    if not curveList:
#        raise RuntimeError, 'No Curves Selected'
    
    historyDelete = []
    
    curveList4GraphString = cmds.getAttr(currNode + '.curveList4Graph')
    
    origCurveCVpos = []
    closestPointPos = []
    dVector = []
    cvUV = []
    cvCountL = []
    curveFaces = []
    volumeResizePos = []
    rgbExists = False
    regionExists = False
    flM = 0
    flS = 0
    
    if not curveList4GraphString:
        existList = []
        oldCount = 0
        newList = curveList

    else:
        existList = Pickle.loads(str(curveList4GraphString))
        oldCount = len(existList)
        newList = list(set(curveList) - set(existList))
#        newList = [crv for crv in curveList if crv not in existList]
        origCurveCVpos = Pickle.loads(str(cmds.getAttr(currNode + '.origCurveCVpos')))
        closestPointPos = Pickle.loads(str(cmds.getAttr(currNode + '.closestPointPos')))
        dVector = Pickle.loads(str(cmds.getAttr(currNode + '.dVector')))
        cvUV = Pickle.loads(str(cmds.getAttr(currNode + '.cvUV')))
        cvCountL = Pickle.loads(str(cmds.getAttr(currNode + '.cvCountL')))
        curveFaces = Pickle.loads(str(cmds.getAttr(currNode + '.curveFaces')))
        
        rgbInfoString = cmds.getAttr(currNode + '.rgbInfo')
        if rgbInfoString:
            rgbInfo = Pickle.loads(str(rgbInfoString))
            rgbPerList = Pickle.loads(str(cmds.getAttr(currNode + '.rgbPerList')))
            rgbExists = True
        
        
        regionPerListString = cmds.getAttr(currNode + '.regionPerList')
        if regionPerListString:
            regionPerList = Pickle.loads(str(regionPerListString))
            regionExists = True
        
        if cmds.getAttr(currNode + '.volumeResizePos'):
            volumeResizePos = Pickle.loads(str(cmds.getAttr(currNode + '.volumeResizePos')))

#    for crv in newList:
#        existList.append(crv)
    
    

    removedIpolFromGraph = []
    removedIpolFromGraphString = cmds.getAttr(currNode + '.removedIpolFromGraph')
    if removedIpolFromGraphString:
        removedIpolFromGraph = Pickle.loads(str(removedIpolFromGraphString)) 

    if removedIpolFromGraph:
        if mode == 'auto':
            newList = [crv for crv in newList if crv not in removedIpolFromGraph]
        elif mode == 'manual':
            removedIpolFromGraph = list(set(removedIpolFromGraph) - set(newList))
            removedIpolFromGraphString = Pickle.dumps(removedIpolFromGraph)
            cmds.setAttr(currNode + '.removedIpolFromGraph', removedIpolFromGraphString, type = 'string')

            
            
        
        
    existList.extend(newList)
    finalListString = Pickle.dumps(existList)
    cmds.setAttr(currNode + '.curveList4Graph', finalListString, type = 'string')
    
            
    baseMesh = cmds.getAttr(currNode + '.paintOnMesh')
#    baseMesh = cmds.getAttr(currNode + '.scalpMesh')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    
    totalFaces = cmds.polyEvaluate(baseMesh, f = True)
    if not curveFaces:
        for f in range(0,totalFaces):
            curveFaces.append([])
            
    if baseMesh == scalpMesh:
        
        attr = 'scalpMesh'
        targetAttr = 'volumeMesh'
#        print 'base is ', attr
#        print 'target is ', targetAttr
    else:
        attr = 'volumeMesh'
        targetAttr = 'scalpMesh'
#        print 'base is ', attr
#        print 'target is ', targetAttr

#    baseCPNode = cmds.getAttr(currNode + '.' + attr + 'CPNode')
#    targetCPNode = cmds.getAttr(currNode + '.' + targetAttr + 'CPNode')
    baseCPNode = createCPNode(baseMesh)
    historyDelete.append(baseCPNode)
    smoothNode = ''
    if targetAttr == 'volumeMesh':
        smoothNode = cmds.polySmooth(cmds.getAttr(currNode + '.' + targetAttr))[0]   
    targetCPNode = createCPNode(cmds.getAttr(currNode + '.' + targetAttr))
    historyDelete.append(targetCPNode)
    
    targetFoll = createFollicle(targetAttr)
    historyDelete.append(targetFoll)
    targetFollShp = cmds.listRelatives(targetFoll, s = True)[0]
    distanceMax = []

    cv1 = []
    cp1 = []
    d1 = []
    dV = []
    uv1 = []
   
    currentCount = len(newList)
    progBarVis = False
    if cmds.getAttr(currNode + '.lastState') == 'graphInit':
        progBarVis = True   
    if currentCount > 1:
        cmds.text('gbProgressBarText', edit = True,  vis = progBarVis, label = 'Adding ' + str(currentCount) + 'Curves for Graph')        
        cmds.progressBar('gbProgressBar', edit = True, pr = 0, max = currentCount, vis = progBarVis)
    
#    print 'oldcount', oldCount
#    print newList
#    print len(newList)
    zeroPos = [0.0,0.0,0.0]
    zeroDistFound = False
    ipol3DGrpChildren = []
    if mode == 'manual':
        manualCurves = []
        
        cmds.setAttr(currNode + '.useManualForGraph', True)
        groupUnder = createManualCurvesGrp()
    elif mode == 'ipol':
        groupUnder = 'charInterpolation_' + scalpMesh
    
    i3DGrp = 'charInterpolation_' + scalpMesh
    i3DGrpChildren = []
    if cmds.objExists(i3DGrp):      
        i3DGrpChildren = cmds.listRelatives(cmds.listRelatives(i3DGrp, ad = True, typ = 'nurbsCurve'), p = True)
        iPrefix = 'ipol3DCrv_' + scalpMesh + 'vtx_'
    
            
                
    
    for crv in newList:
        currParent = cmds.listRelatives(crv, p = True)
        if not currParent:
            cmds.parent(crv, groupUnder)
        else:    
            if currParent[0] == i3DGrp:
                continue
            elif not currParent[0] == groupUnder:            
                cmds.parent(crv, groupUnder)
    
    toBeResizeString =  cmds.getAttr(currNode + '.toBeResize')
    toBeResizeList = []
    if toBeResizeString:
        toBeResizeList = Pickle.loads(str(toBeResizeString))    
    
        
    toBeResizeList = list(set(toBeResizeList + convertCurveToIDList(newList)))
#    for tbr in toBeResizeList:
#        if not tbr.isdigit():
#            print '6616', tbr
            
    
    toBeResizeListString = Pickle.dumps(toBeResizeList)  
    cmds.setAttr(currNode + '.toBeResize', toBeResizeListString, type = 'string')   
    
    
    totalIter = currentCount
    percentCheck = [(per * totalIter) / 100 for per in range(0,100,10)]
    masterTime = time.time()      
    iter = 0
    checkTime = False
    firstLoop = False
    bgRGB = [0,1,1]
    
        
    
    
    for eachC in range(0,currentCount):
        
        
        if iter in percentCheck:
            checkTime = True
        else:
            checkTime = False            

        if checkTime:
            loopStart = time.time()
                
        iter = iter + 1

        
        
        sp = cmds.getAttr(newList[eachC] +'.spans')
        dg = cmds.getAttr(newList[eachC] +'.degree') 
        ncv = sp + dg
        

        curveID = oldCount + eachC
#        print 'curveId' , curveID
        cv = 0
        while cv < ncv:
#        for cv in range(0,ncv):
            pos = cmds.xform((newList[eachC] + '.cv['+ str(cv) + ']'), query = True, ws = True, t = True)
            cmds.setAttr((baseCPNode + '.ip'),pos[0], pos[1], pos[2])
            cpU = cmds.getAttr(baseCPNode + '.u')
            cpV = cmds.getAttr(baseCPNode + '.v')
            
                
            if cv == 0:
                u0 = cpU
                v0 = cpV
            cmds.setAttr(targetFollShp + '.parameterU', cpU)
            cmds.setAttr(targetFollShp + '.parameterV', cpV)  
            cpPos = cmds.xform(targetFoll, q = True, ws = True, t = True)
            
            if not zeroDistFound:
                 if -0.25 <= cpPos[0] <= 0.25 and -0.25 <= cpPos[1] <= 0.25 and -0.25 <= cpPos[2] <= 0.25:
#                dist = math.sqrt(cpPos[0]**2 + cpPos[1]**2 + cpPos[2]**2)
#                if dist <= 0.25:
                    zeroDistFound = True
                    zeroPos = cpPos
                
#            countThis = True
            if cpPos == zeroPos:
#                print 'entered zeroPos ADD', newList[eachC]
                countThis = False
                ncv = ncv - 1
                cmds.delete(newList[eachC] + '.cv[' + str(cv) + ']')

            else:

                cv = cv + 1                
                cpF = cmds.getAttr(baseCPNode + '.f')
                
                if newList[eachC] in i3DGrpChildren:
                    if not newList[eachC].split(iPrefix)[1] in curveFaces[cpF]:
                        curveFaces[cpF].append(newList[eachC].split(iPrefix)[1])
                else:
                    if not newList[eachC] in curveFaces[cpF]:
                        curveFaces[cpF].append(newList[eachC])

                    
    #            cmds.setAttr(targetCPNode + '.ip', cpPos[0], cpPos[1], cpPos[2])
    #            cpPos = list(cmds.getAttr(targetCPNode + '.p')[0])
                diffV = (cpPos[0] - pos[0], cpPos[1] - pos[1], cpPos[2] - pos[2])
                
                uv = (u0, v0)
                tpos = tuple(pos)
                tcpPos = tuple(cpPos)
      
                cv1.append(tpos)
                cp1.append(tcpPos)
                dV.append(diffV)
            
        

        cvCountL.append(ncv)        
        origCurveCVpos.append(cv1)
        closestPointPos.append(cp1)
        dVector.append(dV)
        cvUV.append(uv)
        volumeResizePos.append([])

        
            
        cv1 = []
        cp1 = []
        dV = []
        uv1 = []
        
        cmds.text('gbProgressBarText', edit = True, label = 'Adding Curves for Volume Adjust : ' + str(currentCount - eachC) + ' Curves Remaining')
        cmds.progressBar('gbProgressBar', edit = True, s = 1)
        
        if checkTime:
            timeRemaining = (time.time() - loopStart) * (totalIter - iter)
            trM, trS = divmod(timeRemaining, 60)
    
            if not firstLoop and trS > 1.0:
                flM = trM
                flS = trS 
                firstLoop = True
            
        timeElapsed = time.time() - masterTime
        teM, teS = divmod(timeElapsed, 60)
        messageString = 'Time Remaining: ' + str('%02d' % trM) + ':' + str('%02d' % trS) + '\t' + 'Time Elapsed: ' + str('%02d' % teM) + ':' + str('%02d' % teS) 

        cmds.text('gbMessageStatusText', edit = True, vis = True,  label = '  ' + messageString)
        bgRGB = list(mm.eval('hsv_to_rgb <<' + str(remapNew(0,0.333,0,totalIter,iter)) + ',1.0,1.0>>;'))
        cmds.text('gbMessageStatusColor',edit = True, vis = True, bgc = bgRGB)
        
        
    
    origCurveCVposString = Pickle.dumps(origCurveCVpos)
    closestPointPosString = Pickle.dumps(closestPointPos)
    dVectorString = Pickle.dumps(dVector)
    cvUVString = Pickle.dumps(cvUV)
    cvCountLString = Pickle.dumps(cvCountL)
    curveFacesString = Pickle.dumps(curveFaces)
    volumeResizePosString = Pickle.dumps(volumeResizePos)
    
    

#    print 'settting'
    cmds.setAttr(currNode + '.origCurveCVpos', origCurveCVposString, type = 'string')
    cmds.setAttr(currNode + '.closestPointPos', closestPointPosString, type = 'string')
    cmds.setAttr(currNode + '.dVector', dVectorString, type = 'string')
    cmds.setAttr(currNode + '.cvUV', cvUVString, type = 'string')        
    cmds.setAttr(currNode + '.cvCountL', cvCountLString, type = 'string')
    cmds.setAttr(currNode + '.curveFaces', curveFacesString, type = 'string')  
    cmds.setAttr(currNode + '.volumeResizePos', volumeResizePosString, type = 'string')
       
    
    if rgbExists:
        for i in range(currentCount):
            rgbInfo.append([])
            rgbPerList.append([])
            
        rgbInfoString = Pickle.dumps(rgbInfo)
        rgbPerListString = Pickle.dumps(rgbPerList)            
        
        cmds.setAttr(currNode + '.rgbInfo', rgbInfoString, type = 'string') 
        cmds.setAttr(currNode + '.rgbPerList', rgbPerListString, type = 'string') 
        
    if regionExists:
        for i in range(currentCount):
            regionPerList.append([[],[]])
        
        regionPerListString = Pickle.dumps(regionPerList)
        cmds.setAttr(currNode + '.regionPerList', regionPerListString, type = 'string')
                
#    cmds.delete(targetFoll)
    for h in historyDelete:
        if cmds.objExists(h):
            cmds.delete(h)
            
    if smoothNode:
        cmds.delete(smoothNode)
    
    cmds.text('gbProgressBarText', edit = True,  vis = False)
    cmds.progressBar('gbProgressBar', edit = True, vis = False)
    cmds.progressBar('gbProgressBar', edit = True, pr = 0)
    
    if flM or flS:    
        finalMessage = 'Total Time Expected: ' + str('%02d' % flM) + ':' + str('%02d' % flS) + '\t' + 'Time Taken: ' + str('%02d' % teM) + ':' + str('%02d' % teS) 
        reportGBMessage(finalMessage, False, False, 'yellow')
        cmds.text('gbMessageStatusText', edit = True, label = finalMessage)
        cmds.text('gbMessageStatusColor',edit = True, vis = True, bgc = [0.0,1.0,0.0])
    
    
    

def removeCurvesFromGraph(cType, cList):
    
    
    import cPickle as Pickle
    currNode = cmds.getAttr('gbNode.currentGBNode')

#    print 'ctype' , cType
    origCurveCVpos = []
    closestPointPos = []
    dVector = []
    cvUV = []
    cvCountL = []
    curveFaces = []
    
    removeIDList = []
    removedIpolCurves = []
    
    curveList4GraphString = cmds.getAttr(currNode + '.curveList4Graph')
    lastState = cmds.getAttr(currNode + '.lastState')
    if not curveList4GraphString:
        reportGBMessage('Auto Resize Graph List Empty. ', True, True, 'red')
#        raise RuntimeError, ' Auto Resize Graph List Empty. '
        tabSelectChange()

    existList = Pickle.loads(str(curveList4GraphString))
    if not existList:
        reportGBMessage('Auto Resize Graph List Empty.', True, True, 'red')
#        raise RuntimeError, ' Auto Resize Graph List Empty. '
        tabSelectChange()
    
    removedIpolFromGraphString = cmds.getAttr(currNode + '.removedIpolFromGraph')
    if removedIpolFromGraphString:
        removedIpolCurves = Pickle.loads(str(removedIpolFromGraphString))
        

    
    if cType == 'id':
        removeIDList = cList
    
    else:
        remList = list(set(cList) & set(existList))
#        for crv in cList:
#            if crv in existList:
#                removeIDList.append(existList.index(crv))
#                if 'ipolCrv3D_' in crv:
#                    removedIpolCurves.append(crv)
        if not remList:
            reportGBMessage('Selected Curves are not part of Auto Resize Graph', True, True, 'red')
#            raise RuntimeError, 'Selected Curves are not part of Auto Resize Graph'
                
        scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
        iPrefix = 'ipol3DCrv_' + scalpMesh + 'vtx_'    
        for crv in remList:
            removeIDList.append(existList.index(crv))
            if lastState == 'graphPage':
#                if iPrefix in crv:
                removedIpolCurves.append(crv)
                    
        mixList = convertCurveToIDList(remList)    
    cmds.undoInfo(swf = False)
    origCurveCVpos = Pickle.loads(str(cmds.getAttr(currNode + '.origCurveCVpos')))
    closestPointPos = Pickle.loads(str(cmds.getAttr(currNode + '.closestPointPos')))
    dVector = Pickle.loads(str(cmds.getAttr(currNode + '.dVector')))
    cvUV = Pickle.loads(str(cmds.getAttr(currNode + '.cvUV')))
    cvCountL = Pickle.loads(str(cmds.getAttr(currNode + '.cvCountL')))
    curveFaces = Pickle.loads(str(cmds.getAttr(currNode + '.curveFaces')))
    volumeResizePos = Pickle.loads(str(cmds.getAttr(currNode + '.volumeResizePos')))
    
    manualCurves = []
    manualCurvesString = cmds.getAttr(currNode + '.manualCurves')
    if manualCurvesString:
        manualCurves = Pickle.loads(str(manualCurvesString))
        manualCurvesPos = Pickle.loads(str(cmds.getAttr(currNode + '.manualCurvesPos')))
        
        
    
    rgbInfoString = cmds.getAttr(currNode + '.rgbInfo')
    rgbExists = False
    if rgbInfoString:
        rgbInfo = Pickle.loads(str(rgbInfoString))
        rgbPerList = Pickle.loads(str(cmds.getAttr(currNode + '.rgbPerList')))
        rgbCurves = Pickle.loads(str(cmds.getAttr(currNode + '.rgbCurves')))
        rgbExists = True

    regionExists = False    
    regionPerListString = cmds.getAttr(currNode + '.regionPerList')
    if regionPerListString:
        regionPerList = Pickle.loads(str(regionPerListString))
        regionCtrlCurves = Pickle.loads(str(cmds.getAttr(currNode + '.regionCtrlCurves')))
        regionExists = True
    
    if lastState == 'graphPage':
        for id in removeIDList:
            for cv in range(0,cvCountL[id]):
                cmds.xform(existList[id] + '.cv[' + str(cv) + ']', ws = True, t = origCurveCVpos[id][cv])
            
                
    existList = [x for y, x in enumerate(existList) if y not in removeIDList]
    origCurveCVpos = [x for y, x in enumerate(origCurveCVpos) if y not in removeIDList]
    closestPointPos = [x for y, x in enumerate(closestPointPos) if y not in removeIDList]
    dVector = [x for y, x in enumerate(dVector) if y not in removeIDList]
    cvUV = [x for y, x in enumerate(cvUV) if y not in removeIDList]
    cvCountL = [x for y, x in enumerate(cvCountL) if y not in removeIDList]
    volumeResizePos = [x for y, x in enumerate(volumeResizePos) if y not in removeIDList]
    if rgbExists:
        rgbInfo = [x for y, x in enumerate(rgbInfo) if y not in removeIDList]
        rgbPerList = [x for y, x in enumerate(rgbPerList) if y not in removeIDList]
        for x in range(4):
            for id in mixList:
                if id in rgbCurves[x]:
                    rgbCurves[x].remove(id)
                    
    
    if regionExists:
        regionPerList = [x for y, x in enumerate(regionPerList) if y not in removeIDList]

        for x in range(len(regionCtrlCurves)):
            for id in mixList:
                if id in regionCtrlCurves[x]:
                    regionCtrlCurves[x].remove(id)
        
    manualRemove = False
    if manualCurves:
        manualRemove = True
#        print remList
        delCurve = []
        delPos = []
        
        for rem in remList:
            if rem in manualCurves:
                curveIndex = manualCurves.index(rem)
                delCurve.append(manualCurves[curveIndex])
                delPos.append(manualCurvesPos[curveIndex])
           
        if delCurve:          
            for x in range(len(remList)):
                manualCurves.remove(delCurve[x])
                manualCurvesPos.remove(delPos[x])
            
        
                            
        
        
#    curveFaces = [x for y, x in enumerate(curveFaces) if y not in removeIDList]


#    for id in removeIDList:
#       for cf in range(len(curveFaces)):
#            if id in curveFaces[cf]:
#                curveFaces[cf].remove(id)
            
    for id in mixList:
        for cf in range(len(curveFaces)):
            if id in curveFaces[cf]:
                curveFaces[cf].remove(id)
        
        
    finalListString = Pickle.dumps(existList)
    origCurveCVposString = Pickle.dumps(origCurveCVpos)
    closestPointPosString = Pickle.dumps(closestPointPos)
    dVectorString = Pickle.dumps(dVector)
    cvUVString = Pickle.dumps(cvUV)
    cvCountLString = Pickle.dumps(cvCountL)
    curveFacesString = Pickle.dumps(curveFaces)
    volumeResizePosString = Pickle.dumps(volumeResizePos)
    removedIpolCurvesString = Pickle.dumps(removedIpolCurves)
    if rgbExists:
        rgbInfoString = Pickle.dumps(rgbInfo)
        rgbPerListString = Pickle.dumps(rgbPerList)
        rgbCurvesString = Pickle.dumps(rgbCurves)
    if regionExists:
        regionCtrlCurvesString = Pickle.dumps(regionCtrlCurves)
        regionPerListString = Pickle.dumps(regionPerList)
                
    
    cmds.setAttr(currNode + '.curveList4Graph', finalListString, type = 'string')
    cmds.setAttr(currNode + '.origCurveCVpos', origCurveCVposString, type = 'string')
    cmds.setAttr(currNode + '.closestPointPos', closestPointPosString, type = 'string')
    cmds.setAttr(currNode + '.dVector', dVectorString, type = 'string')
    cmds.setAttr(currNode + '.cvUV', cvUVString, type = 'string')        
    cmds.setAttr(currNode + '.cvCountL', cvCountLString, type = 'string')
    cmds.setAttr(currNode + '.curveFaces', curveFacesString, type = 'string')
    cmds.setAttr(currNode + '.volumeResizePos', volumeResizePosString, type = 'string')
    cmds.setAttr(currNode + '.removedIpolFromGraph', removedIpolCurvesString, type = 'string')
    if rgbExists:
        cmds.setAttr(currNode + '.rgbInfo', rgbInfoString, type = 'string')
        cmds.setAttr(currNode + '.rgbPerList', rgbPerListString, type = 'string')
        cmds.setAttr(currNode + '.rgbCurves', rgbCurvesString, type = 'string')
    if regionExists:
        cmds.setAttr(currNode + '.regionCtrlCurves', regionCtrlCurvesString, type = 'string')
        cmds.setAttr(currNode + '.regionPerList', regionPerListString, type = 'string')
                
    
    if manualRemove:
        manualCurvesString = Pickle.dumps(manualCurves)
        manualCurvesPosString = Pickle.dumps(manualCurvesPos)
        
        cmds.setAttr(currNode + '.manualCurves', manualCurvesString, type = 'string')
        cmds.setAttr(currNode + '.manualCurvesPos', manualCurvesPosString, type = 'string')                
    
    toBeResize = []
    if cmds.getAttr(currNode + '.toBeResize'):
        toBeResize = Pickle.loads(str(cmds.getAttr(currNode + '.toBeResize')))
        toBeResize = [x for x in toBeResize if x not in mixList]
#        for tbr in toBeResize:
#            if not tbr.isdigit():
#                print '6985', tbr
        toBeResizeString = Pickle.dumps(toBeResize)
        cmds.setAttr(currNode + '.toBeResize', toBeResizeString, type = 'string')
    
    toBeUpdatedIpol = []    
    toBeUpdatedIpolString = cmds.getAttr(currNode + '.toBeUpdatedIpol')
    if toBeUpdatedIpolString:
        toBeUpdatedIpol = Pickle.loads(str(toBeUpdatedIpolString))
    if toBeUpdatedIpol:
        toBeUpdatedIpol = [x for x in toBeUpdatedIpol if x not in mixList]
        toBeUpdatedIpolString = Pickle.dumps(toBeUpdatedIpol)
        cmds.setAttr(currNode + '.toBeUpdatedIpol', toBeUpdatedIpolString, type = 'string')
        
    
    if not existList:
        showGraphInit()
#    else:
#        cmds.select(existList, r = True)
    cmds.undoInfo(swf = True)

def removeAndAddGraphCurves(curveIDList,prgBar):
    
#    print 'EDITING THRU REMOVE ADD'
    import cPickle as Pickle
    import time
    
    historyDelete = []
    currNode = cmds.getAttr('gbNode.currentGBNode')
    
    curveList4GraphString = cmds.getAttr(currNode + '.curveList4Graph')
    
    origCurveCVpos = []
    closestPointPos = []
    dVector = []
    cvUV = []
    cvCountL = []
    curveFaces = []
    volumeResizePos = []
    toBeResize = []
    
    

    existList = Pickle.loads(str(curveList4GraphString))
    oldCount = len(existList)
    
    origCurveCVpos = Pickle.loads(str(cmds.getAttr(currNode + '.origCurveCVpos')))
    closestPointPos = Pickle.loads(str(cmds.getAttr(currNode + '.closestPointPos')))
    dVector = Pickle.loads(str(cmds.getAttr(currNode + '.dVector')))
    cvUV = Pickle.loads(str(cmds.getAttr(currNode + '.cvUV')))
    cvCountL = Pickle.loads(str(cmds.getAttr(currNode + '.cvCountL')))
    curveFaces = Pickle.loads(str(cmds.getAttr(currNode + '.curveFaces')))
    volumeResizePos = Pickle.loads(str(cmds.getAttr(currNode + '.volumeResizePos')))

    rgbExists = False
    rgbInfoString = cmds.getAttr(currNode + '.rgbInfo')
    if rgbInfoString:
        rgbInfo = Pickle.loads(str(rgbInfoString))
        rgbPerList = Pickle.loads(str(cmds.getAttr(currNode + '.rgbPerList')))
        rgbCurves = Pickle.loads(str(cmds.getAttr(currNode + '.rgbCurves')))
        rgbExists = True
    
    regionExists = False
    regionPerListString = cmds.getAttr(currNode + '.regionPerList')
    if regionPerListString:
        regionPerList = Pickle.loads(str(regionPerListString))
        regionCtrlCurves = Pickle.loads(str(cmds.getAttr(currNode + '.regionCtrlCurves')))
    
    
    if cmds.getAttr(currNode + '.toBeResize'):
        toBeResize = Pickle.loads(str(cmds.getAttr(currNode + '.toBeResize')))
#    print 'push wala curveIDList', curveIDList
    againCurveIDList = convertCurveToIDList(curveIDList)        
#    toBeResize = list(set(toBeResize + curveIDList))
    toBeResize = list(set(toBeResize + againCurveIDList))
#    for tbr in toBeResize:
#        if not tbr.isdigit():
#            print '7063', tbr
    toBeResizeString = Pickle.dumps(toBeResize)
    cmds.setAttr(currNode + '.toBeResize', toBeResizeString, type = 'string')
    
    
    baseMesh = cmds.getAttr(currNode + '.paintOnMesh')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')

    if baseMesh == scalpMesh:
        attr = 'scalpMesh'
        targetAttr = 'volumeMesh'
#        print 'base is ', attr
#        print 'target is ', targetAttr
    
    else:
        attr = 'volumeMesh'
        targetAttr = 'scalpMesh'
#        print 'base is ', attr
#        print 'target is ', targetAttr
    
    baseCPNode = createCPNode(baseMesh)
    historyDelete.append(baseCPNode)
    
    smoothNode = ''
    if targetAttr == 'volumeMesh':
        smoothNode = cmds.polySmooth(cmds.getAttr(currNode + '.' + targetAttr))[0]   
    targetCPNode = createCPNode(cmds.getAttr(currNode + '.' + targetAttr))
    historyDelete.append(targetCPNode)
    
    targetFoll = createFollicle(targetAttr)
    historyDelete.append(targetFoll)
    targetFollShp = cmds.listRelatives(targetFoll, s = True)[0]
    distanceMax = []

    cv1 = []
    cp1 = []
    d1 = []
    dV = []
    uv1 = []
    
    zeroDistFound = False
    zeroPos = [0.0,0.0,0.0]
    progBarVis = True
    
    i3DGrp = 'charInterpolation_' + scalpMesh
    i3DGrpChildren = []
    if cmds.objExists(i3DGrp):      
        i3DGrpChildren = cmds.listRelatives(cmds.listRelatives(i3DGrp, ad = True, typ = 'nurbsCurve'), p = True)
        iPrefix = 'ipol3DCrv_' + scalpMesh + 'vtx_'
    
#    if cmds.getAttr(currNode + '.lastState') == 'graphInit':
#        progBarVis = True   
    currentCount = len(curveIDList)
    
    prgBar = 'gbWin|gbMenuBar|cL0Layout|gbProgressBarLyt|gbProgressBar'
    cmds.text('gbProgressBarText', edit = True, label = 'Updating Curves for Graph', vis = progBarVis)
    cmds.progressBar(prgBar, edit = True,  pr = 0, max = currentCount, vis = progBarVis)
    
    step = currentCount
    totalIter = step
    percentCheck = [(per * totalIter) / 100 for per in range(0,100,10)]
    masterTime = time.time()      
    iter = 0
    checkTime = False
    firstLoop = False
    bgRGB = [0,1,1]
    flM = 0
    flS = 0
    
    
    for id in curveIDList:
        for cf in range(len(curveFaces)):
            if id in curveFaces[cf]:
                curveFaces[cf].remove(id)
    
    if rgbExists:
        for x in range(4):
            for id in curveIDList:
                if id in rgbCurves[x]:
                    rgbCurves[x].remove(id)
    
    if regionExists:
        for x in range(len(regionCtrlCurves)):
            for id in curveIDList:
                if id in regionCtrlCurves[x]:
                    regionCtrlCurves[x].remove(id)                    
                    
                    
    step = len(curveIDList)
    
    mixCrvList = convertIDToCurveList(curveIDList)
    
    count = 0
    for crv in mixCrvList:
        
        if iter in percentCheck:
#            print iter
            checkTime = True
        else:
            checkTime = False            

        if checkTime:
            loopStart = time.time()
                
        iter = iter + 1
        
        try:        
            id = existList.index(crv)    
        except ValueError:
            continue            
                
        sp = cmds.getAttr(existList[id] +'.spans')
        dg = cmds.getAttr(existList[id] +'.degree') 
        ncv = sp + dg
#        print existList[id]

        cv = 0        
        while cv < ncv:
            pos = cmds.xform((existList[id] + '.cv['+ str(cv) + ']'), query = True, ws = True, t = True)
            cmds.setAttr((baseCPNode + '.ip'),pos[0], pos[1], pos[2])
            cpU = cmds.getAttr(baseCPNode + '.u')
            cpV = cmds.getAttr(baseCPNode + '.v')
            
    
            if cv == 0:
                u0 = cpU
                v0 = cpV
            cmds.setAttr(targetFollShp + '.parameterU', cpU)
            cmds.setAttr(targetFollShp + '.parameterV', cpV)  
            cpPos = cmds.xform(targetFoll, q= True, ws = True, t = True)
            
            if not zeroDistFound:
                if -0.25 <= cpPos[0] <= 0.25 and -0.25 <= cpPos[1] <= 0.25 and -0.25 <= cpPos[2] <= 0.25:
                    zeroDistFound =  True
                    zeroPos = cpPos
            
            if cpPos == zeroPos:
#                print 'entered zeroPos REMADD', existList[id]
#                print 'equal'
                ncv = ncv - 1
                cmds.delete(existList[id] + '.cv[' + str(cv) + ']')

            else:
#            cmds.setAttr(targetCPNode + '.ip', cpPos[0], cpPos[1], cpPos[2])
#            cpPos = list(cmds.getAttr(targetCPNode + '.p')[0])
                
                cv = cv + 1 
                cpF = cmds.getAttr(baseCPNode + '.f')
                
                if existList[id] in i3DGrpChildren:
                    if curveIDList[count] not in curveFaces[cpF]:
                        curveFaces[cpF].append(curveIDList[count])
                else:
                    if existList[id] not in curveFaces[cpF]:
                        curveFaces[cpF].append(existList[id])

#                if curveIDList[count] not in curveFaces[cpF]:
#                    curveFaces[cpF].append(curveIDList[count])
 
#    from add curves                    
#                if newList[eachC] in i3DGrpChildren:
#                    if not newList[eachC].split(iPrefix)[1] in curveFaces[cpF]:
#                        curveFaces[cpF].append(newList[eachC].split(iPrefix)[1])
#                else:
#                    if not newList[eachC] in curveFaces[cpF]:
#                        curveFaces[cpF].append(newList[eachC])
                
                
                                    
                diffV = (cpPos[0] - pos[0], cpPos[1] - pos[1], cpPos[2] - pos[2])
                
                uv = (u0, v0)
                tpos = tuple(pos)
                tcpPos = tuple(cpPos)
      
                cv1.append(tpos)
                cp1.append(tcpPos)
                dV.append(diffV)
            

        cvCountL[id] = ncv
                
        del origCurveCVpos[id][:]
        origCurveCVpos[id].extend(cv1)
        
        del closestPointPos[id][:]
        closestPointPos[id].extend(cp1)
        
        del dVector[id][:]
        dVector[id].extend(dV)
        
        del volumeResizePos[id][:]
        volumeResizePos[id].extend([])
        
        if rgbExists:
            del rgbInfo[id][:]
            rgbInfo[id].extend([])
            
            del rgbPerList[id][:]
            rgbPerList[id].extend([])
        
        if regionExists:
            del regionPerList[id][:]
            regionPerList[id].extend([[],[]])            
            
            
            
                    
        
        cvUV[id] = uv
            
        cv1 = []
        cp1 = []
        dV = []
        uv1 = []
        
        step = step - 1
        cmds.text('gbProgressBarText', edit = True, label = 'Updating Curves for Graph : ' + str(step) + ' Curves Remaining')
        cmds.progressBar(prgBar, edit = True, s = 1)
        
        count = count + 1
        
        if checkTime:
            timeRemaining = (time.time() - loopStart) * (totalIter - iter)
            trM, trS = divmod(timeRemaining, 60)
#            print bgRGB
    
            if not firstLoop and trS > 1.0:
                flM = trM
                flS = trS 
                firstLoop = True
        
        timeElapsed = time.time() - masterTime
        teM, teS = divmod(timeElapsed, 60)
        messageString = 'Time Remaining: ' + str('%02d' % trM) + ':' + str('%02d' % trS) + '\t' + 'Time Elapsed: ' + str('%02d' % teM) + ':' + str('%02d' % teS) 
#        reportGBMessage(messageString, False, False, 'blue')
        cmds.text('gbMessageStatusText', edit = True, vis = True,  label = '  ' + messageString)
#        bgRGB = list(mm.eval('hsv_to_rgb <<' + str(remapNew(0,0.333,0,totalIter,iter)) + ',1.0,' + str(remapNew(0.0,1.0,-1.0,1.0,math.sin(iter))) + '>>;'))
        bgRGB = list(mm.eval('hsv_to_rgb <<' + str(remapNew(0,0.333,0,totalIter,iter)) + ',1.0,1.0>>;'))
        cmds.text('gbMessageStatusColor',edit = True, vis = True, bgc = bgRGB)
        
                        
    
    origCurveCVposString = Pickle.dumps(origCurveCVpos)
    closestPointPosString = Pickle.dumps(closestPointPos)
    dVectorString = Pickle.dumps(dVector)
    cvUVString = Pickle.dumps(cvUV)
    cvCountLString = Pickle.dumps(cvCountL)
    curveFacesString = Pickle.dumps(curveFaces)
    volumeResizePosString = Pickle.dumps(volumeResizePos)
    if rgbExists:
        rgbInfoString = Pickle.dumps(rgbInfo)
        rgbPerListString = Pickle.dumps(rgbPerList)
        rgbCurvesString = Pickle.dumps(rgbCurves)
    if regionExists:
        regionPerListString = Pickle.dumps(regionPerList)        
        regionCtrlCurvesString = Pickle.dumps(regionCtrlCurves)        
        
    
#    cmds.setAttr(currNode + '.curveList4Graph', finalListString, type = 'string')
    cmds.setAttr(currNode + '.origCurveCVpos', origCurveCVposString, type = 'string')
    cmds.setAttr(currNode + '.closestPointPos', closestPointPosString, type = 'string')
    cmds.setAttr(currNode + '.dVector', dVectorString, type = 'string')
    cmds.setAttr(currNode + '.cvUV', cvUVString, type = 'string')        
    cmds.setAttr(currNode + '.cvCountL', cvCountLString, type = 'string')
    cmds.setAttr(currNode + '.curveFaces', curveFacesString, type = 'string')
    cmds.setAttr(currNode + '.volumeResizePos', volumeResizePosString, type = 'string')
    
    if rgbExists:
        cmds.setAttr(currNode + '.rgbInfo', rgbInfoString, type = 'string')
        cmds.setAttr(currNode + '.rgbPerList', rgbPerListString, type = 'string')	
        cmds.setAttr(currNode + '.rgbCurves', rgbCurvesString, type = 'string')	
    if regionExists:
        cmds.setAttr(currNode + '.regionPerList', regionPerListString, type = 'string')	
        cmds.setAttr(currNode + '.regionCtrlCurves', regionCtrlCurvesString, type = 'string')	
                
    
    
#    print origCurveCVpos
    for h in historyDelete:
        if cmds.objExists(h):
            cmds.delete(h)
            
    if smoothNode:
        cmds.delete(smoothNode)
    
    cmds.text('gbProgressBarText', edit = True, vis = False)
    cmds.progressBar('gbProgressBar', edit = True,  vis = False)
    cmds.progressBar('gbProgressBar', edit = True, pr = 0)
#    finalMessage = 'Total Time Expected: ' + str('%02d' % flM) + ':' + str('%02d' % flS) + '\t' + 'Time Taken: ' + str('%02d' % teM) + ':' + str('%02d' % teS) 
#    cmds.text('gbMessageStatusText', edit = True, vis = False, label = finalMessage)
    
    
    if flM or flS:    
        finalMessage = 'Total Time Expected: ' + str('%02d' % flM) + ':' + str('%02d' % flS) + '\t' + 'Time Taken: ' + str('%02d' % teM) + ':' + str('%02d' % teS) 
        reportGBMessage(finalMessage, False, False, 'yellow')
        cmds.text('gbMessageStatusText', edit = True, label = finalMessage)
        cmds.text('gbMessageStatusColor',edit = True, vis = True, bgc = [0.0,1.0,0.0])
    
    updateMeshStripsForGBFFCUpdates(mixCrvList,mixCrvList)
    checkManualAllTime()
        

def pushUpdatedIpolCurves(prgBar):
    
    import cPickle as Pickle
    currNode = cmds.getAttr('gbNode.currentGBNode')
    toBeUpdatedIpolString = cmds.getAttr(currNode + '.toBeUpdatedIpol')
    toBeUpdatedIpol = []
    if toBeUpdatedIpolString:
        toBeUpdatedIpol = Pickle.loads(str(toBeUpdatedIpolString))
        toBeUpdatedIpol = convertIDToCurveList(toBeUpdatedIpol)
    
    if toBeUpdatedIpol:
#        print 'tobeupdated', toBeUpdatedIpol
#        removeCurvesFromGraph('names', toBeUpdatedIpol)
#        addCurvesForGraph(toBeUpdatedIpol)
        removeAndAddGraphCurves(toBeUpdatedIpol,prgBar)
        
        message = cmds.text('gbMessageStatusText', q = True, label = True)
        reportGBMessage(message, False, False, 'yellow')
        cmds.text('gbMessageStatusColor',edit = True, vis = True, bgc = [0.0,1.0,0.0])


    cmds.setAttr(currNode + '.toBeUpdatedIpol','',type = 'string')


def convertIDToCurveList(idList):
    
    currNode = cmds.getAttr('gbNode.currentGBNode')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    baseMeshGrp = cmds.getAttr(currNode + '.baseMeshGroup')
    baseMeshGrpChildren = cmds.listRelatives(baseMeshGrp, c = True)
    i3DGrp = 'charInterpolation_' + scalpMesh
    ipol = False
    curveList = []
    i3DGrpChildren = []
    if i3DGrp in baseMeshGrpChildren:
        i3DGrpChildren = cmds.listRelatives(cmds.listRelatives(i3DGrp, ad = True, typ = 'nurbsCurve'), p = True)
        if i3DGrpChildren:
            ipol = True

#    ipol3DCrv_pSphere1vtx_637                
    iPrefix = 'ipol3DCrv_' + scalpMesh + 'vtx_'
    for id in idList:
        if id.isdigit():
            if iPrefix + id in i3DGrpChildren:
                curveList.append(iPrefix + id)
        else:
            curveList.append(id)
    
    return curveList            
    
            
def convertCurveToIDList(curveList):
    
    currNode = cmds.getAttr('gbNode.currentGBNode')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    baseMeshGrp = cmds.getAttr(currNode + '.baseMeshGroup')
    baseMeshGrpChildren = cmds.listRelatives(baseMeshGrp, c = True)
    i3DGrp = 'charInterpolation_' + scalpMesh
    ipol = False
    idList = []
    i3DGrpChildren = []
    if i3DGrp in baseMeshGrpChildren:
        i3DGrpChildren = cmds.listRelatives(cmds.listRelatives(i3DGrp, ad = True, typ = 'nurbsCurve'), p = True)
        if i3DGrpChildren:
            ipol = True
        else:
            return curveList            

#    ipol3DCrv_pSphere1vtx_637                
    iPrefix = 'ipol3DCrv_' + scalpMesh + 'vtx_'
    for crv in curveList:
        if crv in i3DGrpChildren:
            idList.append(crv.split(iPrefix)[1])
        else:
            idList.append(crv)
    
    return idList            
    
               
def autoResize():
    
    stopGBUndo()
    import cPickle as Pickle
    originalSelection = cmds.ls(sl = True)
    ctx = cmds.currentCtx()
    currNode = cmds.getAttr('gbNode.currentGBNode')
    
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    currentLocalCtrl = cmds.getAttr(currNode + '.currentLocalControl')
    mainGrp = cmds.getAttr(currNode + '.mainGroup')
    mainGrpChildren = cmds.listRelatives(mainGrp, c = True)

    
    if currentLocalCtrl == 'region':
        scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
        cmds.setToolTo('selectSuperContext')
        regionCtrlGrp = 'regionControlGrp_' + scalpMesh
        if not regionCtrlGrp in mainGrpChildren:
            interactiveRegionGraphUpdateOFF()
            reportGBMessage('No Region Controllers Exist, Please paint first', True, True, 'red')
#            raise RuntimeError, 'No Region Controllers Exist, Please paint first'
        regionCtrlGrpChildren = cmds.listRelatives(cmds.listRelatives(regionCtrlGrp, ad = True, typ = 'nurbsCurve'), p = True)
        if regionCtrlGrpChildren:
            regionCtrlGrpChildren = [ctrl for ctrl in regionCtrlGrpChildren if scalpMesh + '_regionCtrl_' in ctrl]
        if not regionCtrlGrpChildren:
            interactiveRegionGraphUpdateOFF()
            forceUpdateAllAutoResize()
            autoResizeGLOBAL()
            reportGBMessage('Minimum 3 Region Controllers should exist', True, True, 'red')
#            raise RuntimeError, 'Minimum 3 Region Controllers should exist'
        if len(regionCtrlGrpChildren) < 3:
            interactiveRegionGraphUpdateOFF()
            reportGBMessage('Minimum 3 Region Controllers should exist', True, True, 'red')
#            raise RuntimeError, 'Minimum 3 Region Controllers should exist'
    
    cmds.undoInfo(swf = False) 
    if currentLocalCtrl == 'color':
        autoResizeCOLOR()
    elif currentLocalCtrl == 'region':
#        print 'going for region'
        autoResizeREGION()
    else:
        autoResizeGLOBAL()
 
    if cmds.getAttr(currNode + '.isGraphRestored'):
#        print 'tried to restore'

       
#        storeStripChangesToDB('restore')
        restoreVolumeResizePos()
#        storeStripChangesToDB('store')
        
#        stripDictDB = getStripValuesDict()
#        if stripDictDB:
#            
 #           stripCurvatureChangeUI(bothNodes)
 #           storeRestoreRootVtxForStripShove(bothNodes, 'store')
 #           stripShoveChange(bothNodes, 'dict')
        
        cmds.setAttr(currNode + '.isGraphRestored', False)
    
    
    toBeResize = []
    toBeResizeString = cmds.getAttr(currNode + '.toBeResize')
    if toBeResizeString:
        toBeResize = Pickle.loads(str(toBeResizeString))
    if toBeResize:        
        checkForClumpUpdateFF(toBeResize)
        
    toBeResizeString = Pickle.dumps([])
    cmds.setAttr(currNode + '.toBeResize', toBeResizeString, type = 'string')        
    
    if originalSelection:
        cmds.select(originalSelection, r = True)
        cmds.setToolTo(ctx)
#    cmds.undoInfo(swf = True) 
    startGBUndo()
                            

 
          
def brainAutoResize(percentList):
    
    import cPickle as Pickle
    import random as random
    
    random.seed(9)
    currNode = cmds.getAttr('gbNode.currentGBNode')
    
    curveList = Pickle.loads(str(cmds.getAttr(currNode + '.curveList4Graph')))
    origCurveCVpos = Pickle.loads(str(cmds.getAttr(currNode + '.origCurveCVpos')))
    dVector = Pickle.loads(str(cmds.getAttr(currNode + '.dVector')))
    toBeResize = Pickle.loads(str(cmds.getAttr(currNode + '.toBeResize')))
    toBeResizeCurveList = convertIDToCurveList(toBeResize)
    volumeResizePos = []
    if cmds.getAttr(currNode + '.volumeResizePos'):
        volumeResizePos = Pickle.loads(str(cmds.getAttr(currNode + '.volumeResizePos')))
    else:
        for i in range(curveList):
            volumeResizePos.append([])    

    globalScale = cmds.intSliderGrp('globalScaleSlider', q = True, v = True) * 0.01 + 1.0
    globalRandom = cmds.intSliderGrp('globalRandomSlider', q = True, v = True) * 0.01
    
    clumpTweak = False
    if cmds.objExists(currNode + '.clumpOveride'):
        clumpTweak = cmds.getAttr(currNode + '.clumpOveride')
        if clumpTweak:
            clumpTweakPer = getClumpTweakPercent(toBeResizeCurveList)
    
        
    '''
    v = p1 - p0;
    Pd = p0 + d/||v|| * v
    => Pd = p0 + ((pc*||v||) / ||v||) * v
    => Pd = p0 + pc * v
    http://math.stackexchange.com/questions/105400/linear-interpolation-in-3-dimensions 
    '''

    stripDictDB = getStripValuesDict()
    if stripDictDB:
        stripCurves = list(set(toBeResizeCurveList) & set(stripDictDB.keys()))
        if stripCurves:
            extNodes = getStripExtrudeNodes(stripCurves)
            storeRestoreStripVtxPos([extNodes, stripCurves], 'restore')
    
    loopIndex = 0    
    for tbr in toBeResizeCurveList:
        crv = curveList.index(tbr)
#        rdm = random.uniform(
        volumePosCrv = []
#        print crv
        randPC = random.uniform(-1.0 * globalRandom, 0.0)
        for cv in range(0,len(origCurveCVpos[crv])):
            # Get the percentage
            
            pc = percentList[crv][cv] * globalScale
            pc = pc + randPC
            pc = max(min(pc, 200.0),0.0)
            # Add/Subtract as per Clump Tweak Graph
            if clumpTweak and clumpTweakPer:
                if clumpTweakPer[loopIndex]:
                    pc = pc + clumpTweakPer[loopIndex][cv]
                    pc = max(min(pc, 10000.0), 0.0)
            # Convert the tuple xyz to list 
            dVL = list(dVector[crv][cv])
            # Multiply the percentage to the total distance
            dVL1 = [dVL[0] * pc, dVL[1] * pc, dVL[2] * pc] 
            # p0 + (pc*v)
            newPos = [sum(pair) for pair in zip(list(origCurveCVpos[crv][cv]), dVL1)] 
            cmds.xform((curveList[crv] + '.cv[' + str(cv) + ']'), ws = True, t = newPos)
            volumePosCrv.append(newPos)
        volumeResizePos[crv] = volumePosCrv
        loopIndex = loopIndex + 1
    
    volumeResizePosString = Pickle.dumps(volumeResizePos)
    cmds.setAttr(currNode + '.volumeResizePos', volumeResizePosString, type = 'string')        
    checkForClumpUpdateFF(toBeResize)
    

    if stripDictDB:
        if stripCurves:
            bothNodes =  [extNodes, stripCurves]
            storeRestoreStripVtxPos(bothNodes, 'store')

            stpName = getStpNameFromExt(extNodes[0])
#        cmds.duplicate(stpName, name = 'Resize_store' + stpName)

            stripCurvatureChangeUI(bothNodes)
            storeRestoreRootVtxForStripShove(bothNodes, 'store')
            stripShoveChange(bothNodes, 'dict')
            updateMeshStripsForGBFFCUpdatesFromUI()
    
    

def autoResizeGLOBAL():
    
    import cPickle as Pickle
    currNode = cmds.getAttr('gbNode.currentGBNode')
    toBeResize = Pickle.loads(str(cmds.getAttr(currNode + '.toBeResize')))
    curveList = Pickle.loads(str(cmds.getAttr(currNode + '.curveList4Graph')))
    curveListIDList = convertCurveToIDList(curveList)
    
    currentGraph = cmds.gradientControlNoAttr('defaultColorGraph', q = True, asString = True)
    prevGraph = cmds.getAttr(currNode + '.defaultGraph')
    
    if currentGraph == prevGraph and not toBeResize:
        return
    if not currentGraph == prevGraph:
        toBeResizeString = Pickle.dumps(curveListIDList)
        cmds.setAttr(currNode + '.toBeResize', toBeResizeString, type = 'string')
    brainAutoResize(getPerGLOBAL())
#    len(curveList)        
                

def getPerGLOBAL():
   
    import cPickle as Pickle
    currNode = cmds.getAttr('gbNode.currentGBNode')
    curveList = Pickle.loads(str(cmds.getAttr(currNode + '.curveList4Graph')))
    toBeResize = Pickle.loads(str(cmds.getAttr(currNode + '.toBeResize')))
    toBeResizeCurveList = convertIDToCurveList(toBeResize)
    
    cvCountL = Pickle.loads(str(cmds.getAttr(currNode + '.cvCountL')))
    cmds.setAttr(currNode + '.defaultGraph', cmds.gradientControlNoAttr('defaultColorGraph', q = True, asString = True), type = 'string')
    
    allCper = []
    perC = []
    dictPer = []
    ''' Set will return only unique cvCount values '''
    onlyOnceCV = list(set(cvCountL)) 
    percentList = []
    allPerCrv = []

    ''' Build a dictionary which will query only once for different number of cvs '''
    
    # Create a list of dictionary 
    for x in range(0,max(onlyOnceCV)+1):   
        dictPer.append(0)
    
    ''' for every different cvCount value , build a query list of values between 0 to 1 for reading from the graph 
    dictPer => a list of percent values from graph for unique cvCount
    '''

    for eachCount in range(0,len(onlyOnceCV)):
        for x in range(0,onlyOnceCV[eachCount]):
            perCV = mm.eval('linstep(0,' + str(onlyOnceCV[eachCount]-1) + ',' + str(x) + ');')
            op1 = cmds.gradientControlNoAttr('defaultColorGraph',q = True, vap = perCV)
            perC.append(op1)
        dictPer[onlyOnceCV[eachCount]] = perC   
        perC = []

    
    for eachCrv in curveList:
        allPerCrv.append([])
    
    for tbr in toBeResizeCurveList:
        eachCrv = curveList.index(tbr)
        allPerCrv[eachCrv] = dictPer[cvCountL[eachCrv]]
        
    return allPerCrv
         
    
def autoResizeCOLOR():
    
    import cPickle as Pickle
    currNode = cmds.getAttr('gbNode.currentGBNode')
    texture = getScalpMeshTextureNode()
    if not texture:
        reportGBMessage('No Texture applied to Scalp Shader', True, True, 'red')
    texChanged = True
    if cmds.nodeType(texture) == 'file':
        texChanged = isTextureChanged(texture)
    
    
    rgbInfo = []        
    rgbInfoString = cmds.getAttr(currNode + '.rgbInfo')
    if rgbInfoString:
        rgbInfo = Pickle.loads(str(rgbInfoString))
    
    toBeResize = Pickle.loads(str(cmds.getAttr(currNode + '.toBeResize')))
    if texChanged or toBeResize:
        if cmds.nodeType(texture) == 'file':
            cmds.setAttr(texture + '.fileTextureName', cmds.getAttr(texture + '.fileTextureName'), type = 'string')
        if not rgbInfo:
            updateRGBInfo(texture, 'firstTime')
        else:
            updateRGBInfo(texture, 'checkAndUpdate')
    
    if rgbInfo:
        updateRGBGraphsTBR()
    else:
        updateRGBGraphs()
        
    toBeResize = Pickle.loads(str(cmds.getAttr(currNode + '.toBeResize')))

    if toBeResize:
#        print 'auto color exec'
        brainAutoResize(getPerlistCOLOR())
           
                        
            
def getPerlistCOLOR():
    
    import cPickle as Pickle
    currNode = cmds.getAttr('gbNode.currentGBNode')
    curveList = Pickle.loads(str(cmds.getAttr(currNode + '.curveList4Graph')))
    rgbGraphs = Pickle.loads(str(cmds.getAttr(currNode + '.rgbGraphs')))
    rgbPerList = Pickle.loads(str(cmds.getAttr(currNode + '.rgbPerList')))
    
    toBeResize = Pickle.loads(str(cmds.getAttr(currNode + '.toBeResize')))
    toBeResizeCurveList = convertIDToCurveList(toBeResize)
    
    cvCountL = Pickle.loads(str(cmds.getAttr(currNode + '.cvCountL')))
    
    allCper = []
    perC = []
    dictPer = []
    
    ''' Set will return only unique cvCount values '''
    onlyOnceCV = list(set(cvCountL)) 
    percentList = []
    allPerCrv = []

    ''' Build a dictionary which will query only once for different number of cvs '''
    
    # Create a list of dictionary 
    for x in range(0,max(onlyOnceCV)+1):   
        dictPer.append(0)
    
    ''' for every different cvCount value , build a query list of values between 0 to 1 for reading from the graph 
    dictPer => a list of percent values to query from graph for unique cvCount
    '''
    
    for eachCount in range(0,len(onlyOnceCV)):
        for x in range(0,onlyOnceCV[eachCount]):
            perCV = mm.eval('linstep(0,' + str(onlyOnceCV[eachCount]-1) + ',' + str(x) + ');')
            perC.append(perCV)
        dictPer[onlyOnceCV[eachCount]] = perC   
        perC = []


    graphLayouts = []
    for i in range(3):
        graph = 'rgbGraphControl' + str(i)
        graphLayouts.append(graph)
    graphLayouts.append('defaultColorGraph')
    
    graphPerList = []
    graphList = []
    perCV = []
    allGraphs = 0
    perCVList = rgbPerList
    
    
    
    for tbr in toBeResizeCurveList:
        eachCrv = curveList.index(tbr)
        ncv = cvCountL[eachCrv]
        
        for cv in range(ncv):
            perGraphList = rgbPerList[eachCrv]
            queryX = dictPer[ncv][cv]
            allGraphs = 0
            for graph in range(4):
                ogP = cmds.gradientControlNoAttr(graphLayouts[graph], q = True, vap = queryX)
                allGraphs = allGraphs + ( ogP * perGraphList[graph])
                
            perCV.append(allGraphs)
            allGraphs = 0
        
        perCVList[eachCrv] = perCV
        perCV = []
            
    
    return perCVList


    
    
def updateRGBGraphs():
    
    import cPickle as Pickle
    currNode = cmds.getAttr('gbNode.currentGBNode')
    rgbGraphs = Pickle.loads(str(cmds.getAttr(currNode + '.rgbGraphs')))
    
    graphName = 'rgbGraphControl'
    graphString = []
    for i in range(3):
        graphString.append(cmds.gradientControlNoAttr(graphName + str(i), q = True, asString = True))
    graphString.append(cmds.gradientControlNoAttr('defaultColorGraph', q = True, asString = True))
    
    graphStringS = Pickle.dumps(graphString)
    cmds.setAttr(currNode + '.rgbGraphs', graphStringS, type = 'string')                                                                           
    
        
    
def updateRGBGraphsTBR():
    
    import cPickle as Pickle
    currNode = cmds.getAttr('gbNode.currentGBNode')
    curveList = Pickle.loads(str(cmds.getAttr(currNode + '.curveList4Graph')))
    rgbGraphs = Pickle.loads(str(cmds.getAttr(currNode + '.rgbGraphs')))
    
    rgbCurves = Pickle.loads(str(cmds.getAttr(currNode + '.rgbCurves')))
    toBeResize = Pickle.loads(str(cmds.getAttr(currNode + '.toBeResize')))
        
    graphName = 'rgbGraphControl'
    graphString = []
    for i in range(3):
        currGraph = cmds.gradientControlNoAttr(graphName + str(i), q = True, asString = True)
        if not currGraph == rgbGraphs[i]:
            toBeResize.extend(rgbCurves[i])
            rgbGraphs[i] = currGraph           
    defaultGraph = cmds.gradientControlNoAttr('defaultColorGraph', q = True, asString = True)
    if not defaultGraph == rgbGraphs[3]:            
        toBeResize.extend(rgbCurves[3])
        rgbGraphs[3] = defaultGraph
        
    toBeResize = list(set(toBeResize))
    
    toBeResizeString = Pickle.dumps(toBeResize)
    rgbGraphsString = Pickle.dumps(rgbGraphs)
    
    
    
    
    cmds.setAttr(currNode + '.toBeResize', toBeResizeString, type = 'string') 
    cmds.setAttr(currNode + '.rgbGraphs', rgbGraphsString, type = 'string')       
    
    
def updateRGBInfo(texture, mode):
    
    import cPickle as Pickle
    currNode = cmds.getAttr('gbNode.currentGBNode')
    curveList = Pickle.loads(str(cmds.getAttr(currNode + '.curveList4Graph')))
    cvUV = Pickle.loads(str(cmds.getAttr(currNode + '.cvUV')))
    toBeResize = Pickle.loads(str(cmds.getAttr(currNode + '.toBeResize')))
    toBeResizeName = convertIDToCurveList(toBeResize)
    
    graphList = []
    for i in range(3):
        graphList.append('rgbGraphControl' + str(i))
    graphList.append('defaultColorGraph')
    
    rgbInfo = []
    rgbPerList = []
    rgbCurves = []
    rgbCurvesID = []
    rgbCurvesNames = []
    if mode == 'firstTime':
        for crv in cvUV:
            rgbInfo.append([])
            rgbPerList.append([])
        rgbCurves = []
        for i in range(4):
            rgbCurvesID.append([])            
            rgbCurvesNames.append([])
        toBeResize = convertCurveToIDList(curveList)
    else:
        rgbInfo = Pickle.loads(str(cmds.getAttr(currNode + '.rgbInfo')))            
        rgbPerList = Pickle.loads(str(cmds.getAttr(currNode + '.rgbPerList')))            
        rgbCurvesID = Pickle.loads(str(cmds.getAttr(currNode + '.rgbCurves')))
        rgbCurvesNames = []
        for i in range(4):
            rgbCurvesNames.append([])
            rgbCurvesNames[i] = convertIDToCurveList(rgbCurvesID[i])
            
        
    for crv in range(len(curveList)):
        colorChanged = False
        curveName = curveList[crv]    
        currRGB = cmds.colorAtPoint(texture, o = 'RGB', u = cvUV[crv][0], v = cvUV[crv][1])
        if not currRGB == rgbInfo[crv]:
            rgbInfo[crv] = currRGB
            if mode == 'checkAndUpdate':
                if curveName not in toBeResizeName:
                    toBeResizeName.append(curveName)
            colorChanged = True                  
              
        if colorChanged or rgbPerList[crv] == []:
                        
            rgbw = getRGBW(currRGB)
#            print rgbPerList[crv], rgbw
            rgbPerList[crv] = rgbw
            for i in range(4):
                if rgbw[i] <= 0.05:
                    if curveName in rgbCurvesNames[i]:
                        rgbCurvesNames[i].remove(curveName)
                else:
                    if not curveName in rgbCurvesNames[i]:
                        rgbCurvesNames[i].append(curveName)                         
                        
    
    for i in range(4):
        rgbCurvesID[i] = convertCurveToIDList(rgbCurvesNames[i])
            
    if mode == 'checkAndUpdate':
        toBeResize = convertCurveToIDList(toBeResizeName)                    
    
    toBeResizeString = Pickle.dumps(toBeResize)
    rgbInfoString = Pickle.dumps(rgbInfo)
    rgbCurvesIDString = Pickle.dumps(rgbCurvesID)
    rgbPerListString = Pickle.dumps(rgbPerList)
    
    cmds.setAttr(currNode + '.toBeResize', toBeResizeString, type = 'string') 
    cmds.setAttr(currNode + '.rgbInfo', rgbInfoString, type = 'string') 
    cmds.setAttr(currNode + '.rgbCurves', rgbCurvesIDString, type = 'string') 
    cmds.setAttr(currNode + '.rgbPerList', rgbPerListString, type = 'string') 
    
    
def getRGBW(currRGB):
    
#    graphLayouts = cmds.columnLayout('colorRampLayout', q = True, ca = True)
#    frameLayouts = graphLayouts
#    graphList = []
#    for i in range(3):
#        graphList.append('rgbGraphControl' + str(i))
    
#    texture = getScalpMeshTextureNode()
    rgb = currRGB
    r = rgb[0]
    g = rgb[1]
    b = rgb[2]
    t = 0
    t = r + g + b
    
    pr = [0,0,0,0]
    
    if t <= 1.15:
        for c in range(0,3):
            if rgb[c] < 0.1:
                pr[c] = 0
            else:
                pr[c] = rgb[c]
    elif t > 2.8:
        pr[0] = 0
        pr[1] = 0
        pr[2] = 0
        pr[3] = 1
    else:

        maxC = rgb.index(max(rgb))
        if max(rgb) > 0.9:
            if maxC == 0:
                oa = 1
                ob = 2
            elif maxC == 1:
                oa = 0
                ob = 2
            else:
                oa = 0
                ob = 1
            mix = (rgb[oa] + rgb[ob]) * .5
            pr[maxC] = rgb[maxC]*(1-mix)
            pr[3] = mix
            
        else:
            if r and g > 0.55:
                mix = 1 - b
                pr[0] = r * 0.5 * mix
                pr[1] = g * 0.5 * mix
                mixC = 2
                pr[2] = 0
            elif r and b > 0.55:
                mix = 1 - g
                pr[0] = r * 0.5 * mix
                pr[2] = b * 0.5 * mix
                mixC = 1
                pr[1] = 0
            else:
                mix = 1 - r
                pr[1] = g * 0.5 * mix
                pr[2] = b * 0.5 * mix
                pr[0] = 0
            pr[3] = mix
 
    return pr
        
    
def isTextureChanged(texture):
    
    import os.path
    import time
    import cPickle as Pickle
    currNode = cmds.getAttr('gbNode.currentGBNode')
    
    path = cmds.getAttr(texture + '.fileTextureName')
    modTime = time.ctime(os.path.getmtime(path))
    texPathTimeString = cmds.getAttr(currNode + '.texPathTime')
    texChanged = False
    if texPathTimeString:
        texPathTime = Pickle.loads(str(texPathTimeString))
        if not texPathTime == [path,modTime]:
            texChanged = True
    else:
        texPathTime = [path, modTime]
        texChanged = True
        
    texPathTimeString = Pickle.dumps([path, modTime])
    cmds.setAttr(currNode + '.texPathTime', texPathTimeString, type = 'string')            
    
    return texChanged
                    
        
    
    
def restoreVolumeResizePos():
    
    import cPickle as Pickle
    currNode = cmds.getAttr('gbNode.currentGBNode')
    curveList = Pickle.loads(str(cmds.getAttr(currNode + '.curveList4Graph')))
    cvCountL = Pickle.loads(str(cmds.getAttr(currNode + '.cvCountL'))) 
    toBeResizeCurveList = convertIDToCurveList(Pickle.loads(str(cmds.getAttr(currNode + '.toBeResize'))))
    volumeResizePos = Pickle.loads(str(cmds.getAttr(currNode + '.volumeResizePos')))
    resizeList = list(set(curveList) - set(toBeResizeCurveList))
    
    recallStripVtx('PRErestorevolresisze')
    
    
#    print 'restorevollll'
    stripDictDB = getStripValuesDict()
    if stripDictDB:
        
        onlyStpCrvs = stripDictDB.keys()
        resizeCrvs = list(set(resizeList) & set(onlyStpCrvs))
        
        extNodes = getStripExtrudeNodes(resizeCrvs)
        bothNodes = [extNodes, resizeCrvs]
        storeRestoreStripVtxPos(bothNodes, 'restore')
    
    for rsz in resizeList:
        crv = curveList.index(rsz)
        for cv in range(cvCountL[crv]):
            cmds.xform(curveList[crv] + '.cv[' + str(cv) + ']', ws = True, t = volumeResizePos[crv][cv])
    
    if stripDictDB:        
        storeRestoreStripVtxPos(bothNodes, 'store')
        stripCurvatureChangeUI(bothNodes)
        storeRestoreRootVtxForStripShove(bothNodes, 'store')
        stripShoveChange(bothNodes, 'dict')
        
    recallStripVtx('POSTrestorevolresisze')        


def getPerListOLD():
   
    import cPickle as Pickle
    currNode = cmds.getAttr('gbNode.currentGBNode')
    curveList = Pickle.loads(str(cmds.getAttr(currNode + '.curveList4Graph')))
    cvCountL = Pickle.loads(str(cmds.getAttr(currNode + '.cvCountL')))
    cmds.setAttr(currNode + '.defaultGraph', cmds.gradientControlNoAttr('defaultColorGraph', q = True, asString = True), type = 'string')
    
    allCper = []
    perC = []
    dictPer = []
    ''' Set will return only unique cvCount values '''
    onlyOnceCV = list(set(cvCountL)) 
    percentList = []
    allPerCrv = []

    ''' Build a dictionary which will query only once for different number of cvs '''
    
    # Create a list of dictionary 
    for x in range(0,max(onlyOnceCV)+1):   
        dictPer.append(0)
    
    ''' for every different cvCount value , build a query list of values between 0 to 1 for reading from the graph 
    dictPer => a list of percent values from graph for unique cvCount
    '''

    for eachCount in range(0,len(onlyOnceCV)):
        for x in range(0,onlyOnceCV[eachCount]):
            perCV = mm.eval('linstep(0,' + str(onlyOnceCV[eachCount]-1) + ',' + str(x) + ');')
            op1 = cmds.gradientControlNoAttr('defaultColorGraph',q = True, vap = perCV)
            perC.append(op1)
        dictPer[onlyOnceCV[eachCount]] = perC   
        perC = []
#    cmds.deleteUI('falloffCurve')

    
    for eachCrv in curveList:
        percentList.append(0)
    
    for eachCrv in range(0,len(curveList)):
        perCrv = dictPer[cvCountL[eachCrv]]
        allPerCrv.append(perCrv)
        
    return allPerCrv


def getPerListColor():
    
    
    import cPickle as Pickle
    currNode = cmds.getAttr('gbNode.currentGBNode')
    curveList = Pickle.loads(str(cmds.getAttr(currNode + '.curveList4Graph')))
    origCurveCVpos = Pickle.loads(str(cmds.getAttr(currNode + '.origCurveCVpos')))
    dVector = Pickle.loads(str(cmds.getAttr(currNode + '.dVector')))
    cvCountL = Pickle.loads(str(cmds.getAttr(currNode + '.cvCountL')))
    cvUV = Pickle.loads(str(cmds.getAttr(currNode + '.cvUV')))
    

    graphPerList = []
   
    allCper = []
    perC = []
    dictPer = []
    
    ''' Set will return only unique cvCount values '''
    onlyOnceCV = list(set(cvCountL)) 
    percentList = []
    allPerCrv = []

    ''' Build a dictionary which will query only once for different number of cvs '''
    
    # Create a list of dictionary 
    for x in range(0,max(onlyOnceCV)+1):   
        dictPer.append(0)
    
    ''' for every different cvCount value , build a query list of values between 0 to 1 for reading from the graph 
    dictPer => a list of percent values to query from graph for unique cvCount
    '''
    
    for eachCount in range(0,len(onlyOnceCV)):
        for x in range(0,onlyOnceCV[eachCount]):
            perCV = mm.eval('linstep(0,' + str(onlyOnceCV[eachCount]-1) + ',' + str(x) + ');')
            perC.append(perCV)
        dictPer[onlyOnceCV[eachCount]] = perC   
        perC = []

    graphLayouts = []
    wrgbGraphs = []
    wrgbGraphs.append(cmds.gradientControlNoAttr('defaultColorGraph', q = True, asString = True))
    for i in range(3):
        graph = 'rgbGraphControl' + str(i)
        graphLayouts.append(graph)
        wrgbGraphs.append(cmds.gradientControlNoAttr(graph, q = True, asString = True))
    
    wrgbGraphsString = Pickle.dumps(wrgbGraphs)
    cmds.setAttr(currNode + '.rgbGraphs', wrgbGraphsString, type = 'string')
    
    graphPerList = []
    graphList = []
    perCV = []
    allGraphs = 0
    perCVList = []
    
    for eachCurve in range(0,len(curveList)):
        noOfCVs = len(origCurveCVpos[eachCurve])
        if graphLayouts == None:
            graphPerList = [['defaultColorGraph'],[1]]
        else:
            graphPerList = checkColorRGB(cvUV[eachCurve][0],cvUV[eachCurve][1])
            
        for eachCV in range(0,noOfCVs):
            graphList = graphPerList[0]
            perGraphList = graphPerList[1]
            queryX = dictPer[noOfCVs][eachCV]
            for eachGraph in range(0,len(graphList)):
                graphName = graphList[eachGraph]
                ogP = cmds.gradientControlNoAttr(graphName, q = True, vap = queryX)
                allGraphs = allGraphs + ( ogP * perGraphList[eachGraph])
                
            perCV.append(allGraphs)
            allGraphs = 0
        perCVList.append(perCV)
        perCV = []
    
    return perCVList

def checkColorRGB(u,v):
    
#    graphLayouts = cmds.columnLayout('colorRampLayout', q = True, ca = True)
#    frameLayouts = graphLayouts
    graphList = []
    for i in range(3):
        graphList.append('rgbGraphControl' + str(i))
    
    texture = getScalpMeshTextureNode()
    rgb = cmds.colorAtPoint(texture, o = 'RGB', u = u, v = v)
    r = rgb[0]
    g = rgb[1]
    b = rgb[2]
    t = 0
    t = r + g + b
    
    pr = [0,0,0]
    
    if t <= 1.15:
        for c in range(0,3):
            if rgb[c] < 0.1:
                pr[c] = 0
            else:
                pr[c] = rgb[c]
    elif t > 2.8:
        pr[0] = 0
        pr[1] = 0
        pr[2] = 0
        pr.append(1)
        graphList.append('defaultColorGraph')
    else:
        graphList.append('defaultColorGraph')
        maxC = rgb.index(max(rgb))
        if max(rgb) > 0.9:
            if maxC == 0:
                oa = 1
                ob = 2
            elif maxC == 1:
                oa = 0
                ob = 2
            else:
                oa = 0
                ob = 1
            mix = (rgb[oa] + rgb[ob]) * .5
            pr[maxC] = rgb[maxC]*(1-mix)
            pr.append(mix)
            
        else:
            if r and g > 0.55:
                mix = 1 - b
                pr[0] = r * 0.5 * mix
                pr[1] = g * 0.5 * mix
                mixC = 2
                pr[2] = 0
            elif r and b > 0.55:
                mix = 1 - g
                pr[0] = r * 0.5 * mix
                pr[2] = b * 0.5 * mix
                mixC = 1
                pr[1] = 0
            else:
                mix = 1 - r
                pr[1] = g * 0.5 * mix
                pr[2] = b * 0.5 * mix
                pr[0] = 0
            pr.append(mix)
 
    return [graphList, pr]


def restoreOrigCV():
    
    import cPickle as Pickle
    currNode = cmds.getAttr('gbNode.currentGBNode')
    curveList = []
    cvCountL = []
    curveListString = cmds.getAttr(currNode + '.curveList4Graph')
    if curveListString:
        curveList = Pickle.loads(str(curveListString))
    if not curveList:
        return        
    
    cvCountL = Pickle.loads(str(cmds.getAttr(currNode + '.cvCountL')))
    origCurveCVpos = Pickle.loads(str(cmds.getAttr(currNode + '.origCurveCVpos')))
        

    for eachC in range(0,len(curveList)):
#        sp = cmds.getAttr(curveList[eachC] +'.spans')
#        dg = cmds.getAttr(curveList[eachC] +'.degree') 
#        ncv = sp + dg
        for cv in range(0,cvCountL[eachC]):
            cmds.xform ((curveList[eachC] + '.cv[' + str(cv) + ']'), ws = True, t = origCurveCVpos[eachC][cv])


def restoreOrigCVOnUpdated():
    
    import cPickle as Pickle
    currNode = cmds.getAttr('gbNode.currentGBNode')
    toBeUpdatedIpolString = cmds.getAttr(currNode + '.toBeUpdatedIpol')
    if toBeUpdatedIpolString:        
        toBeUpdatedIpol = convertIDToCurveList(Pickle.loads(str(toBeUpdatedIpolString)))
    curveList = []
    cvCountL = []
    curveListString = cmds.getAttr(currNode + '.curveList4Graph')
    if curveListString:
        curveList = Pickle.loads(str(curveListString))
    if not curveList:
        return        
    
    cvCountL = Pickle.loads(str(cmds.getAttr(currNode + '.cvCountL')))
    origCurveCVpos = Pickle.loads(str(cmds.getAttr(currNode + '.origCurveCVpos')))
        
    for crv in toBeUpdatedIpol:
        if not cmds.objExists(crv):
            continue
        eachC = curveList.index(crv)
        for cv in range(0,cvCountL[eachC]):
            cmds.xform ((curveList[eachC] + '.cv[' + str(cv) + ']'), ws = True, t = origCurveCVpos[eachC][cv])    

def showGraphInit():
    
    import cPickle as Pickle
    currNode = cmds.getAttr('gbNode.currentGBNode')
    cmds.setAttr(currNode + '.lastState', 'graphInit', type = 'string')
    
    cmds.tabLayout('mainTabs', edit = True, en = True, vis = True)

    cmds.columnLayout('adjVolLayout', edit = True, vis = False)
    cmds.columnLayout('graphInitLyt', edit = True, vis = True)
    cmds.columnLayout('volumeMeshLT', edit = True, vis = False)
    cmds.button('cancelAddNewCharacterBtn', edit = True, vis = False)

    
    useIpol = cmds.getAttr(currNode + '.useIpolForGraph')
    if useIpol:
        if checkIfIpolExists():
            ipolCurvesForVolume()        
        else:
            useIpol = False            
    
    
    useFreeform = cmds.getAttr(currNode + '.useManualForGraph')
    if useFreeform:
        if checkIfFFExists():
            checkManualAllTime()
        else:
            useFreeform = False
                        
    curveString = cmds.getAttr(currNode + '.curveList4Graph')
    curveList = []
    
    if curveString:
        curveList = Pickle.loads(str(curveString))
                
    if curveList:
        if not useIpol:
            cmds.button('useIpolCurves',edit = True, vis = True)
        else:            
            cmds.button('useIpolCurves',edit = True, vis = False)
        if not useFreeform:
            cmds.button('useFreeformCurvesBtn',edit = True, vis = True)
        else:
            cmds.button('useFreeformCurvesBtn',edit = True, vis = False)            
                        
#        cmds.button('useSelectedCurves', edit = True, vis = False)
        cmds.button('continueToGraphBtn', edit = True, vis = True)
#        cmds.button('selGraphCurvesBtn', edit = True, vis = True)
    else:
        if not useIpol:
            cmds.button('useIpolCurves',edit = True, vis = True)
        if not useFreeform:
            cmds.button('useFreeformCurvesBtn',edit = True, vis = True)            
#        cmds.button('useSelectedCurves', edit = True, vis = True)
        cmds.button('continueToGraphBtn', edit = True, vis = False)
#        cmds.button('selGraphCurvesBtn', edit = True, vis = False)
        
    
    
def continueForGraph():
    
#    print 'continue continue'
    stopGBUndo()
    currNode = cmds.getAttr('gbNode.currentGBNode')
    cmds.setAttr(currNode + '.lastState', 'graphPage', type = 'string')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    cmds.setAttr(scalpMesh + '_DISPLAY.visibility' , False)
    scalpMeshShape = cmds.listRelatives(scalpMesh, s = True)[0]
    scalpMeshDISPShape = cmds.listRelatives(scalpMesh + '_DISPLAY', s = True)[0]
    cmds.setAttr(scalpMeshShape + '.displaySmoothMesh', cmds.getAttr(scalpMeshDISPShape + '.displaySmoothMesh'))
    
#    cmds.getAttr('pSphere2_DISPLAYShape.displaySmoothMesh')
    cmds.setAttr(scalpMesh + '.visibility' , True)
    cmds.tabLayout('mainTabs', edit = True, en = True, vis = True)
    cmds.columnLayout('graphInitLyt', edit = True, vis = False)
    cmds.columnLayout('adjVolLayout', edit = True, vis = True)
    cmds.columnLayout('volumeMeshLT', edit = True, vis = False)
    cmds.button('cancelAddNewCharacterBtn', edit = True, vis = False)
    
    addIpolFromGraphUI()
    if cmds.getAttr(currNode + '.currentLocalControl') == 'region':
        regionBasedGraphSelected()
        recallStripVtx('conitnue for grpah REGION')
                    
    elif cmds.getAttr(currNode + '.currentLocalControl') == 'color':
        colorBasedGraphSelected()

    else:
        defaultGraphDisplayUI()
        recallStripVtx('conitnue for grpah')
        autoResize()
        
#    cmds.setAttr(currNode + '.isGraphRestored', False)
    setClumpMeshVisibility(True)
    setMeshStripsVisibilty(True)
    startGBUndo()
    
def defaultGraphDisplayUI():
    
    currNode = cmds.getAttr('gbNode.currentGBNode')
    
    cmds.frameLayout('colorGraphFrame', edit = True, vis = False)
    cmds.button('addColorGraphBtn', edit = True, vis = False)
    cmds.columnLayout('rgbGraphsColumn',edit = True, vis = False) 
    cmds.canvas('whiteCanvas', edit = True, vis = False)    
    cmds.frameLayout('regionBasedGraphFrame', edit = True, vis = False, cl = True)
    cmds.button('colorGraphControlBtn',edit = True, vis = False, en = True)
    cmds.button('regionGraphControlBtn',edit = True, vis = False, en = True)
    cmds.button('loadGraphFromControlBtn', edit = True, vis = False)
    cmds.button('updateGraphOnRegionBtn', edit = True, vis = False)
    cmds.gradientControlNoAttr('defaultColorGraph', edit = True, asString = cmds.getAttr(currNode + '.defaultGraph'))
    
    
def tabSelectChange():
    
    killAllGBJobs()
    if cmds.currentCtx() == 'dynWireCtx1':
        cmds.evalDeferred('cmds.setToolTo(\'selectSuperContext\')', lp = True)
    import cPickle as Pickle
    currNode = cmds.getAttr('gbNode.currentGBNode')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')

    curveString = cmds.getAttr(currNode + '.curveList4Graph')
    curveList = []
    
    if curveString:
        curveList = Pickle.loads(str(curveString))
    
    if curveList:
        curvesPresent = True
    else:
        curvesPresent = False
    
#    print 'curvesPresent', curvesPresent    
    
    lastState = cmds.getAttr(currNode + '.lastState')
    ind = cmds.tabLayout('mainTabs', query = True, sti = True)
#    print 'ind', ind
#    print lastState
    if ind == 1:
        interactiveRegionGraphUpdateOFF()
#        print 'on first tab'
        superCurvesVisibility(True)
        freeformCurvesNormalDisplayLayer()
        setVolMeshReference()
        switchToVolumeMeshForMapping()
        setClumpMeshVisibility(False)
        setMeshStripsVisibilty(False)
        cmds.select(cmds.getAttr(currNode + '.volumeMesh'), d = True)
        if cmds.objExists('regionControlGrp_' + scalpMesh):
            cmds.setAttr('regionControlGrp_' + scalpMesh + '.visibility', False)
        if 'graph' in lastState:
            if curvesPresent:
                if not cmds.getAttr(currNode + '.isGraphRestored'):
                    storeStripChangesToDB('restore')
                    restoreOrigCV()
                    storeStripChangesToDB('store')
                    cmds.setAttr(currNode + '.isGraphRestored', True)
                
            noUVGrid()
            cmds.setAttr(currNode + '.lastState', 'onChar', type = 'string')
            drawOnChar(False)
        cmds.setAttr(scalpMesh + '.visibility', False)
        if cmds.objExists(scalpMesh + '_DISPLAY'):
            cmds.setAttr(scalpMesh + '_DISPLAY.visibility', True)
        
    elif ind == 2:
#        print 'on second tab'
        superCurvesVisibility(False)
        switchToScalpMeshForMapping()
        freeformCurvesRenderDisplayLayer()
#        if cmds.getAttr(currNode + '.performIPS'):
#            createIpolPerSuper('auto')    
#        createIPSforClump()
        if lastState == 'graphPage':
            if curvesPresent:
#                print 'came here to continue'
#                createIPSforClump()
                recallStripVtx('tabselct grphpage')
                continueForGraph()
            else:
                showGraphInit()
            setVolMeshNormal()
        else:
            setVolMeshNormal()
            showGraphInit()
            checkSuperAndIpolAllTime()
            checkManualAllTime()
#            if cmds.getAttr(currNode + '.performIPS'):
#                createIpolPerSuper('auto')
#            createIPSforClump()
            pushUpdatedIpolCurves('progressCurveMapping')
            
            
            message = cmds.text('gbMessageStatusText', q = True, label = True)
            if message:
                reportGBMessage(message, False, False, 'yellow')
                cmds.text('gbMessageStatusColor',edit = True, vis = True, bgc = [0.0,1.0,0.0])				
        cmds.setAttr(scalpMesh + '.visibility', True)
        cmds.setAttr(scalpMesh + '_DISPLAY.visibility', False)            
                    
    '''
    else:
        if 'graph' not in cmds.getAttr(currNode + '.lastState'):
            cmds.tabLayout('mainTabs', edit = True, sti = 2)
            tabSelectChange()
        else:
            showBunchWave()
    '''           
            


def setVolMeshReference():
    
    currNode = cmds.getAttr('gbNode.currentGBNode')
    volMesh = cmds.getAttr(currNode + '.volumeMesh')
    
    cmds.setAttr(volMesh + '.overrideEnabled', 1)
    cmds.setAttr(volMesh + '.overrideDisplayType', 2)
           
def setVolMeshNormal():
    
    currNode = cmds.getAttr('gbNode.currentGBNode')
    volMesh = cmds.getAttr(currNode + '.volumeMesh')
    
    cmds.setAttr(volMesh + '.overrideEnabled', 1)
    cmds.setAttr(volMesh + '.overrideDisplayType', 0)

def updateTargetMesh():
    
    stopGBUndo()
    killAllGBJobs()
    
    if cmds.checkBox('regionGraphInteractiveBtn', q = True, value = True):
        interactiveRegionGraphUpdateOFF()
    import cPickle as Pickle 
    originalSelection = cmds.ls(sl = True)
    softSel = cmds.softSelect(q = True, sse= True)  
    ctx = cmds.currentCtx()
    currNode = cmds.getAttr('gbNode.currentGBNode')
    volumeMesh = cmds.getAttr(currNode + '.volumeMesh')
    createAlteredVerticesList('volumeMesh', volumeMesh)
    alteredList = Pickle.loads(str(cmds.getAttr(currNode + '.alteredVertices')))
    paintOnMesh = cmds.getAttr(currNode + '.paintOnMesh')
    tweakMesh = cmds.getAttr(currNode + '.tweakMesh')
    origSwitchBack = cmds.getAttr(currNode + '.switchBackSuperCurves')
    
    if paintOnMesh == volumeMesh:
    #                    print 'tweak scalp paint vol A'
        switchCurvesToOtherMesh()
        cmds.setAttr(currNode + '.paintOnMesh', scalpMesh, type = 'string')
    #                    print 'tweak scalp paint vol B'                    
        cmds.setAttr(currNode + '.switchBackSuperCurves', True)
    
    if alteredList:
        getGraphCurvesFromAlteredVertices()
#        toBeResize = Pickle.loads(str(cmds.getAttr(currNode + '.toBeResize'))) 
#        print 'update TBR 1' , toBeResize

        restoreOrigCVOnUpdated()
#        toBeResize = Pickle.loads(str(cmds.getAttr(currNode + '.toBeResize'))) 
#        print 'update TBR 2' , toBeResize

        morphMesh('volumeMesh', volumeMesh, False, False)
#        toBeResize = Pickle.loads(str(cmds.getAttr(currNode + '.toBeResize')))         
#        print 'update TBR 3' , toBeResize

        pushUpdatedIpolCurves('editMeshFrameProgress')
#        toBeResize = Pickle.loads(str(cmds.getAttr(currNode + '.toBeResize')))         
#        print 'update TBR 4' , toBeResize

                 
        updateNewShapeRegionCtrl(alteredList)
        
        autoResize()

    updateScalpVolSuperCurves(tweakMesh)
    if cmds.getAttr(currNode + '.switchBackSuperCurves'):
#        print 'cancelupdatemesh'
        switchCurvesToOtherMesh()
        if cmds.getAttr(currNode + '.paintOnMesh') == scalpMesh:
            cmds.setAttr(currNode + '.paintOnMesh', volumeMesh, type = 'string')
        else:
            cmds.setAttr(currNode + '.paintOnMesh', scalpMesh, type = 'string')
        cmds.setAttr(currNode + '.switchBackSuperCurves', False)
    
    cmds.setAttr(currNode + '.switchBackSuperCurves', origSwitchBack)
    if originalSelection:
        cmds.select(originalSelection, r = True)
    cmds.setToolTo(ctx)    
    cmds.softSelect(sse= softSel)            
    startGBUndo()
        
    
def enterTweakMesh(mode):
    
    stopGBUndo()
    currNode = cmds.getAttr('gbNode.currentGBNode')
    tweakMesh = cmds.getAttr(currNode + '.' + cmds.getAttr(currNode + '.tweakMesh'))
    cmds.setAttr(currNode + '.meshNotUpdated', True)
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    scalpMeshDISP = scalpMesh + '_DISPLAY'
    volMesh = cmds.getAttr(currNode + '.volumeMesh')
    cmds.setAttr(scalpMesh + '.visibility', True)
    cmds.setAttr(scalpMeshDISP + '.visibility', False)

    paintOnMesh = cmds.getAttr(currNode + '.paintOnMesh')
    
    goOn = True
    switchCurves = False
    if cmds.radioButtonGrp('selectUpdateMeshRadio', query = True, select = True) == 1:
        if gbType == 0:
            cmds.radioButtonGrp('selectUpdateMeshRadio', edit = True, select = 2)
            reportGBMessage('Edit Scalp Mesh Feature available only in Licensed Version', True, True, 'red')
        setVolMeshReference()
        if not mode == 'penetration':
            result = cmds.confirmDialog(title = 'Update Base Mesh', message = 'Any update to Scalp Mesh might take a bit longer time, do you want to proceed ?', button=['Yes','No'], defaultButton = 'Yes', cancelButton = 'No', dismissString = 'No')
            if result == 'Yes':
                goOn = True
                if not mode == 'penetration':
                    revertFromMeshShapes('scalpMesh', '')
                if paintOnMesh == volMesh:
#                    print 'tweak scalp paint vol A'
                    switchCurvesToOtherMesh()
                    cmds.setAttr(currNode + '.paintOnMesh', scalpMesh, type = 'string')
#                    print 'tweak scalp paint vol B'                    
                    cmds.setAttr(currNode + '.switchBackSuperCurves', True)
            else:
                goOn = False
                cancelUpdateBaseMesh()
        else:
            goOn = True        
    if goOn:
        if cmds.getAttr(currNode + '.tweakMesh') == 'volumeMesh':
            setVolMeshNormal()
            if not mode == 'penetration':
                revertFromMeshShapes('', 'volumeMesh')
            if paintOnMesh == volMesh:
#                print 'tweak vol paint scalp A'                    
                switchCurvesToOtherMesh()
                cmds.setAttr(currNode + '.paintOnMesh', scalpMesh, type = 'string')
#                print 'tweak vol paint scalp B'                    
                cmds.setAttr(currNode + '.switchBackSuperCurves', True)
                
            currSmoothLevel = isSelectedMeshValid(tweakMesh)
            cmds.setAttr(currNode + '.currSmoothLevel', currSmoothLevel)
            div = currSmoothLevel
            if div < 2:
                cmds.button('polySmoothVolMeshBtn', edit = True, label = 'Create a D' + str(div+1) + ' PolySmooth Mesh of Volume Mesh')
                cmds.button('polySmoothVolMeshBtn', edit = True, vis = True)
            else:
                cmds.button('polySmoothVolMeshBtn', edit = True, vis = False)
        else:
            cmds.button('polySmoothVolMeshBtn', edit = True, vis = False)
            
        cmds.tabLayout('mainTabs', edit = True, vis = False)
        cmds.button('updateBaseMeshBtn', edit = True, vis = True)
        cmds.button('tweakMeshBtn', edit = True, vis = False)
        cmds.radioButtonGrp('selectUpdateMeshRadio', edit = True, en = False)
        cmds.menu('selCharMenu', edit = True, en = False)
        cmds.frameLayout('editBaseMeshFrame', edit = True, cll = False)
        cmds.select(tweakMesh, r = True)
        cmds.frameLayout('commonFrame', edit = True, cl = False)
        cmds.frameLayout('htCurvesFrame', edit = True, cl = True)
        cmds.frameLayout('htMeshFrame', edit = True, cl = False)
    #    panelName = cmds.getPanel(withFocus = True)
        panelName = cmds.paneLayout('viewPanes', q=True, pane1=True)
        cmds.setAttr(tweakMesh + '.visibility', True)
#        cmds.isolateSelect(panelName, state = 1)
#        cmds.isolateSelect(panelName, ado = tweakMesh)
        startGBUndo()
    
def showDisplayScalpMesh():
    
    currNode = cmds.getAttr('gbNode.currentGBNode')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
#    volMesh = cmds.getAttr(currNode + '.volumeMesh')
    scalpMeshDISP = scalpMesh + '_DISPLAY'
#    volMeshDISP = volMesh + '_DISPLAY'
    cmds.setAttr(scalpMesh + '.visibility', False)
#    cmds.setAttr(volMesh + '.visibility', False)
    if cmds.objExists(scalpMeshDISP):
        cmds.setAttr(scalpMeshDISP + '.visibility', True)
#    cmds.setAttr(volMeshDISP + '.visibility', True)

def hideDisplayScalpVolMesh():    
    
    currNode = cmds.getAttr('gbNode.currentGBNode')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    volMesh = cmds.getAttr(currNode + '.volumeMesh')
    scalpMeshDISP = scalpMesh + '_DISPLAY'
    volMeshDISP = volMesh + '_DISPLAY'
    cmds.setAttr(scalpMesh + '.visibility', True)
    cmds.setAttr(volMesh + '.visibility', True)
    cmds.setAttr(scalpMeshDISP + '.visibility', False)
    cmds.setAttr(volMeshDISP + '.visibility', False)

def dropEditBaseMesh():
    
    stopGBUndo()
    killAllGBJobs()
    
    currNode = cmds.getAttr('gbNode.currentGBNode')
    revertFromMeshShapes('scalpMesh','volumeMesh')
    hideToolSettings()
    cmds.setAttr(cmds.getAttr('gbNode.currentGBNode') + '.meshNotUpdated', True)
    changeAgain = False
    if cmds.getAttr(cmds.getAttr('gbNode.currentGBNode') + '.superCurves3D'):
#        if cmds.getAttr(currNode + '.paintOnMesh') == cmds.getAttr(currNode + '.volumeMesh'):
#            switchCurvesToOtherMesh()
#            cmds.setAttr(currNode + '.paintOnMesh', cmds.getAttr(currNode + '.scalpMesh'), type = 'string')
#            changeAgain = True
        checkAddRemoveSuperCurves('editMesh')
#        if changeAgain:
#            switchCurvesToOtherMesh()
#            cmds.setAttr(currNode + '.paintOnMesh', cmds.getAttr(currNode + '.volumeMesh'), type = 'string')
    cmds.button('editBaseMeshBtn', edit = True, vis = False)
    cmds.frameLayout('editBaseMeshFrame', edit = True, cl = False, vis = True)
    cmds.button('updateBaseMeshBtn', edit = True, vis = False)
    cmds.button('tweakMeshBtn', edit = True, vis = True)
    cmds.radioButtonGrp('selectUpdateMeshRadio', edit = True, en = True)
    cmds.button('polySmoothVolMeshBtn',edit = True, vis = False)
    cmds.menu('selCharMenu', edit = True, en = True)
    shadedDisplayOnViewport(False)
    updateMeshSelected()
#    startGBUndo()
    
def editBaseMeshOnCollapse():
    
    stopGBUndo()
    cancelUpdateBaseMesh()
    hideToolSettings()
    startGBUndo()
    return
    
def cancelUpdateBaseMesh():

#    panelName = cmds.getPanel(withFocus = True)
#    cmds.isolateSelect(panelName, state = 0)
    
    stopGBUndo()
    cmds.button('editBaseMeshBtn', edit = True, vis = True)
    cmds.frameLayout('editBaseMeshFrame', edit = True, cl = True, vis = False)
    cmds.button('tweakMeshBtn', edit = True, vis = True)
    cmds.button('updateBaseMeshBtn', edit = True, vis = False)
    cmds.tabLayout('mainTabs', edit = True, vis = True)
    cmds.radioButtonGrp('selectUpdateMeshRadio', edit = True, en = True)
    cmds.menu('selCharMenu', edit = True, en = True)
    cmds.frameLayout('editBaseMeshFrame', edit = True, cll = True, cl = False)
    
    currNode = cmds.getAttr('gbNode.currentGBNode')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    volumeMesh = cmds.getAttr(currNode + '.volumeMesh')
    scalpDISP = scalpMesh + '_DISPLAY'
    cmds.setAttr(scalpMesh + '.visibility', False)
    cmds.setAttr(scalpDISP + '.visibility', True)
    if cmds.getAttr(currNode + '.meshNotUpdated'):
        revertFromMeshShapes('scalpMesh', 'volumeMesh')
        cmds.setAttr(currNode + '.meshNotUpdated', False)
    if cmds.getAttr(currNode + '.switchBackSuperCurves'):
#        print 'cancelupdatemesh'
        switchCurvesToOtherMesh()
        if cmds.getAttr(currNode + '.paintOnMesh') == scalpMesh:
            cmds.setAttr(currNode + '.paintOnMesh', volumeMesh, type = 'string')
        else:
            cmds.setAttr(currNode + '.paintOnMesh', scalpMesh, type = 'string')
        cmds.setAttr(currNode + '.switchBackSuperCurves', False)
        
    if not 'graph' in cmds.getAttr(currNode + '.lastState'):
        setVolMeshReference()
    reassignShaders()
    
    cmds.frameLayout('commonFrame', edit = True, cl = True)
    cmds.frameLayout('htCurvesFrame', edit = True, cl = True)
    cmds.frameLayout('htMeshFrame', edit = True, cl = True)
    startGBUndo()
    
    

def updateMeshSelected():
    
    stopGBUndo()
    currNode = cmds.getAttr('gbNode.currentGBNode')
    whichMesh = cmds.getAttr(currNode + '.whichMesh')
    baseMesh = cmds.getAttr(currNode + '.' + whichMesh)

    if whichMesh == 'scalpMesh':
        targetMesh = cmds.getAttr(currNode + '.volumeMesh')
    else:
        targetMesh = cmds.getAttr(currNode + '.scalpMesh')
        
    radioSel = cmds.radioButtonGrp('selectUpdateMeshRadio', query = True, select = True)
    if radioSel == 1:
        if gbType == 0:
            cmds.radioButtonGrp('selectUpdateMeshRadio', edit = True, select = 2)
            cmds.select(cl = True)
            reportGBMessage('Edit Scalp Mesh Feature available only in Licensed Version', True, True, 'red')
        
        cmds.button('updateBaseMeshBtn', edit = True, label = 'Update Base Mesh')
        if whichMesh == 'scalpMesh':
            tweakMesh = 'scalpMesh'
        else:
            tweakMesh = 'volumeMesh'
    else:
        cmds.button('updateBaseMeshBtn', edit = True, label = 'Update Target Mesh')
        if whichMesh == 'scalpMesh':
            tweakMesh = 'volumeMesh'
        else:
            tweakMesh = 'scalpMesh'

#    if tweakMesh == 'volumeMesh':
#        div = cmds.getAttr(currNode + '.currSmoothLevel')
#        if div < 2:
#            cmds.button('polySmoothVolMeshBtn', edit = True, label = 'Create a D' + str(div+1) + ' PolySmooth Mesh of Volume Mesh')
#            cmds.button('polySmoothVolMeshBtn', edit = True, vis = True)
#        else:
#            cmds.button('polySmoothVolMeshBtn', edit = True, vis = False)
#    else:
#        cmds.button('polySmoothVolMeshBtn', edit = True, vis = False)
                
         
    cmds.setAttr(currNode + '.tweakMesh', tweakMesh, type = 'string')
    tweakMeshName = cmds.getAttr(currNode + '.' + tweakMesh)
    if tweakMesh == 'scalpMesh':
        cmds.setAttr(tweakMeshName + '_DISPLAY.visibility', False)
    cmds.select(tweakMeshName, r = True)
    cmds.setAttr(tweakMeshName + '.visibility', True)
#    panelName = cmds.getPanel(withFocus = True)
#    activePanel = cmds.paneLayout('viewPanes', q=True, pane1=True)
#    cmds.isolateSelect( panelName, state=0 )
#    startGBUndo()

def storeMeshShapes():
    
    import cPickle as Pickle
    currNode = cmds.getAttr('gbNode.currentGBNode')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    volumeMesh = cmds.getAttr(currNode + '.volumeMesh')
    
    totalVScalp = cmds.polyEvaluate(scalpMesh, v = True)
    totalVVol = cmds.polyEvaluate(volumeMesh, v = True)
    scalpMeshShape = [cmds.xform(scalpMesh + '.vtx[' + str(i) + ']', q = True, ws = True, t = True) for i in range(totalVScalp)]
    volumeMeshShape = [cmds.xform(volumeMesh + '.vtx[' + str(i) + ']', q = True, ws = True, t = True) for i in range(totalVVol)]
    
    scalpMeshShapeString = Pickle.dumps(scalpMeshShape)
    volumeMeshShapeString = Pickle.dumps(volumeMeshShape)
    cmds.setAttr(currNode + '.scalpMeshShape', scalpMeshShapeString, type = 'string')
    cmds.setAttr(currNode + '.volumeMeshShape', volumeMeshShapeString, type = 'string')

def revertFromMeshShapes(ip1,ip2):
    
    import cPickle as Pickle
    currNode = cmds.getAttr('gbNode.currentGBNode')
        
    if ip1 == 'scalpMesh':
        dispChange = False
        scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
        cmds.makeIdentity(scalpMesh, apply = True)
        scalpMeshShape = Pickle.loads(str(cmds.getAttr(currNode + '.scalpMeshShape')))
        existCount = cmds.polyEvaluate(scalpMesh, v = True)
        if not existCount == len(scalpMeshShape):
            reportGBMessage('Scalp Mesh Topology Changed, Please fix.', True, True, 'red')
#            raise RuntimeError, 'Scalp Mesh Topology Changed, Please fix.'
        else:
            for v in range(len(scalpMeshShape)):
                if not cmds.xform(scalpMesh + '.vtx[' + str(v) + ']', q = True, ws = True, t = True) == scalpMeshShape[v]:
                    dispChange = True
                    cmds.xform(scalpMesh + '.vtx[' + str(v) + ']', ws = True, t = scalpMeshShape[v])

            createFreshDISPMesh()
            resizeDISPMesh(scalpMesh + '_DISPLAY')
#        if dispChange:
#            print 'dispChanged'
#            resizeDISPMesh(scalpMesh + '_DISPLAY')
    
    if ip2 == 'volumeMesh':
        volumeMesh = cmds.getAttr(currNode + '.volumeMesh')  
        cmds.makeIdentity(volumeMesh, apply = True)
        volumeMeshShape = Pickle.loads(str(cmds.getAttr(currNode + '.volumeMeshShape')))
        existCount = cmds.polyEvaluate(volumeMesh, v = True)
        smoothNode = ''
        if not existCount == len(volumeMeshShape):
            currSmoothLevel = cmds.getAttr(currNode + '.currSmoothLevel')
            recreateVolumeMesh(scalpMesh,volumeMesh)
            if currSmoothLevel > 0:
                smoothNode = cmds.polySmooth(volumeMesh, divisions = currSmoothLevel)[0]
        
        for v in range(len(volumeMeshShape)):
            if not cmds.xform(volumeMesh + '.vtx[' + str(v) + ']', q = True, ws = True, t = True) == volumeMeshShape[v]:
                cmds.xform(volumeMesh + '.vtx[' + str(v) + ']', ws = True, t = volumeMeshShape[v])
        
        if smoothNode:
            cmds.delete(smoothNode)
            cmds.delete(volumeMesh, ch = True)    
                
    
def recreateVolumeMesh(scalpMesh,volumeMesh):
    
    cmds.delete(volumeMesh)
    cmds.duplicate(scalpMesh, name = volumeMesh, rr = True, rc = True)
    cmds.setAttr(volumeMesh + '.visibility', True)
        
def polySmoothVolUpdate():
    
#    cmds.undoInfo(swf = False)
    stopGBUndo()
    import cPickle as Pickle
    currNode = cmds.getAttr('gbNode.currentGBNode')
    cmds.button('polySmoothVolMeshBtn', edit = True, vis = False)
    volumeMesh = cmds.getAttr(currNode + '.volumeMesh')
    cmds.makeIdentity(volumeMesh, apply = True)
    currSmoothLevel =  cmds.getAttr(currNode + '.currSmoothLevel')
    if currSmoothLevel < 2:
        cmds.polySmooth(volumeMesh, dv = 1)
        cmds.delete(volumeMesh, ch = True)
    cmds.select(volumeMesh, r = True)
    startGBUndo()
#    cmds.undoInfo(swf = True)
    
 
def execUpdateMesh():
    
    stopGBUndo()    
#    cmds.undoInfo(swf = False)
    import cPickle as Pickle
    selList = cmds.ls(sl = True)
    if selList:
        selObj = selList[0]
    
    currNode = cmds.getAttr('gbNode.currentGBNode')
    tweakMesh = cmds.getAttr(currNode + '.tweakMesh')

#    if tweakMesh == 'scalpMesh':
#        cmds.radioButtonGrp('selectUpdateMeshRadio', edit = True, select = 2)
#        reportGBMessage('Edit Scalp Mesh Feature available only in Licensed Version', True, True, 'red')
        
    mainGroup = cmds.getAttr(currNode + '.mainGroup')
    tweakMeshName = cmds.getAttr(currNode + '.' + tweakMesh)
    cmds.makeIdentity(tweakMeshName, apply = True)
    
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    volumeMesh = cmds.getAttr(currNode + '.volumeMesh')   
    
    lastState = cmds.getAttr(currNode + '.lastState')    
    graph = False
    if 'graph' in lastState:
        graph = True
#        print 'in graph'
        
    totalV = cmds.polyEvaluate(tweakMeshName, v = True)
    meshShapeString = cmds.getAttr(currNode + '.' + tweakMesh + 'Shape')
    meshShape = Pickle.loads(str(meshShapeString))
    
    morphing = False
    match = False
    checkForSmoothMesh = False
    topoChanged = False
    if selList:
        if not selObj == cmds.getAttr(currNode + '.scalpMesh') and not selObj == cmds.getAttr(currNode + '.volumeMesh'):
            cmds.delete(selObj, ch = True)                
            cmds.makeIdentity(selObj, apply = True) 
            selObjShp = cmds.listRelatives(selObj, s = True)
            if selObjShp:
                if cmds.objectType(selObjShp[0], isType = 'mesh'):
                    result = cmds.confirmDialog(title = 'Morph Existing Mesh', message = ' Morph to take the Shape of Selected Mesh?', button = ['Yes', 'No'], defaultButton = 'Yes', cancelButton = 'No', dismissString = 'No')
                    if result == 'Yes':
                        if not cmds.polyEvaluate(selObj, v = True, f = True) == cmds.polyEvaluate(tweakMeshName, v = True, f = True):
                            if tweakMesh == 'volumeMesh':
                                givenSmoothLevel = isSelectedMeshValid(selObj)
                                if givenSmoothLevel == -1:
                                    cmds.undoInfo(swf = True)
                                    reportGBMessage('Mesh Topology Mismatch, Should be same of scalp or smooth scalp upto divisions = 2', True, True, 'red')
#                                    raise RuntimeError, 'Mesh Topology Mismatch, Should be same of scalp or smooth scalp upto divisions = 2'
                                else:
                                    currSmoothLevel = givenSmoothLevel
                                    topoChanged = True
#                                    cmds.setAttr(currNode + '.currSmoothLevel', currSmoothLevel)
                                    smoothNode = cmds.polySmooth(scalpMesh, divisions = currSmoothLevel)
                                    cmds.polyTransfer( selObj, uv=1, ao = scalpMesh)
#                                    print 'succesTransfer A'
                                    cmds.delete(smoothNode)
                                    cmds.delete(scalpMesh, ch = True)
                                    cmds.delete(selObj, ch = True)
                                    morphing = True
                            else:
                                cmds.undoInfo(swf = True)
                                reportGBMessage('Mesh Topology Mismatch', True, True, 'red')
#                                raise RuntimeError, 'Mesh Topology Mismatch'
                        else:
                            cmds.polyTransfer(selObj, uv=1, ao=tweakMeshName, ch = False )
                            cmds.delete(selObj, ch = True)
                            morphing = True
                    else:
                        morphing = False
        else:
            checkForSmoothMesh = True
    
    if not selList or checkForSmoothMesh:
        givenSmoothLevel = isSelectedMeshValid(tweakMeshName)
        if givenSmoothLevel == -1:
            if tweakMesh == 'scalpMesh':
                cmds.undoInfo(swf = True)
                reportGBMessage('Scalp Mesh Topology is changed', True, True, 'red')
#                raise RuntimeError, 'Scalp Mesh Topology is changed'
            else:
                cmds.undoInfo(swf = True)
                reportGBMessage('Volume Mesh Topology should match of scalp or smooth scalp upto divisions = 2', True, True, 'red')
#                raise RuntimeError, 'Volume Mesh Topology should match of scalp or smooth scalp upto divisions = 2'
        else:
            if givenSmoothLevel > 0:
                currSmoothLevel = givenSmoothLevel
                topoChanged = True
#                cmds.setAttr(currNode + '.currSmoothLevel', currSmoothLevel)
                smoothNode = cmds.polySmooth(scalpMesh, divisions = currSmoothLevel)
                cmds.polyTransfer( volumeMesh, uv=1, ao = scalpMesh)
#                print 'successTransfer B'
                cmds.delete(volumeMesh, ch = True)
                cmds.delete(smoothNode)
                cmds.delete(scalpMesh, ch = True)
                
    
    
    alteredList = []    
    if tweakMesh == 'scalpMesh' and not morphing:
#        print 'self scalp'
        createAlteredVerticesList(tweakMesh,tweakMeshName)
        checkPenetrations(scalpMesh,volumeMesh)
        
        penetrationList = Pickle.loads(str(cmds.getAttr(currNode + '.penetratedVertices')))
        proceed = True
        if penetrationList:
            displayPenetratedFaces(penetrationList)
            result = cmds.confirmDialog(title = 'Penetration Found', message = ' Curve projections might not work properly on shaded areas. Do you wish to continue', button = ['Yes. Let it be', 'No. Tweak First'], defaultButton = 'No. Tweak First', cancelButton = 'No. Tweak First', dismissString = 'No. Tweak First')
            if result == 'Yes. Let it be':
                proceed = True
            else:
                proceed = False
                enterTweakMesh('penetration')
                cmds.undoInfo(swf = True)
                return
        if proceed:
            reassignShaders()
            alteredList = Pickle.loads(str(cmds.getAttr(currNode + '.alteredVertices')))
            if alteredList:
                recreatedMesh = recreateOriginalBase(tweakMesh)
#                restoreOrigCV()            
                mapCurvesB2B(recreatedMesh, tweakMeshName)
#                printTOBE()
                cmds.delete(recreatedMesh)
                morphMesh(tweakMesh, tweakMeshName, False,topoChanged)
#                printTOBE()
                if graph:
                    pushUpdatedIpolCurves('editMeshFrameProgress')
                    if lastState == 'graphPage':
                        autoResize()
                updateNewShapeRegionCtrl(alteredList)
#                printTOBE()
    
    elif tweakMesh == 'volumeMesh' and not morphing:
#        print 'self volume'
#        freezeTransformMesh(tweakMeshName)
        createAlteredVerticesList(tweakMesh,tweakMeshName)
#        print '1: createaltered'
        checkPenetrations(scalpMesh,volumeMesh)
       
        penetrationList = Pickle.loads(str(cmds.getAttr(currNode + '.penetratedVertices')))
        proceed = True
        if penetrationList:
            displayPenetratedFaces(penetrationList)
            result = cmds.confirmDialog(title = 'Penetration Found', message = ' Curve projections might not work properly on shaded areas. Do you wish to continue', button = ['Yes. Let it be', 'No. Tweak First'], defaultButton = 'No. Tweak First', cancelButton = 'No. Tweak First', dismissString = 'No. Tweak First')
            if result == 'Yes. Let it be':
                proceed = True
            else:
                proceed = False
                enterTweakMesh('penetration')
#                cmds.undoInfo(swf = True)            
                return
        if proceed:
            reassignShaders()
            alteredList = Pickle.loads(str(cmds.getAttr(currNode + '.alteredVertices')))
            
            if alteredList:
                getGraphCurvesFromAlteredVertices()
                storeStripChangesToDB('restore')
                restoreOrigCVOnUpdated()
                storeStripChangesToDB('store')
                morphMesh(tweakMesh, tweakMeshName, False, topoChanged)
#                print tweakMesh, tweakMeshName, topoChanged

                if graph:
                    pushUpdatedIpolCurves('editMeshFrameProgress')

                    if lastState == 'graphPage':
                        autoResize()

                updateNewShapeRegionCtrl(alteredList)
                
                
    elif tweakMesh == 'scalpMesh' and morphing:
#        print 'morph scalp'
        if cmds.listRelatives(selObj, p = True):
            if not cmds.listRelatives(selObj, p = True)[0] == mainGroup:
                cmds.parent(selObj, mainGroup)
        else:
            cmds.parent(selObj, mainGroup)
        createAlteredVerticesList(tweakMesh,selObj)
        checkPenetrations(selObj,volumeMesh)

        penetrationList = Pickle.loads(str(cmds.getAttr(currNode + '.penetratedVertices')))
        proceed = True
        if penetrationList:
            displayPenetratedFaces(penetrationList)
            result = cmds.confirmDialog(title = 'Penetration Found between Scalp and Volume Mesh', message = ' Curve projections might not work properly on shaded areas. Do you wish to continue', button = ['Yes. Let it be', 'No. Tweak First'], defaultButton = 'No. Tweak First', cancelButton = 'No. Tweak First', dismissString = 'No. Tweak First')
            if result == 'Yes. Let it be':
                proceed = True
            else:
                proceed = False
                enterTweakMesh('penetration')
                cmds.undoInfo(swf = True)
                return
        
        if proceed:
            reassignShaders()
            alteredList = Pickle.loads(str(cmds.getAttr(currNode + '.alteredVertices')))
            if alteredList:
#                restoreOrigCV()
                mapCurvesB2B(tweakMeshName, selObj)
                morphMesh(tweakMesh, selObj, True, topoChanged)
                if graph:
                    pushUpdatedIpolCurves('editMeshFrameProgress')
                    if lastState == 'graphPage':
                        autoResize()
                updateNewShapeRegionCtrl(alteredList)
                cmds.setAttr(selObj + '.visibility', False)
                
                            
    
    elif tweakMesh == 'volumeMesh' and morphing:
#        print 'morph volume'
        if cmds.listRelatives(selObj, p = True):
            if not cmds.listRelatives(selObj, p = True)[0] == mainGroup:
                cmds.parent(selObj, mainGroup)
        else:
            cmds.parent(selObj, mainGroup)

        createAlteredVerticesList(tweakMesh,selObj)
        checkPenetrations(scalpMesh, selObj)
        
        
        penetrationList = Pickle.loads(str(cmds.getAttr(currNode + '.penetratedVertices')))
        proceed = True
        if penetrationList:
            displayPenetratedFaces(penetrationList)
            result = cmds.confirmDialog(title = 'Penetration Found between Scalp and Volume Mesh', message = ' Curve projections might not work properly on shaded areas. Do you wish to continue', button = ['Yes. Let it be', 'No. Tweak First'], defaultButton = 'No. Tweak First', cancelButton = 'No. Tweak First', dismissString = 'No. Tweak First')
            if result == 'Yes. Let it be':
                proceed = True
            else:
                proceed = False
                enterTweakMesh('penetration')
                cmds.undoInfo(swf = True)
                return
        if proceed:
            reassignShaders()
            alteredList = Pickle.loads(str(cmds.getAttr(currNode + '.alteredVertices')))

            if alteredList:
#                restoreOrigCV()      
                morphMesh(tweakMesh, selObj, True, topoChanged)  
                getGraphCurvesFromAlteredVertices()
                restoreOrigCVOnUpdated()
                             
                if graph:
                    pushUpdatedIpolCurves('editMeshFrameProgress')
                    if lastState == 'graphPage':
                        autoResize()
                updateNewShapeRegionCtrl(alteredList)
                cmds.setAttr(selObj + '.visibility', False)
                
    if tweakMesh == 'scalpMesh':
        createFreshDISPMesh()
        resizeDISPMesh(scalpMesh + '_DISPLAY') 
        createStripScalpShoveMeshMain()
     
    cmds.button('tweakMeshBtn', edit = True, vis = True)
    cmds.button('updateBaseMeshBtn', edit = True, vis = False)
    cmds.radioButtonGrp('selectUpdateMeshRadio',edit = True, en = True)
    cmds.menu('selCharMenu', edit = True, en = True)
    cmds.text('editMeshOperation', edit = True, vis = False)
    cmds.progressBar('editMeshFrameProgress', edit = True, vis = False)
    cmds.progressBar('gbProgressBar', edit = True, vis = False)
    cmds.text('gbProgressBarText', edit = True, vis = False)
    cmds.frameLayout('editBaseMeshFrame', edit = True, cll = True)

    
#    print 'switchback' , cmds.getAttr(currNode + '.switchBackSuperCurves')
    updateScalpVolSuperCurves(tweakMesh)
    if cmds.getAttr(currNode + '.switchBackSuperCurves'):
#        print 'updateMeeshSwitch'
        switchCurvesToOtherMesh()
        if cmds.getAttr(currNode + '.paintOnMesh') == scalpMesh:
            cmds.setAttr(currNode + '.paintOnMesh', volumeMesh, type = 'string')
        else:
            cmds.setAttr(currNode + '.paintOnMesh', scalpMesh, type = 'string')
        cmds.setAttr(currNode + '.switchBackSuperCurves', False)
    
    if topoChanged:
        cmds.setAttr(currNode + '.currSmoothLevel', currSmoothLevel)
    cmds.setAttr(currNode + '.meshNotUpdated', False)
    
#    updateScalpVolSuperCurves(tweakMesh)
    cancelUpdateBaseMesh()
#    editBaseMeshOnCollapse()
#    cmds.undoInfo(swf = True)
    if cmds.tabLayout('mainTabs', query = True, sti = True) == 2:
        toBeUpdatedIpol = []
        toBeUpdatedIpolString = Pickle.dumps(toBeUpdatedIpol)
        cmds.setAttr(currNode + '.toBeUpdatedIpol', toBeUpdatedIpolString, type = 'string')
#    startGBUndo()

def freezeTransformMesh(mesh):
    
    cmds.makeIdentity(mesh, apply = True)
        
def displayPenetratedFaces(penetrationList):
    
    currNode = cmds.getAttr('gbNode.currentGBNode') 
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    
    reassignShaders()
    
    tweakMeshName = cmds.getAttr(currNode + '.' + cmds.getAttr(currNode + '.tweakMesh'))
    if tweakMeshName == scalpMesh:
        tweakMeshName = scalpMesh + '_DISPLAY'
    vtxNameList = [tweakMeshName + '.vtx[' + str(v) + ']' for v in penetrationList]
    faces = cmds.ls(cmds.polyListComponentConversion(vtxNameList, fv = True, tf = True), fl = True)
#    cmds.select(faces, r = True)
    cmds.select(cl = True)
    if not cmds.objExists('penetrationShader'):
        shader = cmds.shadingNode('lambert', name = 'penetrationShader', asShader = True)    
        cmds.setAttr(shader + '.color', 1, 0, 0, type = 'double3')
        cmds.setAttr(shader + '.transparency', .3, 0.3, 0.3, type = 'double3')
        cmds.select(cl = True)       
        shaderSG = cmds.sets(name = 'penetrationShaderSG', renderable = True, noSurfaceShader = True)
        cmds.connectAttr(shader + '.outColor', shaderSG + '.surfaceShader', f = True)

    cmds.sets(faces, forceElement = 'penetrationShaderSG')    
    cmds.select(cl = True)
    

def reassignShaders():
    
    currNode = cmds.getAttr('gbNode.currentGBNode')
    displayName = cmds.getAttr(currNode + '.displayName')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    scalpMeshDISP = scalpMesh + '_DISPLAY'
    volumeMesh = cmds.getAttr(currNode + '.volumeMesh')
    
    shaderNames = getShaderNames()
    
    scalpShader = shaderNames[0]
    scalpShaderSG = shaderNames[1]
    
    volumeShader = shaderNames[2]
    volumeShaderSG = shaderNames[3]
    
    scalpDISPShader = shaderNames[4]
    scalpDISPShaderSG = shaderNames[5]
    
    if not cmds.objExists(scalpShader):
        cmds.shadingNode('lambert', name = scalpShader, asShader = True)
        cmds.select(cl = True)
    if not cmds.objExists(scalpShaderSG):
        cmds.sets(name = scalpShaderSG, renderable = True,  noSurfaceShader = True)
        cmds.connectAttr(scalpShader + '.outColor', scalpShaderSG + '.surfaceShader', f = True)
    cmds.sets(scalpMesh, forceElement = scalpShaderSG)
#    cmds.sets(scalpMeshDISP, forceElement = scalpShaderSG) 
    
    if not cmds.objExists(volumeShader):
        cmds.shadingNode('lambert', name = volumeShader, asShader = True)
        cmds.setAttr(volumeShader + '.transparency', 0.75, 0.75, 0.75, type = 'double3')
        cmds.select(cl = True)
    if not cmds.objExists(volumeShaderSG):
        cmds.sets(name = volumeShaderSG, renderable = True,  noSurfaceShader = True)
        cmds.connectAttr(volumeShader + '.outColor', volumeShaderSG + '.surfaceShader', f = True)
    cmds.sets(volumeMesh, forceElement = volumeShaderSG)
    
    
    if not cmds.objExists(scalpDISPShader):
        cmds.shadingNode('lambert', name = scalpDISPShader, asShader = True)
        cmds.select(cl = True)
    if not cmds.objExists(scalpDISPShaderSG):
        cmds.sets(name = scalpDISPShaderSG, renderable = True,  noSurfaceShader = True)
        cmds.connectAttr(scalpDISPShader + '.outColor', scalpDISPShaderSG + '.surfaceShader', f = True)
    if cmds.objExists(scalpMeshDISP):
        cmds.sets(scalpMeshDISP, forceElement = scalpDISPShaderSG)
    
    

def updateScalpVolSuperCurves(tweakMesh):
    
    import cPickle as Pickle
    currNode = cmds.getAttr('gbNode.currentGBNode') 
    baseMeshGroup = cmds.getAttr(currNode + '.baseMeshGroup')
    baseMeshGroupChildren = cmds.listRelatives(baseMeshGroup, c = True)
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    superGrp = 'superCurves_charInterpolation_' + scalpMesh
    if not baseMeshGroupChildren:
        return
    if not superGrp in baseMeshGroupChildren:
        return
    else:
        if not cmds.listRelatives(superGrp, c = True):
            return
    
    superCurves3DString = cmds.getAttr(currNode + '.superCurves3D')
    superCurves3D = []
    if superCurves3DString:
        superCurves3D = Pickle.loads(str(superCurves3DString))
        superCurvesPos = Pickle.loads(str(cmds.getAttr(currNode + '.superCurvesPos')))
    scalpSuperCurvesString = cmds.getAttr(currNode + '.scalpSuperCurves')
    if scalpSuperCurvesString:
        scalpSuperCurves = Pickle.loads(str(scalpSuperCurvesString))
    if not scalpSuperCurvesString or not scalpSuperCurves:
        return
    
    scalpSuperCurvesPos = Pickle.loads(str(cmds.getAttr(currNode + '.scalpSuperCurvesPos')))
    if tweakMesh == 'scalpMesh':

        for s in range(len(scalpSuperCurves)):
            sup = scalpSuperCurves[s]
            if sup in superCurves3D:
                scalpSuperCurvesPos[s] = superCurvesPos[superCurves3D.index(sup)]
            else:
                ncv = cmds.getAttr(sup + '.spans') + cmds.getAttr(sup + '.degree')
                scalpSuperCurvesPos[s] = [cmds.xform(sup + '.cv[' + str(cv) + ']', q = True, ws = True, t = True) for cv in range(ncv)]
    else:
        volumeSuperCurves = Pickle.loads(str(cmds.getAttr(currNode + '.volumeSuperCurves')))
        volumeSuperCurvesPos = Pickle.loads(str(cmds.getAttr(currNode + '.volumeSuperCurvesPos')))
#        paintOnMesh = cmds.getAttr(currNode + '.paintOnMesh')
#        if paintOnMesh == scalpMesh:
#            xf = False
#        else:
#            xf = True
        
        historyDelete = []
        currMeshCPNode = createCPNode(cmds.getAttr(currNode + '.scalpMesh'))
        historyDelete.append(currMeshCPNode)
        nextMeshFoll = createFollicle('volumeMesh')
        nextMeshFollShp = cmds.listRelatives(nextMeshFoll, s = True)[0]
        historyDelete.append(nextMeshFoll)
            
        for s in range(len(volumeSuperCurves)):
            sup = volumeSuperCurves[s]
            scalpPos = scalpSuperCurvesPos[scalpSuperCurves.index(sup)]
            
            ncv = len(scalpPos)
            
            actualPos = []
            projPos = []
            cvDeleted = False
            cv = 0        
            
            zeroDistFound = False
            zeroPos = [0.0,0.0,0.0]
            
            
            while cv < ncv:
                actualPosCV = scalpPos[cv]
                cmds.setAttr(currMeshCPNode + '.ip', actualPosCV[0], actualPosCV[1], actualPosCV[2])
                cU = cmds.getAttr(currMeshCPNode + '.u')
                cV = cmds.getAttr(currMeshCPNode + '.v')
                cmds.setAttr(nextMeshFollShp + '.parameterU', cU)
                cmds.setAttr(nextMeshFollShp + '.parameterV', cV)
                projPosCV = cmds.xform(nextMeshFoll, q = True, ws = True, t = True)
                
                
                if not zeroDistFound:
                    if -0.25 <= projPosCV[0] <= 0.25 and -0.25 <= projPosCV[1] <= 0.25 and -0.25 <= projPosCV[2] <= 0.25:
                        zeroDistFound =  True
                        zeroPos = projPosCV
                
                if projPosCV == zeroPos:
                    ncv = ncv - 1
                    cmds.delete(sup + '.cv[' + str(cv) + ']')
                    cvDeleted = True
                    
                else:
                    projPos.append(projPosCV)
#                    cmds.xform(sup + '.cv[' + str(cv) + ']', ws = True, t = projPosCV)
                    cv = cv + 1
            
            if cvDeleted:
                projPos = []
                cmds.rebuildCurve(sup, ch = True, s = ncv - 3, d = 3)
                cmds.delete(sup, ch = True)
                for cv in range(ncv):
                    projPosCV = cmds.xform(sup + '.cv[' + str(cv) + ']', q = True, ws = True, t = True)
                    projPos.append(projPosCV)
                    
            
            volumeSuperCurvesPos[s] = projPos
            cmds.xform(sup, piv =  projPos[0])    
        
        for h in historyDelete:
            if cmds.objExists(h):
                cmds.delete(h)
        volumeSuperCurvesString = Pickle.dumps(volumeSuperCurves)           
        volumeSuperCurvesPosString = Pickle.dumps(volumeSuperCurvesPos)
        cmds.setAttr(currNode + '.volumeSuperCurves', volumeSuperCurvesString, type = 'string')   
        cmds.setAttr(currNode + '.volumeSuperCurvesPos', volumeSuperCurvesPosString, type = 'string')   


def isSelectedMeshValid(selObj):
    
    import cPickle as Pickle
    currNode = cmds.getAttr('gbNode.currentGBNode') 
    
    allowedSmoothValuesString = cmds.getAttr(currNode + '.allowedSmoothValues')
    allowedSmoothValues = []
    if allowedSmoothValuesString:
        allowedSmoothValues = Pickle.loads(str(allowedSmoothValuesString))
    else:
        scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
        allowedSmoothValues.append(str(cmds.polyEvaluate(scalpMesh, e = True, v = True, f = True)))
        smoothNode = cmds.polySmooth(scalpMesh)[0]
        allowedSmoothValues.append(str(cmds.polyEvaluate(scalpMesh, e = True, v = True, f = True)))
        cmds.setAttr(smoothNode + '.divisions', 2)
        allowedSmoothValues.append(str(cmds.polyEvaluate(scalpMesh, e = True, v = True, f = True)))
        cmds.delete(smoothNode)
        cmds.delete(scalpMesh, ch = True)
    currSmoothLevel = -1
    for i in range(3):
        if str(cmds.polyEvaluate(selObj, e = True, v = True, f = True)) == allowedSmoothValues[i]:
            currSmoothLevel = i
            break
            
    return currSmoothLevel
    
        
def createAlteredVerticesList(tweakMesh, compareMesh):
    
    stopGBUndo()
    import cPickle as Pickle
    currNode = cmds.getAttr('gbNode.currentGBNode')
    
    meshShapeString = cmds.getAttr(currNode + '.' + tweakMesh + 'Shape')
    meshShape = Pickle.loads(str(meshShapeString))
    compareMeshCount = cmds.polyEvaluate(compareMesh, v = True)
    if len(meshShape) > compareMeshCount:
        finalCount = compareMeshCount
    else:
        finalCount = len(meshShape)
#    tweakMeshName = cmds.getAttr(currNode + '.' + cmds.getAttr(currNode + '.tweakMesh'))
    alteredVertices = []
    
    for v in range(0,finalCount):
        if not cmds.xform(compareMesh + '.vtx[' + str(v) + ']', q = True, ws = True, t = True) == meshShape[v]:
            alteredVertices.append(v)
    
    alteredVerticesString = Pickle.dumps(alteredVertices)
    cmds.setAttr(currNode + '.alteredVertices', alteredVerticesString, type = 'string')
        

def checkPenetrations(inMesh,outMesh):
    
    stopGBUndo()
    import cPickle as Pickle
    historyDelete = []
    currNode = cmds.getAttr('gbNode.currentGBNode')
    
    checkList = []
    penetratedVertices = []

    penetratedVerticesString = Pickle.dumps(penetratedVertices)
    cmds.setAttr(currNode + '.penetratedVertices', penetratedVerticesString, type = 'string')
    return

    alteredVertices = []
    penetratedVerticesString = cmds.getAttr(currNode + '.penetratedVertices')
    if penetratedVerticesString:
        penetratedVertices = Pickle.loads(str(penetratedVerticesString))
        checkList.extend(penetratedVertices)
    alteredVerticesString = cmds.getAttr(currNode + '.alteredVertices')
    
    firstTime = False
    if not alteredVerticesString and not penetratedVerticesString:
        firstTime = True
    else:
        alteredVertices = Pickle.loads(str(alteredVerticesString))
        checkList.extend(alteredVertices)
    
    if not alteredVertices and not penetratedVertices and not firstTime:
#        print 'khaali pili'
        return
    
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    volumeMesh = cmds.getAttr(currNode + '.volumeMesh')

    
    dangerList = []
    
    
    foll = createFollicleOtherMesh(outMesh)
    historyDelete.append(foll)
    follShp = cmds.listRelatives(foll, s = True)[0]
    
    checkPlane = createCheckPlane(foll)
    historyDelete.append(checkPlane)
    
    
        
    totalV = cmds.polyEvaluate(scalpMesh, v = True)
    if firstTime:
        checkList = range(totalV)
    else:
        checkList = list(set(checkList))
    
    cmds.text('gbProgressBarText', edit = True, vis = True, label = 'Checking for any Penetrations between Scalp and Volume Mesh')
    cmds.progressBar('gbProgressBar', edit = True, pr = 0, max = totalV-1, vis = True)
 
    for v in range(totalV):
        vpos = cmds.xform(outMesh + '.vtx[' + str(v) + ']', q = True, ws = True, t = True)
        uv = cmds.polyEditUV(cmds.polyListComponentConversion(outMesh + '.vtx[' + str(v) + ']', fv = True, tuv = True)[0],query = True)
        cmds.setAttr(follShp + '.parameterU', uv[0])
        cmds.setAttr(follShp + '.parameterV', uv[1])
        cpos = cmds.xform(checkPlane, q = True, ws = True, t = True)
        spos = cmds.xform(inMesh + '.vtx[' + str(v) + ']', q = True, ws = True, t = True)
        
        vDist = distance3d(vpos, cpos)
        sDist = distance3d(spos, cpos)
        
        if sDist < vDist:
#            print sDist, vDist
           
            dangerList.append(v)
        
        cmds.progressBar('gbProgressBar', edit = True, s = 1)            

    penetratedVerticesString = Pickle.dumps(dangerList)
    cmds.setAttr(currNode + '.penetratedVertices', penetratedVerticesString, type = 'string')
    
    cmds.delete(historyDelete)
    
    cmds.text('gbProgressBarText', edit = True, vis = False)
    cmds.progressBar('gbProgressBar', edit = True, vis = False)
    cmds.progressBar('gbProgressBar', edit = True, pr = 0)

def createCheckPlane(foll):

    checkPlane = cmds.polyPlane(sx = 1, sy = 1)[0]
    cmds.setAttr(checkPlane + '.rx',-90)
    cmds.makeIdentity(checkPlane, apply = True)
    pC = cmds.parentConstraint(foll, checkPlane, mo = False)[0]
    cmds.setAttr(pC + '.target[0].targetOffsetTranslateZ', 15)
    return checkPlane
    

def recreateOriginalBase(tweakMesh):
    
    stopGBUndo()    
    import cPickle as Pickle
    currNode = cmds.getAttr('gbNode.currentGBNode')
    tweakMeshName = cmds.getAttr(currNode + '.' + cmds.getAttr(currNode + '.tweakMesh'))
    meshShape = Pickle.loads(str(cmds.getAttr(currNode + '.' + tweakMesh + 'Shape')))

    cmds.makeIdentity(tweakMeshName, apply = True) 

    dupMesh = cmds.duplicate(tweakMeshName, n = 'originalBaseMesh_' + tweakMeshName, rr = True, rc = True)[0]
    for i in range(len(meshShape)):
        cmds.xform(dupMesh + '.vtx[' + str(i) + ']', ws = True, t = meshShape[i])

    cmds.makeIdentity(dupMesh, apply = True)    
    return dupMesh
    
def mapCurvesB2B(currMesh, newMesh):
    
    stopGBUndo()
    import cPickle as Pickle
    currNode = cmds.getAttr('gbNode.currentGBNode')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    historyDelete = []

    toBeUpdatedIpol = []
    toBeUpdatedIpolString = cmds.getAttr(currNode + '.toBeUpdatedIpol')
    if toBeUpdatedIpolString:
        toBeUpdatedIpol = Pickle.loads(str(toBeUpdatedIpolString))
    
    baseMeshGrp = cmds.getAttr(currNode + '.baseMeshGroup')
    allCurvesList = []
    allCurvesList = cmds.listRelatives(cmds.listRelatives(baseMeshGrp, ad = True, typ = 'nurbsCurve'), p = True)
    if not allCurvesList:
        return
    
    alteredVertices = []
    alteredVerticesString = cmds.getAttr(currNode + '.alteredVertices')
    if alteredVerticesString:
        alteredVertices = Pickle.loads(str(alteredVerticesString))
    if not alteredVerticesString or not alteredVertices:
        return
        
    
    graphCurves = []
    graphCurvesString = cmds.getAttr(currNode + '.curveList4Graph')
    regionGrp = 'regionControlGrp_' + scalpMesh
    regionGrpChildren = []
    if cmds.objExists(regionGrp):
        regionGrpChildren = cmds.listRelatives(regionGrp, c = True)
        
    if graphCurvesString:
        graphCurves = Pickle.loads(str(graphCurvesString))
        alteredGraphCurves = getGraphCurvesFromAlteredVertices()
        if alteredGraphCurves:
            allCurvesList = list(set(allCurvesList) - set(graphCurves))
            if regionGrpChildren:
                allCurvesList = list(set(allCurvesList) - set(regionGrpChildren))
#            allCurvesList.extend([graphCurves[id] for id in alteredGraphCurves])
            allCurvesList.extend(alteredGraphCurves)        
    
#    restoreOrigCVOnUpdated()
    currMeshCPNode = createCPNode(currMesh)
    historyDelete.append(currMeshCPNode)

    newMeshFollicle = createFollicleOtherMesh(newMesh)
    historyDelete.append(newMeshFollicle)
    newMeshFollicleShp = cmds.listRelatives(newMeshFollicle, s = True)[0]
    
    zeroDistFound = False
    zeroPos = [0.0,0.0,0.0]

    toBeUpdatedIpolNames = []    

    for crv in allCurvesList:
        if scalpMesh + '_regionCtrl_' in crv:
            continue
        if crv in graphCurves:
            toBeUpdatedIpolNames.append(crv)
            
        sp = cmds.getAttr(crv + '.spans')
        dg = cmds.getAttr(crv + '.degree')
        ncv = sp + dg
        
        cv = 0
        deleted = False
        while cv < ncv:
            cvPos = cmds.xform(crv + '.cv[' + str(cv) + ']', q = True, ws = True, t = True)
            cmds.setAttr(currMeshCPNode + '.ip', cvPos[0], cvPos[1], cvPos[2])
            cvU = cmds.getAttr(currMeshCPNode + '.u')
            cvV = cmds.getAttr(currMeshCPNode + '.v')
            cmds.setAttr(newMeshFollicleShp + '.parameterU', cvU)
            cmds.setAttr(newMeshFollicleShp + '.parameterV', cvV)  
            cpPos = cmds.xform(newMeshFollicle, q= True, ws = True, t = True)
            if cv == 0:
                cmds.xform(crv, piv = cpPos)
            if not zeroDistFound:
                if 0.0 <= cpPos[0] <= 0.25 and 0.0 <= cpPos[1] <= 0.25 and 0.0 <= cpPos[2] <= 0.25:
                    zeroDistFound = True
                    zeroPos = cpPos
            
            if cpPos == zeroPos: 
#                print 'cv deleted while b2b ', crv
                ncv = ncv - 1
                deleted = True
                cmds.delete(crv + '.cv[' + str(cv) + ']')
            else:
                cmds.xform(crv + '.cv[' + str(cv) + ']', ws = True, t = cpPos)
                cv = cv + 1 
        if deleted:
            cmds.rebuildCurve(crv, ch = True, s = sp, d = dg)
            cmds.delete(crv, ch = True)
    
    
    baseMesh = cmds.getAttr(currNode + '.scalpMesh')
    superGrp = 'superCurves_charInterpolation_' + baseMesh
    if superGrp in cmds.listRelatives(baseMeshGrp, c = True):
        superCurves = cmds.listRelatives(cmds.listRelatives(superGrp, ad = True, typ = 'nurbsCurve'), p = True)
        if superCurves:
            usedSuperCurvesString = cmds.getAttr(currNode + '.superCurves3D')
            if usedSuperCurvesString:
                usedSuperCurves = Pickle.loads(str(usedSuperCurvesString))
                if usedSuperCurves:
                    usedSuperCurvesPosString = cmds.getAttr(currNode + '.superCurvesPos')
                    usedSuperCurvesPos = Pickle.loads(str(usedSuperCurvesPosString))
                    maxCV = cmds.getAttr('gbNode.maxCV')
                    for sup in superCurves:
                        cmds.rebuildCurve(sup , s = maxCV-3, degree = 3)
                        usedSuperCurvesPos[usedSuperCurves.index(sup)] = [cmds.xform(sup + '.cv[' + str(cv) + ']', q = True, ws = True, t = True) for cv in range(maxCV)]
                    usedSuperCurvesPosString = Pickle.dumps(usedSuperCurvesPos)
                    cmds.setAttr(currNode + '.superCurvesPos', usedSuperCurvesPosString, type = 'string')
            
            
    cmds.delete(historyDelete)
    
    if toBeUpdatedIpolNames:
        toBeUpdatedIpol.extend(convertCurveToIDList(toBeUpdatedIpolNames))
        toBeUpdatedIpol = list(set(toBeUpdatedIpol))
        toBeUpdatedIpolString = Pickle.dumps(toBeUpdatedIpol)
        cmds.setAttr(currNode + '.toBeUpdatedIpol', toBeUpdatedIpolString, type = 'string')
#        print 'b2b ipol to be', toBeUpdatedIpol
        
        
                
def printTOBE():
    
    currNode = cmds.getAttr('gbNode.currentGBNode')
    import cPickle as Pickle
    toBeUpdatedIpol = []    
    toBeUpdatedIpolString = cmds.getAttr(currNode + '.toBeUpdatedIpol')
    if toBeUpdatedIpolString:
        toBeUpdatedIpol = Pickle.loads(str(toBeUpdatedIpolString))
#        print 'TOBEBEBBE', toBeUpdatedIpol        
    
def getGraphCurvesFromAlteredVertices():
    
    import cPickle as Pickle
    currNode = cmds.getAttr('gbNode.currentGBNode')
    
    currMesh = cmds.getAttr(currNode + '.scalpMesh')
    graphCurvesString = cmds.getAttr(currNode + '.curveList4Graph')
    graphCurves = []
    if graphCurvesString:
        graphCurves = Pickle.loads(str(graphCurvesString))
    
    if not graphCurves or not graphCurvesString:
        return []
        
    alteredVerticesString = cmds.getAttr(currNode + '.alteredVertices')
    if alteredVerticesString:
        alteredVertices = Pickle.loads(str(alteredVerticesString))
    
    curveFaces = []
    curveFacesString = cmds.getAttr(currNode + '.curveFaces')
    if curveFacesString:
        curveFaces = Pickle.loads(str(curveFacesString))
    
    if not alteredVertices or not curveFaces:
        return graphCurves
    
    alteredCurvesID = []    
    alteredCurves = []
    facesList = cmds.ls(cmds.polyListComponentConversion([currMesh + '.vtx[' + str(i) + ']' for i in alteredVertices],fv = True, tf = True),fl = True)
    for face in facesList:
        faceID = int(face.split(currMesh + '.f[')[1].split(']')[0])
        alteredCurvesID.extend(curveFaces[faceID])
        alteredCurves.extend(convertIDToCurveList(curveFaces[faceID]))
    
    alteredCurvesID = list(set(alteredCurvesID))
    alteredCurves = list(set(alteredCurves))
    
    toBeUpdatedIpolString = cmds.getAttr(currNode + '.toBeUpdatedIpol')
    toBeUpdatedIpol = []
    if toBeUpdatedIpolString:
        toBeUpdatedIpol = Pickle.loads(str(toBeUpdatedIpolString))
    toBeUpdatedIpol.extend(alteredCurvesID)
    toBeUpdatedIpolString = Pickle.dumps(toBeUpdatedIpol)
    cmds.setAttr(currNode + '.toBeUpdatedIpol', toBeUpdatedIpolString, type = 'string')

    return alteredCurves

def morphMesh(tweakMesh, selObj, isXform, topoChanged):
    
    stopGBUndo()
    import cPickle as Pickle
    currNode = cmds.getAttr('gbNode.currentGBNode')
    
    alteredVertices = Pickle.loads(str(cmds.getAttr(currNode + '.alteredVertices')))
    tweakMeshName = cmds.getAttr(currNode + '.' + tweakMesh)
    tweakMeshShape = Pickle.loads(str(cmds.getAttr(currNode + '.' + tweakMesh + 'Shape')))
    
    if topoChanged:
        newFaceCount = cmds.polyEvaluate(selObj, v = True)
        tweakMeshShape = []
        if isXform:
            createNewVolumeMesh(tweakMeshName, selObj)
        for v in range(newFaceCount):
            tweakMeshShape.append(cmds.xform(selObj + '.vtx[' + str(v) + ']', q = True, ws = True, t = True))
    else:        
        for v in alteredVertices:
            newPos = cmds.xform(selObj + '.vtx[' + str(v) + ']', q = True, ws = True, t = True)
            if isXform:
                cmds.xform(tweakMeshName + '.vtx[' + str(v) + ']', ws = True, t = newPos)
            tweakMeshShape[v] = newPos
    
    tweakMeshShapeString = Pickle.dumps(tweakMeshShape)
    cmds.setAttr(currNode +  '.' + tweakMesh + 'Shape', tweakMeshShapeString, type = 'string')
    
def createNewVolumeMesh(origMesh, selObj):
    
    cmds.delete(origMesh)
    cmds.duplicate(selObj, name = origMesh, rr = True, rc = True)
    
def superCurvesVisibility(value):
    
    currNode = cmds.getAttr('gbNode.currentGBNode')
    superGrp = 'superCurves_charInterpolation_' + cmds.getAttr( currNode + '.scalpMesh')
    baseMeshGrpChildren = cmds.listRelatives(cmds.getAttr(currNode + '.baseMeshGroup'), c = True)
    if baseMeshGrpChildren:
        if superGrp in baseMeshGrpChildren:
            cmds.setAttr(superGrp + '.visibility', value)


#=================================================================
# COLOR GRAPHS RGB
#=================================================================


def addColorGraphs():

    stopGBUndo()
    cmds.button('addColorGraphBtn',edit = True, vis = False)
    cmds.columnLayout('addColorOptionsLyt', edit = True, vis = True)
    cmds.frameLayout('colorGraphFrame',edit = True, cl = False, vis = True)
    paint3DSelected()
    startGBUndo()

def newTextureRadioBtn():

    stopGBUndo()
    ind = cmds.radioButtonGrp('newTextureRadio', q = True, sl = True)
    if ind == 1:
        paint3DSelected()
    elif ind == 2:
        imageFilePathSelected()
    else:
        hypershadeSelected()                
    startGBUndo()        

def cancelAddColorGraph():
    cmds.button('addColorGraphBtn',edit = True, vis = True)
    cmds.columnLayout('addColorOptionsLyt', edit = True, vis = False)

def paint3DSelected():
    stopGBUndo()
    cmds.button('enter3DPaintToolBtn',edit = True, vis = True)

    cmds.rowLayout('filePathLayout',edit = True, vis = False)
    cmds.button('launchHSBtn',edit = True, vis = False)
    cmds.button('useSelectedTextureBtn',edit = True, vis = False)
    startGBUndo()
    
def imageFilePathSelected():

    stopGBUndo()
    cmds.setToolTo('selectSuperContext')
    cmds.rowLayout('filePathLayout',edit = True, vis = True)
    cmds.textField('texturefilePathTextField', edit = True, tx = 'Paste Here Path for Image File')
    cmds.button('enter3DPaintToolBtn',edit = True, vis = False)
    cmds.button('launchHSBtn',edit = True, vis = False)
    cmds.button('useSelectedTextureBtn',edit = True, vis = False)
    startGBUndo()
    
def fileTextFieldFocus():
    if cmds.textField('texturefilePathTextField',q = True) == 'Paste Here Path for Image File':
        cmds.textField('texturefilePathTextField', edit = True, tx = '')
    
def hypershadeSelected():
    
    stopGBUndo()
    cmds.button('launchHSBtn',edit = True, vis = True)
    cmds.button('enter3DPaintToolBtn',edit = True, vis = False)
    cmds.rowLayout('filePathLayout',edit = True, vis = False)
    cmds.button('useSelectedTextureBtn',edit = True, vis = False)
    startGBUndo()
    
def launchHSWindow():
    
    stopGBUndo()
    cmds.button('launchHSBtn',edit = True, vis = False)
    cmds.button('useSelectedTextureBtn',edit = True, vis = True)
    mm.eval('HypershadeWindow;')
    startGBUndo()

#=================================================================
# REGION BASED GRAPH CONTROL
#=================================================================

def colorBasedGraphSelected():
    
    stopGBUndo()
    interactiveRegionGraphUpdateOFF()
    
    cmds.frameLayout('colorGraphFrame', edit = True, vis = True, cl = True)
    cmds.frameLayout('regionBasedGraphFrame', edit = True, vis = False)
    cmds.button('colorGraphControlBtn',edit = True, en = False)
    cmds.button('regionGraphControlBtn',edit = True, en = True)
    cmds.button('loadGraphFromControlBtn', edit = True, vis = False)
    cmds.button('updateGraphOnRegionBtn', edit = True, vis = False)
    cmds.frameLayout('localizedControlFrame',edit = True, cl = True)
    currNode = cmds.getAttr('gbNode.currentGBNode')
    cmds.setAttr(currNode + '.currentLocalControl', 'color', type = 'string')

    if cmds.getAttr(currNode + '.rgbGraphs'):
#        cmds.button('addColorGraphBtn', edit = True, vis = True)
        cmds.columnLayout('rgbGraphsColumn', edit = True, vis = True)
        cmds.canvas('whiteCanvas', edit = True, vis = True)
        recallColorGraphs()
        storeStripChangesToDB('restore')
        restoreOrigCV()
        storeStripChangesToDB('store')
        forceUpdateAllAutoResize()
        autoResize()
        
    else:
        storeStripChangesToDB('restore')
        restoreOrigCV()
        storeStripChangesToDB('store')
        cmds.button('addColorGraphBtn',edit = True, vis = True)
    
    regionControlVisibility(False)            
    shadedDisplayOnViewport(True)
    startGBUndo()
    
    
def regionBasedGraphSelected():
    
    stopGBUndo()
    cmds.setToolTo('selectSuperContext')
    cmds.frameLayout('colorGraphFrame', edit = True, vis = False)
    cmds.button('addColorGraphBtn', edit = True, vis = False)
    cmds.columnLayout('rgbGraphsColumn',edit = True, vis = False) 
    cmds.canvas('whiteCanvas', edit = True, vis = False)    
    cmds.frameLayout('regionBasedGraphFrame', edit = True, vis = True, cl = False)
    cmds.button('colorGraphControlBtn',edit = True, en = True)
    cmds.button('regionGraphControlBtn',edit = True, en = False)
    cmds.button('loadGraphFromControlBtn', edit = True, vis = True)
    cmds.button('updateGraphOnRegionBtn', edit = True, vis = True)
    cmds.checkBox('regionGraphInteractiveBtn',edit = True, vis = True)
    
    cmds.frameLayout('localizedControlFrame',edit = True, cl = True)
    currNode = cmds.getAttr('gbNode.currentGBNode')
    cmds.setAttr(currNode + '.currentLocalControl', 'region', type = 'string')
    lastRegion = cmds.getAttr(currNode + '.lastRegionCtrl')
    if lastRegion:
        if cmds.objExists(lastRegion):
#            print 'last region', lastRegion
            cmds.setAttr('regionControlGrp_' + cmds.getAttr(currNode + '.scalpMesh') + '.visibility', True)
            cmds.select(lastRegion, r = True)
            storeStripChangesToDB('restore')
            restoreOrigCV()
            storeStripChangesToDB('store')
            forceUpdateAllAutoResize()
            loadGraphFromSelControl()
            autoResize()
    else:
        storeStripChangesToDB('restore')
        restoreOrigCV()
        storeStripChangesToDB('store')
        
    regionControlVisibility(True)
    shadedDisplayOnViewport(False)
    startGBUndo()
    
def forceUpdateAllAutoResize():
    
    import cPickle as Pickle
    currNode = cmds.getAttr('gbNode.currentGBNode')
    curveList4Graph = []
    curveList4GraphString = cmds.getAttr(currNode + '.curveList4Graph')
    if curveList4GraphString:
        curveList4Graph = Pickle.loads(str(curveList4GraphString))
    if not curveList4Graph:
        return
        
    toBeResize = convertCurveToIDList(curveList4Graph)              
    toBeResizeString = Pickle.dumps(toBeResize)
    cmds.setAttr(currNode + '.toBeResize', toBeResizeString, type = 'string')
    

def shadedDisplayOnViewport(switch):
    
    modelPanels = cmds.getPanel(typ = 'modelPanel')
    visPanels = cmds.getPanel(vis = True)
    activeViewports = list(set(modelPanels)&set(visPanels))
    for view in activeViewports:
        cmds.modelEditor(view, e = True, displayAppearance = 'smoothShaded', displayTextures = switch)
        
        
def regionControlVisibility(switch):
    
    currNode = cmds.getAttr('gbNode.currentGBNode')
    regionGrp = 'regionControlGrp_' + cmds.getAttr(currNode + '.scalpMesh')
    if cmds.objExists(regionGrp):
        cmds.setAttr(regionGrp + '.visibility', switch)
    
def paintRegionControlExec():
    
    stopGBUndo()
    interactiveRegionGraphUpdateOFF()
    
    currNode = cmds.getAttr('gbNode.currentGBNode')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    regionCtrlGrp = 'regionControlGrp_' + scalpMesh
    mainGrp = cmds.getAttr(currNode + '.mainGroup')
    mainGrpChildren = cmds.listRelatives(mainGrp, c = True)
    
    
    if not regionCtrlGrp in mainGrpChildren:
        cmds.group(name = regionCtrlGrp, em = True, parent = mainGrp)
    
    cmds.select(scalpMesh, r = True)        
    cmds.softSelect(edit = True, sse = 0)
	
    cmds.setToolTo('artSelectContext')
    loc = cmds.toolPropertyWindow(q = True, loc = True)
    if loc:
        mm.eval('ToggleToolSettings;')
    cmds.resetTool(cmds.currentCtx())
    mm.eval('setComponentPickMask ' + dQ + 'Facet' + dQ + ' true;')
    fieldLayout = 'MayaWindow|MainToolSettingsLayout|tabLayout1|artSelect|artSelectStrokeFrame|columnLayout4|columnLayout5'
    if cmds.columnLayout(fieldLayout, q = True, exists = True):
        cmds.columnLayout(fieldLayout, e = True, vis = False)
        
    cmds.artSelectCtx('artSelectContext', e = True, asc = 'python(' + dQ + 'addRegionCtrl()' + dQ + ');')
    cmds.artSelectCtx('artSelectContext', e = True, addselection = False)
    cmds.scriptJob( e = ['ToolChanged','resetArtSelectTool()'], runOnce = True)
    
    startGBUndo()
    

def addRegionCtrl():
    

    import cPickle as Pickle
    
    historyDelete = []
    faceList = []
    sel = cmds.ls(sl = True, fl = True, st = True)
    selFaceOnly = cmds.ls(sl = True, fl = True)
    
    currNode = cmds.getAttr('gbNode.currentGBNode')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')

    regionAdded = []
    regionAddedString = cmds.getAttr(currNode + '.regionAdded')
    if regionAddedString:
        regionAdded = Pickle.loads(str(regionAddedString))    
        
    charCPNode = createCPNode(scalpMesh)
    historyDelete.append(charCPNode) 
    
    scalpFoll = createFollicle('scalpMesh')
    historyDelete.append(scalpFoll)
    scalpFollShp = cmds.listRelatives(scalpFoll, s = True)[0]
    
    volFoll = createFollicle('volumeMesh')
    historyDelete.append(volFoll)
    volFollShp = cmds.listRelatives(volFoll, s = True)[0]
    
    if not len(sel):
#        print 'zero'
        reportGBMessage('No Poly Faces Selected', True, True, 'red')
#        raise RuntimeError, 'No Poly Faces Selected'
    
    for s in range(0,len(sel),2):
#        print s
        a = sel[s].split('.')[0]
        b = sel[s+1]
#        print a,b
        if a == scalpMesh and b == 'float3':
            faceList.append(sel[s])
        if len(sel) == 2:
            break

    if not len(faceList):
#        print sel
        reportGBMessage('No Poly Faces Selected', True, True, 'red')            
#        raise RuntimeError, 'No Poly Faces Selected'
    
    regionCtrlGrp = 'regionControlGrp_' + scalpMesh
    
    if 'artSelectC' in cmds.currentCtx():
#        print 'artselectc'
        posF = []
        posF4 = cmds.xform(selFaceOnly, q = True, ws = True, t = True)
        for i in range(0,3):
            posF.append(0)
            for j in range(i,len(posF4),3):
                posF[i] = posF[i] + (posF4[j]/(len(posF4)/3))
        cmds.setAttr(charCPNode + '.ip', posF[0], posF[1], posF[2])
        cpFace = scalpMesh + '.f[' + str(cmds.getAttr(charCPNode + '.f')) + ']'
        del faceList[:]
        faceList.append(cpFace)
        

    regionCtrlList = []
    regionCtrlGraph = []
    regionCtrlCurves = []
    
    regionCtrlListString = cmds.getAttr(currNode + '.regionCtrlName')
    regionCtrlGraphString = cmds.getAttr(currNode + '.regionCtrlGraph')
    regionCtrlCurvesString = cmds.getAttr(currNode + '.regionCtrlCurves')
    if regionCtrlListString:

        regionCtrlList = Pickle.loads(str(regionCtrlListString))
        regionCtrlGraph = Pickle.loads(str(regionCtrlGraphString))
        regionCtrlCurves = Pickle.loads(str(regionCtrlCurvesString))


    regionCtrl = createTemplateRegionCtrl('defaultColorGraph')

#    defaultRegionGraph = '1,1,3,0,0,3'
    defaultRegionGraph = cmds.gradientControlNoAttr( 'defaultColorGraph', q = True, asString = True)
    posF = []
    for face in faceList:
        faceID = face.split('[')[1].split(']')[0]
        regionCtrlName = scalpMesh + '_regionCtrl_' + str(faceID)
#        bulgeJoint = scalpMesh + '_bulgeJoint_' + str(faceID)
        if cmds.objExists(regionCtrlName):
            continue
        if regionCtrlName not in regionAdded:
            regionAdded.append(regionCtrlName)            
        posF = []
        posF4 = cmds.xform(face, q = True, ws = True, t = True)
        for i in range(0,3):
            posF.append(0)
            for j in range(i,len(posF4),3):
                posF[i] = posF[i] + (posF4[j]/(len(posF4)/3))
        cmds.setAttr(charCPNode + '.ip', posF[0], posF[1], posF[2])
        cmds.setAttr(scalpFollShp + '.parameterU', cmds.getAttr(charCPNode + '.u'))
        cmds.setAttr(scalpFollShp + '.parameterV', cmds.getAttr(charCPNode + '.v'))
        cmds.setAttr(volFollShp + '.parameterU', cmds.getAttr(charCPNode + '.u'))
        cmds.setAttr(volFollShp + '.parameterV', cmds.getAttr(charCPNode + '.v'))
#        dist = distance3d(cmds.xform(scalpFoll,q = True, ws = True, t = True), cmds.xform(volFoll,q = True, ws = True, t = True))
        regionCtrlDup = cmds.duplicate(regionCtrl, name =  regionCtrlName, rr = True, rc = True)[0]
        pc = cmds.parentConstraint(volFoll, regionCtrlDup)
        cmds.delete(pc)
#        cmds.rotate('-75deg',  regionCtrlDup, r = True, y = True, ws = True)
        cmds.parent(regionCtrlDup, regionCtrlGrp)
#        dist = dist * 1.5
        dist = 1
#        cmds.scale( dist, dist, dist, regionCtrlDup, z = True, a = True)
        cmds.xform(regionCtrlDup + '.cv[0]', ws = True, t = posF)
        cmds.xform(regionCtrlDup, ws = True, piv = posF)
        
        regionCtrlList.append(regionCtrlName)
        regionCtrlGraph.append(defaultRegionGraph)
        regionCtrlCurves.append([])
        
        cmds.setAttr(regionCtrlName + '.translate', lock = True)
        cmds.setAttr(regionCtrlName + '.rotate', lock = True)
        cmds.setAttr(regionCtrlName + '.scale', lock = True)

    cmds.delete(regionCtrl)
    
    for h in historyDelete:
        if cmds.objExists(h):
            cmds.delete(h)
    
    regionCtrlListString = Pickle.dumps(regionCtrlList)
    regionCtrlGraphString = Pickle.dumps(regionCtrlGraph)
    regionCtrlCurvesString = Pickle.dumps(regionCtrlCurves)
    regionAddedString = Pickle.dumps(regionAdded)
    
    cmds.setAttr(currNode + '.regionCtrlName', regionCtrlListString, type = 'string')
    cmds.setAttr(currNode + '.regionCtrlGraph', regionCtrlGraphString, type = 'string')
    cmds.setAttr(currNode + '.regionCtrlCurves', regionCtrlCurvesString, type = 'string')
    cmds.setAttr(currNode + '.regionAdded', regionAddedString, type = 'string')
    cmds.setAttr(currNode + '.lastRegionCtrl', regionCtrlName, type = 'string')
    
    regionMoved = cmds.getAttr(currNode + '.regionMoved')
    if regionMoved:
        if cmds.objExists(regionMoved):
#            print 'now sel', cmds.ls(sl = True)
            cmds.delete(regionMoved)
            cmds.setAttr(currNode + '.regionMoved', '', type = 'string')
#            print 'new added', regionCtrlName
            cmds.select(regionCtrlName, add = True)
            loadGraphFromSelControl()
            resetArtSelectTool()

    
    
def createTemplateRegionCtrlOLD(graphName):
    
    pos = []
    i = 0.0
    scl = 2
    value = cmds.gradientControlNoAttr(graphName, q = True, vap = 0)
    pos.append([0,0,0])
    pos.append([value,0.0,0])
    pos.append([value,0.0,0])
    while i <= 1.0:
        value = cmds.gradientControlNoAttr(graphName, q = True, vap = i) 
        pos.append([value,0.0,i])
        i = i + 0.1
    pos.append([value,0.0,1])
    pos.append([value,0.0,1])
    pos.append([1,0.0,1])
    crv = cmds.curve( p= pos, d = 3)
    cmds.setAttr(crv + '.overrideEnabled', True)
    cmds.setAttr(crv + '.overrideColor', 17)
    cmds.setAttr(crv + '.scaleX', scl)

    cmds.rotate('-180deg',  crv, z = True, os = True)    
    cmds.makeIdentity(crv, apply = True)

    return crv



def createTemplateRegionCtrl(graphName):
    
    pos = []
    i = 0.0
    currNode = cmds.getAttr('gbNode.currentGBNode')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    
    scl = volumePercentByDistance(10,scalpMesh)
    value = cmds.gradientControlNoAttr(graphName, q = True, vap = 0)
    pos.append([0,0,0])
    pos.append([0,0,0])
    pos.append([value,0.0,0])
    pos.append([value,0.0,0])
    while i <= 1.0:
        value = cmds.gradientControlNoAttr(graphName, q = True, vap = i) 
        pos.append([value,0.0,i])
        i = i + 0.1
    pos.append([value,0.0,1])
    pos.append([value,0.0,1])
    pos.append([1,0.0,1])
    crv = cmds.curve( p= pos, d = 3)
    cmds.setAttr(crv + '.overrideEnabled', True)
    cmds.setAttr(crv + '.overrideColor', 17)
    cmds.setAttr(crv + '.scaleZ', scl)
    cmds.setAttr(crv + '.scaleX', scl*0.5)

    cmds.rotate('-180deg',  crv, z = True, os = True)    
    cmds.makeIdentity(crv, apply = True)

    return crv


        
def createTemplateRegionCtrlOLD():
    
    bulge = cmds.polyCylinder(subdivisionsAxis = 3, subdivisionsHeight = 2, subdivisionsCaps = 0)[0]
    cmds.rotate('90deg',  bulge, x = True)
    cmds.delete(bulge + '.f[0:2]', bulge + '.f[6]')
    cmds.makeIdentity(bulge, apply = True)
    return bulge

def loadGraphFromSelControl():
    
    stopGBUndo()
    import cPickle as Pickle
    currNode = cmds.getAttr('gbNode.currentGBNode')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    checkForRegionCtrlDelete()
    selCtrls = cmds.ls(sl = True)
    
    if not selCtrls:
        reportGBMessage('No Controllers Selected', True, True, 'red')
#        raise RuntimeError, 'No Controllers Selected'
    selCtrl = ''
    properCtrls = []
    if selCtrls:
        for ctrl in selCtrls:
            if scalpMesh + '_regionCtrl_' in ctrl:
                properCtrls.append(ctrl)
                
    if not properCtrls:
        reportGBMessage('Please select Region Controller', True, True, 'red')                                    
#        raise RuntimeError, 'Please select Region Controller'
    else:
        selCtrl = properCtrls[-1]
        cmds.select(selCtrl, r = True)
                        
    
    regionCtrlList = []
    regionCtrlGraph = []
    regionCtrlListString = cmds.getAttr(currNode + '.regionCtrlName')
    regionCtrlGraphString = cmds.getAttr(currNode + '.regionCtrlGraph')
    if regionCtrlListString:
        regionCtrlList = Pickle.loads(str(regionCtrlListString))
        regionCtrlGraph = Pickle.loads(str(regionCtrlGraphString))
    else:
        reportGBMessage('No Region Controllers Exist, Please paint first', True, True, 'red')
#        raise RuntimeError, 'No Region Controllers Exist, Please paint first'
    
    selCtrlGraph = ''
    if selCtrl in regionCtrlList:
        selCtrlGraph = regionCtrlGraph[regionCtrlList.index(selCtrl)]
        cmds.setAttr(currNode + '.lastRegionCtrl', selCtrl, type = 'string')
    
    cmds.gradientControlNoAttr( 'defaultColorGraph', e = True, asString = selCtrlGraph)
    startGBUndo()
    
def regionUpdateGraphToSelControl(mode):
    
    stopGBUndo()
    import cPickle as Pickle
    currNode = cmds.getAttr('gbNode.currentGBNode')
    regionCtrlList = []
    regionCtrlGraph = []
    regionCtrlListString = cmds.getAttr(currNode + '.regionCtrlName')
    regionCtrlGraphString = cmds.getAttr(currNode + '.regionCtrlGraph')
    if regionCtrlListString:
        regionCtrlList = Pickle.loads(str(regionCtrlListString))
        regionCtrlGraph = Pickle.loads(str(regionCtrlGraphString))
    else:
        reportGBMessage('No Region Controllers Exist, Please paint first', True, True, 'red')
#        raise RuntimeError, 'No Region Controllers Exist, Please paint first'
    
    selList = cmds.ls(sl = True, fl = True)
    selRegionCtrl = []
    for sel in selList:
        if sel in regionCtrlListString:
            selRegionCtrl.append(sel)
    
    if not selRegionCtrl:
        reportGBMessage('No Region Controllers  Selected', True, True, 'red')
#        raise RuntimeError, 'No Region Controllers  Selected'

    regionEdited = []
    regionEditedString = cmds.getAttr(currNode + '.regionEdited')
    if regionEditedString:
        regionEdited = Pickle.loads(str(regionEditedString))    
        
        
    currGraphString = cmds.gradientControlNoAttr( 'defaultColorGraph', q = True, asString = True)
    regionParent = cmds.listRelatives(selRegionCtrl[0], p = True)[0]

    for region in selRegionCtrl:
        if not region in regionEdited:
            regionEdited.append(region)
            
        regionCtrlGraph[regionCtrlList.index(region)] = currGraphString
        tempCtrl = createTemplateRegionCtrl('defaultColorGraph')

        posRoot = cmds.xform(region + '.cv[0]', q = True, ws = True, t = True)
        cmds.delete(region + '.cv[0]')
        cmds.xform(region, ws = True, piv = cmds.xform(region + '.cv[0]', q = True, ws = True, t = True))

        prC = cmds.parentConstraint(region, tempCtrl)
        cmds.delete(prC)
        
        cmds.setAttr(tempCtrl + '.scaleZ', cmds.getAttr(region + '.scaleZ'))
        cmds.setAttr(tempCtrl + '.scaleX', cmds.getAttr(region + '.scaleX'))

        cmds.xform(tempCtrl + '.cv[0]', ws = True, t = posRoot)
        cmds.xform(tempCtrl, ws = True, piv = posRoot)

        cmds.delete(region)
        cmds.rename(tempCtrl, region)
#        cmds.rotate('-75deg',  region, r = True, y = True, ws = True)
        cmds.setAttr(region + '.translate', lock = True)
        cmds.setAttr(region + '.rotate', lock = True)
        cmds.setAttr(region + '.scale', lock = True)        
        cmds.parent(region, regionParent)
        
    
    regionCtrlGraphString = Pickle.dumps(regionCtrlGraph)
    regionEditedString = Pickle.dumps(regionEdited)
    cmds.setAttr(currNode + '.regionCtrlGraph', regionCtrlGraphString, type = 'string')
    cmds.setAttr(currNode + '.regionEdited', regionEditedString, type = 'string')
    
    if mode == 'auto':
        checkForRegionEdit()
        getPerListREGION()
    
    cmds.select(selRegionCtrl, r = True)
    startGBUndo()

    
def interactiveRegionGraphUpdateON():
    
    stopGBUndo()
    autoResize()
    cmds.frameLayout('commonFrame', edit = True, cl = True)
    cmds.button('loadGraphFromControlBtn', edit = True, vis = False)
    cmds.button('updateGraphOnRegionBtn' , edit = True, vis = False)
    allJobs = cmds.scriptJob(lj = True)
    for job in allJobs:
        if 'loadGraphFromSelControl' in job:
            cmds.scriptJob(kill = int(job.split(':')[0]))
    cmds.scriptJob(p = 'gbWin', e = ['SelectionChanged', 'loadGraphFromSelControl()'])
    cmds.gradientControlNoAttr( 'defaultColorGraph', edit = True, cc = 'regionUpdateGraphToSelControl(\'auto\')')
    startGBUndo()
    

def killAllGBJobs():
    
    stopGBUndo()
#    jobList = ['loadGraphFromSelControl','stripLiveUIUpdate']
    jobList = ['loadGraphFromSelControl']
    
    allJobs = cmds.scriptJob(lj = True)
    for job in allJobs:
        for each in jobList:
            if each in job:
                cmds.scriptJob(kill = int(job.split(':')[0]))
    
    startGBUndo()         
  

        

def interactiveRegionGraphUpdateOFF():

    stopGBUndo()
    cmds.checkBox('regionGraphInteractiveBtn',edit = True, value = False)
    cmds.button('loadGraphFromControlBtn', edit = True, vis = True)
    cmds.button('updateGraphOnRegionBtn' , edit = True, vis = True)
    allJobs = cmds.scriptJob(lj = True)
    for job in allJobs:
        if 'loadGraphFromSelControl' in job:
            cmds.scriptJob(kill = int(job.split(':')[0]))
    cmds.gradientControlNoAttr( 'defaultColorGraph', edit = True, cc = 'regionUpdateDoNothing()')
    startGBUndo()
    
def regionUpdateDoNothing():
    
    return
    
def mirrorRegionCtrls():
    
    stopGBUndo()
    interactiveRegionGraphUpdateOFF()
    
    import cPickle as Pickle
    sel = cmds.ls(sl = True)
    if not sel:
        reportGBMessage('Please select Region Controller first', True, True, 'red')
#        raise RuntimeError, 'Please select Region Controller first'
    currNode = cmds.getAttr('gbNode.currentGBNode')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    regionGrp = 'regionControlGrp_' + scalpMesh
    regionGrpChildren = []
    if cmds.objExists(regionGrp):
        regionGrpChildren = cmds.listRelatives(regionGrp, c = True)        
	if not regionGrpChildren:
	    reportGBMessage('No Region Controller Exists', True, True, 'red')
#		raise RuntimeError, 'No Region Controller Exists'
    regionCtrl = []
#    print sel
    for s in sel:
        if s in regionGrpChildren:
            regionCtrl.append(s)
#    print regionCtrl
    if not regionCtrl:
        reportGBMessage('No Region Controller Selected', True, True, 'red')
#        raise RuntimeError, 'No Region Controller Selected'
    
    
    regionCtrlName = Pickle.loads(str(cmds.getAttr(currNode + '.regionCtrlName')))
    regionCtrlGraph = Pickle.loads(str(cmds.getAttr(currNode + '.regionCtrlGraph')))
    restoreDefaultGraph = cmds.gradientControlNoAttr('defaultColorGraph', q = True, asString = True)
    
    regionAdded = []
    regionAddedString = cmds.getAttr(currNode + '.regionAdded')
    if regionAddedString:
        regionAdded = Pickle.loads(str(regionAddedString))    
    
    
    historyDelete = []
    axisID = cmds.radioButtonGrp('mirrorRegionCtrlAxisRadio', q = True, sl = True)
    mirrorDict = {1:'X', 2:'Y', 3:'Z'}
    axis = mirrorDict[axisID]
    
    charCPNode = createCPNode(scalpMesh)
    historyDelete.append(charCPNode)
    
    center = cmds.objectCenter(scalpMesh, gl = True)
    tempMirrorScalpDup = scalpMesh + '_MirrorDup'
    tempMirrorGrp = scalpMesh + '_MirrorGrp'
    
    if cmds.objExists(tempMirrorScalpDup):
        cmds.delete(tempMirrorScalpDup)
    else:
        cmds.duplicate(scalpMesh, name = tempMirrorScalpDup, rr = True)

    if cmds.objExists(tempMirrorGrp):
        cmds.delete(tempMirrorGrp)
    
    cmds.group(tempMirrorScalpDup, name = tempMirrorGrp)    
    
    cmds.delete(tempMirrorScalpDup)
    cmds.xform(tempMirrorGrp, cp = True)
    
    for region in regionCtrl:
        regionDup = cmds.duplicate(region, name = region + '_DUP', rr = True)
        cmds.select(cl = True)
        cmds.parent(regionDup, tempMirrorGrp)
    
    command = 'scale -a -1 -1 -1 -scale' + axis + ' ' + tempMirrorGrp
    mm.eval(command)
    
    newRegion = cmds.listRelatives(tempMirrorGrp, c = True)
    for region in newRegion:
        
#        print bulge
        rPos = cmds.pointPosition(region + '.cv[0]')
        cmds.setAttr(charCPNode + '.ip', rPos[0], rPos[1], rPos[2])
        face = cmds.getAttr(charCPNode + '.f')
        newRegionName = scalpMesh + '_regionCtrl_' + str(face)
        if cmds.objExists(newRegionName):
            cmds.delete(newRegionName)
        if newRegionName in regionAdded:
            regionAdded.append(newRegionName)
                            
        regionGraph =  regionCtrlGraph[regionCtrlName.index(region.split('_DUP')[0])]
        cmds.gradientControlNoAttr('defaultColorGraph', edit = True, asString = regionGraph)
        cmds.select(scalpMesh + '.f[' + str(face) + ']', r = True)
        addRegionCtrl()
        cmds.delete(region)
        
    cmds.delete(tempMirrorGrp)
    for h in historyDelete:
        if cmds.objExists(h):
            cmds.delete(h)
            
    cmds.select(regionCtrl, r = True)
    
    regionAddedString = Pickle.dumps(regionAdded)
    cmds.setAttr(currNode + '.regionAdded', regionAddedString, type = 'string')
    
    cmds.gradientControlNoAttr('defaultColorGraph', edit = True, asString = restoreDefaultGraph)
    autoResize()
    startGBUndo()
    
    
    
                
def updateNewShapeRegionCtrl(alteredList):
    
    stopGBUndo()
    import cPickle as Pickle
    currNode = cmds.getAttr('gbNode.currentGBNode')
    historyDelete = []
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    regionGrp = 'regionControlGrp_' + scalpMesh
    if not cmds.objExists(regionGrp):
        return
    regionGrpChildren = cmds.listRelatives(regionGrp, c = True)
    if not regionGrpChildren:
        return
    alteredListVtx = [scalpMesh + '.vtx[' + str(v) + ']' for v in alteredList]    
    alteredListFaces = cmds.ls(cmds.polyListComponentConversion(alteredListVtx, fv = True, tf = True),fl = True)
    regionFaces = [scalpMesh + '.f[' + region.split(scalpMesh + '_regionCtrl_')[1] + ']' for region in regionGrpChildren]
    commonFaces = list(set(alteredListFaces) & set(regionFaces))
    if not commonFaces:
        return
    
    charCPNode = createCPNode(scalpMesh)
    historyDelete.append(charCPNode)
    
    scalpFoll = createFollicle('scalpMesh')
    historyDelete.append(scalpFoll)
    scalpFollShp = cmds.listRelatives(scalpFoll, s = True)[0]    
    
    volFoll = createFollicle('volumeMesh')
    historyDelete.append(volFoll)
    volFollShp = cmds.listRelatives(volFoll, s = True)[0]
    
    regionCtrlNameString = cmds.getAttr(currNode + '.regionCtrlName')
    if regionCtrlNameString:
        regionCtrlName = Pickle.loads(str(regionCtrlNameString))
        regionCtrlGraph = Pickle.loads(str(cmds.getAttr(currNode + '.regionCtrlGraph')))
        
    prevGradientValue = cmds.gradientControlNoAttr('defaultColorGraph', q = True, asString = True)
    
    for face in commonFaces:
            
        regionName = scalpMesh + '_regionCtrl_' + face.split(scalpMesh + '.f[')[1].split(']')[0]
        graphString = regionCtrlGraph[regionCtrlName.index(regionName)]
        cmds.gradientControlNoAttr('defaultColorGraph', edit = True, asString = graphString)
        cmds.delete(regionName)
        regionCtrl = createTemplateRegionCtrl('defaultColorGraph')
        cmds.rename(regionCtrl, regionName)
        posF = []
        posF4 = cmds.xform(face, q = True, ws = True, t = True)
        for i in range(0,3):
            posF.append(0)
            for j in range(i,len(posF4),3):
                posF[i] = posF[i] + (posF4[j]/(len(posF4)/3))
        cmds.setAttr(charCPNode + '.ip', posF[0], posF[1], posF[2])
        cmds.setAttr(scalpFollShp + '.parameterU', cmds.getAttr(charCPNode + '.u'))
        cmds.setAttr(scalpFollShp + '.parameterV', cmds.getAttr(charCPNode + '.v'))
        cmds.setAttr(volFollShp + '.parameterU', cmds.getAttr(charCPNode + '.u'))
        cmds.setAttr(volFollShp + '.parameterV', cmds.getAttr(charCPNode + '.v'))
#        dist = distance3d(cmds.xform(scalpFoll,q = True, ws = True, t = True), cmds.xform(volFoll,q = True, ws = True, t = True))
#        cmds.scale( 1, 1, 1, regionName, z = True, a = True)
#        cmds.makeIdentity(regionName, apply = True)
        pc = cmds.parentConstraint(volFoll, regionName)
        cmds.delete(pc)
        cmds.parent(regionName, regionGrp)
        dist = 1
        cmds.scale( dist, dist, dist, regionName, z = True, a = True)
        cmds.xform(regionName + '.cv[0]', ws = True, t = posF)
        
        cmds.xform(regionName, ws = True, piv = posF)
        cmds.setAttr(regionName + '.translate', lock = True)
        cmds.setAttr(regionName + '.rotate', lock = True)
        cmds.setAttr(regionName + '.scale', lock = True)                
#        cmds.xform(regionName, piv = posF)
        
    
    
    for h in historyDelete:
        if cmds.objExists(h):
            cmds.delete(h)
    
    
    cmds.gradientControlNoAttr('defaultColorGraph', edit = True, asString = prevGradientValue)
                    
    startGBUndo()
                
def getPerListRegionBased(clustName):
    
    
    import cPickle as Pickle
    
    historyDelete = []
    currNode = cmds.getAttr('gbNode.currentGBNode')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    charCPNode = createCPNode(scalpMesh)
    historyDelete.append(charCPNode)
    
    curveList = Pickle.loads(str(cmds.getAttr(currNode + '.curveList4Graph')))
    origCurveCVpos = Pickle.loads(str(cmds.getAttr(currNode + '.origCurveCVpos')))
    dVector = Pickle.loads(str(cmds.getAttr(currNode + '.dVector')))
    cvCountL = Pickle.loads(str(cmds.getAttr(currNode + '.cvCountL')))
    cvUV = Pickle.loads(str(cmds.getAttr(currNode + '.cvUV')))
    

    graphPerList = []
   
    allCper = []
    perC = []
    dictPer = []
    
    ''' Set will return only unique cvCount values '''
    onlyOnceCV = list(set(cvCountL)) 
    percentList = []
    allPerCrv = []

    ''' Build a dictionary which will query only once for different number of cvs '''
    
    # Create a list of dictionary 
    for x in range(0,max(onlyOnceCV)+1):   
        dictPer.append(0)
    
    ''' for every different cvCount value , build a query list of values between 0 to 1 for reading from the graph 
    dictPer => a list of percent values to query from graph for unique cvCount
    '''
    
    for eachCount in range(0,len(onlyOnceCV)):
        for x in range(0,onlyOnceCV[eachCount]):
            perCV = mm.eval('linstep(0,' + str(onlyOnceCV[eachCount]-1) + ',' + str(x) + ');')
            perC.append(perCV)
        dictPer[onlyOnceCV[eachCount]] = perC   
        perC = []

    graphLayouts = []
    regionCtrlList = []
    regionCtrlGraph = []
    regionCtrlListString = cmds.getAttr(currNode + '.regionCtrlName')
    regionCtrlList = Pickle.loads(str(regionCtrlListString))
    
    regionCtrlGraphString = cmds.getAttr(currNode + '.regionCtrlGraph')
    regionCtrlGraph = Pickle.loads(str(regionCtrlGraphString))
    
    if cmds.window('roughWorkGraph', exists = True):
        cmds.deleteUI('roughWorkGraph')
    cmds.window('roughWorkGraph')
    cmds.columnLayout('roughWorkGraphCOL')
    allControls = cmds.lsUI(controls = True)
    for i in range(len(regionCtrlGraph)):
        gName = 'roughGraphWork_' + str(i)
        cmds.gradientControlNoAttr(gName)
        if gName in allControls:
            cmds.deleteUI(gName)
        gradientName = cmds.gradientControlNoAttr(gName, edit = True, asString = regionCtrlGraph[i])
        graphLayouts.append(gradientName)
    
    graphPerList = []
    graphPerList.append([])
    graphPerList.append([])

    graphList = []
    perCV = []
    allGraphs = 0
    perCVList = []
    
    for eachCurve in range(0,len(curveList)):
#        print curveList[eachCurve]
        noOfCVs = len(origCurveCVpos[eachCurve])
        if graphLayouts == None:
            graphPerList = [['defaultColorGraph'],[1]]
        else:
            cmds.setAttr(charCPNode + '.ip', origCurveCVpos[eachCurve][0][0],origCurveCVpos[eachCurve][0][1],origCurveCVpos[eachCurve][0][2])
            vertexID = cmds.getAttr(charCPNode + '.vt')
            scalpVtx = scalpMesh + '.vtx[' + str(vertexID) + ']'
            skinList = cmds.skinPercent(clustName, scalpVtx, q = True, v = True)
            graphPerList = []
            graphPerList.append([])
            graphPerList.append([])
            for s in range(len(skinList)):
                if skinList[s] < 0.1:
                    continue
#                print s, skinList[s]
                graphPerList[0].append('roughGraphWork_' + str(s))
                graphPerList[1].append(skinList[s])
#            graphPerList = checkColorRGB(cvUV[eachCurve][0],cvUV[eachCurve][1])
            
        for eachCV in range(0,noOfCVs):
            graphList = graphPerList[0]
            perGraphList = graphPerList[1]
            queryX = dictPer[noOfCVs][eachCV]
            for eachGraph in range(0,len(graphList)):
                graphName = graphList[eachGraph]
                ogP = cmds.gradientControlNoAttr(graphName, q = True, vap = queryX)
                allGraphs = allGraphs + ( ogP * perGraphList[eachGraph])
#                print eachCV, graphList[eachGraph], perGraphList[eachGraph], ogP, allGraphs
                
            perCV.append(allGraphs)
            allGraphs = 0
        perCVList.append(perCV)
#        print perCVList
        perCV = []
    
    cmds.deleteUI('roughWorkGraph')
    for h in historyDelete:
        if cmds.objExists(h):
            cmds.delete(h) 
            
    return perCVList        

def autoResizeREGION():
    
    import cPickle as Pickle
    origSel = cmds.ls(sl = True)
#    print 'nowww', origSel
    historyDelete = []
    currNode = cmds.getAttr('gbNode.currentGBNode')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    curveList = Pickle.loads(str(cmds.getAttr(currNode + '.curveList4Graph')))
    
    usedRegion = []
    usedRegionString = cmds.getAttr(currNode + '.regionCtrlName')
    if usedRegionString:
        usedRegion = Pickle.loads(str(usedRegionString))    
    
    
    regionCtrlGrp = 'regionControlGrp_' + scalpMesh
    currentRegion = cmds.listRelatives(regionCtrlGrp, c = True)
    
    regionAdded = []
    regionAddedString = cmds.getAttr(currNode + '.regionAdded')
    if regionAddedString:
        regionAdded = Pickle.loads(str(regionAddedString))    
    
    addRegion = [region for region in regionAdded if cmds.objExists(region)]
    removeRegion = list(set(usedRegion) - set(currentRegion))
    commonRegion = list(set(currentRegion) & set(usedRegion))
    
    toBeResizeString =  cmds.getAttr(currNode + '.toBeResize')
    toBeResize = []
    if toBeResizeString:
        toBeResize = Pickle.loads(str(toBeResizeString))    
        
    regionPerList = []
    regionPerListString = cmds.getAttr(currNode + '.regionPerList')
    if not regionPerListString:
        for crv in curveList:
            regionPerList.append([[],[]])
        regionPerListString = Pickle.dumps(regionPerList)
        cmds.setAttr(currNode + '.regionPerList', regionPerListString, type = 'string')   
    
    delIndex = []   
    delRegion = []     
    if removeRegion:
        usedRegionGraph = Pickle.loads(str(cmds.getAttr(currNode + '.regionCtrlGraph')))
        regionCtrlCurves = Pickle.loads(str(cmds.getAttr(currNode + '.regionCtrlCurves')))
        regionPerList = Pickle.loads(str(cmds.getAttr(currNode + '.regionPerList')))
        
        for region in removeRegion:
            index = usedRegion.index(region)
            delIndex.append(index)
            toBeResize.extend(regionCtrlCurves[index])
            
        for region in removeRegion:
            for x in range(len(regionPerList)):
                regionID = region.split(scalpMesh + '_regionCtrl_')[1]
                if regionID in regionPerList[x][0]:
                    del regionPerList[x][0][:]
                    del regionPerList[x][1][:]
                    
#        for tbr in toBeResize:
#            if not tbr.isdigit():
#                print '10619', tbr
                
        usedRegion = [x for y, x in enumerate(usedRegion) if y not in delIndex]
        usedRegionGraph = [x for y, x in enumerate(usedRegionGraph) if y not in delIndex]
        regionCtrlCurves = [x for y, x in enumerate(regionCtrlCurves) if y not in delIndex]
        
        usedRegionString = Pickle.dumps(usedRegion)
        usedRegionGraphString = Pickle.dumps(usedRegionGraph)
        regionCtrlCurvesString = Pickle.dumps(regionCtrlCurves)
        regionPerListString = Pickle.dumps(regionPerList)
        toBeResizeString = Pickle.dumps(toBeResize)
        cmds.setAttr(currNode + '.regionCtrlName', usedRegionString, type = 'string')     
        cmds.setAttr(currNode + '.regionCtrlGraph', usedRegionGraphString, type = 'string')     
        cmds.setAttr(currNode + '.regionCtrlCurves', regionCtrlCurvesString, type = 'string')             
        cmds.setAttr(currNode + '.regionPerList', regionPerListString, type = 'string')        
        cmds.setAttr(currNode + '.toBeResize', toBeResizeString, type = 'string')        
    
    clustName = ''
    if addRegion or removeRegion or toBeResize:
        jointList = []
        faceForDel = []
        charCPNode = createCPNode(scalpMesh)
        historyDelete.append(charCPNode)
        for ctrl in currentRegion:
            cmds.select(cl = True)
            rootPos = cmds.xform(ctrl, q = True, ws = True, t = True)
            cmds.setAttr(charCPNode + '.ip', rootPos[0], rootPos[1], rootPos[2])
            faceForDel.append(cmds.getAttr(charCPNode + '.f'))
            cmds.joint(p = (rootPos[0], rootPos[1], rootPos[2]), n = ('joint3D_' + ctrl))
            jName = cmds.ls(selection = True)[0]
            jointList.append(jName)
            historyDelete.append(jName)
    
        
        clustName = ''
        totalJointList = jointList
        clustName = mm.eval('findRelatedSkinCluster(' + dQ + scalpMesh + dQ + ');')
#        print 'clustname' , clustName
        if clustName:
            cmds.delete(clustName)
        cmds.select(totalJointList, scalpMesh)
        tempGBNode = cmds.getAttr('gbNode.tempGBNode')   
        clustName = cmds.skinCluster(name = tempGBNode, dr = 10.0, mi = 4, omi = False, tsb = True, sm = 0 )[0]
        yldSkin(scalpMesh, totalJointList, faceForDel)
        cmds.select(cl = True)            
        
        toBeResize = list(set(toBeResize))
        toBeResizeString = Pickle.dumps(toBeResize)
        cmds.setAttr(currNode + '.toBeResize', toBeResizeString, type = 'string')     
        
                           
        updateRegionPerList(clustName, addRegion)
        
        if clustName:
            cmds.skinCluster(clustName, edit = True, ub = True)
            
        for h in historyDelete:
    	    if cmds.objExists(h):
                cmds.delete(h)

    
    regionAdded = []
    regionAddedString = Pickle.dumps(regionAdded)
    cmds.setAttr(currNode + '.regionAdded', regionAddedString, type = 'string')     
    
    checkForRegionEdit()
    getPerListREGION()    
    if cmds.objExists(clustName): 	 	
    	cmds.delete(clustName)
    if origSel:
        cmds.select(origSel, r = True)
    
def checkForRegionEdit():
    
    stopGBUndo()    
    import cPickle as Pickle
    currNode = cmds.getAttr('gbNode.currentGBNode')

    regionEdited = []    
    regionEditedString = cmds.getAttr(currNode + '.regionEdited')
    if regionEditedString:
        regionEdited = Pickle.loads(str(regionEditedString))    

    if regionEdited:

        usedRegion = Pickle.loads(str(cmds.getAttr(currNode + '.regionCtrlName')))
        regionCtrlCurves = Pickle.loads(str(cmds.getAttr(currNode + '.regionCtrlCurves')))
        toBeResize = Pickle.loads(str(cmds.getAttr(currNode + '.toBeResize')))
#        print 'regionCtrlCurves:', regionCtrlCurves   
        for region in regionEdited:
            toBeResize.extend(regionCtrlCurves[usedRegion.index(region)])
        
        toBeResize = list(set(toBeResize))
#        for tbr in toBeResize:
#            if not tbr.isdigit():
#                print '10705', tbr
                
        regionEdited = []
        toBeResizeString = Pickle.dumps(toBeResize)
        regionEditedString = Pickle.dumps(regionEdited)
        cmds.setAttr(currNode + '.toBeResize', toBeResizeString, type = 'string')     
        cmds.setAttr(currNode + '.regionEdited', regionEditedString, type = 'string')     
    startGBUndo()        

        
def getPerListREGION():
    
    import cPickle as Pickle
    currNode = cmds.getAttr('gbNode.currentGBNode')
    toBeResize = Pickle.loads(str(cmds.getAttr(currNode + '.toBeResize')))
    if not toBeResize:
        return
    
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    curveList = Pickle.loads(str(cmds.getAttr(currNode + '.curveList4Graph')))
    cvCountL = Pickle.loads(str(cmds.getAttr(currNode + '.cvCountL')))
    
    perC = []
    dictPer = []
    
    ''' Set will return only unique cvCount values '''
    onlyOnceCV = list(set(cvCountL)) 
    percentList = []
    allPerCrv = []

    ''' Build a dictionary which will query only once for different number of cvs '''
    
    # Create a list of dictionary 
    for x in range(0,max(onlyOnceCV)+1):   
        dictPer.append(0)
    
    ''' for every different cvCount value , build a query list of values between 0 to 1 for reading from the graph 
    dictPer => a list of percent values to query from graph for unique cvCount
    '''
    
    for eachCount in range(0,len(onlyOnceCV)):
        for x in range(0,onlyOnceCV[eachCount]):
            perCV = mm.eval('linstep(0,' + str(onlyOnceCV[eachCount]-1) + ',' + str(x) + ');')
            perC.append(perCV)
        dictPer[onlyOnceCV[eachCount]] = perC   
        perC = []

    graphLayouts = []
    

    regionCtrlList = Pickle.loads(str(cmds.getAttr(currNode + '.regionCtrlName')))
    regionCtrlGraph = Pickle.loads(str(cmds.getAttr(currNode + '.regionCtrlGraph')))
    regionPerList = Pickle.loads(str(cmds.getAttr(currNode + '.regionPerList')))
    
    
    if cmds.window('roughWorkGraph', exists = True):
        cmds.deleteUI('roughWorkGraph')
    cmds.window('roughWorkGraph')
    cmds.columnLayout('roughWorkGraphCOL')
    
    for i in range(len(regionCtrlList)):

# regionCtrlName = scalpMesh + '_regionCtrl_' + str(faceID)        
        gradientCtrlName = 'roughGraphWork_' + str(regionCtrlList[i].split(scalpMesh + '_regionCtrl_')[1])
        if cmds.gradientControlNoAttr(gradientCtrlName, exists = True):
            cmds.deleteUI(gradientCtrlName)
        cmds.gradientControlNoAttr(gradientCtrlName)
        gradientName = cmds.gradientControlNoAttr(gradientCtrlName, edit = True, asString = regionCtrlGraph[i])
        graphLayouts.append(gradientName)
    
                    
    toBeResizeNameList = convertIDToCurveList(toBeResize)
    perCVList = []
    perCV = []
    
    for crv in curveList:
        perCVList.append([])
        
    
    for tbr in toBeResizeNameList:
        curveID = curveList.index(tbr)
        noOfCVs = cvCountL[curveID]
        
        for eachCV in range(noOfCVs):
            graphList = regionPerList[curveID][0]
            perGraphList = regionPerList[curveID][1]
            queryX = dictPer[noOfCVs][eachCV]
            
            allGraphs = 0
            for eachGraph in range(0,len(graphList)):
                graphName = 'roughGraphWork_' + graphList[eachGraph]
                ogP = cmds.gradientControlNoAttr(graphName, q = True, vap = queryX)
                allGraphs = allGraphs + ( ogP * perGraphList[eachGraph])
                
            perCV.append(allGraphs)
            allGraphs = 0
        
        perCVList[curveID] = perCV
        perCV = []
        
        
    cmds.deleteUI('roughWorkGraph')            
    
    brainAutoResize(perCVList)
                        
            
    

def updateRegionPerList(clustName, addRegion):
    
    import cPickle as Pickle
#    print 'addregion', addRegion
    historyDelete = []
    currNode = cmds.getAttr('gbNode.currentGBNode')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    charCPNode = ''
    curveList = Pickle.loads(str(cmds.getAttr(currNode + '.curveList4Graph')))
    toBeResize = Pickle.loads(str(cmds.getAttr(currNode + '.toBeResize')))            
    regionCtrlList = Pickle.loads(str(cmds.getAttr(currNode + '.regionCtrlName')))
    regionCtrlCurves = Pickle.loads(str(cmds.getAttr(currNode + '.regionCtrlCurves')))
    regionPerList = Pickle.loads(str(cmds.getAttr(currNode + '.regionPerList')))

#    print 'TBR:: ', toBeResize

    curveIDList = []
    addedRegionCurvesID = []
    totalJointList = []
    if addRegion:
        charCPNode = createCPNode(scalpMesh)
        historyDelete.append(charCPNode)

        addRegionJoint = ['joint3D_' + ctrl for ctrl in addRegion]
        totalJointList = cmds.skinCluster(clustName, q = True, inf = True)
        totalJoints = len(totalJointList)
        addRegionJointIndex = [totalJointList.index(region) for region in addRegionJoint]

        curveIDList = convertCurveToIDList(curveList)
        for crv in range(len(curveIDList)):
            crvID = curveIDList[crv]
            if crvID.isdigit():
                skinPerList = cmds.skinPercent(clustName, scalpMesh + '.vtx[' + str(crvID) + ']', q = True, v = True)
            else:
#                print 'not is digit'
                currPos = cmds.pointPosition(crvID + '.cv[0]', w = True)
                cmds.setAttr(charCPNode + '.ip', currPos[0], currPos[1], currPos[2])
                skinPerList = cmds.skinPercent(clustName, scalpMesh + '.vtx[' + str(cmds.getAttr(charCPNode + '.vt')) + ']', q = True, v = True)

            toBeAdded = False                
            for index in addRegionJointIndex:
                if skinPerList[index] >= 0.1:
                    toBeAdded = True
                    break
            
            if toBeAdded:
                del regionPerList[crv][0][:]
                del regionPerList[crv][1][:]                

                for jnt in range(totalJoints):
                    per = skinPerList[jnt]
                    if per < 0.1:
                        continue
                    
                    regionPerList[crv][0].append(totalJointList[jnt].split('joint3D_' + scalpMesh + '_regionCtrl_')[1])
                    regionPerList[crv][1].append(per)

                    regionIndex = regionCtrlList.index(scalpMesh + '_regionCtrl_' + str(regionPerList[crv][0][-1]))
                    if not crvID in regionCtrlCurves[regionIndex]:
                        regionCtrlCurves[regionIndex].append(crvID)
                    
                    addedRegionCurvesID.append(crvID)
                                
    
            
    if toBeResize:
        toBeResizeLeft = list(set(toBeResize) - set(addedRegionCurvesID))
        if not curveIDList:
            curveIDList = convertCurveToIDList(curveList)
        if not charCPNode:
            charCPNode = createCPNode(scalpMesh)
            historyDelete.append(charCPNode)
        if not totalJointList:
            totalJointList = cmds.skinCluster(clustName, q = True, inf = True)
            totalJoints = len(totalJointList)


#        print 'UPDATEREGIONPERLIST : regionCTRLCRUVES ', regionCtrlCurves
        for tbr in toBeResizeLeft:
            try:
                crvID = curveIDList.index(tbr)
            except ValueError:
                continue                

            if tbr.isdigit():
                skinPerList = cmds.skinPercent(clustName, scalpMesh + '.vtx[' + str(tbr) + ']', q = True, v = True)
            else:
                currPos = cmds.pointPosition(tbr + '.cv[0]', w = True)
                cmds.setAttr(charCPNode + '.ip', currPos[0], currPos[1], currPos[2])
                skinPerList = cmds.skinPercent(clustName, scalpMesh + '.vtx[' + str(cmds.getAttr(charCPNode + '.vt')) + ']', q = True, v = True)
            
            del regionPerList[crvID][0][:]
            del regionPerList[crvID][1][:]
                
            for jnt in range(totalJoints):
                per = skinPerList[jnt]
                if per < 0.1:
                    continue
                
                regionPerList[crvID][0].append(totalJointList[jnt].split('joint3D_' + scalpMesh + '_regionCtrl_')[1])
                regionPerList[crvID][1].append(per)
                
                try:
                    regionIndex = regionCtrlList.index(scalpMesh + '_regionCtrl_' + str(regionPerList[crvID][0][-1]))
                except ValueError:
                    continue                    
                if not tbr in regionCtrlCurves[regionIndex]:
#                    print 'adding tbr', tbr
                    regionCtrlCurves[regionIndex].append(tbr)
                
                
#    for tbr in toBeResize:
#        if not tbr.isdigit():
#            print '10924', tbr
        
    toBeResize = list(set(toBeResize + addedRegionCurvesID))
#    for tbr in toBeResize:
#        if not tbr.isdigit():
#            print '10929', tbr
    regionPerListString = Pickle.dumps(regionPerList)
    regionCtrlCurvesString = Pickle.dumps(regionCtrlCurves)    
    toBeResizeString = Pickle.dumps(toBeResize)        
    
    cmds.setAttr(currNode + '.regionPerList', regionPerListString, type = 'string')
    cmds.setAttr(currNode + '.regionCtrlCurves', regionCtrlCurvesString, type = 'string')
    cmds.setAttr(currNode + '.toBeResize', toBeResizeString, type = 'string')               

    if historyDelete:
        for h in historyDelete:            
            if cmds.objExists(h):
                cmds.delete(h)
    
                    

def createSkinForRegionBased():
    
    import cPickle as Pickle
    currNode = cmds.getAttr('gbNode.currentGBNode')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    regionCtrlListString = cmds.getAttr(currNode + '.regionCtrlName')
    regionCtrlGraphString = cmds.getAttr(currNode + '.regionCtrlGraph')
    regionCtrlList = Pickle.loads(str(regionCtrlListString))
    regionCtrlGraph = Pickle.loads(str(regionCtrlGraphString))
    jointList = []
    historyDelete = []
    
    regionCtrlGrp = 'regionControlGrp_' + scalpMesh
    regionCtrlGrpChildren = cmds.listRelatives(regionCtrlGrp, c = True)
    
       
    for ctrl in regionCtrlList:
        if not ctrl in regionCtrlGrpChildren:
            ind = regionCtrlList.index(ctrl)
            regionCtrlList.remove(ctrl)
            regionCtrlGraph.remove(regionCtrlGraph[ind])
            
    
    charCPNode = createCPNode(scalpMesh)
    historyDelete.append(charCPNode)
    faceForDel = []
    for ctrl in regionCtrlList:
        cmds.select(cl = True)
        rootPos = cmds.xform(ctrl, q = True, ws = True, t = True)
        cmds.setAttr(charCPNode + '.ip', rootPos[0], rootPos[1], rootPos[2])
        faceForDel.append(cmds.getAttr(charCPNode + '.f'))
        cmds.joint(p = (rootPos[0], rootPos[1], rootPos[2]), n = ('joint3D_' + ctrl))
        jName = cmds.ls(selection = True)[0]
        jointList.append(jName)
        historyDelete.append(jName)
        
#    cmds.parent(jointList,superGrp)

    clustName = ''
    totalJointList = jointList
    
    clustName = mm.eval('findRelatedSkinCluster(' + dQ + scalpMesh + dQ + ');')
    if clustName:
        cmds.delete(clustName)
    cmds.select(totalJointList, scalpMesh)
    tempGBNode = cmds.getAttr('gbNode.tempGBNode')   
    clustName = cmds.skinCluster(name = tempGBNode, dr = 10.0, mi = 4, omi = False, tsb = True, sm = 0 )[0]
    yldSkin(scalpMesh, totalJointList, faceForDel)
    cmds.select(cl = True)
    
#    percentList = getPerListRegionBased('skinCluster1')
    percentList = getPerListRegionBased(clustName)
   
    if clustName:
        if cmds.objExists(clustName):
            cmds.skinCluster(clustName, edit = True, ub = True)
    
    for h in historyDelete:
    	if cmds.objExists(h):
            cmds.delete(h)
    
    regionCtrlListString = Pickle.dumps(regionCtrlList)
    regionCtrlGraphString = Pickle.dumps(regionCtrlGraph)
    cmds.setAttr(currNode + '.regionCtrlName', regionCtrlListString, type = 'string')
    cmds.setAttr(currNode + '.regionCtrlGraph', regionCtrlGraphString, type = 'string')
         
    return percentList
        


def touchRotateAngle(p0,pA,pB):
    
    dA = [(c - d) for c, d in zip(pA,p0)] 
    dB = [(c - d) for c, d in zip(pB,p0)] 
    uA = mm.eval('unit <<' + str(dA[0]) + ',' + str(dA[1]) + ',' + str(dA[2]) + '>>')
    uB = mm.eval('unit <<' + str(dB[0]) + ',' + str(dB[1]) + ',' + str(dB[2]) + '>>')
    tRot = cmds.angleBetween(euler = True, v1=uA, v2=uB)            
    return tRot            
    
            
#OldRange = (OldMax - OldMin)  
#NewRange = (NewMax - NewMin)  
#NewValue = (((OldValue - OldMin) * NewRange) / OldRange) + NewMin

def remapNew(newMin,newMax,oldMin,oldMax,oldValue):
    
    oldRange = (oldMax - oldMin)  
    newRange = (newMax - newMin)  
    if oldRange == 0.0:
        return newMin
    else:        
        return (((oldValue - oldMin) * newRange) / oldRange) + newMin
    
def remap(aMin,aMax,vMin,vMax,ip):
    
    vRange = (vMax - vMin)
    aRange = (aMax - aMin)
    return (((ip - vMin) * aRange) / vRange) + aMin



def getShaderNames():
    
    currNode = cmds.getAttr('gbNode.currentGBNode')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    volumeMesh = cmds.getAttr(currNode + '.volumeMesh')
    displayName = cmds.getAttr(currNode + '.displayName')
    scalpShader = displayName + '_SCALP_' + scalpMesh
    if not volumeMesh:
        volumeMesh = 'volumeMesh_' + scalpMesh
    volumeShader = displayName + '_VOL_' + volumeMesh
    scalpDISPShader = displayName + '_SCALP_DISP_' + scalpMesh
    return [scalpShader, scalpShader + '_SG', volumeShader, volumeShader + '_SG',scalpDISPShader, scalpDISPShader + '_SG']
    
    
                                
def launch3DPaint():
    
    stopGBUndo()
    currNode = cmds.getAttr('gbNode.currentGBNode')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    saveFileFor3DPaint()
    shaderNames = getShaderNames()
    scalpShader = shaderNames[0]
    fileTextureAssigned = False
    colorMapped = ''
    lc = cmds.listConnections(scalpShader, s = True, c = True, p = True)
    if scalpShader + '.color' in lc:
        colorMapped = lc[lc.index(scalpShader + '.color') + 1]
        texture = colorMapped.split('.')[0]
        
        fileNode = ''
        if cmds.nodeType(texture) == 'tripleShadingSwitch':
            fileNode = cmds.listConnections(texture, s = True,t = 'file')[0]
            
        elif cmds.nodeType(texture) == 'file':
            fileNode = texture
            
        if fileNode:
            filePath = cmds.getAttr(fileNode + '.fileTextureName')
            if cmds.file(filePath, q = True, ex = True):
                if cmds.file(filePath, q = True, typ = True)[0] == 'image':
                    fileTextureAssigned = True
     
    if not fileTextureAssigned:
        if colorMapped:
            cmds.disconnectAttr(colorMapped, scalpShader + '.color')
    
    cmds.select(scalpMesh, r = True)
    mm.eval('art3dPaintToolScript 4;')
#    cmds.currentCtx()
    ftx = 1024
    fty = 1024
    if not fileTextureAssigned:
        cmds.setAttr(scalpShader + '.color', 0.5, 0.5, 0.5, type = 'double3')
        
    else:        
        ftx = cmds.art3dPaintCtx(cmds.currentCtx(), q = True, ftx = True)
        fty = cmds.art3dPaintCtx(cmds.currentCtx(), q = True, fty = True)
        
        
    
    cmds.evalDeferred('setTextureFor3DPaint (' + str(ftx) + ',' + str(fty) + ')')
    cmds.art3dPaintCtx(cmds.currentCtx(), edit = True, saveTextureOnStroke = True)
        
#    cmds.art3dPaintCtx(cmds.currentCtx(), edit = True, sts = True)
    loc = cmds.toolPropertyWindow(q = True, loc = True)
    if not loc:
        mm.eval('ToggleToolSettings;')
    else:
        mm.eval('ToggleToolSettings;')
        mm.eval('ToggleToolSettings;')
    
    
    rgbTextureAssigned()        
    startGBUndo()

def saveFileFor3DPaint():
    
    if not cmds.file(q = True, sceneName = True):
#        reportGBMessage('Please Save Scene File to Continue with 3D Paint', True, True, 'red')
        browseFilePathSelected('for3dPaint')
        

        
    
                    
def setTextureFor3DPaint(ftx, fty):

    c = 'mm.eval(\'art3dPaintAssignFileTexture( ' + dQ + 'art3dFileTextureFrame' + dQ + ');\')'
    cmds.evalDeferred(c)
    c = 'mm.eval(\'art3dPaintKeepAspectRatio true;\')'
    cmds.evalDeferred(c)
    c = 'mm.eval(\'art3dPaintSetFileSizeX ' + str(ftx) + ';\')'
    cmds.evalDeferred(c)
    c = 'mm.eval(\'art3dPaintSetFileSizeX ' + str(fty) + ';\')'
    cmds.evalDeferred(c)
    optMenu = 'art3dPaintAssignFileTxtWindow|mainForm|colLayout|art3dPaintFileFormatOptionMenu'        
    if cmds.optionMenuGrp(optMenu, exists = True):
        cmds.optionMenuGrp(optMenu, edit = True, v = 'Tiff (tif)')
    c = 'mm.eval(\'art3dPaintFileFormatOptionMenuCmd ' + dQ + 'Tiff (tif)' + dQ + ';\')'
    cmds.evalDeferred(c)
    c = 'mm.eval(\'art3dPaintAssignFileTextureNow;\')'
    cmds.evalDeferred(c)
    

    
                

def browseFilePathSelected(ip):
    
    stopGBUndo()
    currNode = cmds.getAttr('gbNode.currentGBNode')
    shaderNames = getShaderNames()
    scalpShader = shaderNames[0]
    selected = ''            
    
    for3d = False
    if ip == 'browse':
        selectedL = cmds.fileDialog2(cap = 'Browse to Image File', fm = 1, ds = 2)
#        print selectedL
        if selectedL:
            selected = selectedL[0]
#            print selected
        else:
            return            
    elif ip == 'paste':
        selected = cmds.textField('texturefilePathTextField', q = True, tx = True)
    elif ip == 'for3dPaint':
        for3d = True
        selected = ''        


    if selected and not for3d:
        if not cmds.file(selected, q = True, type = True)[0] == 'image':
            reportGBMessage('Please select an image file', True, True, 'red')
#            raise RuntimeError, 'Please select an image file'
        else:
            cmds.textField('texturefilePathTextField', edit = True, tx = selected)
            
    colorMapped = ''
    lc = cmds.listConnections(scalpShader, s = True, c = True, p = True)
    if scalpShader + '.color' in lc:
        colorMapped = lc[lc.index(scalpShader + '.color') + 1]
#        if colorMapped:
#            cmds.disconnectAttr(colorMapped,scalpShader + '.color')
    fileNodeExists = False
    if colorMapped:
        fileNode = colorMapped.split('.')[0]
        if cmds.ls(fileNode, st = True)[1] == 'file':
            fileNodeExists = True
    
    if not fileNodeExists:        
        fileNode = connectFilePlaceTexture(scalpShader)
            
    cmds.setAttr(fileNode + '.fileTextureName', selected, type = 'string')                 
    cmds.select(cl = True)
    rgbTextureAssigned()
    startGBUndo()

def connectFilePlaceTexture(shader):
    
    fileNode = cmds.shadingNode('file', asTexture = True)
    placeNode = cmds.shadingNode('place2dTexture', asUtility = True)
    cmds.connectAttr(placeNode + '.coverage', fileNode + '.coverage', f = True)
    cmds.connectAttr(placeNode + '.translateFrame', fileNode + '.translateFrame', f = True)
    cmds.connectAttr(placeNode + '.rotateFrame', fileNode + '.rotateFrame', f = True)
    cmds.connectAttr(placeNode + '.mirrorU', fileNode + '.mirrorU', f = True)
    cmds.connectAttr(placeNode + '.mirrorV', fileNode + '.mirrorV', f = True)
    cmds.connectAttr(placeNode + '.stagger', fileNode + '.stagger', f = True)
    cmds.connectAttr(placeNode + '.wrapU', fileNode + '.wrapU', f = True)
    cmds.connectAttr(placeNode + '.wrapV', fileNode + '.wrapV', f = True)
    cmds.connectAttr(placeNode + '.repeatUV', fileNode + '.repeatUV', f = True)
    cmds.connectAttr(placeNode + '.offset', fileNode + '.offset', f = True)
    cmds.connectAttr(placeNode + '.rotateUV', fileNode + '.rotateUV', f = True)
    cmds.connectAttr(placeNode + '.noiseUV', fileNode + '.noiseUV', f = True)
    cmds.connectAttr(placeNode + '.vertexUvOne', fileNode + '.vertexUvOne', f = True)
    cmds.connectAttr(placeNode + '.vertexUvTwo', fileNode + '.vertexUvTwo', f = True)
    cmds.connectAttr(placeNode + '.vertexUvThree', fileNode + '.vertexUvThree', f = True)
    cmds.connectAttr(placeNode + '.vertexCameraOne', fileNode + '.vertexCameraOne', f = True)
    cmds.connectAttr(placeNode + '.outUV', fileNode + '.uvCoord', f = True)
    cmds.connectAttr(placeNode + '.outUvFilterSize', fileNode + '.uvFilterSize', f = True)
    
    
    cmds.connectAttr(fileNode + '.outColor', shader + '.color', force = True)
    return fileNode
    
    
    
def useSelectedTextureFromHS():
    
    stopGBUndo()
    shaderNames = getShaderNames()
    selNodeList = cmds.ls(sl = True)
    if not selNodeList:
        reportGBMessage('Nothing Selected, Please select 2D Texture Node', True, True, 'red')
#        raise RuntimeError, 'Nothing Selected, Please select texture node'
    else:
        selNode = selNodeList[0]
        verifySelectedTexture(selNode)
        if cmds.attributeQuery('outColor', node = selNode, ex = True):
            cmds.connectAttr(selNode + '.outColor', shaderNames[0] + '.color', force = True)
            rgbTextureAssigned()
            
        else:
            reportGBMessage('Please select a 2D Texture Node', True, True, 'red')
#            raise RuntimeError, 'Please select a texture node'

    startGBUndo()

def verifySelectedTexture(selNode):
    
    lc = cmds.listConnections(selNode)
    if lc:
        for c in lc:
            if 'place3dTexture' in c:
                reportGBMessage('It\'s a 3D Texture. Please select a 2D Texture Node', True, True, 'red')
            if cmds.ls(c, st = True)[1] == 'shadingEngine':
                reportGBMessage('It\'s a Shader. Please select a 2D Texture Node', True, True, 'red')
                
    
def rgbTextureAssigned():
    
    import cPickle as Pickle
    currNode = cmds.getAttr('gbNode.currentGBNode')
    
#    cmds.frameLayout('colorGraphFrame', edit = True, vis = False)
#    cmds.columnLayout('addColorOptionsLyt',edit = True, vis = False)
    cmds.canvas('whiteCanvas',edit = True, vis = True)
    cmds.columnLayout('rgbGraphsColumn', edit = True, vis = True)
    cmds.button('addColorGraphBtn', edit = True, vis = False)
    
    graphName = 'rgbGraphControl'
    graphString = []
    for i in range(3):
        graphString.append(cmds.gradientControlNoAttr(graphName + str(i), q = True, asString = True))
    graphString.append(cmds.gradientControlNoAttr('defaultColorGraph', q = True, asString = True))
    
    graphStringS = Pickle.dumps(graphString)
    cmds.setAttr(currNode + '.rgbGraphs', graphStringS, type = 'string')                                                                           
        
def recallColorGraphs():
    
    import cPickle as Pickle
    currNode = cmds.getAttr('gbNode.currentGBNode')
    graphName = 'rgbGraphControl'
    rgbGraphsString = cmds.getAttr(currNode + '.rgbGraphs')
    rgbGraphs = Pickle.loads(str(rgbGraphsString))
    for i in range(3):
        cmds.gradientControlNoAttr(graphName + str(i), edit = True, asString = rgbGraphs[i])
    cmds.gradientControlNoAttr('defaultColorGraph', edit = True, asString = rgbGraphs[3])        

def getScalpMeshTextureNode():  
    
    currNode = cmds.getAttr('gbNode.currentGBNode')
    rgbInfoString = cmds.getAttr(currNode + '.rgbInfo')
    
    
    shaderNames = getShaderNames()
    scalpShader = shaderNames[0]
    colorMapped = ''
    lc = cmds.listConnections(scalpShader, s = True, c = True, p = True)
    if scalpShader + '.color' in lc:
        colorMapped = lc[lc.index(scalpShader + '.color') + 1]
    
    if not colorMapped:
        if rgbInfoString:
            reportGBMessage('No texture Assigned. Please assign texture to Scalp Mesh Shader', True, True, 'red') 
#            raise RuntimeError, 'No texture Assigned. Please assign texture to Scalp Mesh Shader'        
        else:
            texture = ''     
    else:
        texture = colorMapped.split('.')[0]
        if cmds.nodeType(texture) == 'file':
            if not cmds.getAttr(texture + '.fileTextureName'):
                cmds.select(texture, r = True)
                reportGBMessage('Please assign proper path to File Texture Node', True, True, 'red')
#                raise RuntimeError, 'Please assign proper path to File Texture Node'
        elif cmds.nodeType(texture) == 'tripleShadingSwitch':
            switchConn = cmds.listConnections(texture, c = True)
            for conn in switchConn:
                if cmds.nodeType(conn) == 'file':
                    return conn
                            
                                
    return texture 
    

def editUsing3DPaintOrAE():
    
    stopGBUndo()
    currNode = cmds.getAttr('gbNode.currentGBNode')        
    texture = getScalpMeshTextureNode()
    if cmds.nodeType(texture) == 'file':
        askToolForEditFileTexture()
#        ftx = cmds.art3dPaintCtx(cmds.currentCtx(), q = True, ftx = True)
#        fty = cmds.art3dPaintCtx(cmds.currentCtx(), q = True, fty = True)
#        setTextureFor3DPaint(ftx,fty)
    else:
        cmds.setToolTo('selectSuperContext')
        mm.eval ('showEditorExact(' + dQ + texture + dQ + ')')       
    startGBUndo()        



def askToolForEditFileTexture():
    
    if cmds.window('askToolForEditTextureWin', exists = True):
        cmds.deleteUI('askToolForEditTextureWin')

    pathToApp = getDefaultEditApp()
    pathComment = False
    if not pathToApp:
        pathToApp = 'No Application Assigned in Preferences'
        pathComment = True
    cmds.window('askToolForEditTextureWin', title = 'Tool For Editing File Texture')
    cmds.columnLayout(adj = True)
    cmds.text(label = 'Select the tool to be used for Editing File Texture')
#    cmds.rowLayout(ad2 = 2, columnAlign2 = ['center','center'], cw2 = [150,150], nc = 2)
    cmds.button(label = '3D Paint Tool', c = 'editUsing3DPaint()')
    cmds.rowLayout('canvasRow',nc = 4)
    cmds.canvas('gbWhiteCanvas', h = 20,w = 124,rgb=(1, 1, 1), pc = 'canvasSelect([1,1,1])')
    cmds.canvas('gbRedCanvas', h = 20,w = 124,rgb=(1, 0, 0), pc = 'canvasSelect([1,0,0])')
    cmds.canvas('gbGreenCanvas', h = 20,w = 124,rgb=(0, 1, 0), pc = 'canvasSelect([0,1,0])')
    cmds.canvas('gbBlueCanvas', h = 20,w = 124,rgb=(0, 0, 1), pc = 'canvasSelect([0,0,1])')
    cmds.setParent('..')
    cmds.button(label = pathToApp, c = 'editUsingDefaultApplication()')
    cmds.button(label = 'Reload Texture', c = 'reloadTextureFromDisk()')
#    cmds.setParent('..')
    cmds.text(label = '')
    cmds.text(label = 'Window > Settings/Preferences > Preferences > Applications > Application Path for Editing Image Files', fn = 'obliqueLabelFont')
    cmds.text(label = 'e.g. C:\\Program Files (x86)\\Adobe\Adobe Photoshop CS2\\Photoshop.exe',fn = 'obliqueLabelFont')
    cmds.showWindow()
    
    w = cmds.rowLayout('canvasRow', q = True, w = True)
    cw = int(round(w/4))
    cmds.canvas('gbWhiteCanvas', edit = True, w = cw)
    cmds.canvas('gbRedCanvas', edit = True, w = cw)
    cmds.canvas('gbGreenCanvas', edit = True, w = cw)
    cmds.canvas('gbBlueCanvas', edit = True, w = cw)
    
def canvasSelect(colorSel):
    
#    print colorSel
    editUsing3DPaint()
    loc = cmds.toolPropertyWindow(q = True, loc = True)
    revert = False
    if not loc:
        revert = True
        mm.eval('ToggleToolSettings;')
    loc = cmds.toolPropertyWindow(q = True, loc = True)                
#    print loc
    allui = cmds.lsUI(controls = True,long = True)
    sliderUI = ''
    for ui in allui:
        if loc in ui:
            if 'art3dColorSlider' in ui:
                sliderUI = ui
                break

#    print sliderUI                

    if not sliderUI:
        if revert:
            mm.eval('ToggleToolSettings;')
        return
    
    cmds.colorSliderGrp(sliderUI, edit = True, rgb = tuple(colorSel))    
    mm.eval('art3dUpdateColor_CB art3dPaintCtx;')
    if revert:
        mm.eval('ToggleToolSettings;')
        
            
def reloadTextureFromDisk():
    
    currNode = cmds.getAttr('gbNode.currentGBNode')        
    texture = getScalpMeshTextureNode()
    cmds.setAttr(texture + '.fileTextureName', cmds.getAttr(texture + '.fileTextureName'), type = 'string')
        
def getDefaultEditApp():
    
    path = cmds.optionVar(q = 'EditImageDir')
    if path:
        path = path.split('\\')[-1].split('.exe')[0]
    
    return path        
    
            

def editUsing3DPaint():
    
    if not cmds.currentCtx() == 'art3dPaintContext':
        currNode = cmds.getAttr('gbNode.currentGBNode')
        cmds.select(cmds.getAttr(currNode + '.scalpMesh'), r = True)
        mm.eval('art3dPaintToolScript 4;')

def editUsingDefaultApplication():
    
    import os
    import subprocess

    currNode = cmds.getAttr('gbNode.currentGBNode')        
    texture = getScalpMeshTextureNode()
    texturePath = cmds.getAttr(texture + '.fileTextureName')
    if texturePath:
        texturePath = os.path.normpath(texturePath)
    appPath = cmds.optionVar(q = 'EditImageDir')
#    print texturePath
    if appPath and texturePath:
        subprocess.Popen([appPath, texturePath])
        
    
################
### PRESETS  ###
################


def savePreset(graphName):
    
    stopGBUndo()
    currNode = cmds.getAttr('gbNode.currentGBNode')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    path = getLocationForPresets('save')

    cmds.window('savePresetWin', title = 'Save Preset')
    cmds.columnLayout('savePresetColumnLyt', adj = True)
    if graphName == 'defaultColorGraph':
        currLocalControl = cmds.getAttr(currNode + '.currentLocalControl')
        if  currLocalControl == 'region':
            lastRegion = cmds.getAttr(currNode + '.lastRegionCtrl')
            if lastRegion:
                suffix = '_' + lastRegion 
            else:
                suffix = '_region'
        elif currLocalControl == 'color':
            suffix = '_white'
        else:
            suffix = '_global'
    elif 'rgbGraphControl' in graphName:
        if graphName == 'rgbGraphControl0':
            suffix = '_red'
        elif graphName == 'rgbGraphControl1':                
            suffix = '_green'
        elif graphName == 'rgbGraphControl2':
            suffix = '_blue'
    elif graphName == 'stripRootGraph':
        suffix = '_rootCurvature'
    elif graphName == 'stripTipGraph':
        suffix = '_tipCurvature'                    
                                                   
    presetName = scalpMesh + suffix
    cmds.textFieldGrp('presetNameText', label = 'Input Preset Name', text = presetName)
    cmds.button(label = 'Save Graph Preset', c = 'saveP(\'' + graphName + '\')')
    cmds.button('overwriteSavePresetBtn', label = 'Overwrite Saved Preset ?', c = 'saveP(\'' + 'overwriteANYHOW' + '\')', vis = False)
    cmds.showWindow()
    startGBUndo()

def saveP(graphName):
    
    currNode = cmds.getAttr('gbNode.currentGBNode')
    
    import os.path
    path = getLocationForPresets('save')
    input = cmds.textFieldGrp('presetNameText', q = True, text = True)
    fullPath = path + '\\' + input + '.txt'
    if not graphName == 'overwriteANYHOW':

        cmds.setAttr(currNode + '.tempData', graphName, type = 'string')
        fileExists = os.path.isfile(fullPath)
        if fileExists:
            cmds.button('overwriteSavePresetBtn', e = True, vis = True)
            cmds.textFieldGrp('presetNameText', edit = True, changeCommand = 'hideOverwritePreset()')
            reportGBMessage('Preset Name Already Exists. Overwrite Existing ?', True, False, 'red')
    
    
    graphName = cmds.getAttr(currNode + '.tempData')
    toStore = cmds.gradientControlNoAttr(graphName, q = True, asString = True)
    f = open(fullPath ,'w')
    f.write(toStore)
    f.close()
    cmds.deleteUI('savePresetWin')
    resetGBStatus()
    

def hideOverwritePreset():
    cmds.button('overwriteSavePresetBtn', e = True, vis = False)
    
def loadPresetFromGraph(graphName):
    
    stopGBUndo()
    path = getLocationForPresets('load')
    attrGraph = []
    fileList = cmds.getFileList(fld = path)
    if not fileList:
        reportGBMessage('No Graph Presets are saved yet', True, True, 'red')
        
    for fl in fileList:
        if fl.split('.')[1] == 'txt':
            attrGraph.append(fl.split('.')[0])
    
    
    if cmds.window('loadGraphPresetWin', exists = True):
        cmds.deleteUI('loadGraphPresetWin')
    cmds.window('loadGraphPresetWin', title = 'Load Presets')
    cmds.columnLayout(adj = True)
    cmds.paneLayout(configuration = 'vertical2', w = 500, h = 100, ps = (1,40,60))
    cmds.textScrollList('presetList' , h = 100, numberOfRows = len(attrGraph), append = attrGraph,selectItem = attrGraph[0])
    cmds.textScrollList('presetList', edit = True, sc = 'updatePrvGraph()', dcc = 'loadPresetExec(\'' + graphName + '\')')
    cmds.gradientControlNoAttr('previewGraph', w = 300, h = 100, enable = False)
    cmds.setParent('..')
    cmds.button(label = 'Load Preset', c = 'loadPresetExec(\'' + graphName + '\')')
    cmds.showWindow()
    updatePrvGraph()
    startGBUndo()
       


def updatePrvGraph():
    
    graph = cmds.textScrollList('presetList', q = True, si = True)[0]
    path = getLocationForPresets('load') + graph + '.txt'
    f = open(path, 'r')
    for i in f:
        cmds.gradientControlNoAttr('previewGraph', edit = True, asString = i)
    f.close()        
        

def loadPresetExec(graphName):
    
    graph = cmds.textScrollList('presetList', q = True, si = True)[0]
    path = getLocationForPresets('load') + graph + '.txt'
    f = open(path, 'r')
    for i in f:
        cmds.gradientControlNoAttr(graphName, edit = True, asString = i)
    f.close() 
    
    currNode = cmds.getAttr('gbNode.currentGBNode')
    currentLocalControl = cmds.getAttr(currNode + '.currentLocalControl')
    if currentLocalControl == 'region': 
        if cmds.checkBox('regionGraphInteractiveBtn', q = True, value = True):
            regionUpdateGraphToSelControl('auto') 
        else:
            regionUpdateGraphToSelControl('manual') 
    if graphName == 'stripRootGraph':
        stripRootGraphChange()
    elif graphName == 'stripTipGraph':
        stripTipGraphChange()                            
                
#    cmds.deleteUI('loadGraphPresetWin')
    
        
def getLocationForPresets(mode):
    
    import os
    import ctypes
    from ctypes.wintypes import MAX_PATH
    
    dll = ctypes.windll.shell32
    buf = ctypes.create_unicode_buffer(MAX_PATH + 1)
    if dll.SHGetSpecialFolderPathW(None, buf, 0x0005, False):
        myDoc = buf.value
#    print myDoc        
    version = cmds.about(version = True)
    if 'x64' in version:
        version = version.split(' x64')[0] + '-x64' 
#    win64 = cmds.about(win64 = True)
#    if win64:
#        version = version + '-x64'
#    F:\Documents and Settings\user.BILLGATE-2DBCEE\My Documents\maya\2012\presets\attrPresets
    
    locationUp = myDoc + '\\maya\\' + version + '\\presets'
    location = locationUp + '\\attrPresets'
#    print location
    gbLocation = ''
    
    if not os.path.exists(locationUp):
        reportGBMessage('Can\'t  Load / Save, Write Access Needed for ' + location, True, True, 'red')
    
    if not os.path.exists(location):
        if os.access(locationUp, os.W_OK):
            os.mkdir(location)
        else:
            if mode == 'save':
                reportGBMessage('Can\'t Save, Write Access Needed for ' + location, True, True, 'red')
            
        

    if os.path.exists(location):
        if os.access(location, os.W_OK):
            gbLocation = location + '\\groomBoy\\'
            if not os.path.exists(gbLocation):
                os.mkdir(gbLocation)
        else:
            if mode == 'save':
                reportGBMessage('Can\'t Save, Write Access Needed for ' + location, True, True, 'red')
#                raise RuntimeError, 'Can\'t Save, Write Access Needed for ' + location
#    2014 x64-x64 
    return gbLocation    

def getLocationForMyDocs():
    
    import os
    import ctypes
    from ctypes.wintypes import MAX_PATH
    
    dll = ctypes.windll.shell32
    buf = ctypes.create_unicode_buffer(MAX_PATH + 1)
    if dll.SHGetSpecialFolderPathW(None, buf, 0x0005, False):
        myDoc = buf.value
#    print myDoc        
    version = cmds.about(version = True)
    win64 = cmds.about(win64 = True)
    if win64:
        version = version + '-x64'

    return myDoc
    
def reportGBMessage(message, isError, isUndo, colorVal = 'red'):

    if gbDebugCheck():  
        scriptEditorDebug()
    else:        
        lineerror()
    colorRange = { 'red' : [1.0,0.0,0.0] , 'yellow' : [1.0,1.0,0.0], 'blue' : [0.0,0.7,1.0] }
#    colorRange[colorVal]
    cmds.text('gbMessageStatusColor',edit = True, vis = True, bgc = colorRange[colorVal])
    cmds.text('gbMessageStatusText', edit = True, vis = True,  label = '  ' + message)

    if colorVal == 'blue':
        return 
            
    cmds.scriptJob(event = ['SelectionChanged','resetGBStatus()'], runOnce = True, killWithScene = True, p = 'gbWin')
    
    if isUndo:
        cmds.undoInfo(swf = True)
    else:
        cmds.undoInfo(swf = False)
    
                
    if isError:
        raise RuntimeError, message
    else:
        cmds.warning(message)        
                
        
def resetGBStatus():
    
    cmds.text('gbMessageStatusColor',edit = True, vis = False)
    cmds.text('gbMessageStatusText', edit = True, vis = False, label = '')



def flushIfDelete():
    
    lastUndo = cmds.undoInfo(q = True, un = True)
    if 'doDelete' in lastUndo:
        cmds.flushUndo()
    
        
def stopGBUndo():
    
    flushIfDelete()        
    resetGBStatus()    
    if cmds.button('editBaseMeshBtn', q = True, vis = True):
        cmds.undoInfo(swf = False)
    else:        
        cmds.undoInfo(state = False)
    
def startGBUndo():
    
    flushIfDelete()
    if cmds.button('editBaseMeshBtn', q = True, vis = True):
        cmds.undoInfo(swf = True)
    else:        
        cmds.undoInfo(state = True)
    
def resizeGBWindow():
    
    curWidth = cmds.window('gbWin', q = True, width = True)
    cmds.window('gbWin',edit = True, widthHeight = [10,10])
    cmds.window('gbWin',edit = True, rtf = True)
    cmds.window('gbWin',edit = True, width = curWidth)

def backupRestoreGB():
    
    if cmds.window('backupRestoreGBWin', exists = True):
        cmds.deleteUI('backupRestoreGBWin')
    cmds.window('backupRestoreGBWin', width = 200, h = 50, title = 'Backup and Restore')
#    cmds.columnLayout(adj = True)
    cmds.tabLayout('bkpResTAB')
    cmds.setParent('..')
    child1 = cmds.columnLayout(adj = True,  p = 'bkpResTAB')
#    cmds.columnLayout('bkpResTab1', adj = True, p = 'bkpResTAB')

    cmds.checkBoxGrp( 'brScalpVolCheck', numberOfCheckBoxes=2,  labelArray2=['Scalp Mesh', 'Volume Mesh'], on1 = 'brScalpCheck()', on2 = 'brVolCheck()' )
    cmds.separator(style='in' )
    
    cmds.checkBoxGrp( 'brSuperIpolManualCheck', columnWidth3 = [110,120,110], numberOfCheckBoxes=3,  labelArray3=['Super Curves','Interpolated Curves', 'Freeform Curves'], on1 = 'brSuperCheck()', on2 = 'brIpolCheck()', on3 = 'brManualCheck()' )
    cmds.separator(style='in')
    
    cmds.radioButtonGrp('brInOutRadio', numberOfRadioButtons = 2, labelArray2 = ['Inside Scene File', 'Outside Scene File'])
    cmds.radioButtonGrp('brInOutRadio', edit = True, cc1 = 'backupInside()', cc2 = 'backupOutside()', sl = 1)
    
    cmds.button(label = 'Backup', c = 'backupElementsForGB()')
    cmds.text('bkpStatus', l = '')
    cmds.setParent('..')
    
    
    textRegStpVis = getTextRegStpVis()
    child2 = cmds.columnLayout('textRegionStpCL', adj = True, p = 'bkpResTAB', vis = textRegStpVis)
    cmds.radioButtonGrp('bkpResRadioGrp', numberOfRadioButtons = 2, labelArray2 = ['Backup', 'Restore'], p = child2)
    cmds.radioButtonGrp('bkpResRadioGrp', edit = True, on1 = 'backupSetupSelected()', on2 = 'restoreSetupSelected()')
    cmds.radioButtonGrp('textRegionRadioGrp',numberOfRadioButtons = 2, labelArray2 = ['Texture Based', 'Region Based'], p = child2) 
    cmds.radioButtonGrp('textRegionRadioGrp', edit = True, on1 = 'restoreTextureSetup()', on2 = 'restoreRegionSetup()')


    
    cmds.columnLayout('backupSetupGB', adj = True, vis = False, p = child2)
#    cmds.textFieldGrp('bkpPrefix', label = 'Prefix')
    cmds.textFieldGrp('bkpDesc', label = 'Description')
    cmds.button(label = 'Backup Setup', c = 'backupSetupForGB()')
    cmds.setParent('backupSetupGB')

    cmds.columnLayout('restoreSetupGB', adj = True, vis = False, p = child2)
    cmds.textFieldButtonGrp('restorePathText', bl = 'Browse',bc = 'browsePathForRestore()',cc = 'checkPathForRestore()' )
    cmds.textScrollList('restoreScrollList', sc = 'backupToRestoreSelected()', h = 50)
    cmds.text('restoreDesc', label = 'Description')
    cmds.text('restoreModifiedDate', label = 'Last Modified Date')
    cmds.button('restoreSetupBtn', label = 'Restore ', c = 'restoreSetupForGB()')
    cmds.setParent('restoreSetupGB')
    cmds.text('textRegStpStatus', vis = False)
    cmds.tabLayout('bkpResTAB', edit = True, tabLabel=((child1, '   Elements   '), (child2, ' Texture | Region Setup ')) )
        
    cmds.showWindow('backupRestoreGBWin')
    
    if not textRegStpVis:
        cmds.text('textRegStpStatus', edit = True, label = 'Please add curves first for Adjust Volume')

def getTextRegStpVis():
    
    import cPickle as Pickle
    currNode = cmds.getAttr('gbNode.currentGBNode')
    vis = False
    curveListString = cmds.getAttr(currNode + '.curveList4Graph')
    curveList = []
    if curveListString:
        curveList = Pickle.loads(str(curveListString))
        
    if curveList:
        vis = True        
    
    return vis        

def backupSetupSelected():
    
    cmds.columnLayout('backupSetupGB',edit = True, vis = True)
    cmds.columnLayout('restoreSetupGB',edit = True, vis = False)

def restoreSetupSelected():
    
    cmds.columnLayout('backupSetupGB',edit = True, vis = False)
    cmds.columnLayout('restoreSetupGB',edit = True, vis = True)
    

def brScalpCheck():
    
    currNode = cmds.getAttr('gbNode.currentGBNode')
    
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    bkp = False    
    if scalpMesh:
        if cmds.objExists(scalpMesh):
            bkp = True

        
    if not bkp:
        cmds.checkBoxGrp('brScalpVolCheck', edit = True, v1 = False)
        reportGBMessage('Scalp Mesh Does Not Exist', False, False, 'red')
    
def brVolCheck():
    
    currNode = cmds.getAttr('gbNode.currentGBNode')
    volumeMesh = cmds.getAttr(currNode + '.volumeMesh')
    
    bkp = False    
    if volumeMesh:
        if cmds.objExists(volumeMesh):
            bkp = True
        
    if not bkp:
        cmds.checkBoxGrp('brScalpVolCheck', edit = True, v2 = False)
        reportGBMessage('Volume Mesh Does Not Exist', False, False, 'red')
    
def brSuperCheck():
    
    currNode = cmds.getAttr('gbNode.currentGBNode')
#    print 'br super'
    baseMeshGroup = cmds.getAttr(currNode + '.baseMeshGroup')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    superGroup = 'superCurves_charInterpolation_' + scalpMesh
    
    bkp = False
    if cmds.objExists(baseMeshGroup):
        if cmds.listRelatives(baseMeshGroup, c = True):
            if superGroup in cmds.listRelatives(baseMeshGroup, c = True) and cmds.objExists(superGroup):
                bkp = True
    
    
    if not bkp:                    
        cmds.checkBoxGrp('brSuperIpolManualCheck', edit = True, v1 = False)
        reportGBMessage('Super Curves Does Not Exist', False, False, 'red')
    
def brIpolCheck(): 

    currNode = cmds.getAttr('gbNode.currentGBNode')
    
    baseMeshGroup = cmds.getAttr(currNode + '.baseMeshGroup')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    ipolGroup = 'charInterpolation_' + scalpMesh
    manualGroup = 'manualCurvesGrp_' + scalpMesh
    
    bkp = False
    if cmds.objExists(baseMeshGroup):
        if cmds.listRelatives(baseMeshGroup, c = True):
            if ipolGroup in cmds.listRelatives(baseMeshGroup, c = True) and cmds.objExists(ipolGroup):
                bkp = True
#            elif manualGroup in cmds.listRelatives(baseMeshGroup, c = True) and cmds.objExists(manualGroup):
#                bkp = True

    if not bkp:                    
        cmds.checkBoxGrp('brSuperIpolManualCheck', edit = True, v2 = False)
        reportGBMessage('Interpolated Curves Does Not Exist', False, False, 'red')                            
                 

def brManualCheck():
    
    currNode = cmds.getAttr('gbNode.currentGBNode')
    
    baseMeshGroup = cmds.getAttr(currNode + '.baseMeshGroup')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    manualGroup = 'manualCurvesGrp_' + scalpMesh
    
    bkp = False
    if cmds.objExists(baseMeshGroup):
        if cmds.listRelatives(baseMeshGroup, c = True):
            if manualGroup in cmds.listRelatives(baseMeshGroup, c = True) and cmds.objExists(manualGroup):
                bkp = True
            
    if not bkp:                    
        cmds.checkBoxGrp('brSuperIpolManualCheck', edit = True, v3 = False)
        reportGBMessage('Freeform Curves Does Not Exist', False, False, 'red')                            
    
    
def backupInside():
    
    cmds.text('bkpStatus', edit = True, label = '')
    
def backupOutside():
    
    cmds.text('bkpStatus', edit = True, label = 'Exported File will be saved in current project directory')
    
def backupElementsForGB():
    
    currNode = cmds.getAttr('gbNode.currentGBNode')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    volumeMesh = cmds.getAttr(currNode + '.volumeMesh')
    displayName = cmds.getAttr(currNode + '.displayName')
    checkBackupElementsAgain()
    returnVal = getBkpPrefix()
    bkpPrefix = returnVal[0]
    bkpSel = returnVal[1]
    
    if not returnVal:
        return
    backupGrp = 'backup_' + displayName
    if bkpSel == 'inside':
        if not bkpPrefix[-2:] == '_1':
            cmds.group(name = bkpPrefix, em = True, parent = backupGrp)
    else:
        cmds.group(name = bkpPrefix, em = True, w = True)
                
    newElements = []

    if cmds.checkBoxGrp('brScalpVolCheck', q = True, v1 = True):
        newScalp = cmds.duplicate(scalpMesh, name = bkpPrefix + '_' + scalpMesh, ic = True, rc = True, rr = True)[0]
        newElements.append(newScalp)
        cmds.delete(newScalp, ch = True)
        cmds.setAttr(bkpPrefix + '_' + scalpMesh + '.visibility', True)
    
    if cmds.checkBoxGrp('brScalpVolCheck', q = True, v2 = True): 
        newVol = cmds.duplicate(volumeMesh, name = bkpPrefix + '_' + volumeMesh, ic = True, rc = True, rr = True)[0]
        newElements.append(newVol)
        cmds.delete(newVol, ch = True)
        cmds.setAttr(newVol + '.visibility', True)
        cmds.setAttr(newVol + '.overrideEnabled', 0)
#        cmds.setAttr(newVol + '.overrideDisplayType', 0)       
        
    if cmds.checkBoxGrp('brSuperIpolManualCheck', q = True, v1 = True):
        superCurvesGrp = 'superCurves_charInterpolation_' + scalpMesh
        origSC = cmds.listRelatives(superCurvesGrp, c = True)
        newSCGrp = cmds.duplicate(superCurvesGrp, name = bkpPrefix + '_' + superCurvesGrp, ic = True, rc = True, rr = True)[0]
        newSC = cmds.listRelatives(newSCGrp, c = True)
        cmds.editDisplayLayerMembers('defaultLayer',newSCGrp, noRecurse = True)
        for x in range(len(newSC)):
            cmds.editDisplayLayerMembers('defaultLayer', newSC[x], noRecurse = True)
            shp = cmds.listRelatives(newSC[x], s = True)[0]
            cmds.editDisplayLayerMembers('defaultLayer', shp, noRecurse = True)
            cmds.setAttr(shp + '.overrideEnabled', 0)
            cmds.rename(newSC[x], bkpPrefix + '_' + origSC[x])
            
            
        newElements.append(newSCGrp)
    
    if cmds.checkBoxGrp('brSuperIpolManualCheck', q = True, v2 = True):
        ipolGrp = 'charInterpolation_' + scalpMesh
        origIpol =  cmds.listRelatives(ipolGrp, c = True)
        newIpolGrp = cmds.duplicate(ipolGrp, name = bkpPrefix + '_' + ipolGrp, ic = True, rc = True, rr = True)[0]
        newIpol = cmds.listRelatives(newIpolGrp, c = True)
        cmds.editDisplayLayerMembers('defaultLayer',newIpolGrp, noRecurse = True)
        for x in range(len(newIpol)):
            cmds.editDisplayLayerMembers('defaultLayer', newIpol[x], noRecurse = True)
            shp = cmds.listRelatives(newIpol[x], s = True)[0]
            cmds.editDisplayLayerMembers('defaultLayer', shp, noRecurse = True)
            cmds.setAttr(shp + '.overrideEnabled', 0)
            cmds.rename(newIpol[x], bkpPrefix + '_' + origIpol[x])
        newElements.append(newIpolGrp)

            
    if cmds.checkBoxGrp('brSuperIpolManualCheck', q = True, v3 = True):
        manualGrp = 'manualCurvesGrp_' + scalpMesh
        if cmds.objExists(manualGrp):
            origManual = cmds.listRelatives(manualGrp, c = True)
            newManualGrp = cmds.duplicate(manualGrp, name = bkpPrefix + '_' + manualGrp, ic = True, rc = True, rr = True)[0]
            newManual = cmds.listRelatives(newManualGrp, c = True)
            if newManual:
                cmds.editDisplayLayerMembers('defaultLayer',newManualGrp, noRecurse = True)
                for x in range(len(newManual)):
                    cmds.editDisplayLayerMembers('defaultLayer', newManual[x], noRecurse = True)
                    shp = cmds.listRelatives(newManual[x], s = True)[0]
                    cmds.editDisplayLayerMembers('defaultLayer', shp, noRecurse = True)
                    cmds.setAttr(shp + '.overrideEnabled', 0)
                    cmds.rename(newManual[x], bkpPrefix + '_' + origManual[x])
                newElements.append(newManualGrp)                
                
    cmds.parent(newElements, bkpPrefix)
    if bkpSel == 'outside':
        bkpDir = cmds.workspace(rd = True, q = True) + 'groomBoy/backup/' + displayName 
        cmds.select(bkpPrefix, r = True)
        cmds.file( bkpDir + '/' + bkpPrefix, force = True, options = 'v=0', typ = 'mayaBinary', es = True)
        cmds.delete(bkpPrefix)
        print ('Backup file path: ' + bkpDir + '/' + bkpPrefix + '.mb')
    
    cmds.text('bkpStatus', edit = True, label = 'Success! Please check Script Editor for Path')        
                        
    
     
def getBkpPrefix():
    
    returnVal = []
    if cmds.radioButtonGrp('brInOutRadio', q = True, sl = True) == 0:
        cmds.text('bkpStatus', edit = True, label = 'Please Select Inside or Outside Scene File')
        return
    elif cmds.radioButtonGrp('brInOutRadio', q = True, sl = True) == 1:
        returnVal.append(getBkpPrefixForInside())
        returnVal.append('inside')
    else:
        returnVal.append(getBkpPrefixForOutside())
        returnVal.append('outside')
                
    return returnVal

# cmds.setAttr('bkpExt_gbChar_01_1_Demo_Face_curveShape104.overrideEnabled', 0)

def getBkpPrefixForInside():
    
    currNode = cmds.getAttr('gbNode.currentGBNode')
    displayName = cmds.getAttr(currNode + '.displayName')
    mainGrp = cmds.getAttr(currNode + '.mainGroup')
    backupGrp = 'backup_' + displayName
    if not cmds.objExists(backupGrp):
        cmds.group(name = backupGrp, em = True, p = mainGrp)
        cmds.group(name = 'bkp_' + displayName + '_1', em = True, parent = backupGrp)
        return 'bkp_' + displayName + '_1'       
    else:
        if cmds.listRelatives(backupGrp, p = True)[0] == mainGrp:
            bkps = cmds.listRelatives(backupGrp, c = True)
            suffix = 1
            if bkps:
                lastBkp = 0
                for bkp in bkps:
                    if 'bkp_' + displayName in bkp:
                        suffix = bkp.split('bkp_' + displayName + '_')[1]
                        if suffix.isdigit():
                            suffix = int(suffix)
                            if suffix > lastBkp:
                                lastBkp = suffix
            return 'bkp_' + displayName + '_' + str(suffix+1)
        else:
            reportGBMessage('Extra Backup Group Exists. Please delete that or rename it', True, True, 'red')
#            print 'extra backup grp exists. delete that first or rename it'
    
        

def getBkpPrefixForOutside():
    
    import os
    currNode = cmds.getAttr('gbNode.currentGBNode')
    displayName = cmds.getAttr(currNode + '.displayName')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    
    projDirectory = cmds.workspace(rd = True, q = True)
    gbDir = projDirectory + 'groomBoy'
    bkpDir = gbDir + '/backup'
    dispDir = bkpDir + '/' + displayName
    bkpPrefix = 'bkpExt_' + displayName 
    
    if not os.path.exists(gbDir):
        os.makedirs(gbDir)
        os.makedirs(bkpDir)
        os.makedirs(dispDir)
        bkpPrefix = bkpPrefix + '_1'
        
    else:
        if not os.path.exists(bkpDir):
            os.makedirs(bkpDir)
            os.makedirs(dispDir)
            bkpPrefix = bkpPrefix + '_1'
            
        else:
            if not os.path.exists(dispDir):
                os.makedirs(dispDir)
                bkpPrefix = bkpPrefix + '_1'
                
            else:
#                print 'here'
                max = 0
                bkpPrefix = bkpPrefix + '_'
                for x in os.listdir(dispDir):
                    if os.path.isfile(dispDir + '/' + x):
                        if bkpPrefix in x:
                            suffix = x.split(bkpPrefix)[1].split('.')[0]
#                            print suffix
                            if suffix.isdigit():
                                suffix = int(suffix)
                                if suffix > max:
                                    max = suffix
                bkpPrefixT = bkpPrefix + str(max+1) 
#                print bkpPrefixT
                if cmds.objExists(bkpPrefixT):
                    while cmds.objExists(bkpPrefixT):
                        max = max + 1
                        bkpPrefixT = bkpPrefix + str(max)
                bkpPrefix = bkpPrefixT                        
    
    return bkpPrefix                        
                                
                          
    

def checkBackupElementsAgain():
    
    elements = []
    if cmds.checkBoxGrp('brScalpVolCheck', q = True, v1 = True):
        brScalpCheck()
    if cmds.checkBoxGrp('brScalpVolCheck', q = True, v2 = True):
        brVolCheck()
    if cmds.checkBoxGrp('brSuperIpolManualCheck', q = True, v1 = True):
        brSuperCheck()    
    if cmds.checkBoxGrp('brSuperIpolManualCheck', q = True, v2 = True):
        brIpolCheck()
    if cmds.checkBoxGrp('brSuperIpolManualCheck', q = True, v3 = True):
        brManualCheck()        
        


def enterReflowMode():
    
    import cPickle as Pickle
    
    
    ffc = cmds.checkBox('autoConvertToManualChk', q = True, v = True)
    if ffc:
        crvList = getCurvesForReflow('ffc')
    else:
        crvList = getCurvesForReflow('sup')
        
    generateNPNodesForReflow(crvList)        
        
        
def getCurvesForReflow(crvType):
    
    import cPickle as Pickle
    currNode = cmds.getAttr('gbNode.currentGBNode')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    baseMeshGrp = cmds.getAttr(currNode + '.baseMeshGroup')
    
    crvList = []
    if crvType == 'ffc':
        crvList = checkIfFFExists()

        if not crvList:
            reportGBMessage('Please draw some Freeform Curves first', True, True, 'red')            
    else:
        crvList = getGBSuperCurves()

        if not crvList:
            reportGBMessage('Please draw Super Curves first', True, True, 'red')                                
    
 
    return crvList

def generateNPNodesForReflow(crvList):

    if len(crvList) > 1:
        cmds.text('gbProgressBarText', edit = True, vis = True, label = 'Rebuilding Database for Reflow') 
        cmds.progressBar('gbProgressBar', edit = True, pr = 0, max = len(crvList)-1, vis = True)
    
    for crv in crvList:
        npName = crv + '_npNode'
        if cmds.objExists(npName):
            cmds.delete(npName)
        cmds.createNode('nearestPointOnCurve', name = npName)
        crvShape = cmds.listRelatives(crv, s = True)[0]
        cmds.connectAttr(crvShape + '.worldSpace[0]', npName + '.inputCurve')
        cmds.progressBar('gbProgressBar', edit = True, s = 1)
        
    cmds.text('gbProgressBarText', edit = True, vis = False)
    cmds.progressBar('gbProgressBar', edit = True, vis = False)
    cmds.progressBar('gbProgressBar', edit = True, pr = 0)
       

def enterReflowModeOLD():
    
    import cPickle as Pickle
    currNode = cmds.getAttr('gbNode.currentGBNode')


    historyDelete = []

    
    if len(superCurves) > 1:
        cmds.text('gbProgressBarText', edit = True, vis = True, label = 'Building Super Curves Database') 
        cmds.progressBar('gbProgressBar', edit = True, pr = 0, max = len(superCurves)-1, vis = True)

    superCurvesPos = []
    superMeshFaces = []
    for super in superCurves:
        sp = cmds.getAttr(super + '.spans')
        dg = cmds.getAttr(super + '.degree')
        ncv = sp + dg
        allCVPos = []
        allCVFace = []
        for cv in range(ncv):
            
            cvPos = cmds.xform(super + '.cv[' + str(cv) + ']', q = True, ws = True, t = True)
            allCVPos.append(cvPos)
            cmds.setAttr(charCPNode + '.ip', cvPos[0], cvPos[1], cvPos[2])
            allCVFace.append(cmds.getAttr(charCPNode + '.f'))
            
        superCurvesPos.append(allCVPos)
        superMeshFaces.append(allCVFace)
        
        cmds.progressBar('gbProgressBar', edit = True, s = 1)
    
    cmds.text('gbProgressBarText', edit = True, vis = False)
    cmds.progressBar('gbProgressBar', edit = True, vis = False)
    cmds.progressBar('gbProgressBar', edit = True, pr = 0)
    
    superCurvesRFString = Pickle.dumps(superCurves)
    superCurvesPosRFString = Pickle.dumps(superCurvesPos) 
    superMeshFacesRFString = Pickle.dumps(superMeshFaces) 
    
    cmds.setAttr(currNode + '.superCurvesRF', superCurvesRFString, type = 'string')
    cmds.setAttr(currNode + '.superCurvesPosRF', superCurvesPosRFString, type = 'string')
    cmds.setAttr(currNode + '.superMeshFacesRF', superMeshFacesRFString, type = 'string')
    
    for h in historyDelete:
        if cmds.objExists(h):
            cmds.delete(h)
    
    
def exitReflowMode():
    return
    
def reflowCleanup():    
    
    ffc = cmds.checkBox('autoConvertToManualChk', q = True, v = True)
    if ffc:
        crvList = getCurvesForReflow('ffc')
    else:
        crvList = getCurvesForReflow('sup')
    
    for crv in crvList:
        npName = crv + '_npNode'
        if cmds.objExists(npName):
            cmds.delete(npName)           

def getGBSuperCurves():
    
    currNode = cmds.getAttr('gbNode.currentGBNode')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    
    baseMeshGrp = cmds.getAttr(currNode + '.baseMeshGroup')
    baseMeshGrpChildren = cmds.listRelatives(baseMeshGrp, c = True)
    superGrp = 'superCurves_charInterpolation_' + scalpMesh
    if not baseMeshGrpChildren:
        return []
    if not superGrp in baseMeshGrpChildren:
        return []
    superGrpChildren = []
    superGrpChildren = cmds.listRelatives(superGrp, c = True)
    if not superGrpChildren:
        return []
    superCurves = []
    superCurves = [crv for crv in superGrpChildren if cmds.ls(cmds.listRelatives(crv, s = True), et = 'nurbsCurve')]   
      
    return superCurves
        


def execReflowMode(rfCrv):
    
    import cPickle as Pickle
    currNode = cmds.getAttr('gbNode.currentGBNode')
    drawMesh = cmds.getAttr(currNode + '.drawMesh')
    cmds.parent(rfCrv, world = True)
    historyDelete = []

    sp = cmds.getAttr(rfCrv + '.spans')
    dg = cmds.getAttr(rfCrv + '.degree')
    ncv = sp + dg
    
    rfPos = [cmds.xform(rfCrv + '.cv[' + str(cv) + ']', q = True, ws = True, t = True) for cv in range(ncv)]
    
    rfRootCV = cmds.xform(rfCrv + '.cv[0]', q = True, ws = True, t = True)
    rfTipCV = cmds.xform(rfCrv + '.cv[' + str(ncv) + ']', q = True, ws = True, t = True)

    if cmds.checkBox('autoConvertToManualChk', q = True, v = True):   
        mode = 'ffc'
        crvList = getCurvesForReflow('ffc')
    else:
        mode = 'sup'
        crvList = getCurvesForReflow('sup')
        
    tipMatch = False
    rootMatch = False
    
    rootCPList = []
    tipCPlist = []
    rootDList = []
    tipDList = []
    rootUList = []
    tipUList = []
    
    for crv in crvList:

#        if cmds.getAttr(crv + '.max') == 1.0:
#            cmds.rebuildCurve(crv, kr = 2)
        npNode = crv + '_npNode'
            
        cmds.setAttr(npNode + '.inPosition', rfRootCV[0], rfRootCV[1], rfRootCV[2])
        rootCP = list(cmds.getAttr(npNode + '.p')[0])
        rootUList.append(cmds.getAttr(npNode + '.pr'))
        rootD = distance3d(rfRootCV, rootCP)
        rootDList.append(rootD)
        
        cmds.setAttr(npNode + '.inPosition', rfTipCV[0], rfTipCV[1], rfTipCV[2])
        tipCP = list(cmds.getAttr(npNode + '.p')[0])
        tipUList.append(cmds.getAttr(npNode + '.pr'))
        tipD = distance3d(rfTipCV, tipCP)
        tipDList.append(tipD)
        
    minDist = volumePercentByDistance(cmds.floatField('reflowThres', q = True, v = True) * 100, drawMesh)

    minRD = min(rootDList)
    minRDX = rootDList.index(minRD)
    minRCrv = crvList[minRDX]
    rootMatchU = rootUList[minRDX]
    
    minTD = min(tipDList)
    minTDX = tipDList.index(minTD)
    minTCrv = crvList[minTDX]
    tipMatchU = tipUList[minTDX]
        
    if minRD <= minDist:
        rootMatch = True
    
    if minTD <= minDist:
        tipMatch = True
#    print rootMatch, '##########', tipMatch
    
    if not rootMatch and not tipMatch:
        cmds.delete(rfCrv)
        for h in historyDelete:
            if cmds.objExists(h):
                cmds.delete(h)
        reportGBMessage('Start or End of curve should touch a Super / Freeform curve', True, True, 'red')


    rootMatchNPos = []
    
    newCurvePos = []
    delCurve = ''
    
    if rootMatch and not tipMatch:
#        print 'root'
        origDg = cmds.getAttr(minRCrv + '.degree')
        origSp = cmds.getAttr(minRCrv + '.spans')
        origNCV = origDg + origSp
                
        for cv in range(origNCV):
            cvPos = cmds.xform(minRCrv + '.cv[' + str(cv) + ']', q = True, ws = True, t = True)
            npNode = minRCrv + '_npNode'
            cmds.setAttr(npNode + '.ip', cvPos[0], cvPos[1], cvPos[2])
            if cmds.getAttr(npNode + '.pr') <= rootMatchU:
                newCurvePos.append(cvPos)
            else:
                break                
        newCurvePos.extend(rfPos)            
        
        delCurve = minRCrv
        origName = minRCrv
    
    elif tipMatch and not rootMatch:
        
#        print 'tip'
        
        newCurvePos = []
        tempPos = []
        origDg = cmds.getAttr(minTCrv + '.degree')
        origSp = cmds.getAttr(minTCrv + '.spans')
        origNCV = origDg + origSp
        
        newCurvePos.extend(rfPos)
        for cv in range(origNCV,0,-1):
            cvPos = cmds.xform(minTCrv + '.cv[' + str(cv) + ']', q = True, ws = True, t = True)
            npNode = minTCrv + '_npNode'
            cmds.setAttr(npNode + '.ip', cvPos[0], cvPos[1], cvPos[2])
            if cmds.getAttr(npNode + '.pr') >= tipMatchU:
                tempPos.append(cvPos)
        
        newCurvePos.extend(list(reversed(tempPos)))
        delCurve = minTCrv
        origName = minTCrv
    
    elif rootMatch and tipMatch:

        breakCurve = False
#        print 'root and tip'
        if not minRCrv == minTCrv:
            breakCurve = True
            
            
            
        newCurvePos = []
        tempPos = []
        
        origDg = cmds.getAttr(minRCrv + '.degree')
        origSp = cmds.getAttr(minRCrv + '.spans')
        origNCV = origDg + origSp
        
        for cv in range(origNCV):
            cvPos = cmds.xform(minRCrv + '.cv[' + str(cv) + ']', q = True, ws = True, t = True)
            npNode = minRCrv + '_npNode'
            cmds.setAttr(npNode + '.ip', cvPos[0], cvPos[1], cvPos[2])
            currU = cmds.getAttr(npNode + '.pr')

            if currU <= rootMatchU:
                newCurvePos.append(cvPos)
            else:
                break
        
        newCurvePos.extend(rfPos)
        
        if not breakCurve:        
            for cv in range(origNCV,0,-1):
                cvPos = cmds.xform(minTCrv + '.cv[' + str(cv) + ']', q = True, ws = True, t = True)
                npNode = minRCrv + '_npNode'
                cmds.setAttr(npNode + '.ip', cvPos[0], cvPos[1], cvPos[2])
                currU = cmds.getAttr(npNode + '.pr')
                if currU >= tipMatchU:
                    tempPos.append(cvPos)
                                            
            newCurvePos.extend(list(reversed(tempPos)))                                        

        delCurve = minRCrv
        origName = minRCrv
        
    if delCurve:
        cmds.delete(delCurve)
                       
    cmds.delete(rfCrv)
    
    newC = cmds.curve(p = newCurvePos, d = origDg, n = origName)
    
    pivotToRoot()
    finalShp = cmds.listRelatives(newC, s = True)[0]
    npNode = newC + '_npNode'
    if not cmds.objExists(npNode):
        cmds.createNode('nearestPointOnCurve', name = npNode)

    cmds.connectAttr(finalShp + '.worldSpace[0]', npNode + '.inputCurve')

    cmds.setAttr(finalShp + '.overrideEnabled', True)
    
    ncvNew = cmds.intField('cvPFXRebuild', q = True, v = True)
    cmds.rebuildCurve(newC, s = ncvNew - origDg, ch = False )
    cmds.smoothCurve(newC + '.cv[*]', s = cmds.intField('smPFXSmooth', q = True, v = True))


    for h in historyDelete:
        if cmds.objExists(h):
            cmds.delete(h)      


    if mode == 'sup':
        scalpMesh = cmds.getAttr(currNode + '.scalpMesh')   
        cmds.parent(newC, 'superCurves_charInterpolation_' + scalpMesh)
        cmds.setAttr(finalShp + '.overrideColor', 13)

    elif mode == 'ffc':
        cmds.select(newC, r = True)
#        convertToFreeform()
    
    
            
    
'''    
def execReflowModeOLD(crv):
    
    import cPickle as Pickle
    currNode = cmds.getAttr('gbNode.currentGBNode')
    drawMesh = cmds.getAttr(currNode + '.drawMesh')
    
    historyDelete = []
    charCPNode = createCPNode(drawMesh)
    historyDelete.append(charCPNode)
    
    rfCVPos = []
    rfFaces = []
    sp = cmds.getAttr(crv + '.spans')
    dg = cmds.getAttr(crv + '.degree')
    ncv = sp + dg
    
    rfRootCV = cmds.xform(crv + '.cv[0]', q = True, ws = True, t = True)
    cmds.setAttr(charCPNode + '.ip', rfRootCV[0], rfRootCV[1], rfRootCV[2])
    rfRootF = cmds.getAttr(charCPNode + '.f')
#    rootFace = drawMesh + '.f[' + str(rfRootF)
    rootFace = rfRootF
    rfRootFaces = [int(x.split(drawMesh + '.f[')[1].split(']')[0]) for x in cmds.ls(cmds.polyListComponentConversion(cmds.polyListComponentConversion(drawMesh + '.f[' + str(rfRootF) + ']', ff = True, tv = True),fv = True, tf = True),fl = True)]
    
    rfTipCV = cmds.xform(crv + '.cv[' + str(ncv) + ']', q = True, ws = True, t = True)
    cmds.setAttr(charCPNode + '.ip', rfTipCV[0], rfTipCV[1], rfTipCV[2])
    rfTipF = cmds.getAttr(charCPNode + '.f')
#    tipFace = drawMesh + '.f[' + str(rfTipF)
    tipFace = rfTipF
    rfTipFaces = [int(x.split(drawMesh + '.f[')[1].split(']')[0]) for x in cmds.ls(cmds.polyListComponentConversion(cmds.polyListComponentConversion(drawMesh + '.f[' + str(rfTipF) + ']', ff = True, tv = True),fv = True, tf = True),fl = True)]

    
    superCurvesRF = Pickle.loads(str(cmds.getAttr(currNode + '.superCurvesRF')))
    superCurvesPosRF = Pickle.loads(str(cmds.getAttr(currNode + '.superCurvesPosRF')))
    superMeshFaces = Pickle.loads(str(cmds.getAttr(currNode + '.superMeshFacesRF')))
    
    commonFaces = []
    superCount = len(superMeshFaces)
    
    tipMatch = False
    rootMatch = False
    
    rootMatchCV = []
    rootMatchPos = []
    rootMatchCurve = []
    
    tipMatchCV = []
    tipMatchPos = []
    tipMatchCurve = []

#    print superMeshFaces

    for supF in range(superCount):
        if rootFace in superMeshFaces[supF]:
            rootMatch = True
            if superCurvesRF[supF] not in rootMatchCurve:
                rootMatchCV.append(superMeshFaces[supF].index(rootFace))
                rootMatchPos.append(superCurvesPosRF[supF][rootMatchCV[-1]])
                rootMatchCurve.append(superCurvesRF[supF])
#                print 'rootmatch'
#                print rootMatchCurve, rootMatchCV, rootMatchPos
                
        if tipFace in superMeshFaces[supF]:
            tipMatch = True
            if superCurvesRF[supF] not in tipMatchCurve:
                tipMatchCV.append(superMeshFaces[supF].index(tipFace))
                tipMatchPos.append(superCurvesPosRF[supF][tipMatchCV[-1]])
                tipMatchCurve.append(superCurvesRF[supF])
#                print 'tipmatch'
#                print tipMatchCurve, tipMatchCV, tipMatchPos
                    
    
#    print 'root' , rootFace, 'tip', tipFace
    if not rootMatch and not tipMatch:
        cmds.delete(crv)
        for h in historyDelete:
            if cmds.objExists(h):
                cmds.delete(h)
        reportGBMessage('Start or End of curve should intersect with some super curve', True, True, 'red')


    rootMatchNPos = []
    minDist = volumePercentByDistance(cmds.floatField('reflowThres', q = True, v = True) * 100, drawMesh)
#    minDist = 0.1
    tipCurve = ''
    rootCurve = ''    
    if rootMatch:
        for x in range(len(rootMatchCurve)):
            nearPtNodeR = cmds.createNode('nearestPointOnCurve')
            historyDelete.append(nearPtNodeR)
            superShp = cmds.listRelatives(rootMatchCurve[x], s = True)[0]
            cmds.connectAttr(superShp + '.worldSpace', nearPtNodeR + '.inputCurve')
            cmds.setAttr(nearPtNodeR + '.ip', rfRootCV[0], rfRootCV[1], rfRootCV[2])
            dist = distance3d(rfRootCV,list(cmds.getAttr(nearPtNodeR + '.p')[0]))
#            print 'root dist', dist
            if dist <= minDist:
                rootCurve = rootMatchCurve[x]
                rootMatchU = cmds.getAttr(nearPtNodeR + '.pr')
                break
                

    if tipMatch:
        if rootCurve:
            tipMatchCurve = [rootCurve]
        for x in range(len(tipMatchCurve)):
            nearPtNodeT = cmds.createNode('nearestPointOnCurve')
            historyDelete.append(nearPtNodeT)
            superShp = cmds.listRelatives(tipMatchCurve[x], s = True)[0]
            cmds.connectAttr(superShp + '.worldSpace', nearPtNodeT + '.inputCurve')
            cmds.setAttr(nearPtNodeT + '.ip', rfTipCV[0], rfTipCV[1], rfTipCV[2])
            dist = distance3d(rfTipCV,list(cmds.getAttr(nearPtNodeT + '.p')[0]))
#            print 'tip dist' , dist
            if dist <= minDist:
                tipCurve = tipMatchCurve[x]
                tipMatchU = cmds.getAttr(nearPtNodeT + '.pr')
                break
                        
    
    if not rootCurve and not tipCurve:
        cmds.delete(crv)
        for h in historyDelete:
            if cmds.objExists(h):
                cmds.delete(h)
        reportGBMessage('Start or End of curve should intersect with some super curve', True, True, 'red')                
    
    
    newCurvePos = []
    if rootCurve:
        dgSup = cmds.getAttr(rootCurve + '.degree')
        spSup = cmds.getAttr(rootCurve + '.spans')
        ncvSup = dgSup + spSup
        for cv in range(ncvSup):
            cvPosSup = cmds.xform(rootCurve + '.cv[' + str(cv) + ']', q = True, ws = True, t = True)
            cmds.setAttr(nearPtNodeR + '.ip', cvPosSup[0], cvPosSup[1], cvPosSup[2])
            if cmds.getAttr(nearPtNodeR + '.pr') < rootMatchU:
                newCurvePos.append(cvPosSup)
        
    
    for cv in range(ncv):
        newCurvePos.append(cmds.xform(crv + '.cv[' + str(cv) + ']', q = True, ws = True, t = True))
        
    
    
    
    if tipCurve:
        dgSup = cmds.getAttr(tipCurve + '.degree')
        spSup = cmds.getAttr(tipCurve + '.spans')
        ncvSup = dgSup + spSup
        for cv in range(ncvSup):
            cvPosSup = cmds.xform(tipCurve + '.cv[' + str(cv) + ']', q = True, ws = True, t = True)
            cmds.setAttr(nearPtNodeT + '.ip', cvPosSup[0], cvPosSup[1], cvPosSup[2])
            if cmds.getAttr(nearPtNodeT + '.pr') <= tipMatchU:
                continue
            else:
                newCurvePos.append(cvPosSup)
                

    
    if rootCurve:
#        print 'rootcurve' , rootCurve
        newName = rootCurve
        if cmds.objExists(rootCurve):
            cmds.delete(rootCurve)


    if tipCurve:
#        print 'tipCurve', tipCurve
        newName = tipCurve
        if cmds.objExists(tipCurve):
            cmds.delete(tipCurve)
            
#    print 'newnew', newName
    cmds.delete(crv)
    newC = cmds.curve(p = newCurvePos, d = dgSup, n = newName)   
    
    pivotToRoot()
    finalShp = cmds.listRelatives(newC, s = True)[0]
    cmds.setAttr(finalShp + '.overrideEnabled', True)
    cmds.setAttr(finalShp + '.overrideColor', 13)

    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')   
    cmds.parent(newC, 'superCurves_charInterpolation_' + scalpMesh)
    
    rfIndex = superCurvesRF.index(newC)
    superCurvesPosRF[rfIndex] = newCurvePos
    ncvNew = cmds.intField('cvPFXRebuild', q = True, v = True)
    cmds.rebuildCurve(newC, s = ncvNew - cmds.getAttr(newC + '.degree'), ch = False )
    cmds.smoothCurve(newC + '.cv[*]', s = cmds.intField('smPFXSmooth', q = True, v = True))
    
    newFaces = []
    for cv in range(ncvNew):
        cvPos = cmds.xform(newC + '.cv[' + str(cv) + ']', q = True, ws = True, t = True)
        cmds.setAttr(charCPNode + '.ip', cvPos[0], cvPos[1], cvPos[2])       
        newFaces.append(cmds.getAttr(charCPNode + '.f'))
    superMeshFaces[rfIndex] = newFaces        
        
    
            
    for h in historyDelete:
        if cmds.objExists(h):
            cmds.delete(h)        
            
    
    superCurvesRFString = Pickle.dumps(superCurvesRF)
    superCurvesPosRFString = Pickle.dumps(superCurvesPosRF)
    superMeshFacesRFString = Pickle.dumps(superMeshFaces)
    
    cmds.setAttr(currNode + '.superCurvesRF', superCurvesRFString, type = 'string')
    cmds.setAttr(currNode + '.superCurvesPosRF', superCurvesPosRFString, type = 'string')                
    cmds.setAttr(currNode + '.superMeshFacesRF', superMeshFacesRFString, type = 'string')        
'''        
             
    
            
        
def insertRemoveCharMenu():
    
    menuList = cmds.menu('selCharMenu', q = True, ia = True)
    if not 'removeCharOption' in menuList:
        cmds.menuItem('removeCharOption', label = 'Remove Current Character', p = 'selCharMenu', c = 'cancelAddNewChar()')

    
    
def convertToFreeform():
    
    import cPickle as Pickle
    currNode = cmds.getAttr('gbNode.currentGBNode')
    sel = cmds.ls(sl = True)
    if not sel:
        reportGBMessage('Nothing Selected', True, True, 'red')
    
    
    selCurves = cmds.listRelatives(cmds.listRelatives(sel, ad = True, typ = 'nurbsCurve'), p = True)    
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    
    manualGrp = createManualCurvesGrp()
    manualGrpChildren = cmds.listRelatives(manualGrp, c = True)
    if manualGrpChildren:
        selCurves = list(set(selCurves) - set(manualGrpChildren))
    
#    selCurves = convertIpoltoManual(selCurves) 
    addToManualCurvesDatabase(selCurves)
#    colorManualCurves(selCurves)
    
def convertToRoughCurves():
    currNode = cmds.getAttr('gbNode.currentGBNode')
    sel = cmds.ls(sl = True)
    if not sel:
        reportGBMessage('Nothing Selected', True, True, 'red')
        
    selCurves = cmds.listRelatives(cmds.listRelatives(sel, ad = True, typ = 'nurbsCurve'), p = True)    
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    
    roughGrp = createRoughMarkingCurvesGrp()
    roughGrpChildren = cmds.listRelatives(roughGrp, c = True)
    if roughGrpChildren:
        selCurves = list(set(selCurves) - set(roughGrpChildren))
        
    cmds.parent(selCurves, roughGrp)

    for sel in selCurves:
        selShp = cmds.listRelatives(sel, s = True)[0]
        cmds.setAttr(selShp + '.overrideEnabled', True)
        cmds.setAttr(selShp + '.overrideColor', 20)  
            
    

    
def convertIpoltoManual(selCurves):
    
    currNode = cmds.getAttr('gbNode.currentGBNode')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    
    ipol3dGrp = 'charInterpolation_' + scalpMesh
    baseMeshGrp = cmds.getAttr(currNode + '.baseMeshGroup')
    ipol3dChildren = []
    if ipol3dGrp in cmds.listRelatives(baseMeshGrp, c = True):
        ipol3dChildren = cmds.listRelatives(ipol3dGrp, c = True)
        
    selCurvesIpol = []
    selCurvesIpol = list(set(selCurves) & set(ipol3dChildren))
    if not selCurvesIpol:       
        return selCurves
    dupIpolList = []
    for ipol in selCurvesIpol:
        dupIpol = 'manual_' + ipol
        dupIpolList.append(cmds.duplicate(ipol, name = dupIpol, rc = True, rr = True)[0])
    
    cmds.parent(dupIpolList, world = True)
    scalpDISP = scalpMesh + '_DISPLAY'
    ipolVertices = [scalpDISP + '.vtx[' + str(crv.split('_')[-1]) + ']' for crv in selCurvesIpol]
    cmds.select(ipolVertices, r = True)
    removeInterpolationFromSelected()
    
    selCurves = list(set(selCurves) - set(selCurvesIpol))
    selCurves.extend(dupIpolList)
    return selCurves    
    

def addToManualCurvesDatabase(selCurves):
    
    currNode = cmds.getAttr('gbNode.currentGBNode')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    paintMesh = cmds.getAttr(currNode + '.paintOnMesh')
    if not paintMesh == scalpMesh:
        redrawOnScalp(selCurves)
        
    manualGrp = createManualCurvesGrp()
    cmds.parent(selCurves, manualGrp)

    for sel in selCurves:
        selShp = cmds.listRelatives(sel, s = True)[0]
        cmds.setAttr(selShp + '.overrideEnabled', True)
        cmds.setAttr(selShp + '.overrideColor', 18)
    

def redrawOnScalp(selCurves):
    
    import cPickle as Pickle
    currNode = cmds.getAttr('gbNode.currentGBNode')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    volumeMesh = cmds.getAttr(currNode + '.volumeMesh')
    
    scalpSuperCurves = []
    scalpSuperCurvesString = cmds.getAttr(currNode + '.scalpSuperCurves')
    if scalpSuperCurvesString:
        scalpSuperCurves = Pickle.loads(str(scalpSuperCurvesString))
        scalpSuperCurvesPos = Pickle.loads(str(cmds.getAttr(currNode + '.scalpSuperCurvesPos')))
    
    historyDelete = []
    currMeshCPNode = createCPNode(cmds.getAttr(currNode + '.volumeMesh'))
    historyDelete.append(currMeshCPNode)
    nextMeshFoll = createFollicle('scalpMesh')
    nextMeshFollShp = cmds.listRelatives(nextMeshFoll, s = True)[0]
    historyDelete.append(nextMeshFoll)
    
    zeroDistFound = False
    zeroPos = [0.0,0.0,0.0]
    
    for sup in selCurves:
        cmds.makeIdentity(sup, apply = True)
        sp = cmds.getAttr(sup + '.spans')
        dg = cmds.getAttr(sup +'.degree') 
        ncv = sp + dg
        
        actualPos = []
        projPos = []
        cvDeleted = False
        
        cv = 0  
        
        while cv < ncv:
#                print 'cv ', cv
            actualPosCV = cmds.xform(sup + '.cv[' + str(cv) + ']', q = True, ws = True, t = True)
            actualPos.append(actualPosCV)
            cmds.setAttr(currMeshCPNode + '.ip', actualPosCV[0], actualPosCV[1], actualPosCV[2])
            cU = cmds.getAttr(currMeshCPNode + '.u')
            cV = cmds.getAttr(currMeshCPNode + '.v')
            cmds.setAttr(nextMeshFollShp + '.parameterU', cU)
            cmds.setAttr(nextMeshFollShp + '.parameterV', cV)
            projPosCV = cmds.xform(nextMeshFoll, q = True, ws = True, t = True)
            
            
            if not zeroDistFound:
                if -0.25 <= projPosCV[0] <= 0.25 and -0.25 <= projPosCV[1] <= 0.25 and -0.25 <= projPosCV[2] <= 0.25:
                    zeroDistFound =  True
                    zeroPos = projPosCV
            
            if projPosCV == zeroPos:
                ncv = ncv - 1
                cmds.delete(sup + '.cv[' + str(cv) + ']')
                cvDeleted = True
                
            else:
                projPos.append(projPosCV)
                cmds.xform(sup + '.cv[' + str(cv) + ']', ws = True, t = projPosCV)
                cv = cv + 1
        
        if cvDeleted:
            projPos = []
            cmds.rebuildCurve(sup, ch = True, s = sp, d = dg)
            cmds.delete(sup, ch = True)
            
        
        
        cmds.xform(sup, piv =  cmds.xform(sup + '.cv[0]', q = True, ws = True, t = True))
        
    for h in historyDelete:
        if cmds.objExists(h):
            cmds.delete(h)        
        
               
    
def checkManualAllTime():
    
    import cPickle as Pickle
    currNode = cmds.getAttr('gbNode.currentGBNode')
    if not cmds.getAttr(currNode + '.useManualForGraph'):
        return
        
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    baseMeshGrp = cmds.getAttr(currNode + '.baseMeshGroup')
    baseMeshGrpChildren = cmds.listRelatives(baseMeshGrp, c = True)

    manualGrp = 'manualCurvesGrp_' + scalpMesh
    currManualCurves = []
    if manualGrp in baseMeshGrpChildren:
        currManualCurves = cmds.listRelatives(cmds.listRelatives(manualGrp, ad = True, typ = 'nurbsCurve'), p = True)
#        print 'currmanualcurves 13165', currManualCurves
        if not currManualCurves:
            currManualCurves = []
    
    usedManualCurvesString = cmds.getAttr(currNode + '.manualCurves')
    usedManualCurves = []
    usedManualCurvesPos = []
    if usedManualCurvesString:
        usedManualCurves = Pickle.loads(str(usedManualCurvesString))
        usedManualCurvesPos = Pickle.loads(str(cmds.getAttr(currNode + '.manualCurvesPos')))
    
    if not usedManualCurves and not currManualCurves:
        return        
        

    removedIpolFromGraph = []
    removedIpolFromGraphString = cmds.getAttr(currNode + '.removedIpolFromGraph')
    if removedIpolFromGraphString:
        removedIpolFromGraph = Pickle.loads(str(removedIpolFromGraphString))
    
                    
    addManual = list(set(currManualCurves) - set(usedManualCurves))
    addManual = list(set(addManual) - set(removedIpolFromGraph))
    
    remManual = list(set(usedManualCurves) - set(currManualCurves))
    commonManual = list(set(currManualCurves) & set(usedManualCurves))
#    print 'manualalltime'
#    print 'curr', currManualCurves
#    print 'used', usedManualCurves
#    print 'add', addManual
#    print 'rem', remManual
#    print 'comm', commonManual
    
    if commonManual:
        cmds.makeIdentity(commonManual, apply = True)
        for man in commonManual:
            usedPos = usedManualCurvesPos[usedManualCurves.index(man)]
            sp = cmds.getAttr(man +'.spans')
            dg = cmds.getAttr(man +'.degree') 
            ncv = sp + dg
            if not ncv == len(usedPos):
#                print ncv
#                print usedPos
#                print 'edit1', man
#                print 'cvs changed for', man
                addManual.append(man)
                remManual.append(man)
                continue
              
            for cv in range(ncv):
                currPos = cmds.xform(man + '.cv[' + str(cv) + ']', q = True, ws = True, t = True)
                dist = max([abs(a - b) for a, b in zip(currPos, usedPos[cv])])
                if dist > 0.15:
#                    print 'cv pos changed for', man, dist
#                if not  currPos == usedPos[cv]:
#                    print 'edit2', man, usedManualCurves.index(man)
#                    print 'cv', cv
#                    print 'curr', currPos
#                    print 'used', usedPos[cv]
                    addManual.append(man)
                    remManual.append(man)
                    break
    
    
            
    
    if remManual:
#        print 'REMOVE', remManual
        remove = 1
        
        delCurve = []
        delPos = []
        
        for rem in remManual:
            curveIndex = usedManualCurves.index(rem)
            delCurve.append(usedManualCurves[curveIndex])
            delPos.append(usedManualCurvesPos[curveIndex])
           
          
        for x in range(len(remManual)):
            usedManualCurves.remove(delCurve[x])
            usedManualCurvesPos.remove(delPos[x])

        removeCurvesFromGraph('names', remManual)
        
    if addManual:
        for man in addManual:
            usedManualCurves.append(man)
            sp = cmds.getAttr(man + '.spans')
            dg = cmds.getAttr(man + '.degree')
            ncv = sp + dg
            usedManualCurvesPos.append([cmds.xform(man + '.cv[' + str(cv) + ']', q = True, ws = True, t = True) for cv in range(ncv)])
    
        addCurvesForGraph(addManual, 'manual')  
#        print 'inside addmanual' , addManual      
#        cmds.setAttr(currNode + '.useManualForGraph', True)        
            
    manualCurvesString = Pickle.dumps(usedManualCurves)
    manualCurvesPosString = Pickle.dumps(usedManualCurvesPos)
    
    cmds.setAttr(currNode + '.manualCurves', manualCurvesString, type = 'string')
    cmds.setAttr(currNode + '.manualCurvesPos', manualCurvesPosString, type = 'string')        
    
#    print 'over to strips', remManual, addManual
    updateMeshStripsForGBFFCUpdates(remManual, addManual)
    updateMeshStripsForGBFFCUpdatesFromUI()
    
#    if addManual or remManual:
#        regenerateClumpFF()
        
            
def addIpolFromGraphUI():
    
    currNode = cmds.getAttr('gbNode.currentGBNode')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    ipol3dGrp = 'charInterpolation_' + scalpMesh
    baseMeshGrp = cmds.getAttr(currNode + '.baseMeshGroup')

    ipolExists = False
    if ipol3dGrp in cmds.listRelatives(baseMeshGrp, c = True):
        ipol3dGrpChildren = cmds.listRelatives(cmds.listRelatives(ipol3dGrp, ad = True, typ = 'nurbsCurve'), p = True)
        if ipol3dGrpChildren:
            ipolExists = True
#            print 'ipol exists'
    
    if not ipolExists:
        cmds.button('addIpolCurvesForGraphBtn', edit = True, vis = False)
        return            
            
    if cmds.getAttr(currNode + '.useIpolForGraph'):
        cmds.button('addIpolCurvesForGraphBtn', edit = True, vis = False)            

    if not cmds.getAttr(currNode + '.useIpolForGraph'):
        if ipolExists:
#            print 'add ipol btn'
            cmds.button('addIpolCurvesForGraphBtn', edit = True, vis = True)
                
        
            
def addIpolFrmGraphPage():
    
    ipolCurvesForVolume()
    cmds.button('addIpolCurvesForGraphBtn', edit = True, vis = False)
    
def snapSelectedToNearestVertex():
    
    selCurves = cmds.listRelatives(cmds.listRelatives(cmds.ls(sl = True), ad = True, typ = 'nurbsCurve'), p = True)
    if not selCurves:
        reportGBMessage('No Curves Selected', False, False, 'yellow')
    currNode = cmds.getAttr('gbNode.currentGBNode')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    paintMesh = cmds.getAttr(currNode + '.paintOnMesh')
    
    historyDelete = []
    scalpCPNode = createCPNode(scalpMesh)
    historyDelete.append(scalpCPNode)
    

    superCPNode = createCPNode(paintMesh)
    historyDelete.append(superCPNode)
    
    baseMeshGrp = cmds.getAttr(currNode + '.baseMeshGroup')
    
    found = False
    for crv in selCurves:
        prntGrp = cmds.listRelatives(crv, p = True) 
        if prntGrp == 'superCurves_charInterpolation_' + scalpMesh:
            if cmds.listRelatives(prntGrp, p = True) == baseMeshGrp:
                cpNode = superCPNode
                cpMesh = paintMesh            
        else:
            cpNode = scalpCPNode
            cpMesh = scalpMesh
            
        rootPos = cmds.xform(crv + '.cv[0]', q = True, ws = True, t = True)
        cmds.setAttr(cpNode + '.ip', rootPos[0],rootPos[1],rootPos[2])
        faceID = cmds.getAttr(cpNode + '.f')
        face = cpMesh + '.f[' + str(faceID) + ']'
        vtxList = cmds.ls(cmds.polyListComponentConversion(face, ff = True, tv = True), fl = True)
        
#        threshold = getThresholdByFace(face)
        per = cmds.floatField('drawAutoSnapThres', q = True, v = True)
        obj = cpMesh
        threshold = volumePercentByDistance(per,obj)
#        print 'threshold:', threshold
#        threshold = volumePercentByDistance(0.25, cpMesh)
        minDist = 0.0
        cpVtx = ''
        cpVtxPos = []
        found = False
        for vtx in vtxList:
            vtxPos = cmds.xform(vtx, q = True, ws = True, t = True)
            dist = distance3d(rootPos, vtxPos)
#            print 'dist: ' , dist, vtx
            if dist <= threshold:
                minDist = dist
                cpVtx = vtx
                cpVtxPos = vtxPos
                found = True
                
        if found:
            cmds.xform(crv + '.cv[0]', ws = True, t = cpVtxPos)                 
            cmds.xform(crv, piv = cpVtxPos)
            
        
    
    if not found:
        reportGBMessage('Curve(s) Root CV not close enough to vertex', False, True, 'red')        
        
        
    for h in historyDelete:
        if cmds.objExists(h):
            cmds.delete(h)
      
    
    

def getThresholdByFace(face):
    
    vtx = cmds.ls(cmds.polyListComponentConversion(face, ff = True, tv = True), fl = True)[:2]
    return distance3d(cmds.xform(vtx[0], q = True, ws = True, t = True), cmds.xform(vtx[1], q = True, ws = True, t = True)) * 0.05
    
def globalSliderChange():
    
    import cPickle as Pickle
    currNode = cmds.getAttr('gbNode.currentGBNode')
    
    curveList = Pickle.loads(str(cmds.getAttr(currNode + '.curveList4Graph')))
    toBeResize = convertCurveToIDList(curveList)
    toBeResizeString = Pickle.dumps(toBeResize)
    cmds.setAttr(currNode + '.toBeResize', toBeResizeString, type = 'string')


    
def showHideUI():
    
    if cmds.window('showHideGBWin', exists = True):
        cmds.deleteUI('showHideGBWin')
    cmds.window('showHideGBWin',rtf = True, width = 150, h = 50, title = 'Show / Hide Elements')
    
    cmds.columnLayout('mainShowHideLyt', adj = True)
    cmds.rowLayout('shAllLyt', nc = 3, p = 'mainShowHideLyt')
    cmds.button(label = 'Show All', c = 'showHideAllUI(True)', p = 'shAllLyt')
    cmds.button(label = 'Hide All', c = 'showHideAllUI(False)', p = 'shAllLyt')
    cmds.button(label = 'Refresh', c = 'refreshShowHideUI()', p = 'shAllLyt')
    cmds.setParent('..')
    cmds.rowLayout('markerScaleLyt', nc = 2, columnAlign2 = ['left', 'right'], ad2 = 2,  p = 'mainShowHideLyt')
    cmds.floatField('markerScaleField', s = 0.1, w = 35, pre = 2, v = 1.0, min = 0.01, max = 100, cc = 'markerScaleChanged()', p = 'markerScaleLyt')
    cmds.button(label = 'Toggle Root Markers', c = 'toggleRootPositionMarkers()', p = 'markerScaleLyt') 
    
    cmds.rowLayout('showDisplayOffsetLyt', nc = 2, columnAlign2 = ['left', 'right'], ad2 = 2,  p = 'mainShowHideLyt')
    currNode = cmds.getAttr('gbNode.currentGBNode')
    currDispOffset = cmds.getAttr(currNode + '.displayMeshOffset')
    cmds.floatField('displayOffsetField', s = 0.1, w = 35, pre = 2, v = currDispOffset, min = 0.01, max = 5.0, cc = 'showHideRefreshDisplayMesh()', p = 'showDisplayOffsetLyt')
    cmds.button(label = 'Display Mesh Offset %', c = 'showHideRefreshDisplayMesh()', p = 'showDisplayOffsetLyt') 
    
    getCurrentMarkerScale()
#    cmds.button(label = 'Toggle Root Markers', c = 'toggleRootPositionMarkers()', p = 'mainShowHideLyt') 
    
    cmds.rowColumnLayout(numberOfColumns=1, p = 'mainShowHideLyt')
    cmds.checkBox('shScalpChk', label = 'Scalp Mesh', vis = False, onc = 'showHide(\'scalpMesh\',True)', ofc = 'showHide(\'scalpMesh\',False)')
    cmds.checkBox('shVolumeChk', label = 'Volume Mesh',vis = False,onc = 'showHide(\'volumeMesh\',True)', ofc = 'showHide(\'volumeMesh\',False)')
    cmds.separator(style= 'in' )
    cmds.checkBox('shBulgesChk', label = 'Smart Volume Bulges',vis = False,onc = 'showHide(\'bulges\',True)', ofc = 'showHide(\'bulges\',False)')
    cmds.separator(style= 'in' )
    cmds.checkBox('shSuperChk', label = 'Super Curves',vis = False,onc = 'showHide(\'superCurves\',True)', ofc = 'showHide(\'superCurves\',False)')
    cmds.checkBox('shIpolChk', label = 'Interpolated Curves',vis = False,onc = 'showHide(\'ipol\',True)', ofc = 'showHide(\'ipol\',False)')
    cmds.checkBox('shManualChk', label = 'Freeform Curves',vis = False,onc = 'showHide(\'manual\',True)', ofc = 'showHide(\'manual\',False)')
    cmds.checkBox('shRoughChk', label = 'Rough Marker Curves',vis = False,onc = 'showHide(\'rough\',True)', ofc = 'showHide(\'rough\',False)')
    
    cmds.separator(style= 'in' )
    cmds.checkBox('shRegionChk', label = 'Region Based Controllers',vis = False,onc = 'showHide(\'region\',True)', ofc = 'showHide(\'region\',False)')
    
    cmds.separator(style= 'in' )
    cmds.checkBox('shMeshStripsChk', label = 'Mesh Strips',vis = False,onc = 'showHide(\'strips\',True)', ofc = 'showHide(\'strips\',False)')

    cmds.showWindow()
    
    
    
    refreshShowHideUI()
    
def refreshShowHideUI():
    
    showHide('scalpMesh', 'fetch')
    showHide('volumeMesh', 'fetch')
    showHide('bulges', 'fetch')
    showHide('superCurves', 'fetch')
    showHide('ipol', 'fetch')
    showHide('manual', 'fetch')
    showHide('rough', 'fetch')
    showHide('region', 'fetch')
    showHide('strips', 'fetch')
    

def showHideAllUI(value):
    
    all = cmds.lsUI(l = True, ctl = True)
    for a in all:
        if 'showHideGBWin' in a:
            if 'checkBox' in a:
                if cmds.checkBox(a, q = True, vis = True):
                    cmds.checkBox(a, edit = True, v = value)
                    
                
    showHide('scalpMesh', value)
    showHide('volumeMesh', value)
    showHide('bulges', value)
    showHide('superCurves', value)
    showHide('ipol', value)
    showHide('manual', value)
    showHide('rough', value)
    showHide('region', value)
    showHide('strips', value)


def showHide(element, value):
    
    currNode = cmds.getAttr('gbNode.currentGBNode')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    
    if element == 'scalpMesh':
        ind = cmds.tabLayout('mainTabs', query = True, sti = True)
        scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
        if ind == 1:
            scalpMesh = scalpMesh + '_DISPLAY'
            
        if cmds.objExists(scalpMesh):
            if value == 'fetch':
                cmds.checkBox('shScalpChk', edit = True, vis = True, v = cmds.getAttr(scalpMesh + '.visibility'))
            else:                
                cmds.setAttr(scalpMesh + '.visibility', value)
                cmds.checkBox('shScalpChk', edit = True, v = value)
    
    elif element == 'volumeMesh':
        volumeMesh = cmds.getAttr(currNode + '.volumeMesh')
        if cmds.objExists(volumeMesh):
            if value == 'fetch':
                cmds.checkBox('shVolumeChk', edit = True, vis = True, v = cmds.getAttr(volumeMesh + '.visibility'))
            else:                
                cmds.setAttr(volumeMesh + '.visibility', value)
                cmds.checkBox('shVolumeChk', edit = True, v = value)
            
    elif element == 'bulges':
        smartGrp = 'smartVolumeGrp_' + scalpMesh
        if cmds.objExists(smartGrp):
            bulgeGrp = 'bulges_' + scalpMesh
            if bulgeGrp in cmds.listRelatives(smartGrp, c = True):
                bulges = cmds.listRelatives(bulgeGrp, c = True)
                if bulges:
                    if value == 'fetch':
                        cmds.checkBox('shBulgesChk', edit = True, vis = True, v = cmds.getAttr(bulgeGrp + '.visibility'))
                    else:    
                        for bulge in bulges:
                            cmds.setAttr(bulge + '.visibility', True) 
                        cmds.setAttr(bulgeGrp + '.visibility', value)
                        cmds.checkBox('shBulgesChk', edit = True, v = value)
                                
    elif element == 'superCurves':
        baseGrp = cmds.getAttr(currNode + '.baseMeshGroup')
        superGrp = 'superCurves_charInterpolation_' + scalpMesh
        baseGrpChildren = cmds.listRelatives(baseGrp, c = True)
        if baseGrpChildren:
            if superGrp in baseGrpChildren:
                superGrpChildren = cmds.listRelatives(superGrp, c = True)
                if superGrpChildren:
                    if value == 'fetch':
                        cmds.checkBox('shSuperChk', edit = True, vis = True, v = cmds.getAttr(superGrp + '.visibility'))
                    else:
                        for super in superGrpChildren:
                            cmds.setAttr(super + '.visibility', True)
                        cmds.setAttr(superGrp + '.visibility', value)                            
                        cmds.checkBox('shSuperChk', edit = True, v = value)
    
    elif element == 'ipol':
        baseGrp = cmds.getAttr(currNode + '.baseMeshGroup')
        ipolGrp = 'charInterpolation_' + scalpMesh
        baseGrpChildren = cmds.listRelatives(baseGrp, c = True)
        if baseGrpChildren:
            if ipolGrp in baseGrpChildren:
                ipolGrpChildren = cmds.listRelatives(ipolGrp, c = True)
                if ipolGrpChildren:
                    if value == 'fetch':
                        cmds.checkBox('shIpolChk', edit = True, vis = True, v = cmds.getAttr(ipolGrp + '.visibility'))
                    else:
                        for ipol in ipolGrpChildren:
                            cmds.setAttr(ipol + '.visibility', True)
                        cmds.setAttr(ipolGrp + '.visibility', value) 
                        cmds.checkBox('shIpolChk', edit = True, v = value)
    
                                                       
    elif element == 'manual':
        baseGrp = cmds.getAttr(currNode + '.baseMeshGroup')
        manualGrp = 'manualCurvesGrp_' + scalpMesh
        baseGrpChildren = cmds.listRelatives(baseGrp, c = True)
        if baseGrpChildren:
            if manualGrp in baseGrpChildren:
                manualGrpChildren = cmds.listRelatives(manualGrp, c = True)
                if manualGrpChildren:
                    if value == 'fetch':
                        cmds.checkBox('shManualChk', edit = True, vis = True, v = cmds.getAttr(manualGrp + '.visibility'))
                    else:
                        for manual in manualGrpChildren:
                            cmds.setAttr(manual + '.visibility', True)
                        cmds.setAttr(manualGrp + '.visibility', value) 
                        cmds.checkBox('shManualChk', edit = True, v = value)
                                                          
    
    elif element == 'rough':
        baseMeshGrp = cmds.getAttr(currNode + '.baseMeshGroup')
        roughGrp = 'roughMarkingCurvesGrp_' + scalpMesh
        baseMeshGrpChildren = cmds.listRelatives(baseMeshGrp, c = True)
        if baseMeshGrpChildren:
            if roughGrp in baseMeshGrpChildren:
                if value == 'fetch':
                    cmds.checkBox('shRoughChk', edit = True, vis = True, v = cmds.getAttr(roughGrp + '.visibility'))
                else:
                    cmds.setAttr(roughGrp + '.visibility', value)
                    cmds.checkBox('shRoughChk', edit = True, v = value)
        
        
        
    
    elif element == 'region':
        mainGrp = cmds.getAttr(currNode + '.mainGroup')
        regionGrp = 'regionControlGrp_' + scalpMesh
        mainGrpChildren = cmds.listRelatives(mainGrp, c = True)
        if mainGrpChildren:
            if regionGrp in mainGrpChildren:
                regionGrpChildren = cmds.listRelatives(regionGrp, c = True)
                if regionGrpChildren:
                    if value == 'fetch':
                        cmds.checkBox('shRegionChk', edit = True, vis = True, v = cmds.getAttr(regionGrp + '.visibility'))
                    else:
                        for region in regionGrpChildren:
                            cmds.setAttr(region + '.visibility', True)
                        cmds.setAttr(regionGrp + '.visibility', value)        
                        cmds.checkBox('shRegionChk', edit = True, v = value)
                        
    elif element == 'strips':
        stripVis = False
        stripGrp = getCurrentMeshStripGroup()
        if stripGrp:
            stripVis = True
            if value == 'fetch':
                cmds.checkBox('shMeshStripsChk', edit = True, vis = True, v = cmds.getAttr(stripGrp + '.visibility'))
            else:
                cmds.setAttr(stripGrp + '.visibility', value)
                cmds.checkBox('shMeshStripsChk', edit = True, v = value)
                                
                
def moveRegionControlExec():
    
    stopGBUndo()
    interactiveRegionGraphUpdateOFF()
    
    currNode = cmds.getAttr('gbNode.currentGBNode')
    import cPickle as Pickle
    
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    regionGrp = 'regionControlGrp_' + scalpMesh
    regionGrpChildren = []
    if cmds.objExists(regionGrp):
        regionGrpChildren = cmds.listRelatives(regionGrp, c = True)        
	if not regionGrpChildren:
	    reportGBMessage('No Region Controller Exists', True, True, 'red')
    
    
    sel = cmds.ls(sl = True)
    if not sel:
        reportGBMessage('Please select Region Controller first', True, True, 'red')

          
    regionCtrl = []
#    print sel
    for s in sel:
        if s in regionGrpChildren:
            regionCtrl.append(s)
#    print regionCtrl
    if not regionCtrl:
        reportGBMessage('No Region Controller Selected', True, True, 'red')
    
    region = regionCtrl[0]            
    cmds.select(region, r = True)
    cmds.setAttr(currNode + '.regionMoved', region, type = 'string')
    loadGraphFromSelControl()
    paintRegionControlExec()
    startGBUndo()
    
            
def launchScaleCurvatureOLD():
    
    if cmds.window('scaleCurvatureGBWin', exists = True):
        cmds.deleteUI('scaleCurvatureGBWin')
    cmds.window('scaleCurvatureGBWin',rtf = True, width = 150, h = 50, title = 'Scale Curvature')
    
    cmds.columnLayout('mainShowHideLyt', adj = True)
    cmds.button(label = 'Update Scale Curvature on Selected Curves', c = 'updateScaleCurvature()')
    cmds.floatSliderGrp('scaleXCurvatureSlider', field = True, label = 'Curvature Intensity X', minValue = -15.0, maxValue = 15.0, fieldMinValue = -360, fieldMaxValue = 360, value = 0.0, fs = 5, ss = 5) 
    cmds.floatSliderGrp('scaleYCurvatureSlider', field = True, label = 'Curvature Intensity Y', minValue = -15.0, maxValue = 15, fieldMinValue = -360, fieldMaxValue = 360, value = 0.0, fs = 5, ss = 5) 
    cmds.floatSliderGrp('scaleZCurvatureSlider', field = True, label = 'Curvature Intensity Z', minValue = -15.0, maxValue = 15, fieldMinValue = -360, fieldMaxValue = 360, value = 0.0, fs = 5, ss = 5) 
    cmds.floatSliderGrp('scaleXCurvatureSlider', edit = True, cc = 'updateScaleCurvature()')
    cmds.floatSliderGrp('scaleYCurvatureSlider', edit = True, cc = 'updateScaleCurvature()')
    cmds.floatSliderGrp('scaleZCurvatureSlider', edit = True, cc = 'updateScaleCurvature()')
    cmds.gradientControlNoAttr('scaleCurvatureGraph', asString = '0,0,3,1,1,3', h = 100, cc = 'updateScaleCurvature()')
    cmds.showWindow('scaleCurvatureGBWin')
    
def updateScaleCurvatureOLD():
    
    import cPickle as Pickle
    selCurves = cmds.listRelatives(cmds.listRelatives(cmds.ls(sl = True), ad = True, typ = 'nurbsCurve'), p = True)
    if not selCurves:
        reportGBMessage('No Curves Selected', True, True, 'red')
    currNode = cmds.getAttr('gbNode.currentGBNode')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    
    curveList4GraphString = cmds.getAttr(currNode + '.curveList4Graph')
    curveList4Graph = Pickle.loads(str(curveList4GraphString))
    volumeResizePos = Pickle.loads(str(cmds.getAttr(currNode + '.volumeResizePos')))
    cvCountL = Pickle.loads(str(cmds.getAttr(currNode + '.cvCountL'))) 
    volumePos = Pickle.loads(str(cmds.getAttr(currNode + '.closestPointPos')))
    
    historyDelete = []
    charCPNode = createCPNode(scalpMesh)
    historyDelete.append(charCPNode)
    
    
    
    rx = cmds.floatSliderGrp('scaleXCurvatureSlider', q = True, v = True)
    ry = cmds.floatSliderGrp('scaleYCurvatureSlider', q = True, v = True)
    rz = cmds.floatSliderGrp('scaleZCurvatureSlider', q = True, v = True)
    
    for crv in selCurves:
        ind = curveList4Graph.index(crv)
        for cv in range(cvCountL[ind]):
            cmds.xform(crv + '.cv[' + str(cv) + ']', ws = True, t = volumeResizePos[ind][cv])
    
    for crv in selCurves:
        
        p0 = cmds.pointOnCurve(crv, pr = 0.0, p = True)
        pA = cmds.pointOnCurve(crv, pr = 0.5, p = True)
#        cmds.setAttr(charCPNode + '.ip', pA[0], pA[1], pA[2])
#        pB = list(cmds.getAttr(charCPNode + '.p')[0])
        pB = volumePos[curveList4Graph.index(crv)][0]
        dA = [(c - d) for c, d in zip(pA,p0)] 
        dB = [(c - d) for c, d in zip(pB,p0)] 
        uA = mm.eval('unit <<' + str(dA[0]) + ',' + str(dA[1]) + ',' + str(dA[2]) + '>>')
        uB = mm.eval('unit <<' + str(dB[0]) + ',' + str(dB[1]) + ',' + str(dB[2]) + '>>')
        tRot = cmds.angleBetween(euler = True, v1=uA, v2=uB)
#        print tRot
        
#        cmds.rotate(tRot[0], tRot[1], tRot[2], dupCrv, r = True)
        
        
        sp = cmds.getAttr(crv + '.spans')
        dg = cmds.getAttr(crv + '.degree')
        ncv = sp + dg
        for cv in range(ncv):
            

#            op1 = cmds.gradientControlNoAttr('scaleCurvatureGraph',q = True, vap = perCV)
#            rot = [x * op1 for x in [rx,ry,rz]]
            rot = [rx,ry,rz]
            ind = curveList4Graph.index(crv)
            piv = volumeResizePos[ind][ncv-cv-1]
            cmds.xform(crv + '.cv[' + str(ncv-cv-1) + ':' + str(ncv-1) + ']', r = True, ra = tRot, ro = rot, rp = piv, os = True)


def launchScaleCurvature():
    
    ind = cmds.tabLayout('mainTabs', query = True, sti = True)
    if ind == 1:
        reportGBMessage('Scale Curvature is available in Adjust Volume Tab only', True, True, 'red')
    if cmds.window('scaleCurvatureGBWin', exists = True):
        cmds.deleteUI('scaleCurvatureGBWin')
    cmds.window('scaleCurvatureGBWin',rtf = True, width = 150, h = 50, title = 'Scale Curvature')
    
    cmds.columnLayout('mainShowHideLyt', adj = True)
    cmds.button(label = 'Restore back' , c = 'restoreBackSelectedResize()')
    cmds.button(label = 'Update Scale Curvature on Selected Curves - Absolute', c = 'updateScaleCurvature()')
    cmds.button(label = 'Update Scale Curvature on Selected Curves - Relative', c = 'updateOnlyScaleCurvature()')
    cmds.floatSliderGrp('scaleFactorSlider', field = True, label = 'Scale Factor', minValue = 0.0, maxValue = 1.0, fieldMinValue = 0.0, fieldMaxValue = 10, value = 1.0 ) 
    cmds.floatSliderGrp('scaleFactorSlider', edit = True, pre = 3, cc = 'updateScaleCurvature()')
    cmds.floatSliderGrp('scaleRootTipSlider', field = True, label = 'Root To Tip Control', minValue = 0.0, maxValue = 1.0, value = 0.0 )     
    cmds.floatSliderGrp('scaleRootTipSlider', edit = True, cc = 'updateScaleCurvature()')
    cmds.checkBox('scaleTextureCheck', label = 'Apply as per Texture')
    cmds.showWindow('scaleCurvatureGBWin')            


def restoreBackSelectedResize():
    
    ind = cmds.tabLayout('mainTabs', query = True, sti = True)
    if ind == 1:
        reportGBMessage('Scale Curvature is available in Adjust Volume Tab only', True, True, 'red')
    
    import cPickle as Pickle
    mainSelection = cmds.ls(sl = True)
    if not mainSelection:
        reportGBMessage('No Curves Selected', True, True, 'red')
        
    selCurves = cmds.listRelatives(cmds.listRelatives(cmds.ls(sl = True), ad = True, typ = 'nurbsCurve'), p = True)
    if not selCurves:
        cmds.select(mainSelection, r = True)
        reportGBMessage('No Curves Selected', True, True, 'red')
    currNode = cmds.getAttr('gbNode.currentGBNode')

    r2t = cmds.floatSliderGrp('scaleRootTipSlider', q = True, v = True)
    factor = cmds.floatSliderGrp('scaleFactorSlider', q = True, v = True)
    
    
    curveList4Graph = Pickle.loads(str(cmds.getAttr(currNode + '.curveList4Graph')))
    volumeResizePos = Pickle.loads(str(cmds.getAttr(currNode + '.volumeResizePos')))
    cvCountL = Pickle.loads(str(cmds.getAttr(currNode + '.cvCountL'))) 
    
    for crv in selCurves:
        ind = curveList4Graph.index(crv)
        ncv = cvCountL[ind]
        for cv in range(ncv):
            cmds.xform(crv + '.cv[' + str(cv) + ']', ws = True, t = volumeResizePos[ind][cv])

    
def updateScaleCurvature():
    
    ind = cmds.tabLayout('mainTabs', query = True, sti = True)
    if ind == 1:
        reportGBMessage('Scale Curvature is available in Adjust Volume Tab only', True, True, 'red')


    import cPickle as Pickle
    mainSelection = cmds.ls(sl = True)
    texture = cmds.checkBox('scaleTextureCheck', q = True, v = True)
    if not texture:
        if not mainSelection:
            reportGBMessage('No Curves Selected', True, True, 'red')
        selCurves = cmds.listRelatives(cmds.listRelatives(cmds.ls(sl = True), ad = True, typ = 'nurbsCurve'), p = True)
        if not selCurves:
            cmds.select(mainSelection, r = True)
            reportGBMessage('No Curves Selected', True, True, 'red')

    currNode = cmds.getAttr('gbNode.currentGBNode')

    r2t = cmds.floatSliderGrp('scaleRootTipSlider', q = True, v = True)
    factor = cmds.floatSliderGrp('scaleFactorSlider', q = True, v = True)
    
            
    curveList4Graph = Pickle.loads(str(cmds.getAttr(currNode + '.curveList4Graph')))
    volumeResizePos = Pickle.loads(str(cmds.getAttr(currNode + '.volumeResizePos')))
    cvCountL = Pickle.loads(str(cmds.getAttr(currNode + '.cvCountL'))) 
    
    
    if texture:
        grayShades = []
        shades = 10
        for i in range(shades):
            grayShades.append([])
        cvUV = Pickle.loads(str(cmds.getAttr(currNode + '.cvUV')))
        texture = getScalpMeshTextureNode()
        if not texture:
            reportGBMessage('No Texture assigned to Scalp Mesh Shader', True, True, 'red')
            
        for crv in range(len(curveList4Graph)):
            currRGB = cmds.colorAtPoint(texture, o = 'RGB', u = cvUV[crv][0], v = cvUV[crv][1])
            totalRGB =  currRGB[0] + currRGB[1] + currRGB[2]
            ncv = cvCountL[crv]
            for cv in range(ncv):
                cmds.xform(curveList4Graph[crv] + '.cv[' + str(cv) + ']', ws = True, t = volumeResizePos[crv][cv])
            if totalRGB == 0.0:
                continue
            currShade = int(round(remap(0,shades-1,0.0,3.0, totalRGB)))
#            print curveList4Graph[crv], cvUV[crv], totalRGB, currShade                
            if r2t == 0.0:
#                cmds.select(curveList4Graph[crv], add = True)
                grayShades[currShade].append(curveList4Graph[crv])
            else:
                startCV = int(r2t * (ncv-1))
                grayShades[currShade].append(curveList4Graph[crv] + '.cv[' + str(startCV) + ':' + str(str(ncv-1)) + ']')
#                cmds.select(curveList4Graph[crv] + '.cv[' + str(startCV) + ':' + str(str(ncv-1)) + ']', add = True)
        
        for x in range(shades):
            if grayShades[x]:
                cmds.select(grayShades[x], r = True)
#                cmds.scale(x,x,x)
                currFactor = remap(1.0,factor,0,shades-1,x)
#                print currFactor
                cmd = 'modifySelectedCurves curvature ' + str(currFactor) + ' 1.0;'
                mm.eval(cmd)    
#        for x in range(shades):
#            print grayShades[x]
        cmds.select(cl = True)                
            
        
    if not texture:
        cmds.select(cl = True)
        for crv in selCurves:
            ind = curveList4Graph.index(crv)
            ncv = cvCountL[ind]
            for cv in range(ncv):
                cmds.xform(crv + '.cv[' + str(cv) + ']', ws = True, t = volumeResizePos[ind][cv])
            if r2t == 0.0:
                cmds.select(crv, add = True)
            else:
                startCV = int(r2t * (ncv-1))
                cmds.select(crv + '.cv[' + str(startCV) + ':' + str(str(ncv-1)) + ']', add = True)
        
        cmd = 'modifySelectedCurves curvature ' + str(factor) + ' 1.0;'
        mm.eval(cmd)    
        cmds.select(mainSelection, r = True)                             

def updateOnlyScaleCurvature():
    
    ind = cmds.tabLayout('mainTabs', query = True, sti = True)
    if ind == 1:
        reportGBMessage('Scale Curvature is available in Adjust Volume Tab only', True, True, 'red')



    import cPickle as Pickle

    mainSelection = cmds.ls(sl = True)
    selCurves = cmds.listRelatives(cmds.listRelatives(cmds.ls(sl = True), ad = True, typ = 'nurbsCurve'), p = True)
    if not selCurves:
        cmds.select(mainSelection, r = True)
        reportGBMessage('No Curves Selected', True, True, 'red')
    currNode = cmds.getAttr('gbNode.currentGBNode')

    curveList4Graph = Pickle.loads(str(cmds.getAttr(currNode + '.curveList4Graph')))
    cvCountL = Pickle.loads(str(cmds.getAttr(currNode + '.cvCountL'))) 

        
    r2t = cmds.floatSliderGrp('scaleRootTipSlider', q = True, v = True)
    factor = cmds.floatSliderGrp('scaleFactorSlider', q = True, v = True)
    
 
    cmds.select(cl = True)

    for crv in selCurves:
        ind = curveList4Graph.index(crv)
        ncv = cvCountL[ind]
        if r2t == 0.0:
            cmds.select(crv, add = True)
        else:
            startCV = int(r2t * (ncv-1))
            cmds.select(crv + '.cv[' + str(startCV) + ':' + str(str(ncv-1)) + ']', add = True)
    
    cmd = 'modifySelectedCurves curvature ' + str(factor) + ' 1.0;'
    mm.eval(cmd)    
    cmds.select(mainSelection, r = True)                             


def backupSetupForGB():
    
    tr = cmds.radioButtonGrp('textRegionRadioGrp', q = True, select = True)                                     
    desc = cmds.textFieldGrp('bkpDesc', q = True, text = True)
    if not desc:
        reportGBMessage('Please enter Description for this backup', True, True, 'red')
    
    if tr == 1:
        textureBackupForGB(desc)
    else:
        regionBackupForGB(desc)


def textureBackupForGB(desc):
    
    import cPickle as Pickle
    import shutil
    import os
    
    currNode = cmds.getAttr('gbNode.currentGBNode')
    rgbGraphs = []
    rgbGraphsString = cmds.getAttr(currNode + '.rgbGraphs')
    if rgbGraphsString:
        rgbGraphs = Pickle.loads(str(rgbGraphsString))
    
    if not rgbGraphs:
        reportGBMessage('Texture Based Control is not used yet', True, True, 'red')
    
    returnValue = bkpSetupFolderCreate('texture')        
    setupDir = returnValue[0]
    bkpPrefix = returnValue[1]
    bkpFolder = setupDir + '/' + bkpPrefix
    
    texture = getScalpMeshTextureNode()
    if cmds.nodeType(texture) == 'file':
        texturePath = cmds.getAttr(texture + '.fileTextureName')
        shutil.copy(texturePath, bkpFolder)    
    
    dupText = cmds.duplicate(texture, n = bkpPrefix + '_color', ic = True, rc = True)[0]
    if cmds.nodeType(texture) == 'file':
        dupFile = bkpFolder + '/' + os.path.basename(texturePath)
        cmds.setAttr(dupText + '.fileTextureName', dupFile, type = 'string')
    
    graphNode = createBkpGraphsNode(bkpPrefix)        
#    createDescFile(desc)    
    descFile = bkpFolder + '/' + bkpPrefix + '_desc.txt'
    f = open(descFile, 'w')
    f.write(desc)
    f.close()
    
#    bkpDir = cmds.workspace(rd = True, q = True) + 'groomBoy/backup/' + displayName 
    toBeExport = [graphNode, dupText]
    cmds.select(toBeExport , r = True)
    cmds.file( bkpFolder + '/' + bkpPrefix, force = True, options = 'v=0', typ = 'mayaBinary', es = True)
    cmds.delete(toBeExport)
    print ('Backup Folder Path: ' + bkpFolder)
        

def bkpSetupFolderCreate(mode):
    
    import os
    currNode = cmds.getAttr('gbNode.currentGBNode')
    displayName = cmds.getAttr(currNode + '.displayName')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    
    projDirectory = cmds.workspace(rd = True, q = True)
    gbDir = projDirectory + 'groomBoy'
    bkpDir = gbDir + '/backup'
    dispDir = bkpDir + '/' + displayName
    setupDir = dispDir + '/' + mode + '_' + displayName 
    bkpPrefix = mode + '_' + displayName
 
    
    if not os.path.exists(gbDir):
        os.makedirs(gbDir)
        os.makedirs(bkpDir)
        os.makedirs(dispDir)
        os.makedirs(setupDir)
        bkpPrefix = bkpPrefix + '_1'
        
    else:
        if not os.path.exists(bkpDir):
            os.makedirs(bkpDir)
            os.makedirs(dispDir)
            os.makedirs(setupDir)
            bkpPrefix = bkpPrefix + '_1'
            
        else:
            if not os.path.exists(dispDir):
                os.makedirs(dispDir)
                os.makedirs(setupDir)
                bkpPrefix = bkpPrefix + '_1'
            
            else:
                if not os.path.exists(setupDir):
                    os.makedirs(setupDir)   
                    bkpPrefix = bkpPrefix + '_1' 

                else:
#                    print 'here'
                    max = 0
                    bkpPrefix = bkpPrefix + '_'
#                    subDirs = [x[0] for x in os.walk(setupDir)][1:]
                    subDirs = os.walk(setupDir).next()[1]
                    for x in subDirs:
                        if os.path.isdir(setupDir + '/' + x):
                            if bkpPrefix in x:
                                suffix = x.split(bkpPrefix)[1]
#                                print suffix
                                if suffix.isdigit():
                                    suffix = int(suffix)
                                    if suffix > max:
                                        max = suffix
                    bkpPrefixT = bkpPrefix + str(max+1) 
#                    print bkpPrefixT
                    if cmds.objExists(bkpPrefixT):
                        while cmds.objExists(bkpPrefixT):
                            max = max + 1
                            bkpPrefixT = bkpPrefix + str(max)
                    bkpPrefix = bkpPrefixT                        
    
    os.makedirs(setupDir + '/' + bkpPrefix)
    return [setupDir, bkpPrefix]
        
    
def createBkpGraphsNode(bkpName):
    
    currNode = cmds.getAttr('gbNode.currentGBNode')
    nwNode = cmds.createNode('network', ss = True, name = bkpName)    
    cmds.addAttr(nwNode, ln = 'rgbGraphs', dt = 'string')
    cmds.addAttr(nwNode, ln = 'defaultGraph', dt = 'string')    
    
    cmds.setAttr(nwNode + '.rgbGraphs', cmds.getAttr(currNode + '.rgbGraphs'), type = 'string')
    cmds.setAttr(nwNode + '.defaultGraph', cmds.getAttr(currNode + '.defaultGraph'), type = 'string')
    
    return nwNode
    
def regionBackupForGB(desc):
    
    import cPickle as Pickle
    import shutil
    import os
    
    currNode = cmds.getAttr('gbNode.currentGBNode')
    regionCtrlName = []
    regionCtrlNameString = cmds.getAttr(currNode + '.regionCtrlName')
    
    if regionCtrlNameString:
        regionCtrlName = Pickle.loads(str(regionCtrlNameString))
    
    if not regionCtrlName:
        reportGBMessage('Region Based Control is not used yet', True, True, 'red')
    
    returnValue = bkpSetupFolderCreate('region')        
    setupDir = returnValue[0]
    bkpPrefix = returnValue[1]
    bkpFolder = setupDir + '/' + bkpPrefix
    
    regionNode = createBkpRegionNode(bkpPrefix) 
    
    descFile = bkpFolder + '/' + bkpPrefix + '_desc.txt'
    f = open(descFile, 'w')
    f.write(desc)
    f.close()
    
    toBeExport = [regionNode]
    cmds.select(toBeExport , r = True)
    cmds.file( bkpFolder + '/' + bkpPrefix, force = True, options = 'v=0', typ = 'mayaBinary', es = True)
    cmds.delete(toBeExport)
    print ('Backup Folder Path: ' + bkpFolder)
        
        
def createBkpRegionNodeOLD(bkpPrefix):
    
    currNode = cmds.getAttr('gbNode.currentGBNode')
    nwNode = cmds.createNode('network', ss = True, name = bkpPrefix)    
    cmds.addAttr(nwNode, ln = 'regionCtrlName', dt = 'string')
    cmds.addAttr(nwNode, ln = 'regionCtrlGraph', dt = 'string')    
    
    cmds.setAttr(nwNode + '.regionCtrlName', cmds.getAttr(currNode + '.regionCtrlName'), type = 'string')
    cmds.setAttr(nwNode + '.regionCtrlGraph', cmds.getAttr(currNode + '.regionCtrlGraph'), type = 'string')
    
    
    return nwNode

def createBkpRegionNode(bkpPrefix):
    
    import cPickle as Pickle
    currNode = cmds.getAttr('gbNode.currentGBNode')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    nwNode = cmds.createNode('network', ss = True, name = bkpPrefix) 
    cmds.addAttr(nwNode, ln = 'regionCtrlPos', dt = 'string')
    cmds.addAttr(nwNode, ln = 'regionCtrlGraph', dt = 'string')
    
    regionCtrlName = Pickle.loads(str(cmds.getAttr(currNode + '.regionCtrlName')))
    regionCtrlPos = []
    for region in regionCtrlName:
        regionCtrlPos.append(cmds.xform(scalpMesh + '.f[' + str(region.split(scalpMesh + '_regionCtrl_')[1]) + ']', q = True, ws = True, t = True))
        
    regionCtrlPosString = Pickle.dumps(regionCtrlPos)
    cmds.setAttr(nwNode + '.regionCtrlPos', regionCtrlPosString, type = 'string')
    cmds.setAttr(nwNode + '.regionCtrlGraph', cmds.getAttr(currNode + '.regionCtrlGraph'), type = 'string')
    
    return nwNode
    
        
        
def restoreTextureSetup():
    
    if cmds.radioButtonGrp('bkpResRadioGrp', q = True, select = True) == 1:
        return 
        
    currNode = cmds.getAttr('gbNode.currentGBNode')
    
    restorePath = cmds.textFieldButtonGrp('restorePathText', q = True, tx = True)
    if restorePath:
        setupDir = restorePath
    else:    
        setupDir = getSetupFolderToRestore('texture')
    
    backupPath = getBackupFromSetupDir(setupDir)
    if not backupPath:
        reportGBMessage('No Backups Found', True, True, 'red')
    
            
def restoreRegionSetup():

    if cmds.radioButtonGrp('bkpResRadioGrp', q = True, select = True) == 1:
        return 
    
    currNode = cmds.getAttr('gbNode.currentGBNode')
    
    restorePath = cmds.textFieldButtonGrp('restorePathText', q = True, tx = True)
    if restorePath:
        setupDir = getSetupFromRestorePath(restorePath)
    else:    
        setupDir = getSetupFolderToRestore('region')
    
    backupPath = getBackupFromSetupDir(setupDir)
    if not backupPath:
        reportGBMessage('No Backups Found', True, True, 'red')

def getSetupFromRestorePath(restorePath):
    
    return restorePath
    
#    import os
#    childDirs = [x[0] for x in os.walk(restorePath)]
#    if childDirs:
#       for dir in childDirs:
#           if dir.split('\\')[-2] == 'groomBoy' and dir.split('\\')[-1] == 'backup':
#                if 'region' dir.split('\\')[-1]                
#                    print dir
            
    
            
def getSetupFolderToRestore(mode):

    import os
    currNode = cmds.getAttr('gbNode.currentGBNode')    
    displayName = cmds.getAttr(currNode + '.displayName')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    
    projDirectory = cmds.workspace(rd = True, q = True)
    gbDir = projDirectory + 'groomBoy'
    bkpDir = gbDir + '/backup'
    dispDir = bkpDir + '/' + displayName
    setupDir = dispDir + '/' + mode + '_' + displayName                 
    
    return setupDir

def checkPathForRestore():
    
    import os
    
    mode = cmds.radioButtonGrp('textRegionRadioGrp', q = True, select = True)
    restorePath = cmds.textFieldButtonGrp('restorePathText', q = True, tx = True)
    default = False
    if not restorePath:
        default = True
        
    if '\\' in restorePath:
        restorePath = restorePath.replace('\\','/')
        
    if not os.path.exists(restorePath) and not default:
        reportGBMessage('Entered Path does not exist', True, True, 'red')
        return False
    else:
        if mode == 1:
            restoreTextureSetup()
        else:
            restoreRegionSetup()            

        return True

def getBackupFromSetupDir(setupDir):
    
    import os
    
    mode = cmds.radioButtonGrp('textRegionRadioGrp', q = True, select = True)
    if mode == 1:
        search = 'texture_'
    else:
        search = 'region_'        
    
    pathDirs = setupDir.split('/')
    if len(pathDirs) > 3:
        if pathDirs[-2] == 'backup' and pathDirs[-3] == 'groomBoy':
            subDirs = os.walk(setupDir).next()[1]
            for sub in subDirs:
                if search in sub:
                    setupDir = setupDir + '/' + sub
                    
           
    subDirs = os.walk(setupDir).next()[1]
    pathDirs = setupDir.split('/')
    if len(pathDirs) > 2:
        subDirs.append(pathDirs[-1])
        subDirs.append(pathDirs[-2])        
        
    cmds.textScrollList('restoreScrollList', edit = True, removeAll = True) 
    backupPath = []
    for subD in subDirs:
        if search in subD:
            if os.path.isdir(setupDir + '/' + subD):
                files = os.listdir(setupDir + '/' + subD)
                if subD + '.mb' in files:
#                    cmds.textFieldButtonGrp('restorePathText', edit = True, tx = setupDir + '/' + subD)
                    cmds.textScrollList('restoreScrollList', edit = True, a = subD)
                    backupPath.append(setupDir + '/' + subD)
            
    return backupPath


def backupToRestoreSelected():
    
    import os
    import time
    
    [finalPath, currBackup, currControl] = getSelectedBackupDetail()
    descFile = finalPath + '/' + currBackup + '_desc.txt'
    mayaFile = finalPath + '/' + currBackup + '.mb'
    desc = 'No Description Found'
    
    if os.path.isfile(descFile):
        f = open(descFile, 'r')
        desc = f.read()
    
    
    lastDate = time.ctime(os.path.getmtime(mayaFile))
    cmds.text('restoreDesc', edit = True, label = desc)
    cmds.text('restoreModifiedDate', edit = True, label = lastDate)
    
def getSelectedBackupDetail():
    
    import os

    cmds.textScrollList('restoreScrollList', q = True, ai = True)
    currBackup = cmds.textScrollList('restoreScrollList', q = True, si = True)[0]
    restorePath = cmds.textFieldButtonGrp('restorePathText', q = True, tx = True)
    mode = cmds.radioButtonGrp('textRegionRadioGrp', q = True, select = True)

    if mode == 1:
        currControl = 'texture'
    else:
        currControl = 'region'

    if restorePath:
        setupDir = restorePath
        subDirs = os.listdir(setupDir)
        for dir in subDirs:
            if currControl in dir:
                setupDir = setupDir + '/' + dir
                break
#        subDirs = os.walk(restorePath).next()[1]
#        if subDirs:
#            if currControl in subDirs:
#                setupDir = os.walk(restorePath).next()[0]
    else:
        setupDir = getSetupFolderToRestore(currControl)            
            
    finalPath = setupDir + '/' + currBackup
    return [finalPath, currBackup, currControl]
                                            
def restoreSetupForGB():
    
    option = cmds.confirmDialog( title='Overwrite Current Setup', message='Existing Setup will not be available once Selected Setup is restored?', button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No' )
    if option == 'No':
        return
    
    [finalPath, currBackup, currControl] = getSelectedBackupDetail()
    mayaFile = finalPath + '/' + currBackup + '.mb' 
    
    if currControl == 'texture':
        execRestoreTextureSetup(finalPath, currBackup)
    else:
        execRestoreRegionSetup(finalPath, currBackup)
        
    autoResize()
    
def execRestoreTextureSetup(finalPath, currBackup):
    
    currNode = cmds.getAttr('gbNode.currentGBNode')
    mayaFile = finalPath + '/' + currBackup + '.mb'
    scalpShader = getShaderNames()[0]
    cmds.file(mayaFile, i = True, ignoreVersion = True)
    
    allTextures = cmds.ls(textures = True)
    for texture in allTextures:
        if currBackup in texture:
            cmds.connectAttr(texture + '.outColor', scalpShader + '.color', force = True)
            break
    
    networkNodes = cmds.ls(type = 'network')
    for node in networkNodes:
        if currBackup in node:
            newRGBGraphs = cmds.getAttr(node + '.rgbGraphs')
            newDefaultGraph = cmds.getAttr(node + '.defaultGraph')
            break
            
    cmds.setAttr(currNode + '.rgbInfo','',type = 'string')            
    cmds.setAttr(currNode + '.rgbPerList','',type = 'string')
    cmds.setAttr(currNode + '.rgbCurves','',type = 'string')
    cmds.setAttr(currNode + '.texPathTime','',type = 'string')
    
    cmds.setAttr(currNode + '.rgbGraphs',newRGBGraphs, type = 'string')
    cmds.setAttr(currNode + '.defaultGraph',newDefaultGraph, type = 'string')
    
    cmds.delete(node)
    
    colorBasedGraphSelected()
    
    
    
def execRestoreRegionSetupOLD(finalPath, currBackup): 
    
    import cPickle as Pickle
    currNode = cmds.getAttr('gbNode.currentGBNode')
    
    mayaFile = finalPath + '/' + currBackup + '.mb'
    
    cmds.file(mayaFile, i = True, ignoreVersion = True)
    
    networkNodes = cmds.ls(type = 'network')
    for node in networkNodes:
        if currBackup in node:
            regionCtrlNameString = cmds.getAttr(node + '.regionCtrlName')
            regionCtrlGraphString = cmds.getAttr(node + '.regionCtrlGraph')
            break
    
    cmds.delete(node)
    regionCtrlName = Pickle.loads(str(regionCtrlNameString))
    regionCtrlGraph = Pickle.loads(str(regionCtrlGraphString))
    
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')

    regionAdded = []
    regionAddedString = cmds.getAttr(currNode + '.regionAdded')
    if regionAddedString:
        regionAdded = Pickle.loads(str(regionAddedString))
        
    clearRegionAttributes()
    regionBasedGraphSelected()
    paintRegionControlExec()
    resetArtSelectTool()
        
    for r in range(len(regionCtrlName)):
        faceID = regionCtrlName[r].split(scalpMesh + '_regionCtrl_')[1]
        face = scalpMesh + '.f[' + faceID + ']'
        cmds.select(face, r = True)
        regionAdded.append(scalpMesh + '_regionCtrl_' + str(faceID))
#        print face
        cmds.gradientControlNoAttr('defaultColorGraph', edit = True, asString = regionCtrlGraph[r])
        addRegionCtrl()
        
    
    regionAddedString = Pickle.dumps(regionAdded)
    cmds.setAttr(currNode + '.regionAdded', regionAddedString, type = 'string')
          
        
def execRestoreRegionSetup(finalPath, currBackup): 
    
    import cPickle as Pickle
    currNode = cmds.getAttr('gbNode.currentGBNode')
    
    mayaFile = finalPath + '/' + currBackup + '.mb'
    
    cmds.file(mayaFile, i = True, ignoreVersion = True)
    
    networkNodes = cmds.ls(type = 'network')
    for node in networkNodes:
        if currBackup in node:
            regionCtrlPosString = cmds.getAttr(node + '.regionCtrlPos')
            regionCtrlGraphString = cmds.getAttr(node + '.regionCtrlGraph')
            break
    
    cmds.delete(node)
    regionCtrlPos = Pickle.loads(str(regionCtrlPosString))
    regionCtrlGraph = Pickle.loads(str(regionCtrlGraphString))
    
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    charCPNode = createCPNode(scalpMesh)
    regionAdded = []
        
    clearRegionAttributes()
    regionBasedGraphSelected()
    paintRegionControlExec()
    resetArtSelectTool()
        
    for r in range(len(regionCtrlPos)):
        cmds.setAttr(charCPNode + '.ip',regionCtrlPos[r][0], regionCtrlPos[r][1],regionCtrlPos[r][2])
        faceID = cmds.getAttr(charCPNode + '.f')
#        faceID = regionCtrlName[r].split(scalpMesh + '_regionCtrl_')[1]
        face = scalpMesh + '.f[' + str(faceID) + ']'
        cmds.select(face, r = True)
        regionAdded.append(scalpMesh + '_regionCtrl_' + str(faceID))
        cmds.gradientControlNoAttr('defaultColorGraph', edit = True, asString = regionCtrlGraph[r])
        addRegionCtrl()
        
    
    regionAddedString = Pickle.dumps(regionAdded)
    cmds.setAttr(currNode + '.regionAdded', regionAddedString, type = 'string')
    cmds.delete(charCPNode)            


        
def clearRegionAttributes():
    
    currNode = cmds.getAttr('gbNode.currentGBNode')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    regionCtrlGrp = 'regionControlGrp_' + scalpMesh
    if cmds.objExists(regionCtrlGrp):
        cmds.delete(regionCtrlGrp)
        
    cmds.setAttr(currNode + '.lastRegionCtrl','', type = 'string')  
    cmds.setAttr(currNode + '.regionCtrlName','', type = 'string')
    cmds.setAttr(currNode + '.regionCtrlGraph','', type = 'string')     
    cmds.setAttr(currNode + '.regionCtrlCurves','', type = 'string')
    cmds.setAttr(currNode + '.regionPerList','', type = 'string')
    cmds.setAttr(currNode + '.regionEdited','', type = 'string')
    cmds.setAttr(currNode + '.regionAdded','', type = 'string')
    
    
def browsePathForRestore():
    
    import os
    fldr = cmds.fileDialog2(cap = 'Browse to Character Folder', fm = 3, ds = 2)
    if fldr:
        path = fldr[0]    
    
    cmds.textFieldButtonGrp('restorePathText', edit = True, tx = path)
    checkPathForRestore()
    


def assignPathToIconsLinux():
    
    import os
#    mayaPath = os.path.normpath(mm.eval('getenv ' + dQ + 'MAYA_LOCATION' + dQ + ';'))
    mayaPath = mm.eval('getenv MAYA_APP_DIR')
    version = cmds.about(v = True)  
    if cmds.about(x64 = True):
        version = str(version) + '-x64'
    path = mayaPath + '/' + str(version) + '/icons/groomBoy/'
    
    chkPath = mayaPath + '/' + str(version) + '/'
    if not os.path.exists(path):
#        reportGBMessage('Please copy the icons folder(groomBoy) as mentioned in Readme file', True, True, 'red')    
        cmds.warning('Please copy the icons folder(groomBoy) as mentioned in Readme file')      
        
#    dirs = os.walk(chkPath).next()[1]
#    found = False
#    if 'icons' not in chkPath:
#        dirs = os.walk(chkPath).next()[1]
        
        

#    print 
#    mayaPath = path
    return path
#    mayaPath = '/home/user/maya/2015-x64/icons'

def assignPathToIconsWindows():
    import os
    mayaPath = os.path.normpath(mm.eval('getenv ' + dQ + 'MAYA_LOCATION' + dQ + ';'))
    mayaPath = mayaPath + '\\icons\\'
    dirs = os.walk(mayaPath).next()[1]
    if 'groomBoy' not in dirs:
#        reportGBMessage('Please copy the icons folder as mentioned in Readme file', True, True, 'red')    
        cmds.warning('Please copy the icons folder(groomBoy) as mentioned in Readme file') 
        
    return mayaPath + 'groomBoy\\'         
    
def assignPathToIcons():
    
#    return '/home/akarmakar/maya/2014-x64/icons/groomBoy/'
    
    gbos = cmds.about(os = True)
    if gbos == 'linux64':
        return assignPathToIconsLinux()
    elif gbos == 'win64' or gbos == 'nt':
        return assignPathToIconsWindows()

def assignPathToIconsOnlyWIN():
    
    import os
    mayaPath = os.path.normpath(mm.eval('getenv ' + dQ + 'MAYA_LOCATION' + dQ + ';'))
    mayaPath = mayaPath + '\\icons\\'
    dirs = os.walk(mayaPath).next()[1]
    if 'groomBoy' not in dirs:
        message = 'Please copy the icons folder as mentioned in Readme file'
        raise RuntimeError, message
#        reportGBMessage('Please copy the icons folder as mentioned in Readme file', True, True, 'red')                                            
#        os.makedirs(mayaPath + '\\groomBoy\\')
        
    return mayaPath + 'groomBoy\\'        

def assignPathToIconsOLD():
    
    import os
#    projDirectory = cmds.workspace(rd = True, q = True)
    projDirectory = getLocationForMyDocs()
    
    f = open(projDirectory + '\iconPath.txt', 'r')
    mayaPath = f.read()        
    f.close()
    return mayaPath
    
def verifyForTESTVERSION(obj,err):
    
    sphereStats = {'triangle': 760, 'uvcoord': 439, 'edge': 780, 'vertex': 382, 'face': 400}
    humanHeadStats = {'triangle': 4156, 'uvcoord': 2214, 'edge': 6278, 'vertex': 2120, 'face': 4156}
    bearStats =  {'triangle': 15210, 'uvcoord': 8455, 'edge': 22862, 'vertex': 7649, 'face': 15210}
    
    
    testStats = [sphereStats, humanHeadStats, bearStats]
    
    currStats = cmds.polyEvaluate(obj, v = True, e = True, f = True, uv = True, t = True)              
    match = False
    for stat in range(len(testStats)):
        if currStats == testStats[stat]:
            match = True
            verifyForPositionTESTVERSION(obj, stat)
            break
            
    if not match:
        if err:
            reportGBMessage('Only specific mesh work in DEMO Version.', True, True, 'red')                
        else:
            return False    
    else:
        return True                    

def verifyForPositionTESTVERSION(obj, match):
    
    checkSpacing = [5,15,30]
    spherePos = [[1.4877812564373016, -9.8768836259841919, -0.48340942710638046], [-0.48340935260057449, -9.8768836259841919, -1.4877809584140778], [-1.4877806603908539, -9.8768836259841919, 0.48340924084186554], [0.4834090918302536, -9.8768836259841919, 1.48778036236763], [2.9389283061027527, -9.5105654001235962, -0.95491565763950348], [-0.95491550862789154, -9.5105654001235962, -2.9389277100563049], [-2.9389271140098572, -9.5105654001235962, 0.95491528511047363], [0.95491498708724976, -9.5105654001235962, 2.9389265179634094], [4.31770920753479, -8.9100652933120728, -1.4029087126255035], [-1.4029085636138916, -8.9100652933120728, -4.3177083134651184], [-4.3177077174186707, -8.9100652933120728, 1.4029081165790558], [1.4029078185558319, -8.9100652933120728, 4.317706823348999], [5.590173602104187, -8.0901700258255005, -1.8163573741912842], [-1.8163572251796722, -8.0901700258255005, -5.5901724100112915], [-5.590171217918396, -8.0901700258255005, 1.8163566291332245], [1.8163561820983887, -8.0901700258255005, 5.5901706218719482], [6.7249894142150879, -7.0710676908493042, -2.1850813925266266], [-2.1850812435150146, -7.0710676908493042, -6.7249882221221924], [-6.7249870300292969, -7.0710676908493042, 2.185080498456955], [2.1850799024105072, -7.0710676908493042, 6.7249858379364014], [7.6942139863967896, -5.8778524398803711, -2.5000014901161194], [-2.5000011920928955, -5.8778524398803711, -7.6942121982574463], [-7.6942110061645508, -5.8778524398803711, 2.5000005960464478], [2.4999998509883881, -5.8778524398803711, 7.6942098140716553], [8.4739810228347778, -4.5399051904678345, -2.7533632516860962], [-2.7533629536628723, -4.5399051904678345, -8.4739798307418823], [-8.4739780426025391, -4.5399051904678345, 2.7533620595932007], [2.7533614635467529, -4.5399051904678345, 8.4739762544631958], [9.0450912714004517, -3.0901697278022766, -2.9389280080795288], [-2.9389277100563049, -3.0901697278022766, -9.0450894832611084], [-9.0450876951217651, -3.0901697278022766, 2.9389271140098572], [2.9389262199401855, -3.0901697278022766, 9.0450859069824219], [9.3934804201126099, -1.5643437206745148, -3.0521267652511597], [-3.0521264672279358, -1.5643437206745148, -9.3934786319732666], [-9.3934768438339233, -1.5643437206745148, 3.0521255731582642], [3.0521246790885925, -1.5643437206745148, 9.3934756517410278], [9.5105713605880737, 0.0, -3.0901718139648438], [-3.0901715159416199, 0.0, -9.5105695724487305], [-9.5105677843093872, 0.0, 3.0901706218719482], [3.0901697278022766, 0.0, 9.5105659961700439], [9.3934804201126099, 1.5643437206745148, -3.0521267652511597], [-3.0521264672279358, 1.5643437206745148, -9.3934786319732666], [-9.3934768438339233, 1.5643437206745148, 3.0521255731582642], [3.0521246790885925, 1.5643437206745148, 9.3934756517410278], [9.0450912714004517, 3.0901697278022766, -2.9389280080795288], [-2.9389277100563049, 3.0901697278022766, -9.0450894832611084], [-9.0450876951217651, 3.0901697278022766, 2.9389271140098572], [2.9389262199401855, 3.0901697278022766, 9.0450859069824219], [8.4739810228347778, 4.5399051904678345, -2.7533632516860962], [-2.7533629536628723, 4.5399051904678345, -8.4739798307418823], [-8.4739780426025391, 4.5399051904678345, 2.7533620595932007], [2.7533614635467529, 4.5399051904678345, 8.4739762544631958], [7.6942139863967896, 5.8778524398803711, -2.5000014901161194], [-2.5000011920928955, 5.8778524398803711, -7.6942121982574463], [-7.6942110061645508, 5.8778524398803711, 2.5000005960464478], [2.4999998509883881, 5.8778524398803711, 7.6942098140716553], [6.7249894142150879, 7.0710676908493042, -2.1850813925266266], [-2.1850812435150146, 7.0710676908493042, -6.7249882221221924], [-6.7249870300292969, 7.0710676908493042, 2.185080498456955], [2.1850799024105072, 7.0710676908493042, 6.7249858379364014], [5.590173602104187, 8.0901700258255005, -1.8163573741912842], [-1.8163572251796722, 8.0901700258255005, -5.5901724100112915], [-5.590171217918396, 8.0901700258255005, 1.8163566291332245], [1.8163561820983887, 8.0901700258255005, 5.5901706218719482], [4.31770920753479, 8.9100652933120728, -1.4029087126255035], [-1.4029085636138916, 8.9100652933120728, -4.3177083134651184], [-4.3177077174186707, 8.9100652933120728, 1.4029081165790558], [1.4029078185558319, 8.9100652933120728, 4.317706823348999], [2.9389283061027527, 9.5105654001235962, -0.95491565763950348], [-0.95491550862789154, 9.5105654001235962, -2.9389277100563049], [-2.9389271140098572, 9.5105654001235962, 0.95491528511047363], [0.95491498708724976, 9.5105654001235962, 2.9389265179634094], [1.4877812564373016, 9.8768836259841919, -0.48340942710638046], [-0.48340935260057449, 9.8768836259841919, -1.4877809584140778], [-1.4877806603908539, 9.8768836259841919, 0.48340924084186554], [0.4834090918302536, 9.8768836259841919, 1.48778036236763], [0.0, -10.0, 0.0]]

  
    humanHeadStats = [[4.3066048622131348, 3.1710019111633301, -1.5855319499969482], [5.2592854499816895, 1.7280621528625488, 0.14150239527225494], [1.9295052289962769, 11.760257720947266, 4.9746975898742676], [1.0153310298919678, 11.207918167114258, 5.0108323097229004], [1.0250905752182007, 11.468475341796875, 4.8720989227294922], [2.0557665824890137, 11.898317337036133, 5.1647424697875977], [2.3192610740661621, 11.535793304443359, 4.6058320999145508], [0.55449831485748291, 9.4078693389892578, 6.485562801361084], [0.3413594663143158, 11.803321838378906, 5.5617880821228027], [1.0170904397964478, 9.7706851959228516, 5.9157919883728027] ,\
    [1.2626471519470215, 11.388833999633789, 4.970573902130127], [1.4989128112792969, 8.2596893310546875, 5.0317254066467285], [1.0357927083969116, 8.0048751831054687, 5.0934815406799316], [0.29221916198730469, 10.845546722412109, 6.3220829963684082], [0.30526849627494812, 8.2431449890136719, 5.9348855018615723], [2.0187914371490479, 6.4609584808349609, 3.6506092548370361], [1.3184716701507568, 7.9231648445129395, 4.9481143951416016], [3.0667471885681152, 10.531000137329102, 4.2485909461975098], [1.2126467227935791, 16.681133270263672, -2.6016950607299805], [4.0676674842834473, 11.373153686523438, -1.1749579906463623] ,\
    [2.2098119258880615, 6.1801190376281738, -2.3101637363433838], [0.45278817415237427, 5.5053138732910156, 2.5650856494903564], [0.5613057017326355, 4.587989330291748, -3.185753345489502], [1.2501293420791626, 8.7869224548339844, -3.3816127777099609], [1.4525474309921265, 7.3704648017883301, 4.8376526832580566], [3.0341219902038574, 5.149442195892334, -0.91946238279342651], [0.55081659555435181, 5.6167216300964355, 3.4626839160919189], [0.66199743747711182, 9.1658229827880859, 5.6274313926696777], [4.1900849342346191, 10.654956817626953, 0.2564232349395752], [4.9149813652038574, 10.261773109436035, -0.19871371984481812] ,\
    [4.1858377456665039, 9.369964599609375, 0.73345208168029785], [4.1406593322753906, 9.0236616134643555, 0.72036838531494141], [4.6509056091308594, 11.144064903259277, 0.0013161897659301758], [4.308861255645752, 11.940185546875, 0.2054695188999176], [3.8599283695220947, 10.128934860229492, -0.93377989530563354], [4.9717845916748047, 11.09023380279541, -0.54154926538467407], [4.6241626739501953, 9.3355302810668945, 0.2283572256565094], [4.5117049217224121, 11.581220626831055, -0.53160059452056885], [4.171689510345459, 11.953628540039063, -0.87898361682891846], [1.2339904308319092, 5.6321020126342773, 1.7452744245529175] ,\
    [0.85650861263275146, 17.022945404052734, 2.3743131160736084], [1.5446367263793945, 7.121826171875, 4.7654647827148437], [1.3061381578445435, 7.9675602912902832, 4.9804706573486328], [1.3952082395553589, 7.953361988067627, 4.9249482154846191], [0.85083580017089844, 12.315766334533691, 5.6078686714172363], [4.4631505012512207, 9.6019115447998047, -0.47023957967758179], [4.4885563850402832, 11.209260940551758, 0.066475927829742432], [1.0872318744659424, 11.451471328735352, 4.8966817855834961], [2.735731840133667, 6.2284636497497559, 0.48064035177230835], [0.25041985511779785, 7.2528195381164551, 5.4608316421508789] ,\
    [1.0850613117218018, 6.463810920715332, 5.3233928680419922], [0.84707146883010864, 7.6344761848449707, 5.4271697998046875], [0.97073876857757568, 13.602962493896484, 5.4100069999694824], [1.4759247303009033, 8.0712432861328125, 4.9627170562744141], [1.8932836055755615, 8.1611709594726563, 4.7369184494018555], [3.2066113948822021, 8.9470748901367188, 3.2817404270172119], [0.016751836985349655, 6.0346417427062988, -2.9010994434356689], [1.7175998687744141, 12.974833488464355, 5.4058146476745605], [2.5476994514465332, 13.416717529296875, 4.6756362915039062], [3.5459175109863281, 11.089797973632813, 3.3030400276184082] ,\
    [3.9469945430755615, 14.586563110351563, 0.98253864049911499], [5.1181793212890625, 1.3695683479309082, 0.61297512054443359], [5.1497626304626465, 0.60605281591415405, 1.4120078086853027], [0.0, 8.8326168060302734, 5.8577265739440918], [0.0, 0.80626338720321655, 2.5309827327728271], [0.0, 3.2624409198760986, 2.051978588104248], [-0.00037753838114440441, 5.1265907287597656, 2.4061872959136963], [4.2597923278808594, 12.380860328674316, -0.0026278495788574219], [3.4096791744232178, 11.636551856994629, -3.111750602722168], [3.2392983436584473, 16.049476623535156, 0.57736968994140625] ,\
    [1.3641451597213745, 9.2840852737426758, -3.743767261505127], [4.1824889183044434, 12.529512405395508, 1.0611761808395386], [3.1308889389038086, 12.004131317138672, 4.2779679298400879], [2.7096827030181885, 11.246002197265625, 4.3898496627807617], [-0.70027023553848267, 1.0500798225402832, 2.5014145374298096], [-1.4426997900009155, 11.314878463745117, 5.0758867263793945], [-3.0322127342224121, 11.705633163452148, 4.3017678260803223], [-1.1271493434906006, 11.780921936035156, 5.0540480613708496], [-1.3858793973922729, 10.74632453918457, 5.086033821105957], [-0.76903921365737915, 11.764593124389648, 5.1211915016174316] ,\
    [-1.2137181758880615, 10.328296661376953, 5.352454662322998], [-1.0598491430282593, 9.562774658203125, 5.4513974189758301], [-0.26003685593605042, 9.2453079223632812, 6.1624369621276855], [-0.72060108184814453, 9.3781394958496094, 5.763817310333252], [-0.92202597856521606, 10.237117767333984, 5.6541123390197754], [-0.97591203451156616, 7.928520679473877, 5.0526480674743652], [-1.2112501859664917, 7.9746479988098145, 5.0166192054748535], [-0.53536999225616455, 7.9070820808410645, 5.1019954681396484], [-0.70987057685852051, 16.722660064697266, 3.0579085350036621], [-3.3421108722686768, 8.935795783996582, 2.7648885250091553] ,\
    [-2.2142682075500488, 11.438310623168945, 4.710810661315918], [-0.99887770414352417, 17.185115814208984, 1.5998849868774414], [-3.7938201427459717, 11.875411987304688, -2.3067963123321533], [-2.1214656829833984, 7.369530200958252, -2.2427992820739746], [-1.1206754446029663, 3.970139741897583, -3.3901534080505371], [-2.292762279510498, 3.6383974552154541, 1.2326964139938354], [-2.8868589401245117, 4.5213241577148437, 0.18598511815071106], [-3.8568103313446045, 10.573683738708496, -1.3238455057144165], [-0.14636717736721039, 9.1271553039550781, 6.0000004768371582], [-2.6214644908905029, 7.6745877265930176, 3.7888033390045166] ,\
    [-0.49020272493362427, 8.2743988037109375, 5.8364295959472656], [-4.7205371856689453, 11.524687767028809, 0.088921666145324707], [-4.6380224227905273, 10.871969223022461, 0.063096284866333008], [-4.1234860420227051, 9.5761775970458984, 0.065417736768722534], [-4.9087862968444824, 10.33709716796875, -0.093395590782165527], [-4.1066393852233887, 9.2347784042358398, 0.77570438385009766], [-4.7649097442626953, 11.386475563049316, -0.18095612525939941], [-4.2471928596496582, 10.651791572570801, 0.059676289558410645], [-4.4945363998413086, 10.557507514953613, -0.10417532920837402], [-4.0127840042114258, 9.3178653717041016, 0.85905218124389648] ,\
    [-4.5244607925415039, 11.495142936706543, 0.25964778661727905], [-3.7991979122161865, 9.1304731369018555, 1.0881884098052979], [-4.8242940902709961, 10.053354263305664, 0.00015634298324584961], [-3.8040769100189209, 13.418614387512207, -2.3263978958129883], [-0.81769335269927979, 7.946465015411377, 5.2778439521789551], [-0.23344437777996063, 12.744076728820801, 5.7739658355712891], [-0.86815172433853149, 8.0440444946289062, 5.3953347206115723], [-4.075101375579834, 10.219484329223633, 0.37296098470687866], [-4.3315410614013672, 9.2480077743530273, -0.23549753427505493], [-3.908217191696167, 9.9545078277587891, -0.0061065554618835449] ,\
    [-4.0246167182922363, 9.7775764465332031, 0.50327205657958984], [-2.5447876453399658, 5.1675353050231934, 0.64480829238891602], [-3.038271427154541, 6.8009476661682129, -0.10517963767051697], [-0.25738722085952759, 7.0264816284179687, 5.406163215637207], [-0.79537487030029297, 5.6557374000549316, 2.3648531436920166], [-0.28255188465118408, 13.664461135864258, 5.4884428977966309], [-1.5009087324142456, 7.9585423469543457, 4.9167723655700684], [-3.8365366458892822, 10.039942741394043, 1.9473627805709839], [-1.3829770088195801, 8.1747589111328125, 5.0804815292358398], [-2.9857666492462158, 12.247180938720703, 4.5598468780517578] ,\
    [-3.5972352027893066, 11.944424629211426, 3.1559419631958008], [-3.572939395904541, 14.250656127929688, 2.6959676742553711], [-2.2497034072875977, 16.523399353027344, 2.4305524826049805], [-3.949291467666626, 11.169815063476563, 1.8941113948822021], [-7.0839519500732422, 1.5870175361633301, -2.1272540092468262], [-4.083620548248291, 13.19896411895752, -1.3679554462432861], [-3.0439388751983643, 11.91431999206543, -3.8013463020324707], [-2.5629110336303711, 16.676322937011719, 0.69693803787231445], [-3.2374401092529297, 11.513965606689453, 3.9379673004150391], [-3.7202315330505371, 11.539825439453125, 2.8126492500305176] ,\
    [-3.6231484413146973, 12.488924980163574, 3.0606133937835693], [-3.5145416259765625, 10.651773452758789, 3.3624873161315918]]


    
    
    bearStats = [[1.6235611438751221, 66.517982482910156, 14.805473327636719], [0.56364208459854126, 67.050216674804688, 15.784689903259277], [0.71818673610687256, 62.186222076416016, 16.882549285888672], [2.2341048717498779, 62.136806488037109, 12.378450393676758], [5.4656095504760742, 68.056449890136719, 8.1290874481201172], [3.5402874946594238, 73.270111083984375, 4.3623123168945312], [5.2667622566223145, 71.269134521484375, 2.437654972076416], [6.6511425971984863, 72.200881958007812, 4.1674327850341797], [3.5715014934539795, 72.561798095703125, 5.4323673248291016], [3.6210346221923828, 71.744583129882813, 3.0278489589691162] ,\
    [5.2071247100830078, 61.021549224853516, 6.1111855506896973], [2.1488721370697021, 71.611747741699219, 9.3783426284790039], [4.9115786552429199, 70.101509094238281, 5.399749755859375], [0.68872183561325073, 60.249649047851563, 15.811457633972168], [3.702244758605957, 59.371528625488281, 6.761690616607666], [4.1274824142456055, 66.763175964355469, -1.8992698192596436], [0.35166698694229126, 72.387588500976563, 3.5538854598999023], [7.2542729377746582, 63.223209381103516, 1.6669881343841553], [1.3884713649749756, 67.886138916015625, 13.475337028503418], [3.5801632404327393, 64.879302978515625, 11.82943058013916] ,\
    [1.6756813526153564, 67.44281005859375, 13.055479049682617], [2.8639674186706543, 63.348556518554688, 15.613572120666504], [3.392240047454834, 62.197406768798828, 11.962861061096191], [2.4203205108642578, 67.41900634765625, 12.832430839538574], [2.0401906967163086, 68.15777587890625, 13.225312232971191], [2.1328005790710449, 64.985801696777344, 17.897605895996094], [0.21861547231674194, 66.374832153320312, 18.338006973266602], [0.96969443559646606, 64.541084289550781, 18.546014785766602], [0.51779305934906006, 65.889488220214844, 18.930576324462891], [1.0283569097518921, 65.937301635742188, 18.807817459106445] ,\
    [1.642248272895813, 65.050491333007813, 18.281349182128906], [9.6480646133422852, 38.559249877929687, -6.4071974754333496], [5.0060958862304687, 56.75494384765625, -8.5345621109008789], [6.9373841285705566, 33.085140228271484, 8.2762908935546875], [10.161368370056152, 39.955524444580078, -3.1283211708068848], [4.9098448753356934, 45.385837554931641, 8.1086540222167969], [2.2253448963165283, 53.947917938232422, 8.7030143737792969], [9.3030767440795898, 52.491962432861328, 5.1654653549194336], [9.9192829132080078, 44.871902465820313, 7.0541348457336426], [15.039444923400879, 46.916709899902344, 5.1076974868774414] ,\
    [9.6940450668334961, 55.819267272949219, 1.1718990802764893], [7.1705927848815918, 52.8218994140625, 6.4266095161437988], [10.537023544311523, 41.419990539550781, 1.731297492980957], [10.736351013183594, 40.51165771484375, 3.786013126373291], [8.0165634155273437, 42.061363220214844, 4.0334362983703613], [4.5932512283325195, 64.361961364746094, -3.5202822685241699], [12.570253372192383, 18.821193695068359, 2.4896717071533203], [6.0596828460693359, 15.656517028808594, 6.5992240905761719], [11.635614395141602, 9.9639787673950195, 2.0192153453826904], [6.623786449432373, 16.715206146240234, -10.757238388061523] ,\
    [12.643411636352539, 32.004009246826172, -4.7493863105773926], [8.4733123779296875, 8.7466354370117187, 5.2504487037658691], [3.439293384552002, 12.819568634033203, -8.1800422668457031], [5.1962885856628418, 7.7751531600952148, -2.1229243278503418], [4.7384762763977051, 60.710445404052734, -5.7575039863586426], [1.6409647464752197, 67.343711853027344, 13.122241973876953], [14.89560604095459, 35.455551147460938, 15.853470802307129], [16.838567733764648, 37.836063385009766, 12.563072204589844], [13.032566070556641, 38.23760986328125, 13.246952056884766], [12.807031631469727, 39.113723754882812, 12.33773136138916] ,\
    [16.382482528686523, 36.693576812744141, 13.803900718688965], [14.27324390411377, 36.169868469238281, 15.173803329467773], [12.389621734619141, 37.844669342041016, 16.268293380737305], [15.767720222473145, 40.758762359619141, 15.235695838928223], [17.649961471557617, 38.571308135986328, 15.491367340087891], [13.124134063720703, 37.802074432373047, 17.571971893310547], [14.584646224975586, 38.478981018066406, 11.733665466308594], [15.902619361877441, 35.852619171142578, 19.919059753417969], [18.274003982543945, 35.437980651855469, 18.14472770690918], [13.411986351013184, 35.143936157226563, 17.996992111206055] ,\
    [12.755703926086426, 34.718925476074219, 19.112852096557617], [12.202360153198242, 36.120567321777344, 18.424062728881836], [12.382416725158691, 36.534027099609375, 17.94378662109375], [15.505012512207031, 34.825309753417969, 20.356479644775391], [18.125091552734375, 34.528388977050781, 19.103353500366211], [13.681484222412109, 34.390037536621094, 19.523632049560547], [15.254551887512207, 35.326591491699219, 18.832370758056641], [16.525152206420898, 34.225337982177734, 18.777921676635742], [18.606523513793945, 33.468791961669922, 18.29008674621582], [17.852479934692383, 34.294029235839844, 17.163688659667969] ,\
    [17.341093063354492, 33.675804138183594, 17.92466926574707], [15.611972808837891, 33.728874206542969, 18.472463607788086], [14.886028289794922, 34.402763366699219, 18.488975524902344], [17.045560836791992, 35.285831451416016, 19.654729843139648], [15.088588714599609, 35.682445526123047, 20.085838317871094], [12.338886260986328, 36.56829833984375, 17.00385856628418], [18.391689300537109, 36.101894378662109, 15.599503517150879], [12.4774169921875, 36.184650421142578, 17.189750671386719], [18.377546310424805, 35.089084625244141, 16.342506408691406], [15.792596817016602, 36.855655670166016, 18.955482482910156] ,\
    [17.698556900024414, 37.197959899902344, 16.884757995605469], [13.297945976257324, 37.149112701416016, 18.274248123168945], [17.760965347290039, 34.461906433105469, 17.032575607299805], [15.921711921691895, 42.389015197753906, 12.24567985534668], [16.387399673461914, 37.910903930664062, 12.189226150512695], [16.204025268554687, 37.035255432128906, 13.141872406005859], [16.172565460205078, 37.190841674804688, 12.860487937927246], [12.551717758178711, 43.196170806884766, 11.040044784545898], [14.011343955993652, 39.027122497558594, 9.0564498901367187], [9.8001480102539063, 0.19248056411743164, 7.3848409652709961] ,\
    [9.7492208480834961, 2.2049412727355957, 7.140352725982666], [12.218357086181641, 1.2195935249328613, 6.1651020050048828], [11.828685760498047, 0.025010466575622559, 6.7751221656799316], [9.8034820556640625, 0.026198029518127441, 6.683800220489502], [8.8654994964599609, 0.64711600542068481, 8.7273073196411133], [11.67988109588623, 1.3127362728118896, 6.9676094055175781], [7.4355707168579102, 0.10248208045959473, 6.7883853912353516], [8.9599113464355469, 2.8515448570251465, 6.1533150672912598], [8.0032835006713867, 3.4021711349487305, 5.0297231674194336], [5.8836965560913086, 2.5131642818450928, 0.94032478332519531] ,\
    [7.276158332824707, 1.3409302234649658, -3.4145255088806152], [7.3906068801879883, 3.8416783809661865, 3.6353750228881836], [5.6915616989135742, 1.1107224225997925, 1.8216927051544189], [8.8481988906860352, -0.011913776397705078, 5.7036786079406738], [9.1174221038818359, -0.11656224727630615, -1.1081696748733521], [10.55972957611084, 0.022981822490692139, 1.9940359592437744], [10.328378677368164, 4.0718984603881836, 0.07041313499212265], [5.5366382598876953, 4.6715559959411621, -0.81748974323272705], [5.8942580223083496, 6.520115852355957, 2.9916322231292725], [9.9829740524291992, 6.9485774040222168, 3.3751416206359863] ,\
    [10.348664283752441, 0.030797481536865234, 6.7395505905151367], [1.1065812110900879, 70.171524047851563, 12.758708000183105], [1.5765833854675293, 68.434539794921875, 13.706389427185059], [0.30074429512023926, 69.723403930664063, 12.910995483398438], [6.0910840034484863, 71.790519714355469, 4.0183682441711426], [14.924118041992188, 38.587898254394531, 10.991872787475586], [1.8408536917036145e-09, 28.605381011962891, 12.213013648986816], [1.0741634248745413e-09, 40.676097869873047, -10.652881622314453], [-2.3068361282348633, 65.682830810546875, 16.511531829833984], [-0.15396785736083984, 67.088958740234375, 15.874636650085449] ,\
    [-2.1157517433166504, 61.528171539306641, 12.611560821533203], [-2.5393326282501221, 61.745983123779297, 14.241537094116211], [-2.4657661914825439, 61.983280181884766, 12.388711929321289], [-6.7797670364379883, 65.958389282226563, 5.7974934577941895], [-3.0598299503326416, 70.716629028320313, 10.085448265075684], [-3.4426817893981934, 72.6968994140625, 5.2037639617919922], [-6.0610132217407227, 73.450996398925781, 3.5350246429443359], [-5.794316291809082, 70.563796997070312, 3.9886610507965088], [-4.6490507125854492, 73.905166625976563, 4.9874420166015625], [-5.0250940322875977, 70.353172302246094, 4.4361567497253418] ,\
    [-4.4844913482666016, 70.250938415527344, 1.8747992515563965], [-4.3568515777587891, 60.264972686767578, 6.8217272758483887], [-1.5776790380477905, 72.096885681152344, 8.4019365310668945], [-3.9845438003540039, 71.005256652832031, 6.3104391098022461], [-0.89867234230041504, 60.145030975341797, 14.776745796203613], [-2.7297849655151367, 58.700401306152344, 7.7772297859191895], [-6.4052290916442871, 64.483749389648437, -1.2788492441177368], [-2.5423212051391602, 68.130363464355469, -1.5033789873123169], [-6.8689427375793457, 63.826202392578125, 2.089266300201416], [-2.4240074157714844, 69.065376281738281, 13.316009521484375] ,\
    [-1.63892662525177, 68.029258728027344, 13.24675178527832], [-0.61339914798736572, 68.332489013671875, 13.724864959716797], [-1.8712922334671021, 66.89178466796875, 13.109708786010742], [-2.6893613338470459, 67.263671875, 12.625994682312012], [-2.8639686107635498, 63.348854064941406, 15.613357543945313], [-2.8128330707550049, 62.057605743408203, 14.265960693359375], [-1.5732259750366211, 67.634658813476563, 13.043097496032715], [-2.4745326042175293, 68.236480712890625, 13.122822761535645], [-1.3482009172439575, 66.244369506835938, 18.079801559448242], [-1.7476557493209839, 64.750823974609375, 18.291095733642578] ,\
    [-1.7044074535369873, 65.316650390625, 17.573984146118164], [-0.56447643041610718, 65.198554992675781, 18.701654434204102], [-1.0586005449295044, 65.810203552246094, 18.803260803222656], [-1.0264123678207397, 64.970512390136719, 18.029857635498047], [-8.7645807266235352, 37.045337677001953, -8.203831672668457], [-8.2884006500244141, 57.631011962890625, -3.480384349822998], [-1.3552461862564087, 21.259025573730469, 11.268060684204102], [-10.58138370513916, 36.862010955810547, -0.66179847717285156], [-9.7749166488647461, 54.895912170410156, -5.2938189506530762], [-5.827115535736084, 53.422012329101563, 6.547238826751709] ,\
    [-1.3279035091400146, 60.035163879394531, -7.0065202713012695], [-9.3030757904052734, 52.491962432861328, 5.1654658317565918], [-14.667201995849609, 47.546710968017578, 1.3093090057373047], [-15.377063751220703, 45.585765838623047, 1.8206040859222412], [-14.891934394836426, 44.063327789306641, 10.482449531555176], [-6.7301125526428223, 47.251987457275391, 7.2396225929260254], [-10.605331420898438, 44.288345336914063, -2.0524599552154541], [-12.841655731201172, 41.654769897460938, 0.70746868848800659], [-13.912779808044434, 39.746383666992187, 5.0338153839111328], [-9.6261129379272461, 42.036094665527344, 4.8544821739196777] ,\
    [-2.4850468635559082, 15.847587585449219, 8.4839286804199219], [-9.4315853118896484, 12.373499870300293, 5.6076812744140625], [-5.8660421371459961, 11.483563423156738, 5.838529109954834], [-13.586042404174805, 17.120227813720703, -1.8137683868408203], [-2.6985158920288086, 18.908504486083984, -12.690615653991699], [-3.4392037391662598, 12.819686889648438, -8.1800498962402344], [-4.9284076690673828, 9.1712970733642578, 4.0008339881896973], [-11.229250907897949, 8.4834880828857422, 1.0475832223892212], [-2.4538226127624512, 11.07017707824707, -5.1149473190307617], [-1.9367583092844143e-09, 21.285312652587891, 11.375214576721191] ,\
    [-17.136785507202148, 37.043037414550781, 13.496005058288574], [-13.243651390075684, 38.137134552001953, 13.144346237182617], [-13.671791076660156, 38.357215881347656, 12.496952056884766], [-18.052690505981445, 37.00994873046875, 14.58397102355957], [-16.059226989746094, 36.105579376220703, 14.707001686096191], [-14.73526668548584, 36.962505340576172, 14.219034194946289], [-12.782196044921875, 38.799503326416016, 16.090000152587891], [-14.341363906860352, 41.559398651123047, 14.075075149536133], [-17.23558235168457, 39.756584167480469, 12.399065017700195], [-16.366064071655273, 37.559268951416016, 17.994213104248047] ,\
    [-16.671546936035156, 39.875358581542969, 15.574724197387695], [-16.973903656005859, 41.037906646728516, 12.331185340881348], [-14.273273468017578, 38.784095764160156, 10.38908576965332], [-15.548398017883301, 34.139209747314453, 20.554092407226562], [-15.652130126953125, 35.710163116455078, 19.808155059814453], [-18.502346038818359, 35.878189086914062, 17.529550552368164], [-13.331997871398926, 34.871547698974609, 18.817771911621094], [-13.829204559326172, 36.165653228759766, 18.648698806762695], [-12.179671287536621, 36.037784576416016, 17.998256683349609], [-12.973584175109863, 35.672359466552734, 19.519939422607422] ,\
    [-13.994458198547363, 34.674415588378906, 20.520181655883789], [-13.74394702911377, 35.612392425537109, 18.595767974853516], [-17.076011657714844, 34.302558898925781, 20.344858169555664], [-16.898481369018555, 35.847492218017578, 19.047191619873047], [-13.702604293823242, 35.165779113769531, 18.414796829223633], [-15.228067398071289, 34.405567169189453, 19.093633651733398], [-17.545143127441406, 34.443008422851562, 17.285469055175781], [-18.209720611572266, 33.4998779296875, 18.088159561157227], [-17.147388458251953, 33.416786193847656, 18.429515838623047], [-15.445282936096191, 33.452381134033203, 19.175271987915039] ,\
    [-14.974963188171387, 34.091365814208984, 20.697269439697266], [-17.820697784423828, 35.759647369384766, 18.706583023071289], [-13.932027816772461, 36.704376220703125, 18.681194305419922], [-18.056659698486328, 35.723014831542969, 15.313976287841797], [-15.145754814147949, 34.565017700195313, 17.475860595703125], [-17.24803352355957, 34.717552185058594, 16.529922485351562], [-13.401882171630859, 37.50616455078125, 18.011215209960937], [-15.480422973632813, 36.628700256347656, 19.14268684387207], [-17.676294326782227, 34.594100952148438, 16.857784271240234], [-15.931377410888672, 38.474342346191406, 11.455901145935059] ,\
    [-15.883082389831543, 37.732810974121094, 12.187676429748535], [-15.921509742736816, 37.242721557617188, 12.810759544372559], [-14.011343002319336, 39.027126312255859, 9.0564498901367187], [-8.8571672439575195, 0.0057115554809570313, 7.157982349395752], [-10.806648254394531, 1.3172943592071533, 7.7362613677978516], [-8.852452278137207, 1.3593301773071289, 8.3221769332885742], [-12.536890983581543, 0.65935307741165161, 4.5464563369750977], [-11.278238296508789, 0.086708545684814453, 7.3818745613098145], [-9.8053035736083984, 0.026131749153137207, 6.6833209991455078], [-6.8197641372680664, 0.82309234142303467, 6.3582353591918945] ,\
    [-8.697361946105957, 0.1893470287322998, 7.9208478927612305], [-11.338313102722168, 2.5467064380645752, 3.6445846557617187], [-11.066170692443848, 2.7961673736572266, 2.0924923419952393], [-9.6921920776367188, 4.3597087860107422, 2.7778205871582031], [-10.190011978149414, 2.9756090641021729, -1.0645198822021484], [-9.4079046249389648, 3.74672532081604, 4.1545228958129883], [-10.235066413879395, 0.63714319467544556, -2.5708532333374023], [-8.3796310424804687, 0.008089900016784668, 4.3421230316162109], [-7.0857982635498047, -0.09361720085144043, -0.39060571789741516], [-10.320069313049316, 0.15530246496200562, -1.4501895904541016] ,\
    [-7.13720703125, 0.027570843696594238, 3.0182416439056396], [-8.6098947525024414, 4.9553112983703613, 3.4767975807189941], [-9.9829740524291992, 6.9485774040222168, 3.3751413822174072], [-0.15496480464935303, 70.163467407226562, 12.450920104980469], [-5.1618714332580566, 71.032463073730469, 4.1204690933227539]]

    
    


    
    testPos = [spherePos, humanHeadStats, bearStats]
    vtxAll = cmds.polyEvaluate(obj, v = True)
    c = 0
    space = checkSpacing[match]
    for v in range(0,vtxAll,space):
        if not cmds.xform(obj + '.vtx[' + str(v) + ']' , q = True, ws = True, t = True) == testPos[match][c]:
            reportGBMessage('Test Model Scalp Mesh are not to be tweaked. Please revert to given mesh', True, True, 'red')
        c = c + 1            
    
    
def scriptEditorWorkOLD():

    if cmds.window('scriptEditorPanel1Window', exists = True):
        lineerror()
    else:        
        mm.eval('ScriptEditor;')    
        cmds.window('scriptEditorPanel1Window', edit = True, vis = False)
        lineerror()
        if cmds.window('scriptEditorPanel1Window', exists = True):
            cmds.deleteUI('scriptEditorPanel1Window')    

def scriptEditorWorkOLD():
    
    
    if cmds.window('dummyWindowForLineErrors', exists = True):
        cmds.deleteUI('dummyWindowForLineErrors')
    cmds.window('dummyWindowForLineErrors')
    cmds.columnLayout()
    dummy = cmds.cmdScrollFieldReporter('dummyReporter', clear = True)
    correctScrollFieldReporter(dummy)
    cmds.deleteUI('dummyWindowForLineErrors')   

def scriptEditorWork():
    
    
    if not cmds.window('dummyWindowForLineErrors', exists = True):
        cmds.window('dummyWindowForLineErrors')
        cmds.columnLayout(vis = False)
        dummy = cmds.cmdScrollFieldReporter('dummyReporter', clear = True)
    dummy = 'dummyReporter'
    correctScrollFieldReporter(dummy)

def correctScrollFieldReporter(dummy):
    
    ln = cmds.cmdScrollFieldReporter(dummy, q = True, lineNumbers = True)
    if ln:
        cmds.cmdScrollFieldReporter(dummy, e = True, lineNumbers = False)

    st = cmds.cmdScrollFieldReporter(dummy, q = True, stackTrace = True)
    if st:
        cmds.cmdScrollFieldReporter(dummy, e = True, stackTrace = False)
        
def scriptEditorDebug():
    
    
    if not cmds.window('dummyWindowForLineErrors', exists = True):
        cmds.window('dummyWindowForLineErrors')
        cmds.columnLayout(vis = False)
        dummy = cmds.cmdScrollFieldReporter('dummyReporter', clear = True)
    dummy = 'dummyReporter'
    correctScrollFieldReporterDebug(dummy)    
    
def correctScrollFieldReporterDebug(dummy):
    
    cmds.cmdScrollFieldReporter(dummy, e = True, lineNumbers = True)
    cmds.cmdScrollFieldReporter(dummy, e = True, stackTrace = True)            

def lineerror():
    
#    return
    if gbDebugCheck():
        scriptEditorDebug()
    else:        
        scriptEditorWork()
         
def lineerrorOLD():
    
    all = cmds.lsUI(mi = True, long = True)
    for a in all:
        if 'cmdScrollFieldReporter' in a:
            parts = a.split('|')
            for p in parts:
                if 'cmdScrollFieldReporter' in p:
                    correctScrollFieldReporter(p)
                    

def autoGBDisplayName():
    
    networkNodes = cmds.ls(type = 'network')
    if networkNodes:
        if 'gbNode' in networkNodes:
            networkNodes.remove('gbNode')

    defaultName = 'gbChar_'
    ver = 01
    version = '01'
    gbName = defaultName + version
    

    if not networkNodes:
        return gbName
    
    
    while not checkIfDPExists(ver):
        ver = ver + 1
    
    if ver < 10:
        version = '0' + str(ver)
    else:
        version = str(ver)
    
    gbName = defaultName + version
    return gbName
    
def checkIfDPExists(ver):
    
    networkNodes = cmds.ls(type = 'network')
    if networkNodes:
        if 'gbNode' in networkNodes:
            networkNodes.remove('gbNode')

    defaultName = 'gbChar_'
    if ver < 10:
        version = '0' + str(ver)
    else:
        version = str(ver)        
    
    gbName = defaultName + version            
    
    found = False
    for each in networkNodes:
        if cmds.attributeQuery('parent', node = each, exists = True):
            if cmds.getAttr(each + '.parent') == 'gbNode':
                dpName = cmds.getAttr(each + '.displayName')
                if dpName == gbName:
                    found = True
                    break                                            

    if found:
        return False
    else:
        return True        
        
def refreshGBDatabase():
        
    import cPickle as Pickle
    currNode = cmds.getAttr('gbNode.currentGBNode')
    curveFaces = []
    curveFaces = Pickle.loads(str(cmds.getAttr(currNode + '.curveFaces')))
    if not curveFaces:
        return
        
    lenCF = len(curveFaces)
    for x in range(lenCF):
        for cf in curveFaces[x]:
            if not cf.isdigit():
#                print 'withname', cf
                curveFaces[x] = convertCurveToIDList(curveFaces[x])                
                break
                
        crvList = convertIDToCurveList(curveFaces[x])
        if crvList:
            for y in range(len(crvList)):
                if crvList[y]:
                    if not cmds.objExists(crvList[y]):
#                        print crvList[y]
                        curveFaces[x].remove(crvList[y])

                                                        
    curveFacesString = Pickle.dumps(curveFaces)
    cmds.setAttr(currNode + '.curveFaces', curveFacesString, type = 'string')

def autoTransferGridToChar():
    
    currNode = cmds.getAttr('gbNode.currentGBNode')
    uvGrid = cmds.getAttr(currNode + '.uvGrid')
    crvGrp = 'handDrawnCurvesOn_' + uvGrid
    uvGridRelatives = cmds.listRelatives(uvGrid, c = True)
    crvList = []
    if crvGrp in uvGridRelatives:
        crvList = cmds.listRelatives(crvGrp, c = True)
    
    if crvList:
        crvList = [crv for crv in crvList if cmds.ls(cmds.listRelatives(crv, s = True), et = 'nurbsCurve')]   
    
    cmds.select(crvList, r = True)
    baseGrp = cmds.getAttr(currNode + '.baseMeshGroup')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    
    mapCharGrp = 'mapFromChar_' + scalpMesh
    mapCharList = []
    if mapCharGrp in uvGridRelatives:
        mapCharList = cmds.listRelatives(mapCharGrp, c = True)
        if mapCharList:
            mapCharList = [crv for crv in mapCharList if cmds.ls(cmds.listRelatives(crv, s = True), et = 'nurbsCurve')]  
            if mapCharList:
                cmds.select(mapCharList,add = True) 
   
    if not crvList and not mapCharList:
        return

    autoMap(1)
    
def checkForTempGBNode():
    
    try:
        cmds.getAttr('gbNode.tempGBNode')
    except ValueError:
        cmds.addAttr('gbNode', ln = 'tempGBNode', dt = 'string')
        cmds.setAttr('gbNode.tempGBNode', 'tempGBNode', type = 'string')        
        
    currNode = cmds.getAttr('gbNode.currentGBNode')
    try:
        cmds.getAttr(currNode + '.regionMoved')
    except ValueError:
        cmds.addAttr(currNode, ln = 'regionMoved', dt = 'string')
                        

def checkForRegionCtrlDelete():
    
    import cPickle as Pickle
    historyDelete = []
    currNode = cmds.getAttr('gbNode.currentGBNode')
    
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    usedRegion = []
    usedRegionString = cmds.getAttr(currNode + '.regionCtrlName')
    if usedRegionString:
        usedRegion = Pickle.loads(str(usedRegionString))    
    
    regionCtrlGrp = 'regionControlGrp_' + scalpMesh
    currentRegion = cmds.listRelatives(regionCtrlGrp, c = True)
    
    
    removeRegion = list(set(usedRegion) - set(currentRegion))
    if removeRegion:
#        print 'here'
        if cmds.objExists(usedRegion[-1]):
            cmds.select(usedRegion[-1], r = True)
        autoResizeREGION()

def repositionCurvesToActiveMesh():
    
    currNode = cmds.getAttr('gbNode.currentGBNode')
    paintMesh = cmds.getAttr(currNode + '.paintOnMesh')
    
    sel = cmds.ls(sl = True)
    if not sel:
        reportGBMessage('Nothing Selected. Please select curves', True, True, 'red')

    selCurves = []
    selCurves = cmds.listRelatives(cmds.listRelatives(cmds.ls(sl = True), ad = True, typ = 'nurbsCurve'), p = True)
    if not selCurves:
        reportGBMessage('No Curves Selected', True, True, 'red')    
    
    charCPNode = createCPNode(paintMesh)
    charFoll = createFollicleOtherMesh(paintMesh)
    cmds.select(cl = True)
    charFollShp = cmds.listRelatives(charFoll, s = True)[0]
        
    
    for crv in selCurves:
        rootPos = cmds.xform(crv + '.cv[0]', q = True, ws = True, t = True)
        cmds.xform(crv, piv = rootPos)
        cmds.setAttr(charCPNode + '.ip', rootPos[0], rootPos[1], rootPos[2])
        crvU = cmds.getAttr(charCPNode + '.u')
        crvV = cmds.getAttr(charCPNode + '.v')
        cmds.setAttr(charFollShp + '.parameterU', crvU)
        cmds.setAttr(charFollShp + '.parameterV', crvV)        
        pc = cmds.pointConstraint(charFoll, crv)
        cmds.delete(pc)
        newPos = cmds.xform(crv, q = True, ws = True, t = True)
        cmds.xform(crv, piv = newPos)
        
    cmds.delete(charCPNode)        
    cmds.delete(charFoll)
    
    if sel:
        cmds.select(sel, r = True)
    
    
        
def touchCurvesToMesh(mesh = 'scalpMesh'):
    
    import time
    currNode = cmds.getAttr('gbNode.currentGBNode')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    volumeMesh = cmds.getAttr(currNode + '.volumeMesh') 
    historyDelete = []
    
    sel = cmds.ls(sl = True)
    if not sel:
        reportGBMessage('Nothing Selected. Please select curves', True, True, 'red')

    selCurves = []
    selCurves = cmds.listRelatives(cmds.listRelatives(cmds.ls(sl = True), ad = True, typ = 'nurbsCurve'), p = True)
    if not selCurves:
        reportGBMessage('No Curves Selected', True, True, 'red')        
    
    if mesh == 'scalpMesh':
        snapMesh = scalpMesh
    else:
        snapMesh = volumeMesh          
          
    charCPNode = createCPNode(snapMesh)
    historyDelete.append(charCPNode)    
    
    if len(selCurves)>1:
        cmds.text('gbProgressBarText', edit = True, vis = True, label = 'Performing Manipulation on ' + str(len(selCurves)) + ' Curves')
        cmds.progressBar('gbProgressBar', edit = True, pr = 0, max = len(selCurves)-1, vis = True)
    step = len(selCurves)
    totalIter = step
    percentCheck = [(per * totalIter) / 100 for per in range(0,100,10)]
    masterTime = time.time()      
    iter = 0
    checkTime = False
    firstLoop = False
    flM = 0
    flS = 0
            
    for crv in selCurves:
        
        if iter in percentCheck:
            checkTime = True
        else:
            checkTime = False            

        if checkTime:
            loopStart = time.time()
                
        iter = iter + 1
        
        p0 = cmds.xform(crv + '.cv[0]', q = True, ws = True, t = True)
        pA = cmds.pointOnCurve(crv, pr = 0.5, p = True)
        cmds.setAttr(charCPNode + '.ip', pA[0], pA[1], pA[2])
        pB = list(cmds.getAttr(charCPNode + '.p')[0])
        
        dA = [(c - d) for c, d in zip(pA,p0)] 
        dB = [(c - d) for c, d in zip(pB,p0)] 
        uA = mm.eval('unit <<' + str(dA[0]) + ',' + str(dA[1]) + ',' + str(dA[2]) + '>>')
        uB = mm.eval('unit <<' + str(dB[0]) + ',' + str(dB[1]) + ',' + str(dB[2]) + '>>')
        tRot = cmds.angleBetween(euler = True, v1 = uA, v2 = uB)
        cmds.rotate(tRot[0], tRot[1], tRot[2], crv, r = True)
        
        dg = cmds.getAttr(crv + '.degree')
        sp = cmds.getAttr(crv + '.spans')
        ncv = dg + sp
        for x in range(ncv):
            pos = cmds.xform(crv + '.cv[' + str(x) + ']', q = True, ws = True, t = True)
            cmds.setAttr(charCPNode + '.ip', pos[0], pos[1], pos[2])
            cmds.xform(crv + '.cv[' + str(x) + ']', ws = True, t = cmds.getAttr(charCPNode + '.p')[0])
        
        step = step - 1                
        cmds.text('gbProgressBarText', edit = True, label = 'Snapping Curves to Scalp Mesh  : ' + str(step) + ' Curves Remaining')
        cmds.progressBar('gbProgressBar', edit = True, s = 1)
        
        if checkTime:
            timeRemaining = (time.time() - loopStart) * (totalIter - iter)
            trM, trS = divmod(timeRemaining, 60)
#            print bgRGB
    
            if not firstLoop and trS > 1.0:
                flM = trM
                flS = trS 
                firstLoop = True
                
        loopEntered = True            
        timeElapsed = time.time() - masterTime
        teM, teS = divmod(timeElapsed, 60)
        messageString = 'Time Remaining: ' + str('%02d' % trM) + ':' + str('%02d' % trS) + '\t' + 'Time Elapsed: ' + str('%02d' % teM) + ':' + str('%02d' % teS) 
#        reportGBMessage(messageString, False, False, 'blue')
        cmds.text('gbMessageStatusText', edit = True, vis = True,  label = '  ' + messageString)
#        bgRGB = list(mm.eval('hsv_to_rgb <<' + str(remapNew(0,0.333,0,totalIter,iter)) + ',1.0,' + str(remapNew(0.0,1.0,-1.0,1.0,math.sin(iter))) + '>>;'))
        bgRGB = list(mm.eval('hsv_to_rgb <<' + str(remapNew(0,0.333,0,totalIter,iter)) + ',1.0,1.0>>;'))
        cmds.text('gbMessageStatusColor',edit = True, vis = True, bgc = bgRGB)            
            
    
    cmds.text('gbProgressBarText', edit = True, vis = False)
    cmds.progressBar('gbProgressBar', edit = True, vis = False)
    cmds.progressBar('gbProgressBar', edit = True, pr = 0)
    if loopEntered:
        finalMessage = 'Total Time Expected: ' + str('%02d' % flM) + ':' + str('%02d' % flS) + '\t' + 'Time Taken: ' + str('%02d' % teM) + ':' + str('%02d' % teS)         
    
    cmds.text('gbMessageStatusText', edit = True, vis = False, label = finalMessage)

def getCheckFolderPath():
    
    import os
    import maya.mel as mm
    mayaPath = os.path.normpath(mm.eval('getenv ' + dQ + 'MAYA_LOCATION' + dQ + ';'))
    return os.path.abspath(os.path.join(mayaPath, os.pardir))
    
def licenseCheckGB():
    
    import ctypes
    from ctypes.wintypes import MAX_PATH
    import sys
    import os
    import datetime

    kernel32 = ctypes.windll.kernel32
    windows_directory = ctypes.create_unicode_buffer(1024)
    if kernel32.GetWindowsDirectoryW(windows_directory, 1024) == 0:
        print 'No Drives Found'
        return
    else:
        windows_drive = os.path.splitdrive(windows_directory)[0]

    sys32Path = os.environ['WINDIR'] + '\\System32'
    
    sys32Path = getCheckFolderPath()
    seconds = os.path.getctime(sys32Path)
    seconds = ('%.7f' %seconds)

#    macID =  getMacAddress()   
#    message = macID + ']|[' + str(seconds)
    message = str(seconds)
    cipher = encryptGB(message)
    userKey = 'amVpYmZtbmZnaWZva2pqaWpu'
    myKey = 'amNrYmduZmZob2ZnaWhob2dp'
                      
    if cipher == userKey or cipher == myKey:
        return True
    else:
        if gbDebugCheck():
            print 'This plugin is compiled to check for key ', userKey
            print 'This machine is giving back this key     ', cipher
        lineerror()
        raise RuntimeError, 'INVALID LICENSE.'

def gbDebugCheck():
    
    mesh = 'debugSphere'
    sc = 5.0
    if cmds.objExists(mesh):
        return True
#        if cmds.getAttr(mesh + '.scaleX') == 5.0:
#            return True
    else:
        return False           
        
def getMacAddress(): 

    import sys
    import os
    
    if sys.platform == 'win32': 
        for line in os.popen('ipconfig /all'): 
            if line.lstrip().startswith('Physical Address'): 
                mac = line.split(':')[1].strip().replace('-',':') 
                break 
                
    return mac 


def getLocationsForSessionFile():
    
    gbos = cmds.about(os = True)
    if gbos == 'win64' or gbos == 'nt':
        return getLocationsForSessionFileWin()
    elif gbos == 'linux64':
        return getLocationsForSessionFileLinux()
                
        
    
def getLocationsForSessionFileLinux():
    
    import os
    mayaPath = mm.eval('getenv MAYA_APP_DIR')
    if gbType == 2:
        sessionPath = mayaPath + '/projects/default/scripts/staticLink.sh'
    else:        
        sessionPath = mayaPath + '/projects/default/scripts/programServices.pdl'

    return [sessionPath]
    

def getLocationsForSessionFileWin():
    
    import os
    import ctypes
    from ctypes.wintypes import MAX_PATH
    
    dll = ctypes.windll.shell32
    buf = ctypes.create_unicode_buffer(MAX_PATH + 1)
    if dll.SHGetSpecialFolderPathW(None, buf, 0x0005, False):
        myDoc = buf.value
    location = []
#    location.append(myDoc + '\\maya\\projects\\default\\scripts\\defaultMaya.sys')
    os.path.normpath(myDoc)
    path = myDoc + '\\maya\\projects\\default\\scripts'
    if not os.path.exists(path):
        os.mkdir(path)

    if gbType == 2:        
        location.append(path + '\\staticLink.sh')
    else:        
        location.append(path + '\\programServices.pdl')
 
    return location

def verifySessionFiles():
    
    import os
    
    
    location = getLocationsForSessionFile()
    sessionValid = []
    valid = []
#    loc = location[0]
    for loc in location:
        if not os.path.isfile(loc):
            valid.append(False)
        else:
            valid.append(True)
            
    if True in valid and False in valid:
        lineerror()
        message = 'Session data is compromised. Kindly mail to us to fix it.'
        raise RuntimeError, message
    
    if not True in valid:
        for loc in location:
            if not os.path.isfile(loc):
                
#                message = 'Session data is compromised. Please run GroomboyInitKey plugin'
#                raise RuntimeError, message
                
                f = open(loc ,'w')
                f.close()                
    
                toStore = getGBSessionData(loc)
                
                f = open(loc ,'w')
                f.write(toStore)
                f.close()                
                return True
    
    leftSessions = 0
    if not False in valid:
        for loc in location:
            f = open(loc,'r')
            cipher = f.read()
            f.close()
            data = decryptGB(cipher)
            info = data.split('|')
            seconds = info[0]
            sessions = info[1]
            
            fileTime = repr(os.path.getctime(loc))
#            print 'left sessions', sessions
            if cmds.about(os = True) == 'linux64':
                if int(sessions) >= 1:
                    sessionValid.append(True)
                    f = open(loc,'w')
                    leftSessions = int(sessions) - 1
                    message = seconds + '|' + str(leftSessions)
                    cipher = encryptGB(message)
                    f.write(cipher)
                    f.close()                
                else:
                    sessionValid.append(False)                
                    break                    
                    
            else:
                if fileTime == seconds and int(sessions) >= 1: 
                    sessionValid.append(True)
                    f = open(loc,'w')
                    leftSessions = int(sessions) - 1
                    message = seconds + '|' + str(leftSessions)
                    cipher = encryptGB(message)
                    f.write(cipher)
                    f.close()    
                else:
                    sessionValid.append(False)                
                    break
                            
    if leftSessions > 0:
        print 'GROOMBOY: ONLY ' + str(leftSessions) + ' SESSIONS LEFT' 
        cmds.warning('GROOMBOY: ONLY ' + str(leftSessions) + ' SESSIONS LEFT' )
#        raise RuntimeWarning, 'GROOMBOY: ONLY ' + str(leftSessions) + ' SESSIONS LEFT'                            

#    if not leftSessions > 0:
#        return False
                    
    if False in sessionValid:
#        return False
        lineerror()
        raise RuntimeError, 'All Sessions Expired. Please buy the Licensed Version'
    
    return True        
    
            
       
def getGBSessionData(loc):
    
    import os
    import datetime
    
    nowTime = repr(os.path.getctime(loc))
    if gbType == 2:
        sessions = '18'
    else:        
        sessions = '9'
    message = nowTime + '|' + sessions
    cipher = encryptGB(message)
    return cipher
    
def getCipherKeyGB():
    
    return '915038565787585829'
    
def encryptGB(message):
    
    import base64
    key = getCipherKeyGB()
    enc = []
    for i in range(len(message)):
        key_c = key[i % len(key)]
        enc_c = chr((ord(message[i]) + ord(key_c)) % 256)
        enc.append(enc_c)
    return base64.urlsafe_b64encode(''.join(enc))

def decryptGB(enc):

    import base64
    key = getCipherKeyGB()
    dec = []
    enc = base64.urlsafe_b64decode(enc)
    for i in range(len(enc)):
        key_c = key[i % len(key)]
        dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
        dec.append(dec_c)
    return ''.join(dec)

       
    
def handyToolsSculptGeo():
    
    mm.eval('SculptGeometryToolOptions;')    
    cmds.rowLayout('htSculptGeoMaxDispLyt', edit = True, vis = True)
    cmds.text('htSculptGeoMaxDispText', edit = True, vis = True)
    cmds.floatField('htSculptGeoMaxDispFloat', edit = True, vis = True)

def handyToolsCollapse():
    
    cmds.rowLayout('htSculptGeoMaxDispLyt', edit = True, vis = False)
    cmds.text('htSculptGeoMaxDispText', edit = True, vis = False)
    cmds.floatField('htSculptGeoMaxDispFloat', edit = True, vis = False)

def createIpolPerSuperOLD(mode = 'manual'):
    
    stopGBUndo()
    import cPickle as Pickle
    currNode = cmds.getAttr('gbNode.currentGBNode')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    baseMeshGrp = cmds.getAttr(currNode + '.baseMeshGroup')
    baseMeshGrpChildren = cmds.listRelatives(baseMeshGrp, c = True)
    superGrp = 'superCurves_charInterpolation_' + scalpMesh
    
    if not superGrp in baseMeshGrpChildren:
        if mode == 'auto':
            return
        reportGBMessage('No Super Curves Exist', True, True, 'red')

    superGrpChildren = []    
    superGrpChildren = cmds.listRelatives(superGrp, c = True)      
    
    if not superGrpChildren:
        if mode == 'auto':
            return
        reportGBMessage('No Super Curves Exist', True, True, 'red')
    
    cmds.setAttr(currNode + '.performIPS', True)
    scalpSuperCurvesPos = []
    scalpSuperCurvesPosString = cmds.getAttr(currNode + '.scalpSuperCurvesPos')
    if scalpSuperCurvesPosString:
        scalpSuperCurvesPos = Pickle.loads(str(scalpSuperCurvesPosString))    

    finalScalpPos = []
    if scalpSuperCurvesPos:
        finalScalpPos = [x[0] for x in scalpSuperCurvesPos]
    
    else:
        for sup in superGrpChildren:
            finalScalpPos.append(cmds.xform(sup + '.cv[0]', q = True, ws = True, t = True))
    vtxSel = []
    charCPNode = createCPNode(scalpMesh)
    scalpMeshDISP = scalpMesh + '_DISPLAY'
    for pos in finalScalpPos:
        cmds.setAttr(charCPNode + '.ip', pos[0], pos[1], pos[2])
        vtxID = cmds.getAttr(charCPNode + '.vt')
        vtxSel.append(scalpMeshDISP + '.vtx[' + str(vtxID) + ']')
    
    cmds.select(vtxSel, r = True)
#    print vtxSel
    currentLastIpol = cmds.getAttr(currNode + '.lastIpolSelection')
#    removeExistingIpolPerSuper()
    existIPS = []
    existIPSString = cmds.getAttr(currNode + '.existIPS')

    if existIPSString:
        existIPS = Pickle.loads(str(existIPSString))
    if existIPS:
        cmds.select(existIPS, r = True)
        removeInterpolationFromSelected()
#        print '??', existIPS

    existIPS = vtxSel        
#    print '!!', existIPS
    cmds.select(existIPS, r = True)
    charInterpolationSelectedFaces()
    if currentLastIpol:
        cmds.setAttr(currNode + '.lastIpolSelection', currentLastIpol, type = 'string')
    cmds.delete(charCPNode)
    cmds.setAttr(currNode + '.existIPS', str(Pickle.dumps(existIPS)), type = 'string')
    startGBUndo()
                

def showHideRefreshDisplayMesh():
    
    stopGBUndo()
    per = cmds.floatField('displayOffsetField', q = True, v = True)
    currNode = cmds.getAttr('gbNode.currentGBNode')
    if cmds.attributeQuery('displayMeshOffset', node = currNode, exists = True):
        dispPer = cmds.setAttr(currNode + '.displayMeshOffset', per)
    else:
        dispPer = cmds.setAttr('gbNode.displayMeshOffset', per)
    
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    scalpDISP = scalpMesh + '_DISPLAY'
    resizeDISPMesh(scalpDISP)
    cmds.select(cl = True)
    hideToolSettings()
    startGBUndo()    
    
            
def handyRefreshDisplayMesh():
    
    stopGBUndo()
    per = cmds.floatField('htDisplayMeshFloat', q = True, v = True)
    currNode = cmds.getAttr('gbNode.currentGBNode')
    if cmds.attributeQuery('displayMeshOffset', node = currNode, exists = True):
        dispPer = cmds.setAttr(currNode + '.displayMeshOffset', per)
    else:
        dispPer = cmds.setAttr('gbNode.displayMeshOffset', per)
    
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    scalpDISP = scalpMesh + '_DISPLAY'
    resizeDISPMesh(scalpDISP)
    startGBUndo()

def handyToolsExpand():
    
    currNode = cmds.getAttr('gbNode.currentGBNode')
    if cmds.attributeQuery('displayMeshOffset', node = currNode, exists = True):
        per = cmds.getAttr(currNode + '.displayMeshOffset')
    else:
        per = cmds.getAttr('gbNode.displayMeshOffset')
    
    cmds.floatField('htDisplayMeshFloat', edit = True, v = per)
    killAllGBJobs()         

def autoUpdateSmartVol():
    
    auto = cmds.checkBox('autoUpdateSmartVolChk', q = True, v = True)


def loadPaintForIpol(mode):
    
    currNode = cmds.getAttr('gbNode.currentGBNode')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    scalpMeshDISP = scalpMesh + '_DISPLAY'
	
    cmds.softSelect(edit = True, sse = 0)
    cmds.select(scalpMeshDISP, r = True)
    cmds.setToolTo('artSelectContext')
    
    loc = cmds.toolPropertyWindow(q = True, loc = True)
    if loc:
        mm.eval('ToggleToolSettings;')
    cmds.resetTool(cmds.currentCtx())
    cmds.artSelectCtx(cmds.currentCtx(), edit = True, unselectall = True)
        
    mm.eval('setComponentPickMask ' + dQ + mode + dQ + ' true;')        
    
def launchClumpMeshKit():
    
    if cmds.window('groomKitClumpMeshWin', exists = True):
        cmds.deleteUI('groomKitClumpMeshWin')
        
    cmds.window('groomKitClumpMeshWin', title = 'Clump Mesh Groom Kit', rtf = True, width = 150)
    cmds.columnLayout('clumpMeshMainLyt', adj = True)
    
    cmds.button('defineClumpScalp', vis = False, label = 'Use Selected Faces to Define Clump Scalp Mesh', c = 'defineClumpScalp()', p = 'clumpMeshMainLyt')
    
    cmds.button('editClumpScalpBtn', vis = False, label = 'Edit Clump Scalp Mesh', c = 'editClumpScalp()', p = 'clumpMeshMainLyt')
    cmds.frameLayout('editClumpScalpFrm', vis = False, label = 'Close Edit Clump Scalp Mesh', cll = True, cl = False, cc = 'collapseEditClumpScalp()', p = 'clumpMeshMainLyt')
    cmds.columnLayout('editClumpFrmColumn', adj = True, p = 'editClumpScalpFrm')
    cmds.button('confirmEditClumpScalpBtn', label = 'Confirm Selected faces as Clump Scalp Mesh', c = 'confirmEditClumpScalp()', p = 'editClumpFrmColumn')
    cmds.button('selectCurrentScalpBtn', label = 'Re-select Faces of Current Scalp Mesh', c = 'selectCurrentScalpFaces()', p = 'editClumpFrmColumn')
    cmds.button('cancelEditClumpScalp', label = 'Cancel Edit Clump Scalp Mesh', c = 'cancelEditClumpScalp()', p = 'editClumpFrmColumn')
    
    cmds.columnLayout('clumpOptionsLyt', adj = True, vis = False, p = 'clumpMeshMainLyt')
    cmds.text(label = 'Tweak Clump Graph', p = 'clumpOptionsLyt')
    cmds.gradientControlNoAttr('clumpTweakGraph', asString = '0.5,0,3,0.5,1,3', w = 200, h = 100, cc = 'clumpTweakExec()', p = 'clumpOptionsLyt')
    cmds.text(label = 'Scale Clump Graph', p = 'clumpOptionsLyt')
    cmds.gradientControlNoAttr('clumpScaleGraph', asString = '0,1,3,1,0,3', w = 200, h = 100, p = 'clumpOptionsLyt')
    cmds.button('updateClumpMeshBtn', label = 'Update Clump Meshes', c = 'regenerateClumpFF()', p = 'clumpOptionsLyt')
    cmds.floatFieldGrp('polyWidthField', label = 'Width for poly Strips', v1 = 0.1, p = 'clumpOptionsLyt')
    cmds.button('updatePolyStripBtn', label = 'Update Poly Strip Meshes', c = 'polyStripFF()', p = 'clumpOptionsLyt')
    cmds.checkBox('clumpScaleInteractiveChk', label = 'Interactive Feedback for Clump Scale Graph', p = 'clumpOptionsLyt')
    cmds.button('copyClumpScaleGraph', label = 'Copy Graph', p = 'clumpOptionsLyt')
    cmds.button('pasteClumpScaleGraph', label = 'Paste Graph', p = 'clumpOptionsLyt')
        
    
    cmds.rowLayout('clumpFlatLyt', nc = 2, p = 'clumpOptionsLyt')
    cmds.checkBox('clumpFlatCheck', label = 'Flatten Clump Mesh', p = 'clumpFlatLyt')
    cmds.intSliderGrp('clumpFlatSlider', label = 'Flatness', p = 'clumpFlatLyt')
    
    cmds.rowLayout('clumpSpansSections', nc = 2, p = 'clumpOptionsLyt')
    cmds.intFieldGrp('clumpSectionsField', label = 'Clump Sections U',v1 = 8,  p = 'clumpSpansSections')
    cmds.intFieldGrp('clumpSpansField', label = 'Clump Spans V', v1 = 8, p = 'clumpSpansSections')
    
    cmds.frameLayout('addRemoveClumpFrm', label = 'Add / Remove Clump Meshes', cll = True, cl = False, p = 'clumpMeshMainLyt')
    cmds.columnLayout('addRemoveClumpLyt', adj = True, p = 'addRemoveClumpFrm')
#    cmds.button('addClumpMeshBtn', label = 'Add Clump Mesh on Selected Curves', p = 'addRemoveClumpLyt')
#    cmds.button('removeClumpMeshBtn', label = 'Remove Clump Mesh on Selected Curves', p = 'addRemoveClumpLyt')
    cmds.button('regionPerClumpBtn', label = 'Add Region Controllers on Selected Clump',c = 'addRegionPerIpol()',  p = 'addRemoveClumpLyt')
    
    
    currNode = cmds.getAttr('gbNode.currentGBNode')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')


    clumpMeshExists = False
    clumpScalpMesh = cmds.getAttr(currNode + '.clumpMesh')
    if clumpScalpMesh:
        if cmds.objExists(clumpScalpMesh):
            clumpMeshExists = True
    
   
    if not clumpMeshExists:
        paintFacesForClumpScalp()
        cmds.button('defineClumpScalp', edit = True, vis = True)
        cmds.columnLayout('clumpOptionsLyt', edit = True, vis = False)
        cmds.frameLayout('addRemoveClumpFrm', edit = True, vis = False)
        
    else:
        cmds.columnLayout('clumpOptionsLyt', edit = True, vis = True)
        clumpScalpMeshDefined()

    cmds.showWindow('groomKitClumpMeshWin')
    cmds.scriptJob(e = ['SelectionChanged', 'loadClumpValues()'], kws = True, p = 'groomKitClumpMeshWin')


def paintFacesForClumpScalp():
    
    currNode = cmds.getAttr('gbNode.currentGBNode')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')

	
    cmds.softSelect(edit = True, sse = 0)
    cmds.select(scalpMesh, r = True)
    cmds.setToolTo('artSelectContext')
    
    loc = cmds.toolPropertyWindow(q = True, loc = True)
    if loc:
        mm.eval('ToggleToolSettings;')
    cmds.resetTool(cmds.currentCtx())
    cmds.artSelectCtx(cmds.currentCtx(), edit = True, unselectall = True)
        
    mm.eval('setComponentPickMask ' + dQ + 'Facet' + dQ + ' true;')        


def defineClumpScalp():
    
    currNode = cmds.getAttr('gbNode.currentGBNode')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    scalpFaces = cmds.polyEvaluate(scalpMesh, f = True)
    selFaces = cmds.ls(sl = True, fl = True)

    if not selFaces:
        reportGBMessage('Please select faces of Scalp Mesh', True, True, 'red')

    clumpMesh = 'clump_' + scalpMesh
    clumpMeshGrp = 'clumpGrp_' + scalpMesh  
    if not cmds.objExists(clumpMeshGrp):
        cmds.group(name = clumpMeshGrp, em = True, parent = cmds.getAttr(currNode + '.mainGroup'))

    if selFaces == len(selFaces):
        clumpMesh = cmds.duplicate(scalpMesh, rr = True, n = clumpMesh)[0]
        cmds.parent(clumpMesh, clumpMeshGrp)

    else:        
        dupScalpMesh = cmds.duplicate(scalpMesh, rr = True)[0]
        
        dupScalpShape = cmds.listRelatives(dupScalpMesh, s = True)[0]
        dupSelFaces = [dupScalpMesh + '.f[' + v.split('.f[')[1] for v in selFaces]
        cmds.select(dupSelFaces, r = True)
        cmds.polyChipOff(ch = True, kft = True, dup = True)
        parts = cmds.polySeparate(dupScalpShape, ch = True)
        parts = [p for p in parts if 'polySeparate' not in p]
        
        if len(parts) > 2:
            cmds.delete(dupScalpMesh)
            reportGBMessage('Please select connected faces', True, True, 'red')
            
        if cmds.polyEvaluate(parts[0], f = True) < scalpFaces:
            extract = parts[0]
        else:
            extract = parts[1]
                        
        clumpMesh = cmds.rename(extract, clumpMesh)
        cmds.setAttr(clumpMesh + '.visibility', False)
#        cmds.polySubdivideFacet(clumpMesh, dv = 2, m = 0, ch = True)
        smoothNode = cmds.polySmooth(clumpMesh, divisions = 1)
        cmds.parent(clumpMesh, clumpMeshGrp)
        cmds.select(cl = True)
        cmds.delete(clumpMesh, ch = True)
        cmds.delete(dupScalpMesh)
    
    cmds.setAttr(currNode + '.clumpMesh', clumpMesh, type = 'string')
    cmds.select(cl = True)
    cmds.selectMode(object = True)
    cmds.setToolTo('selectSuperContext')
    
    clumpScalpMeshDefined()
    
    return clumpMesh                

def clumpScalpMeshDefined():
    
    cmds.button('defineClumpScalp', edit = True, vis = False)
    cmds.button('editClumpScalpBtn', edit = True, vis = True)
    cmds.frameLayout('addRemoveClumpFrm', edit = True, vis = True)
#    createIPSforClump()
    cmds.columnLayout('clumpOptionsLyt', edit = True, vis = True)
    
    
def editClumpScalp():
    
    cmds.button('editClumpScalpBtn', edit = True, vis = False)
    cmds.frameLayout('editClumpScalpFrm' , edit = True, vis = True, cll = False)

def collapseEditClumpScalp():
    
    cmds.frameLayout('editClumpScalpFrm' , edit = True, vis = False, cl = False)
    cmds.button('editClumpScalpBtn', edit = True, vis = True)

    
                
def createIPSforClump():
    
    
    import cPickle as Pickle
    currNode = cmds.getAttr('gbNode.currentGBNode')
    clumpMesh = cmds.getAttr(currNode + '.clumpMesh')
    if not clumpMesh:
#        print 'no clump mesh defined'
        return
    historyDelete = []
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    baseMeshGrp = cmds.getAttr(currNode + '.baseMeshGroup')
    baseMeshGrpChildren = cmds.listRelatives(baseMeshGrp, c = True)
    superGrp = 'superCurves_charInterpolation_' + scalpMesh
    
    if not superGrp in baseMeshGrpChildren:
        reportGBMessage('Ckump Meshes work only on Super Curves. No Super Curves Exist', True, True, 'red')


    superGrpChildren = []    
    superGrpChildren = cmds.listRelatives(superGrp, c = True)      
    
    if not superGrpChildren:
        reportGBMessage('Ckump Meshes work only on Super Curves. No Super Curves Exist', True, True, 'red')
    
    scalpSuperCurvesPos = []
    scalpSuperCurvesPosString = cmds.getAttr(currNode + '.scalpSuperCurvesPos')
    if scalpSuperCurvesPosString:
        scalpSuperCurvesPos = Pickle.loads(str(scalpSuperCurvesPosString))    

    finalScalpPos = []
    if scalpSuperCurvesPos:
#        print 'x[0]'
        finalScalpPos = [x[0] for x in scalpSuperCurvesPos]
    
    else:
        for sup in superGrpChildren:
#            print 'xform'
            finalScalpPos.append(cmds.xform(sup + '.cv[0]', q = True, ws = True, t = True))
    vtxSel = []
    clumpCPNode = createCPNode(clumpMesh)
    historyDelete.append(clumpCPNode)
    scalpCPNode = createCPNode(scalpMesh)
    historyDelete.append(scalpCPNode)
    ips = []
    ipsPos = []
    ipsString = cmds.getAttr(currNode + '.ips')        
    
    
    if ipsString:
        ips = Pickle.loads(str(ipsString))        

        
    currIPS = []
    scalpMeshDISP = scalpMesh + '_DISPLAY'
    
    i3DGrp = 'charInterpolation_' + scalpMesh
    ipolCurves = []
    baseMeshGrp = cmds.getAttr(currNode + '.baseMeshGroup')
    baseMeshGrpChildren = cmds.listRelatives(baseMeshGrp, c = True)
    if i3DGrp in baseMeshGrpChildren: 
        ipolCurves = cmds.listRelatives(cmds.listRelatives(i3DGrp, ad = True, typ = 'nurbsCurve'), p = True)
        usedIpolVertices = [i.split('ipol3DCrv_' + scalpMesh + 'vtx_')[1] for i in ipolCurves if 'ipol3DCrv_' in i]
        
        
    for pos in finalScalpPos:
        cmds.setAttr(clumpCPNode + '.ip', pos[0], pos[1], pos[2])
        dist = distance3d(pos, list(cmds.getAttr(clumpCPNode + '.p')[0]))
        if dist > 0.3:
#            print 'extra dist', dist
            continue
        cmds.setAttr(scalpCPNode + '.ip', pos[0], pos[1], pos[2])
        vtxID = cmds.getAttr(scalpCPNode + '.vt') 
        currIPS.append(vtxID)
        if vtxID not in ips:
            if not vtxID in usedIpolVertices:
                vtxSel.append(scalpMeshDISP + '.vtx[' + str(vtxID) + ']')
    
#    print currIPS
    ipsString = Pickle.dumps(currIPS)    
    
    cmds.setAttr(currNode + '.ips', ipsString, type = 'string')

#    print vtxSel
    if vtxSel:
        generateNewIPS(vtxSel)
    
    
    for h in historyDelete:
        if cmds.objExists(h):
            cmds.delete(h)
        
        
def generateNewIPS(vtxSel):
    
    currNode = cmds.getAttr('gbNode.currentGBNode')
    lastState = cmds.getAttr(currNode + '.lastState')
    if 'graph' in lastState:
        cmds.setAttr(currNode + '.isGraphRestored', True)
        cmds.tabLayout('mainTabs', edit = True, sti = 1)        
        tabSelectChange()
        cmds.tabLayout('mainTabs', edit = True, sti = 2)                
        tabSelectChange()
        continueForGraph()
        autoResize()
        cmds.setAttr(currNode + '.isGraphRestored', False)        
        
    else:
        cmds.select(vtxSel, r = True)
        charInterpolationSelectedFaces()
                

def updateGBClumpMeshes():
    
    import cPickle as Pickle
    currNode = cmds.getAttr('gbNode.currentGBNode')
    clumpMesh = cmds.getAttr(currNode + '.clumpMesh')
    dupClumpMesh = cmds.duplicate(clumpMesh, rr = True)[0]
    historyDelete = []
    if not clumpMesh:
        return
    
    ips = []        
    ipsString = cmds.getAttr(currNode + '.ips')
    if ipsString:
        ips = Pickle.loads(str(ipsString))
    
    if not ips:
        return
    
    clumpCurves = []        
    clumpCurvesFlatPos = []
    
    clumpCurvesString = cmds.getAttr(currNode + '.clumpCurves')
    if clumpCurvesString:
        clumpCurves = Pickle.loads(str(clumpCurvesString))
        clumpVertices = Pickle.loads(str(cmds.getAttr(currNode + '.clumpVertices')))
    if cmds.getAttr(currNode + '.clumpCurvesFlatPos'):
        clumpCurvesFlatPos = Pickle.loads(str(cmds.getAttr(currNode + '.clumpCurvesFlatPos')))
        
            
    toBeUpdatedClumps = []
#    toBeUpdatedClumpsString = cmds.getAttr(currNode + '.toBeUpdatedClumps')
#    if toBeUpdatedClumpString:
#        toBeUpdatedClumps = Pickle.loads(str(toBeUpdatedClumps))
    
    
    
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')        

                      
    commonClumps = list(set(ips) & set(clumpCurves))
    removeClumps = []
    addClumps = []
    if commonClumps:
        for ipol in commonClumps:
            ipolName = ('ipol3DCrv_' + scalpMesh + 'vtx_' + str(ipol))
            currRoot = cmds.xform(ipolName + '.cv[0]', q = True, ws = True, t = True)
            clumpCurvesIndex = clumpCurves.index(ipol)
#            print clumpCurvesIndex
            clumpRoot = clumpCurvesFlatPos[clumpCurvesIndex][0]
#            print currRoot, clumpRoot
            if not currRoot == clumpRoot:
                removeClumps.append(ipol)
                addClumps.append(ipol)
           
#            if not ipol:
#                a = 1     
            else:
                dg = cmds.getAttr(ipolName + '.degree')
                sp = cmds.getAttr(ipolName + '.spans')
                ncv = dg + sp
                if ncv == len(clumpCurvesFlatPos[clumpCurvesIndex]):
                    clumpCurvePosCVs = clumpCurvesFlatPos[clumpCurvesIndex]
                    for i in range(1,ncv):
                        if cmds.xform(ipolName + '.cv[' + str(i) + ']', q = True, ws = True, t = True) <> clumpCurvePosCVs[i]:
                            toBeUpdatedClumps.append(ipol)
                            break
                else:
                    toBeUpdatedClumps.append(ipol)                            
                            
#    print 'tobeupdate', toBeUpdatedClumps                       
    removeClumps = list(set(clumpCurves) - set(ips))
    if removeClumps:
        removeClumpsExec(removeClumps)

    addClumps = list(set(ips) - set(clumpCurves))
    if addClumps:
        addClumpsExec(addClumps)
    
    toCheck = False
    toBeCheckedVertices = []
    if removeClumps:
        if clumpVertices:
            toCheck = True
            for clump in removeClumps:
                index = clumpCurves.index(clump)
                toBeCheckedVertices.extend(clumpVertices[index])
                
    
    skinClumpVertices = createClumpRegions()
    clumpCurves = Pickle.loads(str(cmds.getAttr(currNode + '.clumpCurves')))
    clumpVertices = Pickle.loads(str(cmds.getAttr(currNode + '.clumpVertices')))
    clumpBasePos = Pickle.loads(str(cmds.getAttr(currNode + '.clumpBasePos')))
    toBeExtractedClumps = []
#    print 'addclumps' , addClumps
    toBeExtractedClumps.extend(addClumps)
    
    toBeCheckedVertices = []
    
    
    if addClumps:
        if len(addClumps) == len(ips):
            toBeExtractedClumps = addClumps
        else:    
            toCheck = True
            for clump in addClumps:
                toBeCheckedVertices.extend(skinClumpVertices[ips.index(clump)])
    
    toBeCheckedVertices = list(set(toBeCheckedVertices))
    
    
    if toCheck:
        for vtx in toBeCheckedVertices:
            for vclump in range(len(clumpVertices)):
                if vtx in clumpVertices[vclump]:
                    clumpName = clumpCurves[vclump]
                    if clumpName not in toBeExtractedClumps:
                        toBeExtractedClumps.append(clumpName)
                        break

#    print toBeExtractedClumps
    toBeExtractedClumps = list(set(toBeExtractedClumps))
    
    
    totalPart = []   
    cmds.setAttr(clumpMesh + '.visibility', True)
    cmds.select(cl = True)
#    print 'ips', ips
#    print 'clumpcurves', clumpCurves
    
    from random import randint
    totalE = cmds.polyEvaluate(clumpMesh, e = True)
    distance = []
    for i in range(5):
        e = randint(0,totalE)
        edgePos = cmds.xform(clumpMesh + '.e[' + str(e) + ']', q = True, ws = True, t = True)
        distance.append(distance3d(edgePos[0:3], edgePos[3:6]))
    dist = sum(distance) / len(distance)
    offset = (dist / 2) * -1
#    print distance, offset
#cmds.xform('Demo_Face.e[10]', q = True, ws = True, t = True)
        
    clumpCPNode = createCPNode(clumpMesh)
    historyDelete.append(clumpCPNode)

#    print 'tobeExtracted'    
    for clump in toBeExtractedClumps:
#        dupClumpMesh = cmds.duplicate(clumpMesh, rr = True)[0]
        index = ips.index(clump)
        clumpIndex = clumpCurves.index(clump)
        vertices = skinClumpVertices[clumpIndex]
        verticesName = [clumpMesh + '.vtx[' + str(v) + ']' for v in vertices]
#        verticesName = cmds.ls(sl = True, fl = True)
        toFaces = cmds.ls(cmds.polyListComponentConversion(verticesName, ff = True, fv = True, tf = True, internal = True), fl = True)
#        dupMeshFaces = [face.replace(clumpMesh, dupClumpMesh) for face in toFaces]

#        cmds.select(dupMeshFaces, r = True)        
#        mm.eval('PolySelectTraverse 1;')
        cmds.polyChipOff(toFaces, kft = True, dup = False)
        cmds.select(toFaces, r = True)
#        toEdges = cmds.ls(cmds.polyListComponentConversion(verticesName, ff = True, fv = True, te = True, internal = True), fl = True)
        mm.eval('PolySelectConvert 20;')
        mm.eval('ConvertSelectionToShellBorder;')
        #polyConvertToShellBorder;
        
        
#        cmds.select(verticesName, r = True)
#        mm.eval('PolySelectTraverse 3;')
#        mm.eval('PolySelectConvert 20;')
#        borderE = cmds.ls(sl = True, fl = True)        
#        verticesName = cmds.ls(sl = True)
#        cmds.select(borderV, r = True)

        
#        borderE = cmds.ls(cmds.polyListComponentConversion(borderV, fv = True, te = True, internal = True), fl = True)
#        totalPart.append(verticesName)
#        cmds.select(borderE, add = True)
        baseCrvLinear = cmds.polyToCurve(form = 1, degree = 1)[0]
        baseCrv = cmds.offsetCurve(baseCrvLinear, rn = True, cb = 1, cl = False, d = offset, ugn = False)[0]
        cmds.delete(baseCrv, ch = True)
        cmds.delete(baseCrvLinear)
        newName = 'baseCurve_' + scalpMesh + '_' + str(clump)
        cmds.rename(baseCrv, newName)
        historyDelete.append(newName)        
#        offsetCurve  -ch on -rn true -cb 1 -st true -cl false -d -0.15 -tol 3.53146e-007 -sd 5 -ugn false  "baseCurve_Demo_Face_905" ;
        
        dg = cmds.getAttr(newName + '.degree')
        sp = cmds.getAttr(newName + '.spans')
        ncv = dg + sp
        allPos = []
        rootPos = []
        for cv in range(ncv):
            pos = cmds.xform(newName + '.cv[' + str(cv) + ']', q = True, ws = True, t = True)

            cmds.setAttr(clumpCPNode + '.ip', pos[0], pos[1],pos[2])
            if cv == 0:
                rootPos = list(cmds.getAttr(clumpCPNode + '.p')[0])
            allPos.append(list(cmds.getAttr(clumpCPNode + '.p')[0]))
        allPos.append(rootPos)                    
        clumpBasePos[clumpIndex] = allPos

    
#    print 'clumpbaes', clumpBasePos
    clumpBasePosString = Pickle.dumps(clumpBasePos)
    
    cmds.setAttr(currNode + '.clumpBasePos', clumpBasePosString, type = 'string')            
    
    toBeExtractedClumps.extend(toBeUpdatedClumps)
#    print 'final tobeextract', toBeUpdatedClumps, toBeExtractedClumps
    createFreshClumpMesh(toBeExtractedClumps)    

    cmds.delete(clumpMesh)
    cmds.rename(dupClumpMesh, clumpMesh)
    for h in historyDelete:
        if cmds.objExists(h):
            cmds.delete(h)
            
        
def createFreshClumpMesh(clumps):
    
    import cPickle as Pickle
    currNode = cmds.getAttr('gbNode.currentGBNode')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    
    if not clumps:
        return
#    print 'craete fresh', clumps    
    clumpGrp = 'clumpGrp_' + scalpMesh
    
    clumpCurves = Pickle.loads(str(cmds.getAttr(currNode + '.clumpCurves')))
    clumpSurfaces = Pickle.loads(str(cmds.getAttr(currNode + '.clumpSurfaces')))
    clumpVertices = Pickle.loads(str(cmds.getAttr(currNode + '.clumpVertices')))
    clumpBasePos = Pickle.loads(str(cmds.getAttr(currNode + '.clumpBasePos')))
    clumpCurvesFlatPos = Pickle.loads(str(cmds.getAttr(currNode + '.clumpCurvesFlatPos')))
    clumpScaleGraph = Pickle.loads(str(cmds.getAttr(currNode + '.clumpScaleGraph')))
    clumpFlatness = Pickle.loads(str(cmds.getAttr(currNode + '.clumpFlatness')))
    clumpSectionsU = Pickle.loads(str(cmds.getAttr(currNode + '.clumpSectionsU')))
    clumpSpansV = Pickle.loads(str(cmds.getAttr(currNode + '.clumpSpansV')))
    
    historyDelete = []    
    for clump in clumps:
        clump = int(clump)
        index = clumpCurves.index(clump)
        clumpName = 'ipol3DCrv_' + scalpMesh + 'vtx_' + str(clump)
        ncv = cmds.getAttr(clumpName + '.degree') + cmds.getAttr(clumpName + '.spans')
        allPos = []
        for cv in range(ncv):
            allPos.append(cmds.xform(clumpName + '.cv[' + str(cv) + ']', q = True, ws = True, t = True))
        clumpCurvesFlatPos[index] = allPos
            
        basePos = clumpBasePos[index]
#        print 'basepos', basePos
        baseCrv = cmds.curve(p = basePos, degree = 1, per = True, k = range(len(basePos)))
        u = clumpSectionsU[index]
#        cmds.rebuildCurve(baseCrv, ch = False, s = 50)
#        cmds.smoothCurve(baseCrv + '.cv[*]', s = 1)
        cmds.rebuildCurve(baseCrv, ch = False, s = 30)
        surfaceName = 'clumpSurface_' + scalpMesh + '_' + str(clump)
        if cmds.objExists(surfaceName):
            cmds.delete(surfaceName)
        surfaceName = cmds.extrude(baseCrv, clumpName, name = surfaceName, po = 0, sc = 0.01, et=2 )[0]
        cmds.parent(surfaceName, clumpGrp)
        cmds.delete(surfaceName, ch = True)
#        print baseCrv, clumpName, surfacName
        historyDelete.append(baseCrv)
        clumpSurfaces[index] = surfaceName
        
    
    
    clumpSurfacesString = Pickle.dumps(clumpSurfaces)
    clumpCurvesFlatPosString = Pickle.dumps(clumpCurvesFlatPos)
    cmds.setAttr(currNode + '.clumpSurfaces', clumpSurfacesString, type = 'string')
    cmds.setAttr(currNode + '.clumpCurvesFlatPos' , clumpCurvesFlatPosString, type = 'string')
        
    if historyDelete:
        for h in historyDelete:
            if cmds.objExists(h):
                cmds.delete(h)
    
def removeClumpsExec(removeClumps):
    
    import cPickle as Pickle
    currNode = cmds.getAttr('gbNode.currentGBNode')
    
    clumpCurves = Pickle.loads(str(cmds.getAttr(currNode + '.clumpCurves')))
    clumpSurfaces = Pickle.loads(str(cmds.getAttr(currNode + '.clumpSurfaces')))
    clumpVertices = Pickle.loads(str(cmds.getAttr(currNode + '.clumpVertices')))
    clumpBasePos = Pickle.loads(str(cmds.getAttr(currNode + '.clumpBasePos')))
    clumpCurvesFlatPos = Pickle.loads(str(cmds.getAttr(currNode + '.clumpCurvesFlatPos')))    
    clumpScaleGraph = Pickle.loads(str(cmds.getAttr(currNode + '.clumpScaleGraph')))
    clumpFlatness = Pickle.loads(str(cmds.getAttr(currNode + '.clumpFlatness')))
    clumpSectionsU = Pickle.loads(str(cmds.getAttr(currNode + '.clumpSectionsU')))
    clumpSpansV = Pickle.loads(str(cmds.getAttr(currNode + '.clumpSpansV')))
    
    
    removeIDList = []
    for clump in removeClumps:
        ind = clumpCurves.index(clump)
        removeIDList.append(ind)
#        print clumpSurfaces[ind]
        if cmds.objExists(clumpSurfaces[ind]):
            cmds.delete(clumpSurfaces[ind])
    
    clumpCurves = [x for y, x in enumerate(clumpCurves) if y not in removeIDList]     
    clumpSurfaces = [x for y, x in enumerate(clumpSurfaces) if y not in removeIDList] 
    clumpVertices = [x for y, x in enumerate(clumpVertices) if y not in removeIDList] 
    clumpBasePos = [x for y, x in enumerate(clumpBasePos) if y not in removeIDList] 
    clumpCurvesFlatPos = [x for y, x in enumerate(clumpCurvesFlatPos) if y not in removeIDList] 
    clumpScaleGraph = [x for y, x in enumerate(clumpScaleGraph) if y not in removeIDList]                
    clumpFlatness = [x for y, x in enumerate(clumpFlatness) if y not in removeIDList] 
    clumpSectionsU = [x for y, x in enumerate(clumpSectionsU) if y not in removeIDList] 
    clumpSpansV = [x for y, x in enumerate(clumpSpansV) if y not in removeIDList] 
    
    
    clumpCurvesString = Pickle.dumps(clumpCurves)
    clumpSurfacesString = Pickle.dumps(clumpSurfaces)
    clumpVerticesString = Pickle.dumps(clumpVertices)
    clumpBasePosString = Pickle.dumps(clumpBasePos)
    clumpCurvesFlatPosString = Pickle.dumps(clumpCurvesFlatPos)
    clumpScaleGraphString = Pickle.dumps(clumpScaleGraph)
    clumpFlatnessString = Pickle.dumps(clumpFlatness)
    clumpSectionsUString = Pickle.dumps(clumpSectionsU)
    clumpSpansVString = Pickle.dumps(clumpSpansV)    
            
    
    cmds.setAttr(currNode + '.clumpCurves', clumpCurvesString, type = 'string')
    cmds.setAttr(currNode + '.clumpSurfaces', clumpSurfacesString, type = 'string')
    cmds.setAttr(currNode + '.clumpVertices', clumpVerticesString, type = 'string')
    cmds.setAttr(currNode + '.clumpBasePos', clumpBasePosString, type = 'string')
    cmds.setAttr(currNode + '.clumpCurvesFlatPos', clumpCurvesFlatPosString, type = 'string')
    cmds.setAttr(currNode + '.clumpScaleGraph', clumpScaleGraphString, type = 'string')
    cmds.setAttr(currNode + '.clumpFlatness', clumpFlatnessString, type = 'string')
    cmds.setAttr(currNode + '.clumpSectionsU', clumpSectionsUString, type = 'string')
    cmds.setAttr(currNode + '.clumpSpansV', clumpSpansVString, type = 'string')
    
    
    
        
        
def addClumpsExec(addClumps):
    
    import cPickle as Pickle
    currNode = cmds.getAttr('gbNode.currentGBNode')

    clumpCurves = []
    clumpSurfaces = []
    clumpVertices = []
    clumpBasePos = []
    clumpCurvesFlatPos = []
    clumpScaleGraph = []
    clumpFlatness = []
    clumpSectionsU = []
    clumpSpansV = []
                    
    if cmds.getAttr(currNode + '.clumpCurves'):
        clumpCurves = Pickle.loads(str(cmds.getAttr(currNode + '.clumpCurves')))
        clumpSurfaces = Pickle.loads(str(cmds.getAttr(currNode + '.clumpSurfaces')))
        clumpVertices = Pickle.loads(str(cmds.getAttr(currNode + '.clumpVertices')))
        clumpBasePos = Pickle.loads(str(cmds.getAttr(currNode + '.clumpBasePos')))
        clumpCurvesFlatPos = Pickle.loads(str(cmds.getAttr(currNode + '.clumpCurvesFlatPos')))
        clumpScaleGraph = Pickle.loads(str(cmds.getAttr(currNode + '.clumpScaleGraph')))
        clumpFlatness = Pickle.loads(str(cmds.getAttr(currNode + '.clumpFlatness')))
        clumpSectionsU = Pickle.loads(str(cmds.getAttr(currNode + '.clumpSectionsU')))
        clumpSpansV = Pickle.loads(str(cmds.getAttr(currNode + '.clumpSpansV')))
    
            
    for clump in addClumps:
        clumpCurves.append(clump)
        clumpSurfaces.append([])
        clumpVertices.append([])
        clumpBasePos.append([])
        clumpCurvesFlatPos.append([])
        clumpScaleGraph.append(cmds.gradientControlNoAttr('clumpScaleGraph', q = True, asString = True))
        if not cmds.checkBox('clumpFlatCheck', q = True, v = True):
            flat = -1
        else:
            flat = cmds.intSliderGrp('clumpFlatSlider', q = True, v = True)                   
        clumpFlatness.append(flat)
        clumpSectionsU.append(cmds.intFieldGrp('clumpSpansField', q = True, v1 = True))
        clumpSpansV.append(cmds.intFieldGrp('clumpSectionsField', q = True, v1 = True))
    
    clumpCurvesString = Pickle.dumps(clumpCurves)
    clumpSurfacesString = Pickle.dumps(clumpSurfaces)
    clumpVerticesString = Pickle.dumps(clumpVertices)
    clumpBasePosString = Pickle.dumps(clumpBasePos)
    clumpCurvesFlatPosString = Pickle.dumps(clumpCurvesFlatPos)
    clumpScaleGraphString = Pickle.dumps(clumpScaleGraph)
    clumpFlatnessString = Pickle.dumps(clumpFlatness)
    clumpSectionsUString = Pickle.dumps(clumpSectionsU)
    clumpSpansVString = Pickle.dumps(clumpSpansV)    
            
    
    cmds.setAttr(currNode + '.clumpCurves', clumpCurvesString, type = 'string')
    cmds.setAttr(currNode + '.clumpSurfaces', clumpSurfacesString, type = 'string')
    cmds.setAttr(currNode + '.clumpVertices', clumpVerticesString, type = 'string')
    cmds.setAttr(currNode + '.clumpBasePos', clumpBasePosString, type = 'string')
    cmds.setAttr(currNode + '.clumpCurvesFlatPos', clumpCurvesFlatPosString, type = 'string')
    cmds.setAttr(currNode + '.clumpScaleGraph', clumpScaleGraphString, type = 'string')
    cmds.setAttr(currNode + '.clumpFlatness', clumpFlatnessString, type = 'string')
    cmds.setAttr(currNode + '.clumpSectionsU', clumpSectionsUString, type = 'string')
    cmds.setAttr(currNode + '.clumpSpansV', clumpSpansVString, type = 'string')

def createClumpRegionsOLD():
    
    import cPickle as Pickle
    currNode = cmds.getAttr('gbNode.currentGBNode')
    clumpMesh = cmds.getAttr(currNode + '.clumpMesh')
    ips = []
    ipsString = cmds.getAttr(currNode + '.ips')
    if ipsString:
        ips = Pickle.loads(str(ipsString))
    
    historyDelete = []
    clumpVertices = []
    clumpCurves = []
    
    clumpVerticesString = cmds.getAttr(currNode + '.clumpVertices')
    if clumpVerticesString:
        clumpCurves = Pickle.loads(str(cmds.getAttr(currNode + '.clumpCurves')))
        clumpVertices = Pickle.loads(str(clumpVerticesString))
    
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')

    jointList = []
    for ipol in clumpCurves:
        ipolCrv = 'ipol3DCrv_' + scalpMesh + 'vtx_' + str(ipol)
        rootPos = cmds.xform(ipolCrv + '.cv[0]', q = True, ws = True, t = True)
        cmds.select(cl = True)
        cmds.joint(p = (rootPos[0], rootPos[1], rootPos[2]), n = ('jointClump_' + str(ipol)))
        jName = cmds.ls(sl = True)[0]
        jointList.append(jName)
        cmds.setAttr(jName + '.visibility', False)
        historyDelete.append(jName)
        
    clustName = mm.eval('findRelatedSkinCluster(' + dQ + clumpMesh + dQ + ');')
    if clustName:
        cmds.delete(clustName)
    cmds.select(jointList, clumpMesh)
    tempGBNode = cmds.getAttr('gbNode.tempGBNode')
#    smoothNode = cmds.polySmooth(clumpMesh, divisions = 1)
#    print 'SMMOOTH'
#    cmds.polySubdivideFacet(clumpMesh, dv = 1, m = 0, ch = True)
#    polySubdivideFacet -dv 1 -m 0 -ch 1 polySurface2;
    cmds.delete(clumpMesh, ch = True)
    cmds.select(jointList, clumpMesh)
    clustName = cmds.skinCluster(name = tempGBNode, dr = 0.0, mi = 1, sm = 1 )[0]
    
    totalJointList = cmds.skinCluster(clustName, q = True, inf = True)        
    
    totalV = cmds.polyEvaluate(clumpMesh, v = True)
    
    skinClumpVertices = []
    for i in clumpCurves:
        skinClumpVertices.append([])    
       
    for vtx in range(totalV):
        vertex = clumpMesh + '.vtx[' + str(vtx) + ']'
        jointName = totalJointList[cmds.skinPercent(clustName , vertex, query=True, value=True ).index(1.0)]
        clumpID = int(jointName.split('jointClump_')[1])
        clumpIndex = clumpCurves.index(clumpID)
        skinClumpVertices[clumpIndex].append(vtx)
    
    clumpVerticesString = Pickle.dumps(skinClumpVertices)
    cmds.setAttr(currNode + '.clumpVertices', clumpVerticesString, type = 'string')
    
    cmds.skinCluster(clustName, edit = True, ub = True)
    
    if historyDelete:
        for h in historyDelete:
            if cmds.objExists(h):
                cmds.delete(h)
                
    return skinClumpVertices
    
    
    
def checkForClumpUpdateOLD(toBeResize):
    
    import cPickle as Pickle
    currNode = cmds.getAttr('gbNode.currentGBNode')
    clumpMesh = cmds.getAttr(currNode + '.clumpMesh')
    if not clumpMesh:
        return
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    curveList = [] 
    curveList4GraphString = cmds.getAttr(currNode + '.curveList4Graph')
    curveList = Pickle.loads(str(curveList4GraphString))
    if not curveList:
        return
    ips = []
    ipsString = cmds.getAttr(currNode + '.ips')
    ipsNotEmpty = False
    if ipsString:
        ips = Pickle.loads(str(ipsString))
        ipsNotEmpty = True
    
    if ipsNotEmpty:
        updateGBClumpMeshes()
            
       
    clumpCurves = []
    clumpCurvesString = cmds.getAttr(currNode + '.clumpCurves')
    if clumpCurvesString:
        clumpCurves = Pickle.loads(str(clumpCurvesString))
    
    if not clumpCurves:
        return    
            
    clumpCurvesNames = ['ipol3DCrv_' + scalpMesh + 'vtx_' + str(c) for c in clumpCurves]
    toBeResizeNames = convertIDToCurveList(toBeResize)
    toBeChangedClumps = []
    toBeChangedClumps = list(set(toBeResizeNames) & set(clumpCurvesNames))
    
    
    createFreshClumpMesh(convertCurveToIDList(toBeChangedClumps))


def setClumpMeshVisibility(mode):
    
    import cPickle as Pickle
    currNode = cmds.getAttr('gbNode.currentGBNode')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    mainGrp = cmds.getAttr(currNode + '.mainGroup')
    clumpGrp = 'clumpGrp_' + scalpMesh
    if clumpGrp in cmds.listRelatives(mainGrp, c = True):
        cmds.setAttr(clumpGrp + '.visibility', mode)
    
def addRegionPerIpol():
    
    import cPickle as Pickle
    currNode = cmds.getAttr('gbNode.currentGBNode')
    
#    selected = cmds.ls(sel = True)
#    if not selected:
#        reportGBMessage('Please select clump surfaces', True, True, 'red')
        
    clumpCurves = Pickle.loads(str(cmds.getAttr(currNode + '.clumpCurves')))
    clumpSurfaces = Pickle.loads(str(cmds.getAttr(currNode + '.clumpSurfaces')))
    clumpCurvesFlatPos = Pickle.loads(str(cmds.getAttr(currNode + '.clumpCurvesFlatPos')))
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    for clump in clumpCurves:
        cmds.select(cmds.ls(cmds.polyListComponentConversion(scalpMesh + '.vtx[' + str(clump) + ']', fv = True, tf = True),fl = True)[0], r = True)
        addRegionCtrl()
    
        
       
def switchToScalpMeshForMapping():
    
    
    currNode = cmds.getAttr('gbNode.currentGBNode')
    paintMesh = cmds.getAttr(currNode + '.paintOnMesh')
    
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    volMesh = cmds.getAttr(currNode + '.volumeMesh')
    lastPaintMesh = paintMesh    
    
    if not cmds.objExists(currNode + '.lastPaintMesh'):
        cmds.addAttr(currNode, ln = 'lastPaintMesh', dt = 'string')
    else:
        lastPaintMesh = cmds.getAttr(currNode + '.lastPaintMesh')        

    if paintMesh == volMesh:
        cmds.setAttr(currNode + '.lastPaintMesh', paintMesh, type = 'string')
        switchCurvesToOtherMesh()
        cmds.setAttr(currNode + '.paintOnMesh', scalpMesh, type = 'string')
        cmds.setAttr('gbNode.activeMesh', scalpMesh, type = 'string')        

def switchToVolumeMeshForMapping():
    
    
    currNode = cmds.getAttr('gbNode.currentGBNode')
    paintMesh = cmds.getAttr(currNode + '.paintOnMesh')
    
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    volMesh = cmds.getAttr(currNode + '.volumeMesh')
    
    if not cmds.objExists(currNode + '.lastPaintMesh'):
        return
    
    else:
        lastPaintMesh = cmds.getAttr(currNode + '.lastPaintMesh')        
        if lastPaintMesh == scalpMesh:
            cmds.setAttr(currNode + '.lastPaintMesh', '', type = 'string')
            switchCurvesToOtherMesh()
            cmds.setAttr(currNode + '.paintOnMesh', volMesh, type = 'string')
            cmds.setAttr('gbNode.activeMesh', volMesh, type = 'string')        

            
                
        
def interPercentChanged():
    
    n = int(cmds.intField('interPercentField', q = True, v = True))
    gap = 5
    if (n % gap):
        n = n + (gap - n % gap)
    cmds.intField('interPercentField', edit = True, v = n)
    message = 'Run Interpolation on ' + str(n) + '% of Selected Area'
    cmds.button('interCharBtn', edit = True, label = message)
               
def loadPreviousSelectionForIpol():
    
    import cPickle as Pickle
    currNode = cmds.getAttr('gbNode.currentGBNode')
    lastIpol = []
    if not cmds.objExists(currNode + '.lastIpolSelection'):
        cmds.addAttr(currNode, ln = 'lastIpolSelection', dt = 'string')
    else:
        lastIpolString = cmds.getAttr(currNode + '.lastIpolSelection')
        if lastIpolString:
            lastIpol = Pickle.loads(str(lastIpolString))
            
    if not lastIpol:
        reportGBMessage('No Selections exist', True, True, 'red')
    
    if '.f[' in lastIpol[0]:
        loadPaintForIpol('Facet')
    else:
        loadPaintForIpol('Point')
    
    cmds.select(lastIpol, r = True)
    
def filterIpolSelection(origSel):
    
    import random
    random.seed(9)
    newList = []
    newList.extend(origSel)
    random.shuffle(newList)
    
    per = int(cmds.intField('interPercentField', q = True, v = True))
    total = len(origSel)
    slice = int(total * (per / 100.0))
    finalList = newList[:slice]

    return finalList
    
def freeFormCurvesForVolume():
    
    currNode = cmds.getAttr('gbNode.currentGBNode')
    
    baseMeshGroup = cmds.getAttr(currNode + '.baseMeshGroup')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
  
    manualGroup = 'manualCurvesGrp_' + scalpMesh
    manualGrpChildren = []
    baseMeshGrpChildren = cmds.listRelatives(baseMeshGroup, c = True)
    if baseMeshGrpChildren:
        if manualGroup in baseMeshGrpChildren:
            manualGrpChildren = cmds.listRelatives(manualGroup, c = True)
            if manualGrpChildren:
                cmds.select(manualGrpChildren, r = True)
                curvesForVolume()
    if not manualGrpChildren:
        reportGBMessage('No Freeform Curves Exist', True, True, 'red')    
                
def freeformCurvesRenderDisplayLayer():
    
    sel = cmds.ls(sl = True)
    currNode = cmds.getAttr('gbNode.currentGBNode')
    
    baseMeshGroup = cmds.getAttr(currNode + '.baseMeshGroup')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
  
    manualGroup = 'manualCurvesGrp_' + scalpMesh
    baseMeshGrpChildren = cmds.listRelatives(baseMeshGroup, c = True)
    if baseMeshGrpChildren:
        if manualGroup in baseMeshGrpChildren:
            dispLayers = cmds.ls(type = 'displayLayer')
    
            if not scalpMesh + '_charFreeform_Curves'  in dispLayers:
                cmds.select(manualGroup, r = True)
                dispLayer = cmds.createDisplayLayer(n = scalpMesh + '_charFreeform_Curves' )    
                cmds.setAttr(dispLayer + '.displayType', 2)
    
    if sel:
        cmds.select(sel, r = True)
    else:
        cmds.select(cl = True)                        

                
def freeformCurvesNormalDisplayLayer():  

    currNode = cmds.getAttr('gbNode.currentGBNode')
    
    baseMeshGroup = cmds.getAttr(currNode + '.baseMeshGroup')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
  
    dispLayers = cmds.ls(type = 'displayLayer')
    ffLayer = scalpMesh + '_charFreeform_Curves' 
    if ffLayer in dispLayers:
        cmds.delete(ffLayer)
        
    manualGroup = 'manualCurvesGrp_' + scalpMesh
    baseMeshGrpChildren = cmds.listRelatives(baseMeshGroup, c = True)
    if baseMeshGrpChildren:
        if manualGroup in baseMeshGrpChildren:
            manualGroupChildren = cmds.listRelatives(cmds.listRelatives(manualGroup, ad = True, typ = 'nurbsCurve'), p = True)
            if manualGroupChildren:
                for manual in manualGroupChildren:
                    selShp = cmds.listRelatives(manual, s = True)[0]
                    cmds.setAttr(selShp + '.overrideEnabled', True)
                    cmds.setAttr(selShp + '.overrideColor', 18)
            
       
def toggleRootPositionMarkers():
    
    currNode = cmds.getAttr('gbNode.currentGBNode')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    baseGrp = cmds.getAttr(currNode + '.baseMeshGroup')
    superGrp = 'superCurves_charInterpolation_' + scalpMesh
    freeformGrp = 'manualCurvesGrp_' + scalpMesh
    baseGrpChildren = cmds.listRelatives(baseGrp, c = True)
    superCurves = []
    freeformCurves = []
    
    markerGrp = deleteMarkersForCurves()
    if markerGrp:
        cmds.delete(markerGrp)
        return
    
    if baseGrpChildren:
        if superGrp in baseGrpChildren:
            superGrpChildren = cmds.listRelatives(superGrp, c = True)
            if superGrpChildren:
                superCurves = cmds.listRelatives(cmds.listRelatives(superGrp, ad = True, typ = 'nurbsCurve'), p = True)
        
        if freeformGrp in baseGrpChildren:
            freeformGrpChildren = cmds.listRelatives(freeformGrp, c = True)
            if freeformGrpChildren:
                freeformCurves = cmds.listRelatives(cmds.listRelatives(freeformGrp, ad = True, typ = 'nurbsCurve'), p = True) 
                
    createMarkersForCurves([superCurves,freeformCurves])
    cmds.select(cl = True)

    
def createMarkersForCurves(allCurves):
    
    currNode = cmds.getAttr('gbNode.currentGBNode')
    paintMesh = cmds.getAttr(currNode + '.paintOnMesh')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    volMesh = cmds.getAttr(currNode + '.volumeMesh')
    baseMeshGrp = cmds.getAttr(currNode + '.baseMeshGroup')
    baseMeshGrpChildren = cmds.listRelatives(baseMeshGrp, c = True)
    
    superCurves = allCurves[0]
    ffCurves = allCurves[1]
    if superCurves or ffCurves:
        markerGrp = 'markerGroup_' + scalpMesh
        if not markerGrp in baseMeshGrpChildren:
#            print '>>>>',markerGrp
            cmds.group(name = markerGrp, em = True, parent = baseMeshGrp)
        cmds.setAttr(markerGrp + '.visibility', True)
         
    historyDelete = []
    if superCurves:
        markerScale = getMarkerScale(paintMesh)
        
        scalpFoll = createFollicleOtherMesh(paintMesh)
        charCPNode = createCPNode(paintMesh)
        historyDelete.append(charCPNode)
        historyDelete.append(scalpFoll)
    
        scalpFollShp = cmds.listRelatives(scalpFoll, s = True)[0]
        
        marker = createTemplateMarker()
        historyDelete.append(marker)
        for crv in superCurves:
            markerName = 'marker_' + crv
            if cmds.objExists(markerName):
                cmds.delete(markerName)
                
            markerDup = cmds.duplicate(marker, name =  markerName, rr = True)[0]
            
            cmds.rename(markerDup, markerName)
            pos = cmds.xform(crv + '.cv[0]', q = True, ws = True, t = True)
            
            cmds.setAttr(charCPNode + '.ip', pos[0], pos[1], pos[2])
            cmds.setAttr(scalpFollShp + '.parameterU', cmds.getAttr(charCPNode + '.u'))
            cmds.setAttr(scalpFollShp + '.parameterV', cmds.getAttr(charCPNode + '.v'))
            pc = cmds.parentConstraint(scalpFoll, markerDup)
            cmds.delete(pc)
            cmds.parent(markerDup, markerGrp)
            cmds.scale( markerScale, markerScale, markerScale, markerDup, xyz = True, a = True)
            cmds.setAttr(markerDup + '.overrideEnabled', 1)
            cmds.setAttr(markerDup + '.overrideDisplayType', 2) 
            cmds.makeIdentity(markerDup, apply = True)
            
    
    if ffCurves:
        
        markerScale = getMarkerScale(scalpMesh)
        
        scalpFoll = createFollicleOtherMesh(scalpMesh)
        charCPNode = createCPNode(scalpMesh)
        historyDelete.append(scalpFoll)
        historyDelete.append(charCPNode)
        scalpFollShp = cmds.listRelatives(scalpFoll, s = True)[0]
        
        marker = createTemplateMarker()
        historyDelete.append(marker)
        for crv in ffCurves:
            markerName = 'marker_ff_' + crv
            if cmds.objExists(markerName):
                cmds.delete(markerName)
                
            markerDup = cmds.duplicate(marker, name =  markerName, rr = True)[0]
            
            cmds.rename(markerDup, markerName)
            pos = cmds.xform(crv + '.cv[0]', q = True, ws = True, t = True)
            
            cmds.setAttr(charCPNode + '.ip', pos[0], pos[1], pos[2])
            cmds.setAttr(scalpFollShp + '.parameterU', cmds.getAttr(charCPNode + '.u'))
            cmds.setAttr(scalpFollShp + '.parameterV', cmds.getAttr(charCPNode + '.v'))
            pc = cmds.parentConstraint(scalpFoll, markerDup)
            cmds.delete(pc)
            cmds.parent(markerDup, markerGrp)
            cmds.scale( markerScale, markerScale, markerScale, markerDup, xyz = True, a = True)
            cmds.setAttr(markerDup + '.overrideEnabled', 1)
            cmds.setAttr(markerDup + '.overrideDisplayType', 2) 
            cmds.makeIdentity(markerDup, apply = True)
        
                    
            
    if historyDelete:
        for h in historyDelete:
            if cmds.objExists(h):
                cmds.delete(h)

    markerScaleChanged()            
    cmds.select(cl = True)                
    
                        
    
def deleteMarkersForCurves():
    
    currNode = cmds.getAttr('gbNode.currentGBNode')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    markerGrp = 'markerGroup_' + scalpMesh
    baseMeshGrp = cmds.getAttr(currNode + '.baseMeshGroup')
    baseMeshGrpChildren = cmds.listRelatives(baseMeshGrp, c = True)
    
    if markerGrp in baseMeshGrpChildren:
#        print markerGrp
        return markerGrp
    else:
        return []        
    

def createTemplateMarker():
    
#    marker = cmds.polyPyramid( n = 'marker', sh = 1, ns = 4, sc = 2)[0]
    marker = cmds.polySphere(sx = 8, sy = 8)[0]
    assignMarkerShader(marker)        
    cmds.rotate('90deg',  marker, x = True)
#    cmds.delete(marker + '.f[0:11]')
    cmds.delete(marker + '.f[0:23]', marker + '.f[48:55]')
#    cmds.displaySmoothness(marker, divisionsU = 3, divisionsV = 3, pointsWire = 16, pointsShaded = 4, polygonObject = 3)
    cmds.makeIdentity(marker, apply = True)
    return marker
    
    
def getMarkerScale(mesh):
    
    from random import randint
    totalE = cmds.polyEvaluate(mesh, e = True)
    distance = []
    for i in range(10):
        e = randint(0,totalE)
        edgePos = cmds.xform(mesh + '.e[' + str(e) + ']', q = True, ws = True, t = True)
        distance.append(distance3d(edgePos[0:3], edgePos[3:6]))
    dist = sum(distance) / len(distance)
    dist = dist * 0.2
    return dist
            
def assignMarkerShader(markerObj):
    
    markerShader = 'gbMarkerShader'
    markerShaderSG = 'gbMarkerShaderSG'
    if not cmds.objExists(markerShader):
        cmds.shadingNode('lambert', name = markerShader, asShader = True)
        cmds.setAttr(markerShader + '.color', 1,1,0, type = 'double3')
        cmds.setAttr(markerShader + '.incandescence', 0.5,0.5,0, type = 'double3')
        cmds.select(cl = True)
    if not cmds.objExists(markerShaderSG):
        cmds.sets(name = markerShaderSG, renderable = True,  noSurfaceShader = True)
        cmds.connectAttr(markerShader + '.outColor', markerShaderSG + '.surfaceShader', f = True)
    cmds.sets(markerObj, forceElement = markerShaderSG)        
    

def getCurrentMarkerScale():
    

    currNode = cmds.getAttr('gbNode.currentGBNode')
    if not cmds.objExists(currNode + '.markerScale'):
        cmds.addAttr(currNode, ln = 'markerScale', at = 'float', dv = 1.0)
    sc = cmds.getAttr(currNode + '.markerScale')
    cmds.floatField('markerScaleField', edit = True, v = sc)
        
    
    
    

def markerScaleChanged():
    

    sc = cmds.floatField('markerScaleField',q = True, v = True)
    storeMarkerScale(sc)
    markerGrp = deleteMarkersForCurves()
    markers = []
    if markerGrp:
        markers = cmds.listRelatives(markerGrp, c = True)
        if markers:
            cmds.scale(sc, sc, sc, markers, a = True) 
    

def storeMarkerScale(sc):
    
    currNode = cmds.getAttr('gbNode.currentGBNode')
    if not cmds.objExists(currNode + '.markerScale'):
        cmds.addAttr(currNode, ln = 'markerScale', at = 'float')
    cmds.setAttr(currNode + '.markerScale', sc)
        
    
def gbVideoTuts():
    
    import webbrowser

    webbrowser.open('https://www.youtube.com/channel/UCSxjFR2MA0FppPwDVkNQPHQ')                
                
    
def gbDocumentation():
    
    
    import webbrowser

    webbrowser.open('https://www.youtube.com/channel/UCSxjFR2MA0FppPwDVkNQPHQ')
    
def gbPurchaseMenu():
    
    import webbrowser

    webbrowser.open('http://www.groomboy.com/cart.php')
    
    
def selectVerticesAllIpol():
    
    if not checkIfIpolExists():
        reportGBMessage('No Interpolation Exists', True, True, 'red')
    
    currNode = cmds.getAttr('gbNode.currentGBNode')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    baseMeshGrp = cmds.getAttr(currNode + '.baseMeshGroup')
    baseMeshGrpChildren = cmds.listRelatives(baseMeshGrp, c = True)
    i3DGrp = 'charInterpolation_' + scalpMesh
    i3DGrpChildren = []
    if baseMeshGrpChildren:
        if i3DGrp in baseMeshGrpChildren:
            i3DGrpChildren = cmds.listRelatives(cmds.listRelatives(i3DGrp, ad = True, typ = 'nurbsCurve'), p = True)
    vtxSel = []            
    if i3DGrpChildren:
        vtxList = convertCurveToIDList(i3DGrpChildren)
        vtxSel = [scalpMesh + '_DISPLAY.vtx[' + str(vtx) + ']' for vtx in vtxList]
        if vtxSel:
            loadPaintForIpol('Point')
#            print vtxSel
            cmds.select(vtxSel, r = True)
        
def stepCurvesTool():
    
#    if cmds.tabLayout('mainTabs', query = True, sti = True) == 2:
#        reportGBMessage('Step Curves Tool works only on Draw Curves Tab', True, True, 'red')
    
    if cmds.window('stepCurvesWin', exists = True):
        cmds.deleteUI('stepCurvesWin')
    
    cmds.window('stepCurvesWin', title = 'Step Curves Tool')
    cmds.columnLayout('stepLyt', adj = True)
    cmds.intSliderGrp('stepsCountSlider', field = True, label = 'No. of Steps', minValue = 1, maxValue = 30, fieldMinValue = 1, fieldMaxValue = 50, value = 7, fs = 1, ss = 1) 
#    cmds.intSliderGrp('stepsCountSlider', edit = True, dc = 'globalSliderChange()', cc = 'globalSliderChange()\nautoResize()')

    cmds.floatSliderGrp('endClumpSlider', field = True, label = 'End Clamp', minValue = 0.3, maxValue = 0.8, fieldMinValue = 0.3, fieldMaxValue = 0.95, value = 0.7)
    cmds.floatSliderGrp('tipStepFallSlider', field = True, label = 'Tip Steps Falloff', minValue = 0.0, maxValue = 0.8, fieldMinValue = 0.0, fieldMaxValue = 0.95, value = 0.0)
    cmds.button('stepCurvesBtn', label = 'Step Cut on Selected Curves', c = 'stepCurvesExec()')
    cmds.showWindow()
    
def stepCurvesExec():
    

    selList = []
    selList = cmds.ls(sl = True)
    if not selList:
        reportGBMessage('No Curves Selected', True, True, 'red')     
    curveList = []
    curveList = cmds.listRelatives(cmds.listRelatives(selList, ad = True, typ = 'nurbsCurve'), p = True)        
    if not curveList:
        reportGBMessage('No Curves Selected', True, True, 'red')
    
    steps = cmds.intSliderGrp('stepsCountSlider', q = True, value = True)
    endClump = cmds.floatSliderGrp('endClumpSlider', q = True, value = True)
    tf = cmds.floatSliderGrp('tipStepFallSlider', q = True, value = True)
    
    inc = endClump/(steps-1)
    rootU = [inc * s for s in range(steps)]
    tipFall = [(1 - mm.eval('linstep(0,' + str(steps-1) + ',' + str(x) + ');')) * tf for x in range(steps)] 
    endU = [1 - x for x in tipFall] 
    
    for crv in curveList:
        prnt = cmds.listRelatives(crv, p = True)
        dg = cmds.getAttr(crv + '.degree')
        ncv = cmds.getAttr(crv + '.spans') + dg
        for x in range(steps):
            inc = (endU[x] - rootU[x])/(ncv-1)
            finalU = [rootU[x] + inc*cv for cv in range(ncv)]
            stepName = crv + '_step_' + str(x+1)
            if cmds.objExists(stepName):
                cmds.delete(stepName)
            crvPos = [cmds.pointOnCurve(crv, pr = u, top = True) for u in finalU]
            stepCrv = cmds.curve(p = crvPos, d = dg, n = stepName)
            shape = cmds.listRelatives(stepCrv, s = True)[0]
            cmds.rename(shape, crv + '_step_' + 'Shape' + str(x+1))
            cmds.xform(stepCrv, piv = crvPos[0])
#            cmds.parent(stepCrv, prnt)
         
            

def regenerateClumpFF():
    
    import cPickle as Pickle
    currNode = cmds.getAttr('gbNode.currentGBNode')
    clumpMesh = cmds.getAttr(currNode + '.clumpMesh')
    if not clumpMesh:
        return
    
    
    currFFC = getCurrentFFC()
    
    if not currFFC:
        reportGBMessage('No Freeform Curves Exist', True, True, 'red')
    
    clumpDB = []
    clumpDBString = cmds.getAttr(currNode + '.clumpDB')
    if clumpDBString:
        clumpDB = Pickle.loads(str(clumpDBString))
    
    remClumps = []
    addClumps = currFFC    
    if clumpDB:
        prevFFC = clumpDB.keys()
        commonClumps = list(set(currFFC) & set(prevFFC))
        toBeUpdated = []
        for cmp in commonClumps:
            if not len(clumpDB[cmp][1]) == cmds.getAttr(cmp + '.degree') + cmds.getAttr(cmp + '.spans'):
                toBeUpdated.append(cmp)
                continue
            prevPos = clumpDB[cmp][1]
            for x in range(len(prevPos)):
                if not prevPos[x] == cmds.xform(cmp + '.cv[' + str(x) + ']', q = True, ws = True, t = True):                
                    toBeUpdated.append(cmp)
                    break
                            
                                
            
        addClumps = list(set(currFFC) - set(prevFFC)) + toBeUpdated
        remClumps = list(set(prevFFC) - set(currFFC)) + toBeUpdated

        addClumps = list(set(addClumps))
        remClumps = list(set(remClumps))
        
                    
    if remClumps or addClumps:                
        clumpDB = updateClumpDB(remClumps,addClumps)
        dupClumpMesh = createClumpRegions(clumpMesh, currFFC)                
        getBaseCrvPos(dupClumpMesh, clumpDB)
    
    updateClumpSurfaces()
    
    
def getCurrentFFC():
    
    currNode = cmds.getAttr('gbNode.currentGBNode')
    
    baseMeshGroup = cmds.getAttr(currNode + '.baseMeshGroup')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    manualGroup = 'manualCurvesGrp_' + scalpMesh
    manualGrpChildren = []
    baseMeshGrpChildren = cmds.listRelatives(baseMeshGroup, c = True)
    if baseMeshGrpChildren:
        if manualGroup in baseMeshGrpChildren:
            manualGrpChildren = cmds.listRelatives(manualGroup, c = True)
    
    currFFC = []    
    currFFC = manualGrpChildren    
    clumpMesh = cmds.getAttr(currNode + '.clumpMesh')
    
    charCPNode = createCPNode(clumpMesh)
    finalFFC = []
    for ff in currFFC:
        pos = cmds.xform(ff + '.cv[0]', q = True, ws = True, t = True)
        cmds.setAttr(charCPNode + '.ip', pos[0], pos[1], pos[2])
        cpos = list(cmds.getAttr(charCPNode + '.p')[0])
#        print cpos
        if distance3d(pos, list(cpos)) <= 0.1:
            finalFFC.append(ff)
    
    return finalFFC            
    

    
def updateClumpDB(rem,add):
    
    import cPickle as Pickle
    currNode = cmds.getAttr('gbNode.currentGBNode')
    
    clumpDB = []
    clumpDBString = cmds.getAttr(currNode + '.clumpDB')
    if clumpDBString:
        clumpDB = Pickle.loads(str(clumpDBString))
    
    if clumpDB:
        if rem:
            for rc in rem:
                name = clumpDB[rc][0]
                if cmds.objExists(clumpDB[rc][0]):
                    cmds.delete(clumpDB[rc][0])
                del clumpDB[rc]                    
        
                    
            
    if not clumpDB:
        clumpDB = {}
    
    tempEntry = []
    tempEntry.append('') # 0 clump surface names 
    tempEntry.append([]) # 1 clumpCurvesFlatPos 
    tempEntry.append([]) # 2 clump base curve pos 
    tempEntry.append('') # 3 clump scale graph
    tempEntry.append(0) # 4 base curve u spans
    tempEntry.append(0) # 5 profile curve v spans
    tempEntry.append([]) # 6 clump graph override
    tempEntry.append('') # 7 clump graph STRING override

    for fc in add:
        clumpDB[fc] = tempEntry[:]
        clumpDB[fc][1] = [cmds.xform(fc + '.cv[' + str(x) + ']', q = True, ws = True, t = True) for x in range(cmds.getAttr(fc + '.spans') + cmds.getAttr(fc + '.degree'))]
#        print clumpDB[fc]
        
    cmds.setAttr(currNode + '.clumpDB', Pickle.dumps(clumpDB), type = 'string')
    
    return clumpDB
    
    
def createClumpRegions(clumpMesh, currFFC):
    
#    currNode = cmds.getAttr('gbNode.currentGBNode')
    historyDelete = []
    dupClumpMesh = cmds.duplicate(clumpMesh, name = 'dupClumpMesh', rr = True)[0]

#    historyDelete.append(dupClumpMesh)
    
    smoothNode = cmds.polySmooth(dupClumpMesh, divisions = 1)
    historyDelete.append(smoothNode[0])
    
    totalFFC = len(currFFC)
    facetList = []
    for ffc in currFFC:
        pos = cmds.xform(ffc + '.cv[0]', q = True, ws = True, t = True)
        facetList.append(cmds.polyCreateFacet( p=[tuple(pos), tuple(pos), tuple(pos)] , ch = False)[0])

    polyCloud = cmds.polyUnite(facetList, ch = False, name = 'pointCloud_' + dupClumpMesh)[0]
    historyDelete.append(polyCloud)
    totalV = cmds.polyEvaluate(dupClumpMesh, v = True)
    cmds.select(dupClumpMesh + '.vtx[0:' + str(totalV) + ']', r = True)
    mm.eval('ConvertSelectionToShellBorder;')
    mm.eval('InvertSelection;')
    exceptBorderVtx = cmds.ls(sl = True, fl = True)
#    cmds.select(polyCloud, exceptBorderVtx, r = True)
    cmds.transferAttributes(polyCloud, exceptBorderVtx, transferPositions = True, nml = False, uvs = False, col = False, sampleSpace = 0)
    cmds.polyMergeVertex(exceptBorderVtx, d = 0.01)
    
    cmds.setAttr(dupClumpMesh + '.visibility', True)
    totalV = cmds.polyEvaluate(dupClumpMesh, v = True)
    cmds.select(dupClumpMesh + '.vtx[0:' + str(totalV) + ']', r = True)
    mm.eval('SelectPolygonSelectionBoundary;')
    borderVtx = cmds.ls(sl = True, fl = True)
    mm.eval('PolySelectTraverse 1;')
    nextSelV = cmds.ls(sl = True, fl = True)
    mm.eval('InvertSelection;')
    upperV = cmds.ls(sl = True, fl = True)
    onlyNextSelV = list(set(nextSelV) - set(borderVtx))
    
    cmds.select(borderVtx, r = True)
    mm.eval('InvertSelection;')
    upperBorder = cmds.ls(sl = True, fl = True)
        
    dummyClump = cmds.duplicate(dupClumpMesh, rr = True)[0]       
    historyDelete.append(dummyClump)
    
    upperBorderDummy = [vtx.replace(dupClumpMesh, dummyClump) for vtx in upperBorder]
    cmds.xform(upperBorderDummy, ws = True, r = True, t = [0,50,0])
    
    charCPNode = createCPNode(dummyClump)
    historyDelete.append(charCPNode)
    
    cmds.select(onlyNextSelV, r = True)
    
    facetList = []
    for v in onlyNextSelV:
        pos = cmds.xform(v, q = True, ws = True, t = True)
        cmds.setAttr(charCPNode + '.ip', pos[0], pos[1], pos[2])
        cvt = cmds.getAttr(charCPNode + '.vt')
        cvtPos = cmds.xform(dupClumpMesh + '.vtx[' + str(cvt) + ']', q = True, ws = True, t = True)
        facetList.append(cmds.polyCreateFacet( p=[tuple(cvtPos), tuple(cvtPos), tuple(cvtPos)] , ch = False)[0])
    
    cmds.delete(dummyClump)
    
    if len(facetList) > 2:
        polyCloud = cmds.polyUnite(facetList, ch = False, name = 'pointCloud_' + dupClumpMesh)[0]
    else:
        polyCloud = facetList[0]        
    historyDelete.append(polyCloud)        
    cmds.transferAttributes(polyCloud, borderVtx, transferPositions = True, nml = False, uvs = False, col = False, sampleSpace = 0)
    cmds.polyMergeVertex(borderVtx, d = 0.01)
    
    cmds.polyTriangulate(dupClumpMesh)
    totalE = cmds.polyEvaluate(dupClumpMesh, e = True)
    
    smoothNode = cmds.polySmooth(dupClumpMesh, mth = 0, c = 0.0)
#    cmds.select([dupClumpMesh + '.e[' + str(e) + ']' for e in range(totalE*2)], r = True)    
    cmds.delete([dupClumpMesh + '.e[' + str(e) + ']' for e in range(totalE*2)])
    
    cmds.transferAttributes(clumpMesh, dupClumpMesh, transferPositions = True, nml = False, uvs = False, col = False, sampleSpace = 0)
    cmds.select(dupClumpMesh + '.vtx[*]', r = True)
    cmds.delete()
    
    
    cmds.transferAttributes(clumpMesh, dupClumpMesh, transferPositions = True, nml = False, uvs = False, col = False, sampleSpace = 0)
    totalF = cmds.polyEvaluate(dupClumpMesh, f = True)
    cmds.select(dupClumpMesh + '.f[0:' + str(totalF) + ']', r = True)
    mm.eval('SelectPolygonSelectionBoundary;')
    cmds.delete()
    
    totalV = cmds.polyEvaluate(dupClumpMesh, v = True)
    cmds.select(dupClumpMesh + '.vtx[0:' + str(totalV) + ']', r = True)
    mm.eval('SelectPolygonSelectionBoundary;')
    postDelBorderV = cmds.ls(sl = True, fl = True)
    
    ringDup = cmds.duplicate(clumpMesh, rr = True)[0]
    historyDelete.append(ringDup)
    totalE = cmds.polyEvaluate(ringDup, e = True)
    cmds.select(ringDup + '.e[0:' + str(totalE) + ']', r = True)
    mm.eval('SelectPolygonSelectionBoundary;')
    totalF = cmds.polyEvaluate(ringDup, f = True)
    
    
    extrude = cmds.polyExtrudeEdge(keepFacesTogether = True)[0]
    cmds.move(0,0.02,0, r = True)
#    cmds.setAttr(extrude + '.localTranslateY', 0.2)
    
    cmds.delete(ringDup + '.f[0:' + str(totalF) + ']')
    
    cmds.transferAttributes(ringDup, postDelBorderV, transferPositions = True, nml = False, uvs = False, col = False, sampleSpace = 0)
#    cmds.delete(ringDup)
    
    cmds.polyChipOff(dupClumpMesh, kft = False, dup = False)
    cmds.polySmooth(dupClumpMesh,dv = 1)
    cmds.transferAttributes(clumpMesh, dupClumpMesh, transferPositions = True, nml = False, uvs = False, col = False, sampleSpace = 0)
    
    cmds.polySmooth(dupClumpMesh, mth = 1, dv = 1)
    cmds.transferAttributes(clumpMesh, dupClumpMesh, transferPositions = True, nml = False, uvs = False, col = False, sampleSpace = 0)
    
    cmds.delete(dupClumpMesh, ch = True)
    for h in historyDelete:
        if cmds.objExists(h):
            cmds.delete(h)
            
    return dupClumpMesh
    

def getBaseCrvPos(dupClumpMesh, clumpDB):
    
    import cPickle as Pickle
    import copy
    ffcs = clumpDB.keys()
#    ffcs = cmds.ls(sl = True)
    if not ffcs:
        return
    historyDelete = []    

        
    charCPNode = createCPNode(dupClumpMesh)
    historyDelete.append(charCPNode)
    currNode = cmds.getAttr('gbNode.currentGBNode')
    toBeUpdatedClumpsString = cmds.getAttr(currNode + '.toBeUpdatedClumps')
    toBeUpdatedClumps = []
    if toBeUpdatedClumpsString:
        toBeUpdatedClumps = Pickle.loads(str(toBeUpdatedClumpsString))
        
    finalCurrPos = []
    for fc in ffcs:
        root = clumpDB[fc][1][0]
#        root = cmds.xform(fc + '.cv[0]', q = True, ws = True, t = True)
        cmds.setAttr(charCPNode + '.ip', root[0], root[1], root[2])
        cmds.select(dupClumpMesh + '.f[' + str(cmds.getAttr(charCPNode + '.f')) + ']', r = True)
        
        mm.eval('ConvertSelectionToShell;')
#        print '>>', cmds.ls(sl = True)
        mm.eval('ConvertSelectionToEdges;')
        mm.eval('ConvertSelectionToShellBorder;')
        
#        mm.eval('PolySelectConvert 20;')
#        mm.eval('ConvertSelectionToShellBorder;')
        
        crvName = cmds.polyToCurve(form = 2, degree = 1)[0]
        ncv = cmds.getAttr(crvName + '.degree') + cmds.getAttr(crvName + '.spans')
        prevBaseCrvPos = clumpDB[fc][2]
        currBaseCrvPos = [cmds.xform(crvName + '.cv[' + str(x) + ']', q = True, ws = True, t = True) for x in range(ncv)]
        currBaseCrvPos.append(cmds.xform(crvName + '.cv[0]', q = True, ws = True, t = True))

        if not currBaseCrvPos == prevBaseCrvPos:
            toBeUpdatedClumps.append(fc)
        clumpDB[fc][2] = currBaseCrvPos
        

        cmds.delete(crvName)            
    
        
    cmds.setAttr(currNode + '.clumpDB', str(Pickle.dumps(clumpDB)), type = 'string')
    cmds.setAttr(currNode + '.toBeUpdatedClumps', str(Pickle.dumps(toBeUpdatedClumps)), type = 'string')
    
#    if cmds.objExists(dupClumpMesh):
#        cmds.delete(dupClumpMesh)
            
        
        
def updateClumpSurfaces():
    
    print 'UPDATING CLUMP SURFACES'
    import cPickle as Pickle
    currNode = cmds.getAttr('gbNode.currentGBNode')
    
    clumpDB = []
    clumpDBString = cmds.getAttr(currNode + '.clumpDB')
    if clumpDBString:
        clumpDB = Pickle.loads(str(clumpDBString))
    
    if not clumpDB:
        return
    
    toBeUpdatedClumpsString = cmds.getAttr(currNode + '.toBeUpdatedClumps')
    toBeUpdatedClumps = []
    if toBeUpdatedClumpsString:
        toBeUpdatedClumps = Pickle.loads(str(toBeUpdatedClumpsString))
    
    if not toBeUpdatedClumps:
        return
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    mainGrp = cmds.getAttr(currNode + '.mainGroup')
    
    clumpGrp = 'clumpGrp_' + scalpMesh   
    if not clumpGrp in cmds.listRelatives(mainGrp, c = True):
        cmds.group(name = clumpGrp, em = True, parent = mainGrp)
        
        
        
    ffcsDB = clumpDB.keys()
    toBeUpdatedClumps = list(set(toBeUpdatedClumps))
    for cmp in toBeUpdatedClumps:

        if not cmp in ffcsDB:
            continue
        clumpSurfaceName = 'clumpSurface_' + cmp            
        clumpDB[cmp][0] = clumpSurfaceName
        if cmds.objExists(clumpSurfaceName):
            cmds.delete(clumpSurfaceName)
        basePos = clumpDB[cmp][2]

        baseCurve = cmds.curve(p = basePos, degree = 1, per = True, k = range(len(basePos)))            
#        print 'creating ', baseCurve
#        baseCurveSpans = 10
#        cmds.rebuildCurve(baseCurve, spans = baseCurveSpans)
#        clumpDB[cmp][4] = baseCurveSpans
        surfaceName = cmds.extrude(baseCurve, cmp, name = clumpSurfaceName, po = 0, sc = 0.01, et=2 )[0]
        cmds.parent(surfaceName, clumpGrp)
        cmds.delete(surfaceName, ch = True)
        cmds.delete(baseCurve)
    
    cmds.select(cl = True)        
    cmds.setAttr(currNode + '.clumpDB', str(Pickle.dumps(clumpDB)), type = 'string')
    cmds.setAttr(currNode + '.toBeUpdatedClumps', str(Pickle.dumps([])), type = 'string')
#    print 'done clumping'
          
        
def checkForClumpUpdateFF(toBeResize):
    
    import cPickle as Pickle
    currNode = cmds.getAttr('gbNode.currentGBNode')
    if not cmds.objExists(currNode +  '.clumpMesh'):
        return
        
    clumpMesh = cmds.getAttr(currNode + '.clumpMesh')
    if not clumpMesh:
        return
        
    baseMeshGrp = cmds.getAttr(currNode + '.baseMeshGroup')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    manualGrp = 'manualCurvesGrp_' + scalpMesh
    baseMeshGrpChildren = cmds.listRelatives(baseMeshGrp, c = True)
    if not baseMeshGrpChildren:
        return
    
    if not manualGrp in baseMeshGrpChildren:
        return

    manualGrpChildren = cmds.listRelatives(manualGrp, c = True)        
    validTBR = list(set(toBeResize) & set(manualGrpChildren))
    if validTBR:
        cmds.setAttr(currNode + '.toBeUpdatedClumps', str(Pickle.dumps(validTBR)), type = 'string')
#        print 'from check for clump resize'
        updateClumpSurfaces()
            

def clumpTweakExec():

    import cPickle as Pickle
    currNode = cmds.getAttr('gbNode.currentGBNode')

    clumpDB = []
    clumpDBString = cmds.getAttr(currNode + '.clumpDB')
    if clumpDBString:
        clumpDB = Pickle.loads(str(clumpDBString))
        
    if not clumpDB:
        reportGBMessage('No Clumps Exist', True, True, 'red')
    
    sel = []
    sel = cmds.ls(sl = True)
    if not sel:
        reportGBMessage('Please Select a Clump Surface', True, True, 'red')
    
        
    clumpCurves = clumpDB.keys()
    surfaceToCurves = []
#    clumpMesh = cmds.getAttr(currNode + '.clumpMesh')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    for each in sel:
#        'clumpSurface_' + scalpMesh + '_' + str(clump)
        if not 'clumpSurface_' in each:
            continue
        surfaceToCurves.append(each.split('clumpSurface_')[1:])
    
    sel = surfaceToCurves
#    print clumpCurves
    print sel
    selectedClumps = list(set(clumpCurves) & set(sel[0]))
    
    
#    tweakGraph = cmds.gradientControlNoAttr('', q = True, asString = True)
#    clumpPerList = []
    for cmp in selectedClumps:
        ncv = len(clumpDB[cmp][1])
        perList = []
        for cv in range(ncv):
            perCV = mm.eval('linstep(0,' + str(ncv-1) + ',' + str(cv) + ');')
            p1 = cmds.gradientControlNoAttr('clumpTweakGraph',q = True, vap = perCV)
            p1 = p1 - 0.5
            perList.append(p1)
        clumpDB[cmp][6] = perList[:]
        clumpDB[cmp][7] = cmds.gradientControlNoAttr('clumpTweakGraph', q = True, asString = True)
#        clumpPerList.append(perList[:])
    if not cmds.objExists(currNode + '.clumpOveride'):
        cmds.addAttr(currNode, ln = 'clumpOveride', attributeType = 'bool', dv = False)
        
    cmds.setAttr(currNode + '.clumpOveride', True)
    cmds.setAttr(currNode + '.toBeResize', str(Pickle.dumps(selectedClumps)), type = 'string')
    cmds.setAttr(currNode + '.clumpDB', str(Pickle.dumps(clumpDB)), type = 'string')
#    cmds.setAttr(currNode + '.clumpOveride', str(Pickle.dumps(clumpPerList)), type = 'string')

    autoResize()
    
    
def getClumpTweakPercent(tbrList):
    
    import cPickle as Pickle
    currNode = cmds.getAttr('gbNode.currentGBNode')

    clumpDB = []
    clumpDBString = cmds.getAttr(currNode + '.clumpDB')
    if clumpDBString:
        clumpDB = Pickle.loads(str(clumpDBString))
        
    if not clumpDB:
        return
    
    perList = []
    clumpCurves = clumpDB.keys()
    for tbr in tbrList:
        if tbr in clumpCurves:
            perList.append(clumpDB[tbr][6])
        else:
            perList.append([])
            
    return perList                        
    
def loadClumpValues():
    
    print 'load clump'
    import cPickle as Pickle
    currNode = cmds.getAttr('gbNode.currentGBNode')

    clumpDB = []
    clumpDBString = cmds.getAttr(currNode + '.clumpDB')
    if clumpDBString:
        clumpDB = Pickle.loads(str(clumpDBString))
        
    if not clumpDB:
        return
        
    selection = cmds.ls(sl = True)
    print selection
    sel = ''
    if selection:
        sel = selection[-1]
    else:
        return
            
    clumpCurves = clumpDB.keys()
    clumpSurfaces = [clumpDB[cmp][0] for cmp in clumpCurves]
    print sel, clumpSurfaces
    if sel in clumpSurfaces:

        crv = sel.split('clumpSurface_')[1]
        graph = str(clumpDB[crv][7])
        print 'graph', graph
        if not graph:
            graph = '0.5,0,3,0.5,1,3'
        
        cmds.gradientControlNoAttr('clumpTweakGraph', edit = True, asString = graph)
    
                            
def polyStripFF():
    
#    currFFC = getCurrentFFC()
    currFFC = getIpolCurves()
    if not currFFC:
        return
    currNode = cmds.getAttr('gbNode.currentGBNode')
    scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
    charCPNode = createCPNode(scalpMesh)
    for fc in currFFC:
        normal = cmds.pointOnCurve(fc, no = True)
        tangent = cmds.pointOnCurve(fc, t = True)
        cross = getCrossProductGB(normal,tangent)
        unitCross = list(mm.eval('unit <<' + str(cross[0])+ ',' + str(cross[1]) + ',' + str(cross[2]) + '>>'))
        pos = cmds.pointOnCurve(fc, p = True)
        dist = float(cmds.floatFieldGrp('polyWidthField', q = True, v1 = True)) * 0.5
        newPosA = [a + b for a,b in zip(pos,[dist* x for x in unitCross])]
        newPosB = [a + b for a,b in zip(pos,[-1*dist * x for x in unitCross])]
        baseName = 'baseCrv_polyStrip_' + fc
        if cmds.objExists(baseName):
            cmds.delete(baseName)
        baseCrv = cmds.curve(degree = 1, name = baseName, p = [newPosA, newPosB])
        cmds.xform(baseCrv, piv = pos)
        cmds.setAttr(charCPNode + '.ip', newPosA[0], newPosA[1], newPosA[2])
        cPosA = list(cmds.getAttr(charCPNode + '.p')[0])
        touchRotate(baseCrv, pos, newPosA, cPosA)
#        touchRotate(crv, p0, pA, pB)
        extName = 'extrude_polyStrip_' + fc
        if cmds.objExists(extName):
            cmds.delete(extName)
        cmds.extrude(baseCrv, fc, et = 2, name = extName, po = 0) 

def getIpolCurves():
    
    currNode = cmds.getAttr('gbNode.currentGBNode')
    baseMesh = cmds.getAttr(currNode + '.scalpMesh')
    baseMeshGrp = cmds.getAttr(currNode + '.baseMeshGroup')
    
    i3DGrp = 'charInterpolation_' + baseMesh
    ipolCurves = []
    baseMeshGrpChildren = cmds.listRelatives(baseMeshGrp, c = True)
    if i3DGrp in baseMeshGrpChildren: 
        ipolCurves = cmds.listRelatives(cmds.listRelatives(i3DGrp, ad = True, typ = 'nurbsCurve'), p = True)
            
    return ipolCurves
    
def getCrossProductGB(a, b):
    
    c = [a[1]*b[2] - a[2]*b[1],
         a[2]*b[0] - a[0]*b[2],
         a[0]*b[1] - a[1]*b[0]]

    return c        
        
        
def createLicenseKeyGB():
    
    key = initLicenseGB()
#    createSessionReference()
    if not key:
        return
    
    if cmds.window('gbLicenseWin', exists = True):
        cmds.deleteUI('gbLicenseWin')
    cmds.window('gbLicenseWin', title = 'License Key for Groomboy')
    cmds.columnLayout(adj = True)
    cmds.text(label = 'Please Copy the Key for Your Groomboy Test Version')                
    cmds.text(label = '(Ctrl+A) (Ctrl+C)')
    cmds.textField('licGBTextField', text = key, ed = False, annotation = '(Ctrl+A) (Ctrl+C)')

    cmds.showWindow('gbLicenseWin')
    cmds.setFocus('licGBTextField')

        
def initLicenseGB():
    
    gbos = cmds.about(os = True)
    key = ''
    if gbos == 'linux64':
        key = initLicenseLinuxGB()
    elif gbos == 'win64' or gbos == 'nt':
        key = initLicenseWindowsGB()
    
    message = str(key)
    cipher = encryptGB(message)
#    print message
    return cipher        

def initLicenseLinuxGB():
    
    import os
    import subprocess
    p = subprocess.Popen("ls -l /dev/disk/by-uuid/", stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    parts = output.split('\n')
    idList = []
    
    for p in parts:
        if ' -> ' in p:
            front = p.split(' -> ')[0]
            id = front.split(' ')[-1]
            if len(id) < 36:
                continue
            idList.append(id)
            
    k = getCipherKeyGBK()

    for id in idList:
        k = encryptGBK(id,k)            
    
    return k        
    
def getCipherKeyGBK():
    
    return '925360250734150913286507897425852405'

def encryptGBK(message,key):
    
    import base64
    enc = []
    for i in range(len(message)):
        key_c = key[i % len(key)]
        enc_c = chr((ord(message[i]) + ord(key_c)) % 256)
        enc.append(enc_c)
    return base64.urlsafe_b64encode(''.join(enc))
           

def initLicenseLinuxGBOLD():
    
    import subprocess
    key = ''
    
    p = subprocess.Popen("ls -l /dev/disk/by-path", stdout=subprocess.PIPE, shell=True)
    output, errors = p.communicate()
    all = output.split('\n')
    sda = []
    for a in all:
        sda.append(a.split('/')[-1])
    sda = sda[1:-1] 
    
    cd = False
    key = ''
    for each in sda:
        p = subprocess.Popen("udevadm info -q property -xn " + each, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        parts = output.split('\n')
        for p in parts:
            if 'ID_CDROM' in p:
                cd = True
                break
        if cd:
            cd = False
            continue
        elif key:
            break
        else:
            for p in parts:
                if 'ID_SERIAL=' in p:
                    key = p.split('ID_SERIAL=')[1]
                    break
                        
    if key:
        return key
                  
def initLicenseWindowsGB():

    import os
    import ctypes
    from ctypes.wintypes import MAX_PATH
    '''
    gbos = cmds.about(os = True)
    if gbos =='win64':
        kernel32 = ctypes.windll.kernel32
        windows_directory = ctypes.create_unicode_buffer(1024)
        if kernel32.GetWindowsDirectoryW(windows_directory, 1024) == 0:
            print 'No Drives Found'
        else:
            windows_drive = os.path.splitdrive(windows_directory)[0]
    
            
    #    macID = getMacAddress()     
        sys32Path = os.environ['WINDIR'] + '\\System32'
    '''    
    folderPath = getCheckFolderPath()
    seconds = os.path.getctime(folderPath)
    seconds = ('%.7f' %seconds)
    
#    dec
#    message = macID + ']|[' + str(seconds)

    return seconds

def gbHairPreviewSystem():
    
    currNode = cmds.getAttr('gbNode.currentGBNode')
    if not cmds.objExists(currNode + '.previewGBHair'):
        createGBPreviewSytem()
    launchPreviewWindow()


def createGBPreviewSystem():
    
    currNode = cmds.getAttr('gbNode.currentGBNode')

# -----------------------------------------------    
# ------------ MESH STRIP SECTION ---------------  
# -----------------------------------------------  

def launchClumpMeshGenKit():
    
    if cmds.window('groomKitClumpMeshWin', exists = True):
        cmds.deleteUI('groomKitClumpMeshWin')

    cmds.window('groomKitClumpMeshWin', title = 'Mesh Generation Groom Kit', rtf = True, width = 150)            
    cmds.columnLayout('clumpMeshMainLyt', adj = True)
    

def launchMeshStripGenKit():
    
    origSel = cmds.ls(sl = True)
#    print 'launch'
    createMeshGenGBNode()
    
    if cmds.window('groomKitMeshStripWin', exists = True):
        cmds.deleteUI('groomKitMeshStripWin')

    cmds.window('groomKitMeshStripWin', title = 'Mesh Strip Generation Groom Kit', rtf = True, width = 300)            
    cmds.columnLayout('meshStripMainLyt', adj = True)
    
    cmds.menuBarLayout('gbMeshStripMenuBar')
    cmds.menu('meshStripCustMenu', label = 'Custom Mesh', vis = False)
    cmds.radioMenuItemCollection('meshStripCustMeshRadio')
    meshStripNodes = getMeshStripNodes()
#    print meshStripNodes, '>><<'
    if meshStripNodes:
        for msNode in meshStripNodes:
            cmds.menuItem(msNode + '_radio', label = cmds.getAttr(msNode + '.displayName'), cl = 'meshStripCustMeshRadio', c = 'meshStripRadioSelected()', radioButton = False )
    cmds.menuItem('meshStripMenuDivider', d = True, p = 'meshStripCustMenu')        
    cmds.menuItem('addNewMeshStripMenu', label = 'Add New Mesh Strip Setup', p = 'meshStripCustMenu' , c = 'menuNewMeshStripSetup()')        
    cmds.menuItem('removeMeshStripMenu', label = 'Remove Mesh Strip Setup', p = 'meshStripCustMenu', c = 'menuRemoveMeshStripSetup()')
    
    
    cmds.button('cancelStripDef', label = 'Cancel Mesh Strip Definition', c = 'cancelMeshStripDef()')
    currNode = ''
    if cmds.objExists('gbNode'):
        currNode = cmds.getAttr('gbNode.currentGBNode')
    gbExists = False
    if currNode:  
        gbExists = True
        displayName = cmds.getAttr(currNode + '.displayName')
        scalpMesh = cmds.getAttr(currNode + '.scalpMesh')
        
    cmds.columnLayout('meshStripL0',adj = True, vis = True, p = 'meshStripMainLyt')
    cmds.radioButtonGrp('gbOrCustRadio', cw2 = [160,160] ,vis = False, labelArray2 = ['Use Current Groomboy Setup', 'Use Custom Mesh'], numberOfRadioButtons = 2, on1 = 'useGBForStrip()', on2 = 'useCustForStrip()', sl = 1, p = 'meshStripL0')
    
    if gbType == 0:
        cmds.radioButtonGrp('gbOrCustRadio', edit = True, en2 = False)
        cmds.menu('meshStripCustMenu', edit = True, en = False)


    cmds.button('useGBNodeForStrips', vis = False, c = 'continueGBMeshStripInit()', p = 'meshStripL0')
#    print 'button setting 17247' 
    cmds.button('useSelMeshForStripsBtn', label = 'Use Selected Custom Mesh', vis = False, c = 'continueCustMeshStripInit()', p = 'meshStripL0')
    cmds.button('useSelCurvesCustMeshBtn', label = 'Use Selected Curves as input', vis = False, c = 'useSelCurvesCustMesh()', p = 'meshStripL0')
    

    
    
    cmds.columnLayout('meshStripL1', vis = False, adj = True, p = 'meshStripMainLyt')
#    cmds.checkBox('globalStripChk', p = 'meshStripMainLyt')
#    cmds.columnLayout('stripRegionLyt', adj = True, p = 'meshStripL1')
#    cmds.button('paintStripRegionBtn', label = 'Paint Region Controllers for Mesh Strips', p = 'stripRegionLyt')
#    cmds.button('stripRegionOptionBtn', label = 'Strip Region Controllers Options', p = 'stripRegionLyt')
#    cmds.frameLayout('stripRegionOptionLyt', label = 'Strip Region Controllers Options', cll = True, cl = True, vis = False, p = 'stripRegionLyt')
#    cmds.button(label = 'Mirror Region Controllers', p = 'stripRegionOptionLyt')
#    cmds.floatSliderGrp('gbStripWidthSliderGrp', field = True, label = 'Strip Width', minValue = 0, fieldMaxValue = 360, value = 0.5, fs = 5, ss = 5) 
    
    cmds.button('stripResetOverride', label = 'Reset Override', vis = True, c = 'resetStripOverride()', p = 'meshStripL1')

    cmds.rowLayout('stripWidthRL',nc = 2)
    cmds.floatSliderGrp('stripWidthSlider', label = 'Width', field = True, minValue = 0, maxValue = 10.0, v = 1.0, cc = 'stripWidthChangeUI()', ebg = True, p = 'stripWidthRL')
    cmds.checkBox('stripWidthAdaptiveCB', label = 'Adaptive', cc = 'stripWidthChangeUI()', p = 'stripWidthRL')
    cmds.setParent('..')
    
    cmds.rowLayout('stripAdaptiveWidthRL', vis = False, nc = 2)
    cmds.floatSliderGrp('stripAdpWidthSlider', label = 'Adaptive Width Blend', field = True, minValue = 0, maxValue = 1.0, cc = 'stripWidthChangeUI()', p = 'stripAdaptiveWidthRL')
    cmds.checkBox('stripWidthAdaptiveCBX', label = '',  vis = False, cc = 'stripWidthChangeUI()', p = 'stripAdaptiveWidthRL')
    cmds.setParent('..')

#    --------------------------------------------------------

    cmds.rowLayout('stripSegmentsRL', nc = 2)
    cmds.intSliderGrp('stripSegmentsSlider', label = 'Width Segments', field = True, minValue = 1, maxValue = 10, v = 1, cc = 'stripSegmentsChangeUI()', ebg = True, p = 'stripSegmentsRL')
    cmds.checkBox('stripSegmentsAdaptiveCB', label = 'Adaptive', cc = 'stripSegmentsChangeUI()', p = 'stripSegmentsRL')
    cmds.setParent('..')
    
    cmds.rowLayout('stripAdaptiveSegmentsRL', vis = False, nc = 2)
    cmds.floatSliderGrp('stripAdpSegmentsSlider', label = 'Adaptive Width Segs Blend', field = True, minValue = 0, maxValue = 1.0, cc = 'stripSegmentsChangeUI()', p = 'stripAdaptiveSegmentsRL')
    cmds.checkBox('stripSegmentsAdaptiveCBX', label = '',  vis = False, p = 'stripAdaptiveSegmentsRL')
    cmds.setParent('..')
    
#    ---------------------------------------------------------    
    
    cmds.rowLayout('stripDivRL', nc = 2)    
    cmds.intSliderGrp('stripDivSlider', label = 'Length Segments', field = True, minValue = 1, maxValue = 40, cc = 'stripDivChangeUI()', ebg = True, p = 'stripDivRL')
    cmds.checkBox('stripDivAdaptiveCB', label = 'Adaptive', cc = 'stripDivChangeUI()', p = 'stripDivRL')
    cmds.setParent('..')
    
    cmds.rowLayout('stripAdaptiveDivRL', adj = 1, vis = False, nc = 2)
    cmds.floatSliderGrp('stripAdpDivSlider', label = 'Adaptive Len Segs Blend', field = True, minValue = 0, maxValue = 1.0, cc = 'stripDivChangeUI()', p = 'stripAdaptiveDivRL')
    cmds.checkBox('stripDivAdaptiveCBX', label = '',  vis = False, p = 'stripAdaptiveDivRL')
    cmds.setParent('..')

    
    
    cmds.text('stripTaperGraphText', label = 'Width Scale Graph', ebg = True, vis = False, p = 'meshStripL1')
#    cmds.gradientControl('stripTaperGraph', asString = '1,0,1', h = 100, cc = 'stripTaperGraphChangeUI()', p = 'meshStripL1')
    cmds.gradientControlNoAttr('stripTaperGraph', asString = '1,0,1', h = 100, cc = 'stripTaperGraphChangeUI()', vis = False, p = 'meshStripL1')
    cmds.floatSliderGrp('stripTaperSlider', label = 'Taper', field = True, minValue = 0, maxValue = 2, fieldMinValue = 0.0, fieldMaxValue = 10, cc = 'stripTaperChangeUI()', ebg = True)
    
    cmds.floatSliderGrp('stripRotateSlider', label = 'Rotate', field = True, minValue = -90.0, maxValue = 90.0, cc = 'stripRotateChangeUI()' , vis = False, ebg = True)

    cmds.floatSliderGrp('stripTwistSlider', label = 'Twist', field = True, minValue = -180, maxValue = 180,  cc = 'stripTwistChangeUI()', ebg = True)
    cmds.floatSliderGrp('stripTwistScaleSlider', label = 'Twist Scale', field = True, minValue = 1, maxValue = 10, fieldMaxValue = 5, v = 1.0, cc = 'stripTwistScaleChangeUI()', ebg = True)
    
    cmds.floatSliderGrp('stripShoveSlider', label = 'Root Inset', vis = False, field = True, v = 1.0, minValue = 0.0, maxValue = 10.0, pre = 2, fieldMaxValue = 5.0, cc = 'stripShoveChangeUI()', ebg = True)
    
    
    cmds.floatSliderGrp('stripRotateXSlider', label = 'Rotate X', field = True, minValue = -90.0, maxValue = 90.0, cc = 'stripRotateXChangeUI()' , vis = False, ebg = True)
    cmds.floatSliderGrp('stripRotateYSlider', label = 'Rotate Y', field = True, minValue = -90.0, maxValue = 90.0, cc = 'stripRotateYChangeUI()' , vis = False, ebg = True)
    cmds.floatSliderGrp('stripRotateZSlider', label = 'Rotate Z', field = True, minValue = -90.0, maxValue = 90.0, cc = 'stripRotateZChangeUI()' , vis = False, ebg = True)
    
    
    cmds.text('stripCurvatureText', label = 'Strip Curvature Graph', vis = False, ebg = True, p = 'meshStripL1')
    cmds.gradientControlNoAttr('stripCurvatureGraph', asString = '0.5,0,2', vis = False, h = 100, cc = 'stripCurvatureChange()', p = 'meshStripL1')
    
    
    cmds.text(label = '', p = 'meshStripL1')
    
    cmds.columnLayout('stripCurvatureMainCL', adj = True, p = 'meshStripL1')
    cmds.paneLayout( 'stripPaneL', h = 125, configuration = 'vertical3', p = 'stripCurvatureMainCL' )
    cmds.columnLayout('stripRootGraphCL', adj = True, p = 'stripPaneL')
    cmds.text('stripRootTxt', label = 'Root Curvature Graph',  p = 'stripRootGraphCL' , ebg = True)
    cmds.gradientControlNoAttr('stripRootGraph', asString = '0.5,0.2', w = 230, h = 100, cc = 'stripRootGraphChange()', p = 'stripRootGraphCL')
# font = "boldLabelFont"    
    cmds.popupMenu(b = 3)
    cmds.menuItem(label = 'Copy Graph', c = 'copyPasteCurvatureGraph(0,0)')
    cmds.menuItem(label = 'Paste Graph', c = 'copyPasteCurvatureGraph(0,1)')
    cmds.menuItem(label = 'Swap Graphs', c = 'copyPasteCurvatureGraph(2,2)')

    cmds.menuItem(label = 'Save Graph', c = 'savePreset(\'stripRootGraph\')')
    cmds.menuItem(label = 'Load Graph', c = 'loadPresetFromGraph(\'stripRootGraph\')')
        
    cmds.menuItem(label = '-', c = 'loadStripGraphPreset(0,0)')
    cmds.menuItem(label = '(', c = 'loadStripGraphPreset(0,1)')
    cmds.menuItem(label = ')', c = 'loadStripGraphPreset(0,2)')        
    cmds.menuItem(label = 'S', c = 'loadStripGraphPreset(0,3)')
    
    cmds.setParent('..')
    cmds.columnLayout('stripGraphOptionsCL',adj = True, p = 'stripPaneL')
#    cmds.text(label = '', p = 'stripGraphOptionsCL')
#    cmds.button('rootToTipGraphCopyBtn', label = '>', w = 10, h = 38, c = 'rootToTipGraphCopy(0)', p = 'stripGraphOptionsCL')
#    cmds.button('tipToRootGraphCopyBtn', label = '<', w = 10, h = 38, c = 'rootToTipGraphCopy(1)', p = 'stripGraphOptionsCL')
    cmds.text('stripCurvatureHeightText', label = 'Height', p = 'stripGraphOptionsCL')
    cmds.floatSlider('stripCurvatureHeightSlider', s = 0.01, v = 0.5, h = 75, min = 0.0, max = 1.0, ebg = True, hr = False, cc = 'stripCurvatureHeightSliderChange()', dgc = 'stripCurvatureHeightSliderChange()', p = 'stripGraphOptionsCL')
    cmds.floatField('stripCurvatureHeightField', s = 0.01, v = 0.5, w = 10, pre = 2, ebg = True, cc = 'stripCurvatureHeightFieldChange()', p = 'stripGraphOptionsCL')
    cmds.setParent('..')
    cmds.columnLayout('stripTipGraphCL', adj = True, p = 'stripPaneL')
    cmds.text('stripTipTxt', label = 'Tip Curvature Graph',  ebg = True, p = 'stripTipGraphCL')
    cmds.gradientControlNoAttr('stripTipGraph', asString = '0.5,0.2', w = 230, h = 100, cc = 'stripTipGraphChange()', p = 'stripTipGraphCL')

    cmds.popupMenu(b = 3)
    cmds.menuItem(label = 'Copy Graph', c = 'copyPasteCurvatureGraph(1,0)')
    cmds.menuItem(label = 'Paste Graph', c = 'copyPasteCurvatureGraph(1,1)')
    cmds.menuItem(label = 'Swap Graphs', c = 'copyPasteCurvatureGraph(2,2)')

    cmds.menuItem(label = 'Save Graph', c = 'savePreset(\'stripTipGraph\')')
    cmds.menuItem(label = 'Load Graph', c = 'loadPresetFromGraph(\'stripTipGraph\')')

    cmds.menuItem(label = '-', c = 'loadStripGraphPreset(1,0)')
    cmds.menuItem(label = '(', c = 'loadStripGraphPreset(1,1)')
    cmds.menuItem(label = ')', c = 'loadStripGraphPreset(1,2)')        
    cmds.menuItem(label = 'S', c = 'loadStripGraphPreset(1,3)')

    cmds.setParent('..')
    cmds.floatSliderGrp('stripCurvatureBiasSlider', label = 'Root-Tip Graph Bias', step = 0.01, field = True, v = 0.5, minValue = 0.01, maxValue = 0.99, cc = 'stripGraphBiasChange()', ebg = True, p = 'stripCurvatureMainCL')
    cmds.floatSliderGrp('stripCurvatureFalloffSlider', label = 'Root-Tip Graph Falloff', step = 0.01, field = True, v = 0.0, minValue = 0.0, maxValue = 0.99, cc = 'stripGraphFalloffChange()', ebg = True, p = 'stripCurvatureMainCL')        
    
    cmds.button('addStripsBtn', label = 'Generate Strips on Selected Curves', c = 'addStripsFromCurvesUI()', p = 'meshStripL1')
    cmds.button('removeStripsBtn', label = 'Remove Selected Strips', c = 'removeStripsUI()', p = 'meshStripL1')
    cmds.button('updateMeshStripsBtn', label = 'Update Mesh Strips', c = 'updateMeshStripsForGBFFCUpdatesFromUI()', p = 'meshStripL1')

    
    cmds.frameLayout('miscStripLyt', label = 'Misc Strip Controls', vis = False, cll = True, cl = True, p = 'meshStripL1')
    cmds.columnLayout(adj = True,p = 'miscStripLyt')
    cmds.floatSliderGrp( 'stripDivOptimizeGrp', label = 'Max Divisions', field=True, ss = 1.0, pre = 0, v = 10.0, p = 'miscStripLyt' )
    cmds.floatSliderGrp('stripDivOptimizeGrp', edit = True, cc = 'stripDivOptimize()')
    cmds.columnLayout('gbStripStatusArea', adj = True, p = 'meshStripMainLyt')
#    cmds.text('gbMProgressBarText', vis = False)
#    cmds.progressBar('gbProgressBar', vis = False, width = 300)
 
    cmds.rowLayout('gbStripMessageLayout', nc = 2, p = 'gbStripStatusArea')
    cmds.text('gbStripMessageStatusColor', h = 20, label = '   ', vis = False, p = 'gbStripMessageLayout')
    cmds.text('gbStripMessageStatusText', font = 'obliqueLabelFont', vis = False, p = 'gbStripMessageLayout')
    cmds.showWindow('groomKitMeshStripWin')
    
    cleanupAbortedMSNodes()
    
    if not checkForCurrentMeshStrip():
        meshStripWinInit()
    if cmds.getAttr('meshGenGBNode.currentMeshStripNode'):
        stripLiveUIUpdateInit()
#    cmds.columnLayout('meshStripL0', edit = True, vis = True) 
#    cmds.columnLayout('meshStripL1', edit = True, vis = False)    
    if origSel:
        cmds.select(origSel, r = True)
    else:
        cmds.select(cl = True)        
    
    checkForCancelMeshStripVis()

    if checkForCurrentMeshStrip():
#        print 'control ui'
        meshStripControlsUIShow()
             
    

def checkForCancelMeshStripVis():
    
    currMSNode = ''
    if cmds.objExists('meshGenGBNode'):
        currMSNode = cmds.getAttr('meshGenGBNode.currentMeshStripNode')
    if not currMSNode:
        cmds.button('cancelStripDef', edit = True, vis = False)
    else:
        if not cmds.getAttr(currMSNode + '.stripIPCurves'):
            cmds.button('cancelStripDef', edit = True, vis = True)                

def checkForCurrentMeshStrip():
    
    currMSNode = ''
    if cmds.objExists('meshGenGBNode'):
        currMSNode = cmds.getAttr('meshGenGBNode.currentMeshStripNode')
        
    if currMSNode:
        if cmds.getAttr(currMSNode + '.msGrp'):
            return True
#            meshStripControlsUIShow()
                

def cancelMeshStripDef():
    
    option = cmds.confirmDialog( title='Cancel Mesh Strip Character Setup', message='Are you sure you do not want to continue with this Character?', button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No' )
    if option == 'Yes':
        cancelMeshStripCharSetup()
    
    
def cleanupAbortedMSNodes():
    
    meshStripNodes = getMeshStripNodes()
    nodeDeleted = False
    if meshStripNodes:
        for node in meshStripNodes:
            if not cmds.getAttr(node + '.stripIPCurves'):
#                print 'deleted node', node
                cmds.delete(node)
                nodeDeleted = True
    meshStripNodes = getMeshStripNodes('all')
    lastNode = ''
    if meshStripNodes:
        lastNode = meshStripNodes[-1]
    else:
        menuNewMeshStripSetup()
                
#    print 'setting at 17356'
    if nodeDeleted:
        cmds.setAttr('meshGenGBNode.currentMeshStripNode', lastNode, type = 'string')
    

def cancelMeshStripCharSetup():
    
    currMSNode = cmds.getAttr('meshGenGBNode.currentMeshStripNode')
    ipScalp = cmds.getAttr(currMSNode + '.inputScalp')
    msGrp = cmds.getAttr(currMSNode + '.msGrp')
    meshStripNodes = getMeshStripNodes()
    meshStripNodes.remove(currMSNode)
    updateMeshStripMenuRadio(currMSNode)
    cmds.delete(currMSNode)
    menuNewMeshStripSetup()

def updateMeshStripMenuRadio(msNode):
    
    meshStripNodes = getMeshStripNodes()
    ipScalp = cmds.getAttr(msNode + '.inputScalp')
    cmds.deleteUI(msNode + '_radio', mi = True)
    

def menuNewMeshStripSetup():
    
    cmds.columnLayout('meshStripL0', edit = True, vis = True)
    cmds.columnLayout('meshStripL1', edit = True, vis = False)
    cmds.button('cancelStripDef', edit = True, vis = False)
    useGB = False
    if cmds.objExists('gbNode'):
#        if cmds.getAttr('gbNode.currentGBNode'):
            if checkForExistingGBMSNodes():
                useGB = True
                cmds.radioButtonGrp('gbOrCustRadio', edit = True ,vis = True, sl = 1)
                useGBForStrip()

    if not useGB:
#        cmds.radioButtonGrp('gbOrCustRadio', edit = True ,vis = True, sl = 2)
#        print 'use cust 17404'
        if not gbType == 0:
            useCustForStrip()
        else:
            reportGBMeshStripMessage('Groomboy DEMO Version works only with Groomboy Setup. Please draw Freeform Guides and Assign Volume ', True, True, 'red')
#            reportGBMessage('Groomboy DEMO Version works only with Groomboy Setup', True, True, 'red')
                        

def menuRemoveMeshStripSetup():
    
    meshStripNodes = getMeshStripNodes('all')
    if not meshStripNodes:
        reportGBMeshStripMessage('No Mesh Strip Setup found', True, True, 'red')
        
    option = cmds.confirmDialog( title='Remove Mesh Strip Setup', message='Are you sure you do not want to continue with this Character Mesh Strip Setup?', button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No' )
    if option == 'Yes':
        menuRemoveMeshStripSetupExec()

def updateStripRadioComplete():       

    meshStripNodes = getMeshStripNodes()  

    if cmds.radioMenuItemCollection('meshStripCustMeshRadio', q = True, exists = True):
        allMI = cmds.lsUI(mi = True)
        for mi in allMI:
            if cmds.menuItem(mi, q = True, collection = True) == 'meshStripCustMeshRadio':
                cmds.deleteUI(mi)
#        cmds.deleteUI('meshStripCustMeshRadio', ric = True)
#    cmds.radioMenuItemCollection('meshStripCustMeshRadio', p = 'meshStripCustMenu')
#    if meshStripNodes:
#        for msNode in meshStripNodes:
#            cmds.menuItem(msNode + '_radio', label = cmds.getAttr(msNode + '.displayName'), c = 'meshStripRadioSelected()', radioButton = False, p = 'meshStripCustMeshRadio')
#    cmds.menuItem('meshStripMenuDivider', d = True, p = 'meshStripCustMenu')        
#    cmds.menuItem('addNewMeshStripMenu', label = 'Add New Mesh Strip Setup', p = 'meshStripCustMenu' , c = 'menuNewMeshStripSetup()')   
#    cmds.menuItem('removeMeshStripMenu', label = 'Remove Mesh Strip Setup', p = 'meshStripCustMenu', c = 'menuRemoveMeshStripSetup()')
    

def menuRemoveMeshStripSetupExec():
    
    currMSNode = cmds.getAttr('meshGenGBNode.currentMeshStripNode')
        
    gbNode = ''
    if cmds.attributeQuery('connectedGBNode', node = currMSNode, exists = True):
        gbNode = cmds.getAttr(currMSNode + '.connectedGBNode')
    
    if not gbNode:
        ipScalp = cmds.getAttr(currMSNode + '.inputScalp')
        ipCurvesGrp = 'inputStripCurvesFor_' + ipScalp
        cmds.parent(ipScalp, world = True)
        cmds.parent(ipCurvesGrp, world = True)
        cmds.rename(ipCurvesGrp, 'curvesGroup')
        cmds.deleteUI(currMSNode + '_radio', mi = True)
        
    msGrp = cmds.getAttr(currMSNode + '.msGrp')
    cmds.delete(msGrp)
    cmds.delete(currMSNode)
    
    meshStripNodes = getMeshStripNodes()
    lastNode = ''
    if meshStripNodes:
        lastNode = meshStripNodes[-1]
    cmds.setAttr('meshGenGBNode.currentMeshStripNode', lastNode, type = 'string')
    updateStripRadioComplete()
    menuNewMeshStripSetup()       
                
    
def checkForExistingGBMSNodes():
    
    
    currNode = cmds.getAttr('gbNode.currentGBNode')
    gbMeshStripNodes = getMeshStripNodes('gb')          
    if gbMeshStripNodes:
        for msNode in gbMeshStripNodes:
            gbNode = cmds.getAttr(msNode + '.connectedGBNode')
            if currNode == gbNode:
                return False
            else:
                return True                
    else:
        return True                       
            
    
    
    
def meshStripWinInit():

    cmds.columnLayout('meshStripL0', edit = True, vis = True)
    cmds.columnLayout('meshStripL1', edit = True, vis = False) 
    
    meshStripNodes = getMeshStripNodes()   
    if meshStripNodes:
        cmds.menu('meshStripCustMenu', edit = True, vis = True)
    cmds.button('cancelStripDef', edit = True, vis = False)
    currMSNode = cmds.getAttr('meshGenGBNode.currentMeshStripNode')
    currNode = ''
    if currMSNode:
        mesh = cmds.getAttr(currMSNode + '.inputScalp')
#        cmds.radioMenuItemCollection('meshStripCustMeshRadio', edit = True, select = currMSNode + '_radio')
        if not cmds.objExists(currMSNode + '.connectedGBNode'):
#        if not cmds.getAttr(currMSNode + '.connectedGBNode'):
            cmds.menuItem(currMSNode + '_radio', edit = True, rb = True)
        if not cmds.getAttr(currMSNode + '.stripIPCurves') and not cmds.attributeQuery('connectedGBNode', node = currMSNode, exists = True):
#            print 'here'
            cmds.radioButtonGrp('gbOrCustRadio', edit = True, vis = False)
            cmds.button('useSelMeshForStripsBtn', edit = True, vis = False)
            cmds.button('useSelCurvesCustMeshBtn', edit = True, vis = True)
            cmds.columnLayout('meshStripL1', edit = True, vis = False)
        else:
            meshStripControlsUIShow()
    
    else:
        if cmds.objExists('gbNode'):
            currNode = cmds.getAttr('gbNode.currentGBNode')
         
        if not currNode:
#            print 'use cust 17513'
            useCustForStrip()
        else:
            cmds.radioButtonGrp('gbOrCustRadio', edit = True, vis = True)
            cmds.button('useGBNodeForStrips', edit = True, vis = False)
            cmds.button('useSelMeshForStripsBtn', edit = True, vis = False)
            useGBForStrip()            
                        
                          
def useGBForStrip():
    
    useGB = False
    if cmds.objExists('gbNode'):
        currNode = cmds.getAttr('gbNode.currentGBNode')
        displayName = cmds.getAttr(currNode + '.displayName')
        manualCurves = cmds.getAttr(currNode + '.manualCurves')
        if manualCurves and displayName:
            useGB = True

#    print 'display name', displayName    
    if useGB:
#        print 'jere'
        cmds.button('useGBNodeForStrips', edit = True, vis = True)
        cmds.button('useGBNodeForStrips', edit = True, label = 'Use ' + displayName + ' Setup for Mesh Strips')
    else:
        reportGBMeshStripMessage('No Groomboy Setup found', True, True, 'red')
        cmds.button('useGBNodeForStrips', edit = True, vis = False)
    
    cmds.button('useSelMeshForStripsBtn', edit = True, vis = False)

#    meshStripControlsUIShow()
    resetGBMeshStripStatus()
    
      
def useCustForStrip():
    
    meshSel = True
    sel = cmds.ls(sl = True)
    if len(sel) > 0:
        if not cmds.ls(cmds.listRelatives(sel[0], s = True), type = 'mesh'):
            message = 'Use Selected Mesh'
            meshSel = False
#            reportGBMeshStripMessage('No Poly Mesh Selected', False, True, 'yellow')                                            
    else:
#        reportGBMeshStripMessage('Nothing Selected', False, True, 'yellow')
        message = 'Use Selected Mesh'
        meshSel = False
    
       
    if meshSel:
        message = 'Use ' + sel[0] + ' as Scalp for Mesh Strips'
    cmds.button('useGBNodeForStrips', edit = True, vis = False)
#    print 'button here 17561'
    cmds.button('useSelMeshForStripsBtn', edit = True, vis = True, label = message)
    cmds.button('useSelCurvesCustMeshBtn', edit = True, vis = False)
        
    
def reportGBMeshStripMessage(message, isError, isUndo, colorVal = 'red'):
    
#    print message
    colorRange = { 'red' : [1.0,0.0,0.0] , 'yellow' : [1.0,1.0,0.0], 'blue' : [0.0,0.7,1.0] }
    cmds.text('gbStripMessageStatusColor', edit = True, vis = True, bgc = colorRange[colorVal])
    cmds.text('gbStripMessageStatusText', edit = True, vis = True,  label = '  ' + message)
    
    cmds.scriptJob(event = ['SelectionChanged','resetGBMeshStripStatus()'], runOnce = True, killWithScene = True, p = 'groomKitMeshStripWin')
    
    if isError:
        raise RuntimeError, message
    else:
        cmds.warning(message)

def continueCustMeshStripInit():

    sel = cmds.ls(sl = True)
    meshSel = True
    if len(sel) > 0:
        if not cmds.ls(cmds.listRelatives(sel[0], s = True), type = 'mesh'):
            meshSel = False
            reportGBMeshStripMessage('No Poly Mesh Selected', True, True, 'red')                                            
    else:
        meshSel = False
        reportGBMeshStripMessage('Nothing Selected', True, True, 'red')
    
    if meshSel:
        if gbType == 0:
            result = verifyForTESTVERSION(sel[0], False)
            if not result:
                cmds.select(cl = True)
                useCustForStrip()
                reportGBMeshStripMessage('Only specific mesh work in DEMO Version.', True, True, 'red')     
                
            
            
    if meshSel:
        
        inputScalp = cmds.duplicate(sel[0], name = sel[0] + '_GB', rc = True, rr = True)[0]
        cmds.setAttr(sel[0] + '.visibility', False)
        cmds.select(inputScalp, r = True)
        sel[0] = inputScalp
        
        newCustMeshStripNodeCreated(sel[0])
#        meshStripNodeAttrInit(sel[0], 'custom')
        currMSNode = cmds.getAttr('meshGenGBNode.currentMeshStripNode')
        cmds.setAttr(currMSNode + '.inputScalp', sel[0], type = 'string')
    
        
        cmds.button('useSelMeshForStripsBtn', edit = True, vis = False)
        cmds.button('cancelStripDef', edit = True, vis = True)
        cmds.button('useSelCurvesCustMeshBtn', edit = True, vis = True)
        cmds.radioButtonGrp('gbOrCustRadio', edit = True, vis = False)
        
        if not cmds.objExists('gbNode'):
            if cmds.columnLayout('cL0Layout', exists = True):
                cmds.columnLayout('cL0Layout', edit = True, vis = False)
        
        
    
def resetGBMeshStripStatus():
    
    cmds.text('gbStripMessageStatusColor',edit = True, vis = False)
    cmds.text('gbStripMessageStatusText', edit = True, vis = False, label = '')
    
    
def getMeshStripNodes(mode = 'cust'):
    
    meshStripNodes = []
    networkNodes = cmds.ls(type = 'network')
    if networkNodes:
        for node in networkNodes:
            if cmds.attributeQuery('isAMeshStripNode', node = node, exists = True):
                if cmds.getAttr(node + '.isAMeshStripNode'):
                    if mode == 'all':
                        meshStripNodes.append(node)
                    elif mode == 'gb':
                        if cmds.attributeQuery('connectedGBNode', node = node, exists = True):
                            meshStripNodes.append(node)
                    else:                        
                        if not cmds.attributeQuery('connectedGBNode', node = node, exists = True):
                            meshStripNodes.append(node)
    
    return meshStripNodes    
                
    
def useSelCurvesCustMesh():
    
    import cPickle as Pickle
    sel = cmds.ls(sl = True)
    
    super = []
    if not sel:
        reportGBMeshStripMessage('Nothing Selected', True, True, 'red')
    else:        
        super = cmds.listRelatives(cmds.listRelatives(cmds.ls(sl = True), ad = True, typ = 'nurbsCurve'), p = True)
    
    if not super:
        reportGBMeshStripMessage('No Curves Selected', True, True, 'red')
    
    curveList = super    
    
    currMSNode = cmds.getAttr('meshGenGBNode.currentMeshStripNode')
    ipCurvesString = str(Pickle.dumps(curveList))
    cmds.setAttr(currMSNode + '.stripIPCurves', ipCurvesString, type = 'string')
    createMeshStripMainGroup(curveList,'cust')
    
    createStripScalpShoveMeshMain()
    
    generateGBMeshStrips(curveList, 'new')
    
    cmds.select(cl = True)
    meshStripControlsUIShow()
    cmds.evalDeferred('reapplyGBStripShader()')
    

def continueGBMeshStripInit():
    
    import cPickle as Pickle
    currNode = cmds.getAttr('gbNode.currentGBNode')
    ipScalp = cmds.getAttr(currNode + '.scalpMesh')
    meshStripNodeAttrInit(ipScalp, 'gb')
    stripIPCurvesString = cmds.getAttr(currNode + '.manualCurves')
    currMSNode = cmds.getAttr('meshGenGBNode.currentMeshStripNode')
    stripIPCurves = []
    if gbType == 0:
        stripIPCurves = Pickle.loads(str(stripIPCurvesString))
        if stripIPCurves:
            stripMax = getStripMaxCount()
            stripIPCurves = stripIPCurves[0:stripMax]
            stripIPCurvesString = Pickle.dumps(stripIPCurves)
        
    
#    print 'gb node create current ms node', currMSNode
    cmds.setAttr(currMSNode + '.inputScalp', ipScalp, type = 'string')
    cmds.setAttr(currMSNode + '.stripIPCurves', stripIPCurvesString, type = 'string')
    createMeshStripMainGroup(currNode,'gb')
    createStripScalpShoveMeshMain()
    generateGBMeshStrips()
    meshStripControlsUIShow()
    cmds.evalDeferred('reapplyGBStripShader()')
    
def meshStripControlsUIShow():
    
    if not cmds.window('groomKitMeshStripWin', exists = True):
        return
    cmds.columnLayout('meshStripL0', edit = True, vis = False)
    cmds.columnLayout('meshStripL1', edit = True, vis = True)
    cmds.button('cancelStripDef', edit = True, vis = False)

    cmds.menu('meshStripCustMenu', edit = True, vis = True)
    
    stripLiveUIUpdateInit()
    
def newCustMeshStripNodeCreated(chr):
    
    cmds.menu('meshStripCustMenu', edit = True, vis = True)
    cmds.menuItem('meshStripNode_' + chr + '_radio', label = 'Mesh Strips from ' + chr, ia = '', radioButton = True, cl = 'meshStripCustMeshRadio', c = 'meshStripRadioSelected()', p = 'meshStripCustMenu')   
    meshStripNodeAttrInit(chr,'custom')
    
def meshStripNodeAttrInit(mesh, type):
    
    nwNode = cmds.createNode('network', ss = True, name = 'meshStripNode_' + mesh)    
    cmds.addAttr(nwNode, ln = 'isAMeshStripNode', attributeType = 'bool', dv = True)
    if type == 'gb':
        cmds.addAttr(nwNode, ln = 'connectedGBNode', dt = 'string')
        currNode = cmds.getAttr('gbNode.currentGBNode')
        cmds.setAttr(nwNode + '.connectedGBNode', currNode, type = 'string')
#    print 'setting at 17686'        
    cmds.setAttr('meshGenGBNode.currentMeshStripNode', nwNode, type = 'string')
    cmds.addAttr(nwNode, ln = 'displayName', dt = 'string')
    cmds.setAttr(nwNode + '.displayName', 'Mesh Strips from ' + mesh, type = 'string')
    cmds.addAttr(nwNode, ln = 'stripIPCurves', dt = 'string')
    cmds.addAttr(nwNode, ln = 'inputScalp', dt = 'string')
    cmds.setAttr(nwNode + '.inputScalp', mesh, type = 'string')
    cmds.addAttr(nwNode, ln = 'msGrp', dt = 'string')
    cmds.addAttr(nwNode, ln = 'overrideStripCurves', dt = 'string')
    cmds.addAttr(nwNode, ln = 'globalStripValues', dt = 'string')
    cmds.addAttr(nwNode, ln = 'stripValuesDict', dt = 'string')
    cmds.addAttr(nwNode, ln = 'stripProperties', dt = 'string')
    cmds.addAttr(nwNode, ln = 'stripMaxDiv')
    cmds.setAttr(nwNode + '.stripMaxDiv', 10)
    
    cmds.addAttr(nwNode, ln = 'widthAdaptive', attributeType = 'bool', dv = False)
    cmds.addAttr(nwNode, ln = 'widthAdpBlend', attributeType = 'float', dv = 1.0)    

    cmds.addAttr(nwNode, ln = 'divAdaptive', attributeType = 'bool', dv = False)    
    cmds.addAttr(nwNode, ln = 'divAdpBlend', attributeType = 'float', dv = 1.0)    
    
    cmds.addAttr(nwNode, ln = 'segAdaptive', attributeType = 'bool', dv = False)    
    cmds.addAttr(nwNode, ln = 'segAdpBlend', attributeType = 'float', dv = 1.0)    

    cmds.addAttr(nwNode, ln = 'removeStripsList', dt = 'string')
    cmds.addAttr(nwNode, ln = 'addStripsList', dt = 'string') 

    cmds.addAttr(nwNode, ln = 'stripGraphClipboard', dt = 'string')     
    cmds.addAttr(nwNode, ln = 'stripMaxCount', attributeType = 'float', dv = 10.0)     
    cmds.addAttr(nwNode, ln = 'stripDisplacement', attributeType = 'float', dv = 0.0)     
    
       
    
    loadGlobalStripControls()
        
def createMeshGenGBNode():
    
    if cmds.objExists('meshGenGBNode'):
        return
    cmds.createNode('network', n = 'meshGenGBNode')
    cmds.addAttr('meshGenGBNode', ln = 'currentMeshStripNode', dt = 'string')
    cmds.addAttr('meshGenGBNode', ln = 'bgUIColor', at = 'float')

    
def meshStripRadioSelected():
    
    cmds.columnLayout('meshStripL1', edit = True, vis = True)
    meshStripNodes = getMeshStripNodes()
    selectedMSNode = ''
    for msNode in meshStripNodes:
        if cmds.menuItem(msNode + '_radio', q = True, radioButton = True):
#            print msNode, 'AAA'
            selectedMSNode = msNode
#    print 'setting at 17725'
    cmds.setAttr('meshGenGBNode.currentMeshStripNode', selectedMSNode, type = 'string')
#    print cmds.getAttr('meshGenGBNode.currentMeshStripNode'), 'QQQQQ'
#    print selectedMSNode, 'WWWWW'
    
    allMeshStripNodes = getMeshStripNodes('all')
    for msNode in allMeshStripNodes:
        if msNode == selectedMSNode:
            mainGrp = cmds.getAttr(msNode + '.msGrp')
            cmds.setAttr(mainGrp + '.visibility', True)
        else:
            if cmds.attributeQuery('connectedGBNode', node = msNode, exists = True):
                currNode = cmds.getAttr(msNode + '.connectedGBNode')
                mainGrp = cmds.getAttr(currNode + '.mainGroup')
                cmds.setAttr(mainGrp + '.visibility', False)
            else:
                mainGrp = cmds.getAttr(msNode + '.msGrp')
                cmds.setAttr(mainGrp + '.visibility', False)

    allGBNodes = getCharNodes()
    
    for each in allGBNodes:
        cmds.setAttr(cmds.getAttr(each + '.mainGroup') + '.visibility', False)
        cmds.menuItem(each + '_radio', edit = True, rb = False)
    
    
    if cmds.columnLayout('cL0Layout', exists = True):
#        print 'here'
        if cmds.objExists('gbNode'):
#            print 'hiding cl0'
            cmds.columnLayout('cL0Layout', edit = True, vis = False) 
        else:
            cmds.columnLayout('cL0Layout', edit = True, vis = True) 
            

    gbCloseup(cmds.getAttr(selectedMSNode + '.inputScalp'))
    meshStripControlsUIShow()                
    
                

def createMeshStripMainGroup(nodeOrCurves, mode):
    
    currMSNode = cmds.getAttr('meshGenGBNode.currentMeshStripNode')
    currSel = cmds.ls(sl = True)
    import cPickle as Pickle
    ipScalp = cmds.getAttr(currMSNode + '.inputScalp')
    msGrp = ipScalp + '_meshStripsMainGrp' 
    if not cmds.objExists(msGrp):
        msGrp = cmds.group(name = msGrp, em = True, world = True)
        if mode == 'gb':
            parentGrp = cmds.getAttr(nodeOrCurves + '.mainGroup')
            cmds.parent(msGrp, parentGrp)
        else:
            ipScalp = cmds.getAttr(currMSNode + '.inputScalp')
            ipCurves = nodeOrCurves
            ipCurvesGrp = 'inputStripCurvesFor_' + ipScalp
            cmds.group(name = ipCurvesGrp, em = True, parent = msGrp)
            cmds.parent(ipCurves, ipCurvesGrp)
            cmds.parent(ipScalp, msGrp)
                                                
    cmds.setAttr(currMSNode + '.msGrp', msGrp, type = 'string')
    if currSel:
        cmds.select(currSel, r = True)  
    else:
        cmds.select(cl = True)        
    return msGrp


def createMeshStripSubGroup():
    
    currMSNode = cmds.getAttr('meshGenGBNode.currentMeshStripNode')
    msGrp = cmds.getAttr(currMSNode + '.msGrp')
    ipScalp = cmds.getAttr(currMSNode + '.inputScalp')
    
    polyStripGrp = 'polyStripNodesFor_' + ipScalp
    tempStripGrp = 'tempStripNodesFor_' + ipScalp
    if not cmds.objExists(polyStripGrp):
        cmds.group(name = polyStripGrp, em = True, parent = msGrp)
    if not cmds.objExists(tempStripGrp):        
        cmds.group(name = tempStripGrp, em = True, parent = msGrp)
    
    return [polyStripGrp, tempStripGrp]
    
def checkForUniqueNewStrip(newList):
    
    import cPickle as Pickle
    currMSNode = cmds.getAttr('meshGenGBNode.currentMeshStripNode')
    
    stripIPCurves = []
    stripIPCurvesString = cmds.getAttr(currMSNode + '.stripIPCurves')
    if stripIPCurvesString:
        stripIPCurves = Pickle.loads(str(stripIPCurvesString))   
    
    if not stripIPCurves:
        return newList

#    print newList, stripIPCurves, 'new new new'        
    newList = list(set(newList) - set(stripIPCurves))
#    print newList, 'new new new'
    return newList        
    
                
    
def getStripMaxCount():
    
    return 10
    currMSNode = cmds.getAttr('meshGenGBNode.currentMeshStripNode')
    stripMaxCount = cmds.getAttr(currMSNode + '.stripMaxCount')
#    return int(stripMaxCount)
    
def getExistStripCurvesLen():
    
    import cPickle as Pickle
    currMSNode = cmds.getAttr('meshGenGBNode.currentMeshStripNode')
#    existLen = cmds.getAttr(currMSNode + '.stripDisplacement')
    stripIPCurves = []
    stripIPCurvesString = cmds.getAttr(currMSNode + '.stripIPCurves')
    if stripIPCurvesString:
        stripIPCurves = Pickle.loads(str(stripIPCurvesString))   
    
    return len(stripIPCurves)
    
        
    

def generateGBMeshStrips(custCurves = False, mode = 'new'):
    
    import cPickle as Pickle
    import random as random        
    currMSNode = cmds.getAttr('meshGenGBNode.currentMeshStripNode')
    defaultDictValues = getDefaultStripDict()
    currSel = cmds.ls(sl = True)
#    print 'generate gb strips sel', currSel

    ipScalp = cmds.getAttr(currMSNode + '.inputScalp')
#    print '>', getStripValuesDict()
    if custCurves:
        stripIPCurves = custCurves
    else:
        stripIPCurves = getStripIPNodes(True, 'gen')    

#    print 'generate strips from this', stripIPCurves, mode
    newStripIPCurves = []
    '''
    if gbType == 0:
        lenMax = len(stripIPCurves)
        len30 = int(lenMax * 0.3)
        for x in range(len30):
            curStrip = stripIPCurves[random.randrange(0,lenMax)]
            print x, curStrip
            newStripIPCurves.append(curStrip)
        
        stripIPCurves = newStripIPCurves
        print stripIPCurves , '<<<<'    
        
    '''
    charCPNode = createCPNode(ipScalp)
    historyDelete = []
    historyDelete.append(charCPNode)
    
    groupNodes = createMeshStripSubGroup()
    meshStripNodeGrp = groupNodes[0]
    tempStripNodeGrp = groupNodes[1]
    
    extNodes = []
    crvNodes = []
    
    
    stripProperties = getGBStripProperties('only')
    stripAvgLength = stripProperties[0]
    
    
    
    stripMaxCount = getStripMaxCount()
    stripDict = getStripValuesDict()
    
#    print 'to generate strips', stripIPCurves 

    toAddlist = []
    toRemoveList = []
    toRemoveLen = 0
    if gbType == 0:
        existList = stripDict.keys()
        if 'globalPolyExtrude' in existList:
            existList.remove('globalPolyExtrude')
        existLen = len(existList)
        onlyNewList = list(set(stripIPCurves) - set(existList))
        onlyNewLen = len(onlyNewList)
        availLen = stripMaxCount - existLen
        if availLen > 0:
            toRemoveLen = onlyNewLen - availLen
            if toRemoveLen > 0:
                toRemoveList = onlyNewList[-int(toRemoveLen):]
                            
        else:
            toRemoveList = onlyNewList
        
        if toRemoveList:
            for each in toRemoveList:
                stripIPCurves.remove(each)
                cmds.warning('DEMO VERSION: MAX STRIPS COUNT IS: ' + str(int(stripMaxCount)) + ' STRIPS ! ' + each + ' INPUT CURVE NOT ADDED !')
                
        
#        print 'exist', existList, existLen, 'only new', onlyNewList, onlyNewLen, 'avail', availLen, 'torem', toRemoveList, toRemoveLen, 'stripip', stripIPCurves                
                        
                
                                    
        
    

    if gbType == 100:
        
        
        existList = stripDict.keys()
        newList = []
        newList.extend(stripIPCurves)
        toAddList = list(set(newList) & set(existList))
        onlyNewList = list(set(newList) - set(existList))
        onlyNewLen = len(onlyNewList)

#        existLen = len(existList)
        existLen = getExistStripCurvesLen()

        stripMaxCount = getStripMaxCount()
        availLen = stripMaxCount - existLen
        currStripLen = existLen
        
#        print 'exist', existList, existLen, 'to add', toAddList, 'only new', onlyNewList, onlyNewLen
        
        
        for x in range(onlyNewLen):
            if currStripLen <= stripMaxCount:
                stripIPCurves.append(onlyNewList[x])
            else:
                cmds.warning('DEMO VERSION: MAX STRIPS COUNT IS: ' + str(stripMaxCount) + ' ' + onlyNewList[x] + ' INPUT CURVE NOT ADDED')

            currStripLen = currStripLen + 1

        
        
        
        '''
        len30 = int(onlyNewLen * 0.3)
        for x in range(len30):
            curStrip = onlyNewList[random.randrange(0,onlyNewLen)]
#            print x, curStrip
            toAddList.append(curStrip)
        
        
        
        
        availLen = stripMaxCount - existLen
        
        print 'stripMax', stripMaxCount, 'exist', existLen, 'avail', availLen
        maxIndex = 0
        if availLen > 0:
            if availLen <= onlyNewLen:
                maxIndex = availLen
            else:
                maxIndex = onlyNewLen
            toAddList.extend(onlyNewList[0:maxIndex+1])
            
        cmds.setAttr(currMSNode + '.stripDisplacement',existLen + maxIndex)
        
        
        leftCurves = list(set(onlyNewList) - set(toAddList))
        if leftCurves:
            cmds.confirmDialog(title = 'WARNING', message = 'DEMO VERSION !! BUY LICENSED VERSION FOR STRIP GENERATION ON ALL CURVES', button = 'OK')
            cmds.warning('DEMO VERSION: FOLLOWING CURVES NOT ADDED:')
#            print 'DEMO VERSION: FOLLOWING CURVES NOT ADDED:'
            for each in leftCurves:
#                print each
                cmds.warning(each)
        stripIPCurves = toAddList
        '''
    stripIPCurves = list(set(stripIPCurves))
    
#    print 'final list', stripIPCurves
    if mode == 'new':
#        stripIPCurves = checkForUniqueNewStrip(stripIPCurves)
        meshStripDictAdd(stripIPCurves)
    
    stripDict = getStripValuesDict()
#    print 'final stripDict', stripDict
    if cmds.objExists('uvGBTempPlane'):
        cmds.delete('uvGBTempPlane')
    
    uvGBTempPlane = cmds.polyPlane(name = 'uvGBTempPlane', sx = 2, cuv = 2)
#    cmds.polyFlipUV(uvGBTempPlane[0], flipType = 1, local = True)
    
    if mode == 'restore':
        divList = [stripDict[crv][6] for crv in stripIPCurves]
        widthList = [stripDict[crv][0] for crv in stripIPCurves]
        
    else:
        divList = getDivForStrip(stripIPCurves, stripProperties)
        widthList = getWidthForStrip(stripIPCurves, stripProperties)
    
    divCount = 0
#    extEdgeList = [[0],[0,4],[0,4,7],[0,4,7,10],[0,4,7,10,13],[0,4,7,10,13,16]]
#    extEdgeList = [[3],[0,4],[0,8,4],[0,11,4,8],[0,14,11,4,8],[0,17,14,4,12,8]]
    
#    print 'to generate strips', stripIPCurves 

    


    for crv in stripIPCurves:

        if 'globalPolyExtrude' in crv:
            continue
            
        stpName = crv + '_polyStrip'

        if cmds.objExists(stpName):
#            print 'deleting ', stpName
            cmds.delete(stpName, ch = True)
            cmds.delete(stpName)
        
        pos = cmds.pointOnCurve(crv, p = True)
        cmds.setAttr(charCPNode + '.ip', pos[0], pos[1], pos[2])
        normal = list(cmds.getAttr(charCPNode + '.n')[0])
        
#        normal = cmds.pointOnCurve(crv, no = True)
        tangent = cmds.pointOnCurve(crv, t = True)
        cross = getCrossProductGB(normal,tangent)
        unitCross = list(mm.eval('unit <<' + str(cross[0])+ ',' + str(cross[1]) + ',' + str(cross[2]) + '>>'))
        
        
#        scaleWidth = stripDict[crv][0]
#        scaleWidth = 10.0
#        width = getStripWidthFromScale(scaleWidth)
        width = 1.0
        dist = width * 0.5
        
        newPosA = [a + b for a,b in zip(pos,[dist* x for x in unitCross])]
        newPosB = [a + b for a,b in zip(pos,[-1*dist * x for x in unitCross])]
        midAB = pos
        
        
        baseName = 'baseCrv_polyStrip_' + crv
        
        if cmds.objExists(baseName):
#            print 'deleting' , baseName
            cmds.delete(baseName)
        
        baseCrv = cmds.curve(degree = 1, name = baseName, p = [newPosA, midAB, newPosB])
        cmds.setAttr(baseCrv + '.visibility', False)

#        print 'deleting' , baseCrv
#        historyDelete.append(baseCrv)
#        baseCrv = cmds.curve(degree = 1, name = baseName, p = [newPosA, newPosB])
        cmds.xform(baseCrv, piv = pos)
        cmds.setAttr(charCPNode + '.ip', newPosA[0], newPosA[1], newPosA[2])
        cPosA = list(cmds.getAttr(charCPNode + '.p')[0])
        cNormal = list(cmds.getAttr(charCPNode + '.n')[0])
#        touchRotate(baseCrv, pos, newPosA, cPosA)
        
#        cmds.makeIdentity(baseCrv, apply = True)
        
#        currWidLength = cmds.arclen(baseCrv)
#        newScl = width / currWidLength
#        cmds.scale(newScl, newScl, newScl, baseCrv)
                
        offsetDistPer = 5.0
        offsetDist = getStripWidthFromScale(offsetDistPer)
        
        extendCrv = cmds.extendCurve(crv, et = 2, d = offsetDist, s = 1, jn = False, rmk = False, rpo = False)[0]
#        print 'deleting' , extendCrv
        historyDelete.append(extendCrv)
        extendPos = cmds.xform(extendCrv + '.cv[0]', q = True, ws = True, t = True)
        cmds.xform(extendCrv, piv = extendPos)
        
        extendBase = baseCrv + '_extend'
        if cmds.objExists(extendBase):
            cmds.delete(extendBase)
       
        extendBase = cmds.duplicate(baseCrv, rc = True, name = extendBase)[0]
#        print 'deleting' , extendBase
        historyDelete.append(extendBase)
        extendPC = cmds.pointConstraint(extendCrv, extendBase)
#        print 'deleting' , extendPC
        cmds.delete(extendPC)
        
#        print stripDict[crv][9], 'whers the prob'
        segments = stripDict[crv][9]
#        segments = segments + 1
#        segments = convertSegmentsDictToNode(segments)
#        if not segments == 2:
#            cmds.rebuildCurve(baseCrv, rpo = True, rt = 0, end = 1, kr = 0, kt = False, s = segments, d = 1)
#            cmds.rebuildCurve(extendBase, rpo = True, rt = 0, end = 1, kr = 0, kt = False, s = segments, d = 1)
        
#        print 'loft segments', segments, stpName

#        extrudeNodes = cmds.extrude(extendBase, crv, rn = False, po = 1, et = 2,  rsp = 1)
        extrudeNodes = cmds.extrude(baseCrv, crv, rn = False, po = 1, et = 2,  rsp = 1)        
        cmds.rename(extrudeNodes[0], stpName)
        extNode = crv + '_stripNodeE'
        cmds.rename(extrudeNodes[1], extNode)
        
        nurbsTessOrig = cmds.listConnections(extNode, type = 'nurbsTessellate', d = True)
        nurbsTess = crv + '_stripNodeNT'
        cmds.rename(nurbsTessOrig, nurbsTess)
        
        segments = stripDict[crv][9]
        
        divisions = divList[divCount]
        stripDict[crv][6] = divisions
                
        width = widthList[divCount]
        maxPlaneSegs = 10
        
        
        cmds.setAttr(nurbsTess + '.polygonType', 1)
        cmds.setAttr(nurbsTess + '.format', 2)
        cmds.setAttr(nurbsTess + '.vType', 2)
        cmds.setAttr(nurbsTess + '.uNumber', segments+1)
        cmds.setAttr(nurbsTess + '.vNumber', divisions+1)
        
        extendPos = pos        
        cmds.xform(stpName, piv = extendPos)

        
        cmds.parent(stpName, meshStripNodeGrp)
#        cmds.parent(extendBase, tempStripNodeGrp)
#        cmds.parent(baseCrv, tempStripNodeGrp)
        

#        stpExtEdgeList = [stpName + '.e[' + str(x) + ']' for x in [2,5,8,11,14,17,20,23,26,29]]
        
#        print stpExtEdgeList, 'ext edges' 
       

        


        extNodes.append(extNode)
        
        width = widthList[divCount]
#        cmds.scale(width, width, width, extendBase)
        cmds.scale(width, width, width, baseCrv)
        stripDict[crv][0] = width
        

        
        divCount = divCount + 1
        cmds.polyNormal(stpName, normalMode = 2) 

        crvNodes.append(crv)
        
        cmds.move(extendPos[0], extendPos[1], extendPos[2], stpName + '.rotatePivot',  a = True)
        cmds.move(extendPos[0], extendPos[1], extendPos[2], stpName + '.scalePivot',  a = True)
        
        follNode = createFollicleOtherMesh(ipScalp)
        follShp = cmds.listRelatives(follNode, s = True)[0]
        cmds.setAttr(charCPNode + '.ip', midAB[0], midAB[1], midAB[2])
        cmds.setAttr(follShp + '.parameterU', cmds.getAttr(charCPNode+'.u'))
        cmds.setAttr(follShp + '.parameterV', cmds.getAttr(charCPNode+'.v'))
        mainGrp = crv + '_stripCtrlGrp0'
        subGrp = crv + '_stripCtrlGrp1'
        if cmds.objExists(mainGrp):
            cmds.delete(mainGrp)
           
        cmds.group(name = mainGrp, em = True)
        pc = cmds.parentConstraint(follNode, mainGrp)

        cmds.delete(pc)

        cmds.duplicate(mainGrp, name = subGrp, rr = True)
        cmds.select(cl = True)        
        cmds.parent(baseCrv, subGrp)
        cmds.parent(subGrp, mainGrp)
        cmds.parent(mainGrp, tempStripNodeGrp)
        
        cmds.delete(follNode)        
        

    cmds.delete(uvGBTempPlane)
    
    for h in historyDelete:
        if cmds.objExists(h):
            cmds.delete(h)
    
#    storeRestoreStripVtxPos([extNodes, crvNodes],'restore')
    
    if extNodes and crvNodes:
        stripTaperChange([extNodes, crvNodes], stripDict[crv][1])
        stripTwistChange([extNodes, crvNodes], stripDict[crv][4])
        stripTwistScaleChange([extNodes, crvNodes], stripDict[crv][5])
        stripTaperGraphChange([extNodes, crvNodes], stripDict[crv][2])            
        
        stripRotateChange([extNodes, crvNodes], stripDict[crv][3])            
        
        
        storeRestoreStripVtxPos([extNodes, crvNodes],'store')   
             
        stripCurvatureChangeUI([extNodes, crvNodes])
        storeRestoreRootVtxForStripShove([extNodes, crvNodes], 'store')
        
        stripShoveChange([extNodes, crvNodes], stripDict[crv][16])    
    
    stripDictString = cmds.getAttr(currMSNode + '.stripValuesDict')
    stripDict = Pickle.loads(str(stripDictString))
#    print stripDict['bkpExt_gbChar_01_1_Demo_Face_curve34'][13], '18168'
    
    stripDictString = Pickle.dumps(stripDict)
    cmds.setAttr(currMSNode + '.stripValuesDict',str(stripDictString), type = 'string')
    
    
    
    
    getGBStripProperties()
    
    if currSel:
        cmds.select(currSel, r = True)
    else:
        cmds.select(cl = True)
    
    if crvNodes:    
        assignGBStripShader(crvNodes)        
                   
def meshStripDictAdd(stpCrvs,index = 'na' ,value = 'na'):
    
#    print stpCrvs, value

    import cPickle as Pickle
    currMSNode = cmds.getAttr('meshGenGBNode.currentMeshStripNode')
    stripDictString = cmds.getAttr(currMSNode + '.stripValuesDict')
    stripDict = []
    if not stripDictString:
        stripDict = stripDictInit(currMSNode)
    else:
        stripDict = Pickle.loads(str(stripDictString))

    keys = stripDict.keys()
    defaultValuesDict = getDefaultStripDict()
    
#    newCrvs = list(set(stpCrvs) - set(keys))
    
    for crv in stpCrvs:
        if crv in keys:
            if not value == 'na':
                stripDict[crv][index] = value

        else:
            stripDict[crv] = []
            stripDict[crv].extend(defaultValuesDict)
            if not value == 'na':
                stripDict[crv][index] = value            
    
#    print stripDict['bkpExt_gbChar_01_1_Demo_Face_curve34'][13], '18208'
    stripDictString = Pickle.dumps(stripDict)
    cmds.setAttr(currMSNode + '.stripValuesDict', str(stripDictString), type = 'string')

def getDefaultStripDict():

    # 0 - width, 1 - taper, 2 - taper graph, 3 - rotate, 4 - twist, 5 - twist  scale , 6 - divisions, 7 - rotateDirection, 8 - curvature, 9 - segments
    # 10 - rootGraph, 11 - tipGraph, 12 - biasgraph, 13 - stripVtxPos, 14 - falloffgraph, 15 - curvHeight, 16 - shove, 17 - rootvtx, 18 - rotX, 19 - rotY, 20 - rotZ 
    import cPickle as Pickle
    currMSNode = cmds.getAttr('meshGenGBNode.currentMeshStripNode')
    stripDictString = cmds.getAttr(currMSNode + '.stripValuesDict')
    stripDict = {}
    if not stripDictString:
        return [1.0,1,'1,0,2,1,1,2', 0.0, 0, 1, 6, 1, '0.5,0,2,0.5,1,2', 3, '0.5,0,3,0.5,1,3', '0.5,0,3,0.5,1,3', 0.5, [], 0.5, 0.5, 1.0, [], 0.0, 0.0, 0.0]
#                0  1      2          3,  4, 5, 6,  7          8          9          10                 11          12  13  14   15   16  17   18   19   20
    else:
        stripDict = Pickle.loads(str(stripDictString))
        keys = stripDict.keys()
        if 'globalPolyExtrude' in keys:
            return stripDict['globalPolyExtrude']
     

def stripDictInit(msNode):

    dict = {}
    dict['globalPolyExtrude'] = getDefaultStripDict()
    return dict
                            
def touchRotateAngleOnly(p0,pA,pB):
    
    dA = [(c - d) for c, d in zip(pA,p0)] 
    dB = [(c - d) for c, d in zip(pB,p0)] 
    uA = mm.eval('unit <<' + str(dA[0]) + ',' + str(dA[1]) + ',' + str(dA[2]) + '>>')
    uB = mm.eval('unit <<' + str(dB[0]) + ',' + str(dB[1]) + ',' + str(dB[2]) + '>>')
    tRot = cmds.angleBetween( v1=uA, v2=uB)            
    return tRot[3]                   
        
def stripLiveUIUpdateInit():
    
    allJobs = cmds.scriptJob(lj = True)
    stripJob = False
    for job in allJobs:
        if 'stripLiveUIUpdate' in job:
            stripJob = True

    if not stripJob:            
        cmds.scriptJob(e = ['SelectionChanged', 'stripLiveUIUpdate()'], kws = True, cu = True, p = 'groomKitMeshStripWin')
    
    if not cmds.ls(sl = True):
        stripLiveUIUpdate()
    
def killStripLiveUIUpdate():
    
    allJobs = cmds.scriptJob(lj = True)
    for job in allJobs:
        if 'stripLiveUIUpdate' in job:
            cmds.scriptJob(kill = int(job.split(':')[0]))


def getExtCrvFromStripMesh(mesh):
#    mesh = 'bkpExt_gbChar_01_1_Demo_Face_curve31_polyStrip'
    extNode = stripCurve = baseCurve = False

    shp = cmds.listRelatives(mesh, s = True)
    if shp:
        if cmds.ls(shp[0], st = True)[1] == 'mesh' and '_polyStrip' in mesh:
            norm = cmds.listConnections(shp[0], type = 'polyNormal')
            if norm:
                nt = cmds.listConnections(norm[0], type = 'nurbsTessellate')
                if nt and '_stripNodeNT' in nt[0]:
                    ext = cmds.listConnections(nt[0], type = 'extrude')
                    if ext and '_stripNodeE' in ext[0]:
                        extNode = ext[0]
                        baseCurve = cmds.listConnections(extNode + '.profile', type = 'nurbsCurve')[0]
                        stripCurve = cmds.listConnections(extNode + '.path', type = 'nurbsCurve')[0]
                        
                    
#    if extNode and stripCurve and baseCurve:
    return [extNode,[stripCurve, baseCurve]]                   
    

def getStpNameFromExt(ext):
    
    stp = False
    nt = cmds.listConnections(ext, type = 'nurbsTessellate')
    if nt and '_stripNodeNT' in nt[0]:
        norm = cmds.listConnections(nt[0], type = 'polyNormal')
        if norm:
            shp = cmds.listConnections(norm[0], type = 'mesh')
            if shp and '_polyStrip' in shp[0]:
                stp = shp[0]
    
    return stp                    
        
    
    
            
def stripLiveUIUpdate():
    
#    print 'live'
#    cleanupAbortedMSNodes()
    currMSNode = cmds.getAttr('meshGenGBNode.currentMeshStripNode')
    if not currMSNode:
        return
    stripDict = getStripValuesDict()        
    stripCurves = stripDict.keys()
    sel = cmds.ls(sl = True)
    stripNodes = []
    selStrips = []
    if sel:
        for s in sel:
            stripNodes = getExtCrvFromStripMesh(s)
            if stripNodes:
                if stripNodes[0]:
                    selStrips.append(s)
            
    
    if not selStrips:
        loadGlobalStripControls()
    else:
        loadOverrideStripControls(selStrips[0])
        
    if gbType == 0:
        reportGBMeshStripMessage('This is Groomboy DEMO Version !', False, False, 'yellow')
            
#    if sel:
#        cmds.select(sel, r = True)
        
                
def loadGlobalStripControls():
    
    meshStripGlobalControlsDisplay(True)
    loadStripControls('globalPolyExtrude')
    loadAdaptiveStripControls()

def loadAdaptiveStripControls():
    
    currMSNode = cmds.getAttr('meshGenGBNode.currentMeshStripNode')

    widthAdp = cmds.getAttr(currMSNode + '.widthAdaptive')
    cmds.checkBox('stripWidthAdaptiveCB', edit = True, v = widthAdp)
    cmds.rowLayout('stripAdaptiveWidthRL', edit = True, vis = widthAdp)
    cmds.floatSliderGrp('stripAdpWidthSlider', edit = True, v = cmds.getAttr(currMSNode + '.widthAdpBlend'))
    
    segAdp = cmds.getAttr(currMSNode + '.segAdaptive')
    cmds.checkBox('stripSegmentsAdaptiveCB', edit = True, v = segAdp)
    cmds.rowLayout('stripAdaptiveSegmentsRL', edit = True, vis = segAdp)
    cmds.floatSliderGrp('stripAdpSegmentsSlider', edit = True, v = cmds.getAttr(currMSNode + '.segAdpBlend'))
    
    divAdp = cmds.getAttr(currMSNode + '.divAdaptive')
    cmds.checkBox('stripDivAdaptiveCB', edit = True, v = divAdp)
    cmds.rowLayout('stripAdaptiveDivRL', edit = True, vis = divAdp)
    cmds.floatSliderGrp('stripAdpDivSlider', edit = True, v = cmds.getAttr(currMSNode + '.divAdpBlend'))


def loadOverrideStripControls(stripNode):
    
    stripNodes = getExtCrvFromStripMesh(stripNode)
    if not stripNodes[0]:
        return
    
    ext = stripNodes[0]
    crv = stripNodes[1][0]
    meshStripGlobalControlsDisplay(False)
    loadStripControls(crv)
    
#        print crv
    
    
def meshStripGlobalControlsDisplay(mode):
    
#    print 'mode', mode
    widthAdp = cmds.checkBox('stripWidthAdaptiveCB', q = True, v = True)
    cmds.checkBox('stripWidthAdaptiveCB', edit = True, vis = mode)
    if widthAdp:
        cmds.rowLayout('stripAdaptiveWidthRL', edit = True, vis = mode)
    
#    segAdp = cmds.getAttr(currMSNode + '.segAdaptive')
    segAdp = cmds.checkBox('stripSegmentsAdaptiveCB', q = True, v = True)
    cmds.checkBox('stripSegmentsAdaptiveCB', edit = True, vis = mode)
    if segAdp:
        cmds.rowLayout('stripAdaptiveSegmentsRL', edit = True, vis = mode)    
        
#    divAdp = cmds.getAttr(currMSNode + '.divAdaptive')
    divAdp = cmds.checkBox('stripDivAdaptiveCB', q = True, v = True)    
    cmds.checkBox('stripDivAdaptiveCB', edit = True, vis = mode)
    if divAdp:
        cmds.rowLayout('stripAdaptiveDivRL', edit = True, vis = mode)            
    
    visb = not mode
    cmds.floatSliderGrp('stripRotateXSlider', edit = True, vis = visb)
    cmds.floatSliderGrp('stripRotateYSlider', edit = True, vis = visb)
    cmds.floatSliderGrp('stripRotateZSlider', edit = True, vis = visb)
    

def getStripValuesDict():
    
    import cPickle as Pickle
    
    stripExist = False
    if cmds.objExists('meshGenGBNode'):
        if cmds.getAttr('meshGenGBNode.currentMeshStripNode'):
            stripExist = True
    
    if not stripExist:
        return False            
             
    currMSNode = cmds.getAttr('meshGenGBNode.currentMeshStripNode')
    stripDictString = cmds.getAttr(currMSNode + '.stripValuesDict')
    stripDict = {}

    if stripDictString:
        stripDict = Pickle.loads(str(stripDictString))
    else:
        stripDictValue = getDefaultStripDict()        
        stripDict['globalPolyExtrude'] = stripDictValue
#        if 'bkpExt_gbChar_01_1_Demo_Face_curve34' in stripDict.keys():
#            print stripDict['bkpExt_gbChar_01_1_Demo_Face_curve34'][13], '18358'
        stripDictString = Pickle.dumps(stripDict)
        cmds.setAttr(currMSNode + '.stripValuesDict', str(stripDictString), type = 'string')

    return stripDict        

    

def loadStripControls(node):
    
#    print node
    stripDict = getStripValuesDict()
# stripDict['pSphere1_curve6']    
# node = 'stripCurvesA_64'
    if not node in stripDict.keys():
        return
        
    values = stripDict[node]

#   0 - width, 1 - taper, 2 - taper graph, 3 - rotate, 4 - twist, 5 - twist  scale, 6 - divisons
    cmds.intSliderGrp('stripSegmentsSlider', edit = True, value = values[9], bgc = getStripControlBGColor(node, 9))
    cmds.floatSliderGrp('stripWidthSlider', edit = True, value = values[0], bgc = getStripControlBGColor(node, 0))
    cmds.floatSliderGrp('stripTaperSlider', edit = True, value = values[1], bgc = getStripControlBGColor(node, 1))
    cmds.floatSliderGrp('stripRotateSlider', edit = True, value = values[3], bgc = getStripControlBGColor(node, 3))
    
    if node == 'globalPolyExtrude':
        visb = False
    else:
        visb = True
                
    cmds.floatSliderGrp('stripRotateXSlider', edit = True, vis = visb, value = values[18], bgc = getStripControlBGColor(node, 18))
    cmds.floatSliderGrp('stripRotateYSlider', edit = True,  vis = visb, value = values[19], bgc = getStripControlBGColor(node, 19))
    cmds.floatSliderGrp('stripRotateZSlider', edit = True,  vis = visb, value = values[20], bgc = getStripControlBGColor(node, 20))
    
    
    cmds.intSliderGrp('stripDivSlider', edit = True, value = values[6], bgc = getStripControlBGColor(node, 6))
    cmds.gradientControlNoAttr('stripTaperGraph', edit = True, asString = values[2])
    cmds.text('stripTaperGraphText', edit = True, bgc = getStripControlBGColor(node, 2))
#    print values[2]
    cmds.floatSliderGrp('stripTwistSlider', edit = True, value = values[4], bgc = getStripControlBGColor(node, 4))
    cmds.floatSliderGrp('stripTwistScaleSlider', edit = True, value = values[5], bgc = getStripControlBGColor(node, 5))
    
    cmds.floatSliderGrp('stripShoveSlider', edit = True, value = values[16], bgc = getStripControlBGColor(node, 16))
    
    cmds.gradientControlNoAttr('stripCurvatureGraph', edit = True, asString = values[8])
    cmds.text('stripCurvatureText', edit = True, bgc = getStripControlBGColor(node, 8))
    
    cmds.text('stripRootTxt', edit = True, bgc = getStripControlBGColor(node, 10))
    cmds.gradientControlNoAttr('stripRootGraph', edit = True, asString = values[10]) 

    cmds.text('stripCurvatureHeightText', edit = True, bgc = getStripControlBGColor(node, 15))
    cmds.floatSlider('stripCurvatureHeightSlider', edit = True, bgc = getStripControlBGColor(node, 15))
    cmds.floatSlider('stripCurvatureHeightSlider', edit = True, bgc = getStripControlBGColor(node, 15))
    cmds.floatField('stripCurvatureHeightField', edit = True, v = values[15])

    cmds.text('stripTipTxt', edit = True, bgc = getStripControlBGColor(node, 11))
    cmds.gradientControlNoAttr('stripTipGraph', edit = True, asString = values[11]) 
    
    cmds.floatSliderGrp('stripCurvatureBiasSlider', edit = True, value = values[12], bgc = getStripControlBGColor(node, 12))
    cmds.floatSliderGrp('stripCurvatureFalloffSlider', edit = True, value = values[14], bgc = getStripControlBGColor(node, 14))    
    
    
    updateAddRemoveStripsUI()
#    currMSNode = cmds.getAttr('meshGenGBNode.currentMeshStripNode')
#    maxDiv = cmds.getAttr(currMSNode + '.stripMaxDiv')
#    cmds.floatSliderGrp('stripDivOptimizeGrp', edit = True, v = maxDiv)
    
    

def updateAddRemoveStripsUI():
    
    currMSNode = cmds.getAttr('meshGenGBNode.currentMeshStripNode')
    if cmds.attributeQuery('connectedGBNode', node = currMSNode, exists = True):
        value = False
    else:
        value = True
    
    cmds.button('addStripsBtn', edit = True, vis = value)
    cmds.button('removeStripsBtn', edit = True, vis = value)
    
    

def loadStripControlsFROMATTRIBUTES(node):
    
    from operator import itemgetter
    
#    node = 'polyExtrudeEdge7'
    taper = cmds.getAttr(node + '.taper')
    cmds.floatSliderGrp('stripTaperSlider', edit = True, value = taper)
    taperGraph = cmds.getAttr(node + '.taperCurve[*]')
#    print taperGraph, node
    sorted(taperGraph,key=itemgetter(0))
    
    st = []
    for t in taperGraph:
        st.append(t[1])
        st.append(t[0])
#        st.append(t[2])
        st.append(2)

       
#    [(0.0, 0.5, 1.0), (0.56521737575531006, 0.36000001430511475, 1.0)]
#    (0.0, 1.0, 1.0), (0.29565218091011047, 0.0, 1.0)

    cmds.gradientControlNoAttr('stripTaperGraph', edit = True, asString = str(st)[1:-1])
#    cmds.gradientControlNoAttr('stripTaperGraph', edit = True, asString = '0.0, 1.0, 1.0,0.29565218091011047, 0.0, 1.0')
#    cmds.gradientControlNoAttr('stripTaperGraph', q = True, asString = True)
    twist = cmds.getAttr(node + '.twist')
    cmds.floatSliderGrp('stripTwistSlider', edit = True, value = twist)

def stripTaperChangeUI(bothNodes = [], taper = False):
    
    if not bothNodes:
        taper = cmds.floatSliderGrp('stripTaperSlider', q = True, value = True)
        bothNodes = getAffectedStripNodes(1)
        
    storeRestoreStripVtxPos(bothNodes, 'restore')    
    stripTaperChange(bothNodes, taper)
      
    storeRestoreStripVtxPos(bothNodes, 'store')
         
    stripCurvatureChangeUI(bothNodes)

    storeRestoreRootVtxForStripShove(bothNodes, 'store')
    stripShoveChange(bothNodes,'dict')     
    

def stripTaperChange(bothNodes = [], taper = False):
    
    if not bothNodes:
        taper = cmds.floatSliderGrp('stripTaperSlider', q = True, value = True)
        bothNodes = getAffectedStripNodes(1)

    extNodes = bothNodes[0]
    meshStripDictAdd(bothNodes[1], 1, taper)
    
   
    for node in extNodes:
        cmds.setAttr(node + '.scale', taper)
        

def stripTwistChangeUI(bothNodes = [], twist = False):
    
    if not bothNodes:
        twist = cmds.floatSliderGrp('stripTwistSlider', q = True, value = True)
        bothNodes = getAffectedStripNodes(4)
    
    storeRestoreStripVtxPos(bothNodes, 'restore')
    stripTwistChange(bothNodes, twist)
    
    storeRestoreStripVtxPos(bothNodes, 'store')
    stripCurvatureChangeUI(bothNodes)
    
    storeRestoreRootVtxForStripShove(bothNodes, 'store')
    stripShoveChange(bothNodes,'dict')
    

def stripTwistChange(bothNodes = [], twist = False):
    
    if not bothNodes:
        twist = cmds.floatSliderGrp('stripTwistSlider', q = True, value = True)
        bothNodes = getAffectedStripNodes(4)

    extNodes = bothNodes[0]     
    crvNodes = bothNodes[1]
    twistScaleList = []
    stripDict = getStripValuesDict()
    
    globe = False
    
    if 'globalPolyExtrude' in crvNodes:
        globe = True
        crvNodes.remove('globalPolyExtrude')
        
    for crv,ext in zip(crvNodes, extNodes):
        sc = stripDict[crv][5]
        cmds.setAttr(ext + '.rotation', twist * sc)
        
    if globe:
        crvNodes.append('globalPolyExtrude')
            
    meshStripDictAdd(crvNodes, 4, twist)        


def stripTwistScaleChangeUI(bothNodes = [], twistScale = False):
    
    if not bothNodes:
        twistScale = cmds.floatSliderGrp('stripTwistScaleSlider', q = True, value = True)
        bothNodes = getAffectedStripNodes(5)
    
    storeRestoreStripVtxPos(bothNodes, 'restore')
    stripTwistScaleChange(bothNodes, twistScale)
    
    
    storeRestoreStripVtxPos(bothNodes, 'store')
    stripCurvatureChangeUI(bothNodes)
    
    storeRestoreRootVtxForStripShove(bothNodes, 'store')
    stripShoveChange(bothNodes,'dict')  


def stripTwistScaleChange(bothNodes = [], twistScale = False):
    
    if not bothNodes:
        twistScale = cmds.floatSliderGrp('stripTwistScaleSlider', q = True, value = True)
        bothNodes = getAffectedStripNodes(5)

    extNodes = bothNodes[0]     
    crvNodes = bothNodes[1]
    stripDict = getStripValuesDict()

    globe = False    

    if 'globalPolyExtrude' in crvNodes:
        globe = True
        crvNodes.remove('globalPolyExtrude')
        
    for crv,ext in zip(crvNodes, extNodes):
        twist = stripDict[crv][4]
        cmds.setAttr(ext + '.rotation', twist * twistScale)  
    
    if globe:
        crvNodes.append('globalPolyExtrude')
    meshStripDictAdd(crvNodes, 5, twistScale)         
        

def stripShoveChangeUI(bothNodes = [], shove = False):
    
    sel = cmds.ls(sl = True)
    
    if not bothNodes:
        shove = cmds.floatSliderGrp('stripShoveSlider', q = True, v = True)
        bothNodes = getAffectedStripNodes(16)
    
    meshStripDictAdd(bothNodes[1], 16, shove) 
           
    storeRestoreRootVtxForStripShove(bothNodes, 'restore')
    stripShoveChange(bothNodes, 'dict')
    
    if sel:
        cmds.select(sel, r = True)
    else:
        cmds.select(cl = True)   
    

def stripShoveChange(bothNodes = [], shove = False):
    
    sel = cmds.ls(sl = True)
    shove = True
    
    if not bothNodes:
#        print 'no bothnodes for shove'
        bothNodes = getAffectedStripNodes(16)
    
    extNodes = bothNodes[0]
    crvNodes = bothNodes[1]
    
    currMSNode = cmds.getAttr('meshGenGBNode.currentMeshStripNode')
    ipScalp = cmds.getAttr(currMSNode + '.inputScalp')
    charCPNode = createCPNode(ipScalp)
    stpList = []
    stripDict = getStripValuesDict()    
    
    for crv,ext in zip(crvNodes, extNodes):
        rootPos = stripDict[crv][17]
        stp = getStpNameFromExt(ext)
        stpList.append(stp)
        rootVList = getRootVertexForStripShove(stp)
        
        for x in range(len(rootPos)):
            rootX = rootPos[x]
            cmds.setAttr(charCPNode + '.ip', rootX[0], rootX[1], rootX[2])
            newBasePos = list(cmds.getAttr(charCPNode + '.p')[0])
            cmds.xform(stp + '.vtx[' + str(rootVList[x]) + ']', ws = True, t = newBasePos)
    
    cmds.delete(charCPNode)
    
    if sel:
        cmds.select(sel, r = True)
    else:
        cmds.select(cl = True)        
    
    startGBUndo() 
    
    

        
def stripShoveChangeCPM(bothNodes = [], shove = False):       

    
    sel = cmds.ls(sl = True)
    
    if not bothNodes:
#        print 'no bothnodes for shove'
        shove = cmds.floatSliderGrp('stripShoveSlider', q = True, v = True)
        bothNodes = getAffectedStripNodes(16)
        
    extNodes = bothNodes[0]
    crvNodes = bothNodes[1]
    
#    print 'shoving for ', len(crvNodes), crvNodes
    currMSNode = cmds.getAttr('meshGenGBNode.currentMeshStripNode')
    ipScalp = cmds.getAttr(currMSNode + '.inputScalp')
    shoveMesh = ipScalp + '_shoveMesh'
    charCPNode = createCPNode(ipScalp)
    shoveCPNode = createCPNode(shoveMesh)
    stpList = []
    stripDict = getStripValuesDict()    
    
        
    for crv,ext in zip(crvNodes, extNodes):
        shove = stripDict[crv][16]
        rootPos = stripDict[crv][17]
        offsetDistPer = shove

        offsetDist = getStripWidthFromScale(offsetDistPer)

#        tangent = cmds.pointOnCurve(crv, t = True)
        tangent = cmds.pointOnCurve(crv, nt = True)
        stp = getStpNameFromExt(ext)
        stpList.append(stp)
        rootVList = getRootVertexForStripShove(stp)
        
        skip = False
        if shove == 0.0:
            for x in range(len(rootPos)):
                cmds.xform(stp + '.vtx[' + str(rootVList[x]) + ']', ws = True, t = rootPos[x])  
            skip = True                
        
        if skip:
            continue
        
        origDist = []
        newDist = []
        newBasePosList = []
        diffList = 0
#        print rootVList, crv
        for x in range(len(rootPos)):
            rootX = rootPos[x]
            newBasePos = [a + b for a,b in zip(rootX,[offsetDist * t * -1.0 for t in tangent])]
            newBasePosList.append(newBasePos)
            origDist = findClosestPointDistance(charCPNode, rootX)
            newDist = findClosestPointDistance(charCPNode, newBasePos)
            if newDist >= origDist:
                diffList = diffList + 1
            else:
                diffList = diffList - 1
#            print diffList, stp                
        
        if diffList > 0:
            for x in range(len(rootPos)):
                cmds.xform(stp + '.vtx[' + str(rootVList[x]) + ']', ws = True, t = newBasePosList[x])  
                
        else:
            for x in range(len(rootPos)):
                rootX = rootPos[x]
#                print newBasePosList[x]
                cmds.setAttr(shoveCPNode + '.ip', newBasePosList[x][0], newBasePosList[x][1], newBasePosList[x][2])
                cmds.xform(stp + '.vtx[' + str(rootVList[x]) + ']', ws = True, t = list(cmds.getAttr(shoveCPNode + '.p')[0]))
                
    
    
    cmds.delete(charCPNode)
    cmds.delete(shoveCPNode)
    
    if sel:
        cmds.select(sel, r = True)
    else:
        cmds.select(cl = True)        
    
    startGBUndo()
#    gbTyp = getGBType()
#    if gbTyp == 0:
#       postStripExtrudeForDemo(stpList)
                                        

def postStripExtrudeForDemo(stpList):
    
    for stp in stpList:
        extFacNode = cmds.polyExtrudeFacet(stp + '.f[*]', keepFacesTogether = True)
        cmds.setAttr(extFacNode + '.localTranslateZ', 0.5)
        cmds.delete(stp, ch = True)
        


def findClosestPointDistance(cpNode, pos):
    
    cmds.setAttr(cpNode + '.ip', pos[0], pos[1], pos[2])
    cPos = list(cmds.getAttr(cpNode + '.p')[0])    
    return distance3d(pos,cPos)
    
            
def createStripScalpShoveMeshMain():
    
    if not cmds.objExists('meshGenGBNode'):
        return
    
    currMSNode = cmds.getAttr('meshGenGBNode.currentMeshStripNode')
    if not currMSNode:
        return
        
    ipScalp = cmds.getAttr(currMSNode + '.inputScalp')
    if not ipScalp:
        return
    
    createStripScalpShoveMesh(3.0)
    

def createStripScalpShoveMesh(depth):
    
    currMSNode = cmds.getAttr('meshGenGBNode.currentMeshStripNode')
    scalpMesh = cmds.getAttr(currMSNode + '.inputScalp')
    
    shoveMesh = scalpMesh + '_shoveMesh'
    if cmds.objExists(shoveMesh):
        cmds.delete(shoveMesh)
    
    cmds.duplicate(scalpMesh, rr = True, rc = True, name = shoveMesh)
        
    cmds.setAttr(shoveMesh + '.visibility', False)
    
              
    disp = volumePercentByDistance(depth,scalpMesh)
#    print 'dispppp', disp
    whichMode = ''
    tempDup = cmds.duplicate(scalpMesh, name = 'tempDup', rr = True)[0]
    cmds.select(tempDup, r = True)
#    bbox1 = cmds.exactWorldBoundingBox(tempDup) 
#    bbY1 = bbox1[4]
    tempDupShape = cmds.listRelatives(tempDup, s = True)[0]
    
    bbY1 = cmds.getAttr(tempDupShape + '.boundingBoxMaxZ')
#    bbY1min = bbox1[1]
    mm.eval('artPuttyToolScript 3;')
    mm.eval('resetTool artPuttyContext;')
    cmds.artPuttyCtx('artPuttyContext', e = True, mtm = 'pull', sao = 'additive')
    mm.eval('artPuttyCtx -e -maxdisp ' + str(disp) + '`currentCtx`;')
    mm.eval('artPuttyCtx -e -clear `currentCtx`;')
    cmds.setToolTo('selectSuperContext')
#    bbox2 = cmds.exactWorldBoundingBox(tempDup) 
#    bbY2 = bbox2[4]
    bbY2 = cmds.getAttr(tempDupShape + '.boundingBoxMaxZ')
#    bbY2min = bbox2[1]
#    print bbox2
#    print bbox1
#    print bbY2
#    print bbY1
#    print bbY2, bbY1

    if bbY2 < bbY1:
        whichMode = 'pull'
    else:
        whichMode = 'push'
    cmds.delete(tempDup)
        
    cmds.select(shoveMesh, r = True)
    mm.eval('artPuttyToolScript 3;')
    mm.eval('resetTool artPuttyContext;')
    cmds.artPuttyCtx('artPuttyContext', e = True, sao = 'additive', mtm = whichMode)
    mm.eval('artPuttyCtx -e -maxdisp ' + str(disp) + '`currentCtx`;')
    mm.eval('artPuttyCtx -e -clear `currentCtx`;')
    cmds.setToolTo('selectSuperContext')
#    if cmds.button('editBaseMeshBtn', q = True, vis = True):
    cmds.setAttr(shoveMesh + '.visibility', False)
    
    groupNodes = createMeshStripSubGroup()
    cmds.parent(shoveMesh, groupNodes[1])
    cmds.select(cl = True)
    
    
def stripTaperGraphChangeUI(bothNodes = [], gradientGraph = False):
    
#    print bothNodes, gradientGraph
    if not bothNodes:
        gradientGraph = cmds.gradientControlNoAttr('stripTaperGraph', q = True, asString = True)
        bothNodes = getAffectedStripNodes(2)
    
    storeRestoreStripVtxPos(bothNodes, 'restore')    
    stripTaperGraphChange(bothNodes, gradientGraph)
    
    storeRestoreStripVtxPos(bothNodes, 'store')
    stripCurvatureChangeUI(bothNodes)  
    
    storeRestoreRootVtxForStripShove(bothNodes, 'store')
    stripShoveChange(bothNodes,'dict')       


def stripTaperGraphChange(bothNodes = [], gradientGraph = False):
    
    return
#    print bothNodes, gradientGraph
    if not bothNodes:
        gradientGraph = cmds.gradientControlNoAttr('stripTaperGraph', q = True, asString = True)
        bothNodes = getAffectedStripNodes(2)
    
    gradientGraphSplit = gradientGraph.split(',')
    extNodes = bothNodes[0]
#    node = extNodes[0]    
    for node in extNodes:
#        cmds.removeMultiInstance(node + '.taperCurve[1]'), b = True)
        if cmds.objExists(node + '.taperCurve[*]'):
            currP = len(cmds.getAttr(node + '.taperCurve[*]'))
            for x in range(1, 24):
#                print x
                cmds.removeMultiInstance(node + '.taperCurve[' + str(x) + ']' )
 
#            if currP > len(gradientGraphSplit)/3:
#                for x in range(currP, (len(gradientGraphSplit)/3)+1):
#                    cmds.removeMultiInstance( node + '.taperCurve[' + str(x) + ']' )
                    

        for x in range(len(gradientGraphSplit)/3):
            cmds.setAttr(node + '.taperCurve[' + str(x) + '].taperCurve_FloatValue', float(gradientGraphSplit[x*3]))
            cmds.setAttr(node + '.taperCurve[' + str(x) + '].taperCurve_Position', float(gradientGraphSplit[x*3+1]))
            cmds.setAttr(node + '.taperCurve[' + str(x) + '].taperCurve_Interp', float(gradientGraphSplit[x*3+2]))
    
    meshStripDictAdd(bothNodes[1], 2, gradientGraph)            
            
        
def getAffectedStripNodes(index = False):
    
    import cPickle as Pickle
    
    sel = cmds.ls(sl = True)
    
    currMSNode = cmds.getAttr('meshGenGBNode.currentMeshStripNode')
    
#    allNodes = getStripIPNodes()
#    stripIPExtrudes = allNodes[0]
#    stripIPCurves = allNodes[1]

    stripIPCurves = getStripIPNodes(False, 'crv')

    overrideStripCurves = []
    overrideStripCurvesString = cmds.getAttr(currMSNode + '.overrideStripCurves')
    
    if overrideStripCurvesString:
        overrideStripCurves = Pickle.loads(str(overrideStripCurvesString))
    
    if not overrideStripCurves:
        overrideStripCurves = getDefaultOverrideList()
    
    currOverrideStripCurves = overrideStripCurves[index]        

    selStrips = []
    selStripsCurves = []
    if sel:
        for s in sel:
            allStripNodes = getExtCrvFromStripMesh(s)
            if allStripNodes[0]:
                ext = allStripNodes[0]
                crv = allStripNodes[1][0]
                selStrips.append(s)
                selStripsCurves.append(crv)

    if selStripsCurves:
        currOverrideStripCurves = list(set(currOverrideStripCurves + selStripsCurves))
        extNodes = getStripExtrudeNodes(selStripsCurves)
        bothNodes = [extNodes, selStripsCurves]
    else:
        currGlobalCurves = list(set(stripIPCurves) - set(currOverrideStripCurves))
        currGlobalCurves.append('globalPolyExtrude')
        extNodes = getStripExtrudeNodes(currGlobalCurves)
        bothNodes = [extNodes, currGlobalCurves]
    
    overrideStripCurves[index] = currOverrideStripCurves
    overrideStripCurvesString = Pickle.dumps(overrideStripCurves)
    cmds.setAttr(currMSNode + '.overrideStripCurves', str(overrideStripCurvesString), type = 'string')
    
    if sel:
        cmds.select(sel, r = True)
    
    return bothNodes


def getDefaultOverrideList():
    
    defaultDict = getDefaultStripDict()
    overrideList = []
    for x in range(len(defaultDict)):
        overrideList.append([])
    
    return overrideList
    
        

def getStripExtrudeNodes(stripCurves):

    extNodes = []                    
    for each in stripCurves:
        if 'globalPolyExtrude' in each:
            continue
        shp = cmds.listRelatives(each, s = True)[0]
        conn = cmds.listConnections(shp, type = 'extrude')
        if conn and '_stripNodeE' in conn[0]:
            extNodes.append(conn[0])
        else:
            continue                

    return extNodes     
  
def resetStripOverride():
    
    import cPickle as Pickle
    currMSNode = cmds.getAttr('meshGenGBNode.currentMeshStripNode')
    overrideStripCurves = []
    overrideStripCurvesString = cmds.getAttr(currMSNode + '.overrideStripCurves')
    if overrideStripCurvesString:
        overrideStripCurves = Pickle.loads(str(overrideStripCurvesString))
    
    nodes = getAffectedStripNodes()
    extNodes = nodes[0]
    crvNodes = nodes[1]
    allReset = False
    if nodes:
        if 'globalPolyExtrude' in crvNodes:
            option = cmds.confirmDialog( title='Reset All Overrides', message='Manual Overrides for all Curves will be reset. Do You want to conitnue?', button=['Yes','No'], defaultButton='No', cancelButton='No', dismissString='No' )
            if option == 'No':
                allReset = False
                return
            else:
                allReset = True
                
    if allReset:
        totalOverrideStripCurves = []
        if overrideStripCurves:
            for each in overrideStripCurves:
                totalOverrideStripCurves.extend(each)
                    
        totalOverrideStripCurves = list(set(totalOverrideStripCurves))
                                             
        extNodes = getStripExtrudeNodes(totalOverrideStripCurves)
        nodes = [extNodes,totalOverrideStripCurves]
        overrideStripCurves = getDefaultOverrideList()
    else:                    
        for x in range(len(overrideStripCurves)):
            if overrideStripCurves[x]:
                for each in crvNodes:
                    if each in overrideStripCurves[x]:
                        overrideStripCurves[x].remove(each)
                        
#        overrideStripCurves = list(set(overrideStripCurves) - set(crvNodes))
    
    resetBackToGlobalStrip(nodes)
    
    overrideStripCurvesString = Pickle.dumps(overrideStripCurves)
    cmds.setAttr(currMSNode + '.overrideStripCurves', str(overrideStripCurvesString), type = 'string')

            
def resetBackToGlobalStrip(nodes):
    
    dict = getDefaultStripDict()

#    nodes = getAffectedStripNodes()
    
    loadGlobalStripControls()
    
    storeRestoreStripVtxPos(nodes,'restore')   
    
    stripTaperChange(nodes, dict[1])
    stripTwistChange(nodes, dict[4])
    stripTwistScaleChange(nodes, dict[5])
    stripTaperGraphChange(nodes, dict[2])

    stripRotateChange(nodes, dict[3])
    
    stripRotateXChange(nodes, dict[18])
    stripRotateYChange(nodes, dict[19])
    stripRotateZChange(nodes, dict[20])
    
    
    crvNodes = nodes[1]
    stripProperties = getGBStripProperties()

    divList = getDivForStrip(crvNodes, stripProperties)
    stripDivChange(nodes, divList)
    
    widthList = getWidthForStrip(crvNodes, stripProperties)
    stripWidthChange(nodes, widthList)
    

    meshStripDictAdd(crvNodes, 10, dict[10])
    meshStripDictAdd(crvNodes, 11, dict[11])
    meshStripDictAdd(crvNodes, 12, dict[12])
    meshStripDictAdd(crvNodes, 14, dict[14])
    meshStripDictAdd(crvNodes, 15, dict[15])
    meshStripDictAdd(crvNodes, 16, dict[16])
    
    
    storeRestoreStripVtxPos(nodes,'store')    
    stripCurvatureChangeUI(nodes)
    
    storeRestoreRootVtxForStripShove(nodes, 'store')
    stripShoveChange(nodes, 'dict')  
    
    fixStripUVs(nodes, [divList, widthList], stripProperties[0])
    
def getStripWidthFromScale(sc):
    
    currMSNode = cmds.getAttr('meshGenGBNode.currentMeshStripNode')
    ipScalp = cmds.getAttr(currMSNode + '.inputScalp')
    distance = volumePercentByDistance(sc, ipScalp)
    return distance

def getStripIPNodes(errorStop = False, mode = 'both'):
    
    import cPickle as Pickle
    
    currMSNode = cmds.getAttr('meshGenGBNode.currentMeshStripNode')
    currNode = ''
    if cmds.objExists(currMSNode + '.connectedGBNode'):
        currNode = cmds.getAttr(currMSNode + '.connectedGBNode')
    stripIPCurves = []
    if currNode:
        stripIPCurvesString = cmds.getAttr(currNode + '.manualCurves')
        if gbType == 0:
            if mode == 'gen':
                if stripIPCurvesString:
                    stripIPCurves = Pickle.loads(str(stripIPCurvesString))
            else:
                stripIPCurvesString = cmds.getAttr(currMSNode + '.stripIPCurves')
                if stripIPCurvesString:
                    stripIPCurves = Pickle.loads(str(stripIPCurvesString))

                                    

            

            
#            if stripIPCurves:
#                stripMax = getStripMaxCount()
#                stripIPCurves = stripIPCurves[0:stripMax]
#                stripIPCurvesString = Pickle.dumps(stripIPCurves)
        else:
            if stripIPCurvesString:
                stripIPCurves = Pickle.loads(str(stripIPCurvesString))            
           
        if not stripIPCurves:
            if errorStop:
                reportGBMeshStripMessage('No Freeform Curves Exist in Groomboy Setup', True, True, 'red')     

    else:
        stripIPCurvesString = cmds.getAttr(currMSNode + '.stripIPCurves')
        if stripIPCurvesString:
            stripIPCurves = Pickle.loads(str(stripIPCurvesString)) 
            
        if not stripIPCurves:
            if errorStop:
                reportGBMeshStripMessage('No Curves are added in current setup', True, True, 'red')     
    
    extNodes = []

    if stripIPCurves:
        extNodes = getStripExtrudeNodes(stripIPCurves)

    if mode == 'crv' or mode == 'gen':
        return stripIPCurves
    
    else:
        return [extNodes, stripIPCurves]                        
        
    
def getGBStripProperties(mode = 'update'):
    
    import cPickle as Pickle
    currMSNode = cmds.getAttr('meshGenGBNode.currentMeshStripNode')
    stripPropertiesString = cmds.getAttr(currMSNode + '.stripProperties')
    stripProperties = []
    if stripPropertiesString:
        stripProperties = Pickle.loads(str(stripPropertiesString))
    
#    if stripProperties:
#        return stripProperties        
    
#    allNodes =  getStripIPNodes()   
#    stripIPExtrudes = allNodes[0]
#    stripIPCurves = allNodes[1]
    
    stripIPCurves = getStripIPNodes(False, 'crv')
    
    oldAvg = 0
    oldMax = 0
    
    if stripProperties:
        oldAvg = stripProperties[0]
        oldMax = stripProperties[1]
            
    stripProperties = []
    stripLength = []
    
    finalIPCurves = []
    finalIPCurves.extend(stripIPCurves)
    
#    if crvList:
#        for crv in crvList:
#            finalIPCurves.remove(crv)
        
    for crv in finalIPCurves:
        stripLength.append(cmds.arclen(crv))

    if stripLength:
        avg = sum(stripLength)/len(stripLength)
        newSL = list(stripLength)
#        print newSL, stripLength
        maxL = max(newSL)
        
    else:
        avg = 10.0
        maxL = 10.0

    stripProperties = [avg,maxL]
    
    stripPropertiesString = Pickle.dumps(stripProperties)
    cmds.setAttr(currMSNode + '.stripProperties', str(stripPropertiesString), type = 'string')
    
    if mode == 'only':
        return stripProperties
        
    if not oldMax == maxL:
        sel = cmds.ls(sl = True)
        if sel:
            adpUI = storeAdpUIStripControls()
        cmds.select(cl = True)
        loadGlobalStripControls()
#        print 'selection gone', sel
        bothNodes = getAffectedStripNodes(6)
        crvNodes = bothNodes[1]
        divList = getDivForStrip(crvNodes, stripProperties)
        
        storeRestoreStripVtxPos(bothNodes,'restore')

        stripDivChange(bothNodes, divList)
        
        
        bothNodes = getAffectedStripNodes(0)
        crvNodes = bothNodes[1]
        widthList = getWidthForStrip(crvNodes, stripProperties)
        stripWidthChange(bothNodes, widthList)
        
        storeRestoreStripVtxPos(bothNodes,'store')    
        stripCurvatureChangeUI(bothNodes)
        
        storeRestoreRootVtxForStripShove(bothNodes, 'store')
        stripShoveChange(bothNodes, 'dict')         
        
        fixStripUVs(bothNodes, [divList, widthList], avg)
        
        if sel:
#            print 'selection back', sel
            cmds.select(sel, r = True)
            restoreAdpUIStripControls(adpUI)
            stripLiveUIUpdate()
            
        
#        widthList = getAffectedStripNodes(0)
        
        
    return stripProperties


def restoreAdpUIStripControls(adpUI):
    
    return
    
def storeAdpUIStripControls():
    return ''

def stripDivChangeUI():
    
    
    currMSNode = cmds.getAttr('meshGenGBNode.currentMeshStripNode')
    adp = False    
    if cmds.checkBox('stripDivAdaptiveCB', q = True, v = True) and cmds.checkBox('stripDivAdaptiveCB', q = True, vis = True):
        adp = True

    if adp:
        cmds.rowLayout('stripAdaptiveDivRL', edit = True, vis = True)
    else:
        cmds.rowLayout('stripAdaptiveDivRL', edit = True, vis = False)        

    bothNodes = getAffectedStripNodes(6)    
    if bothNodes:
        if not 'globalPolyExtrude' in bothNodes[1]:    
            cmds.setAttr(currMSNode + '.divAdaptive', cmds.checkBox('stripDivAdaptiveCB', q = True, v = True))   
                    
        

    crvNodes = bothNodes[1]
    
    prop = getGBStripProperties('only')
    
    
    divList = getDivForStrip(crvNodes, prop)
    
    storeRestoreStripVtxPos(bothNodes,'restore')
#    print 'div change', bothNodes
    stripDivChange(bothNodes, divList)
    
#    stripDict = getStripValuesDict()
#   curvatureList = [stripDict[crv][8] for crv in crvNodes]
#    stripCurvatureChange(bothNodes, curvatureList)
 
    storeRestoreStripVtxPos(bothNodes,'store')    

    stripCurvatureChangeUI(bothNodes)
    
    storeRestoreRootVtxForStripShove(bothNodes, 'store')
    stripShoveChange(bothNodes, 'dict') 
    fixStripUVs(bothNodes, [divList, []], prop[0])
    
    getGBStripProperties()
    
    
def stripDivChange(bothNodes = [], divList = []):
    
        
    import cPickle as Pickle
#    print 'bothnodes in change', bothNodes
    currMSNode = cmds.getAttr('meshGenGBNode.currentMeshStripNode') 

#        custDiv = cmds.intSliderGrp('stripDivSlider', q = True, v = True)
#        divList = [custDiv] * len(bothNodes[0])
        
    extNodes = bothNodes[0]
    crvNodes = bothNodes[1]
    
    stripDict = getStripValuesDict()
    if 'globalPolyExtrude' in crvNodes:

        stripDict['globalPolyExtrude'][6] = cmds.intSliderGrp('stripDivSlider', q = True, v = True)
        globe = True
        crvNodes.remove('globalPolyExtrude')

#    meshStripDictAdd(crvNodes, 6, custDiv)        

    count = 0 

    for crv,ext in zip(crvNodes, extNodes):
#        print 'for strip change div', crv
        currDiv = divList[count]
        stripDict[crv][6] = currDiv
        nt = cmds.listConnections(ext, type = 'nurbsTessellate')[0]
        cmds.setAttr(nt + '.vNumber', currDiv+1)  

        count = count + 1
        
    stripDictString = Pickle.dumps(stripDict)
    cmds.setAttr(currMSNode + '.stripValuesDict', str(stripDictString), type = 'string')




def getDivForStrip(stripList, prop):
    

    currMSNode = cmds.getAttr('meshGenGBNode.currentMeshStripNode') 
    
    stripAvgLength = prop[0]
    stripMaxLength = prop[1]
    
    widthList = []
    
    maxWidth = cmds.intSliderGrp('stripDivSlider', q = True, v = True)

    adp = False
    if cmds.checkBox('stripDivAdaptiveCB', q = True, vis = True):
        adp = cmds.checkBox('stripDivAdaptiveCB', q = True, v = True)
    
    if adp:
        cmds.setAttr(currMSNode + '.divAdaptive', True)
        adpBlend = cmds.floatSliderGrp('stripAdpDivSlider', q = True, v = True)
        cmds.setAttr(currMSNode + '.divAdpBlend', adpBlend)
    else:
        if 'globalPolyExtrude' in stripList:
            cmds.setAttr(currMSNode + '.divAdaptive', False)
            
    for strip in stripList:
        if strip == 'globalPolyExtrude':
            continue
            
        if not adp:
            widthList.append(maxWidth)
        else:            
            stripLength = cmds.arclen(strip)
            adpWidth = (maxWidth * stripLength) / stripMaxLength
            a = maxWidth
            b = adpWidth
            x = adpBlend
            finalWidth = a + ((b - a) * x)
            if finalWidth <= 1.0:
                finalWidth = 1
            widthList.append(int(finalWidth))

#    print widthList
    return widthList



        
def OLDgetDivForStripOLD(stripList, prop):
    
    stripAvgLength = prop[0]
    stripMaxLength = prop[1]
    
    currMSNode = cmds.getAttr('meshGenGBNode.currentMeshStripNode')
    
    divList = []
    maxDiv = cmds.intSliderGrp('stripDivSlider', q = True, v = True)

    adp = cmds.checkBox('stripDivAdaptiveCB', q = True, v = True)
    for strip in stripList:
        if strip == 'globalPolyExtrude':
            continue
            
        if not adp:
            divList.append(maxDiv)
            cmds.setAttr(currMSNode + '.divAdaptive', False)
        else:            
            cmds.setAttr(currMSNode + '.divAdaptive', True)
            stripLength = cmds.arclen(strip)
            divisions = int((maxDiv * stripLength) / stripMaxLength)
            if divisions <= 1:
                divisions = 1
            divList.append(divisions)
    
    return divList
    
def stripWidthChangeUI():

    currMSNode = cmds.getAttr('meshGenGBNode.currentMeshStripNode')
    adp = False    
    if cmds.checkBox('stripWidthAdaptiveCB', q = True, v = True) and cmds.checkBox('stripWidthAdaptiveCB', q = True, vis = True):
        adp = True

    if adp:
        cmds.rowLayout('stripAdaptiveWidthRL', edit = True, vis = True)
    else:
        cmds.rowLayout('stripAdaptiveWidthRL', edit = True, vis = False)        
    
    bothNodes = getAffectedStripNodes(0)
    crvNodes = bothNodes[1]
    
    if 'globalPolyExtrude' in crvNodes:
        cmds.setAttr(currMSNode + '.widthAdaptive', adp)        
#    cmds.setAttr(currMSNode + '.widthAdpBlend', adpBlend)    
    
    
    prop = getGBStripProperties('only')
    widthList = getWidthForStrip(crvNodes, prop)
    
    storeRestoreStripVtxPos(bothNodes,'restore')
#    print bothNodes, 'from 19904'    
    stripWidthChange(bothNodes, widthList)     
    
    storeRestoreStripVtxPos(bothNodes,'store')    
    stripCurvatureChangeUI(bothNodes)
    
    storeRestoreRootVtxForStripShove(bothNodes, 'store')
    stripShoveChange(bothNodes, 'dict') 
    
    fixStripUVs(bothNodes, [[], widthList], prop[0])
    
    getGBStripProperties()

    
def stripWidthChange(bothNodes = [], widthList = []):
    
    import cPickle as Pickle
    currMSNode = cmds.getAttr('meshGenGBNode.currentMeshStripNode') 

#        custDiv = cmds.intSliderGrp('stripDivSlider', q = True, v = True)
#        divList = [custDiv] * len(bothNodes[0])
        
    extNodes = bothNodes[0]
    crvNodes = bothNodes[1]
    
    stripDict = getStripValuesDict()
    if 'globalPolyExtrude' in crvNodes:
        stripDict['globalPolyExtrude'][0] = cmds.floatSliderGrp('stripWidthSlider', q = True, v = True)
        globe = True
        crvNodes.remove('globalPolyExtrude')

#    meshStripDictAdd(crvNodes, 6, custDiv)        

    count = 0 
    for crv,ext in zip(crvNodes, extNodes):
        currWidth = widthList[count]
        stripDict[crv][0] = currWidth
        baseCrv = cmds.listConnections(ext + '.profile', type = 'nurbsCurve')
        cmds.scale(currWidth, currWidth, currWidth, baseCrv)
        count = count + 1
        
    stripDictString = Pickle.dumps(stripDict)
    cmds.setAttr(currMSNode + '.stripValuesDict', str(stripDictString), type = 'string')
    

def getStripRotateGrpCtrl(crv):
    
    return crv + '_stripCtrlGrp1'
    

def getStripWidthCtrl(crv,ext):
    
    extConn = cmds.listConnections(ext, type = 'cluster')[0]
    clustHandle = cmds.listConnections(extConn, type = 'clusterHandle')[0]
    grp = cmds.listRelatives(clustHandle, p = True)[0]
    expectedName = crv + '_GlobalRotate_Width_Ctrl'
    if expectedName in grp:
        return grp
        
def getWidthForStrip(stripList, prop):

    currMSNode = cmds.getAttr('meshGenGBNode.currentMeshStripNode') 
    
    stripAvgLength = prop[0]
    stripMaxLength = prop[1]
    
    widthList = []
    maxWidth = cmds.floatSliderGrp('stripWidthSlider', q = True, v = True)

    adp = False
    if cmds.checkBox('stripWidthAdaptiveCB', q = True, vis = True):
        adp = cmds.checkBox('stripWidthAdaptiveCB', q = True, v = True)
    
    if adp:
        cmds.setAttr(currMSNode + '.widthAdaptive', True)
        adpBlend = cmds.floatSliderGrp('stripAdpWidthSlider', q = True, v = True)
        cmds.setAttr(currMSNode + '.widthAdpBlend', adpBlend)
    else:
        if 'globalPolyExtrude' in stripList:
            cmds.setAttr(currMSNode + '.widthAdaptive', False)
            
    for strip in stripList:
        if strip == 'globalPolyExtrude':
            continue
            
        if not adp:
            widthList.append(maxWidth)
        else:            
            stripLength = cmds.arclen(strip)
            adpWidth = (maxWidth * stripLength) / stripMaxLength
            a = maxWidth
            b = adpWidth
            x = adpBlend
            finalWidth = a + ((b - a) * x)
            if finalWidth <= 0.01:
                finalWidth = 0.01
            widthList.append(finalWidth)

#    print widthList
    return widthList 

def getStripPolyMeshNodes(extNodes):
    
    for ext in extNodes:
        cmds.listConnections(ext, type = 'mesh')

        
#fixStripUVs(['polyExtrudeEdge65','bkp_gbChar_01_1_Demo_Face_curve66'],[[25],[1.0]],7.22)

def fixStripUVs(bothNodes , divWidthList, stripAvgLength):
    
    return 
    
    extNodes = bothNodes[0]
    crvNodes = bothNodes[1]
    divList = divWidthList[0]
    widthList = divWidthList[1]
    
    if cmds.objExists('uvGBTempPlane'):
        cmds.delete('uvGBTempPlane')
    
    sel = cmds.ls(sl = True)
    uvGBTempPlane = cmds.polyPlane(name = 'uvGBTempPlane', sx = 2, cuv = 2)
#    cmds.polyFlipUV(uvGBTempPlane[0], flipType = 1, local = True)
    
    
    if not divList:
        divList = [cmds.getAttr(ext + '.divisions') for ext in extNodes]
    
    if not widthList:
        widthList = [cmds.getAttr(getStripWidthCtrl(crv,ext) + '.scaleX') for crv,ext in zip(crvNodes,extNodes)]
    


#    print divList, widthList
    for x in range(len(extNodes)):
        polyPlaneNode = crvNodes[x] + '_stripNodeP'
        if not cmds.objExists(polyPlaneNode):
            continue
        segs = cmds.getAttr(polyPlaneNode + '.subdivisionsHeight')
        stpName = cmds.listConnections(extNodes[x], type = 'mesh')[0]
        cmds.setAttr(uvGBTempPlane[1] + '.subdivisionsWidth', segs)
        cmds.setAttr(uvGBTempPlane[1] + '.subdivisionsHeight', divList[x]+1)
        cmds.setAttr(uvGBTempPlane[1] + '.width', widthList[x])
        cmds.setAttr(uvGBTempPlane[1] + '.h', stripAvgLength)
#        cmds.setAttr(uvGBTempPlane[1] + '.h', cmds.arclen(crvNodes[x]))        
        
#        print stpName


        fList = range(segs)
        div = divList[x]
        
        for x in range(segs):
            minF = len(fList)
            for y in range(minF, div + minF):
                fList.append(y)
                
        gList = []        
        hList = []
        for x in range(segs):
            gList.extend(range(x, (div+1) * segs, segs))
        
        rList = range(segs)
        for r in rList:
            gList.remove(r)
            fList.remove(r)
            
#        print gList, fList, range(segs), crvNodes[x]
        
        for y in range(segs):
            cmds.polyClipboard(uvGBTempPlane[0] + '.f[' + str(y) + ']', uv = True, cp = True)
            cmds.polyClipboard(stpName + '.f[' + str(y) + ']', uv = True, ps = True)
            
        
        for y in range(len(gList)):
            cmds.polyClipboard(uvGBTempPlane[0] + '.f[' + str(gList[y]) + ']', uv = True, cp = True)
            cmds.polyClipboard(stpName + '.f[' + str(fList[y]) + ']', uv = True, ps = True)
        

    cmds.delete(uvGBTempPlane)
    if sel:
        cmds.select(sel, r = True)

def stripRotateChangeUI(bothNodes = [], rotAngle = False):
    
    return 
    
    if not bothNodes:
        rotAngle = cmds.floatSliderGrp('stripRotateSlider', q = True, value = True)
        bothNodes = getAffectedStripNodes(3)
        
    storeRestoreStripVtxPos(bothNodes,'restore')
    stripRotateChange(bothNodes, rotAngle)        
    storeRestoreStripVtxPos(bothNodes,'store')
    stripCurvatureChangeUI(bothNodes)    
    
    storeRestoreRootVtxForStripShove(bothNodes, 'store')
    stripShoveChange(bothNodes, 'dict')
    
    
def stripRotateXChangeUI(bothNodes = [], rotAngle = False):
    
    
    if not bothNodes:
        rotAngle = cmds.floatSliderGrp('stripRotateXSlider', q = True, value = True)
        bothNodes = getAffectedStripNodes(18)
        
    storeRestoreStripVtxPos(bothNodes,'restore')
    stripRotateXChange(bothNodes, rotAngle)        
    storeRestoreStripVtxPos(bothNodes,'store')
    stripCurvatureChangeUI(bothNodes)    
    
    storeRestoreRootVtxForStripShove(bothNodes, 'store')
    stripShoveChange(bothNodes, 'dict')

def stripRotateXChange(bothNodes = [], rotAngle = False):
    
    
    if not bothNodes:
        rotAngle = cmds.floatSliderGrp('stripRotateXSlider', q = True, value = True)
        bothNodes = getAffectedStripNodes(18)

    extNodes = bothNodes[0]
    crvNodes = bothNodes[1]
    
    meshStripDictAdd(bothNodes[1], 18, rotAngle)

    stripDict = getStripValuesDict()
    
    for crv,ext in zip(crvNodes, extNodes):
        globalHolder = getStripRotateGrpCtrl(crv)
#        print 'globalholder', globalHolder
#        dir = stripDict[crv][7]
        cmds.setAttr(globalHolder + '.rotateX', rotAngle)
        
        

def stripRotateYChangeUI(bothNodes = [], rotAngle = False):
    
    
    if not bothNodes:
        rotAngle = cmds.floatSliderGrp('stripRotateYSlider', q = True, value = True)
        bothNodes = getAffectedStripNodes(19)
        
    storeRestoreStripVtxPos(bothNodes,'restore')
    stripRotateYChange(bothNodes, rotAngle)        
    storeRestoreStripVtxPos(bothNodes,'store')
    stripCurvatureChangeUI(bothNodes)    
    
    storeRestoreRootVtxForStripShove(bothNodes, 'store')
    stripShoveChange(bothNodes, 'dict')

def stripRotateYChange(bothNodes = [], rotAngle = False):
    
    
    if not bothNodes:
        rotAngle = cmds.floatSliderGrp('stripRotateYSlider', q = True, value = True)
        bothNodes = getAffectedStripNodes(19)

    extNodes = bothNodes[0]
    crvNodes = bothNodes[1]
    
    meshStripDictAdd(bothNodes[1], 19, rotAngle)

    stripDict = getStripValuesDict()
    
    for crv,ext in zip(crvNodes, extNodes):
        globalHolder = getStripRotateGrpCtrl(crv)
#        print 'globalholder', globalHolder
#        dir = stripDict[crv][7]
        cmds.setAttr(globalHolder + '.rotateY', rotAngle)
        

def stripRotateZChangeUI(bothNodes = [], rotAngle = False):
    
    
    if not bothNodes:
        rotAngle = cmds.floatSliderGrp('stripRotateZSlider', q = True, value = True)
        bothNodes = getAffectedStripNodes(20)
        
    storeRestoreStripVtxPos(bothNodes,'restore')
    stripRotateZChange(bothNodes, rotAngle)        
    storeRestoreStripVtxPos(bothNodes,'store')
    stripCurvatureChangeUI(bothNodes)    
    
    storeRestoreRootVtxForStripShove(bothNodes, 'store')
    stripShoveChange(bothNodes, 'dict')

def stripRotateZChange(bothNodes = [], rotAngle = False):
    
    
    if not bothNodes:
        rotAngle = cmds.floatSliderGrp('stripRotateZSlider', q = True, value = True)
        bothNodes = getAffectedStripNodes(20)

    extNodes = bothNodes[0]
    crvNodes = bothNodes[1]
    
    meshStripDictAdd(bothNodes[1], 20, rotAngle)

    stripDict = getStripValuesDict()
    
    for crv,ext in zip(crvNodes, extNodes):
        globalHolder = getStripRotateGrpCtrl(crv)
#        print 'globalholder', globalHolder
#        dir = stripDict[crv][7]
        cmds.setAttr(globalHolder + '.rotateZ', rotAngle)        

        
        
        
        
    

def stripRotateChange(bothNodes = [], rotAngle = False):
    
    return 
    
    if not bothNodes:
        rotAngle = cmds.floatSliderGrp('stripRotateSlider', q = True, value = True)
        bothNodes = getAffectedStripNodes(3)

    extNodes = bothNodes[0]
    crvNodes = bothNodes[1]
    
    meshStripDictAdd(bothNodes[1], 3, rotAngle)

    stripDict = getStripValuesDict()
    
    for crv,ext in zip(crvNodes, extNodes):
        globalHolder = getStripWidthCtrl(crv,ext)
#        print 'globalholder', globalHolder
        dir = stripDict[crv][7]
        cmds.setAttr(globalHolder + '.rotateX', rotAngle * dir)
        
        
def convertSegmentsDictToNode(segments):
    
    if segments == 6:
        return 7
    else:
        return segments        


def stripSegmentsChangeUI():
    
#    print 'seg ui'
    bothNodes = getAffectedStripNodes(9)
    crvNodes = bothNodes[1]
    
    currMSNode = cmds.getAttr('meshGenGBNode.currentMeshStripNode')
    adp = False    
    if cmds.checkBox('stripSegmentsAdaptiveCB', q = True, v = True) and cmds.checkBox('stripSegmentsAdaptiveCB', q = True, vis = True):
        adp = True

    if adp:
        cmds.rowLayout('stripAdaptiveSegmentsRL', edit = True, vis = True)
    else:
        cmds.rowLayout('stripAdaptiveSegmentsRL', edit = True, vis = False)        
    
    if 'globalPolyExtrude' in crvNodes:
        cmds.setAttr(currMSNode + '.segAdaptive', cmds.checkBox('stripSegmentsAdaptiveCB', q = True, v = True)) 
    
    
    
    
    storeRestoreStripVtxPos(bothNodes,'restore')
    prop = getGBStripProperties('only')

    segList = getSegsForStrip(crvNodes, prop)
    
    stripSegmentsChange(bothNodes, segList)
    
    storeRestoreStripVtxPos(bothNodes,'store')
    stripCurvatureChangeUI(bothNodes)
    
    storeRestoreRootVtxForStripShove(bothNodes, 'store')
    stripShoveChange(bothNodes, 'dict')
    
    fixStripUVs(bothNodes, [[], []], prop[0])
    
    getGBStripProperties()


def getSegsForStrip(stripList, prop):
    

    currMSNode = cmds.getAttr('meshGenGBNode.currentMeshStripNode') 
    
    stripAvgLength = prop[0]
    stripMaxLength = prop[1]
    
    widthList = []
    maxWidth = cmds.intSliderGrp('stripSegmentsSlider', q = True, v = True)

    adp = False
    if cmds.checkBox('stripSegmentsAdaptiveCB', q = True, vis = True):
        adp = cmds.checkBox('stripSegmentsAdaptiveCB', q = True, v = True)
    
    if adp:
        cmds.setAttr(currMSNode + '.segAdaptive', True)
        adpBlend = cmds.floatSliderGrp('stripAdpSegmentsSlider', q = True, v = True)
        cmds.setAttr(currMSNode + '.segAdpBlend', adpBlend)
    else:
        if 'globalPolyExtrude' in stripList:
            cmds.setAttr(currMSNode + '.segAdaptive', False)

            
    for strip in stripList:
        if strip == 'globalPolyExtrude':
            continue
            
        if not adp:
            widthList.append(maxWidth)
        else:            
            stripLength = cmds.arclen(strip)
            adpWidth = (maxWidth * stripLength) / stripMaxLength
            a = maxWidth
            b = adpWidth
            x = adpBlend
            finalWidth = a + ((b - a) * x)
            if finalWidth <= 1.0:
                finalWidth = 1
            widthList.append(int(finalWidth))

#    print widthList
    return widthList
    
    
    
    
def OLDgetSegsForStripOLD(stripList, prop):    
    
    stripAvgLength = prop[0]
    stripMaxLength = prop[1]
    
    currMSNode = cmds.getAttr('meshGenGBNode.currentMeshStripNode')
    
    segList = []
    maxSegs = cmds.intSliderGrp('stripSegmentsSlider', q = True, v = True)

    adp = cmds.checkBox('stripSegmentsAdaptiveCB', q = True, v = True) and cmds.checkBox('stripSegmentsAdaptiveCB', q = True, vis = True)
    for strip in stripList:
        if strip == 'globalPolyExtrude':
            continue
            
        if not adp:
            segList.append(maxSegs)
            cmds.setAttr(currMSNode + '.segAdaptive', False)
        else:            
            cmds.setAttr(currMSNode + '.segAdaptive', True)
            stripLength = cmds.arclen(strip)
            segs = int((maxSegs * stripLength) / stripMaxLength)
            if segs <= 1:
                segs = 1
            segList.append(segs)
    
    return segList


def stripSegmentsChange(bothNodes = [], segList = []):
    
    import cPickle as Pickle
    currMSNode = cmds.getAttr('meshGenGBNode.currentMeshStripNode')
        
    extNodes = bothNodes[0]
    crvNodes = bothNodes[1]
    
    stripDict = getStripValuesDict()
    
    if 'globalPolyExtrude' in crvNodes:
        stripDict['globalPolyExtrude'][9] = cmds.intSliderGrp('stripSegmentsSlider', q = True, v = True)
        globe = True
        crvNodes.remove('globalPolyExtrude')
    
    count = 0 

    for crv,ext in zip(crvNodes,extNodes):
        nt = cmds.listConnections(ext, type = 'nurbsTessellate')[0]
        cmds.setAttr(nt + '.uNumber', segList[count] + 1)
        stripDict[crv][9] = segList[count]
        count = count + 1
        
    
    stripDictString = Pickle.dumps(stripDict)
    cmds.setAttr(currMSNode + '.stripValuesDict', str(stripDictString), type = 'string')
    

def updateMeshStripsForGBFFCUpdates(remManual, addManual):
    
    import cPickle as Pickle
    if not cmds.objExists('meshGenGBNode'):
        return
    
    currMSNode = cmds.getAttr('meshGenGBNode.currentMeshStripNode')
    if not currMSNode:
        return
    
    removeStripsList = []
    removeListString = cmds.getAttr(currMSNode + '.removeStripsList')
    if removeListString:
        removeList = Pickle.loads(str(removeListString))
    
    addStripsList = []
    addStripsListString = cmds.getAttr(currMSNode + '.addStripsList')
    if addStripsListString:
        addStripsList = Pickle.loads(str(addStripsListString))
        
    removeStripsList.extend(remManual)
    addStripsList.extend(addManual)
    
    removeStripsList = list(set(removeStripsList))
    addStripsList = list(set(addStripsList))       
    
#    removeStripsList = list(set(remManual) - set(removeStripsList))
#    addStripsList = list(set(addManual) - set(addStripsList))
    
#    print removeStripsList, addStripsList, '@@@@@@@@'
    
    if removeStripsList:
        removeStripsListString = Pickle.dumps(removeStripsList)
        cmds.setAttr(currMSNode + '.removeStripsList', str(removeStripsListString), type = 'string')

    if addStripsList:
        addStripsListString = Pickle.dumps(addStripsList)
        cmds.setAttr(currMSNode + '.addStripsList', str(addStripsListString), type = 'string')


def updateMeshStripsForGBFFCUpdatesFromUI():
    
    import cPickle as Pickle
    if not cmds.objExists('meshGenGBNode'):
        return 
        
    currMSNode = cmds.getAttr('meshGenGBNode.currentMeshStripNode')

    if not currMSNode:
        return 
            
    removeStripsList = []
    removeListString = cmds.getAttr(currMSNode + '.removeStripsList')
    if removeListString:
        removeStripsList = Pickle.loads(str(removeListString))
    
    addStripsList = []
    addStripsListString = cmds.getAttr(currMSNode + '.addStripsList')
    if addStripsListString:
        addStripsList = Pickle.loads(str(addStripsListString))
        
    updateMeshStripsForGBFFCUpdatesEXEC(removeStripsList, addStripsList)
    removeAddStripDatabaseInit()
    
    
def reapplyGBStripShader():
			    
    crvNodes = getStripIPNodes(False, 'crv')
    assignGBStripShader(crvNodes)
    return
    
#    print 're'
    bothNodes = getStripIPNodes(False, 'both') 
    for ext in bothNodes[0]:
        stp = getStpNameFromExt(ext)
        cmds.sets(stp, edit = True, forceElement = 'initialShadingGroup')
#        cmds.sets(stp, edit = True, forceElement = 'stripShaderSG_bkpExt_gbChar_01_1_Demo_Face_GB')
		    

def removeAddStripDatabaseInit():
    
    import cPickle as Pickle
    
    currMSNode = cmds.getAttr('meshGenGBNode.currentMeshStripNode')

    removeStripsListString = Pickle.dumps([])
    addStripsListString = Pickle.dumps([])
#    print 'initilaized remove add strip database'
    cmds.setAttr(currMSNode + '.removeStripsList', str(removeStripsListString), type = 'string')
    cmds.setAttr(currMSNode + '.addStripsList', str(addStripsListString), type = 'string')
        

def updateMeshStripsForGBFFCUpdatesEXEC(remManual, addManual):
    
#    print remManual, addManual, 'inisde EXEC'
    refreshManual = list(set(remManual) & set(addManual))
    onlyRemManual = list(set(remManual) - set(addManual))
    onlyAddManual = list(set(addManual) - set(remManual))
    
    if onlyRemManual:
#        print 'removing strips' , onlyRemManual
        removeStripsFromDict(onlyRemManual)
    
    if onlyAddManual:
#        print 'adding strips', onlyAddManual
        generateGBMeshStrips(onlyAddManual, 'new')
        cmds.evalDeferred('reapplyGBStripShader()')
    
    if refreshManual:
#        print 'refereshing strips', refreshManual
        generateGBMeshStrips(refreshManual, 'addRemove')
        cmds.evalDeferred('reapplyGBStripShader()')
        

def removeStripsFromDict(remList):
    
#    print remList, 'remove list'
    
    
    import cPickle as Pickle
    currMSNode = cmds.getAttr('meshGenGBNode.currentMeshStripNode')
    gbNode = ''
    if cmds.attributeQuery('connectedGBNode', node = currMSNode, exists = True):
        gbNode = cmds.getAttr(currMSNode + '.connectedGBNode')
    
    stripIPCurves = []
    stripIPCurvesString = cmds.getAttr(currMSNode + '.stripIPCurves')
    if stripIPCurvesString:
        stripIPCurves = Pickle.loads(str(stripIPCurvesString))   
    
    if not stripIPCurves:
        return

    overrideStripCurves = []
    overrideStripCurvesString = cmds.getAttr(currMSNode + '.overrideStripCurves')
    
    if overrideStripCurvesString:
        overrideStripCurves = Pickle.loads(str(overrideStripCurvesString))
                        
              
    stripDict = getStripValuesDict()
    
    if not remList:
        return
    ctrlGrp = []    
#    crv = 'bkpExt_gbChar_01_1_Demo_Face_curve6'

    for crv in remList:
        if crv in stripDict.keys():
            del stripDict[crv]
        stpName = ''
        
        if cmds.objExists(crv):
            shp = cmds.listRelatives(crv, s = True)[0]
            conn = cmds.listConnections(shp, type = 'extrude')
            if conn:
                ext = conn[0]
                nt = cmds.listConnections(ext, type = 'nurbsTessellate')
                if nt:
                    norm = cmds.listConnections(nt[0], type = 'polyNormal')
                    if norm:
                        stpName = cmds.listConnections(norm[0], type = 'mesh')
                        

#            rotateGrp = getStripWidthCtrl(crv,ext)    
#            ctrlGrp = cmds.listRelatives(rotateGrp, p = True)
        
        if stpName:
            if cmds.objExists(stpName[0]):
#                print 'remove strips deleting' , stpName[0]
                cmds.delete(stpName[0])        
        
       
        stpNameTry = crv + '_polyStrip'
#        print stpNameTry, 'tryy'
        stpGrps = createMeshStripSubGroup()
        
        if cmds.objExists(stpNameTry):
            prnt =  cmds.listRelatives(stpNameTry, p = True)
            if prnt:
                if prnt[0] == stpGrps[0]:
                    cmds.delete(stpNameTry)
        
        ctrlGrpTry = crv + '_stripCtrlGrp0'
#        print ctrlGrpTry, 'grp tryppp'
        if cmds.objExists(ctrlGrpTry):
            prnt = cmds.listRelatives(ctrlGrpTry, p = True)
            if prnt:
                if prnt[0] == stpGrps[1]:
                    cmds.delete(ctrlGrpTry)
                
        if crv in stripIPCurves:
            stripIPCurves.remove(crv)            
    
        count = len(overrideStripCurves)
        
        for x in range(count):
            if overrideStripCurves[x]:
                if crv in overrideStripCurves[x]:
                    overrideStripCurves[x].remove(crv)
    
    if not gbNode:
        for each in remList:
            if cmds.objExists(each):
                cmds.parent(each, world = True)
        
    stripDictString = Pickle.dumps(stripDict)
    overrideStripCurvesString = Pickle.dumps(overrideStripCurves)        
    stripIPCurvesString = Pickle.dumps(stripIPCurves)
        
    cmds.setAttr(currMSNode + '.overrideStripCurves', str(overrideStripCurvesString), type = 'string')
    cmds.setAttr(currMSNode + '.stripValuesDict', str(stripDictString), type = 'string')
    cmds.setAttr(currMSNode + '.stripIPCurves', str(stripIPCurvesString), type = 'string')

def addStripsFromCurvesUI():
    
    sel = cmds.ls(sl = True)
    
    super = []
    if not sel:
        reportGBMeshStripMessage('Nothing Selected', True, True, 'red')
    else:        
        super = cmds.listRelatives(cmds.listRelatives(cmds.ls(sl = True), ad = True, typ = 'nurbsCurve'), p = True)
    
    if not super:
        reportGBMeshStripMessage('No Curves Selected', True, True, 'red')
    
    currMSNode = cmds.getAttr('meshGenGBNode.currentMeshStripNode')
    msGrp = cmds.getAttr(currMSNode + '.msGrp')
    ipScalp = cmds.getAttr(currMSNode + '.inputScalp')
    curvesGrp = 'inputStripCurvesFor_' + ipScalp
    
    if cmds.objExists(curvesGrp):
        parentGrp = cmds.listRelatives(curvesGrp, p = True)
        if parentGrp:
            if msGrp == parentGrp[0]:
                cmds.parent(super, curvesGrp)
    
    updateMeshStripsForGBFFCUpdatesEXEC([], super)
    
def removeStripsUI():
    
    bothNodes = getAffectedStripNodes()    
    
    if bothNodes:
        extNodes = bothNodes[0]
        crvNodes = bothNodes[1]
        
        if 'globalPolyExtrude' in crvNodes:
            reportGBMeshStripMessage('No Mesh Strips Selected', True, True, 'red')
            
        updateMeshStripsForGBFFCUpdatesEXEC(crvNodes, [])            
        
    
def setMeshStripsVisibilty(mode):
    
    if not cmds.objExists('meshGenGBNode'):
        return
    currMSNode = cmds.getAttr('meshGenGBNode.currentMeshStripNode')
    if not currMSNode:
        return
    msGrp = cmds.getAttr(currMSNode + '.msGrp')
    cmds.setAttr(msGrp + '.visibility', mode)
    

def stripCurvatureChange(bothNodes = [], gradientGraphList = []):
    
    return 
    import cPickle as Pickle
    currMSNode = cmds.getAttr('meshGenGBNode.currentMeshStripNode')
    gradientGraphList = []
    currSel = cmds.ls(sl = True)
    if not bothNodes:
        bothNodes = getAffectedStripNodes(8)
 
#    if not gradientGraph:
        gradientGraph = cmds.gradientControlNoAttr('stripCurvatureGraph', q = True, asString = True)
        gradientGraphList = [gradientGraph] * len(bothNodes[0])
           
    extNodes = bothNodes[0]
    crvNodes = bothNodes[1]
    
    currGraph = cmds.gradientControlNoAttr('stripCurvatureGraph', q = True, asString = True)
    stripDict = getStripValuesDict()
    
    divList = [stripDict[crv][6] for crv in crvNodes]
    widthList = [stripDict[crv][0] for crv in crvNodes]
    
    finalVtxList = []
    finalNormalList = []
    
    
    if 'globalPolyExtrude' in crvNodes:
        stripDict['globalPolyExtrude'][8] = currGraph
        globe = True
        crvNodes.remove('globalPolyExtrude')
    
        
    for crv,ext,graph,div,width in zip(crvNodes,extNodes,gradientGraphList,divList,widthList):
        cmds.gradientControlNoAttr('stripCurvatureGraph', edit = True, asString = graph)
        stpName = cmds.listConnections(ext, type = 'mesh')[0]
   
        vlist = [4,5]
        maxV = 6 + (div * 2)
        minV = maxV - div
        for x in range(minV,maxV):
            vlist.append(x)
        inc = 1.0 / (div)            
        qPt = 0.0
        stripDict[crv][8] = graph
        for x in range(1,len(vlist)):
            currVtx = vlist[x]
#            print x, currVtx, qPt
            graphOp = cmds.gradientControlNoAttr('stripCurvatureGraph', q = True, vap = qPt)
            if graphOp > 0.5:
                pushValue = remapNew(0,width,0.5,1.0,graphOp)
            elif graphOp < 0.5:
                pushValue = remapNew(0,-1.0 * width,0.5,0.0,graphOp)
            else:
                pushValue = 0.0
                
            resetPos = cmds.pointOnCurve(crv,pr = qPt, p=True)
            vtxName = stpName + '.vtx[' + str(currVtx) + ']'
            cmds.xform(vtxName, ws = True, t = resetPos)
#            if not pushValue == 0.0:
#                finalVtxList.append(vtxName)
#                finalNormalList.append(pushValue)
            finalVtxList.append(vtxName)
            finalNormalList.append(pushValue)                    
            qPt = qPt + inc 
    

    if finalVtxList:         
        cmds.select(finalVtxList, r = True)
        cmds.moveVertexAlongDirection(finalVtxList, n = finalNormalList)            
    
    cmds.gradientControlNoAttr('stripCurvatureGraph', edit = True, asString = currGraph)
#    print stripDict['bkpExt_gbChar_01_1_Demo_Face_curve34'][13], '19513'
    stripDictString = Pickle.dumps(stripDict)
    cmds.setAttr(currMSNode + '.stripValuesDict', str(stripDictString), type = 'string')
    
    if currSel:
        cmds.select(currSel, r = True)
    else:
        cmds.select(cl = True)    

    

def getStripDictValuesPerIndex(crvNodes, index):
    
    stripDict = getStripValuesDict()
    for crv in crvNodes:
        stripDict[crv][index]
        
    
def getBGUIColor():
    
#    if not cmds.getAttr('meshGenGBNode.bgUIColor'):
    cmds.button('stripResetOverride', edit = True, ebg = True)   
    bgc = cmds.button('stripResetOverride', q = True, bgc = True)   
    cmds.button('stripResetOverride', edit = True, ebg = False)  
    cmds.setAttr('meshGenGBNode.bgUIColor', bgc[0])
    return bgc[0]

def getStripControlBGColor(crv, index):
    
    import cPickle as Pickle
    currMSNode = cmds.getAttr('meshGenGBNode.currentMeshStripNode')
    defaultBG = [getBGUIColor()]*3
    overBG = [0.4,0.3,0.3]

    overrideStripCurves = []
    overrideStripCurvesString = cmds.getAttr(currMSNode + '.overrideStripCurves')
    
    if overrideStripCurvesString:
        overrideStripCurves = Pickle.loads(str(overrideStripCurvesString))
# overrideStripCurves[1]    
    if not overrideStripCurves:
#        print crv, index, 'not here at all'
        return defaultBG
        
    if crv in overrideStripCurves[index]:
#        print crv, index, 'here'
        return overBG
    else:
#        print crv, index, 'not here'
        return defaultBG                

def createFollicleStripMesh(mesh):
    
        
    meshShp = cmds.listRelatives(mesh, s = True)[0]
    follT = cmds.createNode('transform' , name = mesh + '_follicle')
    follShp = cmds.createNode('follicle', name = follT + 'Shp', parent = follT)
#    uv = cmds.polyEditUV( mesh + '.map[0]', query=True )
    cmds.connectAttr(meshShp + '.worldMatrix[0]', follShp + '.inputWorldMatrix')
    cmds.connectAttr(meshShp + '.worldMesh[0]', follShp + '.inputMesh')
    cmds.connectAttr(follShp + '.outRotate', follT + '.rotate')
    cmds.connectAttr(follShp + '.outTranslate', follT + '.translate')    
    cmds.setAttr(follShp + '.parameterU', 0.5)
    cmds.setAttr(follShp + '.parameterV', 0.5)
    cmds.setAttr(follT + '.visibility', False)
    
    return follT
    
def stripRootGraphChange():
    
    bothNodes = getAffectedStripNodes(10)
    gradientGraph = cmds.gradientControlNoAttr('stripRootGraph', q = True, asString = True)
#    print getStripValuesDict()['bkpExt_gbChar_01_1_Demo_Face_curve15'][13], '$$$'
    meshStripDictAdd(bothNodes[1], 10, gradientGraph) 
    
    stripCurvatureChangeUI(bothNodes)
    
    storeRestoreRootVtxForStripShove(bothNodes, 'store')
    stripShoveChange(bothNodes, 'dict')
    
def stripTipGraphChange():
    
    bothNodes = getAffectedStripNodes(11)
    gradientGraph = cmds.gradientControlNoAttr('stripTipGraph', q = True, asString = True)
    meshStripDictAdd(bothNodes[1], 11, gradientGraph) 

    stripCurvatureChangeUI(bothNodes)

    storeRestoreRootVtxForStripShove(bothNodes, 'store')
    stripShoveChange(bothNodes, 'dict')
    
def stripGraphBiasChange():
    
    bothNodes = getAffectedStripNodes(12)
    bias = cmds.floatSliderGrp('stripCurvatureBiasSlider', q = True, v = True)
    meshStripDictAdd(bothNodes[1], 12, bias) 

    stripCurvatureChangeUI(bothNodes)    

    storeRestoreRootVtxForStripShove(bothNodes, 'store')
    stripShoveChange(bothNodes, 'dict')


def rootToTipGraphCopy(mode):
    
    rootGraph = cmds.gradientControlNoAttr('stripRootGraph', q = True, asString = True)
    tipGraph = cmds.gradientControlNoAttr('stripTipGraph', q = True, asString = True)
    
    if mode == 0:
        cmds.gradientControlNoAttr('stripTipGraph', edit = True, asString = rootGraph)
        stripTipGraphChange()
    
    else:
        cmds.gradientControlNoAttr('stripRootGraph', edit = True, asString = tipGraph)
        stripRootGraphChange()
        
        
def loadStripGraphPreset(rootTip, graph):
    
#    -    (    )    S
#    0    1    2    3
    
    graphShapeList = ['0.5,0,3,0.5,1,3', '0.5,0,3,0.9,0.5,3,0.5,1,3', '0.5,0,3,0.1,0.5,3,0.5,1,3,','0.5,0,3,0.9,0.25,3,0.1,0.75,3,0.5,1,3 ']
    if rootTip == 0:
        cmds.gradientControlNoAttr('stripRootGraph', edit = True, asString = graphShapeList[graph])
        stripRootGraphChange()
    else:
        cmds.gradientControlNoAttr('stripTipGraph', edit = True, asString = graphShapeList[graph])
        stripTipGraphChange()
                

def round_toGB(n, precision):
    correction = 0.5 if n >= 0 else -0.5
    return int( n/precision+correction ) * precision

def round_to_05GB(n):
    return round_toGB(n, 0.00005)

#getVtxListForStripCurvature('bkpExt_gbChar_01_1_Demo_Face_curve18_polyStrip')
def getVtxListForStripCurvature(stpName):
    
    vtxCount = cmds.polyEvaluate(stpName, v = True)
    uvList = cmds.polyEditUV(stpName + '.map[*]', query  = True)
    uList = uvList[::2]
    vList = uvList[1::2]
    uMin = min(uList)
    uMax = max(uList)
    vMin = min(vList)
    vMax = max(vList)
    uCount = len(set(uList)) 
    vCount = len(set(vList))
    
    uInc = (uMax - uMin) / (uCount-1)
    vInc = (vMax - vMin) / (vCount-1)
    
    uCurr = uMin
    vCurr = vMin
    
    sortUV = []
    for x in range(uCount):
        vCurr = vMin
        for y in range(vCount):
            sortUV.append(uCurr)
            sortUV.append(vCurr)
            vCurr = vCurr + vInc
        uCurr = uCurr + uInc
    
#    print uvList
#    print sortUV            
        
    uvGrp = [[round_to_05GB(uvList[x]),round_to_05GB(uvList[x+1])] for x in range(0, vtxCount*2,2)]
    uvSortGrp =  [[round_to_05GB(sortUV[x]),round_to_05GB(sortUV[x+1])] for x in range(0, vtxCount*2,2)]
    
    finalVtxList = []
    for each in uvSortGrp:
        if each in uvGrp:
            finalVtxList.append(uvGrp.index(each))

#    print finalVtxList
    return finalVtxList


def stripCurvatureChangeUI(bothNodes):
    
#    print 'curvature change'
    currSel = cmds.ls(sl = True)
    import cPickle as Pickle
    currMSNode = cmds.getAttr('meshGenGBNode.currentMeshStripNode') 
    
    extNodes = bothNodes[0]
    crvNodes = bothNodes[1]
    
    stripDict = getStripValuesDict()        
    
    if 'globalPolyExtrude' in crvNodes:
        crvNodes.remove('globalPolyExtrude')
    
    stripRootGraphList = [stripDict[crv][10] for crv in crvNodes]
    stripTipGraphList =  [stripDict[crv][11] for crv in crvNodes]
    stripGraphBiasList =  [stripDict[crv][12] for crv in crvNodes]
    stripGraphFalloffList = [stripDict[crv][14] for crv in crvNodes]
    
    heightList = [stripDict[crv][15] for crv in crvNodes]
    widthList = [stripDict[crv][0] for crv in crvNodes]
    segList = [int(stripDict[crv][9]) for crv in crvNodes] 
    divList = [int(stripDict[crv][6]) for crv in crvNodes]
    
    stripList = [getStpNameFromExt(ext) for ext in extNodes]
#    stripList = [cmds.listConnections(ext, type = 'mesh')[0] for ext in extNodes]
            
    bkpRootGraph = cmds.gradientControlNoAttr('stripRootGraph', q = True, asString = True)
    bkpTipGraph = cmds.gradientControlNoAttr('stripTipGraph', q = True, asString = True)
    
    storeRestoreStripVtxPos(bothNodes, 'restore')
    
    finalVtxList = []
    finalNormalDist = []
     
    for crv, ext, rootG, tipG, bias, foff, height, width, segs, divs, stp in zip(crvNodes, extNodes, stripRootGraphList, stripTipGraphList, stripGraphBiasList, stripGraphFalloffList, heightList, widthList, segList, divList, stripList):
#stp = 'bkpExt_gbChar_01_1_Demo_Face_curve19_polyStrip'
        vtxList = getVtxListForStripCurvature(stp)
        stripVtxList = [stp + '.vtx[' + str(x) + ']' for x in vtxList]    
#        print len(stripVtxList), vtxList
        
        cmds.gradientControlNoAttr('stripRootGraph', edit = True, asString = rootG)
        cmds.gradientControlNoAttr('stripTipGraph', edit = True, asString = tipG)
#        tipVtx1 = int((segs+1)*2 + (divs-1))
#        tipVtx2 = int(tipVtx1 + (segs*divs))
        tipVtx1 = 2
        tipVtx2 = 3
        tipPos1 = cmds.xform(stp + '.vtx[' + str(tipVtx1) + ']', q = True, ws = True, t = True)
        tipPos2 =  cmds.xform(stp + '.vtx[' + str(tipVtx2) + ']', q = True, ws = True, t = True)
        tipWidth = distance3d(tipPos1,tipPos2) 
        rootWidth = width 
        
#        print tipVtx1, tipVtx2, tipPos1,tipPos2, tipWidth, width, rootWidth
        segCount = 0    
        segs = int(segs)
        inc = 1.0 / segs
        qPt = 0.0
#        print segs, '<<<'

        vtxCounter = 0
#        print segs, divs , 'segdov'
        for seg in range(int(segs+1)):
            
#            print 'curr seg', seg
#            print stripVtxList , 'vtx list'
            
            
            biasPos = int(bias * (divs+1))

            biasPre = int(biasPos * (1 - foff))
            biasPost = int(biasPos + (((divs + 1) -  biasPos) * foff))
            
            rootP = cmds.gradientControlNoAttr('stripRootGraph', q = True, vap = qPt)
            tipP = cmds.gradientControlNoAttr('stripTipGraph', q = True, vap = qPt)
            
            rootP = remapNew(-1.0,1.0,0.0,1.0,rootP)
            tipP = remapNew(-1.0,1.0,0.0,1.0,tipP)
             
#            print qPt, segCount
            
            for x in range(divs+1):
                
                
                if x < biasPre:
#                    pr = mm.eval('linstep(0,' + str(biasPos) + ',' + str(x) + ');')
                    
#                    finalP = ((1-pr) * rootP) + (pr * tipP)
#                    finalP = ((1-pr) * rootP)    
                    pr = rootP
                    finalP = pr
                    
                
                elif x > biasPost:
#                    pr = mm.eval('linstep(' + str(biasPos) + ',' + str(divs+2) + ',' + str(x) + ');')
#                    finalP = (pr * rootP) + ((1-pr) * tipP)  
#                    finalP = ((1-pr) * tipP)                      
                    pr = tipP
                    finalP = pr
                    
                else:
                    if x < biasPos:
                        pr = remapNew(1.0,0.5,biasPre,biasPos, x)
                        finalP = (pr * rootP) + ((1-pr) * tipP)
                    elif x > biasPos:
                        pr = remapNew(0.5,1.0,biasPos, biasPost, x)
                        finalP = (pr * tipP) + ((1-pr) * rootP)
                    else:
                        pr = 0.5 
                        finalP = (pr * rootP) + (pr * tipP)
                        
                                        
                currWidth =  remapNew(rootWidth, tipWidth, 1, divs, x)                                   
                multHeight = remapNew(0.0,2.0,0.0,1.0,height)
                
                currWidth = currWidth * multHeight
#                print finalP, '<<'            

                
#                adjP = remapNew(-1.0,1.0,0.0,1.0,finalP)
                adjP = finalP
                nDist = adjP * (currWidth*0.5)
#                print vtxCounter
#                print stripVtxList[vtxCounter], stp, x
                if not nDist == 0.0:
                           
                    finalVtxList.append(stripVtxList[vtxCounter])
                    finalNormalDist.append(nDist)

#                print rootP, tipP, biasPos, pr, finalP, adjP, nDist, x, stripVtxList[x], 'rootP, tipP, biasPos, pr, finalP, adjP, nDist, x, stripVtxList[x]'
                vtxCounter = vtxCounter + 1
            segCount = segCount + 1
            qPt = qPt + inc                    
       
    
    if finalVtxList:     
#        print finalVtxList    
        cmds.select(finalVtxList, r = True)
        cmds.moveVertexAlongDirection(finalVtxList, n = finalNormalDist)            
                
#    storeRestoreStripVtxPos(bothNodes, 'store')
    
    cmds.gradientControlNoAttr('stripRootGraph', edit = True, asString = bkpRootGraph)
    cmds.gradientControlNoAttr('stripTipGraph', edit = True, asString = bkpTipGraph)
    
    if currSel:
        cmds.select(currSel, r = True)
    else:
        cmds.select(cl = True) 
            
            
    
def storeRestoreStripVtxPos(bothNodes,mode):
    
    import cPickle as Pickle
    
    extNodes = bothNodes[0]
    crvNodes = bothNodes[1]
    
    stripDict = getStripValuesDict()

    stpList = [getStpNameFromExt(ext) for ext in extNodes if ext]
#    stpList = [cmds.listConnections(ext, type = 'mesh')[0] for ext in extNodes if ext]
#    stp = stpList[0]
    for crv,stp in zip(crvNodes, stpList):
#        print crv, stp
        if mode == 'store':
            stripDict[crv][13] = [cmds.xform(stp + '.vtx[' + str(x) + ']', q = True, ws = True, t = True) for x in range(cmds.polyEvaluate(stp, v = True))]
        elif mode == 'restore':
#            print stripDict[crv][13]
            if not stripDict[crv][13]:
                continue
            for x in range(cmds.polyEvaluate(stp, v = True)):
                cmds.xform(stp + '.vtx[' + str(x) + ']', ws = True, t = stripDict[crv][13][x])
#        print stripDict[crv][13], mode                
        
#    print stripDict['bkpExt_gbChar_01_1_Demo_Face_curve34'][13]
    currMSNode = cmds.getAttr('meshGenGBNode.currentMeshStripNode')
    stripDictString = Pickle.dumps(stripDict)
    cmds.setAttr(currMSNode + '.stripValuesDict', str(stripDictString), type = 'string')
    
def assignGBHotkeys():
    
    cmds.nameCommand( 'drawGBGuidesNameCommand', ann='Draw Groomboy Guides', c='hotCommandForDrawGuides()' )
    cmds.hotkey( keyShortcut='g', altModifier=True, name='drawGBGuidesNameCommand' )

def hotCommandForDrawGuides():
    
    gb = False
    allJobs = cmds.scriptJob(lj = True)
    for job in allJobs:
        if not 'restartGroomBoy' in job:
            return
            
    a = cmds.tabLayout('mainTabs', query = True, vis = True)
    b = cmds.tabLayout('mainTabs', query = True, sti = True) == 1
    c = cmds.button('startDrawBtn', q = True, vis = True)
    
    if a and c:
        if not b:
            cmds.tabLayout('mainTabs', edit = True, sti = 1)
            tabSelectChange()
        startDraw()            
        
        
                
         
#    if cmds.tabLayout('mainTabs', query = True, sti = True) == 1:
        

def assignGBStripShader(crvNodes):
    
    sel = cmds.ls(sl = True)
    currMSNode = cmds.getAttr('meshGenGBNode.currentMeshStripNode')
    ipScalp = cmds.getAttr(currMSNode + '.inputScalp')
    
    stripShader = 'stripShader_' + ipScalp
    stripShaderSG = 'stripShaderSG_' + ipScalp
    stripShaderRamp = 'stripShaderRamp_' + ipScalp
    
    if not cmds.objExists(stripShader):
        cmds.shadingNode('lambert', name = stripShader, asShader = True)
        cmds.select(cl = True)
    if not cmds.objExists(stripShaderSG):
        cmds.sets(name = stripShaderSG, renderable = True,  noSurfaceShader = True)
        cmds.connectAttr(stripShader + '.outColor', stripShaderSG + '.surfaceShader', f = True)

#    extNodes = getStripExtrudeNodes(crvNodes)
     
    stpList = [poly + '_polyStrip' for poly in crvNodes]
#    print stpList  
    for stp in stpList:
        if cmds.objExists(stp):
            cmds.sets(stp, edit = True, forceElement = 'initialShadingGroup')
            cmds.sets(stp, edit = True, forceElement = stripShaderSG)    
    
#    cmds.sets(stpList, edit = True, forceElement = 'initialShadingGroup')
#    cmds.sets(stpList, edit = True, forceElement = stripShaderSG)        
    
            
        
    if not cmds.objExists(stripShaderRamp):
        cmds.createNode('ramp', name = stripShaderRamp)        
        cmds.setAttr(stripShaderRamp + '.colorEntryList[0].color', 1.0,0.3,0.3, type = 'double3')
        cmds.setAttr(stripShaderRamp + '.colorEntryList[1].color', 0.3,0.3,1.0, type = 'double3')
        cmds.setAttr(stripShaderRamp + '.colorEntryList[1].position', 1)
#        setAttr "stripShaderRamp_bkpExt_gbChar_01_1_Demo_Face.colorEntryList[1].position" 1
        cmds.connectAttr(stripShaderRamp + '.outColor', stripShader + '.color', force = True)        
    
    if sel:
        cmds.select(sel, r = True)
    else:
        cmds.select(cl = True)        
        
    
def stripGraphFalloffChange():
    
    bothNodes = getAffectedStripNodes(14)
    bias = cmds.floatSliderGrp('stripCurvatureFalloffSlider', q = True, v = True)
    meshStripDictAdd(bothNodes[1], 14, bias) 
    stripCurvatureChangeUI(bothNodes)    
    
    storeRestoreRootVtxForStripShove(bothNodes, 'store')
    stripShoveChange(bothNodes, 'dict')    

def stripGraphHeightChange():
    
    bothNodes = getAffectedStripNodes(15)
    bias = cmds.floatField('stripCurvatureHeightField', q = True, v = True)
    meshStripDictAdd(bothNodes[1], 15, bias) 
    stripCurvatureChangeUI(bothNodes)    
    
    storeRestoreRootVtxForStripShove(bothNodes, 'store')
    stripShoveChange(bothNodes, 'dict')  
    
def stripCurvatureHeightFieldChange():
    
    value = cmds.floatField('stripCurvatureHeightField', q = True, v = True)
    cmds.floatSlider('stripCurvatureHeightSlider', edit = True, v = value)
    stripGraphHeightChange()
    
def stripCurvatureHeightSliderChange():
    
    value = cmds.floatSlider('stripCurvatureHeightSlider', q  = True, v = True)
    cmds.floatField('stripCurvatureHeightField', edit = True, v = value)
    stripGraphHeightChange()
        
def getCurrentMeshStripGroup():
    
    stripGrp = False
    
    if cmds.objExists('meshGenGBNode'):
        currMSNode = cmds.getAttr('meshGenGBNode.currentMeshStripNode')
        if currMSNode:
            ipScalp = cmds.getAttr(currMSNode + '.inputScalp')
            if ipScalp:
                grpName = ipScalp + '_meshStripsMainGrp'
                if cmds.objExists(grpName):
                    grpChildren = cmds.listRelatives(grpName, c = True)
                    if grpChildren:
                        stripGrp = grpName
                        
    return stripGrp    
    
def copyPasteCurvatureGraph(rootTip, mode):
    
    rootG = cmds.gradientControlNoAttr('stripRootGraph', q = True, asString = True)
    tipG = cmds.gradientControlNoAttr('stripTipGraph', q = True, asString = True)
    currMSNode = cmds.getAttr('meshGenGBNode.currentMeshStripNode')  
    
    if rootTip == 0 and mode == 0:
        cmds.setAttr(currMSNode + '.stripGraphClipboard', rootG, type = 'string')
    elif rootTip == 0 and mode == 1:
        cbGraph = cmds.getAttr(currMSNode + '.stripGraphClipboard')
        if not cbGraph:
            reportGBMeshStripMessage('There is no graph copied. Please copy graph first', True, True, 'red')
        cmds.gradientControlNoAttr('stripRootGraph', edit = True, asString = cbGraph)
        stripRootGraphChange()    
    elif rootTip == 1 and mode == 0:        
        cmds.setAttr(currMSNode + '.stripGraphClipboard', tipG, type = 'string')
    elif rootTip == 1 and mode == 1:
        cbGraph = cmds.getAttr(currMSNode + '.stripGraphClipboard')
        if not cbGraph:
            reportGBMeshStripMessage('There is no graph copied. Please copy graph first', True, True, 'red')
        cmds.gradientControlNoAttr('stripTipGraph', edit = True, asString = cbGraph)
        stripTipGraphChange()    
    elif rootTip == 2 and mode == 2:       
        cmds.gradientControlNoAttr('stripRootGraph', edit = True, asString = tipG) 
        stripRootGraphChange()   
        cmds.gradientControlNoAttr('stripTipGraph', edit = True, asString = rootG) 
        stripTipGraphChange() 
        

def getRootVertexForStripShove(stpName):
    
    
    
    vtxCount = cmds.polyEvaluate(stpName, v = True)
    uvList = cmds.polyEditUV(stpName + '.map[*]', query  = True)
    uList = uvList[::2]
    vList = uvList[1::2]
    uMin = min(uList)
    uMax = max(uList)
    vMin = min(vList)
    vMax = max(vList)
    uCount = len(set(uList)) 
    vCount = len(set(vList))
    
    uInc = (uMax - uMin) / (uCount-1)
    vInc = (vMax - vMin) / (vCount-1)
    
    uCurr = uMin
    vCurr = vMin
    
    sortUV = []
    for x in range(uCount):
        vCurr = vMin
        for y in range(vCount):
            sortUV.append(uCurr)
            sortUV.append(vCurr)
            vCurr = vCurr + vInc
        uCurr = uCurr + uInc
    
#    print uvList
#    print sortUV            
        
    uvGrp = [[round_to_05GB(uvList[x]),round_to_05GB(uvList[x+1])] for x in range(0, vtxCount*2,2)]
    uvSortGrp =  [[round_to_05GB(sortUV[x]),round_to_05GB(sortUV[x+1])] for x in range(0, vtxCount*2,2)]
    
    finalVtxList = []
    for each in uvSortGrp:
        if each in uvGrp:
            finalVtxList.append(uvGrp.index(each))

#    print finalVtxList
    finalVtxList = [int(x) for x in finalVtxList[::vCount]]
    return finalVtxList
    
def storeRestoreRootVtxForStripShove(bothNodes, mode):
    
    import cPickle as Pickle
    
    extNodes = bothNodes[0]
    crvNodes = bothNodes[1]
    
    stripDict = getStripValuesDict()
    
    stpList = [getStpNameFromExt(ext) for ext in extNodes if ext]
    
    for crv,ext,stp in zip(crvNodes, extNodes, stpList):
        indList = getRootVertexForStripShove(stp)
        if mode == 'store':
            stripDict[crv][17] = [cmds.xform(stp + '.vtx[' + str(x) + ']', q = True, ws = True, t = True) for x in indList]
        elif mode == 'restore':
#            print stripDict[crv][13]
            if not stripDict[crv][17]:
                continue
            for x in range(len(indList)):
                cmds.xform(stp + '.vtx[' + str(indList[x]) + ']', ws = True, t = stripDict[crv][17][x])            
                
    
    if mode == 'store':
        currMSNode = cmds.getAttr('meshGenGBNode.currentMeshStripNode')
        stripDictString = Pickle.dumps(stripDict)
        cmds.setAttr(currMSNode + '.stripValuesDict', str(stripDictString), type = 'string')                
                
    
    
def storeStripChangesToDB(mode):
    
    if not cmds.objExists('meshGenGBNode'):
        return
    currMSNode = cmds.getAttr('meshGenGBNode.currentMeshStripNode')
    if not currMSNode:
        return
    
    bothNodes = getStripIPNodes(False, 'both')
    if not bothNodes:
        return
    
    extNodes = bothNodes[0]
    stpName = getStpNameFromExt(extNodes[0])
#    cmds.duplicate(stpName, name = mode +  stpName)

    storeRestoreStripVtxPos(bothNodes, mode)        
    
             
def recallStripVtx(messg):
    
    if not cmds.objExists('meshGenGBNode'):
        return
    currMSNode = cmds.getAttr('meshGenGBNode.currentMeshStripNode')
    if not currMSNode:
        return
    
    bothNodes = getStripIPNodes(False, 'both')
    if not bothNodes:
        return
    
    extNodes = bothNodes[0]
    sel = getStpNameFromExt(extNodes[0])
    
    vt = cmds.polyEvaluate(sel, v = True)
    oPos = [cmds.xform(sel + '.vtx[' + str(x) + ']', q = True, ws = True, t = True) for x in range(vt)]
    
#    print messg, oPos

groomBoyDemo()