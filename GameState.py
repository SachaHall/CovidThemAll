"""
Made by Sacha Hallermeier
"""
import pygame
import random
import time
from Man import *
from functions_variables import *


class GameState:
    def __init__(self, screen, font, smaller_font):
        self.level = 0
        self.prepared = True
        self.did_intro = False
        self.player = Man(6, 500, 300, None, True, random.randint(0, 0))
        people = [Man(3, random.randint(0, w-17), random.randint(0, h-17),
                      [random.randint(0, w-17), random.randint(0, h-17)], False, random.randint(0, 0)) for i in range(20)]
        for i in people:
            i.find_l()
        self.people = people
        self.playing = True
        self.fontt = True
        self.font = font
        self.smaller_font = smaller_font
        self.timer_start = 0
        self.death = 0
        self.high_score_writing = 0
        self.total_time = 60
        self.high_score = high_score
        self.screen = screen

    def end_scene(self):
        global score
        self.screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.playing = True
                    self.fontt = True
                    direction = ""
                    self.timer_start = 0
                    self.player.score = 0
                    self.death = -1
                    self.total_time = 60
                    self.did_intro = False
                    self.prepared = True
                    self.high_score_writing = -1
                    self.people = [Man(3, random.randint(0, w-17), random.randint(0, h-17),
                                       [random.randint(0, w-17), random.randint(0, h-17)], False, random.randint(0, 0)) for i in range(20)]
                    for i in self.people:
                        i.find_l()
                    self.player = Man(6, 500, 300, None, True,
                                      random.randint(0, 0))
                    self.level = 0
        if self.death == 0:
            pygame.mixer.music.load(os.path.join(
                sys.path[0], "sounds/pacman_death.wav"))
            pygame.mixer.music.play()
            if self.high_score_writing == 0 and self.player.score > self.high_score:
                with open(os.path.join(sys.path[0], "highscore.txt"), "w") as f:
                    f.write(str(self.player.score))
                    self.high_score = self.player.score
        self.screen.blit(end, (0, 0))
        self.screen.blit(self.font.render(
            f"Score: {self.player.score}", True, (255, 255, 255)), (w/2-100, h/2-25))
        self.screen.blit(self.font.render(
            f"Highscore: {self.high_score}", True, (255, 255, 255)), (w/2-100, h/2+25))
        pygame.display.flip()
        self.death += 1
        self.high_score_writing += 1

    def intro(self):
        self.screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
            if event.type == pygame.KEYDOWN:
                if event.key == ord('w'):
                    pygame.mixer.music.load(os.path.join(
                        sys.path[0], "sounds/pacman_beginning.wav"))
                    pygame.mixer.music.play()
                else:
                    self.level = 1
                    self.did_intro = True
        if self.fontt == True:
            pygame.mixer.music.load(os.path.join(
                sys.path[0], "sounds/pacman_beginning.wav"))
            pygame.mixer.music.play()
        self.fontt = pygame.font.Font(pygame.font.get_default_font(), 45)
        self.screen.blit(welcome, ((w-welcome.get_width()) /
                                   2, (h-welcome.get_height())/2))
        pygame.display.flip()

    def between_levels(self):
        self.timer_start = 0
        self.screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.did_intro = True
                    self.prepared = False
        self.screen.blit(next_level, ((w-next_level.get_width()) /
                                      2, (h-next_level.get_height())/2))
        self.screen.blit(self.font.render(
            f"Score: {self.player.score}", True, (255, 255, 255)), (0, 0))
        self.screen.blit(self.font.render(
            f"Highscore: {self.high_score}", True, (255, 255, 255)), (0, 45))
        pygame.display.flip()

    def levels(self):
        if (self.level-1) % 3 == 0 and self.level != 1 and self.total_time > 30 and self.timer_start == 0:
            self.total_time -= 10
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
            if event.type == pygame.KEYDOWN:
                if event.key == ord('q'):
                    self.level = -1
                self.player.direction = {pygame.K_UP: "Up", pygame.K_DOWN: "Down",
                                         pygame.K_LEFT: "Left", pygame.K_RIGHT: "Right"}.get(event.key, self.player.direction)
        if self.timer_start == 0:
            self.timer_start = time.time()
        time_left = self.total_time - time.time() + self.timer_start
        self.screen.fill((0, 0, 0))
        check_people(self.people, self.player, self.screen)
        if self.prepared and is_winning(self.people):
            self.prepared = True
            self.did_intro = False
            self.level += 1
        self.player.slide()
        self.screen.blit(self.smaller_font.render(
            f"Score: {self.player.score}", True, (255, 255, 255)), (0, 0))
        self.screen.blit(self.smaller_font.render(
            f"Highscore: {self.high_score}", True, (255, 255, 255)), (0, 24))
        self.screen.blit(self.smaller_font.render(
            f"Timer: {int(time_left)%60}", True, (255, 255, 255)), (w-18*5, 0))
        self.screen.blit(self.player.image, (self.player.x, self.player.y))
        pygame.display.flip()
        if time_left < 0:
            self.level = -1

    def prepare_level2(self):
        self.screen.fill((0, 0, 0))
        people = [Man(3, random.randint(0, w-17), random.randint(0, h-17),
                      [random.randint(0, w-17), random.randint(0, h-17)], False, random.randint(0, 1)) for i in range(20)]
        for i in people:
            i.find_l()
        self.people = people
        player = Man(6, 500, 300, None, True, 0)
        player.score = self.player.score
        self.player = player
        self.prepared = True

    def prepare_level3(self):
        self.screen.fill((white))
        people = [Man(3, random.randint(0, w-17), random.randint(0, h-17),
                      [random.randint(0, w-17), random.randint(0, h-17)], False, random.randint(0, 1)) for i in range(15)]
        for i in people:
            i.find_l()

        self.people = people
        player = Man(6, 500, 300, None, True, 1)
        player.score = self.player.score
        self.player = player
        self.prepared = True

    def random_prepare(self):
        self.screen.fill(black)
        people = []
        for i in range(random.randint(10, 20)):
            a = random.randint(0, 4+self.level)
            if a < 3:
                people.append(Man(3, random.randint(0, w-17), random.randint(0, h-17),
                                  [random.randint(0, w-17), random.randint(0, h-17)], False, 0))
            elif a < self.level//2 + 4:
                people.append(Man(3, random.randint(0, w-17), random.randint(0, h-17),
                                  [random.randint(0, w-17), random.randint(0, h-17)], False, 1))
            else:
                people.append(Man(3, random.randint(0, w-17), random.randint(0, h-17),
                                  [random.randint(0, w-17), random.randint(0, h-17)], False, 2))
            people[-1].find_l()
        a = random.randint(0, len(people)-1)
        if people[a].masked == 2 or people[a].masked == 1:
            player = Man(6, 500, 300, None, True,
                         people[random.randint(0, len(people)-1)].masked)
        else:
            if people[a].masked == 2:
                player = Man(6, 500, 300, None, True, people[a].masked)
            else:
                player = Man(6, 500, 300, None, True,
                             people[random.randint(0, len(people)-1)].masked)
        player.score = self.player.score
        self.player = player
        self.people = people
        self.prepared = True

    def level_manager(self):
        if self.level == -1:
            self.end_scene()
        elif self.level == 0:
            self.intro()
        elif self.level == 1:
            self.levels()
        elif self.level == 2:
            if not self.did_intro:
                self.between_levels()
            if not self.prepared:
                self.prepare_level2()
            if self.prepared and self.did_intro:
                self.levels()
        elif self.level == 3:
            if not self.did_intro:
                self.between_levels()
            if not self.prepared:
                self.prepare_level3()
            if self.prepared and self.did_intro:
                self.levels()
        elif self.level > 3:
            if not self.did_intro:
                self.between_levels()
            if not self.prepared:
                self.random_prepare()
            if self.prepared and self.did_intro:
                self.levels()