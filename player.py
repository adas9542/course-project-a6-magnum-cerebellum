from character import Character
from items import Item
from config import * 
from map import collision_walls
import math
import config
import os 
import json

# import testing_delete

class Player():
    old_pos = player_pos
    def __init__(self, character):
        f = open(os.path.join("data/character_data.json"))
        data = json.load(f)

        self.character_data = data[character.__str__()]

        self.x, self.y = player_pos
        self.angle = player_angle
        #self.health = 10
        self.hp = 100
        self.character = character

        #Initialize this to the starting item stats?? I guess IDK
        self.attack = 0
        self.defense = 0

        self.actions = self.character_data["actions"]
        self.startingItems = self.character_data["items"] #Just strings, need to cast to Item

         # collision parameters
        self.side = 50
        self.rect = pygame.Rect(*player_pos, self.side, self.side)
        self.collision_list = collision_walls 


    @property
    def pos(self):
        return (self.x, self.y)

    # return False if decrease kills player, true otherwise. Update player hp with decreased ammount
    def decrease_hp(self, n):
        if (self.hp - n) <= 0:
            self.hp = 0
            return False
        else:
            self.hp = self.hp - n
            return True

    def add_item(self, item):
        new_item = Item(item)

    def draw(self):
        pass

  #  def __str__(self):
   #     return "player of " + self.character.type
    def detect_collision(self, dx, dy):
        next_rect = self.rect.copy()
        next_rect.move_ip(dx, dy)
        hit_indexes = next_rect.collidelistall(self.collision_list)

        if len(hit_indexes):
            delta_x, delta_y = 0, 0
            for hit_index in hit_indexes:
                hit_rect = self.collision_list[hit_index]
                if dx > 0:
                    delta_x += next_rect.right - hit_rect.left
                else:
                    delta_x += hit_rect.right - next_rect.left
                if dy > 0:
                    delta_y += next_rect.bottom - hit_rect.top
                else:
                    delta_y += hit_rect.bottom - next_rect.top

            if abs(delta_x - delta_y) < 10:
                dx, dy = 0, 0
            elif delta_x > delta_y:
                dy = 0
            elif delta_y > delta_x:
                dx = 0
        self.x += dx
        self.y += dy
        
    def movement(self):
        self.keys_control()
        self.rect.center = self.x, self.y
        self.angle %= DOUBLE_PI

    def keys_control(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            exit()

        if keys[pygame.K_UP]:
            dx = player_speed * cos_a
            dy = player_speed * sin_a
            self.detect_collision(dx, dy)
        if keys[pygame.K_DOWN]:
            dx = -player_speed * cos_a
            dy = -player_speed * sin_a
            self.detect_collision(dx, dy)
        if keys[pygame.K_a]:
            dx = player_speed * sin_a
            dy = -player_speed * cos_a
            self.detect_collision(dx, dy)
        if keys[pygame.K_d]:
            dx = -player_speed * sin_a
            dy = player_speed * cos_a
            self.detect_collision(dx, dy)

        if keys[pygame.K_LEFT]:
            self.angle -= 0.02
        if keys[pygame.K_RIGHT]:
            self.angle += 0.02

        if keys[pygame.K_UP] == False and keys[pygame.K_DOWN] == False: #and keys[pygame.K_LEFT] == False and keys[pygame.K_RIGHT] == False:
            if self.pos != self.old_pos:
                self.old_pos = self.pos
                printtuple = tuple(int(num) for num in self.pos)
                # print(printtuple)
                config.text1.append(printtuple)

                # testing_delete.text1.append(printtuple)



