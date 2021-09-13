# import libraries
import pygame as pg
import numpy as np
import random
from funcs import *
from conf_window import  *


# In order not to write the path to the file every time and not to go into the code myself, 
# I left this task to the user. Now it's both convenient and cool

image_path, font_SIZE = set_params_window()


# Wrapping the file path into a function to convert the image format
image_path = extension_check(image_path)



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
        self.katakana = np.array([random.choice(symbols_extract(image_path)) for i in range(100)] + [' ' for i in range(5)])
        self.font = pg.font.SysFont('Arial', font_size, bold=True)

        # This block is responsible for creating a random position for symbols and adding them to the screen.
        self.matrix = np.random.choice(self.katakana, self.SIZE)
        self.char_intervals = np.random.randint(25, 50, size=self.SIZE)
        self.cols_speed = np.random.randint(100, 250, size=self.SIZE)
        self.prerendered_chars = self.get_prerendered_chars()

        # TODO  Make image change more easier
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
    def get_prerendered_chars(self):
        """It is quite expensive to prepare and render symbols at runtime.
           This function prepares a block of symbols before executing the program. All that remains is to draw them.

        Returns:
            [dict]: Returns a dictionary of symbols ready to be drawn
        """
        char_colors = [(0, green, 0) for green in range(256)]
        prerendered_chars = {}
        for char in self.katakana:
            prerendered_char = {(char, color): self.font.render(char, True, color) for color in char_colors}
            prerendered_chars.update(prerendered_char)
        return prerendered_chars

    
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
                        color = 255 if 240 < color < 250 else color
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


if __name__ == '__main__':
    try:
        app = MatrixVision()
        app.run()
    except:
        error_popup()
    

