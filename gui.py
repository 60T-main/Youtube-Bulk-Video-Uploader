from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askdirectory
import sys
import threading
from project import check_creds, uploader


# Console redirect class (to show console on GUI)
class gui_console():
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, text):
        self.text_widget.insert('end', text)
        self.text_widget.see('end')

class GUI():

    def __init__(self):
        
        # Window setup
        self.window = Tk()
        self.window.title("YouTube Bulk Uploader")
        self.window.resizable(True, True)
        # icon
        icon = PhotoImage(file='youtube-123.png')  
        self.window.iconphoto(True, icon)
        # styles
        style = ttk.Style()
        style.configure('TButton', font=('Roboto', 10), padding=6)
        style.configure('TLabel', font=('Roboto', 12, 'bold'))
        # label
        label_select = ttk.Label(self.window, text="Select the Videos Folder")
        label_select.grid(row=0, column=0, columnspan=2, pady=(20, 10), padx=20)
        # read only text entry for showing folder path 
        self.path_var = StringVar()
        path_entry = ttk.Entry(self.window, textvariable=self.path_var, width=50, state='readonly')
        path_entry.grid(row=1, column=0, padx=(20, 10), pady=10)

        # description entry
        label_desc = ttk.Label(self.window, text="Type video desctiption")
        label_desc.grid(row=2, column=0, columnspan=2, pady=(20, 10), padx=20)
        self.desc_entry = Text(self.window, height=10, width=60,)
        self.desc_entry.grid(row=3, column=0, padx=(20, 10), pady=10)

        # browse button
        choose_btn = ttk.Button(self.window, text="Browse", command=self.choose_folder)  
        choose_btn.grid(row=1, column=2, padx=(0, 20), pady=10)
        # upload button
        upload_btn = ttk.Button(self.window, text="Upload", command=self.start_upload)  
        upload_btn.grid(row=4, column=0, columnspan=2, padx=(0, 20), pady=10)

        # creates GUI console
        self.text_widget = Text(self.window, height=10, width=60)
        self.text_widget.grid(row=5, column=0, columnspan=2, padx=20, pady=(10, 20), sticky="nsew")

        self.window.grid_rowconfigure(3, weight=1)
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=1)


        # Redirect stdout/stderr for GUI console 
        sys.stdout = gui_console(self.text_widget)
        sys.stderr = gui_console(self.text_widget)


    ## GUI functions 
    def choose_folder(self):
        path = askdirectory(title="Choose Folder")
        if path:
            self.path_var.set(path) 
        return None 

    # gathers data and starts upload proccess in separete thread 
    def start_upload(self):
        folder_path = self.path_var.get()
        description = self.desc_entry.get("1.0", "end").strip()
        print(f"Selected folder: {folder_path}")
        print(f"Description: {description}")
        if folder_path:
            # added threading to avoid gui freezes during upload 
            thread = threading.Thread(target=self.run_upload, args=(folder_path, description))
            thread.start()

    # actual upload process
    def run_upload(self,folder_path, description):
        try:
            creds = check_creds()
            uploader(creds, folder_path, description)
        except Exception as e:
            print(f"Error: {e}")



from project import check_creds, uploader

if __name__ == "__main__":
    obj = GUI()
    obj.window.mainloop()