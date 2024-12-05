import json
import vdf
import requests
import os
from operator import itemgetter
import dotenv

def get_cache():
    cached_game_ids: set[str] = set()
    cached_games = []
    file_data =[]

    try:
        print("reading cache")
        with open('game_data.json', 'r') as fp:
            file_data = json.load(fp)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print("no cache, creating")
        with open('game_data.json', 'w') as fp:
            json.dump([], fp)

    for game in file_data:
        if type(game) == dict and "steam_appid" in game.keys():
            print(f"found game: {game["steam_appid"]}")
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
        print(f"{library_location} doesn't exist")
        return (set(),[])

    (cached_game_ids, cached_games) = get_cache()
    print("cached_games:", repr(cached_games)[:50] + "...")

    library_dict = vdf.load(open(library_location))["libraryfolders"]["0"]["apps"]
    library_game_ids = set([key for key in library_dict.keys()])

    ids_removed_since_last_cache = cached_game_ids - library_game_ids
    print("ids_removed_since_last_cache: ", ids_removed_since_last_cache)
    not_cached_ids = library_game_ids - cached_game_ids
    print(f"cached: {cached_game_ids}")
    print(f"not cached: {not_cached_ids}")
    new_cache_ids = set()
    new_cache = []
    for game in not_cached_ids:
        print(f"fetching {game}")
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

def get_combined_cache_and_simple_cache(settings, simple_cache_sort_function=lambda game: game["name"].lower()):
    (cached_game_ids, library_cache) = build_cache(settings["libraryfoldersPath"])
    simple_cache = build_simple_cache(library_cache)
    simple_cache = sorted(simple_cache, key=simple_cache_sort_function)
    return (cached_game_ids, library_cache, simple_cache)

def build_simple_cache(library_cache):
    simple_cache = []
    for game in library_cache:
        # TODO: ensure games from cache are validated (are dicts, contain `steam_appid` and more?) in `build_cache` instead of other places
        if type(game) != dict:
            continue
        name = game.get("name", "not found")
        steam_appid = game.get("steam_appid", "not found")
        game_attributes = { "name": name, "steam_appid": steam_appid, "header_image": game.get("header_image", "not found")}
        if "not found" in game_attributes.values():
            continue
        simple_cache.append(game_attributes)
    return simple_cache

def get_user(loginusers_location):
    # user id can be found here c:\Steam\config\loginusers.vdf
    file_data =[]
    if not os.path.exists(loginusers_location):
        print(f"{loginusers_location} doesn't exist")
        return (set(),[])

    try:
        print("reading time cache")
        with open('game_time_data.json', 'r') as fp:
            file_data = json.load(fp)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print("no time cache, creating")
        with open('game_time_data.json', 'w') as fp:
            json.dump([], fp)
    loginusers_dict = vdf.load(open(loginusers_location))["users"]
    most_recent_user_id = None
    if len(loginusers_dict.keys()) == 1:
        print(type(loginusers_dict))
        print(loginusers_dict)
        most_recent_user_id = list(loginusers_dict.keys())[0]
    else:
        # TODO: add support for multiple users, each 
        most_recent_user_id = loginusers_dict.keys()[0]
        
    
    most_recent_user = (most_recent_user_id, "account_name")
    dotenv.set_key(".env", "USERID", most_recent_user[0])
    return most_recent_user

def get_playtimes(api_key=dotenv.get_key(".env", "STEAM_API_KEY"), user_id=dotenv.get_key(".env", "USERID")):
    request = f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={api_key}&steamid={user_id}&include_appinfo=true&format=json"
    response = requests.get(request)
    print(response.json())
    pass