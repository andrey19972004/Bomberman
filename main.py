# Над кодом работали:
# Никита Гудков
# Иван Сафонов
# Андрей Ткачёв
# Дамир Федотов
# Анна Бушэ
# Харченко Владислав
# Колесникова Алина

import sys
import pygame
from random import randint
from pygame.rect import Rect


class Camera:
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)

    def apply(self, target, speed):
        return target.rect.move((self.state.x * speed / 2, self.state.y))


def camera_func(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l + 800 / 2, -t + 650 / 2

    l = min(0, l)  # Не движемся дальше левой границы
    l = max(-(camera.width - 800), l)  # Не движемся дальше правой границы
    # t = max(-(camera.height-650), t)        # Не движемся дальше нижней границы
    # t = min(0, t)                           # Не движемся дальше верхней границы
    t = 200
    return Rect(l, t, w, h)


class Cell:
    image = None

    def __init__(self, x=0, y=75):
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def process_draw(self, screen, x=0, y=75):
        self.rect.x = x
        self.rect.y = y
        screen.blit(self.image, self.rect)


class Block(Cell):
    image = pygame.image.load("img/blocker.jpg")

    def __init__(self, x=0, y=75):
        super().__init__(x, y)
        self.type = "Block"


class Grass(Cell):
    image = pygame.image.load("img/grass.jpg")

    def __init__(self, x=0, y=75):
        super().__init__(x, y)
        self.type = "Grass"


class Brick(Cell):
    image = pygame.image.load("img/brick.jpg")

    def __init__(self, x=0, y=75):
        super().__init__(x, y)
        self.type = "Brick"


class Area:
    def __init__(self, width=1550, height=650, size_block=50):
        self.area_data = []
        self.width = width
        self.height = height
        self.size_block = size_block
        self.shift_area = 0
        self.rgb = [
            (150, 0, 0),
            (0, 150, 0),
            (0, 0, 150)
        ]
        self.area_data = []
        self.objects = []

        self.create_area()

    def create_area(self):
        h = self.height // 50
        w = self.width // 50
        for i in range(h):
            self.area_data.append([])
        for i in range(h):
            for j in range(w):
                self.area_data[i].append(1)
        for i in range(h):
            self.area_data[i][0] = 0
            self.area_data[i][30] = 0
        for i in range(w):
            self.area_data[0][i] = 0
            self.area_data[12][i] = 0
        for i in range(2, 12, 2):
            for j in range(2, 30, 2):
                self.area_data[i][j] = 0

        for i in range(randint(50, 75)):
            x = randint(1, 29)
            y = randint(1, 11)
            while self.area_data[y][x] == 0 or self.area_data[y][x] == 2:
                x = randint(1, 29)
                y = randint(1, 11)
            self.area_data[y][x] = 2
        self.area_data[1][1] = 1
        self.area_data[1][2] = 1
        self.area_data[2][1] = 1

        for i in range(h):
            print(self.area_data[i])

        # for i in range(13):
        #     for j in range(31):
        #         if self.area_data[i][j] == 0:
        #             self.objects.append(Block(j * 50, i * 50 - 125))
        #         elif self.area_data[i][j] == 1:
        #             self.objects.append(Grass(j * 50, i * 50 - 125))
        #         elif self.area_data[i][j] == 2:
        #             self.objects.append(Brick(j * 50, i * 50 - 125))

        for i in range(13):
            for j in range(31):
                if self.area_data[i][j] == 0:
                    self.objects.append(Block(j * 50, i * 50 + 75))
                elif self.area_data[i][j] == 1:
                    self.objects.append(Grass(j * 50, i * 50 + 75))
                elif self.area_data[i][j] == 2:
                    self.objects.append(Brick(j * 50, i * 50 + 75))

    def process_draw(self, screen, camera, speed):
        for i in self.objects:
            # screen.blit(i.image, camera.apply(i, speed))
            screen.blit(i.image, i.rect)


class Bomberman(Cell):
    image = pygame.image.load("img/bomberman.png")
    def __init__(self, x=50, y=125):
        super().__init__(x, y)
        self.shift_x = 0
        self.shift_y = 0
        self.speed = 5
        self.can_move_Right = True
        self.can_move_Left = True
        self.can_move_Up = True
        self.can_move_Down = True

    def process_draw(self, screen, camera):
        screen.blit(self.image, self.rect)

    def process_logic(self, width, height, area):
        if self.rect.x + self.shift_x < 50:
            self.shift_x = 0
        if self.rect.x + self.shift_x > 705:
            self.shift_x = 0

        if self.rect.y + self.shift_y < 125:
            self.shift_y = 0
        if self.rect.y + self.shift_y > height - 25:
            self.shift_y = 0

        # print(self.rect.x)

        if self.rect.left < 50:
            self.rect.left = 50
        if self.rect.top < 125:
            self.rect.top = 125
        if self.rect.x > 700:
            self.rect.x = 700
        if self.rect.left < 50:
            self.rect.right = 50

    def move(self):
        if self.rect.x <= 800 / 2:
            self.rect.move_ip(self.shift_x, self.shift_y)
        else:
            self.rect.move_ip(self.shift_x / 2, self.shift_y)

class Game:
    def __init__(self, width=800, height=625):
        self.width = width
        self.height = height
        self.size = (width, height)
        self.game_over = False
        self.screen = pygame.display.set_mode(self.size)
        pygame.init()
        self.create_objects()

    def create_objects(self):
        self.area = Area()
        self.bomberman = Bomberman()
        self.camera = Camera(camera_func, 1550, 650)

    def process_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == 97 or event.key == 276 or event.key == 160:
                    self.bomberman.shift_x = -self.bomberman.speed
                elif event.key == 100 or event.key == 275 or event.key == 162:
                    self.bomberman.shift_x = self.bomberman.speed
                elif event.key == 115 or event.key == 274 or event.key == 161:
                    self.bomberman.shift_y = self.bomberman.speed
                elif event.key == 119 or event.key == 273 or event.key == 172:
                    self.bomberman.shift_y = -self.bomberman.speed
                # print(event.key)
            if event.type == pygame.KEYUP:
                self.bomberman.shift_x = 0
                self.bomberman.shift_y = 0

    def process_move(self):
        for i in self.area.objects:
            if i.rect.colliderect(self.bomberman.rect) != 0 and i.type != 'Grass':
                print("COLLIDE")

        self.bomberman.move()

    def main_loop(self):
        while not self.game_over:
            # self.bomberman.can_move_Down = True
            # self.bomberman.can_move_Up = True
            # self.bomberman.can_move_Left = True
            # self.bomberman.can_move_Right = True

            # b2 = Bomberman(self.bomberman.rect.x + 5, self.bomberman.rect.y)
            # for i in range(31*13):
            #     if pygame.sprite.collide_rect(self.bomberman, self.area.objects[i]) == 1:
            #         if self.area.objects[i].type != "Grass":
            #             if self.bomberman.rect.x + 50 + 5 >= self.area.objects[i].rect.x:
            #                 self.bomberman.can_move_Right = False
            #             elif self.bomberman.rect.x - 5 <= self.area.objects[i].rect.x + 50:
            #                 self.bomberman.can_move_Left = False
            #             elif self.bomberman.rect.y + 50 + 5 >= self.area.objects[i].rect.y:
            #                 self.bomberman.can_move_Down = False
            #             elif self.bomberman.rect.y - 5 <= self.area.objects[i].rect.y + 50:
            #                 self.bomberman.can_move_Up = False

            # for i in range(31 * 13):
            #     if pygame.sprite.collide_rect(self, self.area.objects[i]) == 1:
            #         if self.area.objects[i].type != "Grass":
            #             print("ТУТ КОЛЛИЗИЯ!!!!")

            self.process_event()
            self.screen.fill((75, 100, 150))

            # self.camera.update(self.bomberman)
            self.area.process_draw(self.screen, self.camera, self.bomberman.speed)

            self.bomberman.process_logic(self.area.width, self.area.height, self.area)
            self.process_move()
            self.bomberman.process_draw(self.screen, self.camera)

            pygame.display.flip()
            pygame.time.wait(10)
        sys.exit()


def main():
    game = Game(800, 725)
    game.main_loop()


if __name__ == '__main__':
    main()
