import random
import time
import pygame
import threading
import math

""" This pyfile handles all the types of enemies """


class RandomEnemy:
    """ This enemy just moves randomly """
    def __init__(self):
        """ initialize mob variables """
        self.rand_vel_x = 1
        self.rand_vel_y = 1
        self.random_x = random.randint(0, 1000)
        self.random_y = random.randint(0, 650)
        self.random_width = random.randint(30, 60)
        self.random_height = random.randint(30, 60)
        self.random_health = random.randint(1, 5)
        self.pygame_AI = pygame.Rect(self.random_x, self.random_y, self.random_width, self.random_height)
        self.mob_name = 'rand_enemy'
        self.random_enemy_count = 0
        self.can_move = True
        self.mob_room_ID = 0

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

    def room_ID(self):
        """ id of the room the mob was spawned in """
        return self.mob_room_ID

    def hit(self, amount):
        """ lose health by this amount"""
        self.random_health -= amount

    def update_ID(self, ID):
        """ updates ID of mob """
        self.random_enemy_count += ID

    def update_room_ID(self, room_ID):
        """ updates ID of room """
        self.mob_room_ID = room_ID

    def walk_x(self, amount):
        """ walk in x direction """
        self.random_x += amount

    def walk_y(self, amount):
        """ walk in y direction """
        self.random_y += amount

    def change_direction(self):
        """ Changes direction for random walk """
        if self.pygame_AI.x > 0 and self.pygame_AI.x < 1200 and self.pygame_AI.y < 650 and self.pygame_AI.y > 0:
            print('DEBUG:', self.can_move)
            if self.can_move:
                threading.Thread(target=self.random_move_time).start()
                self.rand_walk_x = random.choice([-5, 0, 5])  # this accounts for diagonal and straight movements
                self.rand_walk_y = random.choice([-5, 0, 5])
                self.rand_vel_x = random.choice([1, 2, 3])
                self.rand_vel_y = random.choice([1, 2, 3])
                self.pygame_AI.x += self.rand_walk_x * self.rand_vel_x
                self.pygame_AI.y += self.rand_walk_y * self.rand_vel_y
                self.can_move = False
            else:
                self.pygame_AI.x += self.rand_walk_x * self.rand_vel_x
                self.pygame_AI.y += self.rand_walk_y * self.rand_vel_y
        else:
            self.hit_terrain()
            self.pygame_AI.x += self.rand_walk_x * self.rand_vel_x
            self.pygame_AI.y += self.rand_walk_y * self.rand_vel_y

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
        return self.pygame_AI.x

    def y(self):
        """ returns y """
        return self.pygame_AI.y

    def width(self):
        """ returns width """
        return self.random_width

    def height(self):
        """ returns height """
        return self.random_height


class FollowEnemy:
    """ This enemy chases the player"""

    def __init__(self, player):
        """ initialize mob variables """
        speed = random.randint(2, 3)
        self.rand_vel_x = speed
        self.rand_vel_y = speed
        self.random_x = random.randint(0, 1000)
        self.random_y = random.randint(0, 650)
        self.random_width = random.randint(30, 60)
        self.random_height = random.randint(30, 60)
        self.random_health = random.randint(1, 5)
        self.pygame_AI = pygame.Rect(self.random_x, self.random_y, self.random_width, self.random_height)
        self.mob_name = 'follow_enemy'
        self.random_enemy_count = 0
        self.can_move = True
        self.mob_room_ID = 0

        self.player = player  # holds player info

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

    def room_ID(self):
        """ id of the room the mob was spawned in """
        return self.mob_room_ID

    def hit(self, amount):
        """ lose health by this amount"""
        self.random_health -= amount

    def update_ID(self, ID):
        """ updates ID of mob """
        self.random_enemy_count += ID

    def update_room_ID(self, room_ID):
        """ updates ID of room """
        self.mob_room_ID = room_ID

    def walk_x(self, amount):
        """ walk in x direction """
        self.random_x += amount

    def walk_y(self, amount):
        """ walk in y direction """
        self.random_y += amount

    def change_direction(self):
        """ Changes direction for random walk """
        if self.pygame_AI.x > 0 and self.pygame_AI.x < 1200 and self.pygame_AI.y < 650 and self.pygame_AI.y > 0:
            print('DEBUG:', self.can_move)
            angle = math.atan2(self.pygame_AI.y - self.player.y, self.pygame_AI.x - self.player.x)
            self.rand_walk_x = math.cos(angle) * -2.5
            self.rand_walk_y = math.sin(angle) * -2.5
            self.pygame_AI.x += self.rand_walk_x * self.rand_vel_x
            self.pygame_AI.y += self.rand_walk_y * self.rand_vel_y
        else:
            self.hit_terrain()
            self.pygame_AI.x += self.rand_walk_x * self.rand_vel_x
            self.pygame_AI.y += self.rand_walk_y * self.rand_vel_y

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
        return self.pygame_AI.x

    def y(self):
        """ returns y """
        return self.pygame_AI.y

    def width(self):
        """ returns width """
        return self.random_width

    def height(self):
        """ returns height """
        return self.random_height

class OrthogonalRandom:
    """ This enemy moves orthogonally, but it chooses its next move using the grand-schmidt process """
    def __init__(self):
        """ initialize mob variables """
        random_angle = random.randint(0, 314) / 100  # this accounts for diagonal and straight movements
        self.rand_walk_x = math.cos(random_angle)
        self.rand_walk_y = math.sin(random_angle)
        self.rand_vel_x = 10
        self.rand_vel_y = 10
        self.random_x = random.randint(0, 1000)
        self.random_y = random.randint(0, 650)
        self.random_width = random.randint(30, 60)
        self.random_height = random.randint(30, 60)
        self.random_health = random.randint(1, 5)
        self.pygame_AI = pygame.Rect(self.random_x, self.random_y, self.random_width, self.random_height)
        self.mob_name = 'gsp_enemy'
        self.random_enemy_count = 0
        self.can_move = True
        self.mob_room_ID = 0

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

    def room_ID(self):
        """ id of the room the mob was spawned in """
        return self.mob_room_ID

    def hit(self, amount):
        """ lose health by this amount"""
        self.random_health -= amount

    def update_ID(self, ID):
        """ updates ID of mob """
        self.random_enemy_count += ID

    def update_room_ID(self, room_ID):
        """ updates ID of room """
        self.mob_room_ID = room_ID

    def walk_x(self, amount):
        """ walk in x direction """
        self.random_x += amount

    def walk_y(self, amount):
        """ walk in y direction """
        self.random_y += amount

    def change_direction(self):
        """ Changes direction for random walk """
        if self.pygame_AI.x > 0 and self.pygame_AI.x < 1200 and self.pygame_AI.y < 650 and self.pygame_AI.y > 0:
            print('DEBUG:', self.can_move)
            if self.can_move:
                threading.Thread(target=self.random_move_time).start()

                # grand-schmidt-process:
                vector = (self.rand_walk_x, self.rand_walk_y)

                random_new_angle = random.randint(0, 314) / 100  # this accounts for diagonal and straight movements
                new_vector = (math.cos(random_new_angle), math.sin(random_new_angle))
                inner_product = vector[0] * new_vector[0] + vector[1] + new_vector[1]
                norm_squared = vector[0]**2 + vector[1]**2
                process_coefficient = inner_product / norm_squared
                orthogonal_vector = (new_vector[0] - process_coefficient * vector[0], new_vector[1] - process_coefficient * vector[1])
                orthogonal_norm = (orthogonal_vector[0]**2 + orthogonal_vector[1]**2) ** (1/2)
                final_vector = (orthogonal_vector[0] * orthogonal_norm, orthogonal_vector[1] * orthogonal_norm)
                self.rand_walk_x = final_vector[0]
                self.rand_walk_y = final_vector[1]


                self.pygame_AI.x += self.rand_walk_x * self.rand_vel_x
                self.pygame_AI.y += self.rand_walk_y * self.rand_vel_y
                self.can_move = False
            else:
                self.pygame_AI.x += self.rand_walk_x * self.rand_vel_x
                self.pygame_AI.y += self.rand_walk_y * self.rand_vel_y
        else:
            self.hit_terrain()
            self.pygame_AI.x += self.rand_walk_x * self.rand_vel_x
            self.pygame_AI.y += self.rand_walk_y * self.rand_vel_y

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
        return self.pygame_AI.x

    def y(self):
        """ returns y """
        return self.pygame_AI.y

    def width(self):
        """ returns width """
        return self.random_width

    def height(self):
        """ returns height """
        return self.random_height



if __name__ == '__main__':
    test = RandomEnemy()
    print(test.x())