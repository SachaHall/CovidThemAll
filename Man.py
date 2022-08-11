"""
made by Sacha Hallermeier
"""

import pygame
import sys
import os
import random
w, h = 1280, 720
white_m = pygame.image.load(os.path.join(
    sys.path[0], "images/hom_white.png"))
white_m = pygame.transform.rotozoom(white_m, 0, 1/3)
white_m_wm = pygame.image.load(os.path.join(
    sys.path[0], "images/hom_white_wm.png"))
white_m_wm = pygame.transform.rotozoom(white_m_wm, 0, 1/3)
white_m_ffp2 = pygame.image.load(os.path.join(
    sys.path[0], "images/hom_white_ffp2.png"))
white_m_ffp2 = pygame.transform.rotozoom(white_m_ffp2, 0, 1/3)
green_m = pygame.image.load(os.path.join(sys.path[0], "images/hom_green.png"))
green_m = pygame.transform.rotozoom(green_m, 0, 1/3)
green_m_wm = pygame.image.load(os.path.join(
    sys.path[0], "images/hom_green_wm.png"))
green_m_wm = pygame.transform.rotozoom(green_m_wm, 0, 1/3)
green_m_ffp2 = pygame.image.load(os.path.join(
    sys.path[0], "images/hom_green_ffp2.png"))
green_m_ffp2 = pygame.transform.rotozoom(green_m_ffp2, 0, 1/3)
red_m = pygame.image.load(os.path.join(sys.path[0], "images/hom_red.png"))
red_m = pygame.transform.rotozoom(red_m, 0, 1/3)
red_m_wm = pygame.image.load(os.path.join(
    sys.path[0], "images/hom_red_wm.png"))
red_m_wm = pygame.transform.rotozoom(red_m_wm, 0, 1/3)
red_m_ffp2 = pygame.image.load(os.path.join(
    sys.path[0], "images/hom_red_ffp2.png"))
red_m_ffp2 = pygame.transform.rotozoom(red_m_ffp2, 0, 1/3)
welcome = pygame.image.load(os.path.join(sys.path[0], "images/intro_CTA.jpg"))
next_level = pygame.image.load(
    os.path.join(sys.path[0], "images/next_level.jpg"))
end = pygame.image.load(os.path.join(sys.path[0], "images/end_scene.jpg"))


class Man:
    def __init__(self, speed, x, y, destination, infected, masked):
        self.speed = speed
        self.x = x
        self.y = y
        self.destination = destination
        self.infected = infected
        self.masked = masked
        self.direction = ""
        if self.infected:
            self.name = "player"
            self.score = 0
        else:
            self.name = ""
        if self.masked != 1 and self.masked != 2:
            self.masked = 0
        if self.infected:
            self.image = {0: white_m, 1: white_m_wm,
                          2: white_m_ffp2}.get(self.masked, white_m)
            self.probability = {0: 4, 1: 10, 2: 50}.get(self.masked, 5)
            self.direction = None
        else:
            if self.masked == 0:
                self.probability = 5
                self.image = green_m
            elif self.masked == 1:
                self.probability = 10
                self.image = green_m_wm
            elif self.masked == 2:
                self.probability = 50
                self.image = green_m_ffp2

    def find_l(self):
        try:
            self.m = (self.destination[1]-self.y)/(self.destination[0]-self.x)
        except:
            self.find_d()
            return None
        self.n = self.y-self.m*self.x

    def move(self):
        if self.x < self.destination[0]:
            self.x += self.speed
            self.y = self.m*self.x+self.n
        else:
            self.x -= self.speed
            self.y = self.m*self.x+self.n

    def find_d(self):
        self.destination = [random.randint(0, w-17), random.randint(0, h-17)]
        self.find_l()

    def arrived(self):
        return abs(self.x-self.destination[0]) < self.speed and abs(self.x-self.destination[0]) < self.speed

    def collide(self, other):
        return pygame.Rect(self.x, self.y, green_m.get_height(), green_m.get_width()).colliderect(pygame.Rect(other.x, other.y, green_m.get_height(), green_m.get_width()))

    def change_image(self):
        self.image = {0: red_m, 1: red_m_wm, 2: red_m_ffp2}.get(
            self.masked, self.image)

    def infect(self, other):
        if self.collide(other) and random.randint(1, self.probability) == 1 and random.randint(1, other.probability) == 1:
            if self.name == "player" and not other.infected:
                self.score += 1
            other.infected = True
            other.change_image()
            return True
        return False

    def walls(self):
        if self.x < 0 and self.direction == "Left":
            self.direction = "Right"
        elif self.x > w-self.image.get_width() and self.direction == "Right":
            self.direction = "Left"
        elif self.y < 0 and self.direction == "Up":
            self.direction = "Down"
        elif self.y > h-self.image.get_height() and self.direction == "Down":
            self.direction = "Up"

    def slide(self):
        self.walls()
        if self.direction == "Left":
            self.x -= self.speed
        elif self.direction == "Right":
            self.x += self.speed
        elif self.direction == "Up":
            self.y -= self.speed
        elif self.direction == "Down":
            self.y += self.speed
