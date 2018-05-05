# LD_MayaToolbox
This is a maya toolbox written by Liu Dian.

There are currently two version of this tool:
    
    1. First one is free on this github, only agreement is that you will upload information to my website so I can
    keep track of this tool and improve it to be better. This tool will gather your computer username and the count
    of clicks. The information will be used and only be used for improve this tool. 

    2. Second option is to buy a pro version on gumroad here:  the pro version has a few bonus functions on 
    customizing your UI. If you have concerns about upload your information or just being kind to me, please pay for 
    the pro version toolbox. 

    Free to use both version for commercial or personal use.

Installation:
    
    A. Just double click LDMT_install.bat, you are good to go.

    B. Mannually copy LD_MayaToolbox to C:\Users\% your user name %\Documents\maya\scripts\

        Then type in python scripts below line by line:

        import maya.cmds as cmds 
        import getpass
        import sys
        username = getpass.getuser()
        sys.path.append('c:/Users/'+username+'/Documents/maya/scripts/LD_MayaToolbox')
        cmds.evalDeferred("from LDMT import *")
        cmds.evalDeferred("LDMT()") 
        
本工具有两个版本:
    
    1.其一是github上的这个版本, 唯一需要同意的是上传你的实用信息到我的个人网站, 这样我可以改进这个工具. 这个工具会上传的信息
    仅包括计算机用户名以及按钮点击次数. 这些信息仅会被用于改善工具.

    2.其二是gumroad上的版本, 专业版有一些自定义UI的功能. 如果你对上传使用信息有顾虑或者仅仅是出于善意帮助我, 请购买专业版.

    两个版本都可免费用于商业和个人使用.

安装方法:

    A. 双击 LDMT_install.bat 

    B. 下载压缩包, 解压缩后把 LD_MayaToolbox 整个文件夹复制到 C:\Users\%username%\Documents\maya\scripts\
        然后输入下列python代码 作为按钮启动:
        ```python
        import maya.cmds as cmds 
        import getpass
        import sys
        username = getpass.getuser()
        sys.path.append('c:/Users/'+username+'/Documents/maya/scripts/LD_MayaToolbox')
        cmds.evalDeferred("from LDMT import *")
        cmds.evalDeferred("LDMT()") ```
