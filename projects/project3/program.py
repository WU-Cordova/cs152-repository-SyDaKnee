from datastructures.array import Array
from datastructures.linkedlist import LinkedList
from datastructures.hashmap import HashMap
from datastructures.deque import Deque

RED = "\033[91m"
YELLOW = "\033[93m"
# https://gist.github.com/nazwadi/ca00352cd0d20b640efd - I took the color codes from here.

class Drink:
    def __init__(self, name: str, prices: dict[str, float]):
        self.name = name
        self.prices = prices
    
    def get_price(self, size: str) -> float:
        return self.prices.get(size, 0.0)
    
    def __str__(self):
        prices_display = ", ".join([f"{size}: &{price:.2f}" for size, price in self.prices.items()])
        return f"{self.name} ({prices_display})"


class OrderItem:
    def __init__(self, drink: Drink, size: str, customization: str = ""):
        self.drink = drink
        self.size = size
        self.customization = customization

    def __str__(self):
        if self.customization:
            return f"{self.drink.name} ({self.size}) - {self.customization}"
        return f"{self.drink.name} ({self.size})"


class CustomerOrder:
    def __init__(self, customer_name: str):
        self.customer_name = customer_name
        self.items = LinkedList(OrderItem)

    def add_item(self, item: OrderItem):
        self.items.append(item)

    def __str__(self):
        return f"{self.customer_name}: " + ", ".join(str(item) for item in self.items)


class BistroSystem:
    def __init__(self):
        self.menu = Array([ # Initializing pricing in terms of drink and size. 
            Drink("Bearcat Mocha", {"Small": 4.00, "Medium": 4.50, "Large": 5.00}),
            Drink("Caramel Catpuccino", {"Small": 3.75, "Medium": 4.25, "Large": 5.25}),
            Drink("Meowcha Latte", {"Small": 4.25, "Medium": 4.75, "Large": 4.50}),
            Drink("Vanilla Purrccino", {"Small": 3.50, "Medium": 4.00, "Large": 4.50}),
            Drink("Espresso Whisker Shot", {"Small": 3.00, "Medium": 3.50, "Large": 4.00}),
        ], data_type = Drink)
        self.open_orders = Deque(data_type = CustomerOrder)
        self.completed_orders = LinkedList(CustomerOrder)
        self.sales_summary = HashMap()

    def display_menu(self):
        print("\n☕ Bearcat Bistro Menu ☕")
        for idx, drink in enumerate(self.menu, start = 1):
            print(f"{idx}. {drink}")

    def take_new_order(self):
        print("\nTaking a New Order:")
        name = input("What's a good name? ")
        order = CustomerOrder(name)
        num_drinks = int(input("How many drinks would you like to order? "))

        for i in range(num_drinks):
            drink_num = int(input(f"\nDrink #{i + 1}: Enter the drink number from the menu. (1-5): "))
            drink = self.menu[drink_num - 1]

            size = input(f"What size would you like for the {drink.name} (Small/Medium?Large): ").capitalize()
            while not size in ["Small", "Medium", "Large"]:
                size = input("We don't have that size. Please choose Small, Medium, or Large: ").capitalize()

            customization = input(f"Any customization for your {drink.name}? (Press 'Enter' if none): ")
            order.add_item(OrderItem(drink, size, customization))

        print("\nOrder Summary:")
        for item in order.items:
            print(f"- {item}")

        confirm = input("\nIs this order correct? (yes/no): ").lower()
        if confirm == "yes":
            self.open_orders.enqueue(order)
            print("\nYour order was placed successfully!")
        else:
            print("\nYour order was canceled.")

    def view_open_orders(self):
        print("\nOpen Orders:")
        if self.open_orders.empty():
            print("There are no open orders.")
            return

        for idx, order in enumerate(self.open_orders, start = 1):
            print(f"{idx}. {order.customer_name}: ", end="")
            drink_list = []
            for item in order.items:
                if item.customization:
                    drink_list.append(f"{item.drink.name} ({item.customization})")
                else:
                    drink_list.append(f"{item.drink.name}")
        print(", ".join(drink_list))

    def mark_next_order_complete(self):
        print("\nCompleting the Next Order:")
        if self.open_orders.empty():
            print("There are no orders to complete.")
            return
        
        completed_order = self.open_orders.dequeue()
        self.completed_orders.append(completed_order)

        for item in completed_order.items:
            drink_name = item.drink.name
            price = item.drink.get_price(item.size)

            if drink_name in self.sales_summary:
                count, total = self.sales_summary[drink_name]
                self.sales_summary[drink_name] = (count + 1, total + price)
            else:
                self.sales_summary[drink_name] = (1, price)
        
        print(f"\n ✅ Completed Order for {completed_order.customer_name}! ✅")

    def end_of_day_report(self):
        print("\n📝 End-of-Day Report 📝")
        print("-" * 40)
        print(f"{'Drink Name':<25}{'Qty Sold':<10}{'Total Sales'}")
        total_revenue = 0.0

        for drink_name in self.sales_summary:
            count, total = self.sales_summary[drink_name]
            print(f"{drink_name:<25}{count:<10}{'$' + format(total, '.2f')}")
            total_revenue += total

        print("-" * 40)
        print(f"{'Total Revenue:':<35}${total_revenue:.2f}") # Prefixing the total revenue with a dollar sign, make sure it goes to two decimal places. 

    def run(self):

        print(f"{YELLOW}" + "=" * 40)
        print(f"{RED}" "🐾 Welcome to the Bearcat Bistro Ordering System! 🐾")
        print(f"{YELLOW}" + "=" * 40)

        while True:
            print("\n 📋 Main Menu 📋")
            print("1. Display Menu")
            print("2. Take New Order")
            print ("3. View Open Orders")
            print ("4. Mark Next Order as Complete")
            print ("5. View End-of-Day Report")
            print("6. Exit")

            choice = input("\nEnter your choice: ")
            if choice == "1":
                self.display_menu()
            elif choice == "2":
                self.take_new_order()
            elif choice == "3":
                self.view_open_orders()
            elif choice == "4":
                self.mark_next_order_complete()
            elif choice == "5":
                self.end_of_day_report()
            elif choice == "6":
                print("\nThanks for stopping by!")
                break
            else:
                print("\nThat's an invalid choice. Please try again.")


if __name__ == '__main__':
    system = BistroSystem()
    system.run()

