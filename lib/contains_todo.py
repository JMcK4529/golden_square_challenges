def contains_todo(text):
    if type(text) != str:
        raise TypeError("The input was not a string.")
    elif "#TODO" in text:
        return True
    else:
        return False

