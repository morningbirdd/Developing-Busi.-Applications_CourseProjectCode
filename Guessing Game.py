
import tkinter as tk
from tkinter import messagebox
import random

class GuessingGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Guess the Number Game")
        self.root.geometry("400x350")
        self.root.configure(bg='#f0f0f0')

        self.number_to_guess = random.randint(1, 100)
        self.guesses_left = 5

        self.label = tk.Label(root, text="Guess a number between 1 and 100:", font=("Helvetica", 14), bg='#f0f0f0')
        self.label.pack(pady=10)

        self.entry = tk.Entry(root, font=("Helvetica", 14))
        self.entry.pack(pady=10)

        self.guess_button = tk.Button(root, text="Guess", font=("Helvetica", 12), command=self.check_guess,
                                      bg='#4CAF50', fg='white')
        self.guess_button.pack(pady=10)

        self.clear_button = tk.Button(root, text="Clear", font=("Helvetica", 12), command=self.clear_entry,
                                      bg='#f44336', fg='white')
        self.clear_button.pack(pady=10)

        self.result_label = tk.Label(root, text="", font=("Helvetica", 12), bg='#f0f0f0')
        self.result_label.pack(pady=10)

        self.progress_label = tk.Label(root, text=f"Guesses left: {self.guesses_left}", font=("Helvetica", 12),
                                       bg='#f0f0f0')
        self.progress_label.pack(pady=10)

        self.play_again_button = tk.Button(root, text="Play Again", font=("Helvetica", 12), command=self.reset_game,
                                           bg='#2196F3', fg='white')
        self.play_again_button.pack(pady=10)
        self.play_again_button.config(state="disabled")

    def check_guess(self):
        try:
            guess = int(self.entry.get())
            if guess < 1 or guess > 100:
                raise ValueError("Out of bounds")
        except ValueError:
            self.result_label.config(text="Please enter a valid number between 1 and 100.")
            return

        self.guesses_left -= 1
        self.progress_label.config(text=f"Guesses left: {self.guesses_left}")

        if guess < self.number_to_guess:
            self.result_label.config(text="Too low!", fg='red')
        elif guess > self.number_to_guess:
            self.result_label.config(text="Too high!", fg='red')
        else:
            self.result_label.config(text="Congratulations! You guessed it!", fg='green')
            self.end_game()
            return

        if self.guesses_left == 0:
            self.result_label.config(text=f"Out of guesses! The number was {self.number_to_guess}", fg='red')
            self.end_game()

    def end_game(self):
        self.guess_button.config(state="disabled")
        self.play_again_button.config(state="normal")

    def reset_game(self):
        self.number_to_guess = random.randint(1, 100)
        self.guesses_left = 5
        self.entry.delete(0, tk.END)
        self.result_label.config(text="")
        self.progress_label.config(text=f"Guesses left: {self.guesses_left}")
        self.guess_button.config(state="normal")
        self.play_again_button.config(state="disabled")

    def clear_entry(self):
        self.entry.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    game = GuessingGame(root)
    root.mainloop()


