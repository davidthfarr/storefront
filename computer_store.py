import pandas as pd
import json
import sys
#author David Farr
#15 Dec 23

class computer_store:

    def __init__(self, inventory_data):
        self.inventory = None
        self.shopping_cart = []
        self.customer = None
        self.df_cpu = None
        self.df_gpu = None
        self.df_ram = None
        self.df_psu = None
        self.df_motherboard = None
        self.df_storage = None
        self.load_inventory(inventory_data)

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

        # Convert item_price column to int
        df['item_price'] = df['item_price'].astype(int)

        # Creating another object using groupby
        grouped = df.groupby('item_type')

        # Creating dataframes from the object 
        self.df_cpu = grouped.get_group('CPU').dropna(axis='columns')
        self.df_gpu = grouped.get_group('GPU').dropna(axis='columns')
        self.df_ram = grouped.get_group('RAM').dropna(axis='columns')
        self.df_psu = grouped.get_group('PSU').dropna(axis='columns')
        self.df_motherboard = grouped.get_group('Motherboard').dropna(axis='columns')
        self.df_storage = grouped.get_group('Storage').dropna(axis='columns')
        
        # Create front facing dataframe
        self.df_cpu_front = self.df_cpu.copy()
        self.df_gpu_front = self.df_gpu.copy()
        self.df_psu_front = self.df_psu.copy()
        self.df_ram_front = self.df_ram.copy()
        self.df_motherboard_front = self.df_motherboard.copy()
        self.df_storage_front = self.df_storage.copy()
        
        #Format front facing data frames
        self.df_cpu_front['item_price'] = self.df_cpu_front['item_price'].map('${:,.2f}'.format)
        self.df_cpu_front['item_power_draw'] = self.df_cpu_front['item_power_draw'].map('{:,.1f}W'.format)        
        self.df_gpu_front['item_price'] = self.df_gpu_front['item_price'].map('${:,.2f}'.format)
        self.df_gpu_front['item_power_draw'] = self.df_gpu_front['item_power_draw'].map('{:,.1f}W'.format) 
        self.df_ram_front['item_price'] = self.df_ram_front['item_price'].map('${:,.2f}'.format)
        self.df_ram_front['item_power_draw'] = self.df_ram_front['item_power_draw'].map('{:,.1f}W'.format)
        self.df_ram_front['item_capacity'] = self.df_ram_front['item_capacity'].map('{:,.0f}GB'.format)
        self.df_psu_front['item_price'] = self.df_psu_front['item_price'].map('${:,.2f}'.format)
        self.df_psu_front['item_power_supplied'] = self.df_psu_front['item_power_supplied'].map('{:,.1f}W'.format)
        self.df_motherboard_front['item_price'] = self.df_motherboard_front['item_price'].map('${:,.2f}'.format)
        self.df_motherboard_front['item_power_draw'] = self.df_motherboard_front['item_power_draw'].map('{:,.1f}W'.format)
        self.df_storage_front['item_price'] = self.df_storage_front['item_price'].map('${:,.2f}'.format)
        self.df_storage_front['item_capacity'] = self.df_storage_front['item_capacity'].map('{:,.0f}GB'.format)  

        return inventory_data #Return processed inventory data

    def customer_info(self):
        customer_name = input("Please enter your name: ")
        try:
            customer_budget = float(input("Please enter your budget: "))
            # Assuming the budget entered is a float value
            customer_budget_format = "${:.2f}".format(customer_budget)
            return customer_name, customer_budget_format
        except ValueError:
            print("Invalid input for budget. Please enter a valid number.")
            return None, None

        
    def run(self):
        print("Welcome to Pylandia's Computer Store! ")
        
        customer_name, customer_budget = self.customer_info()
        self.customer = {'name': customer_name, 'budget': float(customer_budget.replace('$',''))}
        
        print("If you need a pace to start, enter the command 'help' to view a full list of commands and how to use them! ")
        
        while True:
            user_input = input("Enter a command here: ")
            if user_input.lower() == 'exit':
                break   
            self.execute_command(user_input)
        
    def execute_command(self, command):
        if command.lower() == 'help':
            self.help()
        elif command.lower() == 'customer_info':
            self.customer_info()
        elif command.lower() == 'cart':
            self.cart()
        elif command.lower() == 'list':
            self.list()
        elif command.lower() == 'details':
            part_id = input('Enter a part ID here: ')
            self.details(part_id)
        elif command.lower() == 'add_to_cart':
            part_id = input('Enter a part ID here: ')
            self.add_to_cart(part_id)
        elif command.lower() == 'remove':
            part_id = input('Enter ID of the part you would like removed from your cart here: ')
            self.remove(part_id)
        elif command.lower() == 'remove':
            part_id = input('Enter a part ID here: ')
            self.remove()
        elif command.lower() == 'build':
            parts = input('Enter your computer parts as a comma separated list: ')
            self.build(parts)
        elif command.lower() == 'compatibility':
            parts = input('Enter your computer parts as a comma separated list: ')
            self.compatibility(parts)
        elif command.lower() == 'budget':
            self.budget()
        elif command.lower() == 'checkout':
            self.checkout()
        elif command.lower() == 'leave':
            self.leave()
        elif command.lower() == 'wallet':
            self.wallet()
        else:
            print('The specified command was not accepted. Please do not add on any spaces or extra characters after entering a command. For more instructions please enter help.')
        # Need to add list, details, purchase, remove, build, compatibility, budget, checkout, leave

    def help(self):
        print('')
        print('The following commands are accepted:')
        print('help - lists all available commands and their function')
        print('list - List available parts')
        print('details - Show details of a specified part. Part IDs ARE case sensitive')
        print('build - Enter parts with commas in between. Will check compatibility and then add all parts to cart for purchase')
        print('budget - set customers budget')
        print('customer_info - reset the customer name and budget')
        print('add_to_cart - Add the specified part via PART_ID to shopping cart. You will not be charged until checkout')
        print('remove - Delete a specified part ')
        print('cart - View the current shopping cart')
        print('wallet - Will show you the cost of items in your cart, your set budget, and your remaining bduget.')
        print('checkout - Complete the purchase and checkout')
        print('leave - Exits the store')


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
            print(self.df_cpu_front)
            print("---- GPU ----")
            print(self.df_gpu_front)
            print("---- RAM ----")
            print(self.df_ram_front)
            print("---- PSU ----")
            print(self.df_psu_front)
            print("---- Motherboard ----")
            print(self.df_motherboard_front)
            print("---- Storage ----")
            print(self.df_storage_front)
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
        for category_df in [self.df_cpu_front, self.df_gpu_front, self.df_ram_front, self.df_psu_front, self.df_motherboard_front, self.df_storage_front]:
            if part_id in category_df['item_id'].values:
                part = category_df[category_df['item_id'] == part_id].iloc[0]
                category = category_df['item_type'].iloc[0]
                break

        if part is not None:
            print(f"Details for Part ID: {part_id} (Category: {category})")
            print(part)
        else:
            print(f"Part with ID {part_id} not found in inventory.")

    def add_to_cart(self, part_id):
        part = self.find_part_by_id(part_id) # Call function to ID part
        if part:
            part_cost = part['item_price'] 
    
            if self.customer:
                # Check total cost of the cart
                total_cart_cost = sum(item['part_details']['item_price'] for item in self.shopping_cart)
                
                if self.customer['budget'] >= total_cart_cost + part_cost:
                    # Add the part to the shopping cart
                    self.shopping_cart.append({
                        'part_id': part_id,
                        'part_details': part  # Store the details of the part in the cart
                    })
    
                    print(f"Part ID: {part_id} added to the cart. Total cart cost: ${total_cart_cost + part_cost}")
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
    
        # Check if customer info is available, if not, prompt for it
        if not self.customer:
            customer_name, customer_budget = self.customer_info()
            self.customer = {'name': customer_name, 'budget': customer_budget}
        else:
            customer_name = self.customer['name']
            customer_budget = self.customer['budget']
    
        for part_id in parts.split(','):
            part = self.find_part_by_id(part_id.strip())
            if part:
                part_type = part['item_type']
                if part_type in required_parts:
                    part_count[part_type] += 1
                    total_cost += part['item_price']
                    computer_parts.append(part)
    
        requirements_met = all(part_count[part_type] >= count for part_type, count in required_parts.items())
    
        if requirements_met:
            #customer_budget_float = float(customer_budget.replace('$', '').replace(',', ''))
            if total_cost <= customer_budget:
                if self.compatibility(computer_parts):
                    print("Custom computer can be built!")
                    for part_id, part in zip(parts.split(','), computer_parts):
                        self.shopping_cart.append({
                            'computer_name': 'Custom',
                            'part_id': part_id,
                            'part_details': part,
                            'total_cost': total_cost # Store the details of the part in the cart'
                        })
                else:
                    print("The selected parts are not compatible. Please review your selection.")
            else:
                print("The total cost exceeds the customer's budget.")
        else:
            missing_parts = [f"{count - part_count[part_type]} {part_type}" for part_type, count in required_parts.items()
                             if part_count[part_type] < count]
            print(f"Missing parts: {', '.join(missing_parts)}")

  
    #Internal function for checking computer compatibility during build function
    def compatibility(self, build_parts):
        
        motherboard = next((part for part in build_parts if part['item_type'] == 'Motherboard'), None)
        cpu = next((part for part in build_parts if part['item_type'] == 'CPU'), None)
        ram = [part for part in build_parts if part['item_type'] == 'RAM']
        psu = next((part for part in build_parts if part['item_type'] == 'PSU'), None)
        gpu = [part for part in build_parts if part['item_type'] == 'GPU']
        storages = [part for part in build_parts if part['item_type'] == 'Storage']
        
        # Check compatibility rules
        if motherboard and cpu and motherboard['item_socket'] != cpu['item_socket']:
            print("Warning: Motherboard and CPU socket types are incompatible.")
            return False

        if len(set(part['item_id'] for part in ram)) != 1:
            print("Warning: All instances of RAM should have the same ID.")
            return False

        if motherboard:
            total_power_draw = sum(part['item_power_draw'] for part in build_parts if part['item_type'] == 'Motherboard')
            if total_power_draw > psu['item_power_supplied']:
                print("Warning: Total power draw exceeds PSU capacity.")
                return False

        if motherboard and len(ram) > motherboard['item_ram_slots']:
            print("Warning: More RAM modules than available RAM slots on the motherboard.")
            return False
        
        if len(gpu) > 1:
            print("Warning: Only one optional GPU is allowed.")
            return False
        
        if len(storages) < 1 or len(storages) > 2:
            print("Warning: 1-2 storage items are necessary for build.")

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
        #parts_in_cart = [item['part_details'] for item in self.shopping_cart]

        total_cost = sum(item['part_details']['item_price'] for item in self.shopping_cart)
        total_cost_formatted = "${:.2f}".format(total_cost)
        budget_remaining = self.customer.get('budget', float('inf')) - total_cost
        budget_remaining_formatted = "${:.2f}".format(budget_remaining)
        if self.customer:
            if total_cost <= self.customer.get('budget', float('inf')):
                print("Purchase successful! Thank you for shopping with us.\n")
                print("Your total purchase cost was: " + total_cost_formatted)
                print("You still have %s  left in your budget if you would like to continue shopping!"%(budget_remaining_formatted))

                #clear shopping cart
                self.shopping_cart = []
            else:
                print("The total cost exceeds the customer's budget.")
        else:
            print("Customer information is not available. Please set the customer information with the customer_info() function.")
            
    def wallet(self):
        total_cost = sum(item['part_details']['item_price'] for item in self.shopping_cart)
        total_cost_formatted = "${:.2f}".format(total_cost)
        budget = self.customer.get('budget', float('inf'))
        budget_formatted = "${:.2f}".format(budget)
        budget_remaining = self.customer.get('budget', float('inf')) - total_cost
        budget_remaining_formatted = "${:.2f}".format(budget_remaining)
        
        print('You set an initial budget of: ' + budget_formatted)
        print('You have %s worth of parts in you cart.'%(total_cost_formatted))
        print('You have %s left to purchase additional items.'%(budget_remaining_formatted))
        


    def leave(self):
        exit()

if __name__ == '__main__':
    if len(sys.argv) !=2:
        print("Usage: python computer_store.py inventory.json")
        sys.exit(1)
        
    inventory_file = sys.argv[1]

    store = computer_store(inventory_file)
    store.run()