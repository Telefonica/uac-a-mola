class Module(object):
    def __init__(self, information, options):
        self._information = information
        self.options = options

    def get_information(self):
        return self._information

    def set_option(self, name, value):
        self.options[name][0] = value

    def get_option(self, name):
        return self.options[name][0]

    def get_options_dict(self):
        return self.options

    def get_options_names(self):
        return self.options.keys()

    def run_module(self):
        raise Exception(
            'ERROR: run_module method must be implemented in the child class')
