import json
import re
import os
import customtkinter as ctk
from utils import get_image_from_url
from cache import get_combined_cache_and_simple_cache
import dotenv

class Game_Card(ctk.CTkFrame):
    def __init__(self, parent, image, game_name):
        super().__init__(master = parent)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure((0,1), weight=0)
        self.grid_columnconfigure(2, weight=1)

        ( image_data, img_width, img_height ) = image
        image_card = ctk.CTkLabel(self, image = image_data, text="")
        image_card.grid(row=0, column=0, pady=(0,0), sticky="w")

        name_label = ctk.CTkLabel(self, text=game_name, font=ctk.CTkFont(family="",size=26))
        name_label.grid(row=0, column=1, padx=(30,0))

class Top_Bar(ctk.CTkFrame):
    scrollable_frame: ctk.CTkScrollableFrame
    game_cards: list[ctk.CTkFrame] = []

    def __init__(self, parent, build_and_display_cache, scrollable_frame):
        super().__init__(master = parent)
        self.build_and_display_cache = build_and_display_cache
        self.scrollable_frame = scrollable_frame
        
        # set up grid layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure((1,3), weight=0)
        self.grid_columnconfigure(2, weight=1)

        # TODO: allow users to save the path by pressing enter while focused on the box
        libraryfolders_path_entry = ctk.CTkEntry(self, placeholder_text=json.load(open("settings.json"))["libraryfoldersPath"])
        libraryfolders_path_entry.grid(row=0, column=0, pady=(10,0), padx=(5, 0), sticky="ew")

        libraryfolders_path_save = ctk.CTkButton( self, text="Save", command=lambda: self.save_path_and_display_games(libraryfolders_path_entry.get()))
        libraryfolders_path_save.grid(row=0, column=1, pady=(10,0))

        spacer = ctk.CTkLabel(self, text="").grid(row=0, column=2, pady=(10,0))

        sort_dropdown = ctk.CTkOptionMenu(self, values=["Sort by:", "Potential playtime", "Highest rated"])
        sort_dropdown.set("Sort by:")
        sort_dropdown.grid(row=0, column=3, pady=(10,0), padx=(0, 5))
        
    def display_games_with_simple_cache(self, simple_cache):
        for game_card in self.game_cards:
            game_card.grid_forget()
        self.game_cards = []
        for index, simple_game in enumerate(simple_cache):
            game_image = ( tk_image, img_width, img_height ) = get_image_from_url(simple_game["header_image"])
            game_card = Game_Card(self.scrollable_frame, game_image, simple_game["name"])
            game_card.grid(row=index, column=0, padx=0, pady=5, sticky="ew")
            self.game_cards.append(game_card)
        
    def save_path_and_display_games(self, new_path):
        self.save_libraryfolders_path_to_settings(new_path)
        self.build_and_display_cache(json.load(open("settings.json")))
        cached_game_ids, library_cache, simple_cache = get_combined_cache_and_simple_cache(json.load(open("settings.json")))
        self.display_games_with_simple_cache(simple_cache)
    
    def save_libraryfolders_path_to_settings(self, new_path: str):
        if not os.path.exists(new_path):
            return
        new_path = new_path.replace("/", "\\")
        user_path_cleaned = re.sub(r"(\?<!\\)\\(\?!\\)", r"\\", new_path)
        settings = json.load(open("settings.json"))
        settings["libraryfoldersPath"] = user_path_cleaned
        with open("settings.json", "w") as settings_file:
            json.dump(settings, settings_file, indent=4)