import os 
def deleteFileWithFormat(targetFolder, targetFormat):
    for root,dirs,files in os.walk(targetFolder):
        for file in files:
            filePath = os.path.join(root,file)
            if filePath.endswith(targetFormat):
                os.remove(filePath)
def run():
    getCurrentFolder = os.getcwd()
    targetFolder = getCurrentFolder[:-9]
    deleteFileWithFormat(targetFolder,'pyc')

if __name__ == "__main__":
    run()