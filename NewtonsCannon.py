import pygame
import math
from scipy.constants import G
from Button import Button

pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption("Newton's Cannon")

WINDOW_SIZE = (800, 800)
screen = pygame.display.set_mode(WINDOW_SIZE)

G /= (1000 ** 3)
EARTH_MASS = 5.97 * (10 ** 24)
EARTH_RADIUS = 6371
dt = 1
x_0 = 400
y_0 = 400
run = True
start = False
velocity = 7.3
phi = 0


class Earth:

    def __init__(self, x, y, radius, mass):
        self.x = x + x_0
        self.y = y + y_0
        self.radius = radius
        self.mass = mass
        self.position = (x, y)
        self.color = "blue"

    def draw(self):
        pygame.draw.circle(
            screen, self.color, (self.x, self.y), self.radius / 50
        )


class Cannonball:

    def __init__(self, x=0, y=0, vel_0=0, phi_0=0, mnt_h=1500):
        self.vel_0 = vel_0
        self.x = x + x_0
        self.y = y + y_0 - (EARTH_RADIUS + mnt_h) / 100
        self.x_r = 20000
        self.mnt_h = mnt_h
        self.y_r = 20000 - EARTH_RADIUS - self.mnt_h
        self.new_x = -10
        self.new_y = -10
        self.a_x = 0
        self.a_y = 0
        self.v_x = vel_0 * math.cos(phi_0 * math.pi / 180)
        self.v_y = -vel_0 * math.sin(phi_0 * math.pi / 180)
        self.r = EARTH_RADIUS + mnt_h

    def move(self):
        a_r = -(G * EARTH_MASS / self.r ** 2)
        self.a_x = a_r * (self.x_r - 20000) / self.r
        if self.x > 20000:
            self.a_x = - self.a_x
        self.a_y = a_r * (self.y_r - 20000) / self.r
        if self.y > 20000:
            self.a_y = - self.a_y
        self.v_x = self.v_x + self.a_x * dt
        self.v_y = self.v_y + self.a_y * dt
        self.x_r = self.x_r + self.v_x * dt + 0.5 * self.a_x * dt ** 2
        self.y_r = self.y_r + self.v_y * dt + 0.5 * self.a_y * dt ** 2
        self.new_x = self.x_r / 50
        self.new_y = self.y_r / 50
        self.r = math.sqrt((self.x_r - 20000) ** 2 + (self.y_r - 20000) ** 2)

    def draw(self):
        pygame.draw.circle(
            screen, "red", (self.new_x, self.new_y), 7
        )

    def restart(self, x, y, vel_0, phi_0, mnt_h=1500):
        self.vel_0 = velocity
        self.x = x + x_0
        self.y = y + y_0 - (EARTH_RADIUS + mnt_h) / 100
        self.x_r = 20000
        self.mnt_h = mnt_h
        self.y_r = 20000 - EARTH_RADIUS - self.mnt_h
        self.new_x = -10
        self.new_y = -10
        self.a_x = 0
        self.a_y = 0
        self.v_x = vel_0 * math.cos(phi_0 * math.pi / 180)
        self.v_y = -vel_0 * math.sin(phi_0 * math.pi / 180)
        self.r = EARTH_RADIUS + mnt_h


earth_img = pygame.image.load('images/Earth.png').convert_alpha()
earth_img = pygame.transform.scale(earth_img, (256, 256))
mountain_img = pygame.image.load('images/mountain.png').convert_alpha()
mountain_img = pygame.transform.scale(mountain_img, (64, 54))

button_1_img = pygame.image.load('images/button_1.png').convert_alpha()
button_10_img = pygame.image.load('images/button_10.png').convert_alpha()
button_min1_img = pygame.image.load('images/button_sub1.png').convert_alpha()
button_min10_img = pygame.image.load('images/button_sub10.png').convert_alpha()
button_01_img = pygame.image.load('images/button_01.png').convert_alpha()
button_min01_img = pygame.image.load('images/button_sub01.png').convert_alpha()

start_img = pygame.image.load('images/button_start.png').convert_alpha()
play_img = pygame.image.load('images/button_play.png').convert_alpha()
pause_img = pygame.image.load('images/button_pause.png').convert_alpha()
exit_img = pygame.image.load('images/button_exit.png').convert_alpha()

start_button = Button(420, 10, start_img, 1)
play_button = Button(515, 10, play_img, 1)
pause_button = Button(610, 10, pause_img, 1)
exit_button = Button(705, 10, exit_img, 1)


v_add_1 = Button(245, 17, button_1_img, 1)
v_add_0_1 = Button(285, 17, button_01_img, 1)
v_sub_1 = Button(325, 17, button_min1_img, 1)
v_sub_0_1 = Button(365, 17, button_min01_img, 1)

phi_add_10 = Button(245, 73, button_10_img, 1)
phi_add_1 = Button(285, 73, button_1_img, 1)
phi_sub_10 = Button(325, 73, button_min10_img, 1)
phi_sub_1 = Button(365, 73, button_min1_img, 1)

x_trace = []
y_trace = []

cannonball = Cannonball(vel_0=velocity, phi_0=phi)
earth = Earth(0, 0, EARTH_RADIUS, EARTH_MASS)

while run:
    clock.tick(7200)

    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, "white", pygame.Rect(10, 10, 400, 50), 2, 3)
    pygame.draw.rect(screen, "white", pygame.Rect(10, 65, 400, 50), 2, 3)

    if start_button.draw(screen):
        cannonball.restart(x=0, y=0, vel_0=velocity, phi_0=phi)
        x_trace.clear()
        y_trace.clear()
        if not start:
            start = True
    if pause_button.draw(screen):
        if start:
            start = False
    if play_button.draw(screen):
        if not start:
            start = True
    if exit_button.draw(screen):
        run = False

    if v_add_1.draw(screen):
        velocity += 1

    if v_add_0_1.draw(screen):
        velocity += 0.1

    if v_sub_1.draw(screen):
        velocity -= 1

    if v_sub_0_1.draw(screen):
        velocity -= 0.1

    if phi_add_10.draw(screen):
        phi += 10

    if phi_add_1.draw(screen):
        phi += 1

    if phi_sub_10.draw(screen):
        phi -= 10

    if phi_sub_1.draw(screen):
        phi -= 1

    earth.draw()

    for i in range(len(x_trace)):
        pygame.draw.circle(
            screen, "red", (x_trace[i], y_trace[i]), 1
        )

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if start:
        if cannonball.r > EARTH_RADIUS:
            cannonball.move()
            cannonball.draw()
            x_trace.append(cannonball.new_x)
            y_trace.append(cannonball.new_y)
        if cannonball.new_x > 800 or cannonball.new_y > 800:
            start = False

    font = pygame.font.SysFont('OpenSans', 26)
    velocity_text = font.render('Velocity: ' + str(round(velocity, 1)) + ' km/s', True, (255, 255, 255))
    screen.blit(velocity_text, (20, 25))
    phi_text = font.render('Angle: ' + str(phi) + u'\u00b0', True, (255, 255, 255))
    screen.blit(phi_text, (20, 80))

    screen.blit(earth_img, (272, 272))
    screen.blit(mountain_img, (370, 241))

    cannonball.draw()

    pygame.display.update()
