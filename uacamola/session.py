import importlib
from termcolor import colored
from support.brush import Brush
import sys


class Session(object):

    def __init__(self, path):
        self.brush = Brush()
        self._module = self.instantiate_module(self.import_path(path))
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
            self.brush.color(" %s\n" % key, 'YELLOW')
            print ' ' + '-' * len(key)
            print " |_%s\n" % value

    def options(self):
        opts = self._module.get_options_dict()
        self.brush.color("\n Options (Field = Value)\n", 'YELLOW')
        print " -----------------------"
        flag = 0
        for key, value in opts.iteritems():
            flag += 1
            # Parameter is mandataroy
            if value[2] is True:
                if str(value[0]) == "None":
                    if flag > 1:
                        print " |"
                    sys.stdout.write(" |_[")
                    self.brush.color("REQUIRED", 'RED')
                    sys.stdout.write("] %s" % key)
                    sys.stdout.write(" = %s (%s)\n" % (value[0], value[1]))
                else:
                    if flag > 1:
                        print " |"
                    sys.stdout.write(" |_%s" % key)
                    sys.stdout.write(" = ")
                    self.brush.color("%s" % value[0], 'GREEN')
                    sys.stdout.write(" (% s)\n" % (value[1]))

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
                    sys.stdout.write(" |_%s" % key)
                    sys.stdout.write(" = ")
                    self.brush.color("%s" % value[0], 'GREEN')
                    sys.stdout.write(" (% s)\n" % (value[1]))

        print "\n"

    def run(self):
        if not(self._module.check_arguments()):
            self.brush.color('[!] REQUIRED ARGUMENTS NOT SET...exiting\n', 'RED')
            return

        self.brush.color('[+] Running module...\n', 'GREEN')
        try:
            self._module.run_module()
        except KeyboardInterrupt:
            self.brush.color('[!] Exiting the module...\n', 'RED')
        except Exception as error:
            self.brush.color('[!] Error running the module:\n', 'RED')
            self.brush.color("  => " + str(error), 'RED')
            self.brush.color('\n[+] Module exited\n', 'GREEN')
        except IndentationError as error:
            self.brush.color('[!] Error running the module:\n', 'RED')
            self.brush.color("  => " + str(error), 'RED')
            self.brush.color('\n[+] Module exited\n', 'GREEN')
 
    def set(self, name, value):
        if name not in self._module.get_options_names():
            self.brush.color('[!] Field not found\n', 'RED')
            return
        self._module.set_value(name, value)

    def instantiate_module(self, path):
        try:
            print '[+] Loading module...'
            m = importlib.import_module(path)
            self.brush.color('[+] Module loaded!\n', 'GREEN')
            return m.CustomModule()
        except ImportError as error:
            self.brush.color('[!] Error importing the module:\n', 'RED')
            self.brush.color("  => " + str(error), 'RED')
            print ""
            return None

    def correct_module(self):
        if self._module is None:
            return False
        return True

    def import_path(self, path):
        path = path.split('\\')
        path = path[path.index('modules'):]
        return ".".join(path)[:-3]

    def get_options(self):
        return ['set ' + key for key, value in self._module.get_options_dict().iteritems()]
