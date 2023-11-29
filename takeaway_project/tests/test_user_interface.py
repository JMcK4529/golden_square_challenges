import pytest
from unittest.mock import Mock
from lib.user_interface import UserInterface

def test_ui_instantiates_with_attributes():
    """Checks that instantiation creates class variables for io, menu
    and order, with Order being instantiated with menu as a parameter
    Also checks notification_sent, which should be False at instantiation"""
    io = Mock()
    menu = Mock()
    OrderClass = Mock()
    order_instance = OrderClass.return_value
    ui = UserInterface(io, menu, OrderClass)
    OrderClass.assert_called_once_with(menu)
    assert ui.io == io
    assert ui.menu == menu
    assert ui.order == order_instance
    assert ui.notification_sent == False

def test_display_greeting():
    """Checks that .display_greeting() returns a simple greeting
    Implicitly tests the ._show() method"""
    io = Mock()
    io.write = Mock()
    menu = Mock()
    OrderClass = Mock()
    ui = UserInterface(io, menu, OrderClass)
    ui.display_greeting()
    io.write.assert_called_once_with("Welcome to Takeaway Ordering!\n")

def test_display_menu():
    """Checks that .display_menu() returns 'Here is the menu:\n'
     concatenated with the output of menu.price_list()
    Implicitly tests the ._show() method"""
    io = Mock()
    io.write = Mock()
    menu = Mock()
    menu.price_list.return_value = "Apple Pie: £3.50\nBanana Split: £4.99"
    OrderClass = Mock()
    ui = UserInterface(io, menu, OrderClass)
    ui.display_menu()
    io.write.assert_called_once_with("Here is the menu:\n" + 
                                     menu.price_list.return_value + "\n")
    
def test_order_prompt_outputs_correct_prompt():
    """Checks that .order_prompt() causes the recurring order prompt
    string to be ouput to the io
    Implicitly tests that ._prompt() calls ._show()
    Implicitly tests ._show()"""
    io = Mock()
    io.write = Mock()
    io.readline.return_value = "add"
    menu = Mock()
    OrderClass = Mock()
    ui = UserInterface(io, menu, OrderClass)
    ui.order_prompt()
    io.write.assert_called_once_with("Would you like to:\n" +
                                     "- Add items to the order [add]\n" +
                                     "- Remove items from the order [rm]\n" +
                                     "- Confirm the order [ok]\n" +
                                     "- Cancel the order [cancel]\n")

def test_order_prompt_reads_strips_and_case_corrects_input():
    """Checks that .order_prompt() uses ._prompt() which
    strips the user input string, then applies .lowercase()
    Implicitly tests that ._prompt() reads input"""
    io = Mock()
    io.write = Mock()
    menu = Mock()
    OrderClass = Mock()
    ui = UserInterface(io, menu, OrderClass)
    inputs = [" Add ", "RM\n", "oK ", " CaNcEl \n"]
    interpretations = ["add", "rm", "ok", "cancel"]
    for input, interpretation in zip(inputs, interpretations):
        io.readline.return_value = input
        assert ui.order_prompt() == interpretation

def test_order_prompt_bad_response_raises_exception():
    """Checks that when a response other than the four accepted inputs is
    received, a message is displayed before asking for a new input
    Implicitly tests both ._show() and ._prompt()"""
    io = Mock()
    io.write = Mock()
    menu = Mock()
    OrderClass = Mock()
    ui = UserInterface(io, menu, OrderClass)
    inputs = [" And ", "RoM\n", "oKay ", " CaNcAl \n"]
    for input in inputs:
        io.readline.return_value = input
        
        with pytest.raises(ValueError) as err:
            ui.order_prompt()
        assert str(err.value) == f"{input.strip()} is an invalid input.\n" + \
            "Please enter only one of the four options provided."
        
        io.write.assert_called_with("Would you like to:\n" +
                                     "- Add items to the order [add]\n" +
                                     "- Remove items from the order [rm]\n" +
                                     "- Confirm the order [ok]\n" +
                                     "- Cancel the order [cancel]\n")
        
def test_add_adds_to_order():
    """"""
    io = Mock()
    io.write = Mock()
    io.readline = Mock(side_effect=["Apple Pie", "1"])

    menu = Mock()
    OrderClass = Mock()
    order_instance = OrderClass.return_value

    def side_effect(*args):
        return args
    order_instance.add_item = Mock(side_effect=side_effect)

    ui = UserInterface(io, menu, OrderClass)
    ui.add()
    order_instance.add_item.assert_called_with("Apple Pie", "1")
    io.write.assert_called_with("OK.\n")

def test_add_raises_exception_when_add_item_raises_exception():
    """"""
    io = Mock()
    io.write = Mock()
    io.readline = Mock(side_effect=["Zebrafish", "1"])

    menu = Mock()
    OrderClass = Mock()
    order_instance = OrderClass.return_value

    def side_effect(*args):
        raise ValueError("Test Error")
    order_instance.add_item = Mock(side_effect=side_effect)

    ui = UserInterface(io, menu, OrderClass)
    with pytest.raises(ValueError) as err:
        ui.add()
    assert str(err.value) == "Order Error: Test Error"
    order_instance.add_item.assert_called_with("Zebrafish", "1")

def test_rm_removes_item_from_order():
    """"""
    io = Mock()
    io.write = Mock()
    io.readline = Mock(side_effect=["Banana Split", "1"])

    menu = Mock()
    OrderClass = Mock()
    order_instance = OrderClass.return_value
    order_instance.items = {"Banana Split": 2}

    def side_effect(*args):
        return args
    order_instance.remove_item = Mock(side_effect=side_effect)
    
    ui = UserInterface(io, menu, OrderClass)
    ui.rm()
    order_instance.remove_item.assert_called_with("Banana Split", "1")
    io.write.assert_called_with("OK.\n")

def test_rm_raises_exception_when_remove_item_raises_exception():
    """"""
    io = Mock()
    io.write = Mock()

    menu = Mock()
    OrderClass = Mock()
    order_instance = OrderClass.return_value

    def side_effect(*args):
        raise ValueError("Test Error")
    order_instance.remove_item = Mock(side_effect=side_effect)
    
    orders = [{}, {"Apple Pie": 3},
              {"Banana Split": 2}, {"Banana Split": 1}]
    # `orders` tests: empty .items, item not in .items, 
    # quantity reduced to 0 and quantity set < 0, respectively

    for order in orders:
        io.readline = Mock(side_effect=["Banana Split", "2"])
        order_instance.items = order
        ui = UserInterface(io, menu, OrderClass)
        with pytest.raises(ValueError) as err:
            ui.rm()
        assert str(err.value) == "Order Error: Test Error"
        order_instance.remove_item.assert_called_with("Banana Split", "2")

def test_ok_asks_for_verification():
    """"""
    io = Mock()
    io.write = Mock()
    io.readline.return_value = "Y"

    menu = Mock()
    OrderClass = Mock()
    order_instance = OrderClass.return_value
    receipt = ["Your current order is\n", "1x Apple Pie @ £3.50\n",
               "1x Banana Split @ £4.99\n", "---\n", "Total = £8.49\n",
               "---"]
    order_instance.show.return_value = "".join(receipt)
    
    ui = UserInterface(io, menu, OrderClass)
    ui.ok()
    io.write.assert_called_once_with("".join(receipt) + "\n" + 
                                     "Is that correct? [Y/N]\n")
    
def test_ok_calls_verify_only_if_user_verifies():
    """"""
    io = Mock()
    io.write = Mock()

    menu = Mock()
    OrderClass = Mock()
    order_instance = OrderClass.return_value
    receipt = ["Your current order is\n", "1x Apple Pie @ £3.50\n",
               "1x Banana Split @ £4.99\n", "---\n", "Total = £8.49\n",
               "---"]
    order_instance.show.return_value = "".join(receipt)
    
    yes_inputs = ["Y", "y"]
    io.readline = Mock(side_effect=yes_inputs)

    for input in yes_inputs:
        order_instance.verify = Mock()
        ui = UserInterface(io, menu, OrderClass)
        assert ui.ok()
        order_instance.verify.assert_called_once()

    no_inputs = ["N", "n"]
    io.readline = Mock(side_effect=no_inputs)

    for input in no_inputs:
        order_instance.verify = Mock()
        ui = UserInterface(io, menu, OrderClass)
        assert ui.ok() == False
        order_instance.verify.assert_not_called()

def test_ok_raises_exception_with_bad_user_input():
    """"""
    io = Mock()
    io.write = Mock()

    menu = Mock()
    OrderClass = Mock()
    order_instance = OrderClass.return_value
    receipt = ["Your current order is\n", "1x Apple Pie @ £3.50\n",
               "1x Banana Split @ £4.99\n", "---\n", "Total = £8.49\n",
               "---"]
    order_instance.show.return_value = "".join(receipt)

    bad_inputs = ["a", "b", "c", "cancel", "exit", "q"]
    io.readline = Mock(side_effect=bad_inputs) 
    for input in bad_inputs:
        ui = UserInterface(io, menu, OrderClass)
        with pytest.raises(ValueError) as err:
            ui.ok()
        assert str(err.value) == "Please enter either [Y] " + \
                                "to confirm your order" + \
                                " or [N] to return to the ordering process."
        order_instance.verify.assert_not_called()

def test_cancel_asks_for_confirmation():
    """"""
    io = Mock()
    io.write = Mock()
    io.readline.return_value = "N"

    menu = Mock()
    OrderClass = Mock()
    order_instance = OrderClass.return_value

    ui = UserInterface(io, menu, OrderClass)
    ui.cancel()
    io.write.assert_called_once_with(
        "Are you sure you want to cancel your order? [Y/N]\n"
        )

def test_cancel_exits_politely_if_user_confirms():
    """"""
    io = Mock()
    io.write = Mock()
    confirms = ["Y", "y"]
    io.readline = Mock(side_effect=confirms)

    menu = Mock()
    OrderClass = Mock()
    order_instance = OrderClass.return_value

    i = 0
    while i < len(confirms):
        ui = UserInterface(io, menu, OrderClass)
        
        with pytest.raises(SystemExit):
            ui.cancel()

        calls = io.write.call_args_list
        for j in range(2):
            args, _ = calls[-j-1]
            assert args[0] == [
            "Are you sure you want to cancel your order? [Y/N]\n",
            "We hope to see you again soon!\n"
            ][-j-1]

        i += 1

def test_cancel_raises_exception_with_bad_user_input():
    """"""
    io = Mock()
    io.write = Mock()
    bad_inputs = ["cancel", "quit", "exit", "q"]
    io.readline = Mock(side_effect=bad_inputs)

    menu = Mock()
    OrderClass = Mock()
    order_instance = OrderClass.return_value

    i = 0
    while i < len(bad_inputs):
        ui = UserInterface(io, menu, OrderClass)
        
        with pytest.raises(ValueError) as err:
            ui.cancel()
        assert str(err.value) == \
            "Please enter either [Y] to exit the program" + \
            " or [N] to return to the ordering process."

        i += 1

def test_cancel_returns_false_if_ordering_should_continue():
    """"""
    io = Mock()
    io.write = Mock()
    rejects = ["N", "n"]
    io.readline = Mock(side_effect=rejects)

    menu = Mock()
    OrderClass = Mock()
    order_instance = OrderClass.return_value

    i = 0
    while i < len(rejects):
        ui = UserInterface(io, menu, OrderClass)
        assert ui.cancel() == False
        i += 1

def test_get_contact_number_asks_and_confirms():
    """Checks that .get_contact_number() asks the user to provide
    a phone number, then confirms that it is correct by asking for
    a Y/N response
    .get_contact_number() should return True for this confirmation"""
    io = Mock()
    io.write = Mock()
    phone_and_confirm = ["07700900714", "Y"]
    io.readline = Mock(side_effect=phone_and_confirm)

    menu = Mock()
    notification = Mock()
    notification.status = 'sent'
    menu.send_notification.return_value = notification

    OrderClass = Mock()
    order_instance = OrderClass.return_value

    ui = UserInterface(io, menu, OrderClass)
    assert ui.get_contact_number()
    calls = io.write.call_args_list
    for i in range(2):
        args, _ = calls[i]
        assert args[0] == ["Please enter your phone number:\n", 
                           f"Your phone number is {phone_and_confirm[0]}.\n" +
                           "Is that correct? [Y/N]\n"][i]

def test_get_contact_number_when_user_does_not_confirm():
    """Checks that .get_contact_number() returns False when the user
    input is negative"""
    io = Mock()    
    io.write = Mock()
    phone_and_reject = ["07700900714", "N"]
    io.readline = Mock(side_effect=phone_and_reject)

    menu = Mock()
    OrderClass = Mock()
    order_instance = OrderClass.return_value

    ui = UserInterface(io, menu, OrderClass)
    assert ui.get_contact_number() == False
    calls = io.write.call_args_list
    for i in range(2):
        args, _ = calls[i]
        assert args[0] == ["Please enter your phone number:\n", 
                           f"Your phone number is {phone_and_reject[0]}.\n" +
                           "Is that correct? [Y/N]\n"][i]

def test_get_contact_number_checks_number_validity():
    """Checks that only valid UK phone numbers are accepted by
    .get_contact_number() - invalid numbers raise an Exception"""
    io = Mock()
    io.write = Mock()
    phone_with_confirm = ["07700900714", "Y",
                         "+447700900714", "Y"]
    invalid_numbers_with_confirms = [
                "0770090071", # too short, leading 07
                "+44770090071", # too short, leading +447
                "01700900714", # right length, bad lead 01
                "+441700900714", # right length, bad lead +441
                "077009007141", # too long, leading 07
                "+4477009007141", # too long, leading +447
                                    ] 
    io.readline = Mock(side_effect=phone_with_confirm)

    menu = Mock()
    notification = Mock()
    notification.status = 'sent'
    menu.send_notification.return_value = notification

    OrderClass = Mock()
    order_instance = OrderClass.return_value

    ui = UserInterface(io, menu, OrderClass)
    for i in range(len(phone_with_confirm)//2):
        assert ui.get_contact_number()
        calls = io.write.call_args_list
        args, _ = calls[-2]
        assert args[0] == f"Your phone number is {phone_with_confirm[i*2]}." + \
                                    "\nIs that correct? [Y/N]\n"
    
    io.readline = Mock(side_effect=invalid_numbers_with_confirms)
    for i in range(len(invalid_numbers_with_confirms)):
        input = invalid_numbers_with_confirms[i]
        with pytest.raises(ValueError) as err:
            ui.get_contact_number()
        assert str(err.value) == f"{input} " + \
            "is not a valid UK phone number."

def test_get_contact_number_calls_send_notification():
    """Checks that a valid phone number causes .get_contact_number()
    to call Menu's .send_notification() method once with the right args"""
    io = Mock()
    io.write = Mock()
    phone_and_confirm = ["+447700900714", "Y"]
    io.readline = Mock(side_effect=phone_and_confirm)

    menu = Mock()
    notification = Mock()
    notification.status = 'sent'
    menu.send_notification.return_value = notification
    OrderClass = Mock()
    order_instance = OrderClass.return_value
    
    ClientClass = Mock

    ui = UserInterface(io, menu, OrderClass)
    ui.get_contact_number()
    menu.send_notification.assert_called_once_with(order_instance, "+447700900714")

def test_get_contact_number_shows_goodbye_message_after_notification_sent():
    """Checks that .get_contact_number() shows a final message
    to the user after calling .send_notification()
    Also checks that self.notification_sent is True after
    .send_notification() is called"""
    io = Mock()
    io.write = Mock()
    phone_and_confirm = ["+447700900714", "Y"]
    io.readline = Mock(side_effect=phone_and_confirm)

    menu = Mock()
    notification = Mock()
    notification.status = 'sent'
    menu.send_notification.return_value = notification
    OrderClass = Mock()
    order_instance = OrderClass.return_value
    
    ClientClass = Mock

    ui = UserInterface(io, menu, OrderClass)
    ui.get_contact_number()
    menu.send_notification.assert_called()
    io.write.assert_called_with("Confirmation of your order is being sent to your phone!\n")
    assert ui.notification_sent

def test_run_good_use_scenario():
    """Checks that run calls the UI methods in the expected
    order when all user inputs are valid"""
    assert False

def test_run_handles_order_prompt_exceptions():
    """Checks that run does not crash when a bad input is given
    to .order_prompt(), and that the program continues as expected"""
    assert False

def test_run_handles_order_add_exceptions():
    """Checks that run does not crash when a bad input is given
    to .add(), and that the program continues as expected"""
    assert False

def test_run_handles_rm_exceptions():
    """Checks that run does not crash when a bad input is given
    to .rm(), and that the program continues as expected"""
    assert False

def test_run_handles_ok_exceptions():
    """Checks that run does not crash when a bad input is given
    to .ok(), and that the program continues as expected"""
    assert False

def test_run_handles_cancel_exceptions():
    """Checks that run does not crash when a bad input is given
    to .cancel(), and that the program continues as expected"""
    assert False

def test_run_handles_get_contact_number_exceptions():
    """Checks that run does not crash when a bad input is given
    to .get_contact_number(), and that the program continues as expected"""
    assert False