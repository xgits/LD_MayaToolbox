import maya.cmds as cmds
import random
curves = cmds.ls(sl=1,o=1)
moveRange = 1
for i in curves:
    spans = cmds.getAttr(i+'.spans')
    print spans
    for index in range(spans):
        cv = i +'.cv['+str(index+1)+']'
        randomX = (random.random()-0.5)*moveRange
        randomY = (random.random()-0.5)*moveRange
        randomZ = (random.random()-0.5)*moveRange
        cmds.move( randomX,randomY,randomZ,cv,r=1)