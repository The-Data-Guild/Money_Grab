import tkinter as tk
from tkinter import scrolledtext, ttk
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import datetime
import os
import sys


class MoneyGrabApp:
    """Simple GUI application to track expenses and generate a PDF split report."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Money Grab")
        self.root.configure(bg="black")
        self.root.geometry("800x600")

        # Data store
        self.expense_dict = {}

        # Styles
        style = ttk.Style()
        style.configure("TLabel", background="black", foreground="green", font=("Courier", 12))
        style.configure("TButton", background="black", foreground="yellow", font=("Courier", 12))
        style.configure("TEntry", background="black", foreground="yellow", font=("Courier", 12))

        # Title
        title_label = ttk.Label(self.root, text="Money Grab", font=("Courier", 24, "bold"))
        title_label.pack(pady=10)

        # Text area for logs
        self.text_area = scrolledtext.ScrolledText(self.root, bg="black", fg="green", height=15, width=80,
                                                  insertbackground="white", selectbackground="yellow",
                                                  selectforeground="black", font=("Courier", 12))
        self.text_area.pack(pady=10, padx=10)

        # Input frame
        input_frame = ttk.Frame(self.root)
        input_frame.pack(pady=10, padx=10, fill="x")

        # Expense name
        ttk.Label(input_frame, text="Expense Name:").pack(side="left", padx=5)
        self.expense_name_entry = ttk.Entry(input_frame, width=30)
        self.expense_name_entry.pack(side="left", padx=5)

        # Expense cost
        ttk.Label(input_frame, text="Expense Cost:").pack(side="left", padx=5)
        self.expense_cost_entry = ttk.Entry(input_frame, width=10)
        self.expense_cost_entry.pack(side="left", padx=5)

        # People
        ttk.Label(input_frame, text="Split By:").pack(side="left", padx=5)
        self.people_entry = ttk.Entry(input_frame, width=10)
        self.people_entry.pack(side="left", padx=5)

        # Buttons
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10, padx=10, fill="x")
        ttk.Button(button_frame, text="Add Expense", command=self.add_expense).pack(side="left", padx=10, pady=5)
        ttk.Button(button_frame, text="Calculate and Generate PDF", command=self.calculate_and_generate).pack(side="left", padx=10, pady=5)

        # Bind Enter: contextual behavior (add or calculate)
        self.root.bind('<Return>', self.on_enter_pressed)

        self.greeting()

    def print_to_gui(self, text: str):
        """Append a line of text to the scrolling text area."""
        self.text_area.insert(tk.END, text + "\n")
        self.text_area.see(tk.END)

    def on_enter_pressed(self, event=None):
        """Contextual Enter handling: add expense when typing entries, calculate when focus is on people."""
        widget = self.root.focus_get()
        try:
            if widget in (self.expense_name_entry, self.expense_cost_entry):
                self.add_expense()
            elif widget == self.people_entry:
                self.calculate_and_generate()
            else:
                self.add_expense()
        except Exception as e:
            self.print_to_gui(f"Error handling Enter: {e}")

    def add_expense(self):
        name = self.expense_name_entry.get().strip()
        cost_str = self.expense_cost_entry.get().strip()
        if not name or not cost_str:
            self.print_to_gui("Error: Please enter both expense name and cost.")
            return
        try:
            cost = float(cost_str)
        except ValueError:
            self.print_to_gui("Error: Invalid cost value. Please enter a number.")
            self.expense_cost_entry.delete(0, tk.END)
            return
        self.expense_dict[name] = cost
        self.print_to_gui(f"Expense '{name}' with cost ${cost:.2f} added.")
        self.expense_name_entry.delete(0, tk.END)
        self.expense_cost_entry.delete(0, tk.END)

    def calculate_and_generate(self):
        if not self.expense_dict:
            self.print_to_gui("Error: No expenses entered.")
            return
        try:
            people = int(self.people_entry.get().strip())
            if people <= 0:
                self.print_to_gui("Error: Number of people must be greater than zero.")
                return
        except ValueError:
            self.print_to_gui("Error: Invalid number of people. Please enter a number.")
            return
        total = sum(self.expense_dict.values())
        self.print_to_gui(f"Total Expenses: ${total:.2f}")
        self.print_to_gui(f"Splitting between {people} people.")
        self.print_to_gui(f"Each person owes: ${(total / people):.2f}")
        pdf_filename = self.generate_pdf(self.expense_dict, total, people)
        if pdf_filename:
            self.print_to_gui(f"PDF report generated: {pdf_filename}")
        self.expense_dict = {}

    def generate_pdf(self, expense_dict: dict, total: float, people: int):
        """Generates a PDF report and returns the filename, or None on error."""
        try:
            current_date = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"split_bills_{current_date}.pdf"
            c = canvas.Canvas(filename, pagesize=letter)
            c.setFont("Helvetica", 12)
            c.drawString(100, 750, "Expense Report")
            y = 700
            c.drawString(100, y, "Expenses:")
            y -= 20
            for expense, price in expense_dict.items():
                c.drawString(120, y, f"{expense}: ${price:.2f}")
                y -= 15
                if y < 60:
                    c.showPage()
                    y = 750
            c.drawString(100, y - 10, f"Total Expenses: ${total:.2f}")
            c.drawString(100, y - 30, f"Number of People: {people}")
            c.drawString(100, y - 50, f"Total Per Person: ${total / people:.2f}")
            c.save()
            return filename
        except Exception as e:
            self.print_to_gui(f"Error generating PDF: {e}")
            return None

    def greeting(self):
        art = r"""
  __  __                 _                      
 |  \/  | ___  _ __ ___ | |__   ___  _ __  _   _ 
 | |\/| |/ _ \| '_ ` _ \| '_ \ / _ \| '_ \| | | |
 | |  | | (_) | | | | | | |_) | (_) | | | | |_| |
 |_|  |_|\___/|_| |_| |_|_.__/ \___/|_| |_|\__, |
                                           |___/ 
  ____                     ____               
 |  _ \ _ __ ___  ___ ___ / ___|  __ _ _ __   
 | |_) | '__/ _ \/ __/ __| |  _  / _` | '_ \  
 |  __/| | |  __/\__ \__ \ |_| | (_| | | | | 
 |_|   |_|  \___||___/___/\____|\__,_|_| |_| 
"""
        self.print_to_gui(art)


def main():
    root = tk.Tk()
    app = MoneyGrabApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
