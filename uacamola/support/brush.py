"""
Author: Santiago Hernandez Ramos
"""
from __future__ import print_function
import color_console as cons


class Brush():

    _COLORS_FOREGROUND = {'BLACK': cons.FOREGROUND_BLACK,
                          'BLUE': cons.FOREGROUND_BLUE,
                          'GREEN': cons.FOREGROUND_GREEN,
                          'CYAN': cons.FOREGROUND_CYAN,
                          'RED': cons.FOREGROUND_RED,
                          'MAGENTA': cons.FOREGROUND_MAGENTA,
                          'YELLOW': cons.FOREGROUND_YELLOW,
                          'GREY': cons.FOREGROUND_GREY}

    _COLORS_BACKGROUND = {'BLACK': cons.BACKGROUND_BLACK,
                          'BLUE': cons.BACKGROUND_BLUE,
                          'GREEN': cons.BACKGROUND_GREEN,
                          'CYAN': cons.BACKGROUND_CYAN,
                          'RED': cons.BACKGROUND_RED,
                          'MAGENTA': cons.BACKGROUND_MAGENTA,
                          'YELLOW': cons.BACKGROUND_YELLOW,
                          'GREY': cons.BACKGROUND_GREY}

    def __init__(self):
        self.default_colors = cons.get_text_attr()
        self.default_bg = self.default_colors & 0x0070

    def color(self, text, color=None, background=None):
        if background is None and color is not None:
            cons.set_text_attr(
                self._COLORS_FOREGROUND[color] | self.default_bg | cons.FOREGROUND_INTENSITY)
            print(text, end='')
            cons.set_text_attr(self.default_colors)
        elif background is not None and color is not None:
            cons.set_text_attr(self._COLORS_FOREGROUND[color] | self._COLORS_BACKGROUND[background]
                               | cons.FOREGROUND_INTENSITY | cons.BACKGROUND_INTENSITY)
            print(text, end='')
            cons.set_text_attr(self.default_colors)
