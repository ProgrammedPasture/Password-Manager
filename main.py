from tkinter import *
from tkinter import messagebox
import random
import string

email = "brandonleekoch@icloud.com"

# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_password():
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(12))  # 12-character password
    password_entry.delete(0, END)
    password_entry.insert(0, password)
    check_password_strength(password)

# ---------------------------- PASSWORD STRENGTH CHECKLIST ------------------------------- #

def check_password_strength(password):
    length = len(password) >= 12
    upper = any(char.isupper() for char in password)
    lower = any(char.islower() for char in password)
    digit = any(char.isdigit() for char in password)
    special = any(char in string.punctuation for char in password)

    if all([length, upper, lower, digit, special]):
        strength_label.config(text="Strong Password", fg="green")
    else:
        strength_label.config(text="Weak Password", fg="red")


# ---------------------------- SAVE PASSWORD ------------------------------- #

def save_password():
    website = website_entry.get()
    email_value = email_entry.get()
    password = password_entry.get()

    if not website or not password:
        messagebox.showinfo(title="Error", message="Website and Password cannot be empty!")
        return

    with open("data.txt", "a") as file:
        file.write(f"{website} | {email_value} | {password}\n")
    website_entry.delete(0, END)
    password_entry.delete(0, END)
    messagebox.showinfo(title="Success", message="Password saved successfully!")


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Koch Security")
window.config(padx=20, pady=20)

#Main Canvas Window
canvas = Canvas(width=200, height=200, highlightthickness=0)
try:
    lock_image = PhotoImage(file="logo.png")
    canvas.create_image(80, 100, image=lock_image)
except TclError:
    canvas.create_text(100, 100, text="Logo Missing", font=("Arial", 20))
canvas.grid(column=1, row=0)

#Labels
website_label = Label(text="Website:", font=("Times New Roman", 20))
website_label.grid(column=0, row=1)
email_label = Label(text="Email:", font=("Times New Roman", 20))
email_label.grid(column=0, row=2)
password_label = Label(text="Password:", font=("Times New Roman", 20))
password_label.grid(column=0, row=3)
strength_label = Label(text="", font=("Times New Roman", 20))
strength_label.grid(column=1, row=5)

#Entries
website_entry = Entry(width=40)
website_entry.grid(column=1, row=1)
website_entry.focus()
email_entry = Entry(width=40)
email_entry.grid(column=1, row=2)
email_entry.insert(0, email)
password_entry = Entry(width=30)
password_entry.grid(column=1, row=3)

#Buttons
generate_button = Button(text="Generate Password", command=generate_password)
generate_button.grid(column=1, row=4, sticky="w", padx=50)

upload_button = Button(text="Upload File", command=save_password)
upload_button.grid(column=1, row=4, sticky="e", padx=50)

#Main Loop
window.mainloop()