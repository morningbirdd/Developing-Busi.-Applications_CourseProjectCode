import tkinter as tk
from tkinter import messagebox
import yfinance as yf

class StockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Stock Viewer")
        self.root.geometry("390x500+200+150")
        self.root.resizable(False, False)  # Fix the window size

        # Create the UI components for stock entries
        self.labels = []
        self.entries = []
        for i in range(5):
            label = tk.Label(root, text=f"Stock {i+1}:")
            label.pack()
            self.labels.append(label)

            entry = tk.Entry(root, width=20)
            entry.pack()
            self.entries.append(entry)

        self.button_fetch = tk.Button(root, text="Fetch Stock Prices", command=self.fetch_stock_prices)
        self.button_fetch.pack()

        # Create the Listbox with Scrollbar to display stock prices
        self.frame = tk.Frame(root)
        self.frame.pack()
        
        self.scrollbar = tk.Scrollbar(self.frame, orient="vertical")
        self.listbox = tk.Listbox(self.frame, height=10, width=50, yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)
        
        self.listbox.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Create buttons to remove entries
        self.button_remove_all = tk.Button(root, text="Remove All Entries", command=self.remove_all_entries)
        self.button_remove_all.pack()

        self.button_remove_selected = tk.Button(root, text="Remove Selected Entries", command=self.remove_selected_entries)
        self.button_remove_selected.pack()

    def fetch_stock_prices(self):
        # Get the stock symbols from the entry widgets
        symbols = [entry.get().strip().upper() for entry in self.entries]

        # Filter out empty entries
        symbols = [symbol for symbol in symbols if symbol]

        if not symbols:
            messagebox.showerror("Input Error", "No stock symbols entered. Please enter at least one stock symbol. (For example: AAPL)")
            return
        
        if len(symbols) < 5:
            proceed = messagebox.askyesno("Input Confirmation", "You have entered less than five stock symbols. Do you want to continue?")
            if not proceed:
                return

        # Fetch stock prices
        for symbol in symbols:
            if symbol:
                stock = yf.Ticker(symbol)
                price = stock.info['currentPrice'] if 'currentPrice' in stock.info else 'N/A'
                self.listbox.insert(tk.END, f"{symbol}: ${price}")

    def remove_all_entries(self):
        self.listbox.delete(0, tk.END)

    def remove_selected_entries(self):
        selected_indices = self.listbox.curselection()
        for index in reversed(selected_indices):
            self.listbox.delete(index)

if __name__ == "__main__":
    root = tk.Tk()
    app = StockApp(root)
    root.mainloop()
