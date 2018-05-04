import subprocess
import getpass
import tempfile
import os
import maya.cmds as cmds

# Replace this with UI / config file
username = getpass.getuser()
inst_mesh_path = "c:/Users/"+username+"/Documents/maya/scripts/LD_MayaToolbox/exe/instantMesh.exe"
def LD_Instamesh(face_count=None):
    if not os.path.exists(inst_mesh_path):
        cmds.warning('Instant Mesh path not found!')
        return

    # Get current selection
    sel_obj = cmds.ls(sl=True)

    if sel_obj:
        print 'Processing Instant Mesh...'
        # if no polycount set just double the amount of the source object
        if not face_count:
            face_count = int(cmds.polyEvaluate(sel_obj, f=True))
            face_count *= 2
        face_count /= 2
        # Create temp file for OBJ export
        temp = tempfile.NamedTemporaryFile(prefix='instantMesh_', suffix='.obj', delete=False)
        temp_path = temp.name

        # Save the currently selected object as an OBJ
        cmds.file(temp_path, force=True, exportSelected=True, type="OBJ")

        # run instamesh command on the OBJ
        print temp_path

        print "Instant Mesh start"
        some_command = inst_mesh_path + " " + temp_path
        p = subprocess.Popen(some_command, False)
        temp.close()

    else:
        cmds.warning('No objects selected...')