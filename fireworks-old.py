import pygame
import random
import os
import math

# 初始化信息
WIDTH = 1152
HEIGHT = 720
FPS = 60
img_path = os.path.join(os.path.dirname(__file__), "img")
audio_path = os.path.join(os.path.dirname(__file__), "audio")

def randv():    # 生成随机初速度
    v = random.random() * 22
    while (v < 15):
        v = random.random() * 22
    return v

def rand_color():   # 随机生成烟花颜色
    color_list = [(244, 214, 215), (55, 20, 88), (151, 68, 114), (230, 190, 146), (244, 252, 255), (230, 197, 246), (181, 180, 222), (191, 85, 177), (255, 199, 209), (200, 50, 66), (223, 219, 216), (158, 167, 164), (173, 254, 255), (185, 219, 149), (72, 141, 235), (252, 117, 249), (232, 169, 180), (155, 157, 170), (182, 98, 130)]
    return color_list[random.randint(0, len(color_list) - 1)]

def add_fireworks(list):  # 添加新的烟花
    if (random.random() < 3 / 60):
        list.append(Fireworks())

class Item(pygame.sprite.Sprite):   # 烟花颗粒
    def __init__(self, vy, x, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((15, 15))
        self.image.fill((0, 0, 0))
        self.image.set_colorkey((0, 0, 0))
        if color == (-1, -1, -1):   # 纯色烟花或者混色烟花
            color = rand_color()
        self.color = color
        self.radius = randv() / 5   # 烟花颗粒的半径
        pygame.draw.circle(self.image, self.color, (8, 8), self.radius) # 形成圆形烟花颗粒
        self.rect = self.image.get_rect()
        self.rect.center = (x, HEIGHT - 10) # 初始位置
        self.vx = 0
        self.vy = vy
        self.is_explode = False # 记录是否已经爆炸过
        self.count = 0

    def update(self, radius):
        self.move()
        if self.rect.y > HEIGHT - 20 and self.is_explode:
            self.kill()
        if self.vy < 2 and not self.is_explode:
            self.explode(radius)
        if self.is_explode: # 爆炸后一段时间删除颗粒
            self.count += 1
            if self.count > 40:
                self.kill()


    def move(self): # vx为水平方向速度,vy为竖直方向速度
        t = 1 / 60
        g = 9.8
        self.rect.x += self.vx * t * 25
        self.rect.y -= (2 * self.vy - g * t) * t / 2 * 25
        self.vy = self.vy - g * t

    def explode(self, radius):
        self.is_explode = True
        angle = random.randint(0, 359) * math.pi / 180
        self.vx += math.cos(angle) * radius
        self.vy -= math.sin(angle) * radius


class Fireworks():  # 烟花列表
    def __init__(self):
        self.list = pygame.sprite.Group()
        self.vy = randv()
        self.x = WIDTH * random.random()
        self.num = random.randint(30, 40) # 单个烟花随机烟花颗粒数量
        color = rand_color()
        if random.randint(1, 2) == 1:   # 纯色烟花或者混色烟花
            color = (-1, -1, -1)
        self.list.add(Item(self.vy, self.x, color) for i in range(self.num))

    def draw(self, screen):
        self.list.draw(screen)

    def update(self):
        radius = random.random() * 10
        while (radius < 8):
            radius = random.random() * 10
        self.list.update(radius)

def main():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))   # 主画布大小
    pygame.display.set_caption("Fireworks --made by xketx")
    pygame.display.set_icon(pygame.image.load(os.path.join((img_path), "fireworks.png")).convert()) # 设置图标
    bgm = pygame.mixer.music.load(os.path.join(audio_path, "bgm.mp3"))  # 背景音乐
    pygame.mixer.music.play(-1) # 循环播放背景音乐
    clock = pygame.time.Clock()

    fireworks_list = [Fireworks() for i in range(5)]    # 初始烟花数目
    running = True  # 是否循环
    count = 2
    while running:  # 循环主程序
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if count == 2:
            screen.blit(pygame.image.load(os.path.join(img_path, "bgp.jpg")), (0, 0))   # 设置背景图片
            count = 0
        add_fireworks(fireworks_list)
        for item in fireworks_list:
            item.update()
            item.draw(screen)
        pygame.display.flip()
        count += 1

    pygame.QUIT
    exit()

if __name__ == "__main__":
    main()