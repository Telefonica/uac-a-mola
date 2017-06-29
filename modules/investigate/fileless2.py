from module import Module
from modules.investigate.procmon_xml_parser import CustomModule as XML_parser
from support.winreg import Registry
from _winreg import HKEY_CURRENT_USER as HKCU
import subprocess
import psutil


class CustomModule(Module):
    def __init__(self):
        information = {"Name": "Fileless2 discovery",
                       "Description": "This module search a list of binaries for fileless 2 UAC bypasses",
                       "Author": "Santiago Hernandez Ramos"}

        # -----------name-----default_value--description
        options = {"binary": [None, "Target of the UAC fileless bypass search, if None, the module will search for all the binaries in the file"],
                   "xml_file": [None, "Path to a procmon like XML file"]}

        # Constructor of the parent class
        super(CustomModule, self).__init__(information, options)

        # Class atributes, initialization in the run_module method
        # after the user has set the values
        self._xml = None
        self._binary = None
        self._results = []
        self.p = None
        self.events = None
        self.events_nf = None

    # This module must be always implemented, it is called by the run option
    def run_module(self):
        # To access user provided attributes, use self._options dictionary
        self._xml = self.options["xml_file"][0]
        self._binary = self.options["binary"][0]

        self.p = XML_parser()
        # Initializating the options of the module
        self.p.parse_tree(self._xml)

        r = Registry()

        self.events = self.p.events()
        self.events_nf = self.p.events_notfound(self.events)

    def kill(self, proc, last_pids=None, new_pids=None):
        new_pids = self.last_process_created(last_pids, new_pids)
        try:
            for p in new_pids:
                subprocess.check_call(["tskill", str(p)])
        except subprocess.CalledProcessError:
            print "[!!] The process %s can't be killed" % proc
            return

    def last_process_created(self, prev_pids, new_pids):
        pids = []
        for p in new_pids:
            if p not in prev_pids:
                pids.append(p)
        return pids

    def execute(self, proc):
        try:
            subprocess.Popen([proc])
        except subprocess.CalledProcessError as error:
            raise error
        except WindowsError:
            print "[!!] The application can't be executed in win32 mode"
            return

    def is_cmd_open(self):
        try:
            return 'cmd.exe' in [psutil.Process(p).name() for p in psutil.pids()]
        except:
            pass

    def events_nf_openkey(self, proc=None):
        events_nf_hkcu = self.p.events_word("HKCU", self.events_nf)
        return self.p.events_operation("RegOpenKey", events_nf_hkcu)

    def events_nf_queryvalue(self, proc=None):
        events_nf_hkcu = self.p.events_word("HKCU", self.events_nf)
        return self.p.events_operation("RegQueryValue", events_nf_hkcu)

    def get_paths_byword(self, events, intext):
        if intext is not None:
            return [p.text for e in events
                    for p in e.findall('.//Path')
                    if intext in p.text]
        else:
            return self.p.paths(events)
