    """ This working module contains functions that have nothing to do in the main file, but without which nothing will work.

    Functions:
        symbols_extract: Creates a list of symbols used when displaying an image from the file name
    """

import os

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