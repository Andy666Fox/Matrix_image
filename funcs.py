
import os
import pygame as pg
from PIL import  Image

def symbols_extract(path_to_image: str) -> list:
    
    """Main function for symbols extracting
    
    Inputs:
        string [str]: path to file
    
    Returns:
        list [list]: List with symbols
    """
    
    corrected_name = os.path.basename(path_to_image)[:-4]
    res = [elem for elem in corrected_name]
    return res

def get_image_size(path: str) -> tuple:
    
    """Utility function for determining the size of the image

    Returns:
        [tuple]: Returns a tuple with the dimensions of the image
    """
    return pg.image.load(path).get_size()

def extension_check(path: str) -> str:
    
    """Utility function needed to convert images to .jpg format

    Returns:
        [str]: The function converts the image to .jpg format, removes the original image and returns the path to the converted image
    """
    
    if path[-4:] == '.jpg':
        pass
    else:
        image = Image.open(path)
        bg = Image.new("RGB", image.size, (255,255,255))
        bg.paste(image,image)
        bg.save(f'{path[:-4]}.jpg')
        os.remove(path)

    return path[:-4] + '.jpg'