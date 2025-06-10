from tkinter import *
import tkinter as tk 
from tkinter import ttk
from tkinter.filedialog import askdirectory
import sys
import threading
from project import check_creds, uploader, get_playlists


# Console redirect class (to show console on GUI)
class gui_console():
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, text):
        self.text_widget.insert('end', text)
        self.text_widget.see('end')

class GUI():

    def __init__(self):
        
        # # COLUMN 1

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
        label_select_path = ttk.Label(self.window, text="Path to folder")
        label_select_path.grid(row=1, column=0, columnspan=2, pady=(20, 10), padx=20)
        self.path_var = StringVar()
        path_entry = ttk.Entry(self.window, textvariable=self.path_var, width=50, state='readonly')
        path_entry.grid(row=2, column=0, padx=(20, 10), pady=10,columnspan=2)

        # description entry
        label_desc = ttk.Label(self.window, text="Type video desctiption")
        label_desc.grid(row=3, column=0, columnspan=2, pady=(20, 10), padx=20)
        self.desc_entry = Text(self.window, height=10, width=60, bd=2, relief="groove")
        self.desc_entry.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")

        # upload button
        upload_btn = ttk.Button(self.window, text="Upload", command=self.start_upload)  
        upload_btn.grid(row=9, column=2, columnspan=1,padx=20, pady=10)


        # # COLUMN 2

        # Playlist label
        label_playlist = ttk.Label(self.window, text="Create Playlist")
        label_playlist.grid(row=0, column=3, columnspan=2, pady=(20, 10), padx=20)

        # Playlist title
        label_playlist_title = ttk.Label(self.window, text="Playlist Name")
        label_playlist_title.grid(row=1, column=3, columnspan=2, pady=(20, 10), padx=20)
        self.playlist_title_var = StringVar()
        playlist_title_entry = ttk.Entry(self.window, textvariable=self.playlist_title_var, width=50, state='write',)
        playlist_title_entry.grid(row=2, column=3, padx=10, pady=5,columnspan=2)

        # playlist entry
        playlist_desc = ttk.Label(self.window, text="Type Playlist desctiption")
        playlist_desc.grid(row=3, column=3, columnspan=2, pady=5, padx=10)
        self.playlist_desc_entry = Text(self.window, height=10, width=60,bd=2, relief="groove")
        self.playlist_desc_entry.grid(row=4, column=3, columnspan=2, padx=10, pady=5, sticky="nsew")

        # Playlist options label
        label_options = ttk.Label(self.window, text="OR choose existing playlist:")
        label_options.grid(row=5, column=3, columnspan=2, pady=(20, 10), padx=20)
        
        # playlist options

        self.selected_option = tk.StringVar()
        self.selected_option.set("Select Playlist or Album") 
        self.playlist_dropdown = tk.OptionMenu(self.window, self.selected_option, "") 
        self.playlist_dropdown.grid(row=6, column=3, columnspan=2, padx=10, pady=10, sticky="ew")

        # browse button
        choose_btn = ttk.Button(self.window, text="Browse", command=self.choose_folder)  
        choose_btn.grid(row=2, column=2, padx=(0, 20), pady=10)



        # # END OF COLUMNS

        # creates GUI console
        self.text_widget = Text(self.window, height=10, width=60, bd=2, relief="groove")
        self.text_widget.grid(row=10, column=1, columnspan=3, padx=(10,20), pady=(10, 20), sticky="nsew")

        # makes it so that content resizes with the window
        self.window.grid_rowconfigure(3, weight=1)
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=1)


        # Redirect stdout/stderr for GUI console 
        sys.stdout = gui_console(self.text_widget)
        sys.stderr = gui_console(self.text_widget)
        
        # ensures the gui is fully rendered before trying to fetch
        self.window.after(100, self.populate_playlist_dropdown)

    ## GUI functions 
    def choose_folder(self):
        path = askdirectory(title="Choose Folder")
        if path:
            self.path_var.set(path) 
        return None 
    
    # Fetches playlists and populates the dropdown menu.
    def populate_playlist_dropdown(self):
        try:
            playlists = get_playlists() 

            # Get the internal menu of the OptionMenu widget
            menu = self.playlist_dropdown["menu"]
            menu.delete(0, "end") # Clear any existing options

            if playlists:
                for playlist in playlists:
                    # Add each playlist as a command to the menu
                    # tk._setit is a helper function to set the StringVar
                    menu.add_command(label=playlist['name'], 
                                     command=tk._setit(self.selected_option, playlist['name']))
                
                # Set the default selected option to the first playlist
                
            else:
                self.selected_option.set("No playlists found")
                # Add a dummy option if no playlists are found, so the menu isn't completely empty
                menu.add_command(label="No playlists found", command=lambda: None)

        except Exception as e:
            print(f"Error loading playlists: {e}")
            self.selected_option.set("Error loading playlists")
            menu = self.playlist_dropdown["menu"]
            menu.delete(0, "end")
            menu.add_command(label="Error loading...", command=lambda: None)

    # gathers data and starts upload proccess in separete thread 
    def start_upload(self):
        folder_path = self.path_var.get()
        description = self.desc_entry.get("1.0", "end").strip()
        playlist_description = None

        # gather playlist enties
        if self.selected_option.get() and self.selected_option.get() != "Select Playlist or Album":
            playlist_title = self.selected_option.get().strip()
            
        elif self.playlist_title_var.get():
            playlist_title = self.playlist_title_var.get().strip()
            playlist_description = self.playlist_desc_entry.get("1.0", "end").strip()
        else:
            playlist_title = None
        
        print(f"Selected folder: {folder_path}")
        print(f"Description: {description}")
        print(f"Playlist: {playlist_title}") if playlist_title else None

        if folder_path:

            # added threading to avoid gui freezes during upload 
            thread = threading.Thread(target=self.run_upload, args=(folder_path, description, playlist_title, playlist_description ))
            thread.start()

    # actual upload process
    def run_upload(self, folder_path, description, playlist_title=None, playlist_desc=None):
        try:
            creds = check_creds()
            uploader(creds, folder_path, description, playlist_title, playlist_desc)
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    obj = GUI()
    obj.window.mainloop()