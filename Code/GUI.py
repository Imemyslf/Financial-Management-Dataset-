import customtkinter
from customtkinter import *

app=CTk() 
app.title("Scrapper")

# win=CTkFrame(app)
# win.pack(padx=20,pady=20)

def f1():
    # print("Aditya")
    link=url_name.get()
    file=file_name.get()
    print(link,file)

url_name=customtkinter.CTkEntry(app,placeholder_text="Paste URL")
# url_name.insert("0.0","")
url_name.grid(row=0,column=0,padx=(10,0),pady=(0,10))



file_name=customtkinter.CTkEntry(app,placeholder_text="File name")
# file_name.insert("0.0","")
file_name.grid(row=1,column=0,padx=(10,0),pady=(0,10))

process=customtkinter.CTkButton(app,text="Process",command=f1)
process.grid(row=2,column=0,padx=(10,0),pady=(0,10))

app.mainloop()
