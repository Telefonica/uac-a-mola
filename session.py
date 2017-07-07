import importlib
from termcolor import colored


class Session(object):

    def __init__(self, path):
        self._module = self.instantiate_module(path[:-3])
        self._path = path

    def header(self):
        return self._path.split("\\")[-1]

    def show(self):
        self.information()
        self.options()

    def information(self):
        info = self._module.get_information()
        print ""
        for key, value in info.iteritems():
            print colored(" %s" % key, 'yellow', attrs=['bold'])
            print ' ' + '-' * len(key)
            print " |_%s\n" % value

    def options(self):
        opts = self._module.get_options_dict()
        print colored("\n Options (Field = Value)", 'yellow', attrs=['bold'])
        print " -----------------------"
        flag = 0
        for key, value in opts.iteritems():
            flag += 1
            # Parameter is mandataroy
            if value[2] is True:
                if str(value[0]) == "None":
                    if flag > 1:
                        print " |"
                    print " |_[" \
                        + colored("REQUIRED", 'yellow', attrs=['bold']) \
                        + "] %s" % key \
                        + " = %s (%s)" % (value[0], value[1])
                else:
                    if flag > 1:
                        print " |"
                    print " |_%s" % key \
                        + " = " \
                        + colored("%s" % value[0], 'green', attrs=['bold']) \
                        + " (% s)" % (value[1])

            # Parameter is optional
            elif value[2] is False:
                if str(value[0]) == "None":
                    if flag > 1:
                        print " |"
                    print " |_[OPTIONAL] %s" % key \
                        + " = %s (%s)" % (value[0], value[1])
                else:
                    if flag > 1:
                        print " |"
                    print " |_%s" % key \
                        + " = " \
                        + colored("%s" % value[0], 'green', attrs=['bold']) \
                        + " (% s)" % (value[1])

        print ""

    def run(self):
        if not(self._module.check_arguments()):
            print colored('[!] REQUIRED ARGUMENTS NOT SET...exiting', 'red', attrs=['bold'])
            return

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
