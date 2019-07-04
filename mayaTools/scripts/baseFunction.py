#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Time      :  14:33
# Email     : spirit_az@foxmail.com
# File      : baseFunctions.py
__author__ = 'ChenLiang.Miao'

# import --+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #

import _winreg
import ctypes
import getpass
import os
import platform
import re
import shutil
import time


# function +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #

# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #

def isSubString(subString, Str):
    flag = True
    for substr in subString:
        if substr not in Str:
            flag = False
    return flag


def GetFileList(FindPath, flagStr):
    fileList = []
    fileNames = os.listdir(FindPath)
    if len(fileNames):
        for fn in fileNames:
            if len(flagStr):
                if isSubString(flagStr, fn):
                    fullFileName = os.path.join(FindPath, fn).replace('\\', '/')
                    fileList.append(fullFileName)
            else:
                fullFileName = os.path.join(FindPath, fn).replace('\\', '/')
                fileList.append(fullFileName)
    if len(fileList):
        fileList.sort()
    return fileList


def getListFlag(FindPath, flagStr):
    fileList = []
    fileNames = getListDir(FindPath, 'file')
    if len(fileNames):
        for fn in fileNames:
            if len(flagStr):
                if os.path.splitext(fn)[-1] == flagStr:
                    fileList.append(fn)
            else:
                fileList.append(fn)
    if len(fileList):
        fileList.sort()
    return fileList


def getListDirK(filepath, mothon, keyword):
    fileList = getListDir(filepath, mothon)
    for each in fileList:
        if re.findall(keyword, each):
            yield each


def getListDir(filepath, mothon):
    if not os.path.exists(filepath):
        return []
    dirs = os.listdir(filepath)
    fileList = []
    for each in dirs:
        if mothon == 'dir' and os.path.isdir(os.path.join(filepath, each)):
            fileList.append(each)

        elif mothon == 'file' and os.path.isfile(os.path.join(filepath, each)):
            fileList.append(each)

    if len(fileList):
        fileList.sort()
    return fileList


def copyFiles(sourceDir, targetDir):
    """
    Copy all files in a directory to a specified directory
    :param sourceDir: 
    :param targetDir: 
    :return: 
    """
    if sourceDir.find(".svn") > 0:
        return
    for f in os.listdir(sourceDir):
        sourceFile = os.path.join(sourceDir, f)
        targetFile = os.path.join(targetDir, f)
        if os.path.isfile(sourceFile):
            if not os.path.exists(targetDir):
                os.makedirs(targetDir)
            if not os.path.exists(targetFile) or (
                    os.path.exists(targetFile) and (
                    time.gmtime(os.path.getmtime(targetFile)) != time.gmtime(
                os.path.getmtime(sourceFile)))):
                try:
                    with open(targetFile, "wb") as f:
                        with open(sourceFile, "rb") as o_f:
                            f.write(o_f.read())
                except:
                    pass
        if os.path.isdir(sourceFile):
            copyFiles(sourceFile, targetFile)


def removeFileInFirstDir(targetDir):
    """
    Delete all files in the first level directory
    :param targetDir:
    :return:
    """
    for file in os.listdir(targetDir):
        targetFile = os.path.join(targetDir, file)
        if os.path.isfile(targetFile):
            os.remove(targetFile)


def remove_dir(dir):
    """

    :param dir:
    :return:
    """
    shutil.rmtree(dir)


def coverFiles(sourceDir, targetDir):
    """
    Copy all files in the first level directory to the specified directory
    :param sourceDir:
    :param targetDir:
    :return:
    """

    for file in os.listdir(sourceDir):
        sourceFile = os.path.join(sourceDir, file)
        targetFile = os.path.join(targetDir, file)
        # cover the files
        if os.path.isfile(sourceFile):
            try:
                with open(targetFile, "wb") as f:
                    with open(sourceFile, "rb") as o_f:
                        f.write(o_f.read())
            except:
                pass


def moveFileto(sourceDir, targetDir):
    """
    Copy the specified file to the directory
    :param sourceDir:
    :param targetDir:
    :return:
    """
    shutil.copy(sourceDir, targetDir)


def writeVersionInfo(targetDir):
    """
    往指定目录写文本文件
    :param targetDir:
    :return:
    """
    open(targetDir, "wb").write("Revison:")


# system command +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #

def copyText(text):
    os.popen(text)


def open_sys(in_path):
    os.system('start %s' % in_path)


# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #

def listDel(lists):
    if not lists:
        return []
    newlist = []
    for each in lists:
        each in newlist or newlist.append(each)
    return newlist


def get_new_ver(in_path):
    os.path.exists(in_path) or os.makedirs(in_path)
    vers = sorted(getListDirK(in_path, 'dir', '^v\d{3}$'), key=lambda x: re.findall('^\d{3}$', x)[0])[0]
    return get_new_version(vers)


def get_new_version(new_ver):
    if not new_ver:
        return 'v001'

    new_ver = 'v%s' % (int(new_ver[1:]) + 1)

    while len(new_ver) < 4:
        new_ver = new_ver.replace('v', 'v0')

    return new_ver


# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #

def get_all_exe():
    sub_key = [r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall',
               r'SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall']

    software_name = []

    for i in sub_key:
        key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, i, 0, _winreg.KEY_ALL_ACCESS)
        for j in range(0, _winreg.QueryInfoKey(key)[0] - 1):
            try:
                key_name = _winreg.EnumKey(key, j)
                key_path = i + '\\' + key_name
                each_key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, key_path, 0, _winreg.KEY_ALL_ACCESS)
                DisplayName, REG_SZ = _winreg.QueryValueEx(each_key, 'DisplayName')
                DisplayName = DisplayName.encode('utf-8')
                software_name.append(DisplayName)
            except WindowsError:
                pass

    software_name = sorted(set(software_name))
    return software_name


# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #

def get_time():
    return str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))


def get_author():
    return getpass.getuser()


# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #

def s_time(func):
    def wrapper(*args):
        s = time.clock()
        func(*args)
        e = time.clock()
        print 'time consuming: ', e - s

    return wrapper


def getFreeSpaceMByte(folder):
    """
    Get the remaining space on the disk
    :param folder: The folder to query
    :return: M
    """
    if platform.system() == 'Windows':
        free_bytes = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(folder), None, None, ctypes.pointer(free_bytes))
        return free_bytes.value * 1.0 / (1024 * 1024)

    else:
        st = os.statvfs(folder)
        return st.f_bavail * st.f_frsize * 1.0 / (1024 * 1024)
