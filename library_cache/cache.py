import json
import vdf
import requests
import os

def get_cache():
    cached_game_ids: set[str] = set()
    cached_games = []
    file_data =[]

    try:
        with open('game_data.json', 'r') as fp:
            file_data = json.load(fp)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        with open('game_data.json', 'w') as fp:
            json.dump([], fp)

    for game in file_data:
        if type(game) == dict and "steam_appid" in game.keys():
            cached_games.append(game)
            cached_game_ids.add(str(game["steam_appid"]))
        else:
            cached_game_ids.add(game)
    return (cached_game_ids, cached_games)

def get_game_details(app_id):
    url = f"https://store.steampowered.com/api/appdetails?appids={app_id}"
    response = requests.get(url)
    data = response.json()

    if data[str(app_id)]['success']:
        game_data = data[str(app_id)]['data']
        return game_data
    else:
        return 'details not found'
    
def build_cache(library_location):
    if not os.path.exists(library_location):
        return (set(),[])

    (cached_game_ids, cached_games) = get_cache()

    library_dict = vdf.load(open(library_location))["libraryfolders"]["0"]["apps"]
    library_game_ids = set([key for key in library_dict.keys()])

    ids_removed_since_last_cache = cached_game_ids - library_game_ids
    not_cached_ids = library_game_ids - cached_game_ids
    new_cache_ids = set()
    new_cache = []
    for game in not_cached_ids:
        response_data = game
        response_data = get_game_details(game)
        game_to_cache = str(game) if type(response_data) == str else response_data
        new_cache.append(game_to_cache)
        cached_game_ids.add(game)
        new_cache_ids.add(game)

    for game in cached_games:
        game_id = game.get("steam_appid")
        if str(game_id) not in ids_removed_since_last_cache:
            new_cache.append(game)
            new_cache_ids.add(str(game_id))

    with open('game_data.json', 'w') as fp:
        json.dump(new_cache, fp)
    return (new_cache_ids, new_cache)