# import time
from pygame import *
import pygame_menu
from Model import Model
from View import View
from Functions import *


class Controller(object):
    """
    a class representing the Controller
    in charge of receiving user input and updating
    the Model and View accordingly
    """
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def init_cards(self, difficulty):
        """
        sets the card array in the Model

        :param difficulty: int, responsible for amount of cards
        :return:
        """
        cards = self.model.get_cards()
        self.model.set_cards(cards_init(cards, difficulty))

    def get_and_draw_scores(self, screen):
        """
        get the scores from the Model
        draw them on the screen using the View

        :param screen: pygame screen
        :return:
        """
        scores = self.model.get_scores()
        scores.sort(key=int)
        self.view.draw_restart(screen)
        for index, score in enumerate(scores):
            self.view.draw_scores(score, screen, DISPLAY_SIZE[0] / 2, SCREEN_INCREASE + 10 + index * 50)

    def initial_draw(self, sleep_time, difficulty):
        """
        takes the cards array and visible cards array from Model
        draws the cards for the first time using View

        :param sleep_time: int, seconds for the cards to remain visible
        :param difficulty: int, how many cards to draw
        :return:
        """
        self.view.initial_draw(self.model.get_cards(), self.model.get_visible_deck(), sleep_time, difficulty)

    def increase_decrease_setting(self, setting, inc_dec):
        """
        increase / decrease the difficulty / time according to user input

        :param setting: string, difficulty or time
        :param inc_dec: string, plus or minus
        :return:
        """
        if setting == "difficulty":
            if inc_dec == "plus":
                if self.model.difficulty < 3:
                    self.model.difficulty += 1
                else:
                    print("max difficulty")
            else:
                if self.model.difficulty > 1:
                    self.model.difficulty -= 1
                else:
                    print("can't decrease difficulty")
        else:
            if inc_dec == "plus":
                self.model.display_time += 1
            else:
                if self.model.display_time > 1:
                    self.model.display_time -= 1
                else:
                    print("can't decrease time")

    def settings_update(self, game_event, screen, runs,):
        """
        listens to user input and activate the correct buttons

        :param game_event: Event
        :param screen: pygame screen
        :param runs: int
        :return:
        """
        if game_event.type == pygame.QUIT:
            self.model.settings_run = False
        if game_event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            start_x = (DISPLAY_WIDTH / 6) + (DISPLAY_WIDTH / 2) - 1
            end_x = (DISPLAY_WIDTH / 6) + (DISPLAY_WIDTH / 2) + DISPLAY_WIDTH / 10
            start_y = DISPLAY_HEIGHT / 6
            end_y = start_y*2
            if start_x < mouse_pos[0] < start_x + DISPLAY_WIDTH / 10:
                if start_y < mouse_pos[1] < start_y + SCREEN_INCREASE:
                    self.increase_decrease_setting("difficulty", "plus")
                elif end_y < mouse_pos[1] < end_y + SCREEN_INCREASE:
                    self.increase_decrease_setting("time", "plus")
            elif end_x < mouse_pos[0] < end_x + DISPLAY_WIDTH / 10:
                if start_y < mouse_pos[1] < start_y + SCREEN_INCREASE:
                    self.increase_decrease_setting("difficulty", "minus")
                if end_y < mouse_pos[1] < end_y + SCREEN_INCREASE:
                    self.increase_decrease_setting("time", "minus")
            if mouse_pos[1] < SCREEN_INCREASE:
                width_start = DISPLAY_SIZE[0] / 2
                if width_start / 2 < mouse_pos[0] < width_start + (width_start / 2):
                    main_menu(screen, runs, self)

    def draw_setting(self, screen):
        """
        take difficulty and display time from model
        using the View, draws the settings window
        :param screen: pygame screen
        :return:
        """
        self.view.draw_settings(screen, self.model.difficulty, self.model.display_time)

    def update(self, game_event, runs, screen, controller):
        """
        listens to user input and activates the right buttons /
        flips the selected cards

        :param game_event: Event
        :param runs: int
        :param screen: pygame screen
        :param controller: Controller
        :return:
        """
        difficulty = controller.model.difficulty
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
                    if difficulty == 3 or \
                            (difficulty == 2 and xy_of_card_selected[0] < 5 and xy_of_card_selected[1] < 4) or \
                            (difficulty == 1 and xy_of_card_selected[0] < 4 and xy_of_card_selected[1] < 3):
                        self.model.add_flips(xy_of_card_selected)
                        if len(self.model.get_flips()) <= 2:
                            self.model.first_flip = show_first_card(screen, self.model.get_cards(), xy_of_card_selected,
                                                                    difficulty)
                        if len(self.model.flips) == 2:
                            # Second card has been flipped
                            self.model.second_flip = time.time()
                            # Do the two cards a match?
                            match = match_check(self.model.get_cards(), self.model.flips, difficulty + 3)
                            if match:
                                make_visible(self.model.get_flips(), self.model.get_found(),
                                             self.model.get_visible_deck(),
                                             self.model.get_cards(), difficulty + 3)
                                self.model.t = 0
                            else:
                                self.model.missed += 1
            elif mouse_pos[0] < DISPLAY_SIZE[0] / 2:
                play_game(runs, screen, controller)
            else:
                # main(NEW_GAME)
                main_menu(screen, runs, controller)

    def scores_event(self, game_event, screen, runs, controller):
        if game_event.type == pygame.QUIT:
            self.model.game_run = False
        if game_event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()
            if mouse_pos[1] < SCREEN_INCREASE:
                width_start = DISPLAY_SIZE[0] / 2
                if width_start / 2 < mouse_pos[0] < width_start + (width_start/2):
                    main_menu(screen, runs, controller)

    def tick(self, difficulty):
        """
        checks that the first flipped card doesn't stay visible
        longer than two seconds

        :param difficulty: int
        :return:
        """
        # Show the cards only for one second
        if len(self.model.get_flips()) >= 2 and time.time() - self.model.second_flip > self.model.t:
            self.model.t = 1
            card_draw(self.model.get_visible_deck(), difficulty)
            self.model.delete_flips()

        # If the user is slow, the card gets flipped back
        if len(self.model.get_flips()) == 1 and time.time() - self.model.first_flip > 3:
            card_draw(self.model.get_visible_deck(), difficulty)
            self.model.delete_flips()

    def done(self):
        """
        game is over, save the score to the scores file
        using the Model
        :return:
        """
        self.model.save_score_in_file()
        return game_finished(self.model.get_found(), self.model.missed)

    def game_finished_check_for_rematch(self, screen, runs, pressed_key, controller):
        """
        asks user for rematch
        Y = yes, N = no
        :param screen: pygame screen
        :param runs: int
        :param pressed_key: key pressed
        :param controller: Controller
        :return:
        """
        if runs == FINISHED:
            if pressed_key[K_y]:
                play_game(runs, screen, controller)
            elif pressed_key[K_n]:
                self.model.game_run = False


def play_game(runs, screen, controller):
    """
    main game function
    :param runs:
    :param screen:
    :param controller:
    :return:
    """
    fps_clock = pygame.time.Clock()
    c = Controller(Model(), View())
    # initialize deck
    c.init_cards(controller.model.difficulty)

    # Load card-back image for all cards at first, and have matches slowly unveiled
    c.model.set_visible_deck()

    # Shows cards for the first time
    c.initial_draw(controller.model.display_time, controller.model.difficulty)
    max_amount_of_matches = controller.model.difficulty * 10
    if controller.model.difficulty == 1:
        max_amount_of_matches += 2
    while c.model.game_run:
        user_input = pygame.event.get()
        pressed_key = pygame.key.get_pressed()
        # Retrieves all user input
        for game_event in user_input:
            c.update(game_event, runs, screen, controller)

        # checks how many cards were flipped
        c.tick(controller.model.difficulty)
        # This comes before quitting to avoid video errors
        pygame.display.flip()
        fps_clock.tick(DESIRED_FPS)

        if len(c.model.get_found()) == max_amount_of_matches:
            # print score and asks for another round
            runs = c.done()

        # if game finished checks for user input
        c.game_finished_check_for_rematch(screen, runs, pressed_key, controller)

    pygame.quit()


def show_scores(runs, screen, controller):
    """
    draws and displays the scores

    :param runs: int
    :param screen: pygame screen
    :param controller: Controller
    :return:
    """
    screen.fill((0, 0, 0))
    c = Controller(Model(), View())
    c.get_and_draw_scores(screen)
    pygame.display.update()
    while c.model.game_run:
        user_input = pygame.event.get()
        for game_event in user_input:
            c.scores_event(game_event, screen, runs, controller)
    pygame.quit()


def settings(screen, c, runs):
    """
    draws and displays the settings

    :param screen: pygame screen
    :param c: Controller
    :param runs: int
    :return:
    """
    c.draw_setting(screen)
    while c.model.settings_run:
        user_input = pygame.event.get()
        for game_event in user_input:
            c.settings_update(game_event, screen, runs)
            c.draw_setting(screen)
    c.model.settings_run = True


def main_menu(screen, runs, c):
    """
    generates the main menu screen

    :param screen: pygame screen
    :param runs: int
    :param c: Controller
    :return:
    """
    # menu = pygame_menu.Menu(600, 400, 'Welcome', theme=pygame_menu.themes.THEME_BLUE)
    menu = pygame_menu.Menu(DISPLAY_HEIGHT * 90 / 100, DISPLAY_WIDTH * 80 / 100, 'Welcome',
                            theme=pygame_menu.themes.THEME_BLUE)
    menu.add_button('Settings', settings, screen, c, runs)
    menu.add_button('Scores', show_scores, runs, screen, c)
    menu.add_button('Play', play_game, runs, screen, c)
    menu.add_button('Quit', pygame_menu.events.EXIT)
    menu.mainloop(screen)


def main(runs):
    c = Controller(Model(), View())
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY_SIZE)
    pygame.display.set_caption(GAME_TITLE)
    main_menu(screen, runs, c)


if __name__ == "__main__":
    main(NEW_GAME)
