import json
import ctypes
import os
import customtkinter
import vdf
import requests

def get_cache():
    cached_game_ids: set[str] = set()
    cached_games = []
    data =[]
    
    try:
        print("reading cache")
        with open('data.json', 'r') as fp:
            data = json.load(fp)
    except FileNotFoundError:
        print("no cache, creating")
        with open('data.json', 'w') as fp:
            json.dump([], fp)
        return get_cache()

    if type(data) == list:
        print(f"list is good")
        print(f"length list: {len(data)}")
        for game in data:
            print(repr(game)[:15])
            if type(game) == dict and "steam_appid" in game.keys():
                print(f"adding game: {game["steam_appid"]}")
                cached_games.append(game)
                cached_game_ids.add(str(game["steam_appid"]))
            else:
                cached_game_ids.add(game)
    return (cached_game_ids, cached_games)

def main():
    print("starting app")
    (cached_game_ids, cached_games) = get_cache()
    print("cache read")
    print("cached_games:", repr(cached_games)[:50] + "...")

    library_location = "C:\Steam\steamapps\libraryfolders.vdf"
    library_dict = vdf.load(open(library_location))["libraryfolders"]["0"]["apps"]
    library_game_ids = set([key for key in library_dict.keys()])

    not_cached_ids = library_game_ids - cached_game_ids
    print(f"cached: {cached_game_ids}")
    print(f"not cached: {not_cached_ids}")
    games_to_cache = []
    for game in not_cached_ids:
        print(f"fetching {game}")
        response_data = game
        # response_data = get_game_details(game)
        game_to_cache = str(game) if type(response_data) == str else response_data
        games_to_cache.append(game_to_cache)
    
    new_cache = cached_games.copy()
    for game in games_to_cache:
        new_cache.append(game)

    # with open('data.json', 'w') as fp:
    #     json.dump(new_cache, fp)
    
    customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
    customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

    app = customtkinter.CTk()  # create CTk window like you do with the Tk window
    app_geometry = (800, 480)
    (app_x_res, app_y_res) = app_geometry
    app.geometry(f"{app_x_res}x{app_y_res}")

    text_box = customtkinter.CTkTextbox(app, app_x_res, app_y_res)
    text_box.insert("0.0" , ",\n".join(library_game_ids))
    text_box.configure(state="disabled")
    text_box.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)


    app.mainloop()

def get_game_details(app_id):
    url = f"https://store.steampowered.com/api/appdetails?appids={app_id}"
    response = requests.get(url)
    data = response.json()

    if data[str(app_id)]['success']:
        game_data = data[str(app_id)]['data']
        return game_data
        # return {
        #     'name': name,
        #     'description': description,
        #     'price': price
        # }
    else:
        return 'details not found'

if __name__ == "__main__":  
    main()
