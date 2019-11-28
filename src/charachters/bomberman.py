import pygame
import time

from src.blocks.cell import Cell

class Bomberman(Cell):
    animation_gap = 2
    animation_bomberman_down_s = ['./img/bomberman/stand/Front.png',
                                './img/bomberman/stand/Fron1.png']
    animation_bomberman_down_a = ['./img/bomberman/run/Runs_down.png',
                                './img/bomberman/run/Runs_down1.png']

    animation_bomberman_up_s = ['./img/bomberman/stand/Back.png']
    animation_bomberman_up_a = ['./img/bomberman/run/Running_back.png',
                                './img/bomberman/run/Running_back1.png']

    animation_bomberman_left_s = ['./img/bomberman/stand/Side_stands.png']
    animation_bomberman_left_a = ['./img/bomberman/run/Runs_left.png',
                                  './img/bomberman/run/Runs_left1.png']

    animation_bomberman_right_s = ['./img/bomberman/stand/Side_stoin1.png']
    animation_bomberman_right_a = ['./img/bomberman/run/Runs_right.png',
                                   './img/bomberman/run/Runs_right1.png']

    image = pygame.image.load(animation_bomberman_up_s[0])

    def __init__(self, x=50, y=125):
        super().__init__(x, y)
        self.shift_x_left = 0
        self.shift_x_right = 0
        self.shift_y_up = 0
        self.shift_y_down = 0
        self.shift_x = 0
        self.shift_y = 0
        self.speed = 5
        self.can_move_Right = True
        self.can_move_Left = True
        self.can_move_Up = True
        self.can_move_Down = True
        # for bonus:
        self.max_count_bombs = 1
        self.long_fire = 2


    def animation_right(self,flag):
        if flag:
            self.image = pygame.image.load(self.animation_bomberman_right_a[0])
        else:
            self.image = pygame.image.load(self.animation_bomberman_right_s[0])


    def animation_left(self,flag):
        if flag:
            self.image = pygame.image.load(self.animation_bomberman_left_a[0])
        else:
            self.image = pygame.image.load(self.animation_bomberman_left_s[0])

    def animation_up(self,flag):
        if flag:
            self.image = pygame.image.load(self.animation_bomberman_up_a[0])
        else:
            self.image = pygame.image.load(self.animation_bomberman_up_s[0])

    def animation_down(self,flag):
        if flag:
            self.image = pygame.image.load(self.animation_bomberman_down_a[0])
        else:
            self.image = pygame.image.load(self.animation_bomberman_down_s[0])

    def process_draw(self, screen, camera, x=0, y=75):
        screen.blit(self.image, camera.apply(self))

    def process_logic(self, height):
        pass

    def move(self):
        if self.shift_x > 0 and self.can_move_Right:
            self.rect.move_ip(self.shift_x, 0)
        if self.shift_x < 0 and self.can_move_Left:
            self.rect.move_ip(self.shift_x, 0)
        if self.shift_y > 0 and self.can_move_Down:
            self.rect.move_ip(0, self.shift_y)
        if self.shift_y < 0 and self.can_move_Up:
            self.rect.move_ip(0, self.shift_y)
