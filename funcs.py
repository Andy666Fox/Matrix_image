import os

def symbols_extract(path_to_image: str) -> list:
    corrected_name = os.path.basename(path_to_image)[:-4]
    res = [elem for elem in corrected_name]
    return res