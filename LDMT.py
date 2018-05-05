# About ####################
# Auther:  Liu Dian
# Email:   xgits@outlook.com
# Website: www.xgits.com
# Version: Github

import maya.cmds as cmds
import maya.mel as mel
import platform
import getpass
import subprocess
import sys
import os
import json
# comment key words:
# CUSTOMIZABLE

################################ Define Globals Start ###############################

# common stuff
LDMT_version             = "0.1" # LDMT's child variable are lowercase with "_"
LDMT_UI_title            = "LD Maya Toolbox" + " " + LDMT_version
LDMT_UI_window           = "LDMT_UI_window"
LDMT_UI_form             = "LDMT_UI_form"
LDMT_UI_tab              = "LDMT_UI_tab"
LDMT_UI_dock             = "LDMT_UI_dock"
LDMT_UI_dock_area        = "left"
LDMT_UI_tab_scrollLayout = "LDMT_UI_tab_scrollLayout"
LDMT_UI_tab1             = "Modeling"
LDMT_UI_width            = 200
LDMT_UI_height           = 980
LDMT_UI_cell_height      = 21

USER_name = getpass.getuser()
MAYA_version = cmds.about(v=1)
MAYA_version_float = float(MAYA_version.split(' ')[0])
MAYA_location = mel.eval('getenv "MAYA_LOCATION"')
MAYA_pyLocation = MAYA_location+"/bin"+"/mayapy.exe"
# operating system
OS = platform.system()
if(OS != "Windows"):
    cmds.error("********** Not supporting " + OS)

# environment path
# naming convension:
# all capital presenting key words, captalize first means abbriviation, lower means complete path.

PATH_MAYA_app_dir = mel.eval("getenv MAYA_APP_DIR")
PATH_Doc_maya_scripts = PATH_MAYA_app_dir + "/scripts"

PATH_LDMT                    = PATH_Doc_maya_scripts   + "/LD_MayaToolbox" # CUSTOMIZABLE: LDMT path! You can customize if you want
PATH_LDMT_plugin             = PATH_LDMT               + "/plugin"
PATH_LDMT_exe                = PATH_LDMT               + "/exe"
              
PATH_LDMT_function           = PATH_LDMT               + "/function"
PATH_LDMT_Func_logging       = PATH_LDMT_function      + "/logging" # for modeling tab
PATH_LDMT_Func_modeling      = PATH_LDMT_function      + "/modeling" # for modeling tab
PATH_LDMT_Func_Mod_transform = PATH_LDMT_Func_modeling + "/transform"
PATH_LDMT_Func_Mod_select    = PATH_LDMT_Func_modeling + "/select"
PATH_LDMT_Func_Mod_generate  = PATH_LDMT_Func_modeling + "/generate"
PATH_LDMT_Func_Mod_uv        = PATH_LDMT_Func_modeling + "/uv"
PATH_LDMT_Func_Mod_trial     = PATH_LDMT_Func_modeling + "/trial"
PATH_LDMT_Func_Mod_debug     = PATH_LDMT_Func_modeling + "/debug"
PATH_LDMT_Func_Mod_editor    = PATH_LDMT_Func_modeling + "/editor"
PATH_LDMT_Func_Mod_file      = PATH_LDMT_Func_modeling + "/file"
PATH_LDMT_Func_Mod_info      = PATH_LDMT_Func_modeling + "/info"

PATH_SOURCE_ALL = ([PATH_LDMT_function,
                    PATH_LDMT_plugin,
                    PATH_LDMT_exe,
                    PATH_LDMT_function,
                    PATH_LDMT_Func_logging,
                    PATH_LDMT_Func_modeling,
                    PATH_LDMT_Func_Mod_transform,
                    PATH_LDMT_Func_Mod_select,
                    PATH_LDMT_Func_Mod_generate,
                    PATH_LDMT_Func_Mod_uv,
                    PATH_LDMT_Func_Mod_trial,
                    PATH_LDMT_Func_Mod_debug,
                    PATH_LDMT_Func_Mod_editor,
                    PATH_LDMT_Func_Mod_file,
                    PATH_LDMT_Func_Mod_info])

# define color
black        = [ 0.00 , 0.00 , 0.00 ]
white        = [ 1.00 , 1.00 , 1.00 ]
beige        = [ 0.74 , 0.74 , 0.74 ]
lighterGrey  = [ 0.36 , 0.36 , 0.36 ]
lightGrey    = [ 0.32 , 0.32 , 0.32 ]
grey         = [ 0.27 , 0.27 , 0.27 ]
darkGrey     = [ 0.22 , 0.22 , 0.22 ]
darkerGrey   = [ 0.17 , 0.17 , 0.17 ]
red          = [ 0.91 , 0.35 , 0.36 ]
orange       = [ 0.86 , 0.58 , 0.34 ]
yellow       = [ 0.75 , 0.70 , 0.23 ]
green        = [ 0.37 , 0.68 , 0.53 ]
cyan         = [ 0.28 , 0.67 , 0.71 ]
blue         = [ 0.35 , 0.65 , 0.80 ]
indigo       = [ 0.47 , 0.58 , 0.81 ]
purple       = [ 0.68 , 0.61 , 0.86 ]
lightYellow  = [ 1.00 , 0.91 , 0.58 ]

#timer
PM_startTime = cmds.timerX()
PM_timeAdder = 0

################################ Define Globals End ###############################

# all defined function is started with f_
################################ Define Main Functions Start ###############################

def LDMT():
    f_sys_path_init()
    f_UI_init()
    f_UI_create()
    f_hotkey_init()
    f_plugin_init()

def f_sys_path_init():
    sizeOfPaths = len(PATH_SOURCE_ALL)
    for i in range(sizeOfPaths):
        if not PATH_SOURCE_ALL[i] in sys.path:
            sys.path.append(PATH_SOURCE_ALL[i])
            
def f_UI_init():
    if MAYA_version_float >= 2016 and cmds.dockControl(LDMT_UI_dock, ex=1):
        cmds.deleteUI(LDMT_UI_dock, ctl=1)
    if cmds.window(LDMT_UI_window, ex=1):
        cmds.deleteUI(LDMT_UI_window)

def f_UI_create():
    cmds.window(LDMT_UI_window, sizeable=0)
    cmds.formLayout(LDMT_UI_form)

    if MAYA_version_float >= 2016:
        cmds.dockControl(
            LDMT_UI_dock,
            w=LDMT_UI_width+9,
            h=LDMT_UI_height,
            fixedHeight=1,
            fixedWidth=1,
            moveable=1,
            area=LDMT_UI_dock_area,
            content=LDMT_UI_window,
            label=LDMT_UI_title,
            bgc=grey)
    else:
        cmds.showWindow(LDMT_UI_window)
        cmds.window(LDMT_UI_window, e=1, h=LDMT_UI_height)

    cmds.tabLayout(LDMT_UI_tab)
    cmds.formLayout(
        LDMT_UI_form,
        e=1,
        parent=LDMT_UI_window,
        attachForm=[(LDMT_UI_tab, 'top', 3), (LDMT_UI_tab, 'left', 5)])

    cmds.scrollLayout(LDMT_UI_tab_scrollLayout, w=LDMT_UI_width + 13)
    cmds.tabLayout(
        LDMT_UI_tab,
        e=1,
        h=LDMT_UI_height,
        tabLabel=[LDMT_UI_tab_scrollLayout, LDMT_UI_tab1])
    
    cmds.gridLayout(
        numberOfColumns=2,
        cellHeight=LDMT_UI_cell_height,
        cellWidth=LDMT_UI_width / 2)
    
    cmds.gridLayout(
        numberOfColumns=2,
        cellHeight=LDMT_UI_cell_height,
        cellWidth=LDMT_UI_width / 4)
    
    cmds.button(ann="UV editor.", bgc=darkGrey, l="UV", c= 'f_command("UV Editor")')
    cmds.button(ann="Shader editor.", bgc=darkGrey, l="Shader", c= 'f_command("Shader Editor")')
    cmds.setParent("..")
    cmds.button(ann="Outliner window.", bgc=darkGrey, dgc='f_command("Script Editor")', l="Outliner", c= 'f_command("Outliner")')
    cmds.setParent("..")
    
    cmds.frameLayout("transformTools",bgc=grey,l="Transform",collapsable=1,
                    preExpandCommand='f_collapseTurnColor("transformTools")',
                    preCollapseCommand='f_collapseTurnColor("transformTools")')

    cmds.gridLayout(numberOfColumns = 2, cellHeight = LDMT_UI_cell_height, cellWidth=LDMT_UI_width/2)
    cmds.gridLayout(numberOfColumns = 2, cellHeight = LDMT_UI_cell_height, cellWidth=LDMT_UI_width/4)
    
    cmds.button(ann="Mirror along X. Use Alt to reverse direction.", 
                bgc=red, l="Mirror X", c= 'f_command("Mirror X")')
    
    cmds.gridLayout(numberOfColumns = 2, cellHeight = LDMT_UI_cell_height, cellWidth=LDMT_UI_width/8)
    cmds.button(ann="Mirror along Y. Use Alt to reverse direction.", 
                bgc=green, l="M.Y", c= 'f_command("Mirror Y")')
    cmds.button(ann="Mirror along Y. Use Alt to reverse direction.", 
                bgc=blue, l="M.Z", c= 'f_command("Mirror Z")')    
    cmds.setParent("..")
    
    cmds.setParent("..")
    cmds.button(ann="Reset pivot.", 
                bgc=darkGrey, l="Reset Pivot", c= 'f_command("Reset Pivot")') 
    cmds.gridLayout(numberOfColumns = 2, cellHeight = LDMT_UI_cell_height, cellWidth=LDMT_UI_width/4)
    cmds.button(ann="Average position along normal.", 
                bgc=orange, l="Average", c= 'f_command("Average")') 
    cmds.gridLayout(numberOfColumns = 3, cellHeight = LDMT_UI_cell_height, cellWidth=LDMT_UI_width/12+1)
    cmds.button(ann="Align along X.", 
                bgc=red, l="X", c= 'f_command("Align X")') 
    cmds.button(ann="Align along Y.", 
                bgc=green, l="Y", c= 'f_command("Align Y")') 
    cmds.button(ann="Align along Z.", 
                bgc=blue, l="Z", c= 'f_command("Align Z")') 
    cmds.setParent("..")
    cmds.setParent("..")
    cmds.button(ann="Delete history. Use Ctrl to delete all.", 
                bgc=darkGrey, l="Del History", c= 'f_command("Delete History")') 
    
    cmds.gridLayout(numberOfColumns = 2, cellHeight = LDMT_UI_cell_height, cellWidth=LDMT_UI_width/4)
    cmds.button(ann="Circle.", 
                bgc=orange, l="Circle", c= 'f_command("Circularize")') 
    cmds.button(ann="Insert mesh as Zbrush.", 
                bgc=orange, l="InsertM", c= 'f_command("Insert Mesh")')
    cmds.setParent("..")
    cmds.button(ann="Like turbo smooth in 3dsmax. Soft to smooth, hard to keep sharp. Use Ctrl to make hard edge as crease.", 
                bgc=orange, l="Turbo Smooth", c= 'f_command("Turbo Smooth")')
    cmds.gridLayout(numberOfColumns = 2, cellHeight = LDMT_UI_cell_height, cellWidth=LDMT_UI_width/4)
    cmds.button(ann="Copy instances of selection to verts.", 
                bgc=orange, l="Copy2V", c= 'f_command("Copy to Vertices")')
    cmds.button(ann="Copy instances of selection to faces.", 
                bgc=orange, l="Copy2F", c= 'f_command("Copy to Faces")')
    cmds.setParent("..")
    cmds.button(ann="Rebuild subdivision.", 
                bgc=orange, l="Rebuild Subdiv", c= 'f_command("Rebuild Subdivision")')
    cmds.button(ann="Blendshape based on topology. Support partial.", 
                bgc=purple, l="Topo Blendshape", c= 'f_command("Topological Blendshape")')
    cmds.button(ann="Wrap cloth with basemesh then blendshape to target.", 
                bgc=purple, l="Wrap Retarget", c= 'f_command("Wrap Retarget")')
    cmds.text(al="center",l="Target Count",ann="Target triangle count.")
    cmds.intField("instantMeshes_targetCount",v=1000,min=1,max=1000000)
    cmds.button(ann="Put mesh into Instant Meshes.exe", 
                bgc=purple, l="Instant Meshes", c= 'f_command("Instant Meshes")')
    cmds.button(ann="Instant Meshes function to remesh.", 
                bgc=purple, l="Remesh", c= 'f_command("Instant Meshes Function")')
    cmds.setParent("..")
    cmds.setParent("..")
    
    # select tools
    cmds.frameLayout("selectTools",bgc=grey,l="Select",collapsable=1,
                    preExpandCommand='f_collapseTurnColor("selectTools")',
                    preCollapseCommand='f_collapseTurnColor("selectTools")')
    cmds.gridLayout(numberOfColumns = 2, cellHeight = LDMT_UI_cell_height, cellWidth=LDMT_UI_width/2)
    cmds.button(ann="Select hard edges. Can be used as filter on current selection.", 
                bgc=orange, l="Hard Edges", c= 'f_command("Select Hard Edges")')  
    cmds.button(ann="Select UV edges borders. Can be used as filter on current selection.", 
                bgc=green, l="UV Borders", c= 'f_command("Select UV Borders")') 
    cmds.button("camSelectButton",ann="Toggle cam based selection.", 
                bgc=orange, l="Cam Select is Off", c= 'f_command("Cam Select")') 
    cmds.button(ann="Select every N element.", 
                bgc=orange, l="N Edge Selector", c= 'f_command("N Edge Selector")')     
    f_queryToggleCamSelect()
    cmds.setParent("..")
    cmds.setParent("..")
    
    cmds.frameLayout("generateTools",bgc=grey,l="Generate",collapsable=1,
                    preExpandCommand='f_collapseTurnColor("generateTools")',
                    preCollapseCommand='f_collapseTurnColor("generateTools")')
    cmds.gridLayout(numberOfColumns = 1, cellHeight = LDMT_UI_cell_height, cellWidth=LDMT_UI_width)
    cmds.gridLayout(numberOfColumns = 4, cellHeight = LDMT_UI_cell_height, cellWidth=LDMT_UI_width/4)
    cmds.button(ann="Curve to procedural ribbon.", 
                bgc=blue, l="Ribbon", c= 'f_command("Curve to Ribbon")') 
    cmds.button(ann="Curve to procedural tube.", 
                bgc=blue, l="Tube", c= 'f_command("Curve to Tube")') 
    cmds.gridLayout(numberOfColumns = 2, cellHeight = LDMT_UI_cell_height, cellWidth=LDMT_UI_width/6)
    cmds.gridLayout(numberOfColumns = 1, cellHeight = LDMT_UI_cell_height, cellWidth=LDMT_UI_width/6)
    cmds.button(ann="Curve to procedural rope. Use shift for helix rope.", 
                bgc=blue, l="Rope", c= 'f_command("Curve to Rope")') 
    cmds.setParent("..")
    cmds.gridLayout(numberOfColumns = 1, cellHeight = LDMT_UI_cell_height, cellWidth=LDMT_UI_width/12)
    cmds.intField("rope_count",ann="Helix mode rope count",v=1,min=1,max=50)
    cmds.setParent("..")
    cmds.setParent("..")
    cmds.button(ann="Generate procedural braid.", 
                bgc=blue, l="Braid", c= 'f_command("Curve to Braid")') 
    cmds.setParent("..")
    # generateTools row 2
    cmds.gridLayout(numberOfColumns = 4, cellHeight = LDMT_UI_cell_height, cellWidth=LDMT_UI_width/4)
    cmds.button(ann="Curve to procedural spiral.", 
                bgc=blue, l="Spiral", c= 'f_command("Curve to Spiral")')
    cmds.button(ann="Curve to procedural instance.", 
                bgc=blue, l="Instance", c= 'f_command("Curve to Instances")')       
    cmds.button(ann="Curve to procedural seams.", 
                bgc=blue, l="Seams", c= 'f_command("Curve to Seams")')
    cmds.button(ann="Curve to procedural stitches.", 
                bgc=blue, l="Stitches", c= 'f_command("Curve to Stitches")')
    cmds.setParent("..")
    
    cmds.gridLayout(numberOfColumns = 2, cellHeight = LDMT_UI_cell_height, cellWidth=LDMT_UI_width/2)
    cmds.button(ann="Cleanup instances to meshes.", 
                bgc=darkGrey, l="Clean Instances", c= 'f_command("Clean Instances")')
    cmds.button(ann="Cleanup tubes to meshes.", 
                bgc=darkGrey, l="Clean tubes", c= 'f_command("Clean Tubes")')
    cmds.setParent("..")
    cmds.setParent("..")
    cmds.setParent("..")

    # UVTools Row 1
    cmds.frameLayout("UVTools",bgc=grey,l="UV",collapsable=1,
                    preExpandCommand='f_collapseTurnColor("UVTools")',
                    preCollapseCommand='f_collapseTurnColor("UVTools")')
    cmds.gridLayout(numberOfColumns = 2, cellHeight = LDMT_UI_cell_height, cellWidth=LDMT_UI_width/2)
    cmds.button(ann="Quick UV unwrap from bonus tools.", 
                bgc=green, l="QuickUV", c= 'f_command("Quick UV")')
    cmds.gridLayout(numberOfColumns = 2, cellHeight = LDMT_UI_cell_height, cellWidth=LDMT_UI_width/4)
    cmds.button(ann="Move all UVs into 0-1.", 
                bgc=green, l="UV In", c= 'f_command("UV In")')    
    cmds.button(ann="Move all overlaping UVs out of 0-1 .", 
                bgc=green, l="UV Out", c= 'f_command("UV Out")') 
    cmds.setParent("..")
    
    # UVTools Row 2
    cmds.button(ann="UV Deluxe.", 
                bgc=green, l="UV Deluxe", c= 'f_command("UV Deluxe")') 
    cmds.button(ann="Check UV bleeding.", 
                bgc=green, l="Check UV Bleed", c= 'f_command("Check UV Bleed")')  
    cmds.setParent("..")
    cmds.setParent("..")
    
    # Trial Row 1
    cmds.frameLayout("trialTools",bgc=grey,l="Trial",collapsable=1,
                    preExpandCommand='f_collapseTurnColor("trialTools")',
                    preCollapseCommand='f_collapseTurnColor("trialTools")')
    cmds.gridLayout(numberOfColumns = 2, cellHeight = LDMT_UI_cell_height, cellWidth=LDMT_UI_width/2)
    cmds.button(ann="Transfer expressions of source's using source as media to target basemesh.", 
                bgc=indigo, l="Face Transfer", c= 'f_command("Face Transfer")') 
    cmds.button(ann="LOD tool.", 
                bgc=indigo, l="LOD", c= 'f_command("LOD")') 
    cmds.setParent("..")
    cmds.setParent("..")

    # Debug Row 1
    cmds.frameLayout("debugTools",bgc=grey,l="Debug",collapsable=1,
                    preExpandCommand='f_collapseTurnColor("debugTools")',
                    preCollapseCommand='f_collapseTurnColor("debugTools")')
    cmds.gridLayout(numberOfColumns = 1, cellHeight = LDMT_UI_cell_height, cellWidth=LDMT_UI_width)
    cmds.gridLayout(numberOfColumns = 4, cellHeight = LDMT_UI_cell_height, cellWidth=LDMT_UI_width/4)
    cmds.button(ann="Optimize scene.", 
                bgc=orange, l="Scene", c= 'f_command("Optimize Scene")') 
    cmds.button(ann="Clean mesh.", 
                bgc=orange, l="Mesh", c= 'f_command("Clean Mesh")') 
    cmds.button(ann="Set normal to face.", 
                bgc=orange, l="Normal", c= 'f_command("Set Normal to Face")') 
    cmds.button(ann="Unlock normal but keep hard/soft edges.", 
                bgc=orange, l="KeepHS", c= 'f_command("Keeping HS")')  
    cmds.setParent("..")
    
    # Debug Row 2
    cmds.gridLayout(numberOfColumns = 4, cellHeight = LDMT_UI_cell_height, cellWidth=LDMT_UI_width/4)
    cmds.button(ann="Batch rename tool.", 
                bgc=orange, l="Rename", c= 'f_command("Batch Rename")') 
    cmds.button(ann="Delete namespace of selected obj.", 
                bgc=orange, l="Delname", c= 'f_command("Delete Namespace")') 
    cmds.button(ann="Ungroup selected groups.", 
                bgc=orange, l="Ungroup", c= 'f_command("Ungroup")') 
    cmds.button(ann="Fix reversed normal.", 
                bgc=orange, l="Reverse", c= 'f_command("Fix Reverse")') 
    cmds.setParent("..")
 
    # Debug Row 3
    cmds.gridLayout(numberOfColumns = 4, cellHeight = LDMT_UI_cell_height, cellWidth=LDMT_UI_width/4)
    cmds.button(ann="Vertice normal display.", 
                bgc=darkGrey, l="VertNm", c= 'f_command("Display Vert Normal")') 
    cmds.button(ann="Face normal Dispaly.", 
                bgc=darkGrey, l="FaceNm", c= 'f_command("Display Face Noraml")') 
    cmds.button(ann="Ungroup selected groups.", 
                bgc=darkGrey, l="Triangle", c= 'f_command("Display Triangle")') 
    cmds.button(ann="Texture border display.", 
                bgc=darkGrey, l="TexBord", c= 'f_command("Display TexBord")') 
    cmds.setParent("..")
    
    # Debug Row 4
    cmds.gridLayout(numberOfColumns = 4, cellHeight = LDMT_UI_cell_height, cellWidth=LDMT_UI_width/4)
    cmds.button(ann="Vertice ID display.", 
                bgc=darkGrey, l="VertID", c= 'f_command("Display Vert ID")') 
    cmds.button(ann="Polycount display.", 
                bgc=darkGrey, l="Count", c= 'f_command("Display Polycount")') 
    cmds.button(ann="Reset display.", 
                bgc=darkGrey, l="Reset", c= 'f_command("Reset Display")') 
    cmds.button(ann="Disable some plugins autoload for basic function.", 
                bgc=darkGrey, l="PluginC", c= 'f_command("Cleanup Plugins")') 
    cmds.setParent("..")
    
    cmds.gridLayout(numberOfColumns = 2, cellHeight = LDMT_UI_cell_height, cellWidth=LDMT_UI_width/2)
    cmds.button(ann="Reset Preferences while keeping hotkeys and shelfs.", 
                bgc=darkerGrey, l="ResetPf", c= 'f_command("Reset Preferences")') 

    cmds.floatSliderGrp("normalDisplaySize",ann="Edit normal display length.",
                        field=1,minValue=0,maxValue=20,fieldMinValue=0,fieldMaxValue=1000,value=1,
                        cw= [1,50],dc = "f_modifyNormalSize()", cc= "f_modifyNormalSize()", cal=[1,"center"])
    cmds.setParent("..")
    cmds.setParent("..")
    cmds.setParent("..")

    # Ediotrs Row 1
    cmds.frameLayout("editorsTools",bgc=grey,l="Editors",collapsable=1,
                    preExpandCommand='f_collapseTurnColor("editorsTools")',
                    preCollapseCommand='f_collapseTurnColor("editorsTools")')
    cmds.gridLayout(numberOfColumns = 3, cellHeight = LDMT_UI_cell_height, cellWidth=LDMT_UI_width/3)
    cmds.button(ann="Open plugin manager.", 
                bgc=darkGrey, l="Plugin", c= 'f_command("Plugin Manager")') 
    cmds.button(ann="Open preference manager.", 
                bgc=darkGrey, l="Preference", c= 'f_command("Preferences Setting")') 
    cmds.button(ann="Open hypergraph window.", 
                bgc=darkGrey, l="Hypergraph", c= 'f_command("Hypergraph Window")') 
    cmds.button(ann="Open node editor.", 
                bgc=darkGrey, l="Node", c= 'f_command("Node Editor")') 
    cmds.button(ann="Open namespace editor.", 
                bgc=darkGrey, l="Namespace", c= 'f_command("Namespace Editor")') 
    cmds.button(ann="Open hotkey editor.", 
                bgc=darkGrey, l="Hotkey", c= 'f_command("Hotkey Editor")') 
    cmds.setParent("..")
    cmds.setParent("..")

    # File Row 1
    cmds.frameLayout("fileTools",bgc=grey,l="File",collapsable=1,
                    preExpandCommand='f_collapseTurnColor("fileTools")',
                    preCollapseCommand='f_collapseTurnColor("fileTools")')
    cmds.gridLayout(numberOfColumns = 2, cellHeight = LDMT_UI_cell_height, cellWidth=LDMT_UI_width/2)
    cmds.button(ann="Open project's folder.", 
                bgc=lightYellow, l="Open Folder", c= 'f_command("Open Folder")') 
    cmds.gridLayout(numberOfColumns = 2, cellHeight = LDMT_UI_cell_height, cellWidth=LDMT_UI_width/4)
    cmds.button(ann="Predefined export.", 
                bgc=darkerGrey, l="Export", c= 'f_command("Predefined Export")') 
    cmds.optionMenu(ann="Choose format to output.",
                bgc=black,changeCommand="print #1")
    cmds.menuItem(l="OBJ")
    cmds.menuItem(l="FBX")
    cmds.menuItem(l="MAX")
    cmds.menuItem(l="UE4")
    cmds.setParent("..")
    cmds.setParent("..")
    cmds.setParent("..")
    
    cmds.frameLayout("infoTools",bgc=grey,l="Info",collapsable=1,
                    preExpandCommand='f_collapseTurnColor("infoTools")',
                    preCollapseCommand='f_collapseTurnColor("infoTools")')
    cmds.gridLayout(numberOfColumns = 2, cellHeight = LDMT_UI_cell_height, cellWidth=LDMT_UI_width/2+1)
    cmds.button(ann="Add LDMT to shelf.", 
                bgc=darkerGrey, l="Add to Shelf", c= 'f_command("Add to Shelf")') 
    cmds.button(ann="Search for commands.", 
                bgc=darkerGrey, l="Command", c= 'f_command("Command Search")') 
    cmds.button(ann="Feedback website.", 
                bgc=darkerGrey, l="Feedback", c= 'f_command("Feedback")') 
    cmds.button(ann="Help website.", 
                bgc=darkerGrey, l="Help Mannul", c= 'f_command("Help Mannual")') 
    cmds.setParent("..")
    cmds.setParent("..")
    cmds.gridLayout(numberOfColumns = 1, cellHeight = LDMT_UI_cell_height, cellWidth=LDMT_UI_width)
    cmds.button(ann="Update.", 
                bgc=darkerGrey, l="Update", c= 'f_command("Update")') 
    cmds.setParent("..")
      
def f_hotkey_init():
    if MAYA_version_float >= 2016:
        hotkeySet = cmds.hotkeySet(q=1,hotkeySetArray=1)
        cmds.hotkeySet(hotkeySet[0],e=1,current=1)

def f_plugin_init():
    cmds.evalDeferred("import rjCMDSearch; rjCMDSearch.install()")
################################ Define Main Functions End ###############################

################################ Define Structured Functions start ###############################

def f_command(command):
    # common window
    if command == "Shader Editor" : mel.eval("HypershadeWindow")
    elif command == "UV Editor" : mel.eval("TextureViewWindow")
    elif command == "Outliner" : mel.eval("OutlinerWindow")
    elif command == "Script Editor": f_outliner_dgc()
    # transform
    elif command == "Mirror X" : f_sourceMel(PATH_LDMT_Func_Mod_transform,"mirrorX")
    elif command == "Mirror Y" : f_sourceMel(PATH_LDMT_Func_Mod_transform,"mirrorY")
    elif command == "Mirror Z" : f_sourceMel(PATH_LDMT_Func_Mod_transform,"mirrorZ")
    elif command == "Reset Pivot" : f_sourceMel(PATH_LDMT_Func_Mod_transform,"resetPivot")
    
    elif command == "Average" : f_sourceMel(PATH_LDMT_Func_Mod_transform,"alignAvg")
    elif command == "Align X" : f_sourceMel(PATH_LDMT_Func_Mod_transform,"alignX")
    elif command == "Align Y" : f_sourceMel(PATH_LDMT_Func_Mod_transform,"alignY")
    elif command == "Align Z" : f_sourceMel(PATH_LDMT_Func_Mod_transform,"alignZ")
    elif command == "Delete History" : f_sourceMel(PATH_LDMT_Func_Mod_transform,"delHistory")

    elif command == "Circularize" : f_circularize()
    elif command == "Insert Mesh" : f_insertMesh()
    elif command == "Turbo Smooth" : f_sourceMel(PATH_LDMT_Func_Mod_transform,"turboSmooth")

    elif command == "Copy to Vertices" : f_copy2Vertex()
    elif command == "Copy to Faces" : f_sourceMel(PATH_LDMT_Func_Mod_transform,"copy2Face")
    elif command == "Rebuild Subdivision" : f_rebuildSubdiv()
    elif command == "Topological Blendshape" : f_topoBlend()
    elif command == "Wrap Retarget" : f_sourceMel(PATH_LDMT_Func_Mod_transform,"wrapRetarget")

    elif command == "Instant Meshes" : f_instantMeshes_exe()
    elif command == "Instant Meshes Function" : f_instantMeshes()

    # select
    elif command == "Select Hard Edges" : f_sourceMel(PATH_LDMT_Func_Mod_select,"selectHardEdge")
    elif command == "Select UV Borders" : f_sourceMel(PATH_LDMT_Func_Mod_select,"selectUVEdgeBorder")
    elif command == "Cam Select": f_toggleCamSelect()
    elif command == "N Edge Selector" : f_selectEveryNEdge()

    # generate
    elif command == "Curve to Ribbon" : f_ribbonGen()
    elif command == "Curve to Tube" : f_tubeGen()
    elif command == "Curve to Rope" : f_ropeGen()
    elif command == "Curve to Braid" : f_braidGen()
    elif command == "Curve to Spiral" : f_spiralGen()

    elif command == "Curve to Instances" : f_instanceGen()
    elif command == "Curve to Seams" : f_seamsEasy("seams")
    elif command == "Curve to Stitches" : f_seamsEasy("stitches")
    elif command == "Clean Instances" : f_sourceMel(PATH_LDMT_Func_Mod_generate,"cleanInstances")
    elif command == "Clean Tubes" : f_sourceMel(PATH_LDMT_Func_Mod_generate,"cleanTubes")

    # uv
    elif command == "Quick UV" : f_sourceMel(PATH_LDMT_Func_Mod_uv,"quickUV")
    elif command == "UV In" : f_sourceMel(PATH_LDMT_Func_Mod_uv, 'moveUVIn')
    elif command == "UV Out" : f_sourceMel(PATH_LDMT_Func_Mod_uv, 'moveUVOut') 
    elif command == "UV Deluxe" : f_UVDeluxe()
    elif command == "Check UV Bleed" : f_sourceMel(PATH_LDMT_Func_Mod_transform,"delHistory") # to be done
    
    # trial
    elif command == "Face Transfer" : f_faceTransfer()
    elif command == "EA LOD" : f_sourceMel(PATH_LDMT_Func_Mod_trial,"lodEA")

    elif command == "Optimize Scene" : mel.eval("OptimizeSceneOptions")
    elif command == "Clean Mesh" : f_sourceMel(PATH_LDMT_Func_Mod_debug,"cleanMesh")
    elif command == "Set Normal to Face" : f_sourceMel(PATH_LDMT_Func_Mod_debug,"cleanNormal")
    elif command == "Keeping HS" : f_keepHS()
    
    elif command == "Batch Rename" : f_sourceMel(PATH_LDMT_Func_Mod_debug,"patternRename")
    elif command == "Delete Namespace" : f_deleteNameSpace()
    elif command == "Ungroup" : f_sourceMel(PATH_LDMT_Func_Mod_debug,"ungroup")
    elif command == "Fix Reverse" : f_sourceMel(PATH_LDMT_Func_Mod_debug,"fixReverse")
    
    elif command == "Display Vert Normal" : cmds.polyOptions(r=1,pt=1,dn=1)
    elif command == "Display Face Normal" : cmds.polyOptions(r=1,f=1,dn=1)
    elif command == "Display Triangle" : mel.eval("TogglePolygonFaceTriangles polyOptions -r -dt 1")
    elif command == "Display TexBord" : mel.eval("ToggleTextureBorderEdges")
    
    elif command == "Display Vert ID" : mel.eval("ToggleVertIDs")
    elif command == "Display Polycount" : mel.eval("TogglePolyCount")
    elif command == "Reset Display" : mel.eval("PolyDisplayReset")
    elif command == "Cleanup Plugins" : f_cleanupPlugin()
    elif command == "Reset Preferences" : f_resetPref()
    
    elif command == "Plugin Manager" : mel.eval("PluginManager")
    elif command == "Preferences Setting" : mel.eval("PreferencesWindow")
    elif command == "Hypergraph Window" : mel.eval("HypergraphDGWindow")
    elif command == "Node Editor" : mel.eval("NodeEditorWindow")
    elif command == "Namespace Editor" : mel.eval("NamespaceEditor")
    elif command == "Hotkey Editor" : mel.eval("HotkeyPreferencesWindow")
    
    elif command == "Open Folder" : f_sourceMel(PATH_LDMT_Func_Mod_debug,"openFolder")
    elif command == "Predefined Export" : f_sourceMel(PATH_LDMT_Func_Mod_transform,"delHistory") # to be done
    
    elif command == "Add to Shelf" : f_sourceMel(PATH_LDMT_Func_Mod_info,"add2Shelf")
    elif command == "Command Search" : f_showSearch()
    elif command == "Feedback" : f_showWebsite('https://github.com/xgits/LD_MayaToolbox')
    elif command == "Help Mannual" : f_showWebsite('http://www.xgits.com')
    elif command == "Update" : f_sourceMel(PATH_LDMT_Func_Mod_info,"update")
    postUsername = USER_name.replace(' ','_',4)
    postCommand = command.replace(' ','_',4)
    postInfo(postUsername,postCommand)
    # finally print feedback
    f_printMessage(command)

def f_sourceMel(melPath,command):
    if mel.eval('exists "'+command+'"'):
        mel.eval(command)
    else:
        message = 'source "' + melPath + '/' + command + '"'
        mel.eval(message)
        mel.eval(command)
        
def f_collapseTurnColor(frameName):
    ifCollapsed = cmds.frameLayout(frameName,q=1,cl=1)
    if ifCollapsed == 1:
        cmds.frameLayout(frameName,e=1,bgc = grey)
    else:
        cmds.frameLayout(frameName,e=1,bgc = darkerGrey)

def f_printMessage(message):
    global PM_startTime
    global PM_timeAdder
    PM_offset = 0
    PM_time = cmds.timerX(startTime = PM_startTime)
    PM_startTime = cmds.timerX()
    if PM_time<1.5:
        PM_offset = 10+20*(PM_timeAdder)
        PM_timeAdder = PM_timeAdder+1 
    else:
        PM_offset = 10
        PM_timeAdder = 0 
    if MAYA_version_float >= 2014:
        cmds.inViewMessage(
        amg = "<span style=\"color:#ffffff\">"+message+"</span>",
        fade = 1, fit = 150, fst = 800, fot = 150, fof = PM_offset, bkc = 0x2288ff, 
        pos = "topCenter", fontSize = 10, a = 0, ta = 0.68)

################################ Define Structured Functions end ###############################

################################ Define Specific Functions Start ###############################

def postInfo(username,function):

    postInfoPath = PATH_LDMT_Func_logging + "/postInfo.py"
    try:
        subprocess.Popen('"'+MAYA_pyLocation+'" '+postInfoPath+' '+username+' '+function,shell=True)
    except:
     subprocess.Popen('python '+postInfoPath+' '+username+' '+function,shell=True)

    
def f_outliner_dgc():
    if  mel.eval('exists charcoalEditor'): mel.eval('charcoalEditor')
    else: mel.eval('ScriptEditor')
    return "Script Editor"

def f_copy2Vertex():
    mods=cmds.getModifiers()
    if mods == 0:
        import copy2VertexPy
        copy2VertexPy.copy2VertexPy()
    else:
        f_sourceMel(PATH_LDMT_Func_Mod_transform,"copy2Vertex")

def f_queryToggleCamSelect():
    IfUsedCamSelect = cmds.selectPref(q=1,useDepth=1)
    if IfUsedCamSelect ==0:
        cmds.button("camSelectButton",e=1,l="Cam Select is Off",bgc=darkerGrey)
    elif IfUsedCamSelect ==1:
        cmds.button("camSelectButton",e=1,l="Cam Select is On",bgc=beige) 
    
def f_toggleCamSelect():
    IfUsedCamSelect = cmds.selectPref(q=1,useDepth=1)
    if IfUsedCamSelect ==1:
        cmds.selectPref(useDepth=0)
        cmds.button("camSelectButton",e=1,l="Cam Select is Off",bgc=darkerGrey)
    elif IfUsedCamSelect ==0:
        cmds.selectPref(useDepth=1)
        cmds.button("camSelectButton",e=1,l="Cam Select is On",bgc=beige)    

def f_modifyNormalSize():
    normalSize = cmds.floatSliderGrp("normalDisplaySize",q=1,v=1)
    cmds.polyOptions( sn=normalSize )

def f_circularize ():
    if mel.eval('exists "CircularizeVtxCmd"'):
        mel.eval("CircularizeVtxCmd")
    else:
        cmds.loadPlugin( PATH_LDMT_Func_Mod_transform + "/CircularizeVtxCmd.py")
        mel.eval("CircularizeVtxCmd")
        
def f_insertMesh():
    mods = cmds.getModifiers()
    pluginPath = PATH_LDMT_plugin+"/duplicateOverSurface.mll"
    if cmds.pluginInfo(pluginPath,q=1,l=1) !=1: 
        cmds.loadPlugin (pluginPath)
    if mods==0:
        cmds.duplicateOverSurface(cmds.ls(sl=True, long=True)[0])
    elif mods==4:
        cmds.duplicateOverSurface(cmds.ls(sl=True, long=True)[0],rotation=False)
        
def f_rebuildSubdiv():
    import rebuildSubdiv
    rebuildSubdiv.rebuildSubdiv()
    
def f_topoBlend():
    import geometryWalker.QT.pickWalker_UI as pickWalker_UI
    pickWalker_UI.pickWalkerUI()
    
def f_instantMeshes_exe():
    sel=cmds.ls(sl=1,o=1)
    if sel == []:
        InstantMeshPath = PATH_LDMT_exe + "/instantMesh.exe"
        subprocess.Popen(InstantMeshPath,False)
    else:
        import instantMesh_exe
        instantMesh_exe.LD_Instamesh()
        
def f_instantMeshes():
    targetCount = cmds.intField("instantMeshes_targetCount",q=1,v=1)
    import instantMesh
    instantMesh.LD_Instamesh(targetCount)
    
def f_selectEveryNEdge():
    mods = cmds.getModifiers()
    if mods==0:
        f_sourceMel(PATH_LDMT_Func_Mod_select,"selectEveryNEdgeTool")
    elif mods==1:
        f_sourceMel(PATH_LDMT_Func_Mod_select,"selectEveryNEdge")
    elif mods==4:
        import patternSelection
        patternSelection.patternSelection()

def f_ribbonGen():
    import ribbonGen
    ribbonGen.ribbonGen()
    f_sourceMel(PATH_LDMT_Func_Mod_debug, "fixReverse")

def f_tubeGen():
    sel = cmds.ls(sl=1)
    import tubeGen
    tubeGen.tubeGen(sel[0])
    f_sourceMel(PATH_LDMT_Func_Mod_debug, "fixReverse")

def f_ropeGen():
    mods = cmds.getModifiers()
    if mods==0:
        pluginPath =PATH_LDMT_plugin + "/curve2spiral.py"
        if cmds.pluginInfo(pluginPath,q=1,l=1) !=1: 
            cmds.loadPlugin (pluginPath)
        f_sourceMel(PATH_LDMT_Func_Mod_generate, "ropeGen")
    elif mods==1:
        pluginPath ="curveWarp"
        if cmds.pluginInfo(pluginPath,q=1,l=1) !=1: 
            cmds.loadPlugin (pluginPath)
        f_sourceMel(PATH_LDMT_Func_Mod_generate, "ropeGen_helix")
        
def f_braidGen():
    sel = cmds.ls(sl=1)
    curveCount = len(sel)
    for i in range(curveCount):
        cmds.select(sel[i],r=1)
        f_sourceMel(PATH_LDMT_Func_Mod_generate, "braidGen")

def f_spiralGen():
    pluginPath =PATH_LDMT_plugin + "/curve2spiral.py"
    if cmds.pluginInfo(pluginPath,q=1,l=1) !=1: 
        cmds.loadPlugin (pluginPath)
    sel = cmds.ls(sl=1)
    curveCount = len(sel)
    for i in range(curveCount):
        cmds.select(sel[i],r=1)
        f_sourceMel(PATH_LDMT_Func_Mod_generate, "braidGen")

def f_instanceGen():
    pluginPath =PATH_LDMT_plugin + "/instanceAlongCurve.py"
    if cmds.pluginInfo (pluginPath,q=1,l=1) !=1: 
        cmds.loadPlugin (pluginPath)
    mel.eval("instanceAlongCurve")

def f_seamsEasy(command):
    if MAYA_version == '2016': pluginPath = PATH_LDMT_plugin + "/seamsEasy_x64_2016.mll"
    elif MAYA_version == '2016.5': pluginPath = PATH_LDMT_plugin + "/seamsEasy_x64_2016.5.mll"
    elif MAYA_version == '2017': pluginPath = PATH_LDMT_plugin + "/seamsEasy_x64_2017.mll"
    elif MAYA_version == '2018': pluginPath = PATH_LDMT_plugin + "/seamsEasy_x64_2018.mll"
    if cmds.pluginInfo(pluginPath,q=1,l=1) !=1: 
        cmds.loadPlugin (pluginPath)
    if command == "seams" : mel.eval("seamsEasy")
    if command == "stitches" : mel.eval("stitchEasy")

def f_UVDeluxe():
    from UVDeluxe import uvdeluxe
    uvdeluxe.createUI()

def f_faceTransfer():
    import faceTransfer.ui
    faceTransfer.ui.show()

def f_keepHS():
    import keepHS
    keepHS.SGtoHS()
    
def f_deleteNameSpace():
    import deleteNamespace
    deleteNamespace.remove_namespaces_from_selection()
def f_cleanupPlugin():
    import cleanupPlugin
    cleanupPlugin.cleanupPlugin()

def f_resetPref():
    import resetPref
    resetPref.resetPref()

def f_showSearch():
    import vt_quicklauncher
    vt_quicklauncher.show()
    
def f_showWebsite(website):
    os.startfile(website)

################################ Define Specific Functions End ###############################

LDMT()



