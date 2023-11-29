import pytest
from unittest.mock import Mock
from lib.user_interface import UserInterface

def test_ui_instantiates_with_attributes():
    """Checks that instantiation creates class variables for io, menu
    and order, with Order being instantiated with menu as a parameter"""
    io = Mock()
    menu = Mock()
    OrderClass = Mock()
    order_instance = OrderClass.return_value
    ui = UserInterface(io, menu, OrderClass)
    OrderClass.assert_called_once_with(menu)
    assert ui.io == io
    assert ui.menu == menu
    assert ui.order == order_instance

def test_display_greeting():
    """Checks that .display_greeting() returns a simple greeting
    Implicitly tests the ._show() method"""
    io = Mock()
    io.write = Mock()
    menu = Mock()
    OrderClass = Mock()
    ui = UserInterface(io, menu, OrderClass)
    ui.display_greeting()
    io.write.assert_called_once_with("Welcome to Takeaway Ordering!")

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
                                     menu.price_list.return_value)
    
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
    io.write.assert_called_with("OK.")

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
    io.write.assert_called_with("OK.")

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
                                     "Is that correct? [Y/N]")
    
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
        "Are you sure you want to cancel your order? [Y/N]"
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
            "Are you sure you want to cancel your order? [Y/N]",
            "We hope to see you again soon!"
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
    a Y/N response"""
    assert False

def test_get_contact_number_checks_number_validity():
    """Checks that only valid UK phone numbers are accepted by
    .get_contact_number() - invalid numbers raise an Exception"""
    assert False

def test_get_contact_number_calls_send_notification():
    """Checks that a valid phone number causes .get_contact_number()
    to call Menu's .send_notification() method once with the right args"""
    assert False

def test_get_contact_number_shows_goodbye_message():
    """Checks that .get_contact_number() shows a final message
    to the user after calling .send_notification()"""
    assert False

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