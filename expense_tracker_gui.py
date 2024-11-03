# expense_tracker_gui.py

import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.filedialog import asksaveasfilename
from expense import Expense
from expense_tracker_logic import ExpenseTrackerLogic


class ExpenseTrackerAppEnhanced(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Enhanced Expense Tracker")
        self.geometry("600x500")

        # Initialize logic handler
        self.tracker_logic = ExpenseTrackerLogic()

        # Adding tabbed interface
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill="both")

        # Tabs
        self.home_tab = tk.Frame(self.notebook)
        self.expense_tab = tk.Frame(self.notebook)
        self.summary_tab = tk.Frame(self.notebook)
        self.export_tab = tk.Frame(self.notebook)

        self.notebook.add(self.home_tab, text="Home")
        self.notebook.add(self.expense_tab, text="Add Expense")
        self.notebook.add(self.summary_tab, text="Summary")
        self.notebook.add(self.export_tab, text="Export Data")

        # Home Tab - Budget Setting
        self.setup_home_tab()

        # Add Expense Tab
        self.setup_expense_tab()

        # Summary Tab
        self.setup_summary_tab()

        # Export Tab
        self.setup_export_tab()

        # Enable functions if budget is already set
        if self.tracker_logic.is_budget_set():
            self.enable_expense_functions()

    def setup_home_tab(self):
        """Sets up the home tab where users can set their budget."""
        home_label = tk.Label(
            self.home_tab, text="Set Your Monthly Budget", font=("Arial", 14, "bold")
        )
        home_label.pack(pady=10)

        self.budget_entry = tk.Entry(self.home_tab, width=20)
        self.budget_entry.pack(pady=5)

        set_budget_button = tk.Button(
            self.home_tab, text="Set Budget", command=self.set_budget
        )
        set_budget_button.pack(pady=5)

        self.update_budget_button = tk.Button(
            self.home_tab,
            text="Update Budget",
            command=self.update_budget,
            state=tk.DISABLED,
        )
        self.update_budget_button.pack(pady=5)

    def setup_expense_tab(self):
        """Sets up the add expense tab."""
        expense_label = tk.Label(
            self.expense_tab, text="Add a New Expense", font=("Arial", 14, "bold")
        )
        expense_label.pack(pady=10)

        # Expense Name
        tk.Label(self.expense_tab, text="Expense Name:").pack()
        self.expense_name_entry = tk.Entry(self.expense_tab, width=30)
        self.expense_name_entry.pack(pady=5)

        # Category
        tk.Label(self.expense_tab, text="Category:").pack()
        self.selected_category = tk.StringVar()
        self.category_dropdown = ttk.Combobox(
            self.expense_tab, textvariable=self.selected_category
        )
        self.category_dropdown["values"] = [
            "🍕 Food",
            "🏠 Home",
            "💼 Work",
            "🥳 Going-out",
            "🎒 Other",
        ]
        self.category_dropdown.pack(pady=5)

        # Amount
        tk.Label(self.expense_tab, text="Amount:").pack()
        self.expense_amount_entry = tk.Entry(self.expense_tab, width=20)
        self.expense_amount_entry.pack(pady=5)

        self.add_expense_button = tk.Button(
            self.expense_tab,
            text="Add Expense",
            command=self.add_expense,
            state=tk.DISABLED,
        )
        self.add_expense_button.pack(pady=10)

    def setup_summary_tab(self):
        """Sets up the summary tab to view spending summaries."""
        summary_label = tk.Label(
            self.summary_tab, text="Expense Summary", font=("Arial", 14, "bold")
        )
        summary_label.pack(pady=10)

        self.summary_button = tk.Button(
            self.summary_tab,
            text="Show Summary",
            command=self.show_summary,
            state=tk.DISABLED,
        )
        self.summary_button.pack(pady=10)

    def setup_export_tab(self):
        """Sets up the export tab to export data to Excel."""
        export_label = tk.Label(
            self.export_tab, text="Export Expenses to Excel", font=("Arial", 14, "bold")
        )
        export_label.pack(pady=10)

        self.export_button = tk.Button(
            self.export_tab,
            text="Export Data",
            command=self.export_data,
            state=tk.DISABLED,
        )
        self.export_button.pack(pady=10)

    def set_budget(self):
        """Sets the monthly budget and enables expense functions."""
        budget_input = self.budget_entry.get()
        try:
            budget = float(budget_input)
            self.tracker_logic.set_budget(budget)
            self.enable_expense_functions()
            messagebox.showinfo("Success", f"Budget set to ${budget}")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for the budget")

    def update_budget(self):
        """Allows the user to update the budget."""
        budget_input = self.budget_entry.get()
        try:
            new_budget = float(budget_input)
            self.tracker_logic.update_budget(new_budget)
            messagebox.showinfo("Success", f"Budget updated to ${new_budget}")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for the budget")

    def add_expense(self):
        """Adds a new expense to the record."""
        name = self.expense_name_entry.get()
        category = self.selected_category.get()
        amount = self.expense_amount_entry.get()
        try:
            expense = Expense(name=name, category=category, amount=float(amount))
            self.tracker_logic.add_expense(expense)
            messagebox.showinfo("Success", "Expense added!")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount")

    def show_summary(self):
        """Displays a summary of expenses, including daily budget."""
        expenses_by_category, total_spent, remaining_budget = (
            self.tracker_logic.summarize_expenses()
        )
        daily_budget = self.tracker_logic.calculate_daily_budget()

        summary_window = tk.Toplevel(self)
        summary_window.title("Expense Summary")

        tk.Label(summary_window, text=f"Total Spent: ${total_spent:.2f}").pack()
        tk.Label(
            summary_window, text=f"Remaining Budget: ${remaining_budget:.2f}"
        ).pack()
        tk.Label(summary_window, text=f"Daily Budget: ${daily_budget:.2f}").pack()
        tk.Label(summary_window, text="Expenses by Category:").pack()

        for category, amount in expenses_by_category.items():
            tk.Label(summary_window, text=f"{category}: ${amount:.2f}").pack()

    def export_data(self):
        """Exports expenses and summary to an Excel file."""
        file_path = asksaveasfilename(
            defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")]
        )
        if not file_path:
            return  # User canceled save dialog
        try:
            self.tracker_logic.export_to_excel(file_path)
            messagebox.showinfo("Success", f"Data exported successfully to {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export data: {e}")

    def enable_expense_functions(self):
        """Enables expense-related buttons once the budget is set."""
        self.add_expense_button.config(state=tk.NORMAL)
        self.summary_button.config(state=tk.NORMAL)
        self.export_button.config(state=tk.NORMAL)
        self.update_budget_button.config(state=tk.NORMAL)


# Running the enhanced application
if __name__ == "__main__":
    app = ExpenseTrackerAppEnhanced()
    app.mainloop()
