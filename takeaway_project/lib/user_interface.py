import os
from lib.menu import Menu
from lib.order import Order
from lib.NotificationError import NotificationError

class UserInterface:
    def __init__(self, io, menu, OrderClass=Order):
        self.io = io
        self.menu = menu
        self.order = OrderClass(self.menu)
        self.notification_sent = False

    def _show(self, message):
        self.io.write(message + "\n")

    def _prompt(self, message):
        self.io.write(message + "\n")
        input = self.io.readline().strip()
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
                            "- Cancel the order [cancel]")
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
    
    def notify(self, phone_no):
        match self._prompt(f"Your phone number is {phone_no}.\n" +
                            "Is that correct? [Y/N]").lower():
            case "y":
                if self.menu.send_notification(
                    self.order, phone_no).status == 'sent':
                    self._show(
                        "Confirmation of your order is " + \
                            "being sent to your phone!")
                    self.notification_sent = True
                    return True
                else:
                    raise NotificationError(
                        "Something went wrong with your notification!")
            case "n":
                return False
            case _:
                raise ValueError("Please enter either [Y] to confirm or " +
                                 "[N] to retry.")
            
    def get_contact_number(self):
        phone_no = self._prompt("Please enter your phone number:")
        if (len(phone_no) == 11 and phone_no[0:2] == "07" 
            and phone_no.isnumeric()) \
        or \
           (len(phone_no) == 13 and phone_no[0:4] == "+447"
            and phone_no[1:].isnumeric()):
            pass
        else:
            raise ValueError(f"{phone_no} is not a valid UK phone number.")

        try:
            return self.notify(phone_no)
        except ValueError as err:
            raise ValueError(err)
        except NotificationError as err:
            raise NotificationError(err)

    def run(self):
        self.display_greeting()
        self.display_menu()

        order_loop = True
        while order_loop:
            try:
                user_in = self.order_prompt()

                match user_in:
                    case "add":
                        self.add()
                    case "rm":
                        self.rm()
                    case "ok":
                        ok_loop = True
                        while ok_loop:
                            try:
                                if self.ok():
                                    order_loop = False
                                ok_loop = False
                            except ValueError as err:
                                self._show(str(err))
                    case "cancel":
                        cancel_loop = True
                        while cancel_loop:
                            try:
                                self.cancel()
                                ok_loop = False
                            except ValueError as err:
                                self._show(str(err))
            
            except ValueError as err:
                self._show(str(err))

        contact_loop = True
        while contact_loop:
            try:
                if self.get_contact_number():
                    contact_loop = False
            except NotificationError as err:
                self._show(str(err))

                confirm_loop = True
                while confirm_loop:
                    try:
                        if self.notify():
                            confirm_loop = False
                    except ValueError() as err:
                        self._show(str(err))
                    except NotificationError as err:
                        self._show(str(err))
                        self._show(
                        "Sorry, we cannot process your order right now.\n" +
                        "Please try again later!")
                        exit()

            except ValueError as err:
                self._show(str(err))