#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Time      :  14:40
# Email     : spirit_az@foxmail.com
# File      : openUI.py
__author__ = 'ChenLiang.Miao'
# import --+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #
import os
import existsUI as exUI
import scriptTool
reload(exUI)
# function +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #


maya_win = exUI.GetMayaMainWindow()
__abs_path__ = scriptTool.getScriptPath().replace('\\', '/')
main_win_name = 'tool name'
scriptVersion = 'version by author'


def icon_path(in_name):
    # return in_name
    return os.path.join(os.path.dirname(__abs_path__), 'icons', in_name).replace('\\', '/')


def getUIPath():
    return os.path.join(__abs_path__, 'UIName.ui').replace('\\', '/')


# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #
windowClss, baseClass = exUI.loadUi(getUIPath())


# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #

class mainFunc(windowClss, baseClass):
    def __init__(self, parent=maya_win):
        super(mainFunc, self).__init__(parent)
        self.setupUi(self)

        self._bt_clicked()

    def _init_ui(self):
        pass

    def _bt_clicked(self):
        pass


def show():
    exUI.UIExists(main_win_name, AsBool=False) and exUI.deleteUI(main_win_name)

    anim_path = icon_path('waiting.gif')
    splash = exUI.mSplashScreen(anim_path, exUI.Qt.WindowStaysOnTopHint)
    splash.show()
    ui = mainFunc()
    # 设置名称 一定不可以在初始化的时候设置，否则会出问题
    ui.setObjectName(main_win_name)
    ui.setWindowTitle('%s %s' % (main_win_name, scriptVersion))
    splash.showMessage('author : %s' % __author__, exUI.Qt.AlignLeft | exUI.Qt.AlignBottom, exUI.Qt.yellow)
    t = exUI.QElapsedTimer()
    t.start()
    while t.elapsed() < 600:
        exUI.QCoreApplication.processEvents()

    splash.finish(ui)
    ui.show()
