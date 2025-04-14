import tkinter as tk
from tkinter import scrolledtext, font, ttk
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import datetime
import os
import sys
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch

def generate_pdf(expense_dict, total, people):
    """Generates PDF with expenses, total, and split amount, and returns filename."""
    try:
        current_date = datetime.datetime.now().strftime("%Y%m%d")
        filename = f"split_bills_{current_date}.pdf"
        c = canvas.Canvas(filename, pagesize=letter)
        c.setFont("Courier", 12)

        # Money Grab ASCII Art
        money_grab_art = """
                                          .--.
                                         |  |
                                         |  |
                                         |  |
                                .-------'--'-------.
                               /                    \\
                              |  Money Grab  |
                               \\____________________/
                                         ||
                                         ||
                                         ||
                                        /--\\
                                       /----\\
                                      /------\\
                                     /--------\\
                                    /----------\\
                                   /------------\\
                                  /--------------\\
                                 /----------------\\
                                /------------------\\
                               /--------------------\\
                              /______________________\\
        """
        c.drawString(50, 730, money_grab_art)

        # Title
        c.setFont("Courier-Bold", 20)
        c.setFillColorRGB(0.3, 0.7, 0.3)  # Greenish
        c.drawCentredString(letter[0] / 2, 630, "Expense Report")

        # Table Header
        c.setFont("Courier-Bold", 12)
        c.setFillColorRGB(0.7, 0.7, 0.7)  # Light Gray
        c.drawString(100, 580, "Expenses:")

        # Create table data
        data = [["Expense Name", "Cost"]]
        for expense, price in expense_dict.items():
            data.append([expense, f"${price:.2f}"])

        # Create table
        table = Table(data)

        # Table Style
        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.black),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.yellow),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Courier-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.black),  # Black background for data
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.green),  # Green text for data
            ('GRID', (0, 0), (-1, -1), 1, colors.gray),
            ('FONTNAME', (0, 1), (-1, -1), 'Courier'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),  # Add left padding
            ('RIGHTPADDING', (0, 0), (-1, -1), 12), # Add right padding
        ])
        table.setStyle(table_style)

        # Calculate table width and position
        table_width = table.wrapOn(c, letter[0], letter[1])[0]
        table_x = (letter[0] - table_width) / 2
        table.drawOn(c, table_x, 400)  # Position the table

        # Summary
        c.setFont("Courier-Bold", 12)
        c.setFillColorRGB(0.7, 0.7, 0.7)  # Light Gray
        y_position = 400 - (len(expense_dict) + 1) * 18 - 20  # Position dynamically
        c.drawString(100, y_position, f"Total Expenses: ${total:.2f}")
        c.drawString(100, y_position - 20, f"Number of People: {people}")
        c.drawString(100, y_position - 40, f"Total Per Person: ${total / people:.2f}")

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
    root.wait_variable(root, True)  # Use the instance variable here
    user_input = text_area.get("end-1c linestart", tk.END).splitlines()[-1]
    text_area.tag_remove("input", "end-1c linestart", tk.END)
    root.setvar(root, False) #reset
    return user_input

def on_enter_pressed(event):
    """Handles Enter key press."""
    event.widget.setvar(event.widget, True) #set the variable of the widget that called this event.

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
    individual_share = total / people # Calculate the individual share
    print_to_gui(f"Total Expenses: ${total:.2f}")
    print_to_gui(f"Splitting between {people} people.")
    print_to_gui(f"Each person owes: ${individual_share:.2f}")
    pdf_filename = generate_pdf(expense_dict, total, people)
    if pdf_filename:
        print_to_gui(f"PDF report generated: {pdf_filename}")
    expense_dict = {}
    expense_name_entry.delete(0, tk.END)
    expense_cost_entry.delete(0, tk.END)
    people_entry.delete(0, tk.END)

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
