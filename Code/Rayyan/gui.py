# import customtkinter
# from customtkinter import *
from Main import getUrl

# Function to call getUrl and handle URL and file name inputs
def f1(href_link):
    # update_label_color("grey")  # Set label to grey initially to indicate processing

    print("\n\n href_link:- ",href_link)

    name = href_link
    company_data = name.split("/")[-2].capitalize()

    n = 9
    # Check if "moneycontrol" exists in the URL
    if "moneycontrol" in name:
        dir_list = [str(i) for i in range(n, 0, -1)]

        for i in range(0, n):
            print("\nLoop start")
            if i == 0:
                link = href_link
                print(f"{i} -> {link}")
                file = dir_list[i]
            else:
                url = href_link.split("/")
                string = url[-1]
                print("\n\n String:- ", string)

                # Find the position of #
                j = string.find('#')

                # Insert "/{i+1}" before #
                if j != -1:
                    modified_string = string[:j] + f"/{i+1}" + string[j:]
                    print("\n modified_string", modified_string)
                    if i >= 2:
                        modified_string = modified_string[2:]
                        print("\n new_modified_string", modified_string)

                print("\n\n Split modified String:- ", modified_string.split("/"))
                url[-1] = modified_string
                link = '/'.join(url)
                print(f"\n\n{i} -> {link}")
                file = dir_list[i]

                 # Insert the updated link

            # Call getUrl function and check result
            result = getUrl(link, file, "moneycontrol", company_data[:-2])

            # Update label color based on success or failure
            # if result:
            #    return "Success\n\n"
            # else:
            #    return "Failed\n\n"
                
    

# # Function to update label color
# def update_label_color(color):
#     label_message.configure(fg_color=color)

# # Function to handle option menu selection
# def optionmenu_callback(choice):
#     global n
#     n = int(choice)  # Convert selected option to integer
#     print("Option menu dropdown clicked:", n)

# # Initialize the main app window
# app = CTk()
# app.title("Scraper")
# app.geometry("400x300")
# app.resizable(False, False)

# # Configure overall grid layout for better alignment
# app.grid_columnconfigure(0, weight=1)

# # Title label for the application
# title_label = customtkinter.CTkLabel(app, text="Web Scraper Tool", font=("Arial", 20, "bold"))
# title_label.grid(row=0, column=0, padx=10, pady=(10, 20))

# # URL Entry widget with placeholder text
# url_name = customtkinter.CTkEntry(app, placeholder_text="Enter URL to scrape", width=300, font=("Arial", 14))
# url_name.grid(row=1, column=0, padx=20, pady=(0, 10))

# # Create a frame for option menu and label
# option_frame = customtkinter.CTkFrame(app, fg_color="transparent") 
# option_frame.grid(row=2, column=0, padx=20, pady=20)

# # Label for the option menu
# option_label = customtkinter.CTkLabel(option_frame, text="How many Years?", font=("Arial", 14, "bold"))
# option_label.grid(row=0, column=0, padx=(0, 10))  

# # Option menu for selecting years
# optionmenu_var = customtkinter.StringVar(value="10")  # Default value
# optionmenu = customtkinter.CTkOptionMenu(option_frame, values=["1", "3", "5", "10"],
#                                          command=optionmenu_callback,
#                                          variable=optionmenu_var)
# optionmenu.grid(row=0, column=1, padx=(10, 0))

# # Initialize 'n' with default value from option menu
# n = int(optionmenu_var.get())

# # Create a frame to hold the button and label_message side by side
# button_frame = customtkinter.CTkFrame(app, fg_color="transparent")
# button_frame.grid(row=4, column=0, padx=20, pady=20)

# # Process Button to trigger the scraping function
# process = customtkinter.CTkButton(button_frame, text="Start Scraping", command=f1, width=180, font=("Arial", 14, "bold"))
# process.grid(row=0, column=0, padx=(0, 50))  # Increased right padding for more spacing

# # Label to indicate the status
# label_message = customtkinter.CTkLabel(button_frame, text="", width=15, height=15, fg_color="grey", corner_radius=12)
# label_message.grid(row=0, column=1, padx=(50, 0))  # Left padding to move it toward the corner

# # Run the app main loop
# app.mainloop()
