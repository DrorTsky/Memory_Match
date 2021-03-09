# import time
from pygame import *
import pygame_menu
from Model import Model
from View import View
from Functions import *

HS_FILE = "high_scores.txt"
AMOUNT_OF_CARDS = 30
SCREEN_INCREASE = 75
DELTA = 106
DISPLAY_SIZE = (750, 905 + SCREEN_INCREASE)
GAME_TITLE = "Memory Match"
DESIRED_FPS = 60
FINISHED = 1
NEW_GAME = 0
CARDS_WIDTH = 125
CARDS_HEIGHT = 181
FONT_NAME = "comicsans"


class Controller(object):

    def __init__(self, model, view):
        self.model = model
        self.view = view

    def init_cards(self):
        cards = self.model.get_cards()
        self.model.set_cards(cards_init(cards))

    def get_and_draw_scores(self, screen):
        scores = self.model.get_scores()
        self.view.draw_restart(screen)
        for index, score in enumerate(scores):
            self.view.draw_scores(score, screen, DISPLAY_SIZE[0] / 2, SCREEN_INCREASE + 10 + index * 50)

    def draw_cards(self, deck):
        self.view.draw_cards(deck)

    def initial_draw(self):
        self.view.initial_draw(self.model.get_cards(), self.model.get_visible_deck())

    def generate_visible_deck(self):
        self.model.set_visible_deck()

    def update(self, game_event, runs, screen):
        if game_event.type == pygame.QUIT:
            self.model.game_run = False
        if game_event.type == pygame.MOUSEBUTTONDOWN:
            # Get position of mouse and put it into card_check
            # to figure out which card mouse is on
            mouse_pos = pygame.mouse.get_pos()
            xy_of_card_selected = card_check(mouse_pos)
            # Make sure card has not been selected before
            if mouse_pos[1] >= SCREEN_INCREASE:
                if xy_of_card_selected not in self.model.get_flips() and \
                        xy_of_card_selected not in self.model.get_found():
                    self.model.add_flips(xy_of_card_selected)
                    if len(self.model.get_flips()) <= 2:
                        self.model.first_flip = show_first_card(screen, self.model.get_cards(), xy_of_card_selected)
                    if len(self.model.flips) == 2:
                        self.model.second_flip = time.time()  # Second card has been flipped
                        match = match_check(self.model.get_cards(), self.model.flips)  # Are the two cards a match?
                        if match:
                            make_visible(self.model.get_flips(), self.model.get_found(), self.model.get_visible_deck(),
                                         self.model.get_cards())
                            self.model.t = 0
                        else:
                            self.model.missed += 1
            elif mouse_pos[0] < DISPLAY_SIZE[0] / 2:
                play_game(runs, screen)
            else:
                main(NEW_GAME)

    def scores_event(self, game_event):
        if game_event.type == pygame.QUIT:
            self.model.game_run = False
        if game_event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if mouse_pos[1] < SCREEN_INCREASE:
                if mouse_pos[0] < DISPLAY_SIZE[0] / 2:
                    # play_game(runs, screen, self)
                    pass
                else:
                    main(NEW_GAME)

    def tick(self):
        # Show the cards only for one second
        if len(self.model.get_flips()) >= 2 and time.time() - self.model.second_flip > self.model.t:
            self.model.t = 1
            card_draw(self.model.get_visible_deck())
            self.model.delete_flips()

        # If the user is slow, the card gets flipped back
        if len(self.model.get_flips()) == 1 and time.time() - self.model.first_flip > 3:
            card_draw(self.model.get_visible_deck())
            self.model.delete_flips()

    def done(self):
        self.model.save_score_in_file()
        return game_finished(self.model.get_found(), self.model.missed)

    def game_finished_check_for_rematch(self, screen, runs, pressed_key):
        if runs == FINISHED:
            if pressed_key[K_y]:
                play_game(runs, screen)
            elif pressed_key[K_n]:
                self.model.game_run = False


def play_game(runs, screen):
    fps_clock = pygame.time.Clock()
    c = Controller(Model(), View())
    # initialize deck
    c.init_cards()

    # Load card-back image for all cards at first, and have matches slowly unveiled
    c.generate_visible_deck()

    # Shows cards for the first time
    c.initial_draw()

    while c.model.game_run:
        user_input = pygame.event.get()
        pressed_key = pygame.key.get_pressed()
        # Retrieves all user input
        for game_event in user_input:
            c.update(game_event, runs, screen)

        # checks how many cards were flipped
        c.tick()
        # This comes before quitting to avoid video errors
        pygame.display.flip()
        fps_clock.tick(DESIRED_FPS)

        if len(c.model.get_found()) == 30:
            # print score and asks for another round
            runs = c.done()

        # if game finished checks for user input
        c.game_finished_check_for_rematch(screen, runs, pressed_key)

    pygame.quit()


def show_scores(screen):

    screen.fill((0, 0, 0))
    c = Controller(Model(), View())
    c.get_and_draw_scores(screen)
    pygame.display.update()
    while c.model.game_run:
        user_input = pygame.event.get()
        for game_event in user_input:
            c.scores_event(game_event)
    pygame.quit()


def main(runs):

    pygame.init()
    screen = pygame.display.set_mode(DISPLAY_SIZE)
    pygame.display.set_caption(GAME_TITLE)

    menu = pygame_menu.Menu(300, 400, 'Welcome', theme=pygame_menu.themes.THEME_BLUE)
    menu.add_button('Scores', show_scores, screen)
    menu.add_button('Play', play_game, runs, screen)
    menu.add_button('Quit', pygame_menu.events.EXIT)

    menu.mainloop(screen)


if __name__ == "__main__":
    main(NEW_GAME)
