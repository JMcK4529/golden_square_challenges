import os

class Menu:
    def __init__(self):
        self._menu = {"Apple Pie": {"price": 3.5, "cook_time": 35},
                      "Banana Split": {"price": 4.99, "cook_time": 5}}
        self._delivery_time = 20

    def is_dish(self, dish):
        if dish in self._menu.keys():
            return True
        else:
            return False
        
    def get_price(self, dish):
        if self.is_dish(dish):
            return self._menu[dish]["price"]
        else:
            raise ValueError(f"{dish} is not on the menu")
    
    def price_list(self):
        prices = []
        for dish in self._menu.keys():
            prices.append(
                f"{dish}: £{'{0:.2f}'.format(self._menu[dish]['price'])}"
                )
        return("\n".join(prices))
    
    def order_time(self, order):
        if order.is_verified():
            return max(
                self._menu[dish]["cook_time"] for dish in order.items.keys()
                ) + self._delivery_time
        else:
            raise Exception("Order must be verified to deliver")
    
    def send_notification(self, order, ClientClass, customer_phone):
        account_sid = os.environ['TWILIO_ACCOUNT_SID']
        auth_token = os.environ['TWILIO_AUTH_TOKEN']
        from_phone = os.environ['TWILIO_PHONE']
    
        client = ClientClass(account_sid, auth_token)
        message = f"Your order will be with you in {self.order_time(order)} minutes!\n" + \
            "Order summary:\n" + \
                f"{order.show()[23:]}"
        client.messages.create(to=customer_phone, 
                               from_=from_phone, 
                               body=message)
        return message