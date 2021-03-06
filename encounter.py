import json
import os
import pygame
import random
import enemies
import random
import config
import player
import game
import transitions
import music_choice
import character

# Global variable to be used to count movements and encounters
step_counter = 0
encounter_trigger = 8192
music_steps = 0
in_battle = False
enemy_selected = False
# Is set to true when the boss fight should be triggered
boss_flag = False
# Is set to true when boss is defeated
boss_defeated = False

# Implements a step counter in order to control random enemy encounters on the map

# Should be called at beginning of level and after every enemy encounter
def restart_encounters():
    global step_counter
    step_counter = 0
    #print("Step counter is " + str(step_counter) + "\n")

def increment_step_counter():
    global step_counter
    global music_steps
    increment = random.randrange(1, 128)
    step_counter += increment
    music_steps += increment
    #print("Step counter after adding is " + str(step_counter) + "\n")
    if step_counter >= encounter_trigger:
        # Then trigger a battle with a random enemy
        global in_battle
        in_battle = True
        # enemy_trigger called in game.py
        #print("Step counter at encounter is " + str(step_counter) + "\n")
        # Restart the counter
        restart_encounters()

# Selects an enemy randomly, but not the boss
def select_enemy():
    global boss_flag
    # If the boss flag is set, then return the boss
    if boss_flag == True:
        print("Chose" + enemies.boss_enemy().type)
        return enemies.boss_enemy()
    # Otherwise, choose any other one
    enemy = enemies.random_enemy()
    if enemy.type == "Ethan":
        enemy = enemies.random_enemy()
        select_enemy()
    print("Chose " + enemy.type)
    return enemy

# Will cause an enemy to be chosen, blitted to screen, and thus a battle to trigger
def enemy_trigger(gameDisplay):
    global enemy_selected
    global in_battle
    enemy = None
    if boss_flag and not enemy_selected:
        enemy_selected = True
        enemy = enemies.random_enemy()
        music_choice.encounter_choice(enemy)
        player.player_speed = 0
        return enemy
    # Select an enemy
    if not enemy_selected:
        enemy = select_enemy()
        enemy_selected = True
        music_choice.encounter_choice(enemy)
    # Stop movement during battle
    player.player_speed = 0
    if enemy_selected:
        return enemy

def player_death():
    global in_battle
    global enemy_selected
    in_battle = False
    enemy_selected = False
    player.player_speed = 2
    # Have to do this as there is a bug where increments count when arrows are pressed during battle
    restart_encounters()
    music_choice.death()

def enemy_blit(gameDisplay, enemy):
    global in_battle
    if in_battle:
        #print("Enemy selected is " + str(enemy.type) + "\n")
        image_path = "assets/enemy_sprites/" + str(enemy.type) + ".png"
        enemy_image = pygame.image.load(image_path)
        enemy_rect = enemy_image.get_rect()
        if boss_flag:
            enemy_rect.x = 600
            enemy_rect.y = 10
            gameDisplay.blit(enemy_image, enemy_rect)
            return
        enemy_rect.x = 500
        enemy_rect.y = 100
        #print("about to get surface\n")
        if gameDisplay is None:
            print("display aint here idiot\n")
        gameDisplay.blit(enemy_image, enemy_rect)
    #print("Stopped blitting enemy")

# Call to stop the battle, when the enemy has been defeated
def enemy_defeated(sc, flag):
    print("Enemy defeated!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
    global in_battle
    global enemy_selected
    global boss_defeated
    if flag:
        # This means that the boss has been defeated
        boss_defeated = True
    # Else, proceed normally
    in_battle = False
    enemy_selected = False
    player.player_speed = 2
    # Set this global variable to zero again (kinda works as an init flag for each new encounter)
    game.enemy_healthBar = 0
    # Have to do this as there is a bug where increments count when arrows are pressed during battle
    restart_encounters()
