class Order:
    def __init__(self, menu):
        self._verified = False
        self.items = {}
        self.menu = menu
    
    def is_verified(self):
        """Returns whether the order has been verified by the customer"""
        return self._verified
    
    def add_item(self, item, quantity):
        """Adds quantity of item to the order - stored in .items"""
        if not self.menu.is_dish(item):
            raise ValueError(f"{item} is not on the menu")
        elif not item in self.items.keys():
            self.items.update({item: quantity})
            self._verified = False
        else:
            self.items[item] += quantity
            self._verified = False

    def remove_item(self, item, quantity):
        """Removes quantity of item from the order, and removes item as a
        key from .items if .items[item] = 0"""
        if not item in self.items.keys():
            raise ValueError(f"{item} is not in the order")
        elif quantity > self.items[item]:
            raise ValueError(f"The order has only {self.items[item]}x {item}")
        elif quantity == self.items[item]:
            self.items.pop(item)
            self._verified = False
        else:
            self.items[item] -= quantity
            self._verified = False

    def show(self):
        if len(self.items) == 0:
            return "There are no items in your order."
        else:
            receipt = "Your current order is:\n"
            prices = []
            quantities = []
            for item in self.items.keys():
                prices.append(self.menu.get_price(item))
                quantities.append(self.items[item])
                receipt += f"{quantities[-1]}x "
                receipt += f"{item} @ £{'{0:.2f}'.format(prices[-1])}\n"
            total = sum([price * quantity for price, quantity 
                         in zip(prices, quantities)])
            receipt += "---\n" + f"Total = £{'{0:.2f}'.format(total)}\n"
            receipt += "---"
            return receipt

    def verify(self):
        if len(self.items) == 0:
            raise Exception("Cannot verify an empty order. " + 
                            "Please cancel or add items.")
        else:
            self._verified = True