from io import BytesIO
import customtkinter
from PIL import Image
import requests

def get_image_from_url(url):
    example_image_response =  requests.get(url)
    print(f"{url}\n{example_image_response.status_code}")
    example_image = Image.open(BytesIO(example_image_response.content))

    tk_image = customtkinter.CTkImage(example_image, size=(example_image.width, example_image.height))
    (width, height) = (example_image.width, example_image.height)
    return (tk_image, width, height)