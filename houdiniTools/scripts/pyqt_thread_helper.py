#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# @Time     : 2019/7/4 18:05
# @Email    : spirit_az@foxmail.com
# @Name     : pyqt_thread_helper.py
__author__ = 'miaochenliang'

# import--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #
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

import threading

use_separate_thread = True

__command_queue = []
__command_queue_lock = threading.RLock()
__command_queue_event = threading.Event()

__pyqt_thread = None


def queueCommand(callable, arguments=()):
    if not use_separate_thread:
        callable(*arguments)
        return

    # start qt thread if it`s not already running
    global __pyqt_thread
    if __pyqt_thread is None:
        __pyqt_thread = threading.Thread(target=__pyQtThreadMain, name='pyqtThread')
        __pyqt_thread.start()

    __command_queue_lock.acquire()
    __command_queue.append((callable, arguments))
    __command_queue_lock.release()

    # signal the pyqt thread to run the task
    __command_queue_event.set()


def __pyQtThreadMain():
    while True:
        # 等待主线程发送信号
        __command_queue_event.wait()

        # 堆栈中移除并重置
        __command_queue_lock.acquire()
        command = __command_queue.pop()
        __command_queue_event.clear()
        __command_queue_lock.release()

        # 执行命令
        command[0].__call__(*command[1])


__pyqt_app = None


def getApplication():
    global __pyqt_app
    if __pyqt_app is None:
        __pyqt_app = QApplication.instance()
    if __pyqt_app is None:
        __pyqt_app = QApplication(['houdini'])

    return __pyqt_app
