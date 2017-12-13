from multiprocessing.connection import Listener
from multiprocessing import Process
from winreg import *
import admin
import os
from _winreg import HKEY_CURRENT_USER as HKCU
from _winreg import HKEY_LOCAL_MACHINE as HKLM
from support.brush import Brush
import ctypes


class CustomListener:

    DEBUG_KEY = "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Image File Execution Options\\"

    def __init__(self, password, port):
        self.password = password
        self.port = port
        self.agents_path = self.agents_path()
        self.brush = Brush()

    def agents_path(self):
        dirpath = os.path.dirname(os.path.realpath(__file__))
        return str(dirpath) + "\\agents\\"

    def listen(self, binlist):
        """
        Listen for the execution of a list of
        binaries
        """
        if binlist is None or binlist == []:
            print "Empty list of binaries"
            return
        # This module must be executed as administrator
        if not admin.isUserAdmin():
            admin.runAsAdmin()
        registry = Registry()
        self.add_debugger(registry, binlist)
        try:
            while True:
                listener = Process(target=self._listen, args=())
                listener.start()
                listener.join()
        except:
            self.del_debugger(registry, binlist)
            return

    def _listen(self):
        """ Listen for information from a client and performs
        actions related to the windows registry """
        registry = Registry()
        listener = Listener(('localhost', self.port), authkey=self.password)
        conn = listener.accept()
        msg = conn.recv()
        if type(msg) is list and len(msg) == 2:
            # Deleting debugger key
            debug_path = self.DEBUG_KEY + msg[0]
            k = registry.open_key(HKLM, debug_path)
            registry.del_value(k, "debugger")
            # Deleting the bad path
            k = registry.open_key(HKCU, msg[1])
            if k:
                self.brush.color("[!!] POSSIBLE UAC BYPASS IN YOUR SYSTEM\n", 'RED')
                registry.delete_key(HKCU, msg[1])
                ctypes.windll.user32.MessageBoxA(
                    None, "UAC BYPASS DETECTADO Y MITIGADO. EJECUCION SEGURA DEL BINARIO", "PELIGRO!", 0)
            os.system(msg[0])
            # Setting the debugger key before breaking connection
            k = registry.open_key(HKLM, debug_path)
            payload = self.build_payload(msg[0][:-3] + "pyw")            
            registry.create_value(k,
                                  "debugger",
                                  payload)
            print "[+] Closing the listener"
            conn.close()
            listener.close()

    def add_debugger(self, registry, binlist):
        """ Adds debugger registry key for 
        each of the processes in the list """
        for binary in binlist:
            path = self.DEBUG_KEY + binary
            k = registry.open_key(HKLM, path)
            if not(k):
                k = registry.create_key(HKLM, path)
            payload = self.build_payload(binary[:-3] + "pyw")
            registry.create_value(k,
                                  "debugger",
                                  payload)
    def del_debugger(self, registry, binlist):
        """ Adds debugger registry key for 
        each of the processes in the list """
        for binary in binlist:
            path = self.DEBUG_KEY + binary
            k = registry.open_key(HKLM, path)
            if not(k):
                return
            registry.del_value(k, "debugger")            

    def build_payload(self, binary):
        return "mshta vbscript:Execute(\"CreateObject(\"\"Wscript.Shell\"\").Run \"\"powershell -Command \"\"\"\"& '%s%s'\"\"\"\"\"\", 0 : window.close\")" % (self.agents_path, binary)
