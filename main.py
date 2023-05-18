import pygame
from time import sleep, perf_counter
from threading import Thread
from random import choice, randint

class Game:
    def __init__(self, resolution, FPS, background_color=(255, 255, 255)):
        self.screen = pygame.display.set_mode(resolution)
        self.background_color = background_color
        self.resolution = resolution
        self.keep_running = True
        self.water_drops = []
        self.buttons = []
        self.objects = []
        self.FPS = FPS
        self.delay = round(1 / FPS, 4)
        self.money = 0

        self.min_size, self.max_size = 10, 25
        self.rate = 0.05

        self.cost_upgrade_rate = 10
        self.cost_upgrade_size = 10

        pygame.init()

        self.font1 = pygame.font.Font('freesansbold.ttf', 32)

        Thread(target=self.fill_and_update).start()

    def draw_all(self):
        for object in self.objects:
            object.draw()

        pygame.draw.rect(self.screen, (0, 0, 0), (0, 0, 10, self.resolution[1]))
        pygame.draw.rect(self.screen, (0, 0, 0), (self.resolution[0] - 10, 0, 10, self.resolution[1]))
        pygame.draw.rect(self.screen, (0, 0, 0), (0, self.resolution[1] - 320, self.resolution[0] // 2 - 30, 320))
        pygame.draw.rect(self.screen, (0, 0, 0), (self.resolution[0] // 2 + 30, self.resolution[1] - 320, self.resolution[0] // 2 - 30, 320))
        pygame.draw.rect(self.screen, (0, 0, 0), (0, 0, self.resolution[0], 90))
        money = self.font1.render(f'Money: {self.money}', True, (0, 255, 0))
        self.screen.blit(money, (0, 0))

        for button in self.buttons:
            button.draw()

    def fill_and_update(self):
        while self.keep_running is True:
            self.screen.fill(self.background_color)
            self.draw_all()
            sleep(self.delay)
            pygame.display.update()

    class Button:
        def __init__(self, colors, value, geometry, frame_width, base_text, optional_text=''):
            self.x, self.y, self.width, self.height = geometry
            self.frame_width = frame_width
            self.geometry = geometry
            self.colors = colors
            self.font = pygame.font.Font('freesansbold.ttf', 22)
            self.optional_text = optional_text
            self.base_text = base_text
            self.hovered = False
            self.value = value
            self.update_value(self.value)

            self.base_text_object = self.font.render(self.base_text, True, self.colors[self.hovered]["text"])

            game.buttons.append(self)

        def update_value(self, value):
            self.value = value
            C = self.colors[self.hovered]
            self.text_object = self.font.render(f"{self.optional_text}{value}", True, C["text"])

        def draw(self):
            F = self.frame_width
            C = self.colors[self.hovered]
            pygame.draw.rect(game.screen, C["frame"], (self.x - F, self.y - F, self.width + F * 2, self.height + F * 2))
            pygame.draw.rect(game.screen, C["background"], (self.x, self.y, self.width, self.height))
            game.screen.blit(self.base_text_object, (self.x, self.y + 15))
            game.screen.blit(self.text_object, (self.x, self.y + 45))

        def clicked(self):
            pass

    class UpgradeRate(Button):
        def __init__(self):
            super().__init__(
                colors={False: {"text": (220, 0, 220),
                                "frame": (200, 0, 0),
                                "background": (75, 75, 75)},
                        True: {"text": (255, 255, 255),
                                "frame": (255, 255, 255),
                                "background": (75, 75, 75)}},
                geometry=(20, 660, 200, 90),
                base_text="    Upgrade Rate",
                optional_text="    Cost: ",
                value=game.cost_upgrade_rate,
                frame_width=10)

        def clicked(self):
            if game.money >= game.cost_upgrade_rate and game.rate > 0.01 and not self.hovered:
                self.hovered = True
                game.money -= game.cost_upgrade_rate
                game.rate = round(game.rate - 0.01, 3)
                game.cost_upgrade_rate *= 4
                sleep(0.2)
                self.update_value(game.cost_upgrade_rate)
                self.hovered = False

    class UpgradeSize(Button):
        def __init__(self):
            super().__init__(
                colors={False: {"text": (220, 0, 220),
                                "frame": (200, 0, 0),
                                "background": (75, 75, 75)},
                        True: {"text": (255, 255, 255),
                                "frame": (255, 255, 255),
                                "background": (75, 75, 75)}},
                geometry=(20, 780, 200, 90),
                base_text="    Upgrade Size",
                optional_text="    Cost: ",
                value=game.cost_upgrade_size,
                frame_width=10)

        def clicked(self):
            if game.money >= game.cost_upgrade_size and game.max_size < 120 and not self.hovered:
                self.hovered = True
                game.money -= game.cost_upgrade_size
                game.min_size += 5
                game.max_size += 5
                game.cost_upgrade_size *= 4
                sleep(0.2)
                self.update_value(game.cost_upgrade_size)
                self.hovered = False

    class WaterDrop:
        def __init__(self, geometry):
            self.x, self.y, self.width, self.height = geometry
            self.geometry = geometry
            color_value = randint(200, 255)
            self.color = (0, color_value, color_value)
            self.acceleration = 1
            self.velocity = 0

            game.water_drops.append(self)
            game.objects.append(self)

        def draw(self):
            self.fall()
            self.check_collision()
            pygame.draw.rect(game.screen, self.color, (self.x, self.y, self.width, self.height))

        def check_collision(self):
            if self.y + self.height >= water.y:
                game.water_drops.remove(self)
                game.objects.remove(self)
                if water.height <= 550:
                    water.height += self.height // 10

        def fall(self):
            self.velocity += self.acceleration
            self.y += self.velocity

    class Water:
        def __init__(self):
            self.height = 0
            self.y = game.resolution[1] - 320

            game.objects.append(self)

        def draw(self):
            if not stopple.is_open:
                self.y = game.resolution[1] - 320 - self.height
            pygame.draw.rect(game.screen, (0, 255, 255), (0, self.y, game.resolution[0], self.height))

    class Faucet:
        def __init__(self, color=(25, 25, 25)):
            self.x, self.y, self.width, self.height = ((game.resolution[0] - 30) // 2, 90, 30, 20)
            self.color = color

            game.objects.append(self)

            Thread(target=self.spawn).start()

        def draw(self):
            pygame.draw.rect(game.screen, (0, 0, 0), (self.x, self.y, self.width, self.height))

        def spawn(self):
            while game.keep_running is True:
                delay = game.rate
                sleep(delay)
                if not stopple.is_open and water.height < 550:
                    size = randint(game.min_size, game.max_size)
                    game.water_drops.append(game.WaterDrop((self.x + (self.width - size) // 2, self.y + self.height, size, size)))

    class Stopple:
        def __init__(self):
            self.y = game.resolution[1] - 320
            self.is_open = False
            game.objects.append(self)

        def draw(self):
            pygame.draw.rect(game.screen, (0, 0, 0), (0, self.y, game.resolution[0], 10))

        def open(self):
            self.is_open = True
            co_ = water.height // 32
            delay = 0.015
            for n in range(1, 88):
                self.y += 10
                water.y += 10
                sleep(delay)
            water.y = game.resolution[1] - 320
            game.money += water.height // 5
            water.height = 0
            for n in range(1, 88):
                self.y -= 10
                sleep(delay)
            self.y = game.resolution[1] - 320
            self.is_open = False
            print(f"Total Money: {game.money}")


game = Game(resolution=(540, 960), FPS=30)
water = game.Water()
faucet = game.Faucet()
stopple = game.Stopple()
upgrade_rate = game.UpgradeRate()
upgrade_size = game.UpgradeSize()

while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p and not stopple.is_open:
                Thread(target=stopple.open).start()
            if event.key == pygame.K_q:
                game.keep_running = False
                pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            left, middle, right = pygame.mouse.get_pressed()
            if left:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for button in game.buttons:
                    x, y, width, height = button.geometry
                    if x < mouse_x < x + width and y < mouse_y < y + height:
                        Thread(target=button.clicked).start()

    sleep(game.delay)
    
