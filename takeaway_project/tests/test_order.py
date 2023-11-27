import pytest
from lib.order import Order
from unittest.mock import Mock

def test_new_instance_of_order_has_empty_items_dict():
    """Checks that .items is an empty dict at instantiation"""
    menu_mock = Mock()
    order = Order(menu_mock)
    assert order.items == {}

def test_order_has_menu_attribute():
    """Checks that menu passed as arg is stored as class variable"""
    menu_mock = Mock()
    order = Order(menu_mock)
    assert order.menu == menu_mock

def test_is_verified_returns_false_immediately():
    """Checks that ._verified = False at instantiation
    Implicitly checks .is_verified for ._verified = False"""
    menu_mock = Mock()
    order = Order(menu_mock)
    assert order.is_verified() == False

def test_add_item_updates_items_dict():
    """Checks that .add_item updates .items with name and quantity of dish"""
    menu_mock = Mock()
    menu_mock.is_dish.return_value = True
    order = Order(menu_mock)
    order.add_item("Apple Pie", 1)
    menu_mock.is_dish.assert_called_with("Apple Pie")
    assert order.items == {"Apple Pie": 1}
    order.add_item("Banana Split", 4)
    menu_mock.is_dish.assert_called_with("Banana Split")
    assert order.items == {"Apple Pie": 1, "Banana Split": 4}

def test_add_item_does_not_overwrite_quantity():
    """Checks that .add_item updates quantities, rather than resetting them"""
    menu_mock = Mock()
    menu_mock.is_dish.return_value = True
    order = Order(menu_mock)
    order.add_item("Apple Pie", 1)
    order.add_item("Banana Split", 4)
    order.add_item("Apple Pie", 2)
    try:
        menu_mock.is_dish.assert_called_once_with("Apple Pie")
        assert False
    except AssertionError:
        pass
    assert order.items == {"Apple Pie": 3, "Banana Split": 4}

def test_add_non_menu_item_raises_exception():
    """Checks that only menu items can be added to .items"""
    menu_mock = Mock()
    menu_mock.is_dish.return_value = False
    order = Order(menu_mock)
    with pytest.raises(ValueError) as err:
        order.add_item("Zebrafish Steak", 1)
    assert str(err.value) == "Zebrafish Steak is not on the menu"
    menu_mock.is_dish.assert_called_with("Zebrafish Steak")

def test_remove_item_updates_items_dict():
    """Checks that .remove_item adjusts quantities in .items"""
    menu_mock = Mock()
    menu_mock.is_dish.return_value = True
    order = Order(menu_mock)
    order.add_item("Apple Pie", 1)
    order.add_item("Banana Split", 4)
    order.remove_item("Banana Split", 3)
    assert order.items == {"Apple Pie": 1, "Banana Split": 1}

def test_remove_item_full_quantity_removes_key_from_dict():
    """Checks that .remove_item removes the key when quantity reduced to 0"""
    menu_mock = Mock()
    menu_mock.is_dish.return_value = True
    order = Order(menu_mock)
    order.add_item("Apple Pie", 1)
    order.add_item("Banana Split", 4)
    order.remove_item("Apple Pie", 1)
    assert order.items == {"Banana Split": 4}

def test_remove_item_over_quantity_raises_exception():
    """Checks that .remove_item cannot set quantities < 0"""
    menu_mock = Mock()
    menu_mock.is_dish.return_value = True
    order = Order(menu_mock)
    order.add_item("Apple Pie", 1)
    order.add_item("Banana Split", 4)
    with pytest.raises(ValueError) as err:
        order.remove_item("Apple Pie", 2)
    assert str(err.value) == "The order has only 1x Apple Pie"

def test_remove_non_order_item_raises_exception():
    """Checks that an exception is raised when .remove_item is passed
    an item that is not in the order"""
    menu_mock = Mock()
    order = Order(menu_mock)
    with pytest.raises(ValueError) as err:
        order.remove_item("Fake Item", 1)
    assert str(err.value) == "Fake Item is not in the order"

def test_show_returns_correct_format():
    """Checks that a correctly formatted string is returned by .show"""
    global check_count
    menu_mock = Mock()
    menu_mock.is_dish.return_value = True
    menu_mock.get_price = Mock(side_effect = [3.5, 4.99])

    order = Order(menu_mock)
    order.add_item("Apple Pie", 1)
    order.add_item("Banana Split", 4)
    assert order.show() == "Your current order is:\n" + \
                            "1x Apple Pie @ £3.50\n" + \
                            "4x Banana Split @ £4.99\n" + \
                            "---\n" + \
                            "Total = £23.46\n" + \
                            "---"

def test_show_empty_order():
    """Checks that .show returns a specific string for an empty order"""
    menu_mock = Mock()
    order = Order(menu_mock)
    assert order.show() == "There are no items in your order."

def test_verify_receipt():
    """Checks that .verify() sets ._verified to True
    Implicitly checks .is_verified for ._verified = True"""
    menu_mock = Mock()
    menu_mock.is_dish.return_value = True

    order = Order(menu_mock)
    order.add_item("Apple Pie", 1)
    order.verify()
    assert order.is_verified()

def test_verify_empty_order_raises_exception():
    """Checks that the order cannot be verified if it is empty"""
    menu_mock = Mock()
    order = Order(menu_mock)
    with pytest.raises(Exception) as err:
        order.verify()
    assert str(err.value) == "Cannot verify an empty order. " + \
                                "Please cancel or add items."

def test_add_or_remove_undoes_verification():
    """Checks that changes made to the order also reset ._verified = False"""
    menu_mock = Mock()
    menu_mock.is_dish.return_value = True
    order = Order(menu_mock)
    order.add_item("Apple Pie", 2)
    order.verify()
    assert order.is_verified()
    order.add_item("Banana Split", 3)
    assert order.is_verified() == False
    order.verify()
    assert order.is_verified()
    order.remove_item("Apple Pie", 1)
    assert order.is_verified() == False