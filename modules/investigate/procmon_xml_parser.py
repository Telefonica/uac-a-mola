from module import Module
from lxml import etree


class CustomModule(Module):
    def __init__(self):
        information = {"Name": "Procmon XML Parser",
                       "Description": "This module parses the XML file that can be exported using Procmon",
                       "Author": "Santiago Hernandez Ramos"}

        # -----------name-------description---default_value
        options = {"xml_path": [None, "Path to the XML file", True],
                   "word": [None, "Keyword for searching for in the XML", False],
                   "process_name": [None, "Keyword for searching by process name in the XML", False],
                   "not_found": [True, "Search only events not found", False],
                   "operation": [None, "Search by Win Register operation", False],
                   "destination": [None, "Destination File to write results", False]}

        # Constructor of the parent class
        super(CustomModule, self).__init__(information, options)

        # Class attributes
        self._tree = None
        # To access user supplied attributes use the
        # structure self.args["atribute_name"]

    # This module must be always implemented, it is called by the run option
    def run_module(self):

        self.parse_tree()
        events = self.events()

        if self.args["not_found"] != "False":
            events = self.events_notfound(events)
        if self.args["word"] != "None":
            events = self.events_word(events)
        if self.args["operation"] != "None":
            events = self.events_operation(events)
        if self.args["process_name"] != "None":
            events = self.events_proc_name(events)

        self.results(events)

    def results(self, events=None):
        if self.args["destination"] is not None:
            try:
                f = open(self.args["destination"], "w")
                print "[*] Writting to file: %s" % str(self.args["destination"])
            except:
                print "[!] Error opening the file"

            for p in self.paths(events):
                f.write(p + "\n")

            f.close()

        else:
            for p in self.paths(events):
                print p

    def parse_tree(self):
        self._tree = etree.parse(self.args["xml_path"])

    def events(self):
        return self._tree.findall('.//event')

    def events_proc_name(self, events):
        return [e for e in events
                for o in e.findall('.//Process_Name')
                if o.text == self.args["process_name"]]

    def events_notfound(self, events):
        return [e for e in events
                for o in e.findall('.//Result')
                if o.text == 'NAME NOT FOUND']

    def events_word(self, events):
        return [e for e in events
                for o in e.findall('.//Path')
                if self.args["word"] in o.text]

    def events_operation(self, events):
        return [e for e in events
                for o in e.findall('.//Operation')
                if self.args["operation"] in o.text]

    def paths(self, events):
        return [p.text for e in events
                for p in e.findall('.//Path')]
