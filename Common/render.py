from PIL import Image, ImageDraw
from typing import Dict
import sys

from Q.Common.Board.pos import Pos
from Q.Common.Board.tile import Tile


class Render:
    def __init__(self, tiles: Dict[Pos, Tile], length: float = 64):
        self.side_length: float = length
        # where the current tile x-position starts
        self.x_px: float = 0
        self.y_px: float = 0
        # first value represents width in px, second value represents height in px
        self.render_map = {
            "star": self.render_star,
            "8star": self.render_8star,
            "square": self.render_square,
            "circle": self.render_circle,
            "diamond": self.render_diamond,
            "clover": self.render_clover
        }
        self.min_x = sys.maxsize
        self.min_y = sys.maxsize
        self.max_x = -sys.maxsize
        self.max_y = -sys.maxsize

        self.set_min_max_values(tiles)
        self.im: Image = Image.new('RGBA', self.get_dimensions_length(), (255, 255, 255, 0))
        self.draw: ImageDraw = ImageDraw.Draw(self.im)

        self.run(tiles)

    # gets the dimensions of the board.
    def set_min_max_values(self, tiles: Dict[Pos, Tile]):
        for pos in tiles.keys():
            self.min_x = min(self.min_x, pos.x)
            self.min_y = min(self.min_y, pos.y)
            self.max_x = max(self.max_x, pos.x)
            self.max_y = max(self.max_y, pos.y)

    # returns a tuple of width and height
    def get_dimensions_length(self) -> tuple:
        x = (-self.min_x + self.max_x) * self.side_length + self.side_length
        y = (-self.min_y + self.max_y) * self.side_length + self.side_length
        return x, y

    # draws each shape beside each other with their respective colors
    def run(self, tiles: Dict[Pos, Tile]):
        for pos, tile in tiles.items():
            shape: str = tile.shape.get_name()
            color: str = tile.color.get_name()
            self.x_px = (-self.min_x * self.side_length) + (self.side_length * pos.x)
            self.y_px = (-self.min_y * self.side_length) + (self.side_length * pos.y)
            self.render_map[shape](color)

    # return the horizontal midpoint of the current tile
    def get_center_x(self) -> float:
        return self.x_px + (0.5 * self.side_length)

    # draws a 4-point star using the ImageDraw
    def render_star(self, color):
        self.draw.polygon([
            (self.x_px, self.y_px,),  # bot left
            (self.x_px + 0.25 * self.side_length, self.y_px + 0.5 * self.side_length),  # middle left
            (self.x_px, self.y_px + self.side_length),  # top left
            (self.get_center_x(), self.y_px + 0.75 * self.side_length),  # top middle
            (self.x_px + self.side_length, self.y_px + self.side_length),  # top right
            (self.x_px + 0.75 * self.side_length, self.y_px + 0.5 * self.side_length),  # middle right
            (self.x_px + self.side_length, self.y_px),  # bot right
            (self.get_center_x(), self.y_px + 0.25 * self.side_length),  # bot middle
        ], fill=color)

    # draws a square using the ImageDraw
    def render_square(self, color):
        self.draw.rectangle([
            (self.x_px, self.y_px),
            (self.x_px + self.side_length, self.y_px + self.side_length)
        ], fill=color)

    # draws an 8-point using the ImageDraw
    def render_8star(self, color):
        self.__smaller_star(color)
        self.__cross_star(color)

    def __smaller_star(self, color):
        delta = lambda x: x * self.side_length / (2 * (2 ** 0.5))
        center_y = 0.5 * self.side_length
        self.draw.polygon([
            # smaller 4 star
            (self.get_center_x() - delta(1), self.y_px + center_y - delta(1)),  # bot left
            (self.get_center_x() - delta(0.5), self.y_px + center_y),  # middle left
            (self.get_center_x() - delta(1), self.y_px + center_y + delta(1)),  # top left
            (self.get_center_x(), self.y_px + center_y + delta(0.5)),  # top middle
            (self.get_center_x() + delta(1), self.y_px + center_y + delta(1)),  # top right
            (self.get_center_x() + delta(0.5), self.y_px + center_y),  # middle right
            (self.get_center_x() + delta(1), self.y_px + center_y - delta(1)),  # bot right
            (self.get_center_x(), self.y_px + center_y - delta(0.5)),  # bot middle
        ], fill=color)

    def __cross_star(self, color):
        delta = lambda x: x * self.side_length / (2 * (2 ** 0.5))
        center_y = 0.5 * self.side_length
        ratio = 1 / 3
        self.draw.polygon([
            # cross star
            (self.get_center_x(), self.y_px),  # bot
            (self.get_center_x() + delta(ratio), self.y_px + center_y - delta(ratio)),  # bot right
            (self.x_px + self.side_length, self.y_px + center_y),  # right
            (self.get_center_x() + delta(ratio), self.y_px + center_y + delta(ratio)),  # top right
            (self.get_center_x(), self.y_px + self.side_length),  # top
            (self.get_center_x() - delta(ratio), self.y_px + center_y + delta(ratio)),  # top left
            (self.x_px, self.y_px + center_y),  # left
            (self.get_center_x() - delta(ratio), self.y_px + center_y - delta(ratio)),  # bot left
        ], fill=color)

    # draws a diamond using the ImageDraw
    def render_diamond(self, color):
        self.draw.polygon([
            (self.x_px, self.y_px + 0.5 * self.side_length),  # left
            (self.get_center_x(), self.y_px),  # bottom
            (self.x_px + self.side_length, self.y_px + 0.5 * self.side_length),  # right
            (self.get_center_x(), self.y_px + self.side_length)  # top
        ], fill=color)

    # draws a circle using the ImageDraw
    def render_circle(self, color):
        self.draw.ellipse([
            (self.x_px, self.y_px),
            (self.x_px + self.side_length, self.y_px + self.side_length)
        ], fill=color)

    # draws a circle using the ImageDraw
    def render_clover(self, color):
        self.__draw_circle(self.x_px + self.side_length * 0.75, self.y_px + 0.5 * self.side_length,
                           color)  # right circle
        self.__draw_circle(self.x_px + self.side_length * 0.25, self.y_px + 0.5 * self.side_length,
                           color)  # left circle
        self.__draw_circle(self.x_px + 0.5 * self.side_length, self.y_px + self.side_length * 0.75, color)  # top circle
        self.__draw_circle(self.x_px + 0.5 * self.side_length, self.y_px + self.side_length * 0.25,
                           color)  # bottom circle

    # draws a circle at the given center_x and given center_y
    def __draw_circle(self, center_x, center_y, color):
        left = center_x - (self.side_length // 4)
        top = center_y + (self.side_length // 4)
        right = center_x + (self.side_length // 4)
        bottom = center_y - (self.side_length // 4)
        self.draw.ellipse([left, bottom, right, top], fill=color)

    # saves the current Image as the given png name
    def save(self, name: str):
        self.im.save(name)

    def show(self):
        self.im.show()

    def get_im(self) -> Image:
        return self.im
