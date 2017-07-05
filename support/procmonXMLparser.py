# This file is part of uac-a-mola
# Copyright (C) Santiago Hernandez Ramos <shramos@protonmail.com>
#
# DESCRIPTION
# This file parses an xml produced by Procmon application and returns
# a dictionary with all the Windows Registry associated operations.

from xml.etree.ElementTree import iterparse
import os
from termcolor import colored


class ProcmonXmlParser():

    def __init__(self, xml_path):
        self.path = xml_path
        self.events = dict(RegOpenKey=[],
                           RegQueryValue=[],
                           RegCloseKey=[],
                           RegQueryKey=[],
                           RegSetValue=[],
                           RegCreateKey=[],
                           RegEnumKey=[],
                           RegEnumValue=[],
                           RegDeleteValue=[],
                           RegQueryKeySecurity=[],
                           RegLoadKey=[],
                           RegDeleteKey=[],
                           RegKeySecurity=[],
                           RegSetKeySecurity=[],
                           RegQueryMultipleValueKey=[],
                           RegFlushKey=[])

    def parse(self):

        tree = iterparse(self.path)

        file_size = int(os.path.getsize(self.path))

        print "\n[*] PARSING FILE: " \
            + colored(self.path.split("\\")[-1], 'yellow', attrs=['bold'])

        print "[*] FILE SIZE: " + \
            colored("%d MB" % (file_size / 1024 / 1024),
                    'yellow', attrs=['bold'])

        print "[*] BUILDING THE STRUCTURES WILL TAKE SOME TIME"

        try:
            for event, elem in tree:
                operation = elem.find('Operation')
                if elem.tag == 'event' and operation is not None:
                    if 'Reg' in operation.text:
                        self.events[operation.text].append(elem)

            print colored("[*] PARSING FINISHED CORRECTLY\n",
                          'green', attrs=['bold'])

            return self.events

        except Exception as error:
            print colored("[*] PARSING FAILED", 'red', attrs=['bold'])
            print colored(" => " + str(error), 'red', attrs=['bold'])

        return None
