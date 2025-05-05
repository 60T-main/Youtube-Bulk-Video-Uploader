from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askdirectory
from uploader import *  

def choose_folder():
    path = askdirectory(title="Choose Folder")
    if path:
        path_var.set(path) 
        return path
    return None 

def start_upload():
    folder_path = choose_folder()  
    if folder_path:  
        creds = check_creds()  
        uploader(creds, folder_path)  

# Create main window
window = Tk()
window.title("YouTube Bulk Uploader")
window.resizable(False, False)

# Icon
icon = PhotoImage(file='youtube-123.png')  
window.iconphoto(True, icon)

# Styling
style = ttk.Style()
style.configure('TButton', font=('Roboto', 10), padding=6)
style.configure('TLabel', font=('Roboto', 12, 'bold'))

# Label
label = ttk.Label(window, text="Select the Videos Folder")
label.grid(row=0, column=0, columnspan=2, pady=(20, 10), padx=20)

# Folder path display
path_var = StringVar()
path_entry = ttk.Entry(window, textvariable=path_var, width=50, state='readonly')
path_entry.grid(row=1, column=0, padx=(20, 10), pady=10)

# Button to choose folder
choose_btn = ttk.Button(window, text="Browse", command=start_upload)  
choose_btn.grid(row=1, column=1, padx=(0, 20), pady=10)

window.mainloop()
