#--encoding: utf-8--

from module import Module
from support.listener import CustomListener
from multiprocessing.connection import Client


class CustomModule(Module):
    def __init__(self):
        information = {"Name": "This module will instrument the binaries selected and detect possible UAC bypasses",
                       "Description": "Bypass Mitigation",
                       "Author": "Santiago Hernandez Ramos"}

        # -----------name-----default_value--description--required?
        options = {"binlist_file": [None, "File with a list of binaries to hook, one on each line", True],
                   "password": [None, "Password for connection", True],
                   "port" : ['5555', "Port for connection", True]}

        # Constructor of the parent class
        super(CustomModule, self).__init__(information, options)

        # Class atributes, initialization in the run_module method
        # after the user has set the values
        self._option_name = None

    # This module must be always implemented, it is called by the run option
    def run_module(self):
        # Executing the listener
        self.print_info("[+] Executing the listener...\n")
        listener = CustomListener(self.args['password'], int(self.args['port']))
        listener.listen(self.read_file())
        
    def read_file(self):
        with open(self.args['binlist_file']) as f:
            binaries = f.readlines()
        return [b.strip() for b in binaries]
