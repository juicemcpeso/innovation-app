# App to play innovation
# Created: 2022-04-23
# Author: juicemcpeso

import random
import math


class Card:
    """Base class for a card in a game"""

    def __init__(self, n):
        self.name = n

    def __repr__(self):
        return "<Card: %s>" % self.name

    def __str__(self):
        return self.name


class InnovationCard(Card):
    """Class of cards specific to the game Innovation"""

    def __init__(self, n, c, a, t, i0, i1, i2, i3, t0, t1, t2):
        Card.__init__(self, n)

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
                             "Effect type must be crown, lead, lightbulb, castle, factory, or clock.")
        for effect_type in effect_type_options:
            if t == effect_type:
                self.effect_type = effect_type_options.index(t)

        # Set each of the card icons to an int 0-5, matching the effect_type.
        icon_options = ['crown', 'leaf', 'lightbulb', 'castle', 'factory', 'clock', '']
        self.icon_0 = None
        self.icon_1 = None
        self.icon_2 = None
        self.icon_3 = None

        # Set icon 0 - top left
        if i0 not in icon_options:
            raise ValueError("Error creating Innovation Card. "
                             "Icon 0 type must be crown, lead, lightbulb, castle, factory, or clock.")

        for icon in icon_options:
            if i0 == icon and i0 != '':
                self.icon_0 = icon_options.index(i0)

        # Set icon 1 - bottom left
        if i1 not in icon_options:
            raise ValueError("Error creating Innovation Card. "
                             "Icon 0 type must be crown, lead, lightbulb, castle, factory, or clock.")

        for icon in icon_options:
            if i1 == icon and i1 != '':
                self.icon_1 = icon_options.index(i1)

        # Set icon 2 - bottom middle
        if i2 not in icon_options:
            raise ValueError("Error creating Innovation Card. "
                             "Icon 0 type must be crown, lead, lightbulb, castle, factory, or clock.")

        for icon in icon_options:
            if i2 == icon and i2 != '':
                self.icon_2 = icon_options.index(i2)

        # Set icon 3 - bottom right
        if i2 not in icon_options:
            raise ValueError("Error creating Innovation Card. "
                             "Icon 0 type must be crown, lead, lightbulb, castle, factory, or clock.")

        for icon in icon_options:
            if i3 == icon and i3 != '':
                self.icon_3 = icon_options.index(i3)


card = InnovationCard('Agriculture', 'red', '1', 'leaf','crown','castle','','lightbulb','','','')
print(card.name)
print(card.color)
print(card.age)
print(card.effect_type)
print(card.icon_0)
print(card.icon_1)
print(card.icon_2)
print(card.icon_3)
