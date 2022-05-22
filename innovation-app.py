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

        self.dogma = []

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

# [Card name, effect number, effect type (str), demand_flag]
class Effect:
    """Class for a card effect"""
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
        return "<Card: %s>" % self.name

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


class Game:
    """Base class for a collection of Pile objects and players"""

    def __init__(self, n, d, se=None):
        self.name = n
        self.date = d
        self.piles = []
        self.players = []
        self.cards = []
        self.effects = []
        self.game_over = False
        self.round = 0

        # Set the random see if not specified
        if se is None:
            self.seed = random.randint(0, 9999999999)
        else:
            if isinstance(se, int) and (0 <= se <= 9999999999):
                self.seed = se
            else:
                raise ValueError("Could not create game. Seed must be int between 0 and 9,999,999,999")

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

    def add_effect_to_game(self, e):
        if isinstance(e, Effect):
            self.effects.append(e)
        else:
            raise ValueError("Could not add effect " + str(e) + " to card game " + str(self.name) + ".")

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
        self.turn_player = None
        self.active_card = None

        self.ordered_players = []

        # Variables for each of the icon types
        self.crown = 0
        self.leaf = 1
        self.lightbulb = 2
        self.castle = 3
        self.factory = 4
        self.clock = 5

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
        # self.cards = {}
        self.achievements = {}
        self.special_achievements = {}
        self.draw_piles = {}

        # Create everything needed for the game
        self.__create_piles()
        self.__create_cards()
        self.__create_special_achievements()
        self.__create_players()
        self.__create_effects()

        # Play a game
        # self.play_game()

    def __create_cards(self):
        with open('cards/card_list.csv', 'r') as handle:
            handle.readline()
            lines = handle.read().splitlines()

        for line in lines:
            card = InnovationCard(*line.split('|'))
            start_pile = self.draw_piles[card.age]
            if not start_pile:
                raise ValueError("Error adding card " + str(card) + " to pile " + str(start_pile) + ".")
            start_pile.add_card_to_bottom(card)
            self.add_card_to_game(card)
            # self.cards.update({card.name: card})

    def __create_special_achievements(self):
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
            # self.cards.update({card.name: card})

    def __create_piles(self):
        # Create the draw piles
        pile_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
        for pile in pile_list:
            draw_pile = Pile(pile, self.seed)
            self.add_pile(draw_pile)
            self.draw_piles.update({int(pile): draw_pile})

        # Create achievement piles
        self.add_pile(Pile('achievements', self.seed))
        self.add_pile(Pile('special achievements', self.seed))

        # Create box and reveal piles
        self.add_pile(Pile('reveal', self.seed))
        self.add_pile(Pile('box', self.seed))

    def __create_players(self):
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

            player = InnovationPlayer(self.player_names[i], i, self.ai_players[i], achievement_pile, score_pile, hand, b_stack, g_stack, p_stack, r_stack, y_stack)
            self.add_player(player)

        for player in self.players:
            # Create a player's share order
            self.set_share_order(player)

    def set_up_game(self):
        """Sets up the game to be played"""
        self.shuffle_piles()

        # Pick a card from each of the piles 1-9 to use as an achievement. Change the name of the card to achievement.
        for i in range(1, 10):
            card = self.get_pile_object(str(i)).get_top_card()
            self.get_pile_object('achievements').add_card_to_bottom(card)
            card.name = "Achievement {n}".format(n=i)
            self.achievements.update({card.age: card})

    def shuffle_piles(self):
        for pile in self.draw_piles.values():
            pile.shuffle_pile()

    def starting_play(self):
        """Give everybody two cards, AI evaluates which one to play. Save the selection. Once all picked, execute"""
        # Each player and their selected starting melds
        starting_actions = []
        starting_melds = []
        # Give each player two cards
        for player in self.players:
            self.active_player = player
            self.draw_to_hand(1)
            self.draw_to_hand(1)

            # Create a list of the possible actions (meld either of the cards)
            action_options = []
            for card in player.hand.cards:
                action_options.append(['meld', card])

            # Select one of the cards to meld
            selected_action = self.select_action(player, action_options)

            # Add the player and their selected card to meld to the list of all the melds.
            starting_actions.append([player, selected_action])
            starting_melds.append([player, selected_action[1]])

        # Once everybody has selected their action, meld them all
        for combination in starting_actions:
            self.active_player = combination[0]
            self.execute_action(combination[1])

        # Determine who has the first card alphabetically and set each player's turn position
        alphabetical_order = sorted(starting_actions, key=lambda x: x[1][1].name)
        self.set_table_positions(alphabetical_order[0][0])

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
            # Print for testing
            print('---')
            print("Round {r} - {n}'s Turn".format(r=self.round, n=player.name))
            if self.number_of_players < 4 and player.table_position == 0:
                # Print for testing
                print("{n}'s first action:".format(n=player.name))
                self.take_action(player)
            elif self.number_of_players == 4 and (player.table_position == 0 or player.table_position == 1):
                # Print for testing
                print("{n}'s first action:".format(n=player.name))
                self.take_action(player)
            else:
                # Print for testing
                print("{n}'s first action:".format(n=player.name))
                self.take_action(player)

                # Print for testing
                print("\n{n}'s second action:".format(n=player.name))
                self.take_action(player)

    def play_round(self):
        """Normal round of Innovation where everybody gets two actions"""
        self.round += 1
        for player in self.ordered_players:
            self.turn_player = player
            # Print for testing
            print('---')
            print("Round {r} - {n}'s Turn".format(r=self.round, n=player.name))
            print("{n}'s first action:".format(n=player.name))
            self.take_action(player)

            # Print for testing
            print("\n{n}'s second action:".format(n=player.name))
            self.take_action(player)

    def play_game(self):
        """Play a game of Innovation"""
        self.set_up_game()
        self.starting_play()
        self.play_first_round()

        # All other rounds
        while not self.game_over:
            self.play_round()

    def game_end(self):
        self.game_over = True
        print('Game over')
        # TODO - write code to evaluate scores
        quit()

    def check_game_end(self):
        """Runs when a card is added to an achievement pile. Checks to see if anybody has met goal."""
        for player in self.players:
            print('{p} has {a} achievements'.format(p=player.name, a=player.achievement_pile.get_pile_size()))
            if player.achievement_pile.get_pile_size() >= self.achievement_goal:
                self.game_end()

    # Base functions
    def base_draw(self, draw_value):
        """Base function to draw a card of a specified value"""
        for value in range(draw_value, 11):
            pile = self.get_pile_object(str(value))
            if pile.get_pile_size() > 0:
                card = pile.get_top_card()
                return card

        self.game_end()

    def base_meld(self, card):
        """Base function to meld a card"""
        self.active_player.stacks[card.color].add_card_to_top(card)

    def return_card(self, card):
        """Base function to return a card"""
        self.draw_piles[card.age].add_card_to_bottom(card)

    def score_card(self, player, card):
        """Base function to score a card"""
        player.score_pile.add_card_to_bottom(card)

    def base_tuck(self, card):
        """Base function to tuck a card in a stack"""
        self.active_player.stacks[card.color].add_card_to_bottom(card)

    def find_and_remove_card(self, card):
        """Finds pile where card is located and removes it from that pile"""
        for pile in self.piles:
            for c in pile.cards:
                if c == card:
                    pile.remove_card(c)

    # Base functions to move cards around
    def transfer_card(self, card, to_location, from_location):
        """Base function to move a card from one pile to another. Do not use for stacks, use meld/tuck instead."""
        from_location.remove_card(card)
        to_location.add_card_to_top(card)

    # Combination functions used as card actions
    def add_card_to_achievement_pile(self, card):
        """Moves selected card to a player's achievement pile"""
        self.find_and_remove_card(card)
        self.active_player.achievement_pile.add_card_to_bottom(card)
        self.check_game_end()

    def add_card_to_hand(self, card):
        """Moves selected card to active player's hand"""
        self.find_and_remove_card(card)
        self.active_player.hand.add_card_to_bottom(card)
        # Print for testing
        print('{p} adds {c} to hand'.format(p=self.active_player, c=card.name))

    def add_card_to_score_pile(self, card):
        """Moves selected card to the score pile"""
        self.find_and_remove_card(card)
        self.score_card(self.active_player, card)
        # Print for testing
        print('{p} adds {c} to score pile'.format(p=self.active_player, c=card.name))

    def draw_to_hand(self, draw_value):
        """Draws a card to a players hand of a specified draw value"""
        card = self.base_draw(draw_value)
        # Print for testing
        print('{p} draws {c}'.format(p=self.active_player, c=card.name))
        self.add_card_to_hand(card)

    def draw_and_meld(self, draw_value):
        card = self.base_draw(draw_value)
        self.find_and_remove_card(card)
        self.base_meld(card)
        # Print for testing
        print('{p} draws and melds {c}'.format(p=self.active_player, c=card.name))

    def draw_and_reveal(self, draw_value):
        card = self.base_draw(draw_value)
        # TODO - update to inform card counting module, remove printing
        print('{p} draws and reveals {c}'.format(p=self.active_player, c=card.name))
        return card

    def meld_card(self, card):
        self.find_and_remove_card(card)
        self.base_meld(card)
        # Print for testing
        print('{p} melds {c}'.format(p=self.active_player.name, c=card.name))

    def tuck_card(self, card):
        self.find_and_remove_card(card)
        self.base_tuck(card)
        # Print for testing
        print('{p} tucks {c}'.format(p=self.active_player.name, c=card.name))

    # Actions
    def action_draw(self):
        self.draw_to_hand(1)

    def action_meld(self):
        self.meld_card(self.active_card)

    def action_achieve(self):
        self.add_card_to_achievement_pile(self.active_card)

    def eligible_achievements(self, player):
        """Returns list of achievements that can be taken by the player"""
        score = player.get_score()
        highest_melded = 0
        eligible_achievements = []
        for stack in player.stacks:
            if len(stack.cards) > 0:
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

        self.draw_if_opponents_shared(sharing_players)

    def execute_dogma(self, sharing_players):
        for effect in self.active_card.dogma:

            if effect.demand:
                # Demand effects
                for eligible_player in self.turn_player.share_order:
                    if eligible_player not in sharing_players:
                        self.active_player = eligible_player
                        # Print for testing
                        print('{t} DEMANDS {p} resolve {c} dogma'.format(t=self.turn_player,
                                                                         p=eligible_player.name,
                                                                         c=self.active_card.name))
                        effect.activate()

            else:
                # Standard effects
                for eligible_player in sharing_players:
                    self.active_player = eligible_player
                    # Print for testing
                    print('{p} resolves {c} dogma'.format(p=eligible_player.name, c=self.active_card.name))
                    effect.activate()

    def determine_who_can_share(self):
        """Function to see who can share in an effect"""
        sharing_players = []
        for opponent in self.turn_player.share_order:
            if opponent == self.turn_player:
                sharing_players.append(self.turn_player)
            elif opponent.count_icons_on_board(self.active_card.effect_type) >= self.turn_player.count_icons_on_board(self.active_card.effect_type):
                sharing_players.append(opponent)

        return sharing_players

    def draw_if_opponents_shared(self, list_of_players):
        non_demand_effects = False
        for effect in self.active_card.dogma:
            if not effect.demand:
                non_demand_effects = True
        if len(list_of_players) > 1 and non_demand_effects:
            # TODO - update this to make sure something in the game state changes
            # Print for testing
            print('{p} draws a card due to other players sharing effect'.format(p=self.turn_player))
            self.action_draw()

    # Functions to select and simulate actions
    def take_action(self, player):
        """Function to take an action"""
        self.active_player = player
        available_actions = self.available_actions(player)
        selected_action = self.select_action(player, available_actions)
        self.execute_action(selected_action)

    def available_actions(self, player):
        options = [['draw', None]]

        # Check to see if a player is eligible to claim any achievements, add them to the available options
        eligible_achievements = self.eligible_achievements(player)
        if len(eligible_achievements) > 0:
            for achievement in eligible_achievements:
                options.append(['achieve', achievement])

        # Check to see if the player has any cards in hand, add the ability to meld them to the available options
        if len(player.hand.cards) > 0:
            for card in player.hand.cards:
                options.append(['meld', card])

        # Check to see if the player has any dogma effects that can be activated
        for stack in player.stacks:
            if len(stack.cards) > 0:
                options.append(['dogma', stack.cards[0]])

        return options

    def select_action(self, player, action_list):
        """Function that takes a list of possible actions and selects which one to execute. Human code will select
        based off input, AI via algorithm."""
        if player.ai_flag:
            # TODO - write function for AI to select an action
            selected_action = self.ai_select_action_random_always_achieve(action_list)
        else:
            # TODO - write function for a human to select an action
            selected_action = action_list[0]

        # Print for testing
        if selected_action[0] == 'draw':
            print('{a}'.format(a=selected_action[0].upper()))
        else:
            print('{a} - {c}'.format(a=selected_action[0].upper(), c=selected_action[1]))

        return selected_action

    def execute_action(self, action):
        """Function that takes an action pair ['action', card]"""
        self.active_card = action[1]

        if action[0] == 'draw':
            self.action_draw()
        elif action[0] == 'meld':
            self.action_meld()
        elif action[0] == 'achieve':
            self.action_achieve()
        elif action[0] == 'dogma':
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
            if option[0] == 'achieve':
                selection = i
                break
            i += 1

        if not selection:
            selection = random.randrange(len(action_list))

        return action_list[selection]

    # Effects
    def __create_effects(self):
        # [Card name, effect number, effect type (str), demand_flag, function]
        effects_list = [['Metalworking', 0, 'castle', False, self.metalworking_effect_0],
                        ['Mysticism', 0, 'castle', False, self.mysticism_effect_0],
                        ['Sailing', 0, 'crown', False, self.sailing_effect_0],
                        ['The Wheel', 0, 'castle', False, self.the_wheel_effect_0],
                        ['Writing', 0, 'lightbulb', False, self.writing_effect_0],
                        ['Calendar', 0, 'leaf', False, self.calendar_effect_0],
                        ['Fermentation', 0, 'leaf', False, self.fermentation_effect_0],
                        ['Colonialism', 0, 'factory', False, self.colonialism_effect_0],
                        ['Experimentation', 0, 'lightbulb', False, self.experimentation_effect_0]]

        for effect_to_add in effects_list:
            effect = Effect(effect_to_add[0], effect_to_add[1], effect_to_add[2], effect_to_add[3], effect_to_add[4])
            self.add_effect_to_game(effect)
            associated_card = self.get_card_object(effect.card_name)
            associated_card.dogma.append(effect)

    # Age 1 Effects
    def metalworking_effect_0(self):
        while True:
            card = self.draw_and_reveal(1)
            if card.contains_icon(self.castle):
                self.add_card_to_score_pile(card)
            else:
                self.add_card_to_hand(card)
                break

    def mysticism_effect_0(self):
        card = self.draw_and_reveal(1)

        if card.color in self.active_player.get_colors_on_board():
            self.meld_card(card)
            self.draw_to_hand(1)
        else:
            self.add_card_to_hand(card)

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

    def fermentation_effect_0(self):
        stacks_with_leaves = 0
        for stack in self.active_player.stacks:
            if stack.count_icons_in_stack(self.leaf) > 0:
                stacks_with_leaves += 1

        i = 0
        while i < stacks_with_leaves:
            self.draw_to_hand(2)
            i += 1

    # Age 4 effects
    def colonialism_effect_0(self):
        while True:
            card = self.draw_and_reveal(3)
            self.tuck_card(card)
            if not card.contains_icon(self.crown):
                break

    def experimentation_effect_0(self):
        self.draw_and_meld(5)

    # Tests
    def test_colonialism(self):
        self.shuffle_piles()
        self.turn_player = self.get_player_object(0)
        self.active_player = self.get_player_object(0)
        self.active_card = self.get_card_object('Colonialism')
        self.meld_card(self.active_card)
        self.action_dogma()

    def test_experimentation(self):
        self.shuffle_piles()
        self.turn_player = self.get_player_object(0)
        self.active_player = self.get_player_object(0)
        self.active_card = self.get_card_object('Experimentation')
        self.meld_card(self.active_card)
        self.action_dogma()


g = InnovationGame('test', '2022-04-25', 2, None, "Shohei", True, "Mookifer", True, 'Jurdrick', True, "Bartolo", True)

g.test_experimentation()

