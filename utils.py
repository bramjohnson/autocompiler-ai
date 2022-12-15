from mutagen import File
from PIL import Image
from io import BytesIO
import shutil, os

Object = lambda **kwargs: type("Object", (), kwargs)

def title(song):
    return get_tag(song, "TIT2")[0].text[0]

def album (song):
    return get_tag(song, "TALB")[0].text[0]

def get_tag(song, tag):
    id3 = File(song)
    if tag in id3.keys():
        return id3.tags.getall(tag)
    else: return ["None"]

def get_album_art(song):
    art = get_tag(song, "APIC:")[0]
    if (art == "None"): shutil.copyfile("./resources/default.jpg", "cover.jpg")
    else:
        try:
            Image.open(BytesIO(art.data)).save("cover.jpg")
        except:
            shutil.copyfile("./resources/default.jpg", "cover.jpg")