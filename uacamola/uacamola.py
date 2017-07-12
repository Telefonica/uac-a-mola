from termcolor import colored
from autocomplete import Completer
from session import Session
import readline
import sys
import os
import banners

END_COMMANDS = ['quit', 'exit', 'q']
CLEAR_COMMANDS = ['clear', 'cls']


def console():
    # Configuring the commpleter
    comp = Completer()
    readline.set_completer_delims(' \t\n;')
    readline.parse_and_bind("tab: complete")
    readline.set_completer(comp.complete)

    print banners.get_banner()
    print colored(' [+] ', 'yellow', attrs=['bold']) + 'Starting the console...'
    print colored(' [*] ', 'green', attrs=['bold']) + 'Console ready!\n\n'

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
                print colored('[!] Please, load a module', 'red', attrs=['bold'])
                continue
            session = Session(user_input[1])
            # The module is incorrect
            if not(session.correct_module()):
                session = None

        elif user_input[0] == 'show':
            if session is None:
                print colored('[!] Please, load a module', 'red', attrs=['bold'])
                continue
            session.show()

        elif user_input[0] == 'set':
            if session is None:
                print colored('[!] Please, load a module', 'red', attrs=['bold'])
                continue
            elif len(user_input) != 3:
                print colored('[!] Wrong number of arguments for set', 'red', attrs=['bold'])
                continue
            else:
                session.set(user_input[1], user_input[2])

        elif user_input[0] == 'run':
            if session is None:
                print colored('[!] Please, load a module', 'red', attrs=['bold'])
                continue
            session.run()


if __name__ == "__main__":
    console()
