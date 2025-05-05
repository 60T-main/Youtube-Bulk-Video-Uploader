from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askdirectory
import sys

# Console redirect class
class gui_console():
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, text):
        self.text_widget.insert('end', text)
        self.text_widget.see('end')

# GUI functions 
def choose_folder():
    path = askdirectory(title="Choose Folder")
    if path:
        path_var.set(path) 
    return None 

def start_upload():
    folder_path = path_var.get()
    print(folder_path)
    if folder_path:  
        creds = check_creds()  
        uploader(creds, folder_path)  

# Window setup
window = Tk()
window.title("YouTube Bulk Uploader")
window.resizable(True, True)

icon = PhotoImage(file='youtube-123.png')  
window.iconphoto(True, icon)

style = ttk.Style()
style.configure('TButton', font=('Roboto', 10), padding=6)
style.configure('TLabel', font=('Roboto', 12, 'bold'))

label = ttk.Label(window, text="Select the Videos Folder")
label.grid(row=0, column=0, columnspan=2, pady=(20, 10), padx=20)

path_var = StringVar()
path_entry = ttk.Entry(window, textvariable=path_var, width=50, state='readonly')
path_entry.grid(row=1, column=0, padx=(20, 10), pady=10)

choose_btn = ttk.Button(window, text="Browse", command=choose_folder)  
choose_btn.grid(row=1, column=1, padx=(0, 20), pady=10)

upload_btn = ttk.Button(window, text="Upload", command=start_upload)  
upload_btn.grid(row=2, column=0, columnspan=2, padx=(0, 20), pady=10)

text_widget = Text(window, height=10, width=60)
text_widget.grid(row=3, column=0, columnspan=2, padx=20, pady=(10, 20), sticky="nsew")

window.grid_rowconfigure(3, weight=1)
window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=1)


# Redirect stdout/stderr BEFORE importing uploader
sys.stdout = gui_console(text_widget)
sys.stderr = gui_console(text_widget)

from uploader import check_creds, uploader


window.mainloop()
