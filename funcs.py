
import os
import pygame as pg

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
    return pg.image.load(path).get_size()