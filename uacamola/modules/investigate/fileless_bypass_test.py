from module import Module
from support.winreg import Registry
from _winreg import HKEY_CURRENT_USER as HKCU


class CustomModule(Module):
    def __init__(self):
        information = {"Name": "Fileless bypass test",
                       "Description": "This module will write in a registry path, execute a binary and clean the registry",
                       "Author": "Santiago Hernandez Ramos"}

        # -----------name-----default_value--description
        options = {"registry_path": [None, "Registry path to set the value", True],
                   "key_value": [None, "Value for the created path", False],
                   "value_Name": [None, "value name for the registry path. HKCU must not be included.", False],
                   "value_Value": [None, "value for the registry path", False],
                   "binary": [None, "This binary would be executed to test for bypass", True]}

        # Constructor of the parent class
        super(CustomModule, self).__init__(information, options)

    # This module must be always implemented, it is called by the run option
    def run_module(self):
        r = Registry()
        k = r.create_key(HKCU, self.args["registry_path"])
        if self.args["key_value"] is not None:
            r.set_value(
                HKCU, self.args["registry_path"], self.args["key_value"])
        if self.args["value_Name"] is not None:
            r.create_value(k, self.args["value_Name"],
                           self.args["value_Value"])

        print "[*] Executing binary and restoring"
