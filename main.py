from tkinter import *
import random
import pandas

BACKGROUND_COLOR = "#B1DDC6"


# -------------------------------------- FUNCTIONS -------------------------------------- #
try:
    data = pandas.read_csv("to_learn.csv")
except FileNotFoundError:
    data = pandas.read_csv("data.csv")

words_to_learn = data.to_dict(orient="records")
current_word = random.choice(words_to_learn)


def new_card():
    global current_word, timer
    window.after_cancel(timer)
    current_word = random.choice(words_to_learn)
    canvas.itemconfig(word, text=current_word['English'].title(), fill="black")
    canvas.itemconfig(language, text="English", fill="black")
    canvas.itemconfig(image, image=card_front_img)
    timer = window.after(3000, func=change_side)


def change_side():
    canvas.itemconfig(word, text=current_word['Ukrainian'].title(), fill="white")
    canvas.itemconfig(language, text="Ukrainian", fill="white")
    canvas.itemconfig(image, image=card_back_img)


def know_word():
    words_to_learn.remove(current_word)
    new_card()
    to_learn_file = pandas.DataFrame(words_to_learn)
    to_learn_file.to_csv("to_learn.csv", index=False)


# -------------------------------------- UI SETUP -------------------------------------- #

window = Tk()
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)
window.title("Flash Card")
timer = window.after(3000, func=change_side)

right_img = PhotoImage(file="images/right.png")
right_button = Button(image=right_img, highlightthickness=0, command=know_word)
right_button.grid(column=1, row=2)

wrong_img = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_img, highlightthickness=0, command=new_card)
wrong_button.grid(column=0, row=2)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
image = canvas.create_image(400, 263, image=card_front_img)
canvas.grid(column=0, row=0, columnspan=2, rowspan=2)

language = canvas.create_text((400, 150), text="", font=("Ariel", 40, "italic"))
word = canvas.create_text((400, 263), text="", font=("Ariel", 60, "bold"))

new_card()

window.mainloop()
