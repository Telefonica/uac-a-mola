from module import Module
import subprocess
from threading import Lock, Thread
import time
import psutil


class CustomModule(Module):
    def __init__(self):
        information = {"Name": "Procmon",
                       "Description": "This module executes procmon for monitoring a list of binaries provided by the user. Require administrator priviledges!",
                       "Author": "Santiago Hernandez Ramos"}

        # -----------name-------description---default_value
        options = {"binlist_path": [None, "Path to the binaries list"],
                   "procmon_path": [None, "Path to procmon binary"],
                   "output": ["results.xml", "Name of the XML output file"]}

        # Constructor of the parent class
        super(CustomModule, self).__init__(information, options)

        # Class atributes, initialization in the run_module method
        # after the user has set the values
        self._binlist_path = None
        self._procmmon_path = None
        self._output = None
        self.lock = Lock()

    # This module must be always implemented, it is called by the run option
    def run_module(self):
        # To access user provided attributes, use self._options dictionary
        self._binlist_path = str(self._options["binlist_path"][0])
        self._procmmon_path = str(self._options["procmon_path"][0])
        self._output = str(self._options["output"][0])

        Thread(target=self.monitoring).start()

        print "\n[*] STARTING PROGRAMS EXECUTION IN 5 SECONDS...\n"
        time.sleep(5)

        for b in self.binaries():
            print "  [+]Executing %s ..." % b
            previous_pid = psutil.pids()
            self.execute(b)
            time.sleep(3)
            new_pid = psutil.pids()
            print "  [-] Killing the process"

            self.kill(b.split('.')[0], previous_pid, new_pid)

        print "\n[*] PLEASE CLOSE PROCMON PROCESS\n"
        self.parsing_results()
        print "\n[*] RESULTS PARSED TO XML\n"

    def monitoring(self):
        try:
            self.lock.acquire()
            subprocess.check_call(
                [self._procmmon_path, "/BackingFile", "tmp"])
            self.lock.release()
        except subprocess.CalledProcessError as error:
            raise error

    def binaries(self):
        with open(self._binlist_path, 'r') as binfile:
            return binfile.read().splitlines()

    def execute(self, proc):
        try:
            subprocess.Popen([proc])
        except subprocess.CalledProcessError as error:
            raise error
        except WindowsError:
            print "[!!] The application can't be executed in win32 mode"
            return

    def kill(self, proc, last_pids=None, new_pids=None):
        new_pids = self.last_process_created(last_pids, new_pids)
        try:
            for p in new_pids:
                subprocess.check_call(["tskill", str(p)])
        except subprocess.CalledProcessError:
            print "[!!] The process %s can't be killed" % proc
            return

    def parsing_results(self):
        self.lock.acquire()
        try:
            subprocess.check_call(
                [self._procmmon_path, "/OpenLog", "tmp.PML", "/SaveAs", self._output])
        except subprocess.CalledProcessError as error:
            raise error

    def last_process_created(self, prev_pids, new_pids):
        pids = []
        for p in new_pids:
            if p not in prev_pids:
                pids.append(p)
        return pids
