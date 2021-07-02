import pygame

class Game:
    def __init__(self):

        # initialize the variables
        self.game_window = pygame.display.set_mode((1280, 720))
        self.game_background = pygame.transform.scale(pygame.image.load('map.png'), (1280, 720))

        # initialize player dimensions
        self.player_dim = (255, 255, 0)
        self.player_setup = pygame.Rect(700, 300, 80, 80)
        self.player_image = pygame.image.load('alex.png')
        self.player = pygame.transform.rotate(pygame.transform.scale(self.player_image, (30, 30)), 270)
        self.game_loop()

    def window_setup(self):
        self.game_window.blit(self.game_background, (0, 0))
        pygame.display.update()

    def handle_movement(self, pressed_key, player):
        if pressed_key[pygame.K_a] and player.x - 10 > 0:
            player.x -= 10
        if pressed_key[pygame.K_w] and player.y - 10 > 0:
            player.y -= 10
        if pressed_key[pygame.K_s] and player.y + 10 < 700:
            player.y += 10
        if pressed_key[pygame.K_d] and player.x - 10 < 1240:
            player.x += 10

    def draw_windows(self):
        self.game_window.blit(self.player, (self.player_setup.x, self.player_setup.y))
        pygame.display.update()

    def game_loop(self):
        self.clock = pygame.time.Clock()
        while True:
            self.clock.tick(30)
            for event in pygame.event.get():
                pass


            self.pressed_key = pygame.key.get_pressed()
            self.handle_movement(pressed_key=self.pressed_key, player=self.player_setup)
            self.window_setup()

            self.draw_windows()



if __name__ == '__main__':
    game = Game()
