from module import Module
from lxml import etree


class CustomModule(Module):
    def __init__(self):
        information = {"Name": "Procmon XML Parser",
                       "Description": "This module parses the XML file that can be exported using Procmon",
                       "Author": "Santiago Hernandez Ramos"}

        # -----------name-------description---default_value
        options = {"xml_path": [None, "Path to the XML file"],
                   "word": [None, "Keyword for searching for in the XML"],
                   "process_name": [None, "Keyword for searching by process name in the XML"],
                   "not_found": [True, "Search only events not found"],
                   "operation": [None, "Search by Win Register operation"]}

        # Constructor of the parent class
        super(CustomModule, self).__init__(information, options)

        # Class attributes
        self._tree = None

    # This module must be always implemented, it is called by the run option
    def run_module(self):
        # To access user provided attributes, use self._options dictionary
        xml_path = str(self._options["xml_path"][0])
        word = str(self._options["word"][0])
        not_found = str(self._options["not_found"][0])
        operation = str(self._options["operation"][0])
        process_name = str(self._options["process_name"][0])

        self._tree = etree.parse(xml_path)
        events = self.events()

        if not_found != "False":
            events = self.events_notfound(events)
        if word != "None":
            events = self.events_word(word, events)
        if operation != "None":
            events = self.events_operation(operation, events)
        if process_name != "None":
            events = self.events_proc_name(process_name, events)

        for p in self.paths(events):
            print p

        return self.paths(events)

    def events(self):
        return self._tree.findall('.//event')

    def events_proc_name(self, proc_name, events):
        return [e for e in events
                for o in e.findall('.//Process_Name')
                if o.text == proc_name]

    def events_notfound(self, events):
        return [e for e in events
                for o in e.findall('.//Result')
                if o.text == 'NAME NOT FOUND']

    def events_word(self, word, events):
        return [e for e in events
                for o in e.findall('.//Path')
                if word in o.text]

    def events_operation(self, op, events):
        return [e for e in events
                for o in e.findall('.//Operation')
                if op in o.text]

    def paths(self, events):
        return [p.text for e in events
                for p in e.findall('.//Path')]
