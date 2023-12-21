# Project 1 - Computer Store

## Introduction

You have been appointed the chief developer for the cutting-edge computer store in the tech-savvy town of Pylandia. As the technological demands grow, customers are seeking a personalized experience to build or buy computers that fit their specific needs and budgets.

Your mission is to create a command-line utility (storefront.py) that opens a text-based user interface in the terminal for the computer store. Here, customers will be welcomed to enter their name and budget, allowing them to navigate through an extensive catalog of computer parts.

Customers may choose to buy individual components or take on the exciting task of building a custom computer. If they opt for the latter, your interface must ensure that the chosen parts are compatible with each other.  You may even choose to provide guidance and suggestions if necessary. The system will also keep track of the customer's budget, making sure the selections align with their financial constraints.

## Requirements

Using the inventory items provided in ```inventory.json``` create a ```storefront.py``` which, prompts the user for their name (string) and budget (integer) at runtime.  After entering their user information, the user should be taken to a text based menu where they have the options to purchase individual computer components from the inventory, or build a complete custom computer from the parts inventory.

The inventory JSON for the ```storefront.py``` must be passed as a positional argument with running ```storefront.py```  IE:  ```./storefront.py inventory.json```

The custom computer build functionality, and the storefront, should be implemented using an object-oriented approach.  

The menu may, at your discretion, use a command approach, or a nested menu structure.  Nested menu implementations should be easy to navigate, and have the ability to return to higher levels of the nested structure.

Whenever displayed to the terminal, all component values should display their respective measurement units.  IE:  ```Price 200``` should be ```$200.00``` as a 2 decimal float value, ```power_supplied 1500``` should be ```1500W``` or ```1500 Watts```, and storage should be displayed in GB.  

Here are examples of commands which might be implemented in a command based approach to the storefront:

**Note:  While this is only an example of what commands could be implemented from the menu, the specification and rubric require that the functionality of all these commands be incorporated into the project somehow.**


| Command       | Arguments               | Output                                             |
|---------------|-------------------------|----------------------------------------------------|
| help | none | Lists all available commands and their function |
| list          | category (optional)     | List available parts and all their attributes (ID, type, etc.) in the specified category   |
| details       | part_id                 | Show details for the specified part                |
| compatibility | part_id1, part_id2, ... | Check compatibility between specified parts        |
| build         | part_ids (comma-separated) | Build a custom computer with specified parts, add the computer to the shopping cart   |
| remove        | part_ids/computer_ids (comma-separated) | Remove specified part or computer from current shopping cart |
| compatibility-build | none | Check compatibility between all parts in current build configuration |
| budget        | amount                  | Set the customer's budget                          |
| purchase      | part_id                 | Add the specified part to shopping cart                       |
| cart          | none                    | View the current shopping cart                     |
| checkout      | none                    | Complete the purchase and checkout                 |


### Build and Compatibility Rules

A Custom computer must have:

1 Motherboard <br>
RAM <br>
1 Processor (CPU) <br>
1 Power Supply Unit (PSU) <br>
1-2 Hard Drive(2) (Storage) <br>
Optional: 1 Graphics Processing Unit (GPU)

The attributes of the individual computer components can be broken down as follows:

```

computer
├── cpu
│   ├── id (string)
│   ├── name (string)
│   ├── power_draw (positive integer)
│   ├── price (positive integer)
│   ├── socket (string)
│   └── type (string)
├── gpu
│   ├── id (string)
│   ├── name (string)
│   ├── overclockable (boolean)
│   ├── power_draw (positive integer)
│   ├── price (positive integer)
│   └── type (string)
├── ram
│   ├── id (string)
│   ├── name (string)
│   ├── power_draw (positive integer)
│   ├── price (positive integer)
│   ├── capacity (positive integer)
│   └── type (string)
├── psu
│   ├── id (string)
│   ├── name (string)
│   ├── power_supplied (positive integer)
│   ├── price (positive integer)
│   └── type (string)
├── motherboard
│   ├── id (string)
│   ├── name (string)
│   ├── power_draw (positive integer)
│   ├── socket (string)
│   ├── ram_slots (positive integer)
│   ├── price (positive integer)
│   └── type (string)
└── storage
    ├── id (string)
    ├── name (string)
    ├── capacity (positive integer)
    ├── price (positive integer)
    └── type (string)


```

Compatibility Rules are as follows:

* Motherboard and CPU must have the same ```socket``` type

* All instances of RAM must be the same ```id```

* The number of instances of RAM must be between 1 and the ```ram_slots``` on the Motherboard

* The total ```power_draw``` of all components should be less than or equal to the ```power_supplied``` of the PSU

The storefront should alert users to incompatible parts and allow for corrections when incompatible parts are selected, and when attempting to checkout/purchase a build with incompatible parts.

## Deliverables

The specific deliverables and point breakdown are available in the project rubric.  For your reference, here is an example checklist of features to design unit tests for, assuming a command based approach

| Area                 | Requirement                                                                                       |
|----------------------|--------------------------------------------------------------------------------------------------|
| Menu                 | ```storefront.py``` prompts for username and budget on startup                                    |
| Inventory Display    | Implementation of 'list' command to view available parts                                          |
| Part Details         | Implementation of 'details' command to view specific part details                                 |
| Compatibility Check  | Implementation of 'compatibility' command to check compatibility between parts                   |
| Custom Build         | Implementation of 'build' command to build a custom computer and add parts to the cart           |
| Remove from Cart     | Implementation of 'remove' command to remove specified parts from the shopping cart               |
| Build Compatibility  | Implementation of 'compatibility-build' command to check the build configuration's compatibility |
| Budget Management    | Implementation of 'budget' command to manage the customer's budget                                |
| Individual Purchase  | Implementation of 'purchase' command to add a specific part to the shopping cart                  |
| View Cart            | Implementation of 'cart' command to view the current shopping cart                                |
| Checkout Process     | Implementation of 'checkout' command to complete the purchase and checkout                        |
| Build Rules          | Adherence to build and compatibility rules as defined in the project requirements                 |
| Measurement Units | All component values should display their respective measurement units as defined in the project requirements |
| Object-Oriented      | Use of object-oriented programming to implement the storefront and custom computer build feature  |
| Modular | Code is appropriately broken down into separate files/modules based on function |

## Extra Credit

| Extra Credit Item                                                                           | Point Value |
|---------------------------------------------------------------------------------------------|-------------|
| Storefront recommends additional components/upgrades when underbudget | 1           | 
| Storefront recommends compromises when overbudget                                           | 1           | 
| System flags when PSU cannot support the current power draw + 50% additional GPU power draw, if the GPU is capable of overclocking | 2           | 
| User data is saved when the program is exited, and user information, budget, and purchase history can be retrieved on startup         | 3           | 
| Project expands saved user data extra credit item to include password projected user accounts | 2 | 
| Storefront implements inventory management, stocking every item at 10, and then running out of items and alerting users. Inventory can be restocked by a user with name "Admin" who has access to the "restock" command from the menu | 3           | 
| Storefront implements inventory management and Admin user is password protected | 1 | 
| Storefront is implemented with a functional nested menu approach to the storefront, as opposed to a command based interface | 3 | 


## Turn-In Instructions

Your final work should be commited to branch called "develop". When you are ready for turn-in:

1. Create a "merge request" to merge "develop" into "main"
2. Select your instructor or mentor in the "reviewers" drop-down menu
3. Select the merge option: "Delete source branch when merge is accepted"