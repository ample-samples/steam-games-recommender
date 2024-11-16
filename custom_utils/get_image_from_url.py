from io import BytesIO
import customtkinter
from PIL import Image
import requests

def get_image_from_url(url):
    image_response =  requests.get(url)
    image = Image.open(BytesIO(image_response.content))
    print(f"fetched {url} | res:{image_response.status_code}")

    tk_image = customtkinter.CTkImage(image, size=(image.width, image.height))
    (width, height) = (image.width, image.height)
    return (tk_image, width, height)