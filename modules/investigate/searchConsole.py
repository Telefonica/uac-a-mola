from module import Module
from support.procmonXMLparser import ProcmonXmlParser
from termcolor import colored


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

    # This method must be always implemented, it is called by the run option
    def run_module(self):
        # To access user provided attributes, use self.args dictionary
        xmlParser = ProcmonXmlParser(self.args["xml_path"])
        self.events = xmlParser.parse()

        operation = None
        process_name = None

        while True:
            if process_name is None:
                user_input = raw_input(
                    'searchConsole[' + colored("All_procs", 'yellow', attrs=['bold']) + ']> ').split()
            else:
                user_input = raw_input(
                    'searchConsole[' + colored(process_name, 'yellow', attrs=['bold']) + ']> ').split()

            if user_input == []:
                continue
            elif len(user_input) == 2 and (user_input[0] == 'op'
                                           or user_input[0] == 'operation'):
                operation = user_input[1]
            elif user_input[0] == 'h' or user_input[0] == 'help':
                self.help()
            elif len(user_input) == 2 and user_input[0] == 'search':
                self.search(user_input[1], operation, process_name)
            elif user_input[0] == 'q' or user_input[0] == 'quit':
                break
            elif len(user_input) == 2 and user_input[0] == 'process':
                process_name = user_input[1]

    def help(self):
        print "search [word]: Name of the word for search for"
        print "process [process_name]: Name of the process for search for"
        print """op, operation [operation_name]: Name of the operation for find for: \
            RegOpenKey
            RegQueryValue
            RegCloseKey
            RegQueryKey
            RegSetValue
            RegCreateKey
            RegEnumKey
            RegEnumValue
            RegDeleteValue
            RegQueryKeySecurity
            RegLoadKey
            RegDeleteKey
            RegKeySecurity
            RegSetKeySecurity
            RegQueryMultipleValueKey
            RegFlushKey"""

    def search(self, word, operation, proc_name):
        if proc_name is None:
            proc_name = ""

        try:
            if operation is not None:
                for e in self.events[operation]:
                    if word.lower() in e.find("Path").text.lower() \
                       and proc_name.lower() in e.find("Process_Name").text.lower():
                        print e.find("Path").text

        except KeyError:
            print colored("[!] WRONG OPERATION", 'red', attrs=['bold'])
            return
