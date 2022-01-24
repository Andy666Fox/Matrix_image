# import libraries

from turtle import color
import pygame as pg
import numpy as np
import random
from funcs import *
from conf_window import  *

from loguru import logger  

logger.add('matrix_log.txt', format="<green>{time}</green> <level>{message}</level>")


# In order not to write the path to the file every time and not to go into the code myself, 
# I left this task to the user. Now it's both convenient and cool

image_path, font_SIZE, sym_stroke, im_color = set_params_window() # Take info from main settings window

# Small change on the next line. If the user has entered their characters in the dialog box, they will be used for display.
# If not, as before, the characters are taken from the file name (more in the Readme)

symbols = sym_stroke if sym_stroke else symbols_extract(image_path)

# Wrapping the file path into a function to convert the image format
try:
    image_path = extension_check(image_path)
    image_path = im_contrast(image_path)
except Exception:
    error_popup()



# main class for image MATRIXOFICATION ))
class Matrix:
    def __init__(self, app, font_size=font_SIZE):
        """ Initialization function. Sets the parameters of the main window and symbols

        Args:
            app (self): Main window
            font_size ([int], optional): The size of the characters. Affects the display quality. Defaults to font_SIZE.
        """
        
        self.app = app
        self.FONT_SIZE = font_size
        self.SIZE = self.ROWS, self.COLS = app.HEIGHT // font_size, app.WIDTH // font_size
        self.katakana = np.array([random.choice(symbols) for i in range(100)] + [' ' for i in range(5)])
        self.font = pg.font.SysFont('Arial', font_size, bold=True)
        
        # This block is responsible for creating a random position for symbols and adding them to the screen.
        self.matrix = np.random.choice(self.katakana, self.SIZE)
        self.char_intervals = np.random.randint(25, 50, size=self.SIZE)
        self.cols_speed = np.random.randint(100, 250, size=self.SIZE)
        self.prerendered_chars, self.color = self.get_prerendered_chars(color=im_color)
        
        self.image = self.get_image(image_path)


    def get_image(self, path_to_file: str) -> pg.PixelArray:
        """Function for representing an image as pg.PixelArray (analog of np.array)

        Args:
            path_to_file ([str]): The path to the file from the user

        Returns:
            [pg.PixelArray]: Format for further processing
        """
        
        image = pg.image.load(path_to_file)
        image = pg.transform.scale(image, self.app.RES)
        pixel_array = pg.pixelarray.PixelArray(image)
        return pixel_array

    # We need to pre-render some chars for optimization
    # TODO Get more optimize this block
    def get_prerendered_chars(self, color='green'):
        """It is quite expensive to prepare and render symbols at runtime.
           This function prepares a block of symbols before executing the program. All that remains is to draw them.

        Returns:
            [dict]: Returns a dictionary of symbols ready to be drawn
        """
        
        # Checking of changed color
        if color == 'red':
            char_colors = [(red, 0, 0) for red in range(256)]
        elif color == 'blue':
            char_colors = [(0, 0, blue) for blue in range(256)]
        else:
            char_colors = [(0, green, 0) for green in range(256)]
        prerendered_chars = {}
        for char in self.katakana:
            prerendered_char = {(char, color): self.font.render(char, True, color) for color in char_colors}
            prerendered_chars.update(prerendered_char)
        return prerendered_chars, color

    
    def run(self):
        """Program start function
        """
        
        frames = pg.time.get_ticks()
        self.change_chars(frames)
        self.shift_column(frames)
        self.draw()

    
    def shift_column(self, frames: int) -> np.roll:
        """Function for calculating the speed of falling symbols

        Args:
            frames (int): number of frames per unit of time
        """
        
        num_cols = np.argwhere(frames % self.cols_speed == 0)
        num_cols = num_cols[:, 1]
        num_cols = np.unique(num_cols)
        self.matrix[:, num_cols] = np.roll(self.matrix[:, num_cols], shift=1, axis=0)

    
    def change_chars(self, frames: int) -> list:
        """Function for creating a new set of symbols

        Args:
            frames (int): number of frames per unit of time
        """
        
        mask = np.argwhere(frames % self.char_intervals == 0)
        new_chars = np.random.choice(self.katakana, mask.shape[0])
        self.matrix[mask[:, 0], mask[:, 1]] = new_chars

    
    def draw(self):
        """Main draw function
        """
        
        for y, row in enumerate(self.matrix):
            for x, char in enumerate(row):
                if char:
                    pos = x * self.FONT_SIZE, y * self.FONT_SIZE
                    _, red, green, blue = pg.Color(self.image[pos])
                    if red and green and blue:
                        color = (red + green + blue) // 3
                        color = 255 if 245 < color < 250 else color
                        
                        # TODO WTF? Make this block more shorter
                        if self.color == 'red':
                            char = self.prerendered_chars[(char, (color, 0, 0))]
                        elif self.color == 'blue':
                            char = self.prerendered_chars[(char, (0, 0, color))]
                        else:
                            char = self.prerendered_chars[(char, (0, color, 0))]
                        char.set_alpha(color)
                        self.app.surface.blit(char, pos)
                        

# Main worker
class MatrixVision:
    """Convenient class helper
    """
    def __init__(self):
        self.RES = self.WIDTH, self.HEIGHT = get_image_size(image_path) 
        
        pg.init()
        
        self.screen = pg.display.set_mode(self.RES)
        self.surface = pg.Surface(self.RES)
        self.clock = pg.time.Clock()
        self.matrix = Matrix(self)


    def draw(self):
        
        self.surface.fill(pg.Color('black'))
        self.matrix.run()
        self.screen.blit(self.surface, (0, 0))
    
    def run(self):
        
        while True:
            self.draw()
            [exit() for i in pg.event.get() if i.type == pg.QUIT]
            pg.display.flip()
            self.clock.tick(30)
    
    # TODO optimize this shit
    logger.log('INFO', f'INPUT:\n    | Image Path: {image_path}|\n    | Font Size: {font_SIZE} |\n    | Changed symbols: {symbols} |\n    | Changed color: {im_color} |\n    | --Program worked fine-- |\n' + '-' * 30)


if __name__ == '__main__':
    
    app = MatrixVision()
    app.run()

    

