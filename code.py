import csv
import tkinter as tk
from tkinter import messagebox

class Product:
    def __init__(self, name, purchase_price, selling_price, inventory):
        self.name = name
        self.purchase_price = purchase_price
        self.selling_price = selling_price
        self.inventory = inventory

class Shop:
    def __init__(self, products_file='products.csv', sales_file='sales.csv'):
        self.products_file = products_file
        self.sales_file = sales_file
        self.products = self.load_products()

    def load_products(self):
        products = []
        try:
            with open(self.products_file, mode='r', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    products.append(Product(row['name'], float(row['purchase_price']), float(row['selling_price']), int(row['inventory'])))
        except FileNotFoundError:
            pass
        return products

    def save_products(self):
        with open(self.products_file, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['name', 'purchase_price', 'selling_price', 'inventory'])
            writer.writeheader()
            for product in self.products:
                writer.writerow({'name': product.name, 'purchase_price': product.purchase_price, 'selling_price': product.selling_price, 'inventory': product.inventory})

    def add_product(self, product):
        self.products.append(product)
        self.save_products()

    def increase_inventory(self, product_name, amount):
        for product in self.products:
            if product.name == product_name:
                product.inventory += amount
                self.save_products()
                return True
        return False

    def reduce_inventory(self, product_name, amount):
        for product in self.products:
            if product.name == product_name and product.inventory >= amount:
                product.inventory -= amount
                self.save_products()
                self.record_sale(product_name, amount, product.selling_price - product.purchase_price)
                return True
        return False

    def record_sale(self, product_name, amount, net_profit):
        with open(self.sales_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([product_name, amount, net_profit])

    def search_product(self, product_name):
        for product in self.products:
            if product.name == product_name:
                return product
        return None

    def list_sold_items(self):
        sold_items = []
        total_profit = 0
        try:
            with open(self.sales_file, mode='r', newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    sold_items.append({'name': row[0], 'amount': int(row[1]), 'net_profit': float(row[2])})
                    total_profit += float(row[2])
        except FileNotFoundError:
            pass
        return sold_items, total_profit

class ShopApp:
    def __init__(self, root):
        self.shop = Shop()
        self.root = root
        self.root.title("Shop Management System")
        self.create_widgets()

    def create_widgets(self):
        self.name_label = tk.Label(self.root, text="Product Name")
        self.name_label.grid(row=0, column=0)
        self.name_entry = tk.Entry(self.root)
        self.name_entry.grid(row=0, column=1)

        self.purchase_price_label = tk.Label(self.root, text="Purchase Price")
        self.purchase_price_label.grid(row=1, column=0)
        self.purchase_price_entry = tk.Entry(self.root)
        self.purchase_price_entry.grid(row=1, column=1)

        self.selling_price_label = tk.Label(self.root, text="Selling Price")
        self.selling_price_label.grid(row=2, column=0)
        self.selling_price_entry = tk.Entry(self.root)
        self.selling_price_entry.grid(row=2, column=1)

        self.inventory_label = tk.Label(self.root, text="Inventory")
        self.inventory_label.grid(row=3, column=0)
        self.inventory_entry = tk.Entry(self.root)
        self.inventory_entry.grid(row=3, column=1)

        self.add_button = tk.Button(self.root, text="Add Product", command=self.add_product)
        self.add_button.grid(row=4, column=0, columnspan=2)

        self.search_label = tk.Label(self.root, text="Search Product")
        self.search_label.grid(row=5, column=0)
        self.search_entry = tk.Entry(self.root)
        self.search_entry.grid(row=5, column=1)
        self.search_button = tk.Button(self.root, text="Search", command=self.search_product)
        self.search_button.grid(row=6, column=0, columnspan=2)

        self.increase_label = tk.Label(self.root, text="Increase Inventory")
        self.increase_label.grid(row=7, column=0)
        self.increase_entry = tk.Entry(self.root)
        self.increase_entry.grid(row=7, column=1)
        self.increase_button = tk.Button(self.root, text="Increase", command=self.increase_inventory)
        self.increase_button.grid(row=8, column=0, columnspan=2)

        self.reduce_label = tk.Label(self.root, text="Reduce Inventory")
        self.reduce_label.grid(row=9, column=0)
        self.reduce_entry = tk.Entry(self.root)
        self.reduce_entry.grid(row=9, column=1)
        self.reduce_button = tk.Button(self.root, text="Reduce", command=self.reduce_inventory)
        self.reduce_button.grid(row=10, column=0, columnspan=2)

        self.list_button = tk.Button(self.root, text="List Sold Items", command=self.list_sold_items)
        self.list_button.grid(row=11, column=0, columnspan=2)

    def add_product(self):
        name = self.name_entry.get()
        purchase_price = float(self.purchase_price_entry.get())
        selling_price = float(self.selling_price_entry.get())
        inventory = int(self.inventory_entry.get())
        product = Product(name, purchase_price, selling_price, inventory)
        self.shop.add_product(product)
        messagebox.showinfo("Success", "Product added successfully")

    def search_product(self):
        name = self.search_entry.get()
        product = self.shop.search_product(name)
        if product:
            messagebox.showinfo("Product Found", f"Name: {product.name}\nPurchase Price: {product.purchase_price}\nSelling Price: {product.selling_price}\nInventory: {product.inventory}")
        else:
            messagebox.showerror("Error", "Product not found")

    def increase_inventory(self):
        name = self.search_entry.get()
        amount = int(self.increase_entry.get())
        if self.shop.increase_inventory(name, amount):
            messagebox.showinfo("Success", "Inventory increased successfully")
        else:
            messagebox.showerror("Error", "Product not found")

    def reduce_inventory(self):
        name = self.search_entry.get()
        amount = int(self.reduce_entry.get())
        if self.shop.reduce_inventory(name, amount):
            messagebox.showinfo("Success", "Inventory reduced successfully")
        else:
            messagebox.showerror("Error", "Product not found or insufficient inventory")

    def list_sold_items(self):
        sold_items, total_profit = self.shop.list_sold_items()
        items_str = "\n".join([f"Name: {item['name']}, Amount: {item['amount']}, Net Profit: {item['net_profit']}" for item in sold_items])
        messagebox.showinfo("Sold Items", f"{items_str}\n\nTotal Net Profit: {total_profit}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ShopApp(root)
    root.mainloop()
