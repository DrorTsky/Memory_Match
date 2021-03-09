from Functions import *


class View(object):

    @staticmethod
    def draw_cards(deck):
        card_draw(deck)

    @staticmethod
    def initial_draw(card_deck, visible_deck):
        draw_initial_screen(card_deck, visible_deck)

    @staticmethod
    def draw_scores(score, screen, x, y):
        size = 36
        color = (225, 225, 235)
        text = "amount of misses: "
        draw_text(screen, text + score, size, color, x, y)

    @staticmethod
    def draw_restart(screen):
        draw_buttons(screen, "one")
