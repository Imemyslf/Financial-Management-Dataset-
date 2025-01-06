import customtkinter
from customtkinter import *
from main import getUrl
import os
# Initialize the main app window
app = CTk()
app.title("Scraper")
app.geometry("400x200")
app.resizable(False, False)

# Configure overall grid layout for better alignment
app.grid_columnconfigure(0, weight=1)
    
# Title label for the application
title_label = customtkinter.CTkLabel(app, text="Web Scraper Tool", font=("Arial", 20, "bold"))
title_label.grid(row=0, column=0, padx=10, pady=(10, 20))

# URL Entry widget with placeholder text
url_name = customtkinter.CTkEntry(app, placeholder_text="Enter URL to scrape", width=300, font=("Arial", 14))
url_name.grid(row=1, column=0, padx=20, pady=(0, 10))

# File name Entry widget with placeholder text
file_name = customtkinter.CTkEntry(app, placeholder_text="File name for saved data", width=300, font=("Arial", 14))
file_name.grid(row=2, column=0, padx=20, pady=(0, 20))

# Create a frame to hold the button and label_message side by side
button_frame = customtkinter.CTkFrame(app,fg_color="transparent")
button_frame.grid(row=4, column=0, padx=20, pady=20)

# Function to update label color
def update_label_color(color):
    label_message.configure(fg_color=color)

# Function to call getUrl and handle URL and file name inputs
def f1():
    # Set label to grey initially to indicate processing
    update_label_color("grey")
    for i in range(0,2):
        print(i)
    
    n = 9
    dir_list = []
    for i in range(0,n):
        dir_list.append(str(n))
        n -= 1
    print(dir_list)
    
    for i in range(0,2):
        print(i)
    
    n = 9
    for i in range(0,n):
        print("Loop start")
        if i == 0:
            link = url_name.get()
            file = dir_list[i]
        else:
            url = url_name.get().split("/")
            string = url[-1]

            # Find the position of #
            j = string.find('#')

            # Insert "/{i+1}" before #
            if j != -1:
                modified_string = string[:j] + f"/{i+1}" + string[j:]
                print(modified_string)

            url[-1] = modified_string
            # print()
            link = '/'.join(url) 
            file = dir_list[i]
        print(i,link,file)

        # #  Call getUrl function and check result
        result = getUrl(link, file)
        
        # Update label color based on success or failure
        if result:
            update_label_color("green")
        else:
            update_label_color("red")
        
        # Reset label color to grey after 3 seconds
        app.after(3000, lambda: update_label_color("grey"))
    
    url_name.delete(0, END)
    file_name.delete(0, END)

# Process Button to trigger the scraping function
process = customtkinter.CTkButton(button_frame, text="Start Scraping", command=f1, width=180, font=("Arial", 14, "bold"))
process.grid(row=0, column=0, padx=(0, 50))  # Increased right padding for more spacing

# Label to indicate the status
label_message = customtkinter.CTkLabel(button_frame, text="", width=15, height=15, fg_color="grey", corner_radius=12)
label_message.grid(row=0, column=1, padx=(50, 0))  # Left padding to move it toward the corner

# Run the app main loop
app.mainloop()