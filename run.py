import pandas as pd

try:
    existing_data = pd.read_excel("stock.xlsx")
except FileNotFoundError:
    existing_data = pd.DataFrame()

def add(existing_data):
    name = input("Input name of menu: ")
    price = int(input("Input price: "))
    quantity = int(input("Input quantity: "))

    new_entry = pd.DataFrame({
        'Menu': [name],
        'Price': [price],
        'Quantity': [quantity]
    })

    try:
        existing_data = pd.read_excel("stock.xlsx")
    except FileNotFoundError:
        existing_data = pd.DataFrame()

    data = pd.concat([existing_data, new_entry], ignore_index=True)
    data.to_excel("stock.xlsx", index=False)
    print("Completely writing to Excel file")
    print("--------------------------------")

def edit(existing_data):
    try:
        existing_data = pd.read_excel("stock.xlsx")
    except FileNotFoundError:
        existing_data = pd.DataFrame()
    print(existing_data)
    
    menu_to_edit = input("Enter the name of the menu to edit: ")
    
    if menu_to_edit in existing_data['Menu'].values:
        new_price = int(input(f"Enter the new price for {menu_to_edit}: "))
        new_quantity = int(input(f"Enter the new quantity for {menu_to_edit}: "))
        
        print("--------------------------------")
        print(f"Before Update:\n{existing_data}")

        existing_data.loc[existing_data['Menu'] == menu_to_edit, 'Price'] = new_price
        existing_data.loc[existing_data['Menu'] == menu_to_edit, 'Quantity'] = new_quantity
        
        existing_data.to_excel("stock.xlsx", index=False)
        
        print(f"After Update:\n{existing_data}")
        print(f"Menu '{menu_to_edit}' updated successfully.")
        print("--------------------------------")
    else:
        print(f"Menu '{menu_to_edit}' not found in the existing data.")

def take_order(existing_data, table_number):
    print(f"\nTable {table_number} Order:")
    order = {}
    while True:
        existing_data = pd.read_excel("stock.xlsx")
        print(existing_data)
        choice = input("Choose a menu or enter '0' to finish: ")
        if choice == '0':
            break

        if choice in existing_data['Menu'].values:
            quantity = int(input(f"Enter the quantity for {choice}: "))
            print("--------------------------------")
            order[choice] = quantity
            
            existing_data.loc[existing_data['Menu'] == choice, 'Quantity'] -= quantity
            existing_data.to_excel("stock.xlsx", index=False)
        else:
            print(f"Menu '{choice}' not found in the existing data.")
    return order

def calculate_total(order, existing_data):
    total = 0
    
    for menu, quantity in order.items():
        menu_data = existing_data[existing_data['Menu'] == menu]
        price = menu_data['Price'].values[0]
        quantity_available = menu_data['Quantity'].values[0]
        
        if quantity <= quantity_available:
            total += price * quantity

        else:
            print(f"Error: Not enough quantity available for '{menu}'")
    return total

def run(existing_data):
    orders = {}
    while True:
        table_number = input("Enter the table number (enter '0' to exit): ")
        if table_number == '0':
            break

        order = take_order(existing_data, table_number)

        if table_number in orders:
            additional_number = len(orders[table_number]) + 1
            orders[table_number][additional_number] = {'order': order, 'total_amount': calculate_total(order, existing_data)}
        else:
            orders[table_number] = {1: {'order': order, 'total_amount': calculate_total(order, existing_data)}}

    return orders

def print_orders(orders):
    print("\nOrders:")
    for table, order_info in orders.items():
        for order_number, details in order_info.items():
            print(f"Table {table} Order {order_number}:\n{details['order']}, Total Amount: ${details['total_amount']}")

def select(existing_data):
    print("-----SoSay Bar&bristro-----")
    while True:
        print('1. Stock')
        print('2. Order')
        select_number = input("Enter the function number (enter '0' to exit): ")

        if select_number == '0':
            break
        elif select_number == '1':
            while True:
                print('1. Add')
                print('2. Edit')
                stock_number = input("Enter the stock function number (enter '0' to exit): ")

                if stock_number == '0':
                    break
                elif stock_number == '1':
                    add(existing_data)
                elif stock_number == '2':
                    edit(existing_data)
                else:
                    print('Please enter a number in the choice')
        elif select_number == '2':
            orders = run(existing_data)
        else:
            print('Please enter a number in the choice')
    
    print_orders(orders)

select(existing_data)


    

