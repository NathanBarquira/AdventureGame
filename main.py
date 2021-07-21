import pygame
import pygame_functions
import threading
import random
import time
import tkinter as tk
import MobClasses
import TerrainClasses

# TODO: maybe make bullets a class


class Game:
    def __init__(self):

        # initialize the variables
        self.game_run = True
        self.game_window = pygame.display.set_mode((1280, 720))
        self.game_background = pygame.transform.scale(pygame.image.load('map.png'), (1280, 720))
        self.projectile_count = []  # list of all projectiles on screen
        self.mob_list = []  # list of all the monsters on the screen
        self.door_list = []  # list of all doors in the room
        self.another_shot = True
        self.box_spawn = True
        self.projectile_velocity = 30
        self.game_height = 720
        self.game_width = 1280

        # initialize colors
        self.shadow = (192, 192, 192)
        self.white = (255, 255, 255)
        self.light_green = (0, 255, 0)
        self.green = (0, 200, 0)
        self.blue = (0, 0, 128)
        self.light_blue = (0, 0, 255)
        self.red = (200, 0, 0)
        self.light_red = (255, 100, 100)
        self.purple = (102, 0, 102)
        self.light_purple = (153, 0, 153)

        # loading pictures
        self.normal_picture = pygame.image.load('main.png')
        self.hurt_picture = pygame.image.load('hurt.png')
        self.rock_image = pygame.image.load('rock.png')
        self.random_monster_image = pygame.image.load('random_monster.png')

        # initialize room variables
        self.test_room_spawn = False
        self.door_closed = True
        self.random_room_spawn = False
        self.terrain_list = []  # handles all the terrain in a room

        # initialize player variables
        self.player_health = 3
        self.player_dead = False
        self.invincible = False

        # initialize monster variables
        self.random_enemy_count = 1
        self.random_move_monster = True  # for handling random movement on monster

        # initialize player dimensions
        self.player_dim = (255, 255, 0)
        self.player_setup = pygame.Rect(700, 300, 30, 30)  # this handles the coordinates for the actual player
        self.bow_setup = pygame.Rect(700, 299, 50, 50)  # this handles the coordinates for the bow
        self.game_loop()

    def window_setup(self):
        self.game_window.blit(self.game_background, (0, 0))
        # pygame.display.update()

    def handle_movement(self, pressed_key, player):
        if pressed_key[pygame.K_a] and player.x - 10 > 0:
            player.x -= 10
        if pressed_key[pygame.K_w] and player.y - 10 > 0:
            player.y -= 10
        if pressed_key[pygame.K_s] and player.y + 10 < 700:
            player.y += 10
        if pressed_key[pygame.K_d] and player.x - 10 < 1240:
            player.x += 10

    def handle_player_collisions(self, pressed_key, player):
        for mobs in self.mob_list:
            if player.colliderect(mobs.AI()):
                if not self.invincible:
                    print('DEBUG: player has been hit!!!!!!!!!!!!!!!!!')
                    self.player_health -= 1
                    self.invincible = True
                    threading.Thread(target=self.invincibility_window).start()

        for terrain in self.terrain_list:
            if player.colliderect(terrain.terrain()):
                print('DEBUG: ran into a rock!')
                if pressed_key[pygame.K_a] and player.x - 10 > 0:
                    player.x += 10
                if pressed_key[pygame.K_w] and player.y - 10 > 0:
                    player.y += 10
                if pressed_key[pygame.K_s] and player.y + 10 < 700:
                    player.y -= 10
                if pressed_key[pygame.K_d] and player.x - 10 < 1240:
                    player.x -= 10
    
    def invincibility_window(self):
        """ handles invincibility after getting hit """
        time.sleep(3)
        self.invincible = False

    def handle_shooting(self, pressed_key, player):
        """ this method will handle the player's shooting"""
        if self.another_shot:
            print('amount of projectiles on map:', len(self.projectile_count))
            if pressed_key[pygame.K_LEFT] and player.x - 10 > 0:
                print('debug shot left')
                self.projectile = pygame.Rect(player.x + player.width // 2, player.y + player.height // 2 - 4, 10, 10)
                self.projectile_count.append(('W', self.projectile))
                self.another_shot = False
                threading.Thread(target=self.timed_shot).start()
            if pressed_key[pygame.K_UP] and player.y - 10 > 0:
                print('debug shot up')
                self.projectile = pygame.Rect(player.x + player.width // 2 - 4, player.y + player.height // 2, 10, 10)
                self.projectile_count.append(('N', self.projectile))
                self.another_shot = False
                threading.Thread(target=self.timed_shot).start()
            if pressed_key[pygame.K_DOWN] and player.y + 10 < 700:
                print('debug shot down')
                self.projectile = pygame.Rect(player.x + player.width // 2 - 4, player.y + player.height // 2, 10, 10)
                self.projectile_count.append(('S', self.projectile))
                self.another_shot = False
                threading.Thread(target=self.timed_shot).start()
            if pressed_key[pygame.K_RIGHT] and player.x - 10 < 1240:
                print('debug shot right')
                self.projectile = pygame.Rect(player.x + player.width // 2, player.y + player.height // 2 - 4, 10, 10)
                self.projectile_count.append(('E', self.projectile))
                self.another_shot = False
                threading.Thread(target=self.timed_shot).start()

    def timed_shot(self):
        """ creates a time delay between shots """
        # TODO: find a good time delay
        time.sleep(0.1)
        self.another_shot = True

    def handle_projectile_motion(self, direction=None):
        """ handle projectile motion """
        for bullet in self.projectile_count:
            if bullet[0] == 'W':
                print('debug recognize left shot')
                if bullet[1].x < 1280 and bullet[1].x > 0:
                    print('debug bullet coordinate', bullet[1].x)
                    bullet[1].x -= self.projectile_velocity
                    for mobs in self.mob_list:
                        if mobs.AI().colliderect(bullet[1]):
                            print('debug hit!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!', mobs.health())
                            mobs.hit(1)
                            bullet[1].x -= 3000
                    for terrain in self.terrain_list:
                        if terrain.terrain().colliderect(bullet[1]):
                            bullet[1].x -= 3000
                else:
                    self.projectile_count.pop(self.projectile_count.index(bullet))
            elif bullet[0] == 'N':
                print('debug recognize upper shot')
                if bullet[1].y < 720 and bullet[1].y > 0:
                    print('debug bullet coordinate', bullet[1].y)
                    bullet[1].y -= self.projectile_velocity
                    for mobs in self.mob_list:
                        if mobs.AI().colliderect(bullet[1]):
                            print('debug hit!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!', mobs.health())
                            mobs.hit(1)
                            bullet[1].y -= 3000
                    for terrain in self.terrain_list:
                        if terrain.terrain().colliderect(bullet[1]):
                            bullet[1].x -= 3000
                else:
                    self.projectile_count.pop(self.projectile_count.index(bullet))
            elif bullet[0] == 'S':
                print('debug recognize down shot')
                if bullet[1].y < 720 and bullet[1].y > 0:
                    print('debug bullet coordinate', bullet[1].y)
                    bullet[1].y += self.projectile_velocity
                    for mobs in self.mob_list:
                        if mobs.AI().colliderect(bullet[1]):
                            print('debug hit!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!', mobs.health())
                            mobs.hit(1)
                            bullet[1].y -= 3000
                    for terrain in self.terrain_list:
                        if terrain.terrain().colliderect(bullet[1]):
                            bullet[1].x -= 3000
                else:
                    self.projectile_count.pop(self.projectile_count.index(bullet))
            elif bullet[0] == 'E':
                print('debug recognize right shot')
                if bullet[1].x < 1280 and bullet[1].x > 0:
                    print('debug bullet coordinate', bullet[1].x)
                    bullet[1].x += self.projectile_velocity
                    for mobs in self.mob_list:
                        if mobs.AI().colliderect(bullet[1]):
                            print('debug hit!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!', mobs.health())
                            mobs.hit(1)
                            bullet[1].x -= 3000
                    for terrain in self.terrain_list:
                        if terrain.terrain().colliderect(bullet[1]):
                            bullet[1].x -= 3000
                else:
                    self.projectile_count.pop(self.projectile_count.index(bullet))

    def check_faint(self):
        """ this method checks to see if you are dead or not by seeing if your health is less than or equal to zero"""
        # TODO: maybe add some game stats?
        if self.player_health <= 0:
            print('DEBUG player is dead!')
            dead_font = pygame.font.SysFont('comicsans', 40)
            dead_text = dead_font.render('You died', True, (255, 255, 255))
            self.player_dead = True
            return dead_text

    def reset_all(self):
        """ should reset all rooms and stuff """
        print('DEBUG: should have reset all')
        self.test_room_spawn = False
        self.random_room_spawn = False

    def draw_windows(self):
        """ Draws windows for game stuff"""

        # These commands will decide if the player is dead or not
        dead_text = self.check_faint()
        if self.player_dead:
            self.game_window.blit(dead_text, (600, 360))
            pygame.display.update()
            self.respawn_window()
            # while self.player_dead:
            #     print('DEBUG: in player dead loop')
            #     pygame.time.delay(1)
            if self.player_dead:
                self.game_run = False
                return pygame.quit()
            elif not self.player_dead:
                print('debug should have respawned')
                self.reset_all()

        # These commands will handle the health
        player_health_font = pygame.font.SysFont('comicsans', 40)
        player_health_text = player_health_font.render('Player Health: ' + str(self.player_health), True, (255, 255, 255))  # last one corresponds to white

        # drawing user health
        self.game_window.blit(player_health_text, (10, 10))

        # drawing doors
        for doors in self.door_list:
            pygame.draw.rect(self.game_window, self.light_green, doors)

        # drawing player invincibility
        if self.invincible:
            player_image = self.hurt_picture
        else:
            player_image = self.normal_picture

        # drawing player
        self.player = pygame.transform.rotate(pygame.transform.scale(player_image, (30, 30)), 0)
        self.game_window.blit(self.player, (self.player_setup.x, self.player_setup.y))

        # drawing monsters
        for mobs in self.mob_list:
            mob_rect = pygame.transform.rotate(pygame.transform.scale(self.random_monster_image, (mobs.width(), mobs.height())), 0)
            self.game_window.blit(mob_rect, (mobs.x(), mobs.y()))

        # drawing terrain
        for terrain in self.terrain_list:
            # pygame.draw.rect(self.game_window, self.white, terrain.terrain())

            rock_rect = pygame.transform.rotate(pygame.transform.scale(self.rock_image, (terrain.width(), terrain.height())), 0)
            self.game_window.blit(rock_rect, (terrain.x(), terrain.y()))

        # drawing projectiles
        if len(self.projectile_count) > 0:
            for projectiles in self.projectile_count:
                pygame.draw.rect(self.game_window, self.light_red, projectiles[1])

        # destroying monster if it has zero health
        for monsters in self.mob_list:
            if monsters.health() <= 0:
                print('debug: monster shouldve been destroyed')
                self.mob_list.pop(self.mob_list.index(monsters))
            else:
                pygame.draw.rect(self.game_window, (255, 0, 0), monsters.AI())

        # the only display update that should be in the loop
        pygame.display.update()

    def first_sprite(self):
        """ test sprite for gif animation for shooting"""
        test_sprite = pygame_functions.makeSprite('arrow_shoot_gif.gif', 3)

    """ handles all tkinter stuff"""

    def board_setup(self):
        """ defines the startup variables for the GUI """
        self.master = tk.Tk()
        self.master.title("Nathan's Game")
        self.master.geometry('+{}+{}'.format(700, 300))
        self.master.resizable(0, 0)

    def runUI(self):
        """ starts game loop """
        self.master.mainloop()

    def respawn_window(self):
        """ makes the window for respawning when you die """
        self.board_setup()
        respawn_label = tk.Label(self.master, text='Do you want to play again?')
        yes_button = tk.Button(self.master, command=self.respawn_yes, text='Yes')
        no_button = tk.Button(self.master, command=self.respawn_no, text='No')
        respawn_label.grid(columnspan=2, row=0)
        yes_button.grid(row=1, column=0)
        no_button.grid(row=1, column=1)
        self.runUI()

    def respawn_yes(self):
        """ if person chooses yes in respawn window """
        # TODO: finish resetting game
        print('debug: person chose yes')
        self.player_dead = False
        self.player_health = 3
        self.invincible = False
        self.master.destroy()
        self.mob_list.clear()

    def respawn_no(self):
        """ if person chooses no in respawn window """
        print('debug: person chose no')
        self.master.destroy()

    """ These will handle all the rooms """
    def open_doors(self):
        """ this will open doors, usually wanna use if room is cleared """
        # TODO: def work on this method
        pass

    def set_door(self):
        """ test method, sets a specific door down """
        set_door = pygame.Rect(self.game_width // 2, 0, 30, 30)
        self.door_list.append(set_door)
        self.door_closed = False
        return set_door

    def handle_doors(self, pressed_key):
        """ handles going through doors """
        for doors in self.door_list:
            if self.player_setup.colliderect(doors):
                if pressed_key[pygame.K_w]:
                    print('DEBUG: went through door')
                    self.clear_doors()
                    self.player_setup.y = 700
                    # TODO: make it so all rooms become false maybe
                    self.test_room_spawn = False
                    self.random_room_spawn = False
                    self.random_room()  # this one! changes
                    self.door_closed = True

    def clear_doors(self):
        """ clears all doors in the map"""
        # TODO: make doors correspond to certain map!
        self.door_list.clear()

    def check_room_empty(self):
        """ This will check if the room is empty """
        # TODO: find a way to create a mob list for every room
        if len(self.mob_list) == 0:
            return True

    def clear_terrain(self):
        """ this will clear all terrain in the room """
        self.terrain_list.clear()

    def test_room(self):
        """ This room will spawn a random amount of random monsters """
        # TODO: maybe make a list of rooms with boolean of open door
        if not self.test_room_spawn:
            self.spawn_random_enemy()
            self.spawn_random_enemy()
            self.spawn_random_enemy()
            self.test_room_spawn = True

        # checks if room is empty
        room_check = self.check_room_empty()
        if room_check:
            print('DEBUG: cleared all enemies')
            if self.door_closed:
                self.set_door()
            else:
                print('DEBUG: shouldve set door')
        self.random_enemy_move()

    def random_room(self):
        """ This room will have a random amount of enemies (TEST) """
        if not self.random_room_spawn:
            self.terrain_list.clear()
            print('debug should be terrain list:', self.terrain_list)

            # spawns random amount of enemies and rocks
            random_amount = random.randint(1, 4)
            random_rock_amount = random.randint(5, 10)
            for _ in range(random_rock_amount):
                self.spawn_rock()
            for _ in range(random_amount):
                self.spawn_random_enemy()
            self.random_room_spawn = True

        # checks if room is empty
        room_check = self.check_room_empty()
        if room_check:
            print('DEBUG: cleared all enemies')
            if self.door_closed:
                self.set_door()
            else:
                print('DEBUG: shouldve set door')
        self.random_enemy_move()

    """ miscellaneous room stuff """
    def spawn_rock(self):
        """ This will spawn a rock that you cannot pass """
        random_rock = TerrainClasses.RandomTerrain()

        # this should fix the player from spawning into a rock and not being able to move
        if random_rock.terrain().colliderect(self.player_setup):
            return self.spawn_rock()

        self.terrain_list.append(random_rock)

    def handle_enemy_collisions(self):
        """ This will handle when enemy runs into rock """
        for mobs in self.mob_list:
            for terrain in self.terrain_list:
                if mobs.AI().colliderect(terrain.terrain()):
                    mobs.hit_terrain()

    """ these will be the monster AI's """

    def random_box(self):
        """ spawns a random breakable box """
        self.box_spawn = False
        for mobs in self.mob_list:
            if mobs[2] == 'box':
                self.box_spawn = True
                break
        if not self.box_spawn:
            self.box = pygame.Rect(random.randint(0, 1100), random.randint(0, 720), 80, 80)
            self.mob_list.append([3, self.box, 'box'])

    def random_enemy_infinite(self):
        """ spawns a random moving enemy
        currently despawns after it exits border """
        self.random_enemy_spawn = False
        for mobs in self.mob_list:
            if mobs.name() == 'rand_enemy':
                self.random_enemy_spawn = True
                if mobs[1].x > 0 and mobs[1].x < 1280 and mobs[1].y < 720 and mobs[1].y > 0:

                    if self.random_move_monster:
                        self.random_move_monster = False
                        threading.Thread(target=self.random_move_time).start()

                        self.rand_walk_x = random.choice(
                            [-5, 0, 5])  # this accounts for diagonal and straight movements
                        self.rand_walk_y = random.choice([-5, 0, 5])
                        mobs[1].x += self.rand_walk_x
                        mobs[1].y += self.rand_walk_y
                    else:
                        mobs[1].x += self.rand_walk_x
                        mobs[1].y += self.rand_walk_y
                else:
                    self.rand_walk_x = self.rand_walk_x * -1
                    self.rand_walk_y = self.rand_walk_y * -1
                    mobs[1].x += self.rand_walk_x
                    mobs[1].y += self.rand_walk_y

        if not self.random_enemy_spawn:
            random_x = random.randint(0, 1000)
            random_y = random.randint(0, 720)
            random_width = random.randint(30, 60)
            random_height = random.randint(30, 60)
            random_health = random.randint(0, 5)
            self.rand_enemy = pygame.Rect(random_x, random_y, random_width, random_height)
            self.mob_list.append([random_health, self.rand_enemy, 'rand_enemy'])

    def random_enemy_move(self):
        """ handles movement of random enemy """
        for mobs in self.mob_list:
            print('debug: mob list', self.mob_list)
            print(mobs.name(), mobs.ID())
            if mobs.name() == 'rand_enemy':
                mobs.change_direction()

    def spawn_random_enemy(self):
        """ spawns random enemy """
        for mobs in self.mob_list:
            if mobs.name() == 'rand_enemy':
                self.random_enemy_count += 1
                break
        random_enemy = MobClasses.RandomEnemy()
        random_enemy.update_ID(self.random_enemy_count)
        for terrain in self.terrain_list:
            if random_enemy.AI().colliderect(terrain.terrain()):
                print('DEBUG: collided')
                return self.spawn_random_enemy()
        self.mob_list.append(random_enemy)

    def random_move_time(self):
        """ method for random change direction of mobs"""
        time.sleep(2)
        self.random_move_monster = True

    def game_loop(self):
        """ where the actual game loop takes place"""
        self.clock = pygame.time.Clock()
        while self.game_run:
            self.clock.tick(30)
            for event in pygame.event.get():
                # TODO: finish event handling
                pass

            self.pressed_key = pygame.key.get_pressed()
            self.handle_movement(pressed_key=self.pressed_key, player=self.player_setup)
            self.handle_shooting(pressed_key=self.pressed_key, player=self.player_setup)

            # TODO: finish handling the shooting
            self.handle_projectile_motion()
            self.handle_doors(pressed_key=self.pressed_key)

            # handle mob spawns
            # self.random_box()
            self.random_room()

            self.window_setup()

            # self.draw_windows()
            # TODO: see if you should have draw windows before or after handle player collisions

            # handles all collisions
            self.handle_player_collisions(pressed_key=self.pressed_key, player=self.player_setup)
            self.handle_enemy_collisions()

            # draws windows
            self.draw_windows()


if __name__ == '__main__':
    game = Game()
