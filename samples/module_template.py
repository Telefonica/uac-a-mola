#--encoding: utf-8--

from module import Module


class CustomModule(Module):
    def __init__(self):
        information = {"Name": "",
                       "Description": "",
                       "Author": ""}

        # -----------name-----default_value--description--required?
        options = {"option_name": [None, "description", True],
                   "option2_name": ["default", "description", False]}

        # Constructor of the parent class
        super(CustomModule, self).__init__(information, options)

        # Class atributes, initialization in the run_module method
        # after the user has set the values
        self._option_name = None

    # This module must be always implemented, it is called by the run option
    def run_module(self):
        # To access user provided attributes, use self._args dictionary
        self.args["option_name"]
        self.args["option2_name"]
