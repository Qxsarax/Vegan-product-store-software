import csv
import time

print("Welcome to the software of a vegan product shop!!")
time.sleep(1)
print("We wish you a good day.")

class VeganStore:
    def __init__(self):
        self.inventory = {}
        self.total_sales = 0
        self.total_costs = 0

    def load_inventory(self, warehouse):

        """
        Load inventory data from a CSV file.
        """

        try:
            with open('warehouse.csv', mode = 'r') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    self.inventory[row['product']] = {'quantity': int(row['quantita']), 'purchase_price': float(row['prezzo_acquisto']), 'selling_price': float(row['prezzo_vendita'])}

        except FileNotFoundError:
            print("File 'warehouse.csv' not found. A new file will be created.")

    def save_inventory(self, warehouse):

        """
        Load inventory data from a CSV file.
        """

        with open('warehouse.csv', mode = 'w', newline='') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=['product', 'quantita', 'prezzo_acquisto', 'prezzo_vendita'])
            csv_writer.writeheader()
            for product, details in self.inventory.items():
                csv_writer.writerow({'product': product, 'quantita': details['quantity'], 'prezzo_acquisto': details['purchase_price'], 'prezzo_vendita': details['selling_price']})

    def add_product(self, product, quantity, purchase_price, selling_price):

        """
        Add a product to the inventory.
        """
        if product in self.inventory:
            return "Error: The product is already present in the warehouse."

        self.inventory[product] = {'quantity': quantity, 'purchase_price': purchase_price, 'selling_price': selling_price}
        return f"ADDED: {quantity} x {product}"

    def list_products(self):

        """
        List all products in the inventory with their quantity and selling price.
        """

        wareshop = "Products in warehouse:\n"
        for name, product in self.inventory.items():
            wareshop += f"- {name}: {product['quantity']} unit, selling price: {product['selling_price']} \n"
        return wareshop

    def sell_product(self, product, quantity):

        """
        Sell a product from the inventory.
        """
        if product in self.inventory and self.inventory[product]['quantity'] >= quantity:
            self.inventory[product]['quantity'] -= quantity
            self.total_sales += quantity * self.inventory[product]['selling_price']
            return "REGISTERED SALE"
        else:
            return "Error: Product not available."

    def calculate_profit(self):

        """
        Calculate gross and net profits based on sales and purchase prices.
        """

        for product, details in self.inventory.items():
            self.total_costs += details['quantity'] * details['purchase_price']
        gross_profit = self.total_sales
        net_profit = gross_profit - self.total_costs
        return f"Gross Profit: {gross_profit}, Net Profit: {net_profit}"


if __name__ == "__main__":
    store = VeganStore()
    store.load_inventory("warehouse.csv")

    while True:
        try:
            cmd = input("Enter a command (help to see the list of commands): ")

            if cmd == "add":
                while True:
                    product = input("Enter the product name: ")
                    try:
                        quantity = int(input("Enter quantity: "))
                        if quantity <= 0:
                            raise ValueError("Error: Quantity must be positive. Please enter a valid value.")
                        purchase_price = float(input("Enter the purchase price: "))
                        if purchase_price <= 0:
                            raise ValueError("Error: The purchase price must be positive. Please enter a valid value.")
                        selling_price = float(input("Enter the sales price: "))
                        if selling_price <= 0:
                            raise ValueError("Error: The sales price must be positive. Please enter a valid value.")
                        
                        print(store.add_product(product, quantity, purchase_price, selling_price))
                        break
                        
                    except ValueError as e:
                        print("Error: ", e)
                        continue

            elif cmd == "list":
                print(store.list_products())

            elif cmd == "sale":
                while True:
                    product = input("Enter the product name: ")
                    quantity = int(input("Enter quantity: "))
                    print(store.sell_product(product, quantity))
                    add = input("Add another product? (yes/no): ")
                    if add.lower() != "yes":
                        print(f"TOTAL SALES: {store.total_sales}")
                        break

            elif cmd == "profits":
                print(store.calculate_profit())

            elif cmd == "help":
                print("Commands:\n - Add: Adds a product into the warehouse.\n - List: Lists the products in the warehouse.\n - Sale: Records a sale made.\n - Profits: Shows the total profits.\n - Help: Show possible commands.\n - Close: Exit the program.\n")

            elif cmd == "close":
                store.save_inventory("warehouse.csv")
                print("Closing of the program. Until we meet again!")
                break

            else:
                print("Command not available. Try again.")

        except ValueError:
                print("Invalid value!")



