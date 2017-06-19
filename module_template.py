from module import Module


class CustomModule(Module):
    def __init__(self):
        information = {"Name": "",
                       "Description": "",
                       "Author": ""}

        # -----------name-----default_value--description
        options = {"option_name": [None, "description"]
                   "option2_name": ["default", "description"]}

        # Constructor of the parent class
        super(CustomModule, self).__init__(information, options)

        # Class atributes, initialization in the run_module method
        # after the user has set the values
        self._option_name = None

    # This module must be always implemented, it is called by the run option
    def run_module(self):
        # To access user provided attributes, use self._options dictionary
        self._option_name = self._options["option_name"][0]
