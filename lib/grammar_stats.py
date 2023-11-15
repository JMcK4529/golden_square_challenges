class GrammarStats:
    def __init__(self):
        self.checks = 0
        self.valid_checks = 0
        pass
  
    def check(self, text):
        # Parameters:
        #   text: string
        # Returns:
        #   bool: true if the text begins with a capital letter and ends with a
        #         sentence-ending punctuation mark, false otherwise
        if type(text) != str:
            raise TypeError("Text input must be a string")
        elif len(text) > 0 and text[-1] in [".", "!", "?"] and text[0].isupper():
            self.checks += 1
            self.valid_checks += 1
            return True
        else:
            self.checks += 1
            return False
        pass
  
    def percentage_good(self):
        # Returns:
        #   int: the percentage of texts checked so far that passed the check
        #        defined in the `check` method. The number 55 represents 55%.
        return round((self.valid_checks/self.checks) * 100)
        pass