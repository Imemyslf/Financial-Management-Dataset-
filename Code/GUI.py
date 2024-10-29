import customtkinter
from customtkinter import *
from main import getUrl

# Initialize the main app window
app = CTk()
app.title("Scraper")
app.geometry("400x200")
app.resizable(False, False)

# Configure overall grid layout for better alignment
app.grid_columnconfigure(0, weight=1)

# Title label for the application
title_label = customtkinter.CTkLabel(
    app, text="Web Scraper Tool", font=("Arial", 20, "bold")
)
title_label.grid(row=0, column=0, padx=10, pady=(10, 20))

# URL Entry widget with placeholder text
url_name = customtkinter.CTkEntry(
    app, placeholder_text="Enter URL to scrape", width=300, font=("Arial", 14)
)
url_name.grid(row=1, column=0, padx=20, pady=(0, 10))

# File name Entry widget with placeholder text
file_name = customtkinter.CTkEntry(
    app, placeholder_text="File name for saved data", width=300, font=("Arial", 14)
)
file_name.grid(row=2, column=0, padx=20, pady=(0, 20))

# Function to call getUrl and handle URL and file name inputs
def f1():
    link = url_name.get()
    file = file_name.get()
    print("Link:", link, "\nFile Name:", file)
    result = getUrl(link, file)
    
    app.geometry("400x250")
    if result != True:
        lable_message = customtkinter.CTkLabel(
            app, text="Failed", font=("Arial", 20, "bold"), text_color="black", 
            fg_color="Red", width=150, corner_radius=20
        )
        lable_message.grid(row=3, column=0, padx=20, pady=10)
    else:
        lable_message = customtkinter.CTkLabel(
            app, text="Successful", font=("Arial", 20, "bold"), text_color="black", 
            fg_color="Green", width=150, corner_radius=20
        )
        lable_message.grid(row=3, column=0, padx=20, pady=10)
    
    # Clear the input fields
    url_name.delete(0, END)
    file_name.delete(0, END)
    
    # Close app after 3 seconds without freezing the UI
    app.after(3000, app.destroy)

# Process Button to trigger the scraping function
process = customtkinter.CTkButton(
    app, text="Start Scraping", command=f1, width=200, font=("Arial", 14, "bold")
)
process.grid(row=4, column=0, padx=20, pady=20)

# Run the app main loop
app.mainloop()
