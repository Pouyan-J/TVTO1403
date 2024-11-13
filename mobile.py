import sqlite3
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox

class Mobile:
    def __init__(self, model, storage, cpu, price, inventory):
        self.model = model
        self.storage = storage
        self.cpu = cpu
        self.price = price
        self.inventory = inventory

class MobileStore:
    def __init__(self):
        self.conn = sqlite3.connect('mobilestore.db')
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS mobiles (
                               model TEXT PRIMARY KEY,
                               storage INTEGER,
                               cpu TEXT,
                               price REAL,
                               inventory INTEGER)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS sales (
                               id INTEGER PRIMARY KEY AUTOINCREMENT,
                               model TEXT,
                               quantity INTEGER,
                               type TEXT,
                               date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
        self.conn.commit()

    def add_mobile(self, mobile):
        self.cursor.execute('INSERT INTO mobiles VALUES (?, ?, ?, ?, ?)', 
                            (mobile.model, mobile.storage, mobile.cpu, mobile.price, mobile.inventory))
        self.conn.commit()

    def update_mobile(self, mobile):
        self.cursor.execute('''UPDATE mobiles SET storage=?, cpu=?, price=?, inventory=?
                               WHERE model=?''', 
                            (mobile.storage, mobile.cpu, mobile.price, mobile.inventory, mobile.model))
        self.conn.commit()

    def delete_mobile(self, model):
        self.cursor.execute('DELETE FROM mobiles WHERE model=?', (model,))
        self.conn.commit()

    def search_mobile(self, model):
        self.cursor.execute('SELECT * FROM mobiles WHERE model=?', (model,))
        return self.cursor.fetchone()

    def buy(self, model, quantity):
        self.cursor.execute('UPDATE mobiles SET inventory=inventory+? WHERE model=?', (quantity, model))
        self.cursor.execute('INSERT INTO sales (model, quantity, type) VALUES (?, ?, ?)', (model, quantity, 'buy'))
        self.conn.commit()

    def sell(self, model, quantity):
        self.cursor.execute('UPDATE mobiles SET inventory=inventory-? WHERE model=?', (quantity, model))
        self.cursor.execute('INSERT INTO sales (model, quantity, type) VALUES (?, ?, ?)', (model, quantity, 'sell'))
        self.conn.commit()

    def total_profit(self):
        self.cursor.execute('SELECT SUM(quantity * price) FROM sales JOIN mobiles ON sales.model = mobiles.model WHERE type="sell"')
        return self.cursor.fetchone()[0]

class MobileStoreGUI:
    def __init__(self, root, store):
        self.store = store
        self.root = root
        self.root.title("Mobile Store Management System")
        self.create_widgets()

    def create_widgets(self):
        self.model_label = ttk.Label(self.root, text="Model:")
        self.model_label.grid(column=0, row=0, padx=10, pady=5)
        self.model_entry = ttk.Entry(self.root)
        self.model_entry.grid(column=1, row=0, padx=10, pady=5)

        self.storage_label = ttk.Label(self.root, text="Storage:")
        self.storage_label.grid(column=0, row=1, padx=10, pady=5)
        self.storage_entry = ttk.Entry(self.root)
        self.storage_entry.grid(column=1, row=1, padx=10, pady=5)

        self.cpu_label = ttk.Label(self.root, text="CPU:")
        self.cpu_label.grid(column=0, row=2, padx=10, pady=5)
        self.cpu_entry = ttk.Entry(self.root)
        self.cpu_entry.grid(column=1, row=2, padx=10, pady=5)

        self.price_label = ttk.Label(self.root, text="Price:")
        self.price_label.grid(column=0, row=3, padx=10, pady=5)
        self.price_entry = ttk.Entry(self.root)
        self.price_entry.grid(column=1, row=3, padx=10, pady=5)

        self.inventory_label = ttk.Label(self.root, text="Inventory:")
        self.inventory_label.grid(column=0, row=4, padx=10, pady=5)
        self.inventory_entry = ttk.Entry(self.root)
        self.inventory_entry.grid(column=1, row=4, padx=10, pady=5)

        self.add_button = ttk.Button(self.root, text="Add Mobile", command=self.add_mobile)
        self.add_button.grid(column=0, row=5, padx=10, pady=10)

        self.update_button = ttk.Button(self.root, text="Update Mobile", command=self.update_mobile)
        self.update_button.grid(column=1, row=5, padx=10, pady=10)

        self.delete_button = ttk.Button(self.root, text="Delete Mobile", command=self.delete_mobile)
        self.delete_button.grid(column=2, row=5, padx=10, pady=10)

        self.buy_button = ttk.Button(self.root, text="Buy Mobile", command=self.buy_mobile)
        self.buy_button.grid(column=0, row=6, padx=10, pady=10)

        self.sell_button = ttk.Button(self.root, text="Sell Mobile", command=self.sell_mobile)
        self.sell_button.grid(column=1, row=6, padx=10, pady=10)

        self.profit_button = ttk.Button(self.root, text="Total Profit", command=self.show_profit)
        self.profit_button.grid(column=2, row=6, padx=10, pady=10)

        self.search_button = ttk.Button(self.root, text="Search Mobile", command=self.search_mobile)
        self.search_button.grid(column=3, row=0, padx=10, pady=10)

    def get_mobile_data(self):
        return Mobile(self.model_entry.get(),
                      int(self.storage_entry.get()),
                      self.cpu_entry.get(),
                      float(self.price_entry.get()),
                      int(self.inventory_entry.get()))

    def add_mobile(self):
        mobile = self.get_mobile_data()
        self.store.add_mobile(mobile)

    def update_mobile(self):
        mobile = self.get_mobile_data()
        self.store.update_mobile(mobile)

    def delete_mobile(self):
        model = self.model_entry.get()
        self.store.delete_mobile(model)

    def buy_mobile(self):
        model = self.model_entry.get()
        quantity = int(self.inventory_entry.get())
        self.store.buy(model, quantity)

    def sell_mobile(self):
        model = self.model_entry.get()
        quantity = int(self.inventory_entry.get())
        self.store.sell(model, quantity)

    def show_profit(self):
        profit = self.store.total_profit()
        profit_label = ttk.Label(self.root, text=f"Total Profit: {profit}")
        profit_label.grid(column=1, row=7, padx=10, pady=10)

    def search_mobile(self):
        model = self.model_entry.get()
        mobile = self.store.search_mobile(model)
        if mobile:
            self.storage_entry.delete(0, tk.END)
            self.storage_entry.insert(0, mobile[1])
            self.cpu_entry.delete(0, tk.END)
            self.cpu_entry.insert(0, mobile[2])
            self.price_entry.delete(0, tk.END)
            self.price_entry.insert(0, mobile[3])
            self.inventory_entry.delete(0, tk.END)
            self.inventory_entry.insert(0, mobile[4])
        else:
            messagebox.showerror("Error", "Mobile model not found")


if __name__ == "__main__":
    store = MobileStore()
    root = tk.Tk()
    app = MobileStoreGUI(root, store)
    root.mainloop()