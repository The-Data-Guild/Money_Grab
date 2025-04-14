import tkinter as tk
from tkinter import scrolledtext, font, ttk
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import datetime
import os
import sys

def generate_pdf(expense_dict, total, people):
    """Generates PDF with expenses, total, split amount, and returns filename."""
    try:
        current_date = datetime.datetime.now().strftime("%Y%m%d")
        filename = f"split_bills_{current_date}.pdf"
        c = canvas.Canvas(filename, pagesize=letter)
        c.setFont("Helvetica", 12)
        c.drawString(100, 750, "Expense Report")

        y_position = 700
        c.drawString(100, y_position, "Expenses:")
        y_position -= 20

        for expense, price in expense_dict.items():
            c.drawString(120, y_position, f"{expense}: ${price:.2f}")
            y_position -= 15

        c.drawString(100, y_position - 10, f"Total Expenses: ${total:.2f}")
        c.drawString(100, y_position - 30, f"Number of People: {people}")
        c.drawString(100, y_position - 50, f"Total Per Person: ${total / people:.2f}")

        c.save()
        print_to_gui(f"PDF report generated: {filename}")
        return filename
    except Exception as e:
        print_to_gui(f"Error generating PDF: {e}")
        return None



def main():
    """Main function to execute the expense calculation and PDF generation."""
    global root, text_area, expense_name_entry, expense_cost_entry, people_entry, add_expense_button, calculate_button
    root = tk.Tk()
    root.title("Money Grab")
    root.configure(bg="black")
    root.geometry("800x600")

    # Style
    style = ttk.Style()
    style.configure("TLabel", background="black", foreground="green", font=("Courier", 12))
    style.configure("TButton", background="black", foreground="yellow", font=("Courier", 12),
                    relief="raised", borderwidth=2, highlightcolor="yellow", highlightthickness=2)
    style.configure("TEntry", background="black", foreground="yellow", font=("Courier", 12),
                    insertcolor="yellow")
    style.map("TButton",
              foreground=[('active', 'black'), ('!active', 'yellow')],
              background=[('active', 'yellow'), ('!active', 'black')],
              relief=[('pressed', 'sunken'), ('!pressed', 'raised')])

    # Title Label
    title_label = ttk.Label(root, text="Money Grab", font=("Courier", 24, "bold"))
    title_label.pack(pady=10)

    # Text Area
    text_area = scrolledtext.ScrolledText(root, bg="black", fg="green", height=15, width=80,
                                         insertbackground="white", selectbackground="yellow",
                                         selectforeground="black", font=("Courier", 12))
    text_area.pack(pady=10, padx=10)
    text_area.tag_configure("input", foreground="yellow")

    # Input Frame
    input_frame = ttk.Frame(root, style="TFrame")
    input_frame.pack(pady=10, padx=10, fill="x")

    # Expense Name Entry
    expense_name_label = ttk.Label(input_frame, text="Expense Name:")
    expense_name_label.pack(side="left", padx=5)
    expense_name_entry = ttk.Entry(input_frame, width=30)
    expense_name_entry.pack(side="left", padx=5)

    # Expense Cost Entry
    expense_cost_label = ttk.Label(input_frame, text="Expense Cost:")
    expense_cost_label.pack(side="left", padx=5)
    expense_cost_entry = ttk.Entry(input_frame, width=10)
    expense_cost_entry.pack(side="left", padx=5)

    # People Entry
    people_label = ttk.Label(input_frame, text="Split By:")
    people_label.pack(side="left", padx=5)
    people_entry = ttk.Entry(input_frame, width=10)
    people_entry.pack(side="left", padx=5)

    # Buttons Frame
    button_frame = ttk.Frame(root, style="TFrame")
    button_frame.pack(pady=10, padx=10, fill="x")
    # Add Expense Button
    add_expense_button = ttk.Button(button_frame, text="Add Expense", command=add_expense)
    add_expense_button.pack(side="left", padx=10, pady=5)

    # Calculate Button
    calculate_button = ttk.Button(button_frame, text="Calculate and Generate PDF", command=calculate_and_generate)
    calculate_button.pack(side="left", padx=10, pady=5)
    root.bind('<Return>', on_enter_pressed)  # Bind Enter key

    greeting()
    root.mainloop()

def print_to_gui(text):
    """Prints text to the GUI text area."""
    text_area.insert(tk.END, text + "\n")
    text_area.see(tk.END)

def simple_input(prompt):
    """Gets input from the user via the GUI, and formats it"""
    print_to_gui(prompt)
    text_area.tag_add("input", text_area.index("end-1c linestart"), tk.END)
    text_area.mark_set("insert", tk.END)
    root.wait_variable(root)
    user_input = text_area.get("end-1c linestart", tk.END).splitlines()[-1]
    text_area.tag_remove("input", "end-1c linestart", tk.END)
    return user_input

def on_enter_pressed(event):
    """Handles Enter key press."""
    root.setvar(root, True)

expense_dict = {}
def add_expense():
    """Adds an expense to the expense dictionary."""
    global expense_dict
    expense_name = expense_name_entry.get().strip()
    expense_cost = expense_cost_entry.get().strip()

    if not expense_name or not expense_cost:
        print_to_gui("Error: Please enter both expense name and cost.")
        return

    try:
        expense_cost = float(expense_cost)
        expense_dict[expense_name] = expense_cost
        print_to_gui(f"Expense '{expense_name}' with cost ${expense_cost:.2f} added.")
        expense_name_entry.delete(0, tk.END)
        expense_cost_entry.delete(0, tk.END)
    except ValueError:
        print_to_gui("Error: Invalid cost value. Please enter a number.")
        expense_cost_entry.delete(0, tk.END)

def calculate_and_generate():
    """Calculates expenses and generates PDF."""
    global expense_dict
    if not expense_dict:
        print_to_gui("Error: No expenses entered.")
        return

    try:
        people = int(people_entry.get().strip())
        if people <= 0:
            print_to_gui("Error: Number of people must be greater than zero.")
            return
    except ValueError:
        print_to_gui("Error: Invalid number of people. Please enter a number.")
        return

    total = sum(expense_dict.values())
    print_to_gui(f"Total Expenses: ${total:.2f}")
    print_to_gui(f"Splitting between {people} people.")
    print_to_gui(f"Each person owes: ${total / people:.2f}")
    pdf_filename = generate_pdf(expense_dict, total, people)
    if pdf_filename:
        print_to_gui(f"PDF report generated: {pdf_filename}")
    expense_dict = {}

def greeting():
    """Displays a welcome message with ASCII art."""
    art = '''
          __  __  ___  _  _  _  _    ____  ____  ___   ___  ____  
         |  \/  |/ _ \| \| |/ \| |  | __ )| __ )| _ ) / _ \| __ ) 
         | |\/| | | | | .` | | | |  |  _ \|  _ \| _ \| | | |  _ \ 
         |_|  |_|_| |_|_|\_|_| |_|  |____/|____/|___/|_| |_|____/ 
           ____  ____  ___   ___  ____   ____  ____  ___   ____  
          / __ \|  _ \| _ ) / _ \| __ ) / __ \|  _ \| _ ) | __ ) 
         / / _` | | | | _ \| | | |  _ \| | | | | | | _ \ |  _ \ 
        | | (_| | |_| | | | | |_| | |_) | |_| | |_| | | | | |_) |
         \ \__,_|____/|_| |_|\___/|____/ \____/|____/|_| |_|____/ 
          \____/                                                  
        '''
    print_to_gui(art)



if __name__ == "__main__":
    root = tk.Tk()
    root.bind('<Return>', on_enter_pressed)
    root.mainloop()
    main()
