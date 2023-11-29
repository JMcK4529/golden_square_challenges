import sys
from lib.menu import Menu
from lib.order import Order
from lib.user_interface import UserInterface


class TerminalIO:
    def readline(self):
        return sys.stdin.readline()

    def write(self, message):
        sys.stdout.write(message)


io = TerminalIO()
menu = Menu()
user_interface = UserInterface(io, menu, Order)
user_interface.run()
