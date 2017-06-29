import importlib
from termcolor import colored


class Session(object):

    def __init__(self, path):
        self._module = self.instantiate_module(path[:-3])
        self._path = path

    def header(self):
        return self._path + '> '

    def show(self):
        self.information()
        self.options()

    def information(self):
        info = self._module.get_information()
        print ""
        for key, value in info.iteritems():
            print ' ' + '-' * len(key)
            print " %s" % key
            print ' ' + '-' * len(key)
            print " => %s\n" % value

    def options(self):
        opts = self._module.get_options_dict()
        print " -----------------------"
        print " Options (Field = Value)"
        print " -----------------------"
        for key, value in opts.iteritems():

            if str(value[0]) == "None":
                print colored(" %s" % key, 'red', attrs=['bold']) \
                    + " = %s (%s)\n" % (value[0], value[1])
            else:
                print colored(" %s" % key, 'red', attrs=['bold']) \
                    + " = " \
                    + colored("%s" % value[0], 'green', attrs=['bold']) \
                    + " (% s)\n" % (value[1])

        print ""

    def run(self):
        print colored('[+] Running module...', 'green', attrs=['bold'])
        try:
            self._module.run_module()
        except Exception as error:
            print colored('[!] Error running the module:', 'red', attrs=['bold'])
            print colored("  => " + str(error), 'red', attrs=['bold'])
        print colored('[+] Module exited', 'green', attrs=['bold'])

    def set(self, name, value):
        if name not in self._module.get_options_names():
            print colored('[!] Field not found', 'red', attrs=['bold'])
            return
        self._module.set_value(name, value)

    def instantiate_module(self, path):
        try:
            print '[+] Loading module...'
            m = importlib.import_module(path.replace('\\', '.'))
            print colored('[+] Module loaded!', 'green', attrs=['bold'])
            return m.CustomModule()
        except ImportError as error:
            print colored('[!] Error importing the module:', 'red', attrs=['bold'])
            print colored("  =>" + str(error), 'red', attrs=['bold'])
            return None

    def correct_module(self):
        if self._module is None:
            return False
        return True
