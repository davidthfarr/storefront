#import pandas as pd
#import json


class computer_store:

    def __init__(self, inventory_data):
        self.inventory = self.load_inventory(inventory_data)
        self.shopping_cart = []
        self.customer = None
        self.df_cpu = None
        self.df_gpu = None
        self.df_ram = None
        self.df_psu = None
        self.df_motherboard = None
        self.df_storage = None

    def load_inventory(self, inventory_data):
        # Parse inventory data and create component instances
        # Populate the inventory with components
        # Read JSON data from the file

        with open('inventory.json', 'r') as file:
            json_data = json.load(file)

        # Extract the 'inventory' list from the JSON
        inventory_data = json_data['inventory']

        # Normalize the JSON data into a DataFrame
        df = pd.json_normalize(inventory_data, sep='_')

        # Creating another object using groupby
        grouped = df.groupby('item_type')

        # Creating dataframes from the object 
        self.df_cpu = grouped.get_group('CPU').dropna(axis='columns')
        self.df_gpu = grouped.get_group('GPU').dropna(axis='columns')
        self.df_ram = grouped.get_group('RAM').dropna(axis='columns')
        self.df_psu = grouped.get_group('PSU').dropna(axis='columns')
        self.df_motherboard = grouped.get_group('Motherboard').dropna(axis='columns')
        self.df_storage = grouped.get_group('Storage').dropna(axis='columns')

        return inventory_data #Return processed inventory data

    def customer_info(self):
        customer_name = input("Please enter your name: ")
        try:
            customer_budget = float(input("Please enter your budget: "))
            # Assuming the budget entered is a float value
            return customer_name, customer_budget
        except ValueError:
            print("Invalid input for budget. Please enter a valid number.")
            return None, None

    def display_menu(self):
        print("Welcome to the Computer Store!")
        print("1. View Available Parts")
        print("2. View Shopping Cart")
        print("3. Build Custom Computer")
        print("4. Remove Item from Cart")
        print("5. Set Budget")
        print("6. Checkout")
        print("7. Exit")

        user_choice = input("Please enter your choice (1-7): ")

        # Process user input
        if user_choice == '1':
            self.display_inventory()
        elif user_choice == '2':
            self.display_cart()
        elif user_choice == '3':
            self.build_custom_computer_menu()
        elif user_choice == '4':
            self.remove_from_cart_menu()
        elif user_choice == '5':
            self.set_budget_menu()
        elif user_choice == '6':
            self.checkout()
        elif user_choice == '7':
            print("Thank you for visiting. Goodbye!")
            exit()
        else:
            print("Invalid choice. Please enter a number from 1 to 7.")

    # Additional methods for menu options would go here

    def display_cart(self, category=None):
        print("Shopping Cart:")
        if not self.shopping_cart:
            print("Your cart is empty.")
        else:
            for item in self.shopping_cart:
                print(f"Part ID: {item['part_id']}")
                print("Details:")
                print(item['part_details'])
                print("--------------")

    def display_inventory(self, category=None):
        print("Available Parts:")
        if category is None:
            # Display all available parts if no specific category is specified
            print("---- CPU ----")
            print(self.df_cpu)
            print("---- GPU ----")
            print(self.df_gpu)
            print("---- RAM ----")
            print(self.df_ram)
            print("---- PSU ----")
            print(self.df_psu)
            print("---- Motherboard ----")
            print(self.df_motherboard)
            print("---- Storage ----")
            print(self.df_storage)
            # Display other component types in a similar manner for RAM, PSU, etc.
            # self.df_ram, self.df_psu, etc.
        else:
            # Display parts in the specified category
            if category.lower() == 'cpu':
                print("---- CPU ----")
                print(self.df_cpu)
            elif category.lower() == 'gpu':
                print("---- GPU ----")
                print(self.df_gpu)
            elif category.lower() == 'ram':
                print("---- RAM ----")
                print(self.df_ram)
            elif category.lower() == 'psu':
                print("---- PSU ----")
                print(self.df_psu)
            elif category.lower() == 'Motherboard':
                print("---- Motherboard ----")
                print(self.df_motherboard)
            elif category.lower() == 'Storage':
                print("---- Storage ----")
                print(self.df_storage)

    def display_details(self, part_id):
        # Check the DataFrames for the part based on its ID
        part = None
        category = None

        # Search for the part in different component DataFrames
        for category_df in [self.df_cpu, self.df_gpu, self.df_ram, self.df_psu, self.df_motherboard, self.df_storage]:
            if part_id in category_df['item_id'].values:
                part = category_df[category_df['item_id'] == part_id].iloc[0]
                category = category_df['item_type'].iloc[0]
                break

        if part is not None:
            print(f"Details for Part ID: {part_id} (Category: {category})")
            print(part)
        else:
            print(f"Part with ID {part_id} not found in inventory.")

    def add_to_cart(self, part):
        # Add a selected part or custom-built onent or a custom-built computer from the shopping cart
        part = self.find_part_by_id(part_id)
        if part:
            # Add the part to the shopping cart
            self.shopping_cart.append({
                'part_id': part_id,
                'quantity': quantity,
                'part_details': part  # You can store the details of the part in the cart
            })
            print(f"Added {quantity} {part['item_type']}(s) to the cart.")
        else:
            print("Part not found in inventory.")
    
    def find_part_by_id(self, part_id):
        # logic to find and return part details based on part_id from the inventory
        # Return the partdetails if found, otherwise return None
        for df in [self.df_cpu, self.df_gpu, self.df_ram, self.df_psu, self.df_motherboard, self.df_storage]:
            part = df[df['item_id'] == part.id]
            if not part.empty:
                return part.to_dict(orient='records')[0]
            
            return None

    def remove_from_cart(self, part):
        # Remove a component or a custom-built computer from the shopping cart
        pass

    def build_custom_computer(self, parts):
        # Build a custom computer with specified parts
        # Add the computer to the shopping cart
        pass

    def check_compatibility(self):
        # Check compatibility between components in the shopping cart
        pass

    def set_budget(self, budget_amount):
        # Set the budget for the current customer
        pass

    def checkout(self):
        # Complete the purchase and checkout process
        # Consider the budget and compatibility before finalizing the purchase
        pass




    