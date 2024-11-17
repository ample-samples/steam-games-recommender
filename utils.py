import json

def get_image_from_url(url):
    from io import BytesIO
    import customtkinter
    from PIL import Image
    import requests

    image_response =  requests.get(url)
    image = Image.open(BytesIO(image_response.content))
    print(f"fetched {url} | res:{image_response.status_code}")

    tk_image = customtkinter.CTkImage(image, size=(image.width, image.height))
    (width, height) = (image.width, image.height)
    return (tk_image, width, height)


def generate_settings_json():
    default_settings = {
        "defaultLibraryfoldersPath": "C:\\Program Files (x86)\\Steam\\steamapps\\libraryfolders.vdf",
        "libraryfoldersPath": "C:\\Program Files (x86)\\Steam\\steamapps\\libraryfolders.vdf"
    }
    with open("settings.json", "w") as settings_json:
        json.dump(default_settings, settings_json)
    
def generate_env():
    env_template = """STEAM_API_KEY=
STEAM_API_DOMAIN_NAME="""
    with open(".env.temp", "w") as env_file:
        env_file.write(env_template)

def create_missing_files():
    try:
        json.load(open("settings.json"))
    except FileNotFoundError:
        generate_settings_json()

    try:
        open(".env.temp")
    except FileNotFoundError:
        generate_env()
