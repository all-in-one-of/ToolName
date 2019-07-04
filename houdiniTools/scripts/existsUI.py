#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# @Time     : 2019/6/27 11:55
# @Email    : spirit_az@foxmail.com
# @Name     : existsUI.py
__author__ = 'miaochenliang'

# import--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #
import hou
import xml
from cStringIO import StringIO

houdiniVersion = int(hou.applicationVersionString().split('.')[0])
USE_PYQT_MODULE = False

if houdiniVersion >= 17:
    try:
        from PyQt5.QtCore import *
        from PyQt5.QtGui import *
        from PyQt5.QtWidgets import *
        from PyQt5 import uic
        from PyQt5 import sip
        from PyQt5.QtCore import pyqtSignal

        USE_PYQT_MODULE = True

    except ImportError:
        from PySide2.QtCore import *
        from PySide2.QtGui import *
        from PySide2.QtWidgets import *
        from PySide2 import shiboken2 as shiboken
        import pyside2uic as uic
        from PySide2.QtCore import Signal as pyqtSignal

        USE_PYQT_MODULE = False
else:
    try:
        from PyQt4.QtCore import *
        from PyQt4.QtGui import *
        from PyQt4 import uic
        from PyQt4 import sip
        from PyQt4.QtCore import pyqtSignal

        USE_PYQT_MODULE = True

    except ImportError:
        from PySide.QtCore import *
        from PySide.QtGui import *
        from PySide.QtWidgets import *
        from PySide import shiboken
        import pysideuic as uic
        from PySide.QtCore import Signal as pyqtSignal

        USE_PYQT_MODULE = False


def unwrapInstance(qObj):
    if USE_PYQT_MODULE:
        return sip.unwrapinstance(qObj)
    else:
        return shiboken.unwrapInstance(qObj)


def getMainWindow():
    """
    get houdini main window
    :return:
    """
    mainWindow = hou.qt.mainWindow()  # type: QWidget
    ptr = pointer(mainWindow)
    return wrapInstance(ptr)


def pointer(widget):
    """

    :param widget: ui name
    :return:
    """
    from PySide2 import shiboken2 as shiboken
    return long(shiboken.getCppPointer(widget)[0])


def wrapInstance(widget):
    if isinstance(widget, basestring):
        widget = hou.ui.findPaneTab(widget)
    if USE_PYQT_MODULE:
        return sip.wrapinstance(long(widget), QObject)
    else:
        return shiboken.wrapInstance(long(widget), QWidget)


def GetQtWidget(QWidgetName, LongName=False):
    RootName = str(getMainWindow().objectName())
    Name = QWidgetName.split('|')[-1]
    for w in QApplication.topLevelWidgets():
        try:
            if w.objectName() == Name:
                if LongName:
                    return w, '|' + '|'.join([RootName, QWidgetName])
                else:
                    return w
        except:
            pass

    try:
        for w in QApplication.topLevelWidgets():
            for c in w.children():
                if c.objectName() == Name:
                    if LongName:
                        return c, '|' + '|'.join([str(w.objectName()), str(c.objectName())])
                    else:
                        return c

    except:
        pass


def UIExists(Name, AsBool=True):
    """
    UI是否已经生成
    :param Name:  窗口名称
    :param AsBool:
    :return:
    """
    QObject = GetQtWidget(Name)
    if QObject:
        if AsBool:
            return bool(QObject)
        return QObject
    elif AsBool:
        return False
    else:
        return None


def Raise(Name):
    """
    UI 是否已经生成
    :param Name: 窗口名称
    :return:
    """
    qobject = GetQtWidget(Name)
    if qobject:
        return qobject
    else:
        return False


def deleteUI(Name):
    """
    根据名字彻底清除删除UI
    :param Name:
    :return:
    """
    qObject = GetQtWidget(Name)
    qObject.setParent(None)
    if USE_PYQT_MODULE:
        sip.delete(qObject)
    else:
        shiboken.delete(qObject)


def loadUi(uiPath):
    """
    read an ui file, get two classes to return..
    """
    if USE_PYQT_MODULE:
        form_class, base_class = __pyqtLoadUi(uiPath)
    else:
        form_class, base_class = __pysideLoadUi(uiPath)
    return form_class, base_class


def __pyqtLoadUi(uiPath):
    """
    read an ui file, use PyQt4 method get two classes to return..
    """
    return uic.loadUiType(uiPath)


def __pysideLoadUi(uiPath):
    """
    read an ui file, use PySide method get two classes to return..
    """
    parsed = xml.etree.ElementTree.parse(uiPath)
    widget_class = parsed.find('widget').get('class')
    form_class = parsed.find('class').text

    with open(uiPath, 'r') as f:
        o = StringIO()
        frame = dict()

        uic.compileUi(f, o, indent=0)

        pyc = compile(o.getvalue(), '<string>', 'exec')
        exec pyc in frame

        form_class = frame['Ui_%s' % form_class]
        base_class = eval(widget_class)

    return form_class, base_class


# start gif --+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+--#

class mSplashScreen(QSplashScreen):
    def __init__(self, animation, flag):
        super(mSplashScreen, self).__init__(QPixmap(), flag)
        self.movie = QMovie(animation)
        # self.movie.setParent(self)
        self.movie.frameChanged.connect(self.onNextFrame)

    def onNextFrame(self):
        pixmap = self.movie.currentPixmap()
        self.setPixmap(pixmap)
        self.setMask(pixmap.mask())

    def showEvent(self, *args):
        self.movie.start()

    def finish(self, widget):
        widget.show()
        super(mSplashScreen, self).finish(widget)
        # deleteUI(self.movie.objectName())
        # deleteUI(self.objectName())


class mSplashScreen_new(QSplashScreen):
    """
    start movie once
    """

    def __init__(self, animation, flag, widget):
        super(mSplashScreen_new, self).__init__(QPixmap(), flag)
        self.movie = QMovie(animation)
        self.movie.setParent(self)
        self.movie.frameChanged.connect(self.onNextFrame)
        self.count = self.movie.frameCount()
        self.step = 0
        self.widget = widget

    def onNextFrame(self):
        if self.step < self.count:
            pixmap = self.movie.currentPixmap()
            self.setPixmap(pixmap)
            self.setMask(pixmap.mask())
            self.step += 1
        else:
            self.finish(self.widget)

    def showEvent(self, *args):
        self.movie.start()

    def finish(self, widget):
        widget.show()
        deleteUI(self.movie)
        deleteUI(self)

