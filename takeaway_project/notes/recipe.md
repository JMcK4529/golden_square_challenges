## User Stories
> As a customer  
> So that I can check if I want to order something  
> I would like to see a list of dishes with prices.

> As a customer  
> So that I can order the meal I want  
> I would like to be able to select some number of several available dishes.

> As a customer  
> So that I can verify that my order is correct  
> I would like to see an itemised receipt with a grand total.

Using `twilio-python` and mocks:
> As a customer  
> So that I am reassured that my order will be delivered on time  
> I would like to receive a text such as "Thank you! Your order was placed and
> will be delivered before 18:52" after I have ordered.

Fair warning: if you push your Twilio API Key to a public GitHub repository,
anyone will be able to see and use it. What are the security implications of
that? How will you keep that information out of your repository?

## Design
Split into UserInterface, Menu and Order classes

### Menu
Menu._menu = {"dish1": {"price": float(£), "cook_time": int(minutes)}}  
example => 
```python
my_menu = Menu()
# my_menu._menu => {"Apple Pie": {"price": 3.5, "cook_time": 35}, "Banana Split": {"price": 4.99, "cook_time": 5}}
```

Menu.is_dish("dish") => returns True if "dish" is a key in Menu._menu
Menu.get_price("dish") => returns the price of "dish" if is_dish("dish")
Menu.price_list() => returns a formatted string with items and prices
example =>
```python
my_menu = Menu()
my_menu.price_list()
> "Apple Pie: £3.50"
> "Banana Split: £4.99"
```

Menu._delivery_time = int(minutes), the time taken to deliver after food is cooked (set at 20 mins)
Menu.order_time(Order) => returns the number of minutes taken to cook and deliver the food

Menu.send_notification(Order) => sends a text to the customer if Order is verified

### Order
Order._verified = False
Order.items = {}
Order.menu = Menu()
Order.add_item(dish, number) => Order.items["dish"] += int(number) for a dish in Menu
Order.remove_item(dish, number) => Order.items["dish"] -= int(number) for a dish in Order.items
Order.show() => returns the name of each item ordered, how many were ordered and the total price of the order
Order.verify() => sets Order._verified = True if len(Order.items) > 0
Order.is_verified() => returns Order._verified

### UserInterface
```
Welcome to Takeaway Ordering!
Here is the menu:
>> Menu.price_list()
Would you like to:
    - Add items to the order [add]
    - Remove items from the order [rm]
    - Confirm the order [ok]
    - Cancel the order [cancel]
<< add
Which item?
<< Apple Pie
How many?
<< 1
>> Order.add_item("Apple Pie", 1)
OK.
>> Order.show()
Your current order is:
1x Apple Pie @ £3.50
---
Total = £3.50
---
Would you like to:
    - Add items to the order [add]
    - Remove items from the order [rm]
    - Confirm the order [ok]
    - Cancel the order [cancel]
<< add
Which item?
<< Banana Split
How many?
<< 4
>> Order.add_item("Banana Split", 4)
OK.
>> Order.show()
Your current order is:
1x Apple Pie @ £3.50
4x Banana Split @ £4.99
---
Total = £23.46
---
Would you like to:
    - Add items to the order [add]
    - Remove items from the order [rm]
    - Confirm the order [ok]
    - Cancel the order [cancel]
<< rm
Which item?
<< Banana Split
How many?
<< 3
>> Order.remove_item("Banana Split", 3)
OK.
>> Order.show()
Your current order is:
1x Apple Pie @ £3.50
1x Banana Split @ £4.99
---
Total = £8.49
---
Would you like to:
    - Add items to the order [add]
    - Remove items from the order [rm]
    - Confirm the order [ok]
    - Cancel the order [cancel]
<< ok
>> Order.show()
Your current order is:
1x Apple Pie @ £3.50
1x Banana Split @ £4.99
---
Total = £8.49
---
Is that correct? [Y/N]
<< Y
>> Order.verify()
>> Order.get_contact_number()
Please enter your phone number:
<< 07234567890
>> Menu.send_notification(Order)
Confirmation of your order is being sent to your phone!
```
