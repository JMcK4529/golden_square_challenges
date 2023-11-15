class VowelRemover:
    def __init__(self, text):
        self.text = text
        self.vowels = ["a", "e", "i", "o", "u"]

    def remove_vowels(self):
        i = 0
        while i < len(self.text):
            print(i)
            if self.text[i].lower() in self.vowels:
                print(self.text)
                self.text = self.text[:i] + self.text[i+1:]
                print(self.text)
            else:
                i += 1
        return self.text