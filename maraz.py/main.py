import tkinter as tk
import random
import math

import level1
import level2
import level3
import level4
import level5
import level6
import level7
import level8
import level9
import level10

LEVELS = [
    (level1.MAX_RANGE, level1.WIN_POINTS),
    (level2.MAX_RANGE, level2.WIN_POINTS),
    (level3.MAX_RANGE, level3.WIN_POINTS),
    (level4.MAX_RANGE, level4.WIN_POINTS),
    (level5.MAX_RANGE, level5.WIN_POINTS),
    (level6.MAX_RANGE, level6.WIN_POINTS),
    (level7.MAX_RANGE, level7.WIN_POINTS),
    (level8.MAX_RANGE, level8.WIN_POINTS),
    (level9.MAX_RANGE, level9.WIN_POINTS),
    (level10.MAX_RANGE, level10.WIN_POINTS),
]

LOSE_POINTS = -1

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

current_level_idx = 0
points = 0
computer_number = None

window = tk.Tk()
window.title("Number Guessing Game - Levels")
window.geometry("480x520")
window.config(bg="#f7fbff")

title_label = tk.Label(window, text="🎯 Number Guessing Game (Levels)", font=("Arial", 16, "bold"), bg="#f7fbff")
title_label.pack(pady=8)

level_frame = tk.Frame(window, bg="#f7fbff")
level_frame.pack(pady=4)

level_label = tk.Label(level_frame, text="Level: 1", font=("Arial", 12, "bold"), bg="#f7fbff")
level_label.grid(row=0, column=0, padx=8)

range_label = tk.Label(level_frame, text="Range: 1 - 10", font=("Arial", 12), bg="#f7fbff")
range_label.grid(row=0, column=1, padx=8)

win_label = tk.Label(level_frame, text="Win: 10", font=("Arial", 12), bg="#f7fbff")
win_label.grid(row=0, column=2, padx=8)

lose_label = tk.Label(level_frame, text=f"Lose: {abs(LOSE_POINTS)}", font=("Arial", 12), bg="#f7fbff")
lose_label.grid(row=0, column=3, padx=8)

entry_guess = tk.Entry(window, font=("Arial", 14), justify="center")
entry_guess.pack(pady=10)

button_frame = tk.Frame(window, bg="#f7fbff")
button_frame.pack(pady=6)

guess_button = tk.Button(button_frame, text="🎲 Guess", font=("Arial", 12, "bold"), width=12)
guess_button.grid(row=0, column=0, padx=6)

next_button = tk.Button(button_frame, text="➡ Next Level", font=("Arial", 12, "bold"), width=12, state=tk.DISABLED)
next_button.grid(row=0, column=1, padx=6)

result_label = tk.Label(window, text="", font=("Arial", 12), bg="#f7fbff")
result_label.pack(pady=8)

points_label = tk.Label(window, text="Points: 0", font=("Arial", 12, "bold"), bg="#f7fbff")
points_label.pack(pady=4)

hints_frame = tk.LabelFrame(window, text="Hints", font=("Arial", 12, "bold"), bg="#f7fbff")
hints_frame.pack(pady=10, padx=10, fill="both")

hint_texts = [
    "Is it a prime number?",
    "Is it odd?",
    "Is it even?",
    "Is it squared?",
    "Can it be divided by 6?"
]

hint_labels = []
for text in hint_texts:
    lbl = tk.Label(hints_frame, text=text, font=("Arial", 11), anchor="w", bg="#f7fbff")
    lbl.pack(anchor="w", padx=8, pady=2)
    hint_labels.append(lbl)

def get_level_info(idx):
    return LEVELS[idx]

def update_level_ui():
    max_range, win_points = get_level_info(current_level_idx)
    level_label.config(text=f"Level: {current_level_idx + 1}")
    range_label.config(text=f"Range: 1 - {max_range}")
    win_label.config(text=f"Win: {win_points}")
    lose_label.config(text=f"Lose: {abs(LOSE_POINTS)}")

def update_hints(num):
    hints = {
        "Is it a prime number?": is_prime(num),
        "Is it odd?": num % 2 == 1,
        "Is it even?": num % 2 == 0,
        "Is it squared?": int(math.sqrt(num)) ** 2 == num,
        "Can it be divided by 6?": num % 6 == 0
    }
    for i, (hint, condition) in enumerate(hints.items()):
        hint_labels[i].config(text=f"{hint} {'(yes)' if condition else '(no)'}")

def start_new_round():
    global computer_number
    max_range, _ = get_level_info(current_level_idx)
    computer_number = random.randint(1, max_range)
    update_hints(computer_number)
    result_label.config(text="A new number has been chosen for this level.")
    entry_guess.delete(0, tk.END)
    next_button.config(state=tk.DISABLED)

def on_guess():
    global points
    try:
        user_guess = int(entry_guess.get())
    except ValueError:
        result_label.config(text="Please enter a valid integer.")
        return

    max_range, win_points = get_level_info(current_level_idx)
    if not (1 <= user_guess <= max_range):
        result_label.config(text=f"Enter a number between 1 and {max_range}.")
        return

    if user_guess == computer_number:
        points += win_points
        points_label.config(text=f"Points: {points}")
        result_label.config(text=f"Afarin! 🎉 You guessed correctly. The number was {computer_number}.")
        if current_level_idx < len(LEVELS) - 1:
            next_button.config(state=tk.NORMAL)
        else:
            result_label.config(text=result_label.cget("text") + "\nYou've completed the final level — congratulations!")
    else:
        points += LOSE_POINTS
        points_label.config(text=f"Points: {points}")
        result_label.config(text=f"Khak to saret 😅 Wrong. The number was {computer_number}.")
        start_new_round()

def on_next_level():
    global current_level_idx
    if current_level_idx < len(LEVELS) - 1:
        current_level_idx += 1
        update_level_ui()
        start_new_round()
    next_button.config(state=tk.DISABLED)

guess_button.config(command=on_guess)
next_button.config(command=on_next_level)

update_level_ui()
start_new_round()

window.mainloop()
