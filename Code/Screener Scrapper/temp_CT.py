from customtkinter import *
import customtkinter

# Function to update label color
def update_label_color(color):
    label_message.configure(fg_color=color)

# Function to handle option menu selection
def optionmenu_callback(choice):
    global n
    n = int(choice)  # Convert selected option to integer
    print("Option menu dropdown clicked:", n)

app = CTk()
app.title("Scraper")
app.geometry("400x250")
app.resizable(False, False)

# Configure overall grid layout for better alignment
app.grid_columnconfigure(0, weight=1)

# Title label for the application
title_label = customtkinter.CTkLabel(app, text="Web Scraper Tool", font=("Arial", 20, "bold"))
title_label.grid(row=0, column=0, padx=10, pady=(10, 20))

# URL Entry widget with placeholder text
url_name = customtkinter.CTkEntry(app, placeholder_text="Enter URL to scrape", width=300, font=("Arial", 14))
url_name.grid(row=1, column=0, padx=20, pady=(0, 10))

# Create a frame to hold the button and label_message side by side
button_frame = customtkinter.CTkFrame(app, fg_color="transparent")
button_frame.grid(row=4, column=0, padx=20, pady=20)

process = customtkinter.CTkButton(button_frame, text="Start Scraping", command=f1, width=180, font=("Arial", 14, "bold"))
process.grid(row=0, column=0, padx=(0, 50))  # Increased right padding for more spacing

# Label to indicate the status
label_message = customtkinter.CTkLabel(button_frame, text="", width=15, height=15, fg_color="grey", corner_radius=12)
label_message.grid(row=0, column=1, padx=(50, 0))  # Left padding to move it toward the corner

# Create a frame for option menu and label
option_frame = customtkinter.CTkFrame(app, fg_color="transparent") 
option_frame.grid(row=2, column=0, padx=20, pady=20)

# Label for the option menu
option_label = customtkinter.CTkLabel(option_frame, text="How many Years?", font=("Arial", 14, "bold"))
option_label.grid(row=0, column=0, padx=(0, 10))  

# Option menu for selecting years
optionmenu_var = customtkinter.StringVar(value="1")  # Default value
optionmenu = customtkinter.CTkOptionMenu(option_frame, values=["1", "3", "5", "10"],
                                         command=optionmenu_callback,
                                         variable=optionmenu_var)
optionmenu.grid(row=0, column=1, padx=(10, 0))

# Initialize 'n' with default value from option menu
n = int(optionmenu_var.get())

app.mainloop()
