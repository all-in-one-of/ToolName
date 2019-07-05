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

houdini_win = exUI.getMainWindow()
__abs_path__ = scriptTool.getScriptPath().replace('\\', '/')
main_win_name = 'tool name'
scriptVersion = 'version by author'


def icon_path(in_name):
    # return in_name
    return os.path.join(os.path.dirname(__abs_path__), 'icons', in_name).replace('\\', '/')


def getUIPath():
    return os.path.join(__abs_path__, 'UI/ui_pipelineTools.ui').replace('\\', '/')


# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #
windowClss, baseClass = exUI.loadUi(getUIPath())


# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #

class mainFunc(windowClss, baseClass):
    def __init__(self, parent=houdini_win):
        super(mainFunc, self).__init__(parent)
        self.setupUi(self)

        self._bt_clicked()

    def _init_ui(self):
        pass

    def _bt_clicked(self):
        pass


def show():
    app = None
    if exUI.USE_PYQT_MODULE:
        import pyqt_thread_helper
        app = pyqt_thread_helper.getApplication()

    exUI.UIExists(main_win_name, AsBool=False) and exUI.deleteUI(main_win_name)
    anim_path = icon_path('waiting.gif')
    splash = exUI.mSplashScreen(anim_path, exUI.Qt.WindowStaysOnTopHint)
    splash.setParent(houdini_win)
    splash.show()
    ui = mainFunc()  # type: exUI.QMainWindow
    # 设置名称 一定不可以在初始化的时候设置，否则会出问题
    ui.setObjectName(main_win_name)
    ui.setWindowTitle('%s %s' % (main_win_name, scriptVersion))
    ui.setWindowIcon(exUI.QIcon(icon_path('MCL.png')))
    splash.showMessage('author : %s' % __author__, exUI.Qt.AlignLeft | exUI.Qt.AlignBottom, exUI.Qt.yellow)
    t = exUI.QElapsedTimer()
    t.start()
    while t.elapsed() < 600:
        exUI.QCoreApplication.processEvents()
    splash.finish(ui)

    if app:
        import pyqt_houdini
        pyqt_houdini.exec_(app, splash, ui)