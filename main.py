import json
import customtkinter as ctk
from custom_utils.get_image_from_url import get_image_from_url
from library_cache.cache import build_cache
from custom_widgets.widgets import Top_Bar, Game_Card

def main():
    settings = json.load(open("settings.json"))

    ctk.set_appearance_mode("System")  # Modes: system (default), light, dark
    ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

    app = ctk.CTk()  # create CTk window like you do with the Tk window
    app_geometry = (1200, 1200)
    (app_x_res, app_y_res) = app_geometry
    app.geometry(f"{app_x_res}x{app_y_res}")

    # text_box.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

    scrollable_frame = ctk.CTkScrollableFrame(master=app, width=app_x_res, height=app_y_res)
    app.grid_rowconfigure(0, weight=0)
    app.grid_rowconfigure(1, weight=1)
    app.grid_columnconfigure(0, weight=1)
    scrollable_frame.grid(row=1, column=0, padx=0, pady=0, sticky="nsew")
    
    simple_cache = []
    (cached_game_ids, library_cache) = ([], [])
    
    #x get user's libraryfolders
    #x check settings.json for libraryfoldersPath
    #x if it libraryfolders isn't found, display warning message
    #x when the user enters a path into the top bar, save that path to settings.json
    # after saving, rerun cache retrieve and simple_cache build
    # display simple cache
    
    try:
        # user id can be found here c:\Steam\config\loginusers.vdf
        cached_game_ids, library_cache, simple_cache = build_and_display_cache(settings)

    except (FileNotFoundError, KeyError):
        # TODO: allow user to enter the path for their libraryfolders.vdf and save this to a settings.json
        warning_label = ctk.CTkLabel(scrollable_frame, anchor="w", justify=ctk.LEFT, text="A valid libraryfolders.vdf has not found, please set it with the button above\nDefault path: C:\\Program Files (x86)\\Steam\\steamapps\\libraryfolders.vdf")
        warning_label.grid(row=0, column=0)


    Top_Bar(app, build_and_display_cache).grid(row=0, column=0, sticky="nsew", padx=0, pady=0)

    game_card_list = display_simple_cache(scrollable_frame, simple_cache)
    
    app.mainloop()
    
def remove_game_cards(game_card_list):
    for game_card in game_card_list:
        game_card.place_forget()
    
def build_and_display_cache(settings):
    (cached_game_ids, library_cache) = build_cache(settings["libraryfoldersPath"])
    simple_cache = build_simple_cache(library_cache)
    return (cached_game_ids, library_cache, simple_cache)
    
def build_simple_cache(library_cache):
    simple_cache = []
    for game in library_cache:
        # TODO: ensure games from cache are validated (are dicts, contain `steam_appid` and more?) in `build_cache`
        if type(game) != dict:
            continue
        name = game.get("name", "not found")
        steam_appid = game.get("steam_appid", "not found")
        game_attributes = { "name": name, "steam_appid": steam_appid, "header_image": game.get("header_image", "not found")}
        print(repr(game_attributes))
        if "not found" in game_attributes.values():
            continue
        simple_cache.append(game_attributes)
    return simple_cache


def display_simple_cache(master, simple_cache):
    game_cards = []
    for index, simple_game in enumerate(simple_cache):
        game_image = ( tk_image, img_width, img_height ) = get_image_from_url(simple_game["header_image"])
        # master.panel.grid(row=index, column=0, padx=0, pady=5)
        game_card = Game_Card(master, game_image, simple_game["name"]).grid(row=index, column=0, padx=0, pady=5, sticky="ew")
        game_cards.append(game_card)
    return game_cards
    
if __name__ == "__main__":
    main()