import tkinter as tk
from tkinter import messagebox, ttk
import csv

class BookManager:
    def __init__(self, filename):
        self.filename = filename

    def add_book(self, title, year, isbn, author):
        with open(self.filename, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([title, year, isbn, author])

    def search_book(self, title=None, year=None, isbn=None, author=None):
        results = []
        with open(self.filename, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if (title and row[0] == title) or (year and row[1] == year) or (isbn and row[2] == isbn) or (author and row[3] == author):
                    results.append(row)
        return results

    def delete_book(self, title=None, year=None, isbn=None, author=None):
        books = []
        with open(self.filename, 'r') as file:
            reader = csv.reader(file)
            books = [row for row in reader if not ((title and row[0] == title) or (year and row[1] == year) or (isbn and row[2] == isbn) or (author and row[3] == author))]
        
        with open(self.filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(books)

    def list_books(self):
        books = []
        with open(self.filename, 'r') as file:
            reader = csv.reader(file)
            books = [row for row in reader]
        return books

class BookManagerGUI:
    def __init__(self, root, manager):
        self.manager = manager
        self.root = root
        self.root.title("Book Manager")

        self.title_label = tk.Label(root, text="Title")
        self.title_label.grid(row=0, column=0)
        self.title_entry = tk.Entry(root)
        self.title_entry.grid(row=0, column=1)

        self.year_label = tk.Label(root, text="Year")
        self.year_label.grid(row=1, column=0)
        self.year_entry = tk.Entry(root)
        self.year_entry.grid(row=1, column=1)

        self.isbn_label = tk.Label(root, text="ISBN")
        self.isbn_label.grid(row=2, column=0)
        self.isbn_entry = tk.Entry(root)
        self.isbn_entry.grid(row=2, column=1)

        self.author_label = tk.Label(root, text="Author")
        self.author_label.grid(row=3, column=0)
        self.author_entry = tk.Entry(root)
        self.author_entry.grid(row=3, column=1)

        self.add_button = tk.Button(root, text="Add Book", command=self.add_book)
        self.add_button.grid(row=4, column=0, columnspan=2)

        self.search_button = tk.Button(root, text="Search Book", command=self.search_book)
        self.search_button.grid(row=5, column=0, columnspan=2)

        self.delete_button = tk.Button(root, text="Delete Book", command=self.delete_book)
        self.delete_button.grid(row=6, column=0, columnspan=2)

        self.list_button = tk.Button(root, text="List Books", command=self.list_books)
        self.list_button.grid(row=7, column=0, columnspan=2)

        self.result_text = tk.Text(root, height=10, width=50)
        self.result_text.grid(row=8, column=0, columnspan=2)

    def add_book(self):
        title = self.title_entry.get()
        year = self.year_entry.get()
        isbn = self.isbn_entry.get()
        author = self.author_entry.get()
        self.manager.add_book(title, year, isbn, author)
        messagebox.showinfo("Success", "Book added successfully")

    def search_book(self):
        title = self.title_entry.get()
        year = self.year_entry.get()
        isbn = self.isbn_entry.get()
        author = self.author_entry.get()
        results = self.manager.search_book(title, year, isbn, author)
        self.result_text.delete(1.0, tk.END)
        for book in results:
            self.result_text.insert(tk.END, f"Title: {book[0]}, Year: {book[1]}, ISBN: {book[2]}, Author: {book[3]}\n")

    def delete_book(self):
        title = self.title_entry.get()
        year = self.year_entry.get()
        isbn = self.isbn_entry.get()
        author = self.author_entry.get()
        self.manager.delete_book(title, year, isbn, author)
        messagebox.showinfo("Success", "Book deleted successfully")

    def list_books(self):
        books = self.manager.list_books()
        self.result_text.delete(1.0, tk.END)
        for book in books:
            self.result_text.insert(tk.END, f"Title: {book[0]}, Year: {book[1]}, ISBN: {book[2]}, Author: {book[3]}\n")

if __name__ == "__main__":
    root = tk.Tk()
    manager = BookManager('books.csv')
    app = BookManagerGUI(root, manager)
    root.mainloop()
