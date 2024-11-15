import json
import re
import os
from customtkinter import CTkFrame, CTkButton, CTkEntry, CTkLabel, CTkComboBox, CTkOptionMenu

class Top_Bar(CTkFrame):
    def __init__(self, parent, label_text, button_text):
        super().__init__(master = parent)
        
        # set up grid layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure((0,1,3), weight=0)
        self.grid_columnconfigure(2, weight=1)

        libraryfolders_path_entry = CTkEntry(self, placeholder_text=json.load(open("settings.json"))["libraryfoldersPath"])
        libraryfolders_path_entry.grid(row=0, column=0, pady=(10,0), padx=(5, 0))

        # libraryfolders_path_save = CTkButton(self, text="Save", command=lambda: print(libraryfolders_path_entry.get()))
        libraryfolders_path_save = CTkButton(self, text="Save", command=lambda: self.save_libraryfolders_path_to_settings(libraryfolders_path_entry.get()))
        libraryfolders_path_save.grid(row=0, column=1, pady=(10,0))

        spacer = CTkLabel(self, text="").grid(row=0, column=2, pady=(10,0))

        sort_dropdown = CTkOptionMenu(self, values=["Sort by:", "Potential playtime", "Highest rated"])
        sort_dropdown.set("Sort by:")
        sort_dropdown.grid(row=0, column=3, pady=(10,0), padx=(0, 5))
    
    def save_libraryfolders_path_to_settings(self, new_path: str):
        print(new_path)
        new_path = new_path.replace('\\', r"\\")
        new_path = new_path.replace("/", "\\")
        user_path_cleaned = re.sub(r"(\?<!\\)\\(\?!\\)", r"\\", new_path)
        if not os.path.exists(user_path_cleaned):
            return

        settings = json.load(open("settings.json"))
        settings["libraryfoldersPath"] = user_path_cleaned
        with open("settings.json", "w") as settings_file:
            json.dump(settings, settings_file)
