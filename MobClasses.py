import random
import time
import pygame
import threading

""" This pyfile handles all the types of enemies """


class RandomEnemy:
    def __init__(self):
        """ initialize mob variables """
        self.random_x = random.randint(0, 1000)
        self.random_y = random.randint(0, 650)
        self.random_width = random.randint(30, 60)
        self.random_height = random.randint(30, 60)
        self.random_health = random.randint(1, 5)
        self.pygame_AI = pygame.Rect(self.random_x, self.random_y, self.random_width, self.random_height)
        self.mob_name = 'rand_enemy'
        self.random_enemy_count = 0
        self.can_move = True

    def health(self):
        """ the mob's health """
        return self.random_health

    def AI(self):
        """ pygame rectangle object of AI variables """
        return self.pygame_AI

    def name(self):
        """ name of mob """
        return self.mob_name

    def ID(self):
        """ id of how many of this mob are in the level """
        return self.random_enemy_count

    def hit(self, amount):
        """ lose health by this amount"""
        self.random_health -= amount

    def update_ID(self, ID):
        """ updates ID of mob """
        self.random_enemy_count += ID

    def walk_x(self, amount):
        """ walk in x direction """
        self.random_x += amount

    def walk_y(self, amount):
        """ walk in y direction """
        self.random_y += amount

    def change_direction(self):
        """ Changes direction for random walk """
        if self.pygame_AI.x > 0 and self.pygame_AI.x < 1240 and self.pygame_AI.y < 650 and self.pygame_AI.y > 0:
            print('DEBUG:', self.can_move)
            if self.can_move:
                threading.Thread(target=self.random_move_time).start()
                self.rand_walk_x = random.choice([-5, 0, 5])  # this accounts for diagonal and straight movements
                self.rand_walk_y = random.choice([-5, 0, 5])
                self.pygame_AI.x += self.rand_walk_x
                self.pygame_AI.y += self.rand_walk_y
                self.can_move = False
            else:
                self.pygame_AI.x += self.rand_walk_x
                self.pygame_AI.y += self.rand_walk_y
        else:
            self.rand_walk_x = self.rand_walk_x * -1
            self.rand_walk_y = self.rand_walk_y * -1
            self.pygame_AI.x += self.rand_walk_x
            self.pygame_AI.y += self.rand_walk_y

    def random_move_time(self):
        """ method for random change direction of mobs"""
        print('debug in random move time')
        time.sleep(2)
        self.can_move = True
