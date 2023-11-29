import os
from lib.menu import Menu
from lib.order import Order

class UserInterface:
    def __init__(self, io, menu, OrderClass=Order):
        self.io = io
        self.menu = menu
        self.order = OrderClass(self.menu)

    def _show(self, message):
        self.io.write(message)

    def _prompt(self, message):
        self._show(message)
        input = self.io.readline()
        input = input.strip()
        return input

    def display_greeting(self):
        self._show("Welcome to Takeaway Ordering!")

    def display_menu(self):
        self._show("Here is the menu:\n" + 
                   self.menu.price_list())
    
    def order_prompt(self):
        input = self._prompt("Would you like to:\n" +
                            "- Add items to the order [add]\n" +
                            "- Remove items from the order [rm]\n" +
                            "- Confirm the order [ok]\n" +
                            "- Cancel the order [cancel]\n")
        match input.lower():
            case "add":
                return "add"
            case "rm":
                return "rm"
            case "ok":
                return "ok"
            case "cancel":
                return "cancel"
            case _:
                raise ValueError(f"{input} is an invalid input.\n" + 
                    "Please enter only one of the four options provided.")
            
    def add(self):
        dish = self._prompt("Which item?")
        quantity = self._prompt("How many?")
        try:
            self.order.add_item(dish, quantity)
            self._show("OK.")
        except ValueError as err:
            raise ValueError(f"Order Error: {err}")

    def rm(self):
        dish = self._prompt("Which item?")
        quantity = self._prompt("How many?")
        try:
            self.order.remove_item(dish, quantity)
            self._show("OK.")
        except ValueError as err:
            raise ValueError(f"Order Error: {err}")

    def ok(self):
        input = self._prompt(f"{self.order.show()}\n" +
                              "Is that correct? [Y/N]")
        if input.lower() == "y":
            self.order.verify()
            return True
        elif input.lower() == "n":
            return False
        else:
            raise ValueError("Please enter either [Y] to confirm your order"
                             + " or [N] to return to the ordering process.")


    def cancel(self):
        input = self._prompt(
            "Are you sure you want to cancel your order? [Y/N]"
        )
        if input.lower() == "n":
            return False
        elif input.lower() == "y":
            self._show("We hope to see you again soon!")
            exit()
        else:
            raise ValueError("Please enter either [Y] to exit the program"
                             + " or [N] to return to the ordering process.")

    def get_contact_number(self):
        pass

    def run(self):
        pass
        