#!/usr/bin/env python
# coding: utf-8

# In[1]:


import csv
import time

print("Benvenuto/a all'interno del software di un negozio di prodotti vegani!!")
time.sleep(1)
print("Ti auguriamo una buona giornata.")

class VeganStore:
    def __init__(self):
        self.inventory = {}
        self.total_sales = 0
        self.total_costs = 0

    def load_inventory(self, magazzino):

        """
        Load inventory data from a CSV file.
        """

        try:
            with open('magazzino.csv', mode = 'r') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    self.inventory[row['product']] = {'quantity': int(row['quantita']), 'purchase_price': float(row['prezzo_acquisto']), 'selling_price': float(row['prezzo_vendita'])}

        except FileNotFoundError:
            print("File 'magazzino.csv' non trovato. Verrà creato un nuovo file.")

    def save_inventory(self, magazzino):

        """
        Load inventory data from a CSV file.
        """

        with open('magazzino.csv', mode = 'w', newline='') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=['product', 'quantita', 'prezzo_acquisto', 'prezzo_vendita'])
            csv_writer.writeheader()
            for product, details in self.inventory.items():
                csv_writer.writerow({'product': product, 'quantita': details['quantity'], 'prezzo_acquisto': details['purchase_price'], 'prezzo_vendita': details['selling_price']})

    def add_product(self, product, quantity, purchase_price, selling_price):

        """
        Add a product to the inventory.
        """
        if product in self.inventory:
            return "Errore: Il prodotto è già presente all'interno del magazzino."

        self.inventory[product] = {'quantity': quantity, 'purchase_price': purchase_price, 'selling_price': selling_price}
        return f"AGGIUNTO: {quantity} x {product}"

    def list_products(self):

        """
        List all products in the inventory with their quantity and selling price.
        """

        wareshop = "Prodotti in magazzino:\n"
        for name, product in self.inventory.items():
            wareshop += f"- {name}: {product['quantity']} unità, prezzo di vendita: {product['selling_price']} \n"
        return wareshop

    def sell_product(self, product, quantity):

        """
        Sell a product from the inventory.
        """
        if product in self.inventory and self.inventory[product]['quantity'] >= quantity:
            self.inventory[product]['quantity'] -= quantity
            self.total_sales += quantity * self.inventory[product]['selling_price']
            return "VENDITA REGISTRATA"
        else:
            return "Errore: prodotto non disponibile."

    def calculate_profit(self):

        """
        Calculate gross and net profits based on sales and purchase prices.
        """

        for product, details in self.inventory.items():
            self.total_costs += details['quantity'] * details['purchase_price']
        gross_profit = self.total_sales
        net_profit = gross_profit - self.total_costs
        return f"Profitto Lordo: {gross_profit}, Profitto Netto: {net_profit}"


if __name__ == "__main__":
    store = VeganStore()
    store.load_inventory("magazzino.csv")

    while True:
        try:
            cmd = input("Inserisci un comando(aiuto per vedere la lista dei comandi): ")

            if cmd == "aggiungi":
                while True:
                    product = input("Inserisci il nome del prodotto: ")
                    try:
                        quantity = int(input("Inserisci la quantità: "))
                        if quantity <= 0:
                            raise ValueError("Errore: La quantità deve essere positiva. Inserisci un valore valido.")
                        purchase_price = float(input("Inserisci il prezzo di acquisto: "))
                        if purchase_price <= 0:
                            raise ValueError("Errore: Il prezzo d'acquisto deve essere positivo. Inserisci un valore valido.")
                        selling_price = float(input("Inserisci il prezzo di vendita: "))
                        if selling_price <= 0:
                            raise ValueError("Errore: Il prezzo di vendita deve essere positivo. Inserisci un valore valido.")
                        
                        print(store.add_product(product, quantity, purchase_price, selling_price))
                        break
                        
                    except ValueError as e:
                        print("Errore: ", e)
                        continue

            elif cmd == "elenca":
                print(store.list_products())

            elif cmd == "vendita":
                while True:
                    product = input("Inserisci il nome del prodotto: ")
                    quantity = int(input("Inserisci la quantità: "))
                    print(store.sell_product(product, quantity))
                    add = input("Aggiungere un altro prodotto? (si/no): ")
                    if add.lower() != "si":
                        print(f"VENDITE TOTALI: {store.total_sales}")
                        break

            elif cmd == "profitti":
                print(store.calculate_profit())

            elif cmd == "aiuto":
                print("Comandi:\n - Aggiungi: Aggiunge un prodotto all'interno del magazzino.\n - Elenca: Elenca i prodotti in magazzino.\n - Vendita: Registra una vendita effettuata.\n - Profitti: Mostra i profiti totali.\n - Aiuto: Mostra i possibili comandi.\n - Chiudi: Esci dal programma.\n")

            elif cmd == "chiudi":
                store.save_inventory("magazzino.csv")
                print("Chiusura del programma. Arrivederci!")
                break

            else:
                print("Comando non disponibile. Riprova.")

        except ValueError:
                print("Valore non valido!")


# In[ ]:




