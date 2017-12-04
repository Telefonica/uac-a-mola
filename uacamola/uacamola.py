#--encoding: utf-8--

from autocomplete import Completer
from session import Session
import readline
import sys
import os
import banners
from support.brush import Brush
from termcolor import colored


END_COMMANDS = ['quit', 'exit', 'q']
CLEAR_COMMANDS = ['clear', 'cls']

def console():
    # Configuring the commpleter
    comp = Completer(['load', 'set', 'show', 'run', 'back', 'quit', 'help'])
    readline.set_completer_delims(' \t\n;')
    readline.parse_and_bind("tab: complete")
    readline.set_completer(comp.complete) 
    brush = Brush()

    print (banners.get_banner())
    brush.color(' [+]', 'YELLOW')
    print ' Starting the console...'
    brush.color(' [*]', 'GREEN')
    print ' Console ready!\n\n'

    session = None

    while True:

        if session is None:
            user_input = raw_input(
                colored('uac-a-mola> ', 'yellow', attrs=['bold'])).split()
        else:
            user_input = raw_input(
                "uac-a-mola["
                + colored(session.header(), 'yellow', attrs=['bold'])
                + "]> ").split()

        if user_input == []:
            continue

        elif user_input[0] in CLEAR_COMMANDS:
            os.system('cls')

        elif user_input[0] == 'back':
            session = None

        elif user_input[0] in END_COMMANDS:
            sys.exit(0)

        elif user_input[0] == 'load':
            if (len(user_input) == 1):
                brush.color('[!] Please, load a module\n', 'RED')
                continue
            session = Session(user_input[1])
            brush = Brush()

            # The module is incorrect
            if not(session.correct_module()):
                session = None

        elif user_input[0] == 'show':
            if session is None:
                brush.color('[!] Please, load a module\n', 'RED')
                continue
            session.show()

        elif user_input[0] == 'set':
            if session is None:
                brush.color('[!] Please, load a module\n', 'RED')
                continue
            elif len(user_input) != 3:
                brush.color('[!] Wrong number of arguments for set\n', 'RED')
                continue
            else:
                session.set(user_input[1], user_input[2])

        elif user_input[0] == 'run':
            if session is None:
                brush.color('[!] Please, load a module\n', 'RED')
                continue
            session.run()


if __name__ == "__main__":
    console()
