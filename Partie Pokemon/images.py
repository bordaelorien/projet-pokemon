
from PIL import Image, ImageTk
from paths import *

def imagePokemon(id,name, size=(400, 400)):
    """
    Charge les images des pokmemons et les redimensionne
    """
    img = Image.open(pathPokemon(id, name.lower()))
    img = img.resize(size, Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(img)

