
import tkinter as tk
from tkinter import messagebox

class IceCreamStand:
    def __init__(self, root):
        self.root = root
        self.root.title("Ice Cream Stand")

        # Inventory
        self.inventory = {
            "vanilla": 0,
            "chocolate": 0,
            "sprinkles": 0,
            "whip_cream": 0,
            "hot_fudge": 0
        }
        
        # Financial data
        self.sales = 0.0
        self.expenses = 0.0

        # Create GUI components
        self.create_widgets()

    def create_widgets(self):
        # Inventory section
        tk.Label(self.root, text="Inventory").grid(row=0, column=0, columnspan=2)
        self.inventory_labels = {}
        for idx, (item, quantity) in enumerate(self.inventory.items()):
            tk.Label(self.root, text=item.capitalize()).grid(row=idx + 1, column=0)
            self.inventory_labels[item] = tk.Label(self.root, text=str(quantity))
            self.inventory_labels[item].grid(row=idx + 1, column=1)

        # Add to Inventory section
        tk.Label(self.root, text="Add to Inventory").grid(row=0, column=2, columnspan=2)
        self.add_inventory_vars = {}
        self.add_inventory_checks = {}
        inventory_text = {
            "vanilla": "Add 256.0 oz of Vanilla",
            "chocolate": "Add 256.0 oz of Chocolate",
            "sprinkles": "Add 64.0 oz of Sprinkles",
            "whip_cream": "Add 64.0 oz of Whipped Cream",
            "hot_fudge": "Add 48.0 oz of Hot Fudge"
        }
        for idx, item in enumerate(self.inventory.keys()):
            var = tk.IntVar()
            self.add_inventory_vars[item] = var
            chk = tk.Checkbutton(self.root, text=inventory_text[item], variable=var)
            chk.grid(row=idx + 1, column=2)
            self.add_inventory_checks[item] = chk
        tk.Button(self.root, text="Add To Inventory", command=self.add_to_inventory).grid(row=len(self.inventory) + 1, column=2, columnspan=2)

        # Order Form section
        tk.Label(self.root, text="Order Form").grid(row=0, column=4, columnspan=2)
        self.selected_flavor = tk.StringVar(value="vanilla")
        tk.Radiobutton(self.root, text="Vanilla", variable=self.selected_flavor, value="vanilla").grid(row=1, column=4, sticky="w")
        tk.Radiobutton(self.root, text="Chocolate", variable=self.selected_flavor, value="chocolate").grid(row=2, column=4, sticky="w")
        tk.Label(self.root, text="Scoops").grid(row=3, column=4, sticky="w")
        self.scoops_var = tk.IntVar()
        tk.Entry(self.root, textvariable=self.scoops_var).grid(row=3, column=5)
        self.order_vars = {
            "sprinkles": tk.BooleanVar(),
            "whip_cream": tk.BooleanVar(),
            "hot_fudge": tk.BooleanVar()
        }
        for idx, item in enumerate(["sprinkles", "whip_cream", "hot_fudge"]):
            tk.Checkbutton(self.root, text=item.replace("_", " ").capitalize(), variable=self.order_vars[item]).grid(row=idx + 4, column=4, columnspan=2)
        tk.Button(self.root, text="Place Order", command=self.place_order).grid(row=7, column=4, columnspan=2)

        # Financial Data section
        tk.Label(self.root, text="Financial Data").grid(row=0, column=6, columnspan=2)
        self.sales_label = tk.Label(self.root, text="Sales: $0.00")
        self.sales_label.grid(row=1, column=6, columnspan=2)
        self.expenses_label = tk.Label(self.root, text="Expenses: $0.00")
        self.expenses_label.grid(row=2, column=6, columnspan=2)
        self.profit_label = tk.Label(self.root, text="Profit: $0.00")
        self.profit_label.grid(row=3, column=6, columnspan=2)

        # Feedback section
        tk.Label(self.root, text="Feedback").grid(row=0, column=8, columnspan=2)
        self.feedback_text = tk.Text(self.root, height=10, width=40, state='disabled')
        self.feedback_text.grid(row=1, column=8, columnspan=2, rowspan=4)

    def update_inventory_display(self):
        for item, label in self.inventory_labels.items():
            label.config(text=str(self.inventory[item]))

    def update_financial_display(self):
        self.sales_label.config(text=f"Sales: ${self.sales:.2f}")
        self.expenses_label.config(text=f"Expenses: ${self.expenses:.2f}")
        self.profit_label.config(text=f"Profit: ${self.sales - self.expenses:.2f}")

    def update_feedback(self, message, error=False):
        self.feedback_text.config(state='normal')
        self.feedback_text.insert(tk.END, message + "\n")
        self.feedback_text.config(state='disabled')

    def add_to_inventory(self):
        costs = {"vanilla": 15.00, "chocolate": 15.00, "sprinkles": 40.00, "whip_cream": 12.00, "hot_fudge": 10.00}
        units = {"vanilla": 256, "chocolate": 256, "sprinkles": 64, "whip_cream": 64, "hot_fudge": 48}
        
        for item, var in self.add_inventory_vars.items():
            if var.get() == 1:
                self.inventory[item] += units[item]
                self.expenses += costs[item]
                self.update_feedback(f"Added {units[item]} units of {item}. Cost: ${costs[item]:.2f}")

        self.update_inventory_display()
        self.update_financial_display()

    def place_order(self):
        order_units = {"vanilla": 4, "chocolate": 4, "sprinkles": 0.25, "whip_cream": 1, "hot_fudge": 0.5}
        required_inventory = {item: 0 for item in self.inventory.keys()}
        selected_flavor = self.selected_flavor.get()
        scoops = self.scoops_var.get()
        if scoops > 0:
            required_inventory[selected_flavor] = scoops * order_units[selected_flavor]
        for item in ["sprinkles", "whip_cream", "hot_fudge"]:
            if self.order_vars[item].get():
                required_inventory[item] += order_units[item]

        if all(self.inventory[item] >= required_inventory[item] for item in self.inventory.keys()):
            for item in self.inventory.keys():
                self.inventory[item] -= required_inventory[item]
            self.sales += 3.00 + max(0, scoops - 1)
            self.update_inventory_display()
            self.update_financial_display()
            self.update_feedback("Order placed successfully.")
        else:
            self.update_feedback("Not enough inventory to fulfill the order.", error=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = IceCreamStand(root)
    root.mainloop()
