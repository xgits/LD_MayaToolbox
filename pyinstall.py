import os 
import shutil
import getpass
currentPath = os.getcwd()
username = getpass.getuser()
targetPath = 'c:/Users/'+username+'/Documents/maya/scripts/LD_MayaToolbox'

for src_dir, dirs, files in os.walk(currentPath):
    dst_dir = src_dir.replace(currentPath, targetPath, 1)
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
    for file_ in files:
        src_file = os.path.join(src_dir, file_)
        dst_file = os.path.join(dst_dir, file_)
        if os.path.exists(dst_file):
            os.remove(dst_file)
        shutil.copy(src_file, dst_dir)