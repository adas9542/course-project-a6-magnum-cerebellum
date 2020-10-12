import time
import random
import pygame
import math
import music
import config
from button import Button
import inventory
from inventory import inventoryMain
import game

#####################################################################################
#This provides the functions for computing and displaying health/mana bars.
#####################################################################################

class Bar:

    def __init__(self, color, font, pos, gameDisplay):
        self.color = color
        self.font = font
        self.pos = pos
        #self.rend  # Used for rendering
        self.lowflag = False # Flag set when health is =< 25% total health, will be implemented further
        self.display = gameDisplay
        # This initialization will be changed according to character stats once set up
        self.totalhealth = 100
        self.totalmana = 100
        #
        self.currenthealth = self.totalhealth
        self.currentmana = self.totalmana

        self.set_rect()
        self.createBar()

    def barText(self):
        if self.currenthealth / self.totalhealth <= .25:
            bar = "\n" + "MP: " + str(self.currentmana) + " / " + str(self.totalmana)
        else:
            bar = "HP: " + str(self.currenthealth) + " / " + str(self.totalhealth) + "\n" + "MP: " + str(self.currentmana) + " / " + str(self.totalmana)
        self.rend = self.font.render(bar, True, self.color)

    def createBar(self):
        self.barText()
        self.display.blit(self.rend, self.rect)

    def set_rect(self):
        self.barText()
        self.rect = self.rend.get_rect()
        self.rect.center = self.pos

    def updateBar(self):
        self.barText()
        # Check if we should render health as red first
        if self.currenthealth / self.totalhealth <= .25:
            healthBar = "HP: " + str(self.currenthealth) + " / " + str(self.totalhealth)
            self.display.blit(self.font.render(healthBar, True, config.red), self.rect)

        self.display.blit(self.rend, self.rect)

    def subtractHealth(self, lost):
        self.currenthealth -= lost
        self.updateBar()

    def addHealth(self, gain):
        self.currenthealth += gain
        self.updateBar()

    def subtractMana(self, lost):
        self.currentmana -= lost
        self.updateBar()

    def addMana(self, gain):
        self.currentmana += gain
        self.updateBar()





