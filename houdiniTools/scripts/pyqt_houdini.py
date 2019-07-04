#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# @Time     : 2019/7/3 18:58
# @Email    : spirit_az@foxmail.com
# @Name     : pyqt_houdini.py
__author__ = 'miaochenliang'

# import--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #
import re
import hou
import existsUI as exUI

houdiniVersion = exUI.houdiniVersion

if houdiniVersion >= 17:
    from PyQt5.QtCore import *
    from PyQt5.QtGui import *
    from PyQt5.QtWidgets import *
    from PyQt5 import uic
    from PyQt5 import sip
    from PyQt5.QtCore import pyqtSignal

else:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *
    from PyQt4 import uic
    from PyQt4 import sip
    from PyQt4.QtCore import pyqtSignal


# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #
class integrateEventLoop(object):
    def __init__(self, applicate, dialogs):
        self.applicate = applicate  # type: QApplication()
        self.dialogs = dialogs
        self.event_loop = QEventLoop()

    def exec_(self):
        hou.ui.addEventLoopCallback(self.processEvents)

    def processEvents(self):
        if not anyQtWindowAreOpen():
            hou.ui.removeEventLoopCallback(self.processEvents)

        self.event_loop.processEvents()
        self.applicate.sendPostedEvents(None, 0)


def anyQtWindowAreOpen():
    return any(w.isVisible() for w in QApplication.topLevelWidgets())


def exec_(application, *args):
    integrateEventLoop(application, args).exec_()


def execSynchronously(application, *args):
    exec_(application, *args)
    hou.ui.waitUntil(lambda: not anyQtWindowAreOpen())
