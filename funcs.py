"""A module containing service functions. Not that it was so necessary, but it does not clog up the main file
"""

import os
import pygame as pg
import PIL
from PIL import  Image, ImageEnhance

#----------------------------------------------------------------

def symbols_extract(path_to_image: str) -> list:
    
    """ Utility function for extracting characters for further display
    
    Inputs:
        string [str]: path to file
    
    Returns:
        list [list]: List with symbols
    """
    
    corrected_name: str = str(os.path.basename(path_to_image)[:-4]).strip(' ')
    res: list[str] = [elem for elem in corrected_name]
    
    return res

#----------------------------------------------------------------

def get_image_size(path: str) -> tuple:
    
    """Utility function for determining the size of the image

    Returns:
        [tuple]: Returns a tuple with the dimensions of the image
    """
    return pg.image.load(path).get_size()

#----------------------------------------------------------------

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
        #os.remove(path)

    return path[:-4] + '.jpg'

#----------------------------------------------------------------


def im_contrast(path_to_file: str) -> str:
    
    """ Utility function increasing the contrast of the image

    Returns:
        str : Returns the path to a new image with increased contrast 
    """
    
    im: PIL.Image = Image.open(path_to_file)
    
    enhancer = ImageEnhance.Sharpness(im)
    res = enhancer.enhance(4)
    
    enhancer = ImageEnhance.Contrast(res)
    res = enhancer.enhance(2)
    
    new_path = f'redux_{path_to_file}'
    res.save(new_path)
    
    return new_path