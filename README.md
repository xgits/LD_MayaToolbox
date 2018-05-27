
# Wiki
    [Documents 说明文档](https://github.com/xgits/LD_MayaToolbox/wiki/)

# About LD MayaToolbox
    This is a maya toolbox written by Liu Dian. Gathered many useful script and plugins written by me or open sourced.

    There are currently two version of this tool:
    
    1. First one is free on this github, only agreement is that you will upload information to my website so I can
    keep track of this tool and improve it to be better. This tool will gather your computer username and the count
    of clicks. The information will be used and only be used for improve this tool. 

    2. Second option is to buy a pro version on gumroad:  the pro version has a few functions with bonus performance. 
    If you have concerns about upload your information or just being kind to me, you can buy this version of toolbox. 

    Free to use both version for commercial or personal use.
<html><script src="https://gumroad.com/js/gumroad.js"></script><a class="gumroad-button" href="https://gum.co/xgits">Gumroad Link</a>
</html>
# Installation:

    Download ZIP or clone the source project and then:

    First method: auto install (recommended): If your scripts folder is in C:\ , Just double click LDMT_install.bat 
    inside the folder, you are good to go. Start maya it will autoload.Special case: If your scripts folder 
    (like C:\Users\%username%\Documents\maya\scripts\) is customized to another directory, please open customPath.txt
    and replace content in it to your path, and double click customInstall.bat.

    Second method: mannual install: Manually rename the unzipped folder and rename it to LD_MayaToolbox, copy 
    LD_MayaToolbox folder to C:\Users\%username%\Documents\maya\scripts\ and copy the userSetup.py in LD_MayaToolbox 
    to (scripts folder like  C:\Users\%username%\Documents\maya\scripts\) as well if you want to load on startup.

    If you choose to not autoload this tool, open maya and copy and paste it in script editor as python, run it or add 
    this script to shelf by middle click and drag.

    ```python
    import maya.cmds as cmds 
    import maya.mel as mel
    import sys
    PATH_MAYA_app_dir = mel.eval("getenv MAYA_APP_DIR")
    sys.path.append(PATH_MAYA_app_dir+'/scripts/LD_MayaToolbox')
    cmds.evalDeferred("from LDMT import *")
    cmds.evalDeferred("LDMT()") 
    ```

# 简介 LD MayaToolbox
    这是一个 maya 工具箱, 集成了众多本人原创和开源的maya脚本插件.

    本工具有两个版本:
    
    1.其一是github上的这个版本, 唯一需要同意的是上传你的实用信息到我的个人网站, 这样我可以改进这个工具. 这个工具会上传的信息
    仅包括计算机用户名以及按钮点击次数. 这些信息仅会被用于改善工具.

    2.其二是gumroad上的版本, 专业版有部分功能效率更高且可以选择是否上传数据.如果你对上传使用信息有顾虑或者出于鼓励, 请购买专业版.
    两个版本都可用于商业和个人使用.
<script src="https://gumroad.com/js/gumroad.js"></script><a class="gumroad-button" href="https://gum.co/xgits">Gumroad Link</a>

# 安装方法:
    下载ZIP压缩包, 或者github项目, 然后:

    第一种 自动安装 (推荐): 直接双击 LDMT_install.bat, 启动maya 就会自动启动本工具. 
                          特殊情况: 如果你的C:\Users\%username%\Documents\maya\scripts\ 文件夹不在这个地址, 
                          请打开customPath.txt, 然后把里面的地址替换成你的脚本地址, 点击customInstall即可安装.
                    

    第二种 手动安装: 下载压缩包, 解压缩后重命名为 LD_MayaToolobx ,将LD_MayaToolbox复制到    
    C:\Users\%username%\Documents\maya\scripts\. 然后将LD_MayaToolbox里的userSetup.py复制到
    C:\Users\%username%\Documents\maya\scripts\, 如果你需要自动启动.
        
    如果你选择不自动启动, 打开maya之后请输入以下 python代码 中键拖到工具架, 作为按钮启动:
    ```python
    import maya.cmds as cmds 
    import maya.mel as mel
    import sys
    PATH_MAYA_app_dir = mel.eval("getenv MAYA_APP_DIR")
    sys.path.append(PATH_MAYA_app_dir+'/scripts/LD_MayaToolbox')
    cmds.evalDeferred("from LDMT import *")
    cmds.evalDeferred("LDMT()") 
    ```
If you want to support me or this project, please donate to :

Paypal:

[![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](http://paypal.me/xgits)

Alipay 支付宝

![](http://www.xgits.com:8181/uploads/201805/resume/attach_15300a3ac989111e.png)
