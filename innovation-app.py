# App to play innovation
# Created: 2022-04-23
# Author: juicemcpeso

import random
import math
import copy


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

        self.dogma = []
        self.tests = []

        # Set color to an int 0-4, alphabetically with options
        color_options = ['blue', 'green', 'purple', 'red', 'yellow','']
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
        effect_type_options = ['crown', 'leaf', 'lightbulb', 'castle', 'factory', 'clock','']
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
                             "Icon 0 type must be crown, leaf, lightbulb, castle, factory, or clock.")

        for icon in icon_options:
            if i0 == icon and i0 != '':
                self.icon_0 = icon_options.index(i0)

        # Set icon 1 - bottom left
        if i1 not in icon_options:
            raise ValueError("Error creating Innovation Card. "
                             "Icon 0 type must be crown, leaf, lightbulb, castle, factory, or clock.")

        for icon in icon_options:
            if i1 == icon and i1 != '':
                self.icon_1 = icon_options.index(i1)

        # Set icon 2 - bottom middle
        if i2 not in icon_options:
            raise ValueError("Error creating Innovation Card. "
                             "Icon 0 type must be crown, leaf, lightbulb, castle, factory, or clock.")

        for icon in icon_options:
            if i2 == icon and i2 != '':
                self.icon_2 = icon_options.index(i2)

        # Set icon 3 - bottom right
        if i2 not in icon_options:
            raise ValueError("Error creating Innovation Card. "
                             "Icon 0 type must be crown, leaf, lightbulb, castle, factory, or clock.")

        for icon in icon_options:
            if i3 == icon and i3 != '':
                self.icon_3 = icon_options.index(i3)

        self.icons = [self.icon_0, self.icon_1, self.icon_2, self.icon_3]

        # Add in event texts
        self.effect_text_0 = t0
        self.effect_text_1 = t1
        self.effect_text_2 = t2

    def count_icons_on_card(self, icon_type):
        total_icons = 0
        for icon in self.icons:
            if icon == icon_type:
                total_icons += 1

        return total_icons

    def contains_icon(self, icon_type):
        contains_icon = False
        for icon in self.icons:
            if icon == icon_type:
                contains_icon = True
                break

        return contains_icon


class SpecialAchievementCard(Card):
    """Class of special achievement cards for the game Innovation"""
    def __init__(self, n, c, a):
        Card.__init__(self, n)

        self.criteria_text = c
        self.alternative_text = a

        self.current_pile = None
        self.current_position = 0


class Test:

    def __init__(self, tn, sup, act, fun, cd=None):
        self.name = 'Test: ' + tn
        self.setup = sup
        self.act = act
        self.function = fun
        self.associated_card = cd

        self.toggle = True
        self.result = False

    def activate(self):
        if self.associated_card:
            self.setup(self.associated_card.name)
        else:
            self.setup()
        self.act()
        self.result = False
        self.result = self.function()

    def __repr__(self):
        return "<%s>" % self.name

    def __str__(self):
        return self.name


class Effect:
    """Class for a card effect"""

    # [Card name, effect number, effect type (str), demand_flag]
    def __init__(self, cn, en, et, d, f):
        self.name = cn + ' Effect ' + str(en)
        self.card_name = cn
        self.function = None

        if not isinstance(en, int):
            raise ValueError("Error creating Innovation effect. Effect number must be an integer.")
        self.number = en

        # Set effect type to an int 0-5, in specified order
        effect_type_options = ['crown', 'leaf', 'lightbulb', 'castle', 'factory', 'clock']
        if et not in effect_type_options:
            raise ValueError("Error creating Innovation Effect. "
                             "Effect type must be crown, lead, lightbulb, castle, factory, or clock.")
        for effect_type in effect_type_options:
            if et == effect_type:
                self.type = effect_type_options.index(et)

        if not isinstance(d, bool):
            raise ValueError("Error creating Innovation effect. Demand must be True or False.")
        self.demand = d

        self.function = f

    def activate(self):
        self.function()

    def __repr__(self):
        return "<%s>" % self.name

    def __str__(self):
        return self.name


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

    def is_card_in_pile(self, card):
        if card in self.cards:
            return True
        else:
            return False

    def get_card_position(self, card):
        try:
            return self.cards.index(card)
        except ValueError:
            raise ValueError("Could not find index of " + str(card) + " in card pile " + str(self) + ".")

    def get_pile_size(self):
        return len(self.cards)

    def get_top_card(self):
        if len(self.cards):
            card = self.cards.pop(0)
            return card

    def get_bottom_card(self):
        if len(self.cards):
            card = self.cards.pop(-1)
            return card

    def see_top_card(self):
        if len(self.cards) > 0:
            return self.cards[0]

    def see_bottom_card(self):
        if len(self.cards) > 0:
            return self.cards[-1]

    def shuffle_pile(self):
        random.seed(self.seed)
        random.shuffle(self.cards)

    def highest_card_value(self):
        highest_value = 0
        if self.cards:
            for card in self.cards:
                if card.age > highest_value:
                    highest_value = card.age

        return highest_value

    def __repr__(self):
        string = "<CardPile: %s>\n" % self.name
        for card in self.cards:
            string += "\t" + repr(card) + "\n"
        return string

    def __str__(self):
        return self.name


class InnovationStack(Pile):
    """Class for an Innovation stack on a board"""

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
        if len(self.cards) > 1:
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

    def contains_icon(self, icon_type):
        if self.count_icons_in_stack(icon_type) > 0:
            return True
        else:
            return False

    def count_icons_in_stack(self, icon_type):
        """Gets the total number of icons of a type in a stack"""
        total_icons = 0
        pile_size = self.get_pile_size()

        # If there are no cards in the stack, return 0.
        if pile_size == 0:
            return total_icons

        # Add the icons for the top card
        card = self.cards[0]
        total_icons = card.count_icons_on_card(icon_type)

        # Add in additional icons if the stack is splayed
        if pile_size > 1:
            if self.splay_left:
                for card in self.cards[1:]:
                    if card.icon_3 == icon_type:
                        total_icons += 1
            elif self.splay_right:
                for card in self.cards[1:]:
                    if card.icon_0 == icon_type:
                        total_icons += 1
                    if card.icon_1 == icon_type:
                        total_icons += 1
            elif self.splay_up:
                for card in self.cards[1:]:
                    if card.icon_1 == icon_type:
                        total_icons += 1
                    if card.icon_2 == icon_type:
                        total_icons += 1
                    if card.icon_3 == icon_type:
                        total_icons += 1

        return total_icons

    def total_icons_in_stack(self):
        """Counts all icons in a stack and returns a list"""
        icon_list = [0, 1, 2, 3, 4, 5]
        total_icons = []

        for icon in icon_list:
            total_icons.append(self.count_icons_in_stack(icon))

        return total_icons

    def get_splay_type(self):
        if self.splay_left and not self.splay_right and not self.splay_up:
            return 'left'
        elif not self.splay_left and self.splay_right and not self.splay_up:
            return 'right'
        elif not self.splay_left and not self.splay_right and self.splay_up:
            return 'up'
        if not self.splay_left and not self.splay_right and not self.splay_up:
            return 'none'
        else:
            raise ValueError("Multiple splay types")

class Player:
    """Base class for a player in a game"""

    def __init__(self, n):
        self.name = n

    def __repr__(self):
        return "<Player: %s>" % self.name

    def __str__(self):
        return self.name


class InnovationPlayer(Player):
    """Class for a player for the game Innovation"""

    def __init__(self, n, num, ai, p_achieve, p_score, p_hand, s_blue, s_green, s_purple, s_red, s_yellow):
        Player.__init__(self, n)

        if not isinstance(num, int):
            raise ValueError("Error creating Innovation player. Player number must be an integer.")
        self.number = num

        if not isinstance(ai, bool):
            raise ValueError("Error creating Innovation player. AI flag must be True or False.")
        self.ai_flag = ai

        # Associate all the piles with the player
        self.achievement_pile = p_achieve
        self.score_pile = p_score
        self.hand = p_hand

        # Associate all the stacks with the player
        self.blue_stack = s_blue
        self.green_stack = s_green
        self.purple_stack = s_purple
        self.red_stack = s_red
        self.yellow_stack = s_yellow
        self.stacks = [self.blue_stack, self.green_stack, self.purple_stack, self.red_stack, self.yellow_stack]

        self.options = []
        self.selected_option = None

        self.table_position = 0
        self.share_order = []

        self.winner = False

    def total_icons_on_board(self):
        """Returns a list of the total icons a player has of each type"""
        total_icons = []
        icons = [0, 1, 2, 3, 4, 5]

        for icon in icons:
            total_icons.append(self.count_icons_on_board(icon))

        return total_icons

    def count_icons_on_board(self, icon_type):
        """Counts all icons of a specific type on a board"""
        total_icons = 0
        all_stacks = [self.blue_stack, self.green_stack, self.purple_stack, self.red_stack, self.yellow_stack]
        for stack in all_stacks:
            total_icons = total_icons + stack.count_icons_in_stack(icon_type)

        return total_icons

    def get_score(self):
        """Returns the total value of cards in a players score pile"""
        total_score = 0
        for card in self.score_pile.cards:
            total_score = total_score + card.age

        return total_score

    def get_colors_on_board(self):
        current_colors = []
        for stack in self.stacks:
            if stack.get_pile_size() > 0:
                current_colors.append(stack.color)
        return current_colors

    def clear_options(self):
        self.options = []

    def is_color_splayed(self, color, direction):
        if self.stacks[color].get_splay_type() == direction:
            return True
        else:
            return False

    def get_colors_splayed_a_direction(self, direction):
        splayed_stacks = []
        for stack in self.stacks:
            if stack.get_splay_type() == direction:
                splayed_stacks.append(stack.color)

        return splayed_stacks

    def get_number_colors_splayed_a_direction(self, direction):
        return len(self.get_colors_splayed_a_direction(direction))


class Action:
    def __init__(self, t, p, c=None):
        action_type_options = ['draw', 'meld', 'achieve', 'dogma']
        if t not in action_type_options:
            raise ValueError("Error creating Innovation Action. "
                             "Effect type must be draw, meld, achieve, or dogma.")
        self.type = t

        self.player = p

        self.card = c

        if self.card:
            self.name = "{p}'s action: {t} - {c}".format(p=self.player.name, t=self.type.upper(), c=self.card.name)
        else:
            self.name = "{p}'s action: {t}".format(p=self.player.name, t=self.type.upper())

    def __repr__(self):
        return "<%s>" % self.name

    def __str__(self):
        return self.name


class Option:
    def __init__(self, n, t):
        self.name = n
        self.type = t

    def __repr__(self):
        return "<%s>" % self.name

    def __str__(self):
        return self.name


class PassOption(Option):
    def __init__(self):
        Option.__init__(self, 'Pass', 'pass')


class SplayOption(Option):
    def __init__(self, n, t, c, d):
        Option.__init__(self, n, t)
        self.color = c
        self.direction = d


class Game:
    """Base class for a collection of Pile objects and players"""

    def __init__(self, n, d, se=None):
        self.name = n
        self.date = d
        self.piles = []
        self.players = []
        self.cards = []
        self.effects = []
        self.tests = []
        self.game_over = False
        self.round = 0

        # Set the random see if not specified
        if se is None:
            self.seed = self.set_random_seed()
        else:
            if isinstance(se, int) and (0 <= se <= 9999999999):
                self.seed = se
            else:
                raise ValueError("Could not create game. Seed must be int between 0 and 9,999,999,999")

    def set_random_seed(self):
        return random.randint(0, 9999999999)

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

    def get_pile_object(self, n):
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

    def get_player_object(self, player_number):
        player = None
        player_list = list(filter(lambda x: x.number == player_number, self.players))
        if len(player_list):
            player = player_list.pop()
        return player

    def add_card_to_game(self, c):
        """Adds a card object to the game's list of cards"""
        if isinstance(c, Card):
            self.cards.append(c)
        else:
            raise ValueError("Could not add card " + str(c) + " to card game " + str(self.name) + ".")

    def get_card_object(self, card_name):
        """Given a card name (string), returns the card object"""
        card = None
        card_list = list(filter(lambda x: x.name == card_name, self.cards))
        if len(card_list):
            card = card_list.pop()
        return card

    def get_cards_from_list(self, card_list):
        output_list = []
        for card_name in card_list:
            output_list.append(self.get_card_object(card_name))
        return output_list

    def add_effect_to_game(self, e):
        if isinstance(e, Effect):
            self.effects.append(e)
        else:
            raise ValueError("Could not add effect " + str(e) + " to card game " + str(self.name) + ".")

    def add_test_to_game(self, t):
        if isinstance(t, Test):
            self.tests.append(t)
        else:
            raise ValueError("Could not add effect " + str(t) + " to card game " + str(self.name) + ".")

    def __repr__(self):
        string = "<Game: %s on %s>" % (self.name, self.date)
        for pile in self.piles:
            string += "\t" + repr(pile) + "\n"
        return string

    def __str__(self):
        return "%s on %s" % (self.name, self.date)


class InnovationGame(Game):
    """Class of a game of Innovation"""

    def __init__(self, n, d, num_p, se=None, p1_n='', p1_ai=False, p2_n='', p2_ai=False, p3_n='', p3_ai=False, p4_n='', p4_ai=False):
        Game.__init__(self, n, d, se)

        # Set number of players
        if not isinstance(num_p, int) and (2 <= num_p <= 4):
            raise ValueError("Could not create game. Number of players must be int between 2 and 4")
        self.number_of_players = num_p

        possible_player_names = [p1_n, p2_n, p3_n, p4_n]
        possible_ai_players = [p1_ai, p2_ai, p3_ai, p4_ai]
        self.player_names = []
        self.ai_players = []

        self.active_player = None
        self.active_card = None
        self.turn_player = None
        self.turn_card = None

        self.ordered_players = []

        # Variables for each of the icon types
        self.crown = 0
        self.leaf = 1
        self.lightbulb = 2
        self.castle = 3
        self.factory = 4
        self.clock = 5

        # Variables for each of the colors
        self.colors = ['blue', 'green', 'purple', 'red', 'yellow']
        self.blue = 0
        self.green = 1
        self.purple = 2
        self.red = 3
        self.yellow = 4

        self.stacks = []

        # Variables for each of the directions
        self.left = 'left'
        self.right = 'right'
        self.up = 'up'

        for i in range(self.number_of_players):
            self.player_names.append(possible_player_names[i])
            self.ai_players.append(possible_ai_players[i])

        # Set number of achievements needed to win game
        if self.number_of_players == 2:
            self.achievement_goal = 6
        elif self.number_of_players == 3:
            self.achievement_goal = 5
        elif self.number_of_players == 4:
            self.achievement_goal = 4

        # Create dictionaries to find objects
        self.special_achievements = {}
        self.draw_piles = []
        self.piles_at_beginning_of_action = {}
        self.piles_at_beginning_of_effect = {}
        self.piles_at_beginning_of_no_share = {}
        self.pile_state_history = []

        # Create everything needed for the game
        self.verbose = True
        self.testing = False

        # Play a game (Play Ball!)
        self.create_game()
        # self.set_up_game()
        # self.play_game()

    def create_game(self):
        self.create_piles()
        self.create_cards()
        self.create_achievements()
        self.create_special_achievements()
        self.create_players()
        self.create_effects()

    def create_cards(self):
        with open('cards/card_list.csv', 'r') as handle:
            handle.readline()
            lines = handle.read().splitlines()

        for line in lines:
            card = InnovationCard(*line.split('|'))
            start_pile = self.get_pile_object(str(card.age))
            if not start_pile:
                raise ValueError("Error adding card " + str(card) + " to pile " + str(start_pile) + ".")
            start_pile.add_card_to_bottom(card)
            self.add_card_to_game(card)

    def create_achievements(self):
        for i in range(1, 10):
            card = InnovationCard("Achievement {n}".format(n=i), '', str(i), '', '', '', '', '', '', '', '')
            self.get_pile_object('achievements').add_card_to_bottom(card)
            self.add_card_to_game(card)

    def create_special_achievements(self):
        """Makes the five special achievement cards"""
        with open('cards/special_achievement_list.csv', 'r') as handle:
            handle.readline()
            lines = handle.read().splitlines()

        for line in lines:
            card = SpecialAchievementCard(*line.split('|'))
            start_pile = self.get_pile_object('special achievements')
            if not start_pile:
                raise ValueError("Error adding card " + str(card) + " to pile " + str(start_pile) + ".")
            start_pile.add_card_to_bottom(card)
            self.add_card_to_game(card)

    def create_piles(self):
        # Create the draw piles
        pile_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
        for pile in pile_list:
            draw_pile = Pile(pile, self.seed)
            self.add_pile(draw_pile)
            self.draw_piles.append(draw_pile)
            # self.draw_piles.update({int(pile): draw_pile})

        # Create achievement piles
        self.add_pile(Pile('achievements', self.seed))
        self.add_pile(Pile('special achievements', self.seed))

        # Create box, removed, and reveal piles
        self.add_pile(Pile('box', self.seed))
        self.add_pile(Pile('removed', self.seed))
        self.add_pile(Pile('reveal', self.seed))

    def create_players(self):
        self.players = []
        for i in range(self.number_of_players):
            # Create an achievement pile, score_pile, and hand for each player, add to master list
            achievement_pile = Pile((self.player_names[i] + " achievement pile"), self.seed)
            self.add_pile(achievement_pile)
            score_pile = Pile((self.player_names[i] + " score pile"), self.seed)
            self.add_pile(score_pile)
            hand = Pile((self.player_names[i] + " hand"), self.seed)
            self.add_pile(hand)

            # Create stacks of each color for each player
            b_stack = InnovationStack(self.player_names[i] + "'s blue stack", 'blue', self.seed)
            g_stack = InnovationStack(self.player_names[i] + "'s green stack", 'green', self.seed)
            p_stack = InnovationStack(self.player_names[i] + "'s purple stack", 'purple', self.seed)
            r_stack = InnovationStack(self.player_names[i] + "'s red stack", 'red', self.seed)
            y_stack = InnovationStack(self.player_names[i] + "'s yellow stack", 'yellow', self.seed)
            self.add_pile(b_stack)
            self.add_pile(g_stack)
            self.add_pile(p_stack)
            self.add_pile(r_stack)
            self.add_pile(y_stack)
            self.stacks.append(b_stack)
            self.stacks.append(g_stack)
            self.stacks.append(p_stack)
            self.stacks.append(r_stack)
            self.stacks.append(y_stack)

            player = InnovationPlayer(self.player_names[i], i, self.ai_players[i], achievement_pile, score_pile, hand, b_stack, g_stack, p_stack, r_stack, y_stack)
            self.add_player(player)

        for player in self.players:
            # Create a player's share order
            self.set_share_order(player)

    def set_up_game(self):
        """Sets up the game to be played"""
        self.shuffle_piles()
        self.remove_cards_used_as_achievements()
        self.set_action_pile_state()
        self.set_effect_pile_state()

    def remove_cards_used_as_achievements(self):
        for i in range(1, 10):
            card = self.get_pile_object(str(i)).get_top_card()
            self.get_pile_object('removed').add_card_to_bottom(card)

    def shuffle_piles(self):
        for pile in self.draw_piles:
            pile.shuffle_pile()

    def starting_play(self):
        """Give everybody two cards, AI evaluates which one to play. Save the selection. Once all picked, execute"""
        # Each player and their selected starting melds
        starting_actions = []
        starting_melds = []
        # Give each player two cards
        for player in self.players:
            self.active_player = player
            self.turn_player = player
            self.draw_to_hand(1)
            self.draw_to_hand(1)

            # Create a list of the possible actions (meld either of the cards)
            action_options = []
            for card in player.hand.cards:
                meld_action = Action('meld', player, card)
                action_options.append(meld_action)

            # Select one of the cards to meld
            selected_action = self.select_action(action_options)

            # Add the player and their selected card to meld to the list of all the melds.
            starting_actions.append(selected_action)

        # Once everybody has selected their action, meld them all
        for action in starting_actions:
            self.turn_player = action.player
            self.execute_action(action)

        # Determine who has the first card alphabetically and set each player's turn position
        alphabetical_order = sorted(starting_actions, key=lambda x: x.card.name)
        self.set_table_positions(alphabetical_order[0].player)

    def set_table_positions(self, first_player):
        """Given the first player, sets the table positions for each player"""
        position = 0
        first_player.table_position = position
        self.ordered_players.append(first_player)

        start_index = first_player.number
        index = start_index + 1
        position += 1
        while index != start_index:
            if index > self.number_of_players - 1:
                index = 0
                if index == start_index:
                    break
            self.get_player_object(index).table_position = position
            self.ordered_players.append(self.get_player_object(index))
            position += 1
            index += 1

    def set_share_order(self, player):
        """Based off a player's number and table position, create a list of the order they share cards in. Could do this
        each time a dogma is shared, figured it would be quicker if it was created once."""
        share_order = []
        start_index = player.number
        index = start_index
        while True:
            index += 1
            if index > self.number_of_players - 1:
                index = 0
            if index == start_index:
                share_order.append(self.get_player_object(index))
                break
            share_order.append(self.get_player_object(index))
        player.share_order = share_order

    def play_first_round(self):
        """Round structure for the first round where players sometimes get fewer actions"""
        self.round += 1

        for player in self.ordered_players:
            self.turn_player = player
            self.print_for_testing("---\nRound {r} - {n}'s Turn".format(r=self.round, n=player.name))

            if self.number_of_players < 4 and player.table_position == 0:
                self.print_for_testing("{n}'s first action:".format(n=player.name))
                self.take_action()
            elif self.number_of_players == 4 and (player.table_position == 0 or player.table_position == 1):
                self.print_for_testing("{n}'s first action:".format(n=player.name))
                self.take_action()
            else:
                self.print_for_testing("{n}'s first action:".format(n=player.name))
                self.take_action()

                self.print_for_testing("\n{n}'s second action:".format(n=player.name))
                self.take_action()

    def play_round(self):
        """Normal round of Innovation where everybody gets two actions"""
        self.round += 1
        for player in self.ordered_players:
            self.turn_player = player
            self.print_for_testing("---\nRound {r} - {n}'s Turn\n{n}'s first action:".format(r=self.round,
                                                                                             n=player.name))
            self.take_action()

            self.print_for_testing("\n{n}'s second action:".format(n=player.name))
            self.take_action()

    def play_game(self):
        """Play a game of Innovation"""
        self.starting_play()
        self.play_first_round()

        # All other rounds
        while not self.game_over:
            self.play_round()

    # Game end functions
    def game_end(self):
        self.game_over = True
        print('Game over')
        # TODO - write code to evaluate scores
        if not self.testing:
            quit()

    def check_game_end_ai(self):
        top_cards = self.get_all_top_cards()
        if (self.get_card_object('Robotics') in top_cards) and (self.get_card_object('Software') in top_cards):
            lowest_players = self.get_players_with_lowest_score()
            if len(lowest_players) == 1:
                lowest_players[0].winner = True
                self.game_end()

    def check_game_end_achievements(self):
        """Runs when a card is added to an achievement pile. Checks to see if anybody has met goal."""
        for player in self.players:
            self.print_for_testing('{p} has {a} achievements'.format(p=player.name,
                                                                     a=player.achievement_pile.get_pile_size()))
            if player.achievement_pile.get_pile_size() >= self.achievement_goal:
                player.winner = True
                self.game_end()

    def get_players_with_lowest_score(self):
        scores = []
        lowest_players = []
        for player in self.players:
            scores.append(player.get_score())
        lowest_score = min(scores)

        for player in self.players:
            if player.get_score() == lowest_score:
                lowest_players.append(player)

        return lowest_players

    def get_players_with_highest_score(self):
        scores = []
        highest_players = []
        for player in self.players:
            scores.append(player.get_score())
        highest_score = max(scores)

        for player in self.players:
            if player.get_score() == highest_score:
                highest_players.append(player)

        return highest_players

    # Save game state
    def get_pile_state(self):
        pile_state = {}
        check_added_cards = []
        for pile in self.piles:
            card_list = []
            for card in pile.cards:
                if card in check_added_cards:
                    raise ValueError("Duplicate card. Card {c} is already in pile {p}".format(c=card.name, p=pile.name))
                card_list.append(card.name)
                check_added_cards.append(card)
            pile_state.update({pile.name: card_list})

        return pile_state

    def update_pile_state_history(self, pile_state):
        self.pile_state_history.append(pile_state)

    def set_action_pile_state(self):
        current_state = self.get_pile_state()
        self.piles_at_beginning_of_action = current_state
        self.update_pile_state_history(current_state)

    def set_effect_pile_state(self):
        current_state = self.get_pile_state()
        self.piles_at_beginning_of_effect = current_state
        self.update_pile_state_history(current_state)

    def set_no_share_pile_state(self):
        current_state = self.get_pile_state()
        self.piles_at_beginning_of_no_share = current_state
        self.update_pile_state_history(current_state)

    def set_card_location_from_dictionary(self, card_dict):
        for card_info, pile_info in card_dict.items():
            self.get_card_object(card_info).current_pile = self.get_pile_object(pile_info[0])
            self.get_card_object(card_info).current_position = int(pile_info[1])

    def return_cards_to_piles(self):
        for card in self.cards:
            self.move_card_to_pile(card, card.current_pile)

    def sort_cards_in_piles(self):
        for pile in self.piles:
            pile.cards = sorted(pile.cards, key=lambda x: x.current_position)

    # Base functions
    def base_draw(self, draw_value):
        """Base function to draw a card of a specified value"""
        if draw_value == 0:
            draw_value = 1
        for value in range(draw_value, 11):
            pile = self.get_pile_object(str(value))
            if pile.get_pile_size() > 0:
                card = pile.get_top_card()
                self.active_card = card
                return card

        self.game_end()

    def base_meld(self, card):
        """Base function to meld a card"""
        self.active_player.stacks[card.color].add_card_to_top(card)

    def base_return(self, card):
        """Base function to return a card"""
        self.get_pile_object(str(card.age)).add_card_to_bottom(card)

    def base_score(self, card):
        """Base function to score a card"""
        self.active_player.score_pile.add_card_to_bottom(card)

    def base_tuck(self, card):
        """Base function to tuck a card in a stack"""
        self.active_player.stacks[card.color].add_card_to_bottom(card)

    # Base functions to move cards around
    def transfer_card(self, card, to_location, from_location):
        """Base function to move a card from one pile to another. Do not use for stacks, use meld/tuck instead."""
        from_location.remove_card(card)
        to_location.add_card_to_top(card)

    def find_and_remove_card(self, card):
        """Finds pile where card is located and removes it from that pile"""
        for pile in self.piles:
            for c in pile.cards:
                if c == card:
                    pile.remove_card(c)

    def find_card(self, card):
        for pile in self.piles:
            for c in pile.cards:
                if c == card:
                    return pile

    def move_card_to_pile(self, card, pile):
        self.find_and_remove_card(card)
        pile.add_card_to_bottom(card)

    # Combination functions used as card actions
    def add_card_to_achievement_pile(self):
        """Moves selected card to a player's achievement pile"""
        self.find_and_remove_card(self.active_card)
        self.active_player.achievement_pile.add_card_to_bottom(self.active_card)
        self.print_for_testing('{p} claims achievement: {c}'.format(p=self.active_player, c=self.active_card.name))
        self.check_game_end_achievements()

    def claim_special_achievement(self, achievement_name):
        card = g.get_card_object(achievement_name)
        if card in self.get_pile_object('special achievements').cards:
            self.find_and_remove_card(card)
            self.active_player.achievement_pile.add_card_to_bottom(card)
            self.print_for_testing('{p} claims special achievement: {c}'.format(p=self.active_player, c=card.name))
            self.check_game_end_achievements()
        else:
            self.print_for_testing('Special achievement {c} already claimed'.format(c=card.name))

    def add_card_to_hand(self):
        """Moves selected card to active player's hand"""
        self.find_and_remove_card(self.active_card)
        self.active_player.hand.add_card_to_bottom(self.active_card)
        self.print_for_testing('{p} adds {c} to hand'.format(p=self.active_player, c=self.active_card.name))

    def add_card_to_score_pile(self):
        """Moves selected card to the score pile"""
        self.find_and_remove_card(self.active_card)
        self.base_score(self.active_card)
        self.print_for_testing('{p} adds {c} to score pile'.format(p=self.active_player, c=self.active_card.name))

    def draw_to_hand(self, draw_value):
        """Draws a card to a players hand of a specified draw value"""
        self.base_draw(draw_value)
        self.print_for_testing('{p} draws {c}'.format(p=self.active_player, c=self.active_card.name))
        self.add_card_to_hand()

    def draw_to_hand_multiple(self, draw_value, number_of_cards):
        for i in range(number_of_cards):
            self.draw_to_hand(draw_value)
            i = i + 1

    def draw_and_meld(self, draw_value):
        self.base_draw(draw_value)
        self.find_and_remove_card(self.active_card)
        self.base_meld(self.active_card)
        self.print_for_testing('{p} draws and melds {c}'.format(p=self.active_player, c=self.active_card.name))

    def draw_and_reveal(self, draw_value):
        self.base_draw(draw_value)
        # TODO - update to inform card counting module, remove printing
        self.print_for_testing('{p} draws and reveals {c}'.format(p=self.active_player, c=self.active_card.name))

    def draw_and_score(self, draw_value):
        self.base_draw(draw_value)
        self.print_for_testing('{p} draws and scores an age {c} card'.format(p=self.active_player, c=self.active_card.age))
        self.add_card_to_score_pile()

    def draw_and_tuck(self, draw_value):
        self.base_draw(draw_value)
        self.find_and_remove_card(self.active_card)
        self.base_tuck(self.active_card)
        # TODO - update to inform card counting module
        self.print_for_testing('{p} draws and tucks {c}'.format(p=self.active_player, c=self.active_card.name))

    def return_card(self):
        self.find_and_remove_card(self.active_card)
        self.base_return(self.active_card)
        self.print_for_testing('{p} returns {c}'.format(p=self.active_player.name, c=self.active_card.name))

    def score_cards(self, card_list):
        for card in card_list:
            self.find_and_remove_card(card)
            self.base_score(card)
            self.print_for_testing('{p} scores {c}'.format(p=self.active_player.name, c=card.name))

    def meld_card(self):
        self.find_and_remove_card(self.active_card)
        self.base_meld(self.active_card)
        self.print_for_testing('{p} melds {c}'.format(p=self.active_player.name, c=self.active_card.name))

    def tuck_card(self):
        self.find_and_remove_card(self.active_card)
        self.base_tuck(self.active_card)
        self.print_for_testing('{p} tucks {c}'.format(p=self.active_player.name, c=self.active_card.name))

    # Actions
    def action_draw(self):
        self.draw_to_hand(1)

    def action_meld(self):
        self.active_card = self.turn_card
        self.meld_card()

    def action_achieve(self):
        self.active_card = self.turn_card
        self.add_card_to_achievement_pile()

    def eligible_achievements(self, player):
        """Returns list of achievements that can be taken by the player"""
        score = player.get_score()
        highest_melded = 0
        eligible_achievements = []
        for stack in player.stacks:
            if stack.cards:
                if stack.cards[0].age > highest_melded:
                    highest_melded = stack.cards[0].age

        for achievement in self.get_pile_object('achievements').cards:
            if highest_melded >= achievement.age and (score >= (achievement.age * 5)):
                eligible_achievements.append(achievement)

        return eligible_achievements

    def action_dogma(self):
        """Function to execute the dogma effects"""
        sharing_players = self.determine_who_can_share()
        self.execute_dogma(sharing_players)

    def execute_dogma(self, sharing_players):
        dogma_was_shared = False
        self.set_action_pile_state()
        for effect in self.turn_card.dogma:
            if effect.demand:
                # Demand effects
                for eligible_player in self.turn_player.share_order:
                    if eligible_player not in sharing_players:
                        self.set_effect_pile_state()
                        self.active_player = eligible_player
                        self.print_for_testing('{t} DEMANDS {p} resolve {c} dogma'.format(t=self.turn_player,
                                                                                          p=eligible_player.name,
                                                                                          c=self.turn_card.name))
                        effect.activate()

            else:
                # Standard effects
                for eligible_player in sharing_players:
                    self.set_effect_pile_state()
                    self.active_player = eligible_player
                    self.print_for_testing('{p} resolves {c} dogma'.format(p=eligible_player.name, c=self.turn_card.name))
                    effect.activate()

                    # Only run sharing code if it's not the turn player and nobody has shared yet.
                    if eligible_player != self.turn_player and not dogma_was_shared:
                        dogma_was_shared = self.check_if_opponent_shared()

        if dogma_was_shared:
            self.print_for_testing('{p} draws a card due to other players sharing effect'.format(p=self.turn_player))
            self.action_draw()

    def execute_dogma_for_yourself(self):
        self.set_no_share_pile_state()
        for effect in self.active_card.dogma:
            if not effect.demand:
                self.print_for_testing('{p} resolves {c} dogma'.format(p=self.active_player.name, c=self.active_card.name))
                effect.activate()

    def determine_who_can_share(self):
        """Function to see who can share in an effect"""
        sharing_players = []
        for opponent in self.turn_player.share_order:
            if opponent == self.turn_player:
                sharing_players.append(self.turn_player)
            elif opponent.count_icons_on_board(self.turn_card.effect_type) >= self.turn_player.count_icons_on_board(self.turn_card.effect_type):
                sharing_players.append(opponent)

        return sharing_players

    def check_if_opponent_shared(self):
        original_state = self.piles_at_beginning_of_effect
        current_state = self.get_pile_state()
        if original_state != current_state:
            return True
        else:
            return False

    def draw_if_opponents_shared(self, list_of_players):
        non_demand_effects = False
        for effect in self.active_card.dogma:
            if not effect.demand:
                non_demand_effects = True
        if len(list_of_players) > 1 and non_demand_effects:
            # TODO - update this to make sure something in the game state changes
            self.print_for_testing('{p} draws a card due to other players sharing effect'.format(p=self.turn_player))
            self.action_draw()

    # Functions to select and simulate actions
    def take_action(self):
        """Function to take an action"""
        self.set_action_pile_state()
        self.set_effect_pile_state()
        self.active_player = self.turn_player
        available_actions = self.available_actions()
        selected_action = self.select_action(available_actions)
        self.execute_action(selected_action)

    def available_actions(self):
        draw_action = Action('draw', self.turn_player, None)
        options = [draw_action]

        # Check to see if a player is eligible to claim any achievements, add them to the available options
        eligible_achievements = self.eligible_achievements(self.turn_player)
        if len(eligible_achievements) > 0:
            for achievement in eligible_achievements:
                achievement_action = Action('achieve', self.turn_player, achievement)
                options.append(achievement_action)

        # Check to see if the player has any cards in hand, add the ability to meld them to the available options
        if self.turn_player.hand.cards:
            for card in self.turn_player.hand.cards:
                meld_action = Action('meld', self.turn_player, card)
                options.append(meld_action)

        # Check to see if the player has any dogma effects that can be activated
        for stack in self.turn_player.stacks:
            if stack.cards:
                dogma_action = Action('dogma', self.turn_player, stack.see_top_card())
                options.append(dogma_action)

        return options

    def select_action(self, action_list):
        """Function that takes a list of possible actions and selects which one to execute. Human code will select
        based off input, AI via algorithm."""
        if self.turn_player.ai_flag:
            # TODO - write function for AI to select an action
            selected_action = self.ai_select_action_random_always_achieve(action_list)
        else:
            # TODO - write function for a human to select an action
            pass

        self.print_for_testing(selected_action.name)

        return selected_action

    def execute_action(self, action):
        """Function that takes an action pair ['action', card]"""
        self.active_card = action.card
        self.turn_card = action.card
        self.active_player = self.turn_player

        if action.type == 'draw':
            self.action_draw()
        elif action.type == 'meld':
            self.action_meld()
        elif action.type == 'achieve':
            self.action_achieve()
        elif action.type == 'dogma':
            self.action_dogma()

    # AIs
    def ai_select_action_random(self, action_list):
        """Baseline AI to determine which action to select by random selection"""
        index = random.randrange(len(action_list))
        return action_list[index]

    def ai_select_action_random_always_achieve(self, action_list):
        """If this AI can select an achievement it does, otherwise it picks randomly.
        If it can pick multiple, it picks the lowest available achievement."""
        selection = None

        i = 0
        for option in action_list:
            if option.type == 'achieve':
                selection = i
                break
            i += 1

        if not selection:
            selection = random.randrange(len(action_list))

        return action_list[selection]

    def ai_select_random_option(self):
        index = random.randrange(len(self.active_player.options))
        return self.active_player.options[index]

    # Options
    def take_option(self):
        self.select_option()
        self.execute_option()

    def select_option(self):
        self.active_player.selected_option = None
        if self.active_player.ai_flag:
            # TODO - write function for AI to select an action
            self.active_player.selected_option = self.ai_select_random_option()
        else:
            # TODO - write function for a human to select an action
            pass

    def execute_option(self):
        if self.active_player.selected_option.type == 'splay':
            self.execute_option_splay()

        self.print_for_testing("{p} chooses to {s}".format(p=self.active_player.name,
                                                           s=self.active_player.selected_option.name.lower()))

    def execute_option_splay(self):
        selected_option = self.active_player.selected_option
        self.active_player.stacks[selected_option.color].set_splay(selected_option.direction)

    # Create options
    def create_pass_option(self):
        self.active_player.options.append(PassOption())

    def create_splay_option(self, splay_color, splay_direction):
        name = "Splay {c} cards {d}".format(c=self.colors[splay_color], d=splay_direction)
        self.active_player.options.append(SplayOption(name, 'splay', splay_color, splay_direction))

    # Effects
    def create_effects(self):
        # [Card name, effect number, effect type (str), demand_flag, function]
        effects_list = [['Metalworking', 0, 'castle', False, self.metalworking_effect_0],           # Age 1
                        ['Mysticism', 0, 'castle', False, self.mysticism_effect_0],
                        ['Sailing', 0, 'crown', False, self.sailing_effect_0],
                        ['The Wheel', 0, 'castle', False, self.the_wheel_effect_0],
                        ['Writing', 0, 'lightbulb', False, self.writing_effect_0],
                        ['Calendar', 0, 'leaf', False, self.calendar_effect_0],                     # Age 2
                        ['Fermenting', 0, 'leaf', False, self.fermenting_effect_0],
                        ['Paper', 0, 'lightbulb', False, self.paper_effect_0],                      # Age 3
                        ['Paper', 0, 'lightbulb', False, self.paper_effect_1],
                        ['Colonialism', 0, 'factory', False, self.colonialism_effect_0],            # Age 4
                        ['Experimentation', 0, 'lightbulb', False, self.experimentation_effect_0],
                        ['Astronomy', 0, 'lightbulb', False, self.astronomy_effect_0],              # Age 5
                        ['Astronomy', 1, 'lightbulb', False, self.astronomy_effect_1],
                        ['Steam Engine', 0, 'factory', False, self.steam_engine_effect_0],
                        ['Atomic Theory', 0, 'lightbulb', False, self.atomic_theory_effect_0],      # Age 6
                        ['Atomic Theory', 1, 'lightbulb', False, self.atomic_theory_effect_1],
                        ['Machine Tools', 0, 'factory', False, self.machine_tools_effect_0],
                        ['Electricity', 0, 'factory', False, self.electricity_effect_0],            # Age 7
                        ['Genetics', 0, 'lightbulb', False, self.genetics_effect_0],                # Age 9
                        ['A.I.', 0, 'lightbulb', False, self.ai_effect_0],                          # Age 10
                        ['A.I.', 1, 'lightbulb', False, self.ai_effect_1],
                        ['Robotics', 0, 'factory', False, self.robotics_effect_0],
                        ['Software', 0, 'clock', False, self.software_effect_0],
                        ['Software', 1, 'clock', False, self.software_effect_1]]

        for effect_to_add in effects_list:
            effect = Effect(effect_to_add[0], effect_to_add[1], effect_to_add[2], effect_to_add[3], effect_to_add[4])
            self.add_effect_to_game(effect)
            associated_card = self.get_card_object(effect.card_name)
            associated_card.dogma.append(effect)

    # Supporting effects functions
    def get_all_top_cards(self):
        top_cards = []
        for stack in self.stacks:
            if stack.cards:
                top_cards.append(stack.see_top_card())

        return top_cards

    # Age 1 Effects
    def metalworking_effect_0(self):
        while True:
            self.draw_and_reveal(1)
            if self.active_card.contains_icon(self.castle):
                self.add_card_to_score_pile()
            else:
                self.add_card_to_hand()
                break

    def mysticism_effect_0(self):
        self.draw_and_reveal(1)

        if self.active_card.color in self.active_player.get_colors_on_board():
            self.meld_card()
            self.draw_to_hand(1)
        else:
            self.add_card_to_hand()

    def sailing_effect_0(self):
        self.draw_and_meld(1)

    def the_wheel_effect_0(self):
        self.draw_to_hand(1)
        self.draw_to_hand(1)

    def writing_effect_0(self):
        self.draw_to_hand(2)

    # Age 2 effects
    def calendar_effect_0(self):
        if self.active_player.score_pile.get_pile_size() > self.active_player.hand.get_pile_size():
            self.draw_to_hand(3)
            self.draw_to_hand(3)

    def fermenting_effect_0(self):
        stacks_with_leaves = 0
        for stack in self.active_player.stacks:
            if stack.contains_icon(self.leaf):
                stacks_with_leaves += 1

        i = 0
        while i < stacks_with_leaves:
            self.draw_to_hand(2)
            i += 1
    # Age 3 effects
    def paper_effect_0(self):
        self.active_player.clear_options()
        self.create_splay_option(self.blue, 'left')
        self.create_splay_option(self.green, 'left')
        self.create_pass_option()
        self.take_option()

    def paper_effect_1(self):
        colors_splayed_left = self.active_player.get_number_colors_splayed_a_direction(self.left)
        self.draw_to_hand_multiple(4, colors_splayed_left)

    # Age 4 effects
    def colonialism_effect_0(self):
        while True:
            self.draw_and_tuck(3)
            if not self.active_card.contains_icon(self.crown):
                break

    def experimentation_effect_0(self):
        self.draw_and_meld(5)

    # Age 5 effects
    def astronomy_effect_0(self):
        while True:
            self.draw_and_reveal(6)
            if self.active_card.color == self.green or self.active_card.color == self.blue:
                self.meld_card()
            else:
                break

    def astronomy_effect_1(self):
        do_cards_meet_criteria = []
        for stack in self.active_player.stacks:
            if stack.color != self.purple:
                if stack.cards:
                    top_card = stack.see_top_card()
                    if top_card.age >= 6:
                        do_cards_meet_criteria.append(True)
                    else:
                        do_cards_meet_criteria.append(False)
                else:
                    do_cards_meet_criteria.append(False)

        if all(do_cards_meet_criteria):
            self.claim_special_achievement('Universe')

    def steam_engine_effect_0(self):
        self.draw_and_tuck(4)
        self.draw_and_tuck(4)

        if self.active_player.yellow_stack.cards:
            self.active_card = self.active_player.yellow_stack.get_bottom_card()
            self.add_card_to_score_pile()

    # Age 6 effects
    def atomic_theory_effect_0(self):
        self.active_player.clear_options()
        self.create_splay_option(self.blue, 'right')
        self.create_pass_option()
        self.take_option()

    def atomic_theory_effect_1(self):
        self.draw_and_meld(7)

    def machine_tools_effect_0(self):
        highest_value = self.active_player.score_pile.highest_card_value()
        self.draw_and_score(highest_value)

    # Age 7 effects
    def electricity_effect_0(self):
        number_of_cards_returned = 0
        for stack in self.active_player.stacks:
            if stack.cards:
                card = stack.see_top_card()
                if not card.contains_icon(self.factory):
                    self.active_card = card
                    self.return_card()
                    number_of_cards_returned += 1

        i = 0
        while i < number_of_cards_returned:
            self.draw_to_hand(8)
            i += 1

    # Age 8 effects

    # Age 9 effects
    def genetics_effect_0(self):
        self.draw_and_meld(10)
        active_stack = self.active_player.stacks[self.active_card.color].cards
        if len(active_stack) > 1:
            self.score_cards(active_stack[1:])

    # Age 10 effects
    def ai_effect_0(self):
        self.draw_and_score(10)

    def ai_effect_1(self):
        self.check_game_end_ai()

    def robotics_effect_0(self):
        if self.active_player.green_stack.cards:
            self.active_card = self.active_player.green_stack.get_top_card()
            self.add_card_to_score_pile()

        self.draw_and_meld(10)

        self.execute_dogma_for_yourself()

    def software_effect_0(self):
        self.draw_and_score(10)

    def software_effect_1(self):
        self.draw_and_meld(10)
        self.draw_and_meld(10)
        self.execute_dogma_for_yourself()

    # Tests
    def print_for_testing(self, string_to_print):
        if self.verbose:
            print(string_to_print)

    def create_tests(self):
        # Test name, setup function, action function, evaluation function, corresponding card
        test_list = [['Metalworking', self.set_up_test_generic, self.test_metalworking, self.get_card_object('Metalworking')],
                     ['Mysticism', self.set_up_test_generic, self.test_mysticism, self.get_card_object('Mysticism')],
                     ['Sailing', self.set_up_test_generic, self.test_sailing, self.get_card_object('Sailing')],
                     ['The Wheel', self.test_the_wheel_setup, self.test_the_wheel, self.get_card_object('The Wheel')],
                     ['Writing', self.set_up_test_generic, self.test_writing, self.get_card_object('Writing')],
                     ['Calendar (no score cards)', self.set_up_test_generic, self.test_calendar, self.get_card_object('Calendar')],
                     ['Calendar (score cards)', self.test_calendar_setup, self.test_calendar, self.get_card_object('Calendar')],
                     ['Fermenting', self.test_fermenting_setup, self.test_fermenting, self.get_card_object('Fermenting')],
                     ['Paper', self.set_up_test_generic, self.test_paper, self.get_card_object('Paper')],
                     ['Colonialism', self.set_up_test_generic, self.test_colonialism, self.get_card_object('Colonialism')],
                     ['Experimentation', self.set_up_test_generic, self.test_experimentation, self.get_card_object('Experimentation')],
                     ['Astronomy', self.test_astronomy_setup, self.test_astronomy, self.get_card_object('Astronomy')],
                     ['Steam Engine', self.set_up_test_generic, self.test_steam_engine, self.get_card_object('Steam Engine')],
                     ['Atomic Theory', self.set_up_test_generic, self.test_atomic_theory, self.get_card_object('Atomic Theory')],
                     ['Atomic Theory (cards to splay)', self.test_atomic_theory_setup, self.test_atomic_theory, self.get_card_object('Atomic Theory')],
                     ['Machine Tools', self.test_machine_tools_setup, self.test_machine_tools, self.get_card_object('Machine Tools')],
                     ['Electricity', self.test_electricity_setup, self.test_electricity, self.get_card_object('Electricity')],
                     ['Genetics', self.test_genetics_setup, self.test_genetics, self.get_card_object('Genetics')],
                     ['A.I. (no robotics/software)', self.set_up_test_generic, self.test_ai, self.get_card_object('A.I.')],
                     ['A.I. (robotics/software, tied lowest score)', self.test_ai_setup_0, self.test_ai, self.get_card_object('A.I.')],
                     ['A.I. (robotics/software, winner)', self.test_ai_setup_1, self.test_ai, self.get_card_object('A.I.')],
                     ['Robotics', self.set_up_test_generic, self.test_robotics, self.get_card_object('Robotics')],
                     ['Software', self.set_up_test_generic, self.test_software, self.get_card_object('Software')]]

        for test_to_add in test_list:
            test = Test(test_to_add[0], test_to_add[1], self.action_dogma, test_to_add[2], test_to_add[3])
            self.add_test_to_game(test)
            associated_card = test_to_add[3]
            associated_card.tests.append(test)

    def run_all_tests(self):
        passed_tests = []
        failed_tests = []
        self.testing = True

        for test in self.tests:
            if test.toggle:
                test.activate()
                if test.result and self.test_cards_and_piles():
                    passed_tests.append(test)
                else:
                    failed_tests.append(test)

        self.determine_pass_or_fail(failed_tests)

    def test_a_card(self, card_name):
        passed_tests = []
        failed_tests = []
        self.testing = True

        card = self.get_card_object(card_name)
        for test in card.tests:
            test.activate()
            if test.result:
                passed_tests.append(test)
            else:
                failed_tests.append(test)

        self.determine_pass_or_fail(failed_tests)

    def test_no_share_effect(self, card):
        # TODO - update to only run tests on non-DEMAND effects
        results = []
        for test in card.tests:
            test.activate()
            results.append(test.result)
        return all(results)

    def determine_pass_or_fail(self, failed_test_list):
        if failed_test_list:
            print('The following tests failed:')
            for test in failed_test_list:
                print(test.name)
        else:
            print('All tests passed')

    def test_cards_and_piles(self):
        initial_cards_in_game = self.test_convert_piles_to_card_list(self.piles_at_beginning_of_effect)
        current_cards_in_game = self.test_convert_piles_to_card_list(self.get_pile_state())
        return initial_cards_in_game == current_cards_in_game

    def test_convert_piles_to_card_list(self, pile_dict):
        cards = []
        for pile in pile_dict:
            for card in pile_dict[pile]:
                cards.append(card)

        alphabetical_sorted_cards = sorted(cards)
        return alphabetical_sorted_cards

    def set_up_test_generic(self, card_name):
        self.print_for_testing('Test: {t}'.format(t=card_name))
        self.create_game()
        self.shuffle_piles()
        self.turn_player = self.get_player_object(0)
        self.active_player = self.get_player_object(0)
        self.turn_card = self.get_card_object(card_name)
        self.active_card = self.turn_card
        self.meld_card()

    # See cards at beginning of effect
    def test_get_player_stacks_at_beginning_of_effect(self):
        player_stack_names = []
        for stack in self.active_player.stacks:
            player_stack_names.append(stack.name)

        stacks_at_beginning_of_effect = []
        for pile_name in self.piles_at_beginning_of_effect:
            if pile_name in player_stack_names:
                card_list = self.get_cards_from_list(self.piles_at_beginning_of_effect[pile_name])
                stacks_at_beginning_of_effect.append(card_list)

        return stacks_at_beginning_of_effect

    def test_get_all_stacks_at_beginning_of_effect(self):
        player_stack_names = []
        for player in self.players:
            for stack in player.stacks:
                player_stack_names.append(stack.name)

        stacks_at_beginning_of_effect = []
        for pile_name in self.piles_at_beginning_of_effect:
            if pile_name in player_stack_names:
                card_list = self.get_cards_from_list(self.piles_at_beginning_of_effect[pile_name])
                stacks_at_beginning_of_effect.append(card_list)

        return stacks_at_beginning_of_effect

    def test_see_initial_score_pile(self):
        starting_score = self.get_cards_from_list(self.piles_at_beginning_of_effect[self.active_player.score_pile.name])
        return starting_score

    def test_see_initial_hand(self):
        starting_hand = self.get_cards_from_list(self.piles_at_beginning_of_effect[self.active_player.hand.name])
        return starting_hand

    def test_get_initial_highest_cards(self, card_list):
        highest_value = self.test_get_initial_highest_card_value(card_list)
        highest_cards = []
        for card in card_list:
            if card.age == highest_value:
                highest_cards.append(card)
        return highest_cards

    def test_get_initial_highest_card_value(self, card_list):
        highest_value = 0
        for card in card_list:
            if card.age > highest_value:
                highest_value = card.age
        return highest_value

    def test_get_initial_card_pile(self, card_name):
        for pile in self.piles_at_beginning_of_effect:
            if card_name in self.piles_at_beginning_of_effect[pile]:
                return self.get_pile_object(pile)

    # Test the functions
    def test_no_changes(self):
        return self.piles_at_beginning_of_effect == self.get_pile_state()

    def test_game_over(self):
        return self.game_over

    def test_enough_cards_available_to_draw(self, draw_value, number_of_cards):
        cards_to_draw = self.test_see_all_draw_cards(draw_value)

        if len(cards_to_draw) >= number_of_cards:
            return True
        else:
            return False

    def test_enough_cards_available_to_draw_given_pile(self, pile, number_of_cards):
        if len(pile) >= number_of_cards:
            return True
        else:
            return False

    def test_see_draw_card(self, draw_value):
        i = draw_value
        if i == 0:
            i = 1

        while i <= 10:
            pile = self.piles_at_beginning_of_effect[str(i)]
            if pile:
                drawn_card = self.get_card_object(pile[0])
                return drawn_card
            i = i + 1

    def test_see_all_draw_cards(self, draw_value):
        draw_cards = []
        i = draw_value
        while i <= 10:
            pile = self.piles_at_beginning_of_effect[str(i)]
            for card in pile:
                draw_cards.append(self.get_card_object(card))
            i = i + 1
        return draw_cards

    def test_see_all_draw_cards_beginning_of_action(self, draw_value):
        draw_cards = []
        i = draw_value
        while i <= 10:
            pile = self.piles_at_beginning_of_action[str(i)]
            for card in pile:
                draw_cards.append(self.get_card_object(card))
            i = i + 1
        return draw_cards

    def test_see_next_draw_cards(self, draw_value, number_of_cards):
        cards_to_see = []
        draw_cards = self.test_see_all_draw_cards(draw_value)

        i = 0
        while i < number_of_cards:
            cards_to_see.append(draw_cards[i])
            i = i + 1

        return cards_to_see

    def test_see_next_draw_cards_given_pile(self, pile, number_of_cards):
        cards_to_see = []
        i = 0
        while i < number_of_cards:
            cards_to_see.append(pile[i])
            i = i + 1

        return cards_to_see

    def test_draw_cards(self, draw_value, number_of_cards):
        results = []

        if number_of_cards == 0:
            return True
        else:
            if self.test_enough_cards_available_to_draw(draw_value, number_of_cards):
                cards = self.test_see_next_draw_cards(draw_value, number_of_cards)

                for card in cards:
                    if self.active_player.hand.is_card_in_pile(card) \
                            and not self.get_pile_object(str(card.age)).is_card_in_pile(card):
                        results.append(True)
                    else:
                        results.append(False)

                return all(results)

            else:
                return self.test_game_over()

    def test_draw_and_meld(self, draw_value, number_of_cards):
        if self.test_enough_cards_available_to_draw(draw_value, number_of_cards):
            cards_to_draw = self.test_see_next_draw_cards(draw_value, number_of_cards)

            return self.test_meld_multiple_cards(cards_to_draw)

        else:
            return self.test_game_over()

    def test_draw_and_score(self, draw_value, number_of_cards):
        if self.test_enough_cards_available_to_draw(draw_value, number_of_cards):
            cards_to_draw = self.test_see_next_draw_cards(draw_value, number_of_cards)
            return self.test_score_multiple_cards(cards_to_draw)

        else:
            return self.test_game_over()

    def test_draw_and_score_beginning_of_action(self, draw_value, number_of_cards):
        initial_draw_pile = self.test_see_all_draw_cards_beginning_of_action(draw_value)
        if self.test_enough_cards_available_to_draw_given_pile(initial_draw_pile, number_of_cards):
            cards_to_draw = self.test_see_next_draw_cards_given_pile(initial_draw_pile, number_of_cards)
            return self.test_score_multiple_cards(cards_to_draw)

        else:
            return self.test_game_over()

    def test_draw_and_tuck(self, draw_value, number_of_cards):
        if self.test_enough_cards_available_to_draw(draw_value, number_of_cards):
            cards_to_draw = self.test_see_next_draw_cards(draw_value, number_of_cards)

            return self.test_tuck_multiple_cards(cards_to_draw)

        else:
            return self.test_game_over()

    def test_tuck_card(self, card):
        if self.active_player.stacks[card.color].see_bottom_card() == card:
            return True
        else:
            return False

    def test_tuck_multiple_cards(self, card_list):
        count_by_color = [0, 0, 0, 0, 0]
        results = []
        card_list.reverse()
        for card in card_list:
            index = -1 - count_by_color[card.color]
            if self.active_player.stacks[card.color].cards[index] == card:
                results.append(True)
            else:
                results.append(False)
            count_by_color[card.color] = count_by_color[card.color] + 1

        return all(results)

    def test_meld_card(self, card):
        return self.active_player.stacks[card.color].see_top_card() == card

    def test_meld_multiple_cards(self, card_list):
        count_by_color = [0, 0, 0, 0, 0]
        results = []
        card_list.reverse()
        for card in card_list:
            index = 0 + count_by_color[card.color]
            if self.active_player.stacks[card.color].cards[index] == card:
                results.append(True)
            else:
                results.append(False)
            count_by_color[card.color] = count_by_color[card.color] + 1

        return all(results)

    def test_return_card(self, card):
        return self.get_pile_object(str(card.age)).see_bottom_card == card

    def test_return_multiple_cards(self, card_list):
        count_by_age = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        results = []
        card_list.reverse()
        for card in card_list:
            index = -1 - count_by_age[(card.age - 1)]
            if self.get_pile_object(str(card.age)).cards[index] == card:
                results.append(True)
            else:
                results.append(False)

            count_by_age[(card.age - 1)] = count_by_age[(card.age - 1)] + 1

        return all(results)

    def test_score_card(self, card):
        return self.active_player.score_pile.is_card_in_pile(card)

    def test_score_multiple_cards(self, card_list):
        results = []
        for card in card_list:
            results.append(self.active_player.score_pile.is_card_in_pile(card))
        return all(results)

    def test_if_card_in_hand(self, card):
        return self.active_player.hand.is_card_in_pile(card)

    def test_if_multiple_cards_in_hand(self, card_list):
        results = []
        for card in card_list:
            results.append(self.active_player.hand.is_card_in_pile(card))
        return all(results)

    def test_if_cards_still_in_draw_pile(self, card_list):
        results = []
        for card in card_list:
            results.append(self.get_pile_object(str(card.age)).is_card_in_pile(card))
        return all(results)

    def test_splay(self, color, direction):
        if self.active_player.stacks[color].get_pile_size() > 1:
            if self.active_player.stacks[color].get_splay_type == direction:
                return True
            else:
                return False
        else:
            return True

    # Age 1 tests
    def test_metalworking(self):
        deck = self.test_see_all_draw_cards(1)
        cards_that_will_be_drawn = []

        for card in deck:
            cards_that_will_be_drawn.append(card)
            if not card.contains_icon(self.castle):
                break

        scored_correctly = self.test_score_multiple_cards(cards_that_will_be_drawn[:-1])
        drawn_correctly = self.active_player.hand.is_card_in_pile(cards_that_will_be_drawn[-1])

        return scored_correctly and drawn_correctly

    def test_mysticism(self):
        current_colors = []
        stacks_at_beginning = self.test_get_player_stacks_at_beginning_of_effect()
        i = 0
        for stack in stacks_at_beginning:
            if stack:
                current_colors.append(i)
            i = i + 1

        next_cards = self.test_see_next_draw_cards(1, 2)

        if next_cards[0].color in current_colors:
            return self.test_meld_card(next_cards[0]) and self.test_if_card_in_hand(next_cards[1])
        else:
            return self.test_if_card_in_hand(next_cards[0])

    def test_sailing(self):
        return self.test_draw_and_meld(1, 1)

    def test_the_wheel_setup(self, card_name):
        self.set_up_test_generic(card_name)
        self.active_player = self.get_player_object(1)
        self.active_card = self.get_card_object('Mysticism')
        self.meld_card()
        self.active_card = self.get_card_object('The Wheel')
        self.active_player = self.get_player_object(0)
        self.turn_player = self.active_player

    def test_the_wheel(self):
        return self.test_draw_cards(1, 2)

    def test_writing(self):
        return self.test_draw_cards(2, 1)

    # Age 2 tests
    def test_calendar_setup(self, card_name):
        """Condition where player has cards in score pile"""
        self.set_up_test_generic(card_name)
        self.active_player = self.get_player_object(0)
        self.active_card = self.get_card_object('A.I.')
        self.add_card_to_score_pile()
        self.active_card = self.get_card_object('Calendar')

    def test_calendar(self):
        if len(self.test_see_initial_score_pile()) > len(self.test_see_initial_hand()):
            return self.test_draw_cards(3, 2)
        else:
            return self.test_no_changes()

    def test_fermenting_setup(self, card_name):
        self.set_up_test_generic(card_name)
        self.active_card = g.get_card_object('Sailing')
        g.meld_card()
        self.active_card = g.get_card_object('Calendar')
        g.meld_card()

    def test_fermenting(self):
        # TODO - Update to compare against pre-dogma format once the player state is saved with splay information
        total_leaves = 0
        for stack in self.active_player.stacks:
            if stack.contains_icon(self.leaf):
                total_leaves = total_leaves + 1

        return self.test_draw_cards(2, total_leaves)

    # Age 3 tests
    def test_paper(self):
        return self.test_paper_0() and self.test_paper_1()

    def test_paper_0(self):
        if self.active_player.selected_option.type == 'splay':
            selected_color = self.active_player.selected_option.color
            return self.test_splay(selected_color, self.left)
        else:
            return True

    def test_paper_1(self):
        colors_splayed_left = self.active_player.get_number_colors_splayed_a_direction(self.left)
        return self.test_draw_cards(4, colors_splayed_left)

    # Age 4 tests
    def test_colonialism(self):
        all_cards = self.test_see_all_draw_cards(3)
        cards_to_be_drawn = []
        for card in all_cards:
            cards_to_be_drawn.append(card)
            if not card.contains_icon(self.crown):
                break

        return self.test_tuck_multiple_cards(cards_to_be_drawn)

    def test_experimentation(self):
        return self.test_draw_and_meld(5, 1)

    # Age 5 tests
    def test_astronomy_setup(self, card_name):
        self.set_up_test_generic(card_name)

        # Red
        self.active_card = g.get_card_object('Machine Tools')
        self.meld_card()
        # Green
        self.active_card = g.get_card_object('Bicycle')
        self.meld_card()
        # Yellow
        self.active_card = g.get_card_object('Antibiotics')
        self.meld_card()
        # Blue
        self.active_card = g.get_card_object('Atomic Theory')
        self.meld_card()

        self.turn_card = self.get_card_object('Astronomy')
        self.active_card = self.turn_card

    def test_astronomy(self):
        universe_original_pile = self.test_get_initial_card_pile('Universe')
        all_cards = self.test_see_all_draw_cards_beginning_of_action(6)
        cards_to_be_drawn = []
        for card in all_cards:
            cards_to_be_drawn.append(card)
            if card.color == self.blue or card.color == self.green:
                pass
            else:
                break

        return self.test_astronomy_0(cards_to_be_drawn[:-1]) and self.test_astronomy_1(universe_original_pile)

    def test_astronomy_0(self, card_list):
        return self.test_meld_multiple_cards(card_list)

    def test_astronomy_1(self, universe_pile):
        top_cards_are_6 = []
        universe = self.get_card_object('Universe')
        universe_original_pile = universe_pile

        for stack in self.active_player.stacks:
            if stack.color != self.purple:
                if stack.cards:
                    if stack.see_top_card().age >= 6:
                        top_cards_are_6.append(True)
                    else:
                        top_cards_are_6.append(False)
                else:
                    top_cards_are_6.append(False)

        if all(top_cards_are_6):
            if universe_original_pile == self.get_pile_object('special achievements'):
                if self.find_card(universe) == self.active_player.achievement_pile:
                    return True
                else:
                    return False
            elif universe_original_pile == self.find_card(universe):
                return True
            else:
                return False
        else:
            return universe_original_pile == self.find_card(universe)

    def test_steam_engine(self):
        yellow_stack = self.piles_at_beginning_of_effect[self.active_player.yellow_stack.name]
        bottom_yellow = self.get_card_object(yellow_stack[-1])
        yellow_cards = []

        cards = self.test_see_next_draw_cards(4, 2)
        if len(cards) == 2:
            for card in cards:
                if card.color == self.yellow:
                    cards.remove(card)
                    yellow_cards.append(card)

        if len(yellow_cards) == 1:
            bottom_yellow = yellow_cards[0]
        elif len(yellow_cards) == 2:
            bottom_yellow = yellow_cards[1]

        score_correctly = self.test_score_card(bottom_yellow)

        tuck_correctly = self.test_tuck_multiple_cards(cards)

        return score_correctly and tuck_correctly

    # Age 6 tests
    def test_atomic_theory_setup(self, card_name):
        self.set_up_test_generic(card_name)

        self.active_player = self.get_player_object(0)
        self.active_card = g.get_card_object('Calendar')
        self.meld_card()
        self.active_card = g.get_card_object('Alchemy')
        self.meld_card()
        self.active_card = g.get_card_object('Atomic Theory')
        self.meld_card()

    def test_atomic_theory(self):
        return self.test_atomic_theory_0() and self.test_atomic_theory_1()

    def test_atomic_theory_0(self):
        if self.active_player.selected_option == 'splay':
            return self.test_splay(self.blue, 'right')
        else:
            return True

    def test_atomic_theory_1(self):
        return self.test_draw_and_meld(7, 1)

    def test_machine_tools_setup(self, card_name):
        self.set_up_test_generic(card_name)
        self.active_card = self.get_card_object('Steam Engine')
        self.add_card_to_score_pile()

    def test_machine_tools(self):
        initial_score_pile = self.test_see_initial_score_pile()
        highest_card_value = self.test_get_initial_highest_card_value(initial_score_pile)

        return self.test_draw_and_score(highest_card_value, 1)

    # Age 7 tests
    def test_electricity_setup(self, card_name):
        self.set_up_test_generic(card_name)
        self.active_card = self.get_card_object('Astronomy')
        self.meld_card()
        self.active_card = self.get_card_object('Metalworking')
        self.meld_card()
        self.active_card = self.get_card_object('Machine Tools')
        self.meld_card()
        self.active_card = self.get_card_object('Experimentation')
        self.meld_card()

    def test_electricity(self):
        cards_to_return = []
        for stack in self.test_get_player_stacks_at_beginning_of_effect():
            if stack:
                card = stack[0]
                if not card.contains_icon(self.factory):
                    cards_to_return.append(card)

        if cards_to_return:
            returned_correctly = self.test_return_multiple_cards(cards_to_return)
            draw_correctly = self.test_draw_cards(8, len(cards_to_return))
        else:
            returned_correctly = True
            draw_correctly = True

        return returned_correctly and draw_correctly

    # Age 8 tests

    # Age 9 tests
    def test_genetics_setup(self, card_name):
        self.set_up_test_generic(card_name)
        self.active_card = self.get_card_object('Mysticism')
        self.meld_card()
        self.active_card = self.get_card_object('Astronomy')
        self.meld_card()

    def test_genetics(self):
        starting_score = self.get_cards_from_list(self.piles_at_beginning_of_action[self.active_player.score_pile.name])
        starting_stack = self.get_cards_from_list(self.piles_at_beginning_of_action[self.active_player.stacks[self.active_card.color].name])

        if starting_stack:
            scored_correctly = self.test_score_multiple_cards(starting_stack)
        else:
            if starting_score == self.active_player.score_pile.cards:
                scored_correctly = True
            else:
                scored_correctly = False

        melded_correctly = self.test_draw_and_meld(10, 1)

        return melded_correctly and scored_correctly

    # Age 10 tests
    def test_ai_setup_0(self, card_name):
        """Case where robotics and software are present, but no lowest score"""
        self.set_up_test_generic(card_name)
        self.active_player = self.get_player_object(1)
        self.active_card = self.get_card_object('Robotics')
        self.meld_card()
        self.active_card = self.get_card_object('Astronomy')
        self.add_card_to_score_pile()
        self.active_card = self.get_card_object('Steam Engine')
        self.add_card_to_score_pile()
        self.active_player = self.get_player_object(0)
        self.active_card = self.get_card_object('Software')
        self.meld_card()

    def test_ai_setup_1(self, card_name):
        """Case where robotics and software are present, and lowest score"""
        self.set_up_test_generic(card_name)
        self.active_player = self.get_player_object(1)
        self.active_card = self.get_card_object('Robotics')
        self.meld_card()
        self.active_card = self.get_card_object('Calendar')
        self.add_card_to_score_pile()
        self.active_player = self.get_player_object(0)
        self.active_card = self.get_card_object('Software')
        self.meld_card()

    def test_ai(self):
        return self.test_ai_0() and self.test_ai_1()

    def test_ai_0(self):
        # TODO - Fix the dependency on the effect state
        result = self.test_draw_and_score_beginning_of_action(10, 1)
        return result

    def test_ai_1(self):
        robotics_and_software = []
        robotics = self.get_card_object('Robotics')
        software = self.get_card_object('Software')
        scores = []
        lowest_score_counter = 0
        game_should_be_over = False

        stacks = self.test_get_all_stacks_at_beginning_of_effect()
        for stack in stacks:
            if stack:
                if stack[0] == robotics or stack[0] == software:
                    robotics_and_software.append(stack[0])

        if len(robotics_and_software) == 2 and robotics in robotics_and_software and software in robotics_and_software:
            for player in self.players:
                scores.append(player.get_score())
                min_score = min(scores)
            for score in scores:
                if score == min_score:
                    lowest_score_counter += 1

            if lowest_score_counter == 1:
                game_should_be_over = True

        if game_should_be_over:
            return self.test_game_over()
        else:
            return not self.test_game_over()

    def test_robotics(self):
        card_to_score = None

        if self.piles_at_beginning_of_action[self.active_player.green_stack.name]:
            card_to_score = self.get_card_object(self.piles_at_beginning_of_effect[self.active_player.green_stack.name][0])

        card_to_draw = self.test_see_draw_card(10)

        if card_to_score:
            if card_to_score.name in self.piles_at_beginning_of_no_share[self.active_player.score_pile.name]:
                scored_correctly = True
            else:
                False
        else:
            scored_correctly = True

        if self.piles_at_beginning_of_no_share[self.active_player.stacks[card_to_draw.color].name][0] == card_to_draw.name:
            melded_correctly = True
        else:
            melded_correctly = False

        no_share_correctly = self.test_no_share_effect(card_to_draw)

        return scored_correctly and melded_correctly and no_share_correctly

    def test_software(self):
        return self.test_software_0() and self.test_software_1()

    def test_software_0(self):
        return self.test_draw_and_score_beginning_of_action(10, 1)

    def test_software_1(self):
        draw_and_meld_correctly = self.test_draw_and_meld(10, 2)
        melded_cards = self.test_see_next_draw_cards(10, 2)
        if len(melded_cards) == 2:
            no_share_card = melded_cards[1]

        no_share_correctly = self.test_no_share_effect(no_share_card)

        if len(melded_cards) == 2:
            return draw_and_meld_correctly and no_share_correctly
        elif len(melded_cards) < 2 and self.game_over:
            return True
        else:
            return False


g = InnovationGame('test', '2022-04-25', 2, None, "Mookifer", True, "Debbie", True, 'Jurdrick', True, "Blanch", True)
g.create_tests()
g.test_a_card('Paper')
# g.create_game()
# g.active_player = g.get_player_object(0)
# g.active_card = g.get_card_object('Clothing')
# g.meld_card()
# g.active_card = g.get_card_object('Sailing')
# g.meld_card()
#
# g.active_card = g.get_card_object('Paper')
# g.execute_dogma_for_yourself()
