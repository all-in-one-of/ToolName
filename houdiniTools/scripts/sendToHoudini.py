#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# @Time     : 2019/6/27 16:04
# @Email    : spirit_az@foxmail.com
# @Name     : sendToHoudini.py
__author__ = 'miaochenliang'

"""
copy to houdini:
import hrpyc
hrpyc.start_server(port = 8701)


"""
# import--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #
import hrpyc


# function --+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #
def run(port = 8701):
    connect, hou = hrpyc.import_remote_module(port = port)
    return connect, hou


import sys

in_path = 'E:/../python/toolModule/houdiniTools'

in_path in sys.path or sys.path.insert(0, in_path)
from houdiniTools.scripts import openUI
reload(openUI)
openUI.show()
