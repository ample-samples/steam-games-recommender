import json
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
    except (FileNotFoundError, json.JSONDecodeError) as e:
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

def get_game_details(app_id):
    url = f"https://store.steampowered.com/api/appdetails?appids={app_id}"
    response = requests.get(url)
    data = response.json()

    if data[str(app_id)]['success']:
        game_data = data[str(app_id)]['data']
        return game_data
    else:
        return 'details not found'
    
# TODO: fix sending an empty set when cache is first build
def build_cache(library_location):
    print("starting app")
    (cached_game_ids, cached_games) = get_cache()
    print("cache read")
    print("cached_games:", repr(cached_games)[:50] + "...")

    library_dict = vdf.load(open(library_location))["libraryfolders"]["0"]["apps"]
    library_game_ids = set([key for key in library_dict.keys()])

    not_cached_ids = library_game_ids - cached_game_ids
    print(f"cached: {cached_game_ids}")
    print(f"not cached: {not_cached_ids}")
    games_to_cache = []
    for game in not_cached_ids:
        print(f"fetching {game}")
        response_data = game
        response_data = get_game_details(game)
        game_to_cache = str(game) if type(response_data) == str else response_data
        games_to_cache.append(game_to_cache)
    
    new_cache = cached_games.copy()
    for game in games_to_cache:
        new_cache.append(game)

    with open('data.json', 'w') as fp:
        json.dump(new_cache, fp)
    return (cached_game_ids, new_cache)