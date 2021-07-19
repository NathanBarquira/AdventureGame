import random
import time
import pygame
import threading

""" This pyfile handles all the types of terrain """


class RandomTerrain:
    def __init__(self):
        """ initializes terrain variables """
        self.random_x = random.randint(30, 1000)
        self.random_y = random.randint(30, 650)
        self.random_width = random.randint(30, 60)
        self.random_height = random.randint(30, 60)
        self.random_health = random.randint(1, 5)
        self.mob_name = 'terrain'
        self.random_enemy_count = 0
        self.can_move = True
        self.pygame_terrain = pygame.Rect(self.random_x, self.random_y, self.random_width, self.random_height)

    def terrain(self):
        """ Terrain """
        return self.pygame_terrain

    def x(self):
        """ returns x """
        return self.random_x

    def y(self):
        """ returns y """
        return self.random_y

    def width(self):
        """ returns width """
        return self.random_width

    def height(self):
        """ returns height """
        return self.random_height




