import json
import customtkinter as ctk
from custom_utils.get_image_from_url import get_image_from_url
from library_cache.cache import build_cache
from custom_widgets.widgets import Top_Bar

def main():
    settings = json.load(open("settings.json"))

    ctk.set_appearance_mode("System")  # Modes: system (default), light, dark
    ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

    app = ctk.CTk()  # create CTk window like you do with the Tk window
    app_geometry = (800, 1200)
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
    # when the user enters a path into the top bar, save that path to settings.json
    # after saving, rerun cache retrieve and simple_cache build
    # display simple cache
    
    try:
        (cached_game_ids, library_cache) = build_cache(settings["libraryfoldersPath"])
        print(cached_game_ids)
        simple_cache = build_simple_cache(library_cache)
            
    except FileNotFoundError:
        # TODO: allow user to enter the path for their libraryfolders.vdf and save this to a settings.json
        warning_label = ctk.CTkLabel(scrollable_frame, text="libraryfolders.vdf not found, please set it with the button above\ndefault path: C:\Steam\steamapps\libraryfolders.vdf")
        warning_label.grid(row=0, column=0)


    Top_Bar(app, "Text 1", "Button 1").grid(row=0, column=0, sticky="nsew", padx=0, pady=0)

    text_box = ctk.CTkTextbox(app, app_x_res, app_y_res)
    text_box.insert("0.0" , ",\n".join(cached_game_ids))
    text_box.configure(state="disabled")

    display_simple_cache(scrollable_frame, simple_cache)
    
    app.mainloop()
    
def build_simple_cache(library_cache):
    simple_cache = []
    for game in library_cache:
        # TODO: ensure games from cache are validated (are dicts, contain `steam_appid` and more?) in `build_cache`
        if type(game) != dict:
            continue
        name = game.get("name", "not found")
        steam_appid = game.get("steam_appid", "not found")
        game_attributes = { "name": name, "steam_appid": steam_appid, "header_image": game.get("header_image", "not found")}
        if "not found" in game_attributes.values():
            continue
        simple_cache.append(game_attributes)
    return simple_cache


def display_simple_cache(master, simple_cache):
    for index, simple_game in enumerate(simple_cache):
        print(repr(simple_game))
        ( tk_image, img_width, img_height ) = get_image_from_url(simple_game["header_image"])
        master.panel = ctk.CTkLabel(master, image = tk_image, text="", width=img_width, height=img_height)
        master.panel.grid(row=index, column=0, padx=0, pady=5)
    
    
if __name__ == "__main__":
    main()