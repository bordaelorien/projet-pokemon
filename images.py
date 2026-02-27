
from PIL import Image, ImageTk
from paths import *

def imagePokemon(id,name, size=(400, 400)):
    """
    charge les images des pokmemons et les redimensionne
    """
    img = Image.open(pathPokemon(id, name))
    img = img.resize(size, Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(img)

def ImageType1(pokemon):
    type=pokemon["Type 1"]
    imageType=pathType(type)
    return imageType

def ImageType2(pokemon):
    type=pokemon["Type 2"]
    if isinstance(type,str):
        imageType=pathType(type)
    else:
        imageType=False
    return imageType

