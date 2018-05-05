import subprocess
import getpass
import tempfile
import os
import maya.cmds as cmds

# Replace this with UI / config file
PATH_MAYA_app_dir = mel.eval("getenv MAYA_APP_DIR")
inst_mesh_path = PATH_MAYA_app_dir+"/scripts/LD_MayaToolbox/exe/instantMesh.exe"

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
        some_command = inst_mesh_path + " " + temp_path + " -o " + temp_path + " -f " + str(face_count) + " -D" + " -b"
        p = subprocess.Popen(some_command, stdout=subprocess.PIPE, shell=True)
        p.communicate()
        p.wait()
        print "Instant Mesh end"
        print some_command

        # import back the temp OBJ file
        returnedNodes = cmds.file(temp_path,
                                  i=True,
                                  type="OBJ",
                                  rnn=True,
                                  ignoreVersion=True,
                                  options="mo=0",
                                  loadReferenceDepth="all")
        # delete the temp file
        temp.close()
        # Select the imported nodes
        if returnedNodes:
            cmds.select(returnedNodes, r=True)

        print 'Instant Mesh done...'

    else:
        cmds.warning('No objects selected...')


