import pytest
import os
from lib.menu import Menu
from unittest.mock import Mock

def test_is_dish_true_if_in_menu():
    """Checks that .is_dish returns True for args which are in the menu
    Implicitly tests that menu objects are created with a ._menu dictionary"""
    menu = Menu()
    for dish in ["Apple Pie", "Banana Split"]:
        assert menu.is_dish(dish)

def test_is_dish_false_if_not_in_menu():
    """Checks that .is_dish returns False for args which are in the menu"""
    menu = Menu()
    for dish in ["Coffee Cake", "Doughnut", "Eclair", "Flapjack"]:
        assert menu.is_dish(dish) == False

def test_get_price_if_in_menu():
    """Checks that .get_price returns price for args which are in the menu"""
    menu = Menu()
    assert menu.get_price("Apple Pie") == 3.5
    assert menu.get_price("Banana Split") == 4.99

def test_get_price_raises_exception_if_not_in_menu():
    """Checks that .get_price raises an Exception for args which are not in
    the menu"""
    menu = Menu()
    for dish in ["Coffee Cake", "Doughnut", "Eclair", "Flapjack"]:
        with pytest.raises(ValueError) as err:
            menu.get_price(dish)
        assert str(err.value) == f"{dish} is not on the menu"

def test_price_list():
    """Checks that .price_list returns a formatted string including
    all items and prices from ._menu"""
    menu = Menu()
    assert menu.price_list() == "Apple Pie: £3.50\nBanana Split: £4.99"

def test_order_time_for_verified_order():
    """Checks that .order_time returns the sum of the longest cook_time of
    an item in the order and the delivery time (fixed at 20 mins)
    Implicitly checks that ._delivery_time = 20"""
    order = Mock()
    order.items = {"Apple Pie": 1, "Banana Split": 3}
    order.is_verified.return_value = True
    menu = Menu()
    assert menu.order_time(order) == 55
    order.items = {"Banana Split": 3}
    assert menu.order_time(order) == 25

def test_order_time_for_unverified_order():
    """Checks that order times are only calculated for orders which
    have been verified"""
    order = Mock()
    order.is_verified.return_value = False
    menu = Menu()
    with pytest.raises(Exception) as err:
        menu.order_time(order)
    assert str(err.value) == "Order must be verified to deliver"

def test_send_notification_for_verified_order():
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    from_phone = os.environ['TWILIO_PHONE']
    to_phone = os.environ['PERSONAL_PHONE']

    Client = Mock()
    client_instance = Client.return_value
    notif = Mock
    receipt = "Your current order is:\n" + \
            "1x Apple Pie @ £3.50\n" + \
            "3x Banana Split @ £4.99\n" + \
            "---\n" + \
            "Total = £18.47\n" + \
            "---"
    notif.body = receipt
    client_instance.messages.create = Mock(side_effect=notif)

    menu = Menu()
    order = Mock()
    order.items = {"Apple Pie": 1, "Banana Split": 3}
    order.is_verified.return_value = True
    order.show.return_value = receipt
    
    notification = menu.send_notification(order, to_phone, Client)
    Client.assert_called_once_with(account_sid, auth_token)
    client_instance.messages.create.assert_called_once_with(
                        to=to_phone, 
                        from_=from_phone, 
                        body="Your order will be with you in 55 minutes!\n" +
                            "Order summary:\n" +
                            "1x Apple Pie @ £3.50\n" +
                            "3x Banana Split @ £4.99\n" +
                            "---\n" +
                            "Total = £18.47\n" +
                            "---"
                        )
    assert notification.body == "Your order will be with you in 55 minutes!\n" + \
                            "Order summary:\n" + \
                            "1x Apple Pie @ £3.50\n" + \
                            "3x Banana Split @ £4.99\n" + \
                            "---\n" + \
                            "Total = £18.47\n" + \
                            "---"
    
def test_send_notification_corrects_numbers_starting_with_07():
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    from_phone = os.environ['TWILIO_PHONE']
    to_phone = "07700900714"

    Client = Mock()
    client_instance = Client.return_value
    client_instance.messages.create = Mock()

    menu = Menu()
    order = Mock()
    order.items = {"Apple Pie": 1, "Banana Split": 3}
    order.is_verified.return_value = True
    order.show.return_value = "Your current order is:\n" + \
                            "1x Apple Pie @ £3.50\n" + \
                            "3x Banana Split @ £4.99\n" + \
                            "---\n" + \
                            "Total = £18.47\n" + \
                            "---"
    
    menu.send_notification(order, to_phone, Client)

    Client.assert_called_once_with(account_sid, auth_token)
    client_instance.messages.create.assert_called_once_with(
                        to="+447700900714", 
                        from_=from_phone, 
                        body="Your order will be with you in 55 minutes!\n" +
                            "Order summary:\n" +
                            "1x Apple Pie @ £3.50\n" +
                            "3x Banana Split @ £4.99\n" +
                            "---\n" +
                            "Total = £18.47\n" +
                            "---"
                        )