from procmonXMLparser import ProcmonXmlParser
from procmonXMLfilter import by_operation, by_notfound, by_process, parse_events


p_parser = ProcmonXmlParser("C:\Users\user\Desktop\\resultados.xml")
events = p_parser.parse()
events = by_operation(events, 'regopenkey')
events = by_notfound(events)
events = by_process(events, 'procmon.exe')
events = parse_events(events)
for k in events.keys():
    for e in events[k]:
        print e
