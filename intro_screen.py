import math
import pygame, sys
from queue import LifoQueue
from character import Character, create_all_characters
import config
from button import Button
# import davis


pygame.init()
# pygame.display.init()
gameDisplay = pygame.display.set_mode((config.display_width, config.display_height))

buttons = []
def changing_term(string):
    font = config.SPOOKY_SMALL_FONT
    space = font.size(' ')[0]
    word_counter = 0
    words = [word.split(' ') for word in string.splitlines()]
    x, y = (config.display_width / 7, config.display_height / 5)
    time = 0
    term = ''
    gameDisplay.fill(config.black)

    for letters in range(len(string)):  # grabs every letter from the text
        term += string[letters]
        term_surface = font.render(term, True, config.red)
        word_surface = font.render(words[0][word_counter], True, config.red)
        term_rect = term_surface.get_rect()
        term_rect.center = (config.display_width / 7, config.display_height / 5)
        word_width, word_height = word_surface.get_size()
        term_width, term_height = term_surface.get_size()
        w = term_width

        if word_counter >= len(words[0]) - 1 and string[letters] == words[0][len(words[0]) - 1][-1]:
            buttons.append(Button("Next", config.white, config.SPOOKY_SMALL_FONT, (1290, 530), gameDisplay))

            print(buttons[0].text)

        if string[
            letters] == ' ':  # if there is a space between words then check if the next word will fit onto the screen
            word_counter += 1
            if word_width + w + space > math.floor((5 * (
                    config.display_width / 6))):  # reset the position of the word to print the word/characetr in the next line
                term = string[letters]
                term_surface = font.render(term, True, config.red)
                y = y + term_height

        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_c:  # if c button is not pressed text will appear on screen with default settings
                    time = 100
            if event.type == pygame.KEYDOWN:  # must press c button to move the text faster
                if event.key == pygame.K_c:
                    time = 10
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()


        gameDisplay.blit(term_surface, (config.display_width / 7, y))
        pygame.display.update()
        pygame.time.wait(time)

def prev():
    prev_val = LifoQueue()


def main():
    bool = True
    changing_term(

        "Hello World! You are a student in University at Buffalo's Davis Hall- "
        "and you've been trapped inside. The dark halls are filled with horrors, "
        "and the exit is guarded by a frightening entity... What type of student are "
        "you? How will you fight your way through to your escape? However, the real "
        "question is... Can you escape?"
    )
    # davis.character_selection()
    while bool:
        for button in buttons:
            Button.check_Hover(button, gameDisplay)
        for event in pygame.event.get():
            # Button.check_Hover(buttons[0], gameDisplay)
            if (event.type == pygame.MOUSEBUTTONDOWN):
                print(pygame.mouse.get_pos())
            if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and buttons[0].rect.collidepoint(
                    pygame.mouse.get_pos())):

                bool = False
                break

            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                sys.exit()


# main() #uncomment this to run this file separaetly from the main davis file
