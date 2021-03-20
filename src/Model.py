from Functions import *


class Model(object):
    """
    a class that represents the Model
    in charge of saving and manipulating data
    """
    def __init__(self):
        self.scores = []
        self.cards = []
        self.visible_deck = []
        self.flips = []
        self.found = []
        self._game_run = True
        self._settings_run = True
        self._t = 1
        self._difficulty = 3
        self._display_time = 2
        self._first_flip = 0
        self._second_flip = 0
        self._missed = 0

    def get_flips(self):
        return self.flips

    def add_flips(self, value):
        self.flips.append(value)

    def delete_flips(self):
        self.flips.clear()

    def get_found(self):
        return self.found

    def add_found(self, value):
        self.found.append(value)

    @property
    def game_run(self):
        return self._game_run

    @game_run.setter
    def game_run(self, value):
        self._game_run = value

    @property
    def settings_run(self):
        return self._settings_run

    @settings_run.setter
    def settings_run(self, value):
        self._settings_run = value

    @property
    def t(self):
        return self._t

    @t.setter
    def t(self, value):
        self._t = value

    @property
    def difficulty(self):
        return self._difficulty

    @difficulty.setter
    def difficulty(self, value):
        self._difficulty = value

    @property
    def display_time(self):
        return self._display_time

    @display_time.setter
    def display_time(self, value):
        self._display_time = value

    @property
    def first_flip(self):
        return self._first_flip

    @first_flip.setter
    def first_flip(self, value):
        self._first_flip = value

    @property
    def second_flip(self):
        return self._second_flip

    @second_flip.setter
    def second_flip(self, value):
        self._second_flip = value

    @property
    def missed(self):
        return self._missed

    @missed.setter
    def missed(self, value):
        self._missed = value

    def get_scores(self):
        scores_file = open(HS_FILE, "r")
        self.scores = scores_file.read().splitlines()
        scores_file.close()
        return self.scores

    def save_score_in_file(self):
        scores_file = open(HS_FILE, "a")
        scores_file.write(str(self.missed)+"\n")
        scores_file.close()

    def get_cards(self):
        return self.cards

    def set_cards(self, cards):
        self.cards = cards

    def set_visible_deck(self):
        self.visible_deck = initialise_visible_deck(AMOUNT_OF_CARDS)

    def get_visible_deck(self):
        return self.visible_deck
