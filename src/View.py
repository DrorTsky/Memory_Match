from Functions import *


class View(object):
    """
    a class that represent the View
    in charge of drawing data onto the GUI
    """
    @staticmethod
    def draw_cards(deck, difficulty):
        """
        draws cards onto screen according to difficulty

        :param deck: string array, cards image paths
        :param difficulty: int, how many cards to draw
        :return:
        """
        card_draw(deck, difficulty)

    @staticmethod
    def initial_draw(card_deck, visible_deck, sleep_time, difficulty):
        """
        draws the an amount of cards onto the screen according to
        "difficulty", show them for "sleep_time" seconds, switch to
        card backs

        :param card_deck: string array, image paths
        :param visible_deck: string array, card backs
        :param sleep_time: int, how long to remain visible
        :param difficulty: int, how many cards to draw
        :return:
        """
        draw_initial_screen(card_deck, visible_deck, sleep_time, difficulty)

    @staticmethod
    def draw_scores(score, screen, x, y):
        """
        prints the scores onto screen in x,y location
        :param score: string, number representing the misses
        :param screen: pygame screen
        :param x: int
        :param y: int
        :return:
        """
        size = 36
        color = (225, 225, 235)
        text = "amount of misses: "
        draw_text(screen, text + score, size, color, x, y)

    @staticmethod
    def draw_restart(screen):
        """
        draws the restart button
        :param screen: pygame screen
        :return:
        """
        draw_buttons(screen, "one")

    @staticmethod
    def draw_settings(screen, difficulty, settings_time):
        """
        draws the settings buttons on screen

        :param screen: pygame screen
        :param difficulty: int
        :param settings_time: int
        :return:
        """
        screen.fill((0, 0, 0))
        draw_settings_buttons(screen, difficulty, 1)
        draw_settings_buttons(screen, settings_time, 2)
        draw_buttons(screen, 1)
        pygame.display.update()
