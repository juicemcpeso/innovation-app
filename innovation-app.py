# App to play innovation
# Created: 2022-04-23
# Author: juicemcpeso

import random
import math


class Card:
    def __init__(self, n, c, a, t, i0, i1, i2, i3, t0, t1, t2):
        self.name = n

        # Set color to an int 0-4, alphabetically with options
        color_options = ['blue', 'green', 'purple', 'red', 'yellow']
        if c not in color_options:
            raise ValueError("Error creating Innovation Card. Color must be blue, green, purple, red, or yellow.")
        for color in color_options:
            if c == color:
                self.color = color_options.index(c)

        # Set age to an int
        if not a.isdigit() and (int(a) >= 1 or int(a) <= 10):
            raise ValueError("Error creating Innovation Card. Age must be a number between 1 and 10.")
        self.age = int(a)

        # Set effect type to an int 0-5, in specified order
        effect_type_options = ['crown', 'leaf', 'lightbulb', 'castle', 'factory', 'clock']
        if t not in effect_type_options:
            raise ValueError("Error creating Innovation Card. "
                             "Type must be crown, lead, lightbulb, castle, factory, or clock.")
        for effect_type in effect_type_options:
            if t == effect_type:
                self.effect_type = effect_type_options.index(t)

    def __repr__(self):
        return "<Card: %s>" % self.name

    def __str__(self):
        return self.name


card = Card('Agriculture', 'red', '1', 'leaf','','','','','','','')
print(card.name)
print(card.color)
print(card.effect_type)
