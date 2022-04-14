from tkinter import *
import pandas as pd
import random

BACKGROUND_COLOR = "#B1DDC6"
new_words = {}
try:
    data = pd.read_csv('data/words_to_learn.csv')
except FileNotFoundError:
    data = pd.read_csv('data/french_words.csv')
data_dict = data.to_dict(orient="records")


def generate_new_flash():
    global new_words, flip_timer
    window.after_cancel(flip_timer)
    new_words = random.choice(data_dict)
    new_french_word = new_words['French']
    # new_english_word = new_words['English']
    canvas.itemconfig(canvas_image, image=front_card)
    canvas.itemconfig(canvas_title, text="French", fill="black")
    canvas.itemconfig(canvas_word, text=new_french_word, fill="black")
    flip_timer = window.after(3000, flip_card)


def flip_card():
    global new_words
    canvas.itemconfig(canvas_image, image=back_card)
    canvas.itemconfig(canvas_title, text="English", fill="white")
    canvas.itemconfig(canvas_word, text=new_words["English"], fill="white")


def is_known():
    data_dict.remove(new_words)
    generate_new_flash()
    data_to_save = pd.DataFrame(data_dict)
    data_to_save.to_csv("data/words_to_learn.csv", index=False)

# ------------------------------------- GUI --------------------------------- #
window = Tk()
window.title("Flash-cards")
window.config(padx=30, pady=30, bg=BACKGROUND_COLOR)
flip_timer = window.after(3000, flip_card)


#CANVAS
front_card = PhotoImage(file="images/card_front.png")
back_card = PhotoImage(file="images/card_back.png")
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
canvas_image = canvas.create_image(400, 263, image=front_card)
canvas.grid(row=0, column=0, columnspan=2)

canvas_title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
canvas_word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))


#BUTTONS
correct = PhotoImage(file="images/right.png")
wrong = PhotoImage(file="images/wrong.png")
correct_button = Button(image=correct, highlightthickness=0, bd=0, command=is_known)
correct_button.grid(row=1, column=1)
wrong_button = Button(image=wrong, highlightthickness=0, bd=0, command=generate_new_flash)
wrong_button.grid(row=1, column=0)

generate_new_flash()

window.mainloop()