def is_grammar_correct(text):
    if type(text) != str:
        raise TypeError("Input was not a string")
    elif len(text) > 0 and text[-1] in [".", "?", "!"] and text[0].upper() == text[0]:
        return True
    else:
        return False

