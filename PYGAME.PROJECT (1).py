import os
import pygame
import random


FPS = 100
width = 304  # ширина экрана
height = 380  # высота экрана
WHITE = (255, 255, 255)
BLUE = (0, 70, 225)
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
mishen = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
hero_sprites = pygame.sprite.Group()
exitGame = False


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print("Cannot load image:", name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
    return image


class Platform(pygame.sprite.Sprite):
    def __init__(self, radius, x, y):
        super().__init__(all_sprites)
        self.radius = radius
        x = 175
        y = 400
        self.image = load_image("platform.png", (0, 0, 0))
        self.rect = pygame.Rect(100, 310, 69, 21)
        self.vx = 4
        self.vy = 0
        self.add(horizontal_borders)

    def update(self, x):
        self.rect = self.rect.move(self.vx + x, self.vy)

    def draw(self):
        sc_game.blit(self.image, self.rect)


class Hero(pygame.sprite.Sprite):
    def __init__(self, radius, x, y):
        super().__init__(all_sprites, hero_sprites)
        self.radius = radius
        self.image = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color("yellow"), (radius, radius), radius)
        self.rect = pygame.Rect(x, y, 2 * radius, 2 * radius)
        self.vx = 2
        self.vy = -2
        self.Count = 0
        self.new_game = False

    def collide(self, platforms):
        find = False
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                find = True
                thing = p
        if find:
            mishen.remove(thing)
            all_sprites.remove(thing)
            platforms.remove(thing)
            self.Count += 1

    def update(self, platforms):
        self.collide(platforms)
        self.rect = self.rect.move(self.vx, self.vy)

        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.vy = -self.vy
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.vx = -self.vx

        pl = pygame.sprite.spritecollideany(self, mishen)

        if pl:
            if self.rect.x >= pl.rect.left and self.rect.x - 2 * self.radius <= pl.rect.right:
                self.vy = -self.vy
            if self.rect.y + 2 * self.radius >= pl.rect.top and self.rect.y \
                    + 2 * self.radius <= pl.rect.bottom and self.rect.x - 4 * self.radius <= pl.rect.left:
                self.vx = -self.vx
            if self.rect.y + 2 * self.radius >= pl.rect.top and self.rect.y \
                    + 2 * self.radius <= pl.rect.bottom and self.rect.x - 2 * self.radius >= pl.rect.right:
                self.vx = -self.vx
        if self.rect.y >= height:
            exitGame = True
            exit_punkts = [(20, 140, u'Вы проиграли!', (255, 255, 30), (255, 30, 255), 0),
                           (130, 210, u'Exit', (255, 255, 30), (255, 30, 255), 1)]
            game = Menu(exit_punkts)
            game.startMenu()
            self.new_game = True
            self.rect.x = 150
            self.rect.y = 150

    def draw(self):
        sc_game.blit(self.image, self.rect)


pygame.init()
sc = pygame.display.set_mode((width, height))
sc.fill(WHITE)


class Border(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:  # вертикальная стенка
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        elif y1 == y2:  # горизонтальная стенка
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)
        else:
            self.add(mishen)
            self.image = pygame.Surface([29, 10])
            self.rect = pygame.Rect(x1, y1, 29, 10)

    def draw(self):
        sc_game.blit(self.image, self.rect)

    def update(self, platforms):
        if pygame.sprite.spritecollideany(self, hero_sprites):
            pass


class Menu:
    def __init__(self, punkts=[12, 140, u"Punkt", (20, 20, 20), (20, 20, 255), 0]):
        self.punkts = punkts

    def draw(self, poverhnost, font, num_punkt):
        fon = pygame.transform.scale(load_image('space.png'), (width, height))
        sc.blit(fon, (0, 0))
        poverhnost.blit(font.render("PyArcanoid ;)", 1, (0, 255, 0)), (45, 45))
        for i in self.punkts:
            if num_punkt == i[5]:
                poverhnost.blit(font.render(i[2], 1, i[4]), (i[0], i[1]))
            else:
                poverhnost.blit(font.render(i[2], 1, i[3]), (i[0], i[1]))

    def startMenu(self):
        done = True

        font_menu = pygame.font.Font(None, 50)

        punkt = 0
        while done:
            mp = pygame.mouse.get_pos()
            for i in self.punkts:
                if mp[0] > i[0] and mp[0] < i[0] + 155 and mp[1] > i[1] and mp[1] < i[1] + 50:
                    punkt = i[5]
            self.draw(sc, font_menu, punkt)
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    exit()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        exit()
                    if e.key == pygame.K_UP:
                        if punkt > 0:
                            punkt -= 1
                    if e.key == pygame.K_DOWN:
                        if punkt < len(self.punkts) - 1:
                            punkt += 1
                    if e.key == pygame.K_RETURN:
                        if punkt == 0:
                            done = False
                        elif punkt == 1:
                            exit()
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    if punkt == 0:
                        done = False
                    elif punkt == 1:
                        exit()

            pygame.display.flip()


sc_game = pygame.Surface((width, height - 20))
sc_state = pygame.Surface((width, 20))
sc_game.fill(WHITE)
sc_state.fill((10, 10, 100))

inf_font = pygame.font.Font(None, 24)

clock = pygame.time.Clock()

punkts = [(120, 140, u'Start', (255, 255, 30), (255, 30, 255), 0),
          (130, 210, u'Exit', (255, 255, 30), (255, 30, 255), 1)]
game = Menu(punkts)
game.startMenu()

ball = []
h1_dr = False
h1 = Hero(7, random.randint(10, width - 100), random.randint(100, height - 200))
h1_dr = True
X = 100
platforms = []
count_pl = 0
x_pl = 10
y_pl = 10
pygame.display.update()

sc.fill(WHITE)
for j in range(3):
    for i in range(9):
        platforms.append(Border(x_pl, y_pl, 29, 10 + 10))
        platforms[count_pl].draw()
        x_pl += 32
        count_pl += 1
    x_pl = 10
    y_pl += 15
ball.append(Platform(20, random.randint(20, width - 100), random.randint(200, height - 50)))
b1 = Border(5, 5, width - 5, 5)
b1.draw()
# b2 = Border(5, height - 25, width - 5, height - 25)
# b2.draw()
b3 = Border(5, 5, 5, height - 25)
b3.draw()
b4 = Border(width - 5, 5, width - 5, height - 25)
b4.draw()
while 1:
    b1.draw()
    # b2.draw()
    b3.draw()
    b4.draw()
    if h1.new_game:
        x_pl = 10
        y_pl = 10
        for i in platforms:
         mishen.empty()
         all_sprites.remove(platforms)
        platforms.clear()
        count_pl = 0
        for j in range(3):
            for i in range(9):
                platforms.append(Border(x_pl, y_pl, 29, 10 + 10))
                platforms[count_pl].draw()
                x_pl += 32
                count_pl += 1
            x_pl = 10
            y_pl += 15
        h1.new_game = False

    pygame.display.update()
    sc_state.fill((10, 10, 100))
    sc_game.fill(WHITE)
    x_pl = 10
    y_pl = 10
    x_pl1 = 10
    y_pl1 = 25
    x_pl2 = 10
    y_pl2 = 40

    ball[0].draw()
    # ball[i].update()
    if h1_dr:
        h1.draw()
        h1.update(platforms)

    for i in platforms:
        i.draw()

    key = pygame.key.get_pressed()
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            exit()
        if key[pygame.K_RIGHT] and X < 205:
            if X + 50 < 180:
                X = X + 50
            else:
                X = 232
        if key[pygame.K_LEFT] and X > 0:
            if X - 50 > 5:
                X = X - 50
            else:
                X = 5
        if i.type == pygame.MOUSEBUTTONDOWN:
            if i.button == 3:
                h1 = Hero(7, random.randint(10, width - 100), random.randint(100, height - 200))
                h1_dr = True

    if h1_dr:
        sc_state.blit(inf_font.render(u"Сбито:" + str(h1.Count), 1, (255, 255, 255)), (10, 2))
    ball[0].rect.topleft = X, 310
    sc.blit(sc_game, (0, 20))
    sc.blit(sc_state, (0, 0))
    if h1.Count == 27:
        WinGame = True
        win_punkts = [(20, 120, 'Вы выйграли!!!', (255, 255, 30), (255, 30, 255), 0),
                      (130, 210, u'Exit', (255, 255, 30), (255, 30, 255), 1)]
        game = Menu(win_punkts)
        game.startMenu()

    clock.tick(FPS)
