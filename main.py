import pygame
import pygame_functions

class Game:
    def __init__(self):

        # initialize the variables
        self.game_window = pygame.display.set_mode((1280, 720))
        self.game_background = pygame.transform.scale(pygame.image.load('map.png'), (1280, 720))
        self.projectile_count = []

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
        # TODO: add projectile later
        if pressed_key[pygame.K_LEFT] and player.x - 10 > 0:
            print('debug shot left')
            self.projectile = pygame.Rect(player.x, player.y + player.height // 2, 10, 5)
            self.projectile_count.append(('W', self.projectile))
        if pressed_key[pygame.K_UP] and player.y - 10 > 0:
            print('debug shot up')
            self.projectile = pygame.Rect(player.x, player.y + player.height // 2, 10, 5)
            self.projectile_count.append(('N', self.projectile))
        if pressed_key[pygame.K_DOWN] and player.y + 10 < 700:
            print('debug shot down')
            self.projectile = pygame.Rect(player.x, player.y + player.height // 2, 10, 5)
            self.projectile_count.append(('S', self.projectile))
        if pressed_key[pygame.K_RIGHT] and player.x - 10 < 1240:
            print('debug shot right')
            self.projectile = pygame.Rect(player.x, player.y + player.height // 2, 10, 5)
            self.projectile_count.append(('E', self.projectile))

    def handle_projectile_motion(self, direction=None):
        """ handle projectile motion """
        # if direction == 'NE':
        for bullet in self.projectile_count:
            if bullet[0] == 'W':
                print('debug recognize left shot')
                if bullet[1].x < 1280 and bullet[1].x > 0:
                    print('debug bullet coordinate', bullet[1].x)
                    bullet[1].x -= 15
                else:
                    self.projectile_count.pop(self.projectile_count.index(bullet))
            elif bullet[0] == 'N':
                print('debug recognize left shot')
                if bullet[1].y < 720 and bullet[1].y > 0:
                    print('debug bullet coordinate', bullet[1].y)
                    bullet[1].y -= 15
                else:
                    self.projectile_count.pop(self.projectile_count.index(bullet))
            elif bullet[0] == 'S':
                print('debug recognize left shot')
                if bullet[1].y < 720 and bullet[1].y > 0:
                    print('debug bullet coordinate', bullet[1].y)
                    bullet[1].y += 15
                else:
                    self.projectile_count.pop(self.projectile_count.index(bullet))
            elif bullet[0] == 'E':
                print('debug recognize left shot')
                if bullet[1].x < 1280 and bullet[1].x > 0:
                    print('debug bullet coordinate', bullet[1].x)
                    bullet[1].x += 15
                else:
                    self.projectile_count.pop(self.projectile_count.index(bullet))


    def draw_windows(self):
        self.game_window.blit(self.player, (self.player_setup.x, self.player_setup.y))
        if len(self.projectile_count) > 0:
            pygame.draw.rect(self.game_window, (255, 0, 0), self.projectile)
        pygame.display.update()

    def first_sprite(self):
        """ test sprite for gif animation for shooting"""
        test_sprite = pygame_functions.makeSprite('arrow_shoot_gif.gif', 3)

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

            self.window_setup()

            self.draw_windows()




if __name__ == '__main__':
    game = Game()
