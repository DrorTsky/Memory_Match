# Memory Match Game by Nathan Carmine
import pygame
import random
import pygame.mixer
import pygame.time
import time

# ratio of width 1/6 , height 1/5
HS_FILE = "high_scores.txt"
AMOUNT_OF_CARDS = 30
SCREEN_INCREASE = 75
DELTA = 106
DISPLAY_WIDTH = 600
DISPLAY_HEIGHT = 725
# DISPLAY_WIDTH = 750
# DISPLAY_HEIGHT = 905
DISPLAY_SIZE = (DISPLAY_WIDTH, DISPLAY_HEIGHT + SCREEN_INCREASE)
GAME_TITLE = "Memory Match"
DESIRED_FPS = 60
FINISHED = 1
NEW_GAME = 0
CARDS_WIDTH = 100
# CARDS_WIDTH = 125
# CARDS_HEIGHT = 181
CARDS_HEIGHT = 145
FONT_NAME = "comicsans"
FONT_BUTTON_SIZE = 45


class Button:
    """
    A class to represent a button

    Attributes
    ------------
    color: rgb
    x: int
    y: int
    width: int
    height: int
    text: string
    """
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win, outline=None):
        """
        draws button

        :param win: pygame window
        :param outline:
        :return:
        """
        # Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont(FONT_NAME, FONT_BUTTON_SIZE)
            text = font.render(self.text, True, (0, 0, 0))
            win.blit(text, (self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 -
                                                                                        text.get_height() / 2)))

    def is_over(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        # if pos[0] > self.x and pos[0] < self.x + self.width:
        if self.x < pos[0] < self.x + self.width:
            # if pos[1] > self.y and pos[1] < self.y + self.height:
            if self.y < pos[1] < self.y + self.height:
                return True

        return False


"""
NON DATA ALTERING METHODS
"""


def draw_text(screen, text, size, color, x, y):
    """
    draws a string onto the given x,y in the given color

    :param screen: pygame screen
    :param text: string
    :param size: int
    :param color: rgb
    :param x: int
    :param y: int
    :return:
    """
    font = pygame.font.Font(pygame.font.match_font(FONT_NAME), size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text_surface, text_rect)


def draw_initial_screen(card_deck, visible_deck, sleep_time, difficulty):
    """
    draws the an amount of cards onto the screen according to "difficulty",
    show them for "sleep_time" seconds, switch to card backs

    :param card_deck: string array, image paths
    :param visible_deck: string array, image paths
    :param sleep_time: int
    :param difficulty: int
    :return:
    """
    card_draw(card_deck, difficulty)
    pygame.display.update()
    time.sleep(sleep_time)
    card_draw(visible_deck, difficulty)


def match_check(deck, flipped, card_range):
    """
    checks if the cards from the "flipped" array match

    :param deck: string array, image paths
    :param flipped: string array, selected image paths
    :param card_range: difficulty helper variable
    :return:
    """
    if deck[card_range * flipped[0][1] + flipped[0][0]] == deck[card_range * flipped[1][1] + flipped[1][0]]:
        return deck[card_range * flipped[0][1] + flipped[0][0]]


# Get mouse position, and check which card it's on using division


def card_check(mouse_pos):
    """
    checks which card is selected by mouse click

    :param mouse_pos: tuple of (x = int, y = int) ,position of cursor
    :return: tuple of (x = int, y = int), card in the cursor position
    """
    mouse_x_coordinate = mouse_pos[0]
    mouse_y_coordinate = mouse_pos[1]
    car_x_coordinate = int(mouse_x_coordinate / CARDS_WIDTH)
    car_y_coordinate = int((mouse_y_coordinate - SCREEN_INCREASE) / CARDS_HEIGHT)
    card = (car_x_coordinate, car_y_coordinate)
    return card


def card_draw(cards, difficulty):
    """
    draws cards on screen according to difficulty
    difficulty 3 = 30 cards
    difficulty 2 = 20 cards
    difficulty 1 = 12 cards

    :param cards: string array, image paths
    :param difficulty: int, helps asses how many cards to draw
    :return:
    """
    screen = pygame.display.set_mode(DISPLAY_SIZE)
    draw_buttons(screen, "two")
    x_range = 3 + difficulty
    y_range = 2 + difficulty
    # Place card images in their appropriate spots by multiplying card width & height
    for i in range(x_range):
        for j in range(y_range):
            screen.blit(cards[i + x_range * j], (i * CARDS_WIDTH, SCREEN_INCREASE + j * CARDS_HEIGHT))
            # screen increase makes sure cards are drawn below set amount of pixels


def draw_buttons(screen, amount):
    """
    draws either just the "TO MAIN MENU" button or "TO MAIN MENU" and "RESTART" button

    :param screen: pygame screen
    :param amount: int, how many buttons to draw
    :return:
    """
    button_width = (DISPLAY_SIZE[0] / 2) - 2
    if amount == "two":
        restart_button = Button((101, 110, 125), 0, 0, button_width, SCREEN_INCREASE, "RESTART")
        back_button = Button((101, 110, 125), DISPLAY_SIZE[0] / 2, 0, button_width + 2, SCREEN_INCREASE, "TO MAIN MENU")
        restart_button.draw(screen)
        back_button.draw(screen)
    else:
        width_start = DISPLAY_SIZE[0] / 2
        back_button = Button((101, 110, 125), width_start - (width_start / 2), 0, button_width + 2,
                             SCREEN_INCREASE, "TO MAIN MENU")
        back_button.draw(screen)


"""
DATA ALTERING METHODS
"""


# Load the main card images (used in cards_init())
def load_cards(char):
    """
    loads a card image from folder given the right string
    and crops it to the right size

    :param char: part of the image name
    :return: string: card path
    """
    card = "./card_images/%s.png" % char
    load_card = pygame.image.load(card).convert()
    cropped_card = pygame.transform.scale(load_card, (CARDS_WIDTH, CARDS_HEIGHT))
    return cropped_card


def cards_init(cards, difficulty):
    """
    appends image paths to array
    duplicates the array
    shuffles the array

    :param cards: string array, represents the game cards
    :param difficulty: int, helps understand how many cards to load
    :return: string array, image paths
    """
    # Load images into array
    if difficulty == 1:
        bottom_range = 11
    elif difficulty == 2:
        bottom_range = 7
    else:
        bottom_range = 2
    for i in range(bottom_range, 17):
        cards.append(load_cards(i))
    # Multiply the deck by two so there is one pair of everything
    cards *= 2
    # Shuffle the deck
    random.shuffle(cards)
    return cards


# creates the visible deck
def initialise_visible_deck(amount_of_cards):
    """
    generates a string array with "amount_of_cards" card back cover image

    :param amount_of_cards: amount of cards in the deck
    :return: string array, "amount_of_cards" card back cover image
    """
    visible_deck = []
    card_back = pygame.transform.scale(pygame.image.load("./card_images/card_back_cover.png").convert(),
                                       (CARDS_WIDTH, CARDS_HEIGHT))
    for x in range(amount_of_cards):
        visible_deck.append(card_back)
    return visible_deck


def game_finished(found, missed):
    """
    prints amount of misses and asks the user for a new game

    :param found: string array, array with all the found cards
    :param missed: int, amount of time user missed
    :return: int
    """
    found.append("WIN")
    print("YOU WIN!")
    print("Score: %d misses" % missed)
    print("\nPlay again? (y/n)")  # User presses "y" or "n" in the card window
    return FINISHED


def make_visible(flips, found, visible_deck, card_deck, card_range):
    """
    makes the "flips" cards visible by appending their image paths
    to the "visible_deck" array and prints how many matches found

    :param flips: string array, flipped cards image paths
    :param found: string array, found cards image paths
    :param visible_deck: string array, currently visible cards image paths
    :param card_deck: string array, cards image paths
    :param card_range: int, helps find the correct card by difficulty
    :return:
    """
    # If a match, append coordinates of two cards to found array,
    # and have them permanently displayed by adding them to the visible deck
    for flipped_card in flips:
        # creates a list of newly found cards coordinates
        found.append(flipped_card)
        # appends card fronts to the deck of card covers
        visible_deck[card_range * flipped_card[1] + flipped_card[0]] = card_deck[card_range * flipped_card[1]
                                                                                 + flipped_card[0]]

    print(f'Matches found: {int(len(found) / 2)}/{int((card_range * (card_range-1))/2)}')


def show_first_card(screen, card_deck, xy_of_card_selected, difficulty):
    """
    makes the first selected card visible

    :param screen: pygame screen
    :param card_deck: string array, cards image paths
    :param xy_of_card_selected: tuple, location of selected card
    :param difficulty: int
    :return: float, current time in seconds
    """
    card_range = 3 + difficulty
    screen.blit(card_deck[card_range * xy_of_card_selected[1] + xy_of_card_selected[0]],
                (CARDS_WIDTH * xy_of_card_selected[0], SCREEN_INCREASE + CARDS_HEIGHT * xy_of_card_selected[1]))
    return time.time()  # First card has been flipped


def draw_settings_buttons(screen, counter, amount):
    """
    draws the settings buttons
    amount = 1: difficulty button
    amount = 2: time button

    :param screen: pygame screen
    :param counter: int, level of difficulty / time
    :param amount: int, which button to draw
    :return:
    """
    if amount == 1:
        name = "difficulty   "
    else:
        name = "time   "
    plus_minus_button_width = DISPLAY_WIDTH / 10
    buttons_starting_x_position = DISPLAY_WIDTH / 6
    buttons_starting_y_position = DISPLAY_HEIGHT / 6
    counter_button_width = (DISPLAY_WIDTH / 2) - 2
    dif_plus = Button((101, 110, 125), buttons_starting_x_position + counter_button_width + 1,
                      amount * buttons_starting_y_position, plus_minus_button_width, SCREEN_INCREASE, "+")

    dif_minus = Button((101, 110, 125), buttons_starting_x_position + (DISPLAY_WIDTH / 2) + plus_minus_button_width,
                       amount * buttons_starting_y_position, plus_minus_button_width, SCREEN_INCREASE, "-")

    restart_button = Button((101, 110, 125), buttons_starting_x_position,
                            amount * buttons_starting_y_position, counter_button_width, SCREEN_INCREASE,
                            name + str(counter))
    restart_button.draw(screen)
    dif_plus.draw(screen)
    dif_minus.draw(screen)
