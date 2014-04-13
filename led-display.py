#!/usr/bin/python
# -*- coding: utf-8 -*-

##
# "Fake" LED Display message ( pygame )
# David Art <david.madbox@gmail.com>
# font : http://www.dafont.com/fr/display-otf.font
##

import pygame
#~ from pygame.locals import *
from pygame import Color

## True / False
FULL_SCREEN = 0
## window size if not fullscreen
WIN_SIZE = (480, 320)
## background color
BG_COLOR = Color("black")
## font color
FG_COLOR = ((0, 255, 0),        # green
            (255, 0, 60),       # red
            (0, 0, 255),        # blue
            (238, 0, 238),      # magenta
            (145, 45, 238),     # purple
            (255, 127, 0))      # drakorange

class Display:

    ind_color = 0

    def __init__(self, message, speed=1.0, fontname="font.ttf", color=None):

        self.speed = speed
        self.fontname = fontname
        if color:
            self.color = Color(color)
        else:
            self.color = FG_COLOR[0]

        pygame.init()
        pygame.mouse.set_visible(False)
        info = pygame.display.Info()
        flags = pygame.HWSURFACE|pygame.DOUBLEBUF

        if FULL_SCREEN:
            self.width = info.current_w
            self.height = info.current_h
            self.screen = pygame.display.set_mode([info.current_w, info.current_h],
                pygame.FULLSCREEN|flags)
        else:
            self.width = WIN_SIZE[0]
            self.height = WIN_SIZE[1]
            self.screen = pygame.display.set_mode(WIN_SIZE, flags)

        self.clock = pygame.time.Clock()
        self.font_size = int(self.height * .9)
        self.message = message
        self.render()
        self.pos = self.width
        (self.fontrender_w, self.fontrender_h) = self.font.size(message)

    def render(self):
        #~ self.font = pygame.font.SysFont("freemono", self.font_size)
        self.font = pygame.font.Font(self.fontname, self.font_size)
        self.fontrender = self.font.render(self.message, 1, FG_COLOR[self.ind_color])

    def update(self):
        now = pygame.time.get_ticks()
        duration = now - self.timer
        self.timer = now
        speed = self.width * self.speed / 2000
        dist = speed * duration
        self.pos -= dist
        if self.pos < -self.fontrender_w:
            self.pos = self.width
        self.can_draw = True

    def draw(self):
        if self.can_draw:
            self.screen.fill(BG_COLOR)
            pos_y = (self.height - self.fontrender_h) / 2
            self.screen.blit(self.fontrender, (self.pos, pos_y))
            pygame.display.flip()

    def changeColor(self, operator):
        if operator == "+":
            self.ind_color += 1
            if self.ind_color >= len(FG_COLOR):
                self.ind_color = 0
        else:
            self.ind_color -= 1
            if self.ind_color < 0:
                self.ind_color = len(FG_COLOR) - 1
        self.render()

    def changeSpeed(self, operator):
        if operator == "+" and self.speed < 5:
            self.speed += .25
        elif operator == "-" and self.speed >= .5:
            self.speed -= .25

    def run(self):

        self.timer = pygame.time.get_ticks()
        self.running = True

        while self.running:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_UP:
                        self.changeSpeed("+")
                    elif event.key == pygame.K_DOWN:
                        self.changeSpeed("-")
                    elif event.key == pygame.K_LEFT:
                        self.changeColor("-")
                        self.font_size -= 1
                    elif event.key == pygame.K_RIGHT:
                        self.changeColor("+")
                        self.font_size += 1

            self.update()
            self.draw()
            #~ self.clock.tick(60)

if __name__ == "__main__":

    message = "Raspberry 3.14159265359"
    display = Display(message)
    display.run()
