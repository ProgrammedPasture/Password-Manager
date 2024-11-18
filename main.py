from tkinter import *
from tkinter import messagebox, END
import random
import string
import json

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


# ---------------------------- SEARCH PASSWORD ------------------------------- #

def search_password():
    website = website_entry.get().lower()  # Convert input to lowercase for consistency

    if not website:
        messagebox.showinfo(title="Error", message="Please enter a website to search.")
        return

    try:
        # Open the JSON file and load data
        with open("data.json", "r") as data_file:
            try:
                data = json.load(data_file)
            except json.JSONDecodeError:
                messagebox.showinfo(title="Error", message="Data file is empty or corrupted.")
                return
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No data file found.")
        return

    # Check if the website exists in the data
    if website in data:
        email = data[website]["email"]
        password = data[website]["password"]
        messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
    else:
        messagebox.showinfo(title="Not Found", message=f"No details for {website} found.")

# ---------------------------- SAVE PASSWORD ------------------------------- #

def save_password():
    website = website_entry.get().lower()  # Convert website to lowercase
    email_value = email_entry.get()
    password = password_entry.get()
    new_entry = {
        website: {
            "email": email_value,
            "password": password
        }
    }

    if not website or not password:
        messagebox.showinfo(title="Error", message="Website and Password cannot be empty!")
        return

    try:
        # Read the existing data
        with open("data.json", "r") as data_file:
            try:
                data = json.load(data_file)
            except json.JSONDecodeError:
                # If the file is empty or invalid, reset the data to an empty dictionary
                data = {}
    except FileNotFoundError:
        # If the file doesn't exist, start with an empty dictionary
        data = {}

    # Update the data with the new entry
    data.update(new_entry)

    try:
        # Write the updated data back to the file
        with open("data.json", "w") as data_file:
            json.dump(data, data_file, indent=4)  # `indent=4` makes the JSON more readable
        website_entry.delete(0, END)
        password_entry.delete(0, END)
        messagebox.showinfo(title="Success", message="Password saved successfully!")
    except Exception as e:
        messagebox.showinfo(title="Error", message=f"An error occurred: {e}")
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
website_entry = Entry(width=30)
website_entry.grid(column=1, row=1, sticky= "w")
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

search_button = Button(text="Search", command=search_password)
search_button.grid(column=1, row=1, sticky="e", padx=5)

#Main Loop
window.mainloop()