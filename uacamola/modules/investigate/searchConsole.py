# This file is part of uac-a-mola
# Copyright (C) Santiago Hernandez Ramos <shramos@protonmail.com>
#
# DESCRIPTION
# This file is aimed for simplify the search of some Registry values
# that resides in a Procmon XML generated file.

from module import Module
from support.procmonXMLparser import ProcmonXmlParser
from termcolor import colored
import os
from support.procmonXMLfilter import *
import copy


class CustomModule(Module):
    def __init__(self):
        information = {"Name": "SearchConsole",
                       "Description": "This module parses a procmon xml file, and allows you to interactively search for Registry access patterns inside it",
                       "Author": "Santiago Hernandez Ramos"}

        options = {"xml_path": [None, "description", True]}

        # Constructor of the parent class
        super(CustomModule, self).__init__(information, options)

        # Class variables
        self.events = None
        self.display = dict(Operation=False,
                            Process_Name=False,
                            PID=False,
                            Path=True,
                            Result=False,
                            Detail=False)

        self.filters = dict(Operation=None,
                            Process_Name=None,
                            PID=None,
                            Path=None,
                            Pattern=None)

    # This method must be always implemented, it is called by the run option
    def run_module(self):
        # To access user provided attributes, use self.args dictionary
        print self.get_banner()
        xmlParser = ProcmonXmlParser(self.args["xml_path"])
        self.events = xmlParser.parse()
        # Releasing memory
        del xmlParser

        while True:
            if self.filters["Process_Name"] is None:
                user_input = raw_input(
                    'searchConsole[' + colored("all_procs", 'yellow', attrs=['bold']) + ']> ').split()
            else:
                user_input = raw_input(
                    'searchConsole[' + colored(self.filters["Process_Name"], 'yellow', attrs=['bold']) + ']> ').split()

            if user_input == []:
                continue
            elif user_input[0] == 'h' or user_input[0] == 'help':
                self.help()
            elif user_input[0] == 'run':
                self.run()
            elif user_input[0] == 'q' or user_input[0] == 'quit':
                break
            elif user_input[0] == 'show':
                self.show()
            elif user_input[0] == 'clear':
                os.system('cls')
            elif len(user_input) == 3 and user_input[0] == 'display' and user_input[2] in ["true", "True", "false", "False"]:
                if user_input[1] in ["Process_Name", "Operation", "PID",
                                     "Path", "Result", "Detail"]:
                    self.display[user_input[1]] = user_input[2]
                else:
                    print colored("[!] WRONG FILTER: Please respect uppercase letters", 'red', attrs=['bold'])
                    continue

            elif len(user_input) > 3 and user_input[0] == 'set' and user_input[1] == 'Pattern':
                self.filters[user_input[1]] = user_input[2:]
            elif len(user_input) == 3 and user_input[0] == 'set':
                if user_input[1] in ["Process_Name", "Operation", "PID",
                                     "Path", "Result", "Pattern"]:
                    self.filters[user_input[1]] = user_input[2]
                else:
                    print colored("[!] WRONG FILTER: Please respect uppercase letters", 'red', attrs=['bold'])
                    continue

    def help(self):
        pass

    def show(self):

        print colored("\n Filters", 'yellow', attrs=['bold'])
        print " -------"

        for key, value in self.filters.iteritems():
            if str(self.filters[key]).lower() == "none":
                print " |_" + key + " = " + str(value)
            else:
                print " |_" + colored(key + " = " + str(value), 'green', attrs=['bold'])

        print colored("\n Display", 'yellow', attrs=['bold'])
        print " -------"

        for key, value in self.display.iteritems():
            if str(self.display[key]).lower() == "false":
                print " |_" + key + " = " + str(value)
            else:
                print " |_" + colored(key + " = " + str(value), 'green', attrs=['bold'])

        print ""

    def run(self):
        events = copy.deepcopy(self.events)

        if str(self.filters["Process_Name"]).lower() != "None".lower():
            events = by_process(events, self.filters["Process_Name"])
        if str(self.filters["Operation"]).lower() != "None".lower():
            events = by_operation(events, self.filters["Operation"])
        if str(self.filters["PID"]).lower() != "None".lower():
            events = by_pid(events, self.filters["PID"])
        if str(self.filters["Pattern"]).lower() != "None".lower():
            events = by_pattern(events, self.filters["Pattern"])

        self.pretty_print(events)

    def pretty_print(self, events):
        for k in events.keys():
            print colored("\n" + k, 'green', attrs=['bold'])
            print colored("-" * len(k), 'green', attrs=['bold'])
            for e in events[k]:
                for k2, value in self.display.iteritems():
                    if str(value).lower() == "true":
                        print e.find(k2).text
                print ""

    def get_banner(self):
        banner = """  ____                      _      ____                      _
 / ___|  ___  __ _ _ __ ___| |__  / ___|___  _ __  ___  ___ | | ___
 \\___ \\ / _ \\/ _` | '__/ __| '_ \\| |   / _ \\| '_ \\/ __|/ _ \\| |/ _ \\
  ___) |  __| (_| | | | (__| | | | |__| (_) | | | \\__ | (_) | |  __/
 |____/ \\___|\\__,_|_|  \\___|_| |_|\\____\\___/|_| |_|___/\\___/|_|\\___|
                                                                    """
        return banner
