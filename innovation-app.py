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

        # Add in event texts
        self.effect_text_0 = t0
        self.effect_text_1 = t1
        self.effect_text_2 = t2


class Pile:
    """Base class for a collection of card objects"""

    def __init__(self, n, seed, card_list=[]):
        self.name = n
        self.seed = seed
        self.cards = []
        for card in card_list:
            self.add_card_to_bottom(card)

    def add_card_to_bottom(self, card_object):
        """Adds a card to the top of a pile"""
        if isinstance(card_object, Card):
            self.cards.append(card_object)
        else:
            raise ValueError("Could not add card " + str(card_object) + " to bottom of card pile " + str(self) + ".")

    def add_card_to_top(self, card_object):
        """Adds a card to the bottom of a pile"""
        if isinstance(card_object, Card):
            self.cards.insert(0, card_object)
        else:
            raise ValueError("Could not add card " + str(card_object) + " to top of card pile " + str(self) + ".")

    def remove_card(self, c):
        try:
            self.cards.remove(c)
        except ValueError:
            raise ValueError("Could not remove card " + str(c) + " from card pile " + str(self) + ".")

    def get_card(self, n):
        card = None
        card_list = list(filter(lambda x: x.name == n, self.cards))
        if len(card_list):
            card = card_list.pop()
        return card

    def get_pile_size(self):
        return len(self.cards)

    def get_top_card(self):
        if len(self.cards):
            card = self.cards.pop(0)
            return card

    def shuffle_pile(self):
        random.seed(self.seed)
        random.shuffle(self.cards)

    def __repr__(self):
        string = "<CardPile: %s>\n" % self.name
        for card in self.cards:
            string += "\t" + repr(card) + "\n"
        return string

    def __str__(self):
        return self.name

# TODO - Class InnovationPile(Pile) (is this needed?)


class InnovationStack(Pile):
    """Class for an innovation stack on a board"""

    def __init__(self, n, c, seed):
        Pile.__init__(self, n, seed, [])

        # Set color to an int 0-4, alphabetically with options
        color_options = ['blue', 'green', 'purple', 'red', 'yellow']
        if c not in color_options:
            raise ValueError("Error creating Innovation Card. Color must be blue, green, purple, red, or yellow.")
        for color in color_options:
            if c == color:
                self.color = color_options.index(c)

        self.splay_left = False
        self.splay_right = False
        self.splay_up = False

    def set_splay(self, splay_direction):
        """Takes splay direction as input, sets splay in that direction"""
        splay_options = ['left', 'right', 'up']
        if splay_direction not in splay_options:
            raise ValueError("Error setting splay. Splay must be left, right, or up.")

        self.cancel_splay()
        if splay_direction == 'left':
            self.splay_left = True
        elif splay_direction == 'right':
            self.splay_right = True
        elif splay_direction == 'up':
            self.splay_up = True

    def cancel_splay(self):
        """Sets all splays to false"""
        self.splay_left = False
        self.splay_right = False
        self.splay_up = False


class Player:
    """Base class for a player in a game"""

    def __init__(self, n):
        self.name = n

    def __repr__(self):
        return "<Player: %s>" % self.name

    def __str__(self):
        return self.name

# TODO - class InnovationPlayer(player)


class Game:
    """Base class for a collection of CardPile objects"""

    def __init__(self, n, d):
        self.name = n
        self.date = d
        self.piles = []
        self.players = []

    def add_pile(self, p):
        if isinstance(p, Pile):
            self.piles.append(p)
        else:
            raise ValueError("Could not add pile " + str(p) + " to card game " + str(self.name) + ".")

    def remove_pile(self, p):
        try:
            self.piles.remove(p)
        except ValueError:
            raise ValueError("Could not remove pile " + str(p) + " from card game " + str(self.name) + ".")

    def get_pile(self, n):
        pile = None
        pile_list = list(filter(lambda x: x.name == n, self.piles))
        if len(pile_list):
            pile = pile_list.pop()
        return pile

    def add_player(self, p):
        if isinstance(p, Player):
            self.players.append(p)
        else:
            raise ValueError("Could not add player " + str(p) + " to card game " + str(self.name) + ".")

    def get_player(self, player_number):
        player = None
        player_list = list(filter(lambda x: x.number == player_number, self.players))
        if len(player_list):
            player = player_list.pop()
        return player

    def __repr__(self):
        string = "<CardGame: %s on %s>" % (self.name, self.date)
        for pile in self.piles:
            string += "\t" + repr(pile) + "\n"
        return string

    def __str__(self):
        return "%s on %s" % (self.name, self.date)

# TODO - Class InnovationGame(Game)
a = InnovationCard('a', 'blue', '1', 'crown', '','','','','','','')
b = InnovationCard('b', 'blue', '1', 'leaf', '','','','','','','')
c = InnovationCard('c', 'blue', '1', 'castle', '','','','','','','')
s = Pile('test', 18, [a, b])
s.shuffle_pile()
print(s.cards)
s.add_card_to_bottom(c)
print(s.cards)
