import pytest
from lib.contact import *

def test_init_wrong_type():
    with pytest.raises(TypeError) as err:
        contact = Contact("name", 123)
    assert str(err.value) == "Phone number must be a string"

    with pytest.raises(TypeError) as err:
        contact = Contact(123,"0123456789")
    assert str(err.value) == "Name must be a string"

def test_init_wrong_value_number():
    with pytest.raises(ValueError) as err:
        contact = Contact("name", "1123456789")
    assert str(err.value) == "Phone numbers must begin with 0"

def test_empty_string():
    with pytest.raises(ValueError) as err:
        contact = Contact("", "0123456789")
    assert str(err.value) == "Empty string cannot be a name"

def test_correct_contact_info():
    contact = Contact("Some Guy", "01234567890")
    assert (contact.name, contact.number) == ("Some Guy", "01234567890")

def test_format_contact():
    contact = Contact("Some Guy", "01234567890")
    assert contact.format() == "Some Guy: 01234567890"