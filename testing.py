#import pandas as pd
#import json
#author David Farr
#14 Dec 23

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
        print("To view available parts enter list(), optional category is category = cpu, gpu, psu, ram, motherboard or storage as a string.")
        print("To view shopping cart enter cart()")
        print("To build custom computer enter build(part_ids comma separated)")
        print("Remove Item from Cart with remove(part_ids)")
        print("Set Budget with budget(amount = int)")
        print("Add to the shopping cart with purchase(part_id)")
        print("View the shopping cart with cart()")
        print("Complete the purchase and checkout with checkout()")

        print("Please begin the process by selecting one of the below options to begin your experience!")
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
            self.list()
        elif user_choice == '2':
            self.cart()
        elif user_choice == '3':
            self.build()
        elif user_choice == '4':
            self.remove()
        elif user_choice == '5':
            self.budget()
        elif user_choice == '6':
            self.checkout()
        elif user_choice == '7':
            print("Thank you for visiting. Goodbye!")
            exit()
        else:
            print("Invalid choice. Please enter a number from 1 to 7.")

    def help(self):
        print('The following commands are accepted:')
        print('help() - lists all available commands and their function')
        print('list(category=optional)- List available part and all their attributes (ID, type, etc.) in the specified category')
        print('details(part_id)- Show details of the specified part')
        print('compatibility(part_id1,part_id2,..)- Check if compatibility between specified parts')
        print('build(part_ids comma seperated)- Remove specified part or computer from current shopping carts')
        print('compatibiility-build(none)- Check compatibility between all parts in current build configuration')
        print('budget(amount)- set customers budget')
        print('purchase(part_id)- Add the specified part to shopping cart')
        print('cart(none)- View the current shopping cart')
        print('checkout(none)- Complete the purchase and checkout')


    def cart(self, category=None):
        print("Shopping Cart:")
        if not self.shopping_cart:
            print("Your cart is empty.")
        else:
            for item in self.shopping_cart:
                print(f"Part ID: {item['part_id']}")
                print("Details:")
                print(item['part_details'])
                print("--------------")

    def list(self, category=None):
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

    def details(self, part_id):
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

    def purchase(self, part_id):
        part = self.find_part_by_id(part_id) # Call function to ID part
        if part:
            part_cost = part['price'] 

            if self.customer:
                if self.customer['budget'] >= part_cost:
                    # Add the part to the shopping cart
                    self.shopping_cart.append({
                        'part_id': part_id,
                        'part_details': part  # Store the details of the part in the cart
                    })

                    # Deduct the cost of the part from the customer's budget
                    self.customer['budget'] -= part_cost
                    print(f"Part ID: {part_id} added to the cart. Remaining budget: {self.customer['budget']}")
                else:
                    print("Insufficient budget to purchase this part.")
            else:
                print("Customer information is not available. Please set the customer's budget first.")
        else:
            print("Part not found in inventory.")

    
    def find_part_by_id(self, part_id):
        # logic to find and return part details based on part_id from the inventory
        # Return the part details if found, otherwise return None
        for df in [self.df_cpu, self.df_gpu, self.df_ram, self.df_psu, self.df_motherboard, self.df_storage]:
            part = df[df['item_id'] == part_id]
            if not part.empty:
                return part.to_dict(orient='records')[0]

        return None  # Return None after checking all DataFrames


    def remove(self, part_id):
        # Remove a component or a custom-built computer from the shopping cart
        found = False
        for item in self.shopping_cart:
            if item['part_id'] == part_id:
                self.shopping_cart.remove(item)
                print(f"Part ID: {part_id} removed from the cart.")
                found = True
                break

            if not found:
                print(f"Part ID: {part_id} not found in the cart.")

    def build(self, parts):
        required_parts = {
            'Motherboard': 1,
            'RAM': 1,
            'CPU': 1,
            'PSU': 1,
            'Storage': 1,
            'GPU': 0
        }

        part_count = {part_type: 0 for part_type in required_parts}
        total_cost = 0
        computer_parts = []
        for part_id in parts.split(','):
            part = self.find_part_by_id(part_id)
            if part:
                part_type = part['item_type']
                if part_type in required_parts:
                    part_count[part_type] += 1
                    total_cost += part['price']
                    computer_parts.append(part)
        # Check if all required parts are present and within budget

        requirements_met = True
        missing_parts = []
        customer_budget = self.customer.get('budget')

        if customer_budget is None:
            customer_budget = float('inf') # If no budget provided assume unlimited

        for part_type, count in required_parts.items():
            if part_count[part_type] < count:
                requirements_met = False
                missing_parts.append(f"{count - part_count[part_type]}")
        
        if requirements_met:
            if total_cost <= customer_budget:
            # Assemble the computer parts into a build configuration
                computer_parts = []
                for part_id in parts.split(','):
                    part = self.find_part_by_id(part_id)
                    if part:
                        computer_parts.append(part)
            # Check compatibility before adding to the cart
                if self.check_compatibility(computer_parts):
                    print("Custom computer can be built!")
                    self.shopping_cart.append({
                        'computer_name': 'Custom',
                        'parts': computer_parts,
                        'total_cost': total_cost
                    })
                else:
                    print("The selected parts are not compatible. Please review your selection.")
            else:
                print("The total cost exceeds the customer's budget.")
        else:
            print(f"Missing parts: {', '.join(missing_parts)}")
            


            

    def compatibility(self, build_parts):
        # Extract component data from build_parts
        motherboard = next((part for part in build_parts if part['part_type'] == 'Motherboard'), None)
        cpu = next((part for part in build_parts if part['part_type'] == 'CPU'), None)
        ram = [part for part in build_parts if part['part_type'] == 'RAM']
        psu = next((part for part in build_parts if part['part_type'] == 'PSU'), None)

        # Check compatibility rules
        if motherboard and cpu and motherboard['socket'] != cpu['socket']:
            print("Warning: Motherboard and CPU socket types are incompatible.")
            return False

        if len(set(part['id'] for part in ram)) != 1:
            print("Warning: All instances of RAM should have the same ID.")
            return False

        if motherboard and len(ram) > motherboard['ram_slots']:
            print("Warning: More RAM modules than available RAM slots on the motherboard.")
            return False

        total_power_draw = sum(part['power_draw'] for part in build_parts if part['part_type'] != 'PSU')
        if psu and total_power_draw > psu['power_supplied']:
            print("Warning: Total power draw exceeds PSU capacity.")
            return False

        return True


    def budget(self):
        # Allows a user to update their budget
        if self.customer:
            try:
                new_budget = float(input("Please enter your new budget: "))
                self.customer['budget'] = new_budget
                print("Budget updated successfully!")
            except ValueError:
                print("Invalid input for the budget. Please enter a valid number.")        
                
    def checkout(self):
        # Complete the purchase and checkout process
        if not self.shopping_cart:
            print("Your shopping cart is empty.")
            return
        
        # Extract the parts from the shopping cart
        parts_in_cart = [item['part_details'] for item in self.shopping_cart]

        total_cost = sum(item['part_details']['price'] for item in self.shopping_cart)

        if self.customer:
            if total_cost <= self.customer.get('budget', float('inf')):
                print("Purchase successful! Thank you for shopping with us.")

                #clear shopping cart
                self.shopping_cart = []
            else:
                print("The total cost exceeds the customer's budget.")
        else:
            print("Customer information is not available. Please set the customer information with the")




    
