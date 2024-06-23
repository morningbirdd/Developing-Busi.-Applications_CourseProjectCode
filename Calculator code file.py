import tkinter as tk

# List to store history records
history = []

# Function to handle button input
def get_input(entry, argu):
    entry.insert("end", argu)

# Function for backspace (undo input)
def backspace(entry):
    entry.delete(len(entry.get()) - 1)

# Function to clear the entry content (clear window)
def clear(entry):
    entry.delete(0, "end")

# Function to calculate the input expression
def calc(entry):
    input_data = entry.get()
    if not input_data:
        return
    clear(entry)
    try:
        output_data = str(eval(input_data))
        history.append((input_data, output_data))
    except Exception:
        entry.insert("end", "Calculation Error")
    else:
        if len(output_data) > 20:
            entry.insert("end", "Value Overflow")
        else:
            entry.insert("end", output_data)

# Function to show calculation history
def show_history():
    history_window = tk.Toplevel(root)
    history_window.title("Calculation History")
    
    # Set window size
    history_window.geometry("400x400")
    history_window.minsize(400, 400)
    
    for idx, (expression, result) in enumerate(history):
        expression_label = tk.Label(history_window, text=f"{idx+1}. {expression} = {result}", font=("Arial", 12))
        expression_label.pack(anchor="w", padx=10, pady=2)

if __name__ == '__main__':
    
    # Main window setup
    root = tk.Tk()
    root.title("Simple Calculator")
    root.configure(bg='white')
    root.resizable(0, 0)

    # Color configuration
    button_bg = 'lightgray'
    math_sign_bg = 'lightcyan'
    cal_output_bg = 'lightgreen'
    button_active_bg = 'gray'

    # Entry widget
    entry = tk.Entry(root, justify="right", font=("Arial", 20), bd=10, bg='white')
    entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

    def place_button(text, func, func_params, bg=button_bg, **place_params):
        button = tk.Button(root, text=text, command=lambda: func(*func_params), bg=bg, fg='black', activebackground=button_active_bg, font=("Arial", 14), bd=5)
        button.grid(**place_params, sticky="nsew")

    # Layout buttons
    button_texts = [
        ('7', '8', '9', '+'),
        ('4', '5', '6', '-'),
        ('1', '2', '3', '*'),
        ('0', '.', '/', '='),
    ]
    for row, texts in enumerate(button_texts, 1):
        for col, text in enumerate(texts):
            if text in '+-*/':
                place_button(text, get_input, (entry, text), bg=math_sign_bg, row=row, column=col, ipadx=5, ipady=5, padx=5, pady=5)
            elif text == '=':
                place_button(text, calc, (entry,), bg=cal_output_bg, row=row, column=col, ipadx=5, ipady=5, padx=5, pady=5)
            else:
                place_button(text, get_input, (entry, text), row=row, column=col, ipadx=5, ipady=5, padx=5, pady=5)

    place_button('<-', backspace, (entry,), row=5, column=0, ipadx=5, ipady=5, padx=5, pady=5)
    place_button('C', clear, (entry,), row=5, column=1, ipadx=5, ipady=5, padx=5, pady=5)
    place_button('History', show_history, (), bg='lightblue', row=5, column=2, columnspan=2, ipadx=5, pady=5)

    for i in range(6):
        root.grid_rowconfigure(i, weight=1)
    for i in range(4):
        root.grid_columnconfigure(i, weight=1)

    root.mainloop()
