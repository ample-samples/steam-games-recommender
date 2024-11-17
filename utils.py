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
    import json

    default_settings = {"defaultLibraryfoldersPath": "C:\\Program Files (x86)\\Steam\\steamapps\\libraryfolders.vdf", "libraryfoldersPath": "C:\\Program Files (x86)\\Steam\\steamapps\\libraryfolders.vdf"}
    with open("settings.json", "w") as settings_json:
        json.dump(default_settings, settings_json)
    