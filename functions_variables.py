import sys
import os

black = (0, 0, 0)
white = (255, 255, 255)

with open(os.path.join(sys.path[0], "highscore.txt")) as f:
    high_score = int(f.read())


def check_people(to_infect, main_player, screen):
    for i in to_infect:
        if not i.arrived():
            i.move()
        else:
            i.find_d()
        main_player.infect(i)
        if i.infected:
            for j in to_infect[:to_infect.index(i)]+to_infect[to_infect.index(i)+1:]:
                i.infect(j)
        screen.blit(i.image, (i.x, i.y))


def is_winning(to_infect):
    return False not in [a.infected for a in to_infect]
