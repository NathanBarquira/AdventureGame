import pygame
import pygame_functions
import threading
import random
import time
import tkinter as tk

# TODO: maybe make bullets a class


class Game:
    def __init__(self):

        # initialize the variables
        self.game_run = True
        self.game_window = pygame.display.set_mode((1280, 720))
        self.game_background = pygame.transform.scale(pygame.image.load('map.png'), (1280, 720))
        self.projectile_count = []  # list of all projectiles on screen
        self.mob_list = []  # list of all the monsters on the screen
        self.another_shot = True
        self.box_spawn = True
        self.projectile_velocity = 30

        # loading pictures
        self.normal_picture = pygame.image.load('alex.png')
        self.hurt_picture = pygame.image.load('hurt.png')

        # initialize room variables
        self.test_room_spawn = False

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

    def handle_player_collisions(self, player):
        for mobs in self.mob_list:
            if player.colliderect(mobs.AI()):
                if not self.invincible:
                    print('DEBUG: player has been hit!!!!!!!!!!!!!!!!!')
                    self.player_health -= 1
                    self.invincible = True
                    threading.Thread(target=self.invincibility_window).start()
                    # TODO: make blinking not laggy


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
                self.projectile = pygame.Rect(player.x, player.y + player.height // 2, 10, 5)
                self.projectile_count.append(('W', self.projectile))
                self.another_shot = False
                threading.Thread(target=self.timed_shot).start()
            if pressed_key[pygame.K_UP] and player.y - 10 > 0:
                print('debug shot up')
                self.projectile = pygame.Rect(player.x, player.y + player.height // 2, 10, 5)
                self.projectile_count.append(('N', self.projectile))
                self.another_shot = False
                threading.Thread(target=self.timed_shot).start()
            if pressed_key[pygame.K_DOWN] and player.y + 10 < 700:
                print('debug shot down')
                self.projectile = pygame.Rect(player.x, player.y + player.height // 2, 10, 5)
                self.projectile_count.append(('S', self.projectile))
                self.another_shot = False
                threading.Thread(target=self.timed_shot).start()
            if pressed_key[pygame.K_RIGHT] and player.x - 10 < 1240:
                print('debug shot right')
                self.projectile = pygame.Rect(player.x, player.y + player.height // 2, 10, 5)
                self.projectile_count.append(('E', self.projectile))
                self.another_shot = False
                threading.Thread(target=self.timed_shot).start()

    def timed_shot(self):
        """ creates a time delay between shots """
        # TODO: find a good time delay
        time.sleep(1)
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

    def draw_windows(self):
        """ Draws windows for game stuff"""

        # These commands will decide if the player is dead or not
        dead_text = self.check_faint()
        if self.player_dead:
            self.game_window.blit(dead_text, (600, 360))
            pygame.display.update()
            # use tkinter for this part if possible
            self.respawn_window()
            # while self.player_dead:
            #     print('DEBUG: in player dead loop')
            #     pygame.time.delay(1)
            if self.player_dead:
                self.game_run = False
                return pygame.quit()
            elif not self.player_dead:
                print('debug should have respawned')

        # These commands will handle the health
        player_health_font = pygame.font.SysFont('comicsans', 40)
        player_health_text = player_health_font.render('Player Health: ' + str(self.player_health), True, (255, 255, 255))  # last one corresponds to white

        # drawing user health
        self.game_window.blit(player_health_text, (10, 10))

        # drawing player


        if self.invincible:
            player_image = self.hurt_picture
        else:
            player_image = self.normal_picture

        self.player = pygame.transform.rotate(pygame.transform.scale(player_image, (30, 30)), 270)
        self.game_window.blit(self.player, (self.player_setup.x, self.player_setup.y))

        if len(self.projectile_count) > 0:
            for projectiles in self.projectile_count:
                pygame.draw.rect(self.game_window, (255, 0, 0), projectiles[1])

        for monsters in self.mob_list:
            if monsters.health() <= 0:
                print('debug: monster shouldve been destroyed')
                self.mob_list.pop(self.mob_list.index(monsters))
            else:
                pygame.draw.rect(self.game_window, (255, 0, 0), monsters.AI())
        pygame.display.update()

    def first_sprite(self):
        """ test sprite for gif animation for shooting"""
        test_sprite = pygame_functions.makeSprite('arrow_shoot_gif.gif', 3)

    """ handles all tkinter stuff"""

    def board_setup(self):
        """ defines the startup variables for the GUI """
        self.master = tk.Tk()
        self.master.title("Nathan's game")
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
    def check_room_empty(self):
        """ This will check if the room is empty """
        # TODO: find a way to create a mob list for every room
        if len(self.mob_list) == 0:
            return True

    def test_room(self):
        """ This room will spawn a random amount of random monsters """
        if not self.test_room_spawn:
            self.spawn_random_enemy()
            self.spawn_random_enemy()
            self.spawn_random_enemy()
            self.test_room_spawn = True

        room_check = self.check_room_empty()
        if room_check:
            print('DEBUG: cleared all enemies')

        self.random_enemy_move()

    """ these will be the monster AI's """

    def random_box(self):
        """ spawns a random breakable box """
        # TODO: fix having multiple boxes or just one
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


        # if not self.random_enemy_spawn:
    def spawn_random_enemy(self):
        """ spawns random enemy """
        for mobs in self.mob_list:
            if mobs.name() == 'rand_enemy':
                self.random_enemy_count += 1
                break
        random_enemy = RandomEnemy()
        random_enemy.update_ID(self.random_enemy_count)
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
                pass


            self.pressed_key = pygame.key.get_pressed()
            self.handle_movement(pressed_key=self.pressed_key, player=self.player_setup)
            self.handle_shooting(pressed_key=self.pressed_key, player=self.player_setup)

            # TODO: finish handling the shooting
            self.handle_projectile_motion()

            # handle mob spawns
            # self.random_box()
            self.test_room()

            self.window_setup()

            self.draw_windows()

            self.handle_player_collisions(self.player_setup)


class RandomEnemy:
    def __init__(self):
        self.random_x = random.randint(0, 1000)
        self.random_y = random.randint(0, 720)
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

    def rand_walk_x(self, amount):
        """ walk in x direction """
        self.random_x += amount

    def rand_walk_y(self, amount):
        """ walk in y direction """
        self.random_y += amount

    def change_direction(self):
        """ Changes direction for random walk """
        # TODO: try to make load time faster if possible
        if self.pygame_AI.x > 0 and self.pygame_AI.x < 1240 and self.pygame_AI.y < 650 and self.pygame_AI.y > 0:
            if self.can_move:
                threading.Thread(target=self.random_move_time()).start()
                self.rand_walk_x = random.choice([-5, 0, 5])  # this accounts for diagonal and straight movements
                self.rand_walk_y = random.choice([-5, 0, 5])
                self.can_move = False
                self.pygame_AI.x += self.rand_walk_x
                self.pygame_AI.y += self.rand_walk_y
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
        time.sleep(2)
        self.can_move = True


if __name__ == '__main__':
    game = Game()
