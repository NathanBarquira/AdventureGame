import pygame
import pygame_functions
import threading
import random
import time

class Game:
    def __init__(self):

        # initialize the variables
        self.game_window = pygame.display.set_mode((1280, 720))
        self.game_background = pygame.transform.scale(pygame.image.load('map.png'), (1280, 720))
        self.projectile_count = []  # list of all projectiles on screen
        self.mob_list = []  # list of all the monsters on the screen
        self.another_shot = True
        self.box_spawn = True
        self.random_move_monster = True  # for handling random movement on monster
        self.projectile_velocity = 30
        # self.random_box() debug to test random hit

        # initialize player dimensions
        self.player_dim = (255, 255, 0)
        self.player_setup = pygame.Rect(700, 300, 80, 80)  # this handles the coordinates for the actual player
        self.bow_setup = pygame.Rect(700, 299, 50, 50)  # this handles the coordinates for the bow
        self.player_image = pygame.image.load('alex.png')
        self.player = pygame.transform.rotate(pygame.transform.scale(self.player_image, (30, 30)), 270)
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

    def handle_shooting(self, pressed_key, player):
        """ this method will handle the player's shooting"""
        # TODO: make this a timed shot
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
                        if mobs[1].colliderect(bullet[1]):
                            print('debug hit!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!', mobs[0])
                            mobs[0] -= 1
                            bullet[1].x -= 3000
                else:
                    self.projectile_count.pop(self.projectile_count.index(bullet))
            elif bullet[0] == 'N':
                print('debug recognize left shot')
                if bullet[1].y < 720 and bullet[1].y > 0:
                    print('debug bullet coordinate', bullet[1].y)
                    bullet[1].y -= self.projectile_velocity
                    for mobs in self.mob_list:
                        if mobs[1].colliderect(bullet[1]):
                            print('debug hit!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!', mobs[0])
                            mobs[0] -= 1
                            bullet[1].y -= 3000
                else:
                    self.projectile_count.pop(self.projectile_count.index(bullet))
            elif bullet[0] == 'S':
                print('debug recognize left shot')
                if bullet[1].y < 720 and bullet[1].y > 0:
                    print('debug bullet coordinate', bullet[1].y)
                    bullet[1].y += self.projectile_velocity
                    for mobs in self.mob_list:
                        if mobs[1].colliderect(bullet[1]):
                            print('debug hit!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!', mobs[0])
                            mobs[0] -= 1
                            bullet[1].y -= 3000
                else:
                    self.projectile_count.pop(self.projectile_count.index(bullet))
            elif bullet[0] == 'E':
                print('debug recognize left shot')
                if bullet[1].x < 1280 and bullet[1].x > 0:
                    print('debug bullet coordinate', bullet[1].x)
                    bullet[1].x += self.projectile_velocity
                    for mobs in self.mob_list:
                        if mobs[1].colliderect(bullet[1]):
                            print('debug hit!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!', mobs[0])
                            mobs[0] -= 1
                            bullet[1].x -= 3000
                else:
                    self.projectile_count.pop(self.projectile_count.index(bullet))


    def draw_windows(self):
        self.game_window.blit(self.player, (self.player_setup.x, self.player_setup.y))
        if len(self.projectile_count) > 0:
            for projectiles in self.projectile_count:
                pygame.draw.rect(self.game_window, (255, 0, 0), projectiles[1])

        for monsters in self.mob_list:
            if monsters[0] <= 0:
                print('debug: monster shouldve been destroyed')
                self.mob_list.pop(self.mob_list.index(monsters))
            else:
                pygame.draw.rect(self.game_window, (255, 0, 0), monsters[1])
        pygame.display.update()

    def first_sprite(self):
        """ test sprite for gif animation for shooting"""
        test_sprite = pygame_functions.makeSprite('arrow_shoot_gif.gif', 3)

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

    def random_enemy(self):
        """ spawns a random moving enemy
        currently despawns after it exits border """
        self.random_enemy_spawn = False
        for mobs in self.mob_list:
            if mobs[2] == 'rand_enemy':
                self.random_enemy_spawn = True
                if mobs[1].x > 0 and mobs[1].x < 1280 and mobs[1].y < 720 and mobs[1].y > 0:
                    # TODO: make movement more fluid

                    if self.random_move_monster:
                        self.random_move_monster = False
                        threading.Thread(target=self.random_move_time).start()

                        self.rand_walk_x = random.randint(-3, 3)
                        self.rand_walk_y = random.randint(-3, 3)
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
                break
        if not self.random_enemy_spawn:
            random_x = random.randint(0, 1000)
            random_y = random.randint(0, 720)
            random_width = random.randint(30, 60)
            random_height = random.randint(30, 60)
            random_health = random.randint(0, 5)
            self.rand_enemy = pygame.Rect(random_x, random_y, random_width, random_height)
            self.mob_list.append([random_health, self.rand_enemy, 'rand_enemy'])

    def random_move_time(self):
        time.sleep(3)
        self.random_move_monster = True


    def game_loop(self):
        self.clock = pygame.time.Clock()
        while True:
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
            self.random_enemy()

            self.window_setup()

            self.draw_windows()


if __name__ == '__main__':
    game = Game()
