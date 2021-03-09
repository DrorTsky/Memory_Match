# Memory Match Game by Nathan Carmine
import pygame
import random
import pygame.mixer
import pygame.time
import time

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


class Button:
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win, outline=None):
        # Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont(FONT_NAME, 60)
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
    font = pygame.font.Font(pygame.font.match_font(FONT_NAME), size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text_surface, text_rect)


def draw_initial_screen(card_deck, visible_deck):
    card_draw(card_deck)
    pygame.display.update()
    time.sleep(2)
    card_draw(visible_deck)


def match_check(deck, flipped):
    if deck[6 * flipped[0][1] + flipped[0][0]] == deck[6 * flipped[1][1] + flipped[1][0]]:
        return deck[6 * flipped[0][1] + flipped[0][0]]


# Get mouse position, and check which card it's on using division


def card_check(mouse_pos):
    mouse_x_coordinate = mouse_pos[0]
    mouse_y_coordinate = mouse_pos[1]
    car_x_coordinate = int(mouse_x_coordinate / 125)
    car_y_coordinate = int((mouse_y_coordinate - SCREEN_INCREASE) / 181)
    card = (car_x_coordinate, car_y_coordinate)
    return card


def card_draw(cards):
    screen = pygame.display.set_mode(DISPLAY_SIZE)
    draw_buttons(screen, "two")
    # Place card images in their appropriate spots by multiplying card width & height
    for i in range(6):
        for j in range(5):
            screen.blit(cards[i + 6 * j], (i * 125, SCREEN_INCREASE + j * 181))
            # screen increase makes sure cards are drawn below set amount of pixels


def draw_buttons(screen, amount):
    button_width = (DISPLAY_SIZE[0] / 2) - 2
    if amount == "two":
        restart_button = Button((101, 110, 125), 0, 0, button_width, SCREEN_INCREASE, "RESTART")
        back_button = Button((101, 110, 125), DISPLAY_SIZE[0] / 2, 0, button_width + 2, SCREEN_INCREASE, "TO MAIN MENU")
        restart_button.draw(screen)
        back_button.draw(screen)
    else:
        width_start = DISPLAY_SIZE[0] / 2
        back_button = Button((101, 110, 125), width_start - (width_start/2), 0, button_width + 2,
                             SCREEN_INCREASE, "TO MAIN MENU")
        back_button.draw(screen)


"""
DATA ALTERING METHODS
"""


# Load the main card images (used in cards_init())
def load_cards(char):
    card = "./card_images/%s.png" % char
    load_card = pygame.image.load(card).convert()
    cropped_card = pygame.transform.scale(load_card, (CARDS_WIDTH, CARDS_HEIGHT))
    return cropped_card


def cards_init(cards):
    # Load images into array
    for i in range(2, 17):
        cards.append(load_cards(i))
    # Multiply the deck by two so there is one pair of everything
    cards *= 2
    # Shuffle the deck
    random.shuffle(cards)
    return cards


# creates the visible deck
def initialise_visible_deck(amount_of_cards):
    visible_deck = []
    card_back = pygame.transform.scale(pygame.image.load("./card_images/card_back_cover.png").convert(),
                                       (CARDS_WIDTH, CARDS_HEIGHT))
    for x in range(amount_of_cards):
        visible_deck.append(card_back)
    return visible_deck


def game_finished(found, missed):
    found.append("WIN")
    print("YOU WIN!")
    print("Score: %d misses" % missed)
    print("\nPlay again? (y/n)")  # User presses "y" or "n" in the card window
    return FINISHED


def make_visible(flips, found, visible_deck, card_deck):
    # If a match, append coordinates of two cards to found array,
    # and have them permanently displayed by adding them to the visible deck
    for flipped_card in flips:
        # creates a list of newly found cards coordinates
        found.append(flipped_card)
        # appends card fronts to the deck of card covers
        visible_deck[6 * flipped_card[1] + flipped_card[0]] = card_deck[6 * flipped_card[1]
                                                                        + flipped_card[0]]

    print("Matches found: %d/15" % (len(found) / 2))


def show_first_card(screen, card_deck, xy_of_card_selected):
    screen.blit(card_deck[6 * xy_of_card_selected[1] + xy_of_card_selected[0]],
                (125 * xy_of_card_selected[0], SCREEN_INCREASE + 181 * xy_of_card_selected[1]))
    return time.time()  # First card has been flipped
