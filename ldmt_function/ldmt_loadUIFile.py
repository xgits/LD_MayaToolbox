#import shiboken
import maya.OpenMayaUI as omui
try:
  from PySide2.QtCore import * 
  from PySide2.QtGui import * 
  from PySide2.QtWidgets import *
  from PySide2 import __version__
  from pyside2uic import *
  from shiboken2 import wrapInstance 
except ImportError:
  from PySide.QtCore import * 
  from PySide.QtGui import * 
  from PySide import __version__
  from pysideuic import *
  from shiboken import wrapInstance 
from cStringIO import StringIO
import xml.etree.ElementTree as xml

def get_maya_window():

    ptr = omui.MQtUtil.mainWindow()
    #if ptr is not None:
    return wrapInstance(long(ptr), QMainWindow)

def load_ui_type(ui_file):

    parsed = xml.parse(ui_file)
    widget_class = parsed.find('widget').get('class')
    form_class = parsed.find('class').text
    
    with open(ui_file,'r') as f:
        o = StringIO()
        frame = {}

        compileUi(f, o, indent = 0)
        print o.getvalue()
        pyc = compile(o.getvalue(), '<string>', 'exec')
        exec pyc in frame

    
        # Fetch the base_class and form class based on their type in the xml from design
        form_class = frame['Ui_{0}'.format(form_class)]
        base_class = eval('{0}'.format(widget_class))

    return form_class, base_class