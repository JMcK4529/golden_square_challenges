class Contact:
    def __init__(self, name, number):
        if type(number) != str:
            raise TypeError("Phone number must be a string")
        elif type(name) != str:
            raise TypeError("Name must be a string")
        elif number[0] != "0":
            raise ValueError("Phone numbers must begin with 0")
        elif name == "":
            raise ValueError("Empty string cannot be a name")
        else:
            self.name = name
            self.number = number

    def format(self):
        return f"{self.name}: {self.number}"