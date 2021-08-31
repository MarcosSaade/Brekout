"""
-Power ups (power downs)
-High score

~5.3 hours of coding

"""

import pygame
import sys
import random

pygame.init()


class Main:
    def __init__(self):
        self.pause_menu = PauseMenu()
        self.game_over_menu = GameOverMenu()
        self.game_screen = GameScreen()
        self.player = Player()
        self.ball = Ball()
        self.flow = Flow()
        self.pm_active = False
        self.game_over = False
        self.score = 0
        self.lives = 3

    def logic_control(self):
        if self.pm_active:
            self.pause_menu.draw()
        elif self.game_over:
            self.game_over_menu.draw()
        else:
            self.game_loop()

    def game_loop(self):
        screen.fill((200, 200, 200))
        self.game_screen.high_score()
        self.game_screen.draw_lives()
        self.game_screen.draw_blocks()
        self.game_screen.show_score()
        self.player.draw()
        self.player.move()
        self.ball.draw()
        self.ball.move()
        self.flow.check_win()


class GameScreen:
    def __init__(self):
        self.blocks = []
        self.block_state = []
        self.multiply = True
        self.rows = 4

        self.image = []
        self.image_hard = pygame.image.load('rectangle.png').convert_alpha()
        self.image_hit = pygame.image.load('rectangle_hit.png').convert_alpha()
        self.image_damaged = pygame.image.load('rectangle_damaged.png').convert_alpha()

        self.score_font = pygame.font.Font('fonts/VCR_OSD_MONO.ttf', 24)

    def make_blocks(self):
        for i in range(self.rows):
            for j in range(7):
                self.blocks.append(pygame.rect.Rect(j, i, 10, 10))

        for i in range(len(self.blocks)):
            self.block_state.append(3)

        if self.multiply:
            for block in range(len(self.blocks)):
                self.blocks[block][0] *= 100
                self.blocks[block][0] += 50
                self.blocks[block][1] *= 20
            self.multiply = False

        self.image = [self.image_hard for _ in range(len(self.blocks))]

    def draw_blocks(self):
        if len(self.blocks) == 0:
            self.make_blocks()

        for i in range(len(self.blocks)):
            screen.blit(self.image[i], self.blocks[i])

    def high_score(self):
        pass

    def draw_lives(self):
        for i in range(main.lives):
            pygame.draw.circle(screen, (30, 30, 30), (i * 20 + 20, 570), 5)

    def show_score(self):
        score_text = self.score_font.render(f'Score:{main.score}', False, (0, 30, 0))
        screen.blit(score_text, (640, 560))


class Player:
    def __init__(self):
        self.x = 340
        self.speed = 0
        self.length = 100
        self.line = pygame.rect.Rect(self.x, 550, self.length, 7)

    def draw(self):
        pygame.draw.rect(screen, (100, 100, 100), self.line)

    def move(self):
        # self.x = main.ball.x - 60 AI

        self.x += self.speed
        self.line = pygame.rect.Rect(self.x, 550, self.length, 7)

        if self.x < 10:
            self.x = 10
        if self.x > 790 - self.length:
            self.x = 790 - self.length


class Ball:
    def __init__(self):
        self.x = 400
        self.y = 530
        self.speed_x = 5
        self.speed_y = -5

    def draw(self):
        pygame.draw.circle(screen, (30, 30, 30), (self.x, self.y), 5)

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y

        if self.x >= 795 or self.x <= 5:
            self.speed_x *= -1
        if self.y <= 5:
            self.speed_y *= -1

        if self.collision_block():
            self.speed_y *= -1

        self.collision_border()

    def collision_border(self):
        if self.y == 550:
            if self.x in range(main.player.x, main.player.x + main.player.length):
                self.speed_y *= -1
                self.speed_x *= random.choice([1, -1])

        if self.y >= 600:
            main.lives -= 1
            if main.lives == 0:
                main.game_over = True
            else:
                main.flow.new_ball()

    def collision_block(self):
        for i in main.game_screen.blocks:
            index = main.game_screen.blocks.index(i)

            if self.y == i[1] + 15 and self.x in range(i[0], i[0] + 100):
                main.game_screen.block_state[index] -= 1

                if main.game_screen.block_state[index] <= 0:
                    main.game_screen.image.pop(index)
                    main.game_screen.blocks.pop(index)
                    main.game_screen.block_state.pop(index)
                    main.score += 100
                else:
                    if main.game_screen.block_state[index] == 2:
                        main.game_screen.image[index] = main.game_screen.image_hit
                    elif main.game_screen.block_state[index] == 1:
                        main.game_screen.image[index] = main.game_screen.image_damaged

                return True


class PauseMenu:
    def __init__(self):
        self.font_big = pygame.font.Font('fonts/VCR_OSD_MONO.ttf', 50)
        self.font_small = pygame.font.Font('fonts/VCR_OSD_MONO.ttf', 30)
        self.pause_text = self.font_big.render('PAUSED', False, (100, 100, 100))
        self.continue_text = self.font_small.render('PRESS P TO CONTINUE', False, (200, 200, 200))

    def draw(self):
        screen.blit(self.pause_text, (300, 200))
        screen.blit(self.continue_text, (215, 300))
        pygame.time.delay(100)


class GameOverMenu:
    def __init__(self):
        self.font_big = pygame.font.Font('fonts/VCR_OSD_MONO.ttf', 70)
        self.font_small = pygame.font.Font('fonts/VCR_OSD_MONO.ttf', 30)
        self.breakout_text = self.font_big.render('Game Over', False, (100, 200, 50))
        self.play_text = self.font_small.render('PRESS SPACEBAR TO PLAY AGAIN', False, (100, 50, 200))

    def draw(self):
        screen.blit(self.breakout_text, (240, 300))
        screen.blit(self.play_text, (170, 400))


class Flow:
    def check_win(self):
        if len(main.game_screen.blocks) == 0:
            print('won')
            main.game_screen.block_state = []
            main.game_screen.make_blocks()
            main.game_screen.multiply = True

            if main.game_screen.rows < 8:
                main.game_screen.rows += 1

            print(main.game_screen.rows)

    def new_ball(self):
        main.ball.x = 400
        main.ball.y = 100
        main.ball.speed_x = random.choice([5, -5])
        main.ball.speed_y = 5

        main.player.x = 340
        main.player.speed = 0

        pygame.time.wait(100)

    def restart(self):
        # Reset ball
        main.ball.x = 400
        main.ball.y = 100
        main.ball.speed_x = random.choice([5, -5])
        main.ball.speed_y = 5

        # Reset player
        main.player.x = 340
        main.player.speed = 0

        # Reset lives
        main.lives = 3

        # Reset score
        main.score = 0

        # Reset blocks
        main.game_screen.blocks = []
        main.game_screen.multiply = True


def events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if not main.game_over:
                if main.pm_active:
                    if event.key == pygame.K_p:
                        main.pm_active = False
                else:
                    if event.key == pygame.K_p:
                        main.pm_active = True
                    if event.key == pygame.K_RIGHT:
                        main.player.speed = 7
                    if event.key == pygame.K_LEFT:
                        main.player.speed = -7
            else:
                if event.key == pygame.K_SPACE:
                    main.flow.restart()
                    main.game_over = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT and main.player.speed > 0:
                main.player.speed = 0
            if event.key == pygame.K_LEFT and main.player.speed < 0:
                main.player.speed = 0


clock = pygame.time.Clock()
screen = pygame.display.set_mode((800, 600))

main = Main()

while True:
    events()
    screen.fill((0, 0, 0))
    main.logic_control()
    pygame.display.update()
    clock.tick(60)
