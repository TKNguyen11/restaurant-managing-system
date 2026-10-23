"""This program is a simple restaurant managing system."""

import os
import csv


class Order:
    """
    Represents an order with a dish name, price, and an optional special request.
    Args:
         dish: Name of the dish
         price: price of the dish
         request: extra request for the dish

    Attributes:
         dish: Stores dish
         price: Stores price
         request: Stores request

    Returns: The dish with its price and extra request, if there is one.

    >>> order1 = Order("BEER", 4.00)
    >>> print(order1)
    BEER: 4.00 €
    
    >>> order2 = Order("FOREST-BURGER", 12.00, "Extra Patty")
    >>> print(order2)
    FOREST-BURGER (Special Request: Extra Patty): 13.00 €
    
    >>> order3 = Order("PIZZA-HAWAI", 10.00, "Extra Ananas")
    >>> print(order3)
    PIZZA-HAWAI (Special Request: Extra Ananas): 11.00 €
    """
    
    def __init__(self, dish, price, request=""):
        """
        Initialize order details.
        Args:
             dish: Name of the dish
             price: Price of the dish
             request: Extra request for the dish
        """
        
        self.dish = dish 
        self.price = price + 1 if request else price  # Adds 1 to the price if there is a special request
        self.request = request


    def __str__(self):
        """Returns a string representation of the order."""
        
        request_text = f" (Special Request: {self.request})" if self.request else ""
        return f"{self.dish}{request_text}: {self.price:.2f} €"


class Table:
    """
    Represents a table in the restaurant, managing its orders.
    Args:
         num: Table number
         dish: Name of the dish
         price: Price of the dish
         request: Extra request for the dish

    Attributes:
         num: Stores num

    Returns: The bill for the table as a .txt.

    >>> order4 = Table(1)
    >>> order4.add_order("PIZZA-MOZAARELLA", 10.00)
    Order added: PIZZA-MOZAARELLA: 10.00 €
    
    >>> order4.add_order("ICE-TEE (LEMON)", 4.00)
    Order added: ICE-TEE (LEMON): 4.00 €
    
    >>> order4.cancel_order("PIZZA-MOZAARELLA")
    Order for 'PIZZA-MOZAARELLA' was successfully canceled.
    
    >>> order4.create_bill()
    Bill for Table 1 saved in 'bill_table_1.txt'.   
    """
    
    def __init__(self, num):
        """
        Initialize table number and an empty list to store orders.
        Args:
             num: Table number
        """
        
        self.num = num
        self.orders = []  # Empty list to store orders for this table
        

    def add_order(self, dish, price, request=""):
        """
        Adds an order to the table.
        Args:
             dish: Name of the dish
             price: Price of the dish
             request: Extra request for the dish

        Returns:
             The added order.
        """
        
        order = Order(dish, price, request)
        self.orders.append(order)
        print(f"Order added: {order}")
        

    def cancel_order(self, dish):
        """
        Cancels an order by dish name.
        Args:
             dish: Name of the dish

        Returns:
             If the dish was succesfully canceled or if it couldnt be found.
        """
        
        for order in self.orders:
            if order.dish == dish:
                self.orders.remove(order)
                print(f"Order for '{dish}' was successfully canceled.")
                return
        print(f"No order for '{dish}' found.")
        

    def create_bill(self):
        """
        Creates and saves a bill for the table, listing all orders.
        Returns:
            Bill as a .txt.
        """
        
        if not self.orders:
            print(f"No orders for Table {self.num}.")
            return

        total = sum(order.price for order in self.orders)
        filename = f"bill_table_{self.num}.txt"
        # Write the bill to a text file.
        with open(filename, "w", encoding="utf-8") as file:
            file.write(f"Bill for Table {self.num}\n")
            for order in self.orders:
                file.write(f"{order}\n")
            file.write(f"Total: {total:.2f} €\n")

        print(f"Bill for Table {self.num} saved in '{filename}'.")


class Restaurant:
    """
    Manages multiple tables in the restaurant.
    Args:
         num_tables: Number of tables
         num: Table number

    Returns:
         Every table with its amount of orders.  
    """
    
    def __init__(self, num_tables):
        """
        Create a list of tables with the specified number.
        Args:
             num_tables: Number of tables
        """
        
        self.tables = [Table(i + 1) for i in range(num_tables)]  # Creates a list of tables
        

    def get_table(self, num):
        """
        Retrieves a table by its number.
        Args:
             num: Table number
        Returns:
             None if the table exists, error message if it does not.
        """
        
        if 1 <= num <= len(self.tables):
            return self.tables[num - 1]
        else:
            print("Invalid table number!")
            return None
        

    def show_tables(self):
        """
        Displays the number of orders for each table.
        Returns:
             Tables and their amount of orders.
        """
        
        for table in self.tables:
            print(f"Table {table.num}: {len(table.orders)} orders")


class Menu:
    """
    Loads and displays the menu from a CSV file.
    Args:
         csv_file: Placeholder for "food.csv"
         name: Name of the dishes in "food.csv"
    """
    
    def __init__(self, csv_file):
        """
        Load the menu from a CSV file.
        Args:
             csv_file: Placeholder for "food.csv"
        """
        
        self.products = self.load_menu(csv_file)
        

    def load_menu(self, csv_file):
        """
        Loads products from a CSV file into a list.
        Args:
             csv_file: Placeholder for "food.csv"

        Returns:
             Error message if the file was not found.     
        """
        
        products = []
        try:
            with open(csv_file, "r", encoding="utf-8") as file:
                reader = csv.reader(file, delimiter=';')
                next(reader)  # Skip the header line
                for row in reader:
                    try:
                        name, typ, category, price = row[0], row[1], row[2], float(row[3].replace(',', '.'))
                        products.append((name, price))
                    except (IndexError, ValueError):
                        print(f"Error in line: {row}")
        except FileNotFoundError:
            print(f"File '{csv_file}' not found.")
        return products
    

    def display_menu(self):
        """
        Displays the menu with available products.
        Returns:
             Menu or an error message if it could not be loaded.
        """
        
        if not self.products:
            print("The menu is empty or could not be loaded.")
            return
        for name, price in self.products:
            print(f"{name}: {price:.2f} €")
            

    def get_product_by_name(self, name):
        """
        Retrieves a product by its name.
        Args:
             name: Name of the dishes in "food.csv"
        Returns:
             None
        """
        
        for product_name, price in self.products:
            if product_name.lower() == name.lower():
                return product_name, price
        return None


def main():
    """
    Provides a console-based interface for managing the restaurant.
    """
    
    menu = Menu("food.csv")
    restaurant = Restaurant(3)  # Create a restaurant with 3 tables

    while True:
        print("\n--- Restaurant Management ---")
        print("1. Display Menu")
        print("2. Add Order")
        print("3. Cancel Order")
        print("4. Create Bill")
        print("5. Show All Tables")
        print("6. Exit")

        choice = input("Choose an option (1-6): ")

        if choice == "1":
            menu.display_menu()

        elif choice == "2":
            try:
                table_num = int(input("Enter table number: "))
                table = restaurant.get_table(table_num)
                if table:
                    product_name = input("Enter product name: ")
                    product = menu.get_product_by_name(product_name)
                    if product:
                        special_request = input("Special request (optional): ")
                        table.add_order(product[0], product[1], special_request)
                    else:
                        print("Product not found.")
            except ValueError:
                print("Invalid input! Please enter a number.")

        elif choice == "3":
            try:
                table_num = int(input("Enter table number: "))
                table = restaurant.get_table(table_num)
                if table:
                    dish_name = input("Enter the name of the dish to cancel: ")
                    table.cancel_order(dish_name)
            except ValueError:
                print("Invalid input! Please enter a number.")

        elif choice == "4":
            try:
                table_num = int(input("Enter table number: "))
                table = restaurant.get_table(table_num)
                if table:
                    table.create_bill()
            except ValueError:
                print("Invalid input! Please enter a number.")

        elif choice == "5":
            restaurant.show_tables()

        elif choice == "6":
            print("Program exited.")
            break

        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()

if __name__ == "__main__":
    import doctest
    doctest.testmod()

    # Test cases for Order class
    order1 = Order("BEER", 4.00)
    print(order1)
    
    order2 = Order("FOREST-BURGER", 12.00, "Extra Patty")
    print(order2)
    
    order3 = Order("PIZZA-HAWAI", 10.00, "Extra Ananas")
    print(order3)


    # Test cases for Table class
    order4 = Table(1)
    order4.add_order("PIZZA-MOZAARELLA", 10.00)
    
    order4.add_order("ICE-TEE (LEMON)", 4.00)

    order4.cancel_order("PIZZA-MOZAARELLA")
    
    order4.create_bill()


    
    

