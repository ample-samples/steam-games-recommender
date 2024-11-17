import json
import customtkinter as ctk
from utils import create_missing_files
from cache import get_combined_cache_and_simple_cache
from widgets import Top_Bar

def main():
    create_missing_files()
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app_geometry = (800, 800)
    (app_x_res, app_y_res) = app_geometry
    app.geometry(f"{app_x_res}x{app_y_res}")

    scrollable_frame = ctk.CTkScrollableFrame(master=app, width=app_x_res, height=app_y_res)
    app.grid_rowconfigure(0, weight=0)
    app.grid_rowconfigure(1, weight=1)
    app.grid_columnconfigure(0, weight=1)
    scrollable_frame.grid(row=1, column=0, padx=0, pady=0, sticky="nsew")
    
    simple_cache = []
    (cached_game_ids, library_cache) = ([], [])
    
    try:
        # user id can be found here c:\Steam\config\loginusers.vdf
        cached_game_ids, library_cache, simple_cache = get_combined_cache_and_simple_cache(json.load(open("settings.json")))

    except (FileNotFoundError, KeyError):
        # TODO: allow user to enter the path for their libraryfolders.vdf and save this to a settings.json
        warning_label = ctk.CTkLabel(scrollable_frame, anchor="w", justify=ctk.LEFT, text="A valid libraryfolders.vdf has not found, please set it with the button above\nDefault path: C:\\Program Files (x86)\\Steam\\steamapps\\libraryfolders.vdf\nPlease restart the application after saving the path")
        warning_label.grid(row=0, column=0)
    if len(cached_game_ids) == 0:
        warning_label = ctk.CTkLabel(scrollable_frame, anchor="w", justify=ctk.LEFT, text="No games have been found in libraryfolders.vdf, are you sure it's been set correctly using the button above?\nDefault path: C:\\Program Files (x86)\\Steam\\steamapps\\libraryfolders.vdf\nPlease restart the application after saving the path")
        warning_label.grid(row=0, column=0)


    top_bar = Top_Bar(app, get_combined_cache_and_simple_cache, scrollable_frame)
    top_bar.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)

    game_card_list = top_bar.display_games_with_simple_cache(simple_cache)
    
    app.mainloop()
    
def remove_game_cards(game_card_list):
    for game_card in game_card_list:
        game_card.place_forget()

if __name__ == "__main__":
    main()