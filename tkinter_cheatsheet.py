import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Create the main application window
root = tk.Tk()
root.title("Sample Form")

# Create a label
label = ttk.Label(root, text="Enter your name:")
label.grid(column=0, row=0, padx=10, pady=5)

# Create an entry widget
entry = ttk.Entry(root)
entry.grid(column=1, row=0, padx=10, pady=5)

# Define the button click function
def on_button_click():
    user_input = entry.get()
    messagebox.showinfo("Information", f"Hello, {user_input}!")

# Create a button
button = ttk.Button(root, text="Submit", command=on_button_click)
button.grid(column=1, row=1, padx=10, pady=10)

# Run the Tkinter event loop
root.mainloop()