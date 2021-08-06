import random
import time
import pygame
import threading

""" This pyfile handles all the types of items """


class FasterFireRate:
    """ This item makes you shoot faster """
    def __init__(self):
        """ initialize mob variables """
        self.random_x = random.randint(0, 1000)
        self.random_y = random.randint(0, 650)
        self.random_width = random.randint(30, 60)
        self.random_height = random.randint(30, 60)
        self.random_health = random.randint(1, 5)
        self.pygame_item = pygame.Rect(self.random_x, self.random_y, self.random_width, self.random_height)
        self.item_name = 'speed_boost'
        self.can_move = True
        self.mob_room_ID = 0

    def health(self):
        """ the mob's health """
        return self.random_health

    def item(self):
        """ pygame rectangle object of AI variables """
        return self.pygame_item

    def name(self):
        """ name of mob """
        return self.item_name

    def room_ID(self):
        """ id of the room the mob was spawned in """
        return self.mob_room_ID

    def hit(self, amount):
        """ lose health by this amount"""
        self.random_health -= amount

    def update_room_ID(self, room_ID):
        """ updates ID of room """
        self.mob_room_ID = room_ID

    def walk_x(self, amount):
        """ walk in x direction """
        self.random_x += amount

    def walk_y(self, amount):
        """ walk in y direction """
        self.random_y += amount

    def random_move_time(self):
        """ method for random change direction of mobs"""
        print('debug in random move time')
        time.sleep(2)
        self.can_move = True

    def hit_terrain(self):
        """ method for when mob runs into terrain """
        self.rand_walk_x = self.rand_walk_x * -1
        self.rand_walk_y = self.rand_walk_y * -1

    def kill(self):
        """ when the mob kills itself """
        self.random_health = 0

    def x(self):
        """ returns x """
        return self.pygame_item.x

    def y(self):
        """ returns y """
        return self.pygame_item.y

    def width(self):
        """ returns width """
        return self.random_width

    def height(self):
        """ returns height """
        return self.random_height