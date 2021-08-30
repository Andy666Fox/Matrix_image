# import libraries
import pygame as pg
import numpy as np
import random
import time




image_path = input('Enter path to the image: ')

# main class for image MATRIXOFICATION ))
class Matrix:
    def __init__(self, app, font_size=6):
        
        self.app = app
        self.FONT_SIZE = font_size
        self.SIZE = self.ROWS, self.COLS = app.HEIGHT // font_size, app.WIDTH // font_size
        self.katakana = np.array([random.choice([0,2]) for i in range(100)] + ['' for i in range(1)])
        self.font = pg.font.SysFont('Arial', font_size, bold=True)

        self.matrix = np.random.choice(self.katakana, self.SIZE)
        self.char_intervals = np.random.randint(25, 50, size=self.SIZE)
        self.cols_speed = np.random.randint(100, 250, size=self.SIZE)
        self.prerendered_chars = self.get_prerendered_chars()

        # Change path to image here
        # TODO  Make image change more easier
        self.image = self.get_image(image_path)

    def get_image(self, path_to_file):
        image = pg.image.load(path_to_file)
        image = pg.transform.scale(image, self.app.RES)
        pixel_array = pg.pixelarray.PixelArray(image)
        return pixel_array

    # We need to pre-render some shars for optimization
    # TODO Get more optimize this block
    def get_prerendered_chars(self):
        char_colors = [(0, green, 0) for green in range(256)]
        prerendered_chars = {}
        for char in self.katakana:
            prerendered_char = {(char, color): self.font.render(char, True, color) for color in char_colors}
            prerendered_chars.update(prerendered_char)
        return prerendered_chars

    
    def run(self):
        frames = pg.time.get_ticks()
        self.change_chars(frames)
        self.shift_column(frames)
        self.draw()

    
    def shift_column(self, frames):
        num_cols = np.argwhere(frames % self.cols_speed == 0)
        num_cols = num_cols[:, 1]
        num_cols = np.unique(num_cols)
        self.matrix[:, num_cols] = np.roll(self.matrix[:, num_cols], shift=1, axis=0)

    
    def change_chars(self, frames):
        mask = np.argwhere(frames % self.char_intervals == 0)
        new_chars = np.random.choice(self.katakana, mask.shape[0])
        self.matrix[mask[:, 0], mask[:, 1]] = new_chars

    
    def draw(self):
        for y, row in enumerate(self.matrix):
            for x, char in enumerate(row):
                if char:
                    pos = x * self.FONT_SIZE, y * self.FONT_SIZE
                    _, red, green, blue = pg.Color(self.image[pos])
                    if red and green and blue:
                        color = (red + green + blue) // 3
                        color = 255 if 248 < color < 250 else color
                        char = self.prerendered_chars[(char, (0, color, 0))]
                        char.set_alpha(color)
                        self.app.surface.blit(char, pos)

class MatrixVision:
    def __init__(self):
        self.RES = self.WIDTH, self.HEIGHT = 704, 910
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
            self.clock.tick(200)

if __name__ == '__main__':
    app = MatrixVision()
    app.run()

