#!/usr/bin/python3
# -*- coding: utf-8 -*-

##
# "Fake" LED Display message ( pygame )
# David Art <david.madbox@gmail.com> 
##

import pygame
from font import char

FPS = 30
## True / False 
FULLSCREEN = False
## window size if not fullscreen
WIN_SIZE = (720, 480)
##  min 10, max = 30
MAX_COL = 17
## background color
BG_COLOR = (0, 0, 0)
## font color
FG_COLOR = ((0, 255, 0), # green
            (255, 0, 60), # red
            (0, 0, 255), # blue
            (238, 0, 238), # magenta
            (145, 45, 238), # purple
            (240, 240, 60), # yellow
            (255, 127, 0), # drakorange
            (255, 255, 255), # white
            (78, 238, 148)) # seagreen
            

class Led:

    def __init__(self, width, height, model="circle"):
        self.width = width
        self.height = height
        self.model = model

    def draw(self, screen, x, y, color):
        if self.model == "rect":
            pygame.draw.rect(screen, color, [x+1, y+1, self.width-2, self.height-2])
        elif self.model == "circle":
            pygame.draw.ellipse(screen, color, [x, y, self.width, self.height])

class Display:

    ind_color = 0
    anim_count = 0
    speed = 10

    def __init__(self, msg, ledmodel="rect", screen=None):

        ## FIXME! 
        if screen:
            # use this screen to display
            # need to get size (width/height) to setup Led
            self.screen = screen
        else:
            pygame.init()
            info = pygame.display.Info()

            if FULLSCREEN:
                self.width = info.current_w
                self.height = info.current_h
                self.screen = pygame.display.set_mode([info.current_w, info.current_h], pygame.FULLSCREEN)
            else:
                self.width = WIN_SIZE[0]
                self.height = WIN_SIZE[1]
                self.screen = pygame.display.set_mode(WIN_SIZE)

            pygame.time.set_timer(pygame.USEREVENT, 1000 / FPS)

        self.led_w = self.width / float(MAX_COL)
        # 9 =  7 (lines) + 1 margin-top + 1 margin-bottom
        self.led_h = self.height / 9.0
        self.led = Led(self.led_w, self.led_h, ledmodel)

        self.setMessage(msg.lower())

    def setMessage(self, message):
        ## FIXME! complete rewrite needed ..
        ## just a quick a hack to test
        self.msg = message
        self.buffer = ["0"*MAX_COL] * 7
        for letter in message:
            if letter in char:
                ch = char[letter].split()
                for l in range(7):
                    self.buffer[l] += ch[l] + " "
            else:
                for l in range(7):
                    self.buffer[l] += " " * 6
        for l in range(7):
            self.buffer[l] += "0" * MAX_COL
        self.index = 0

    def update(self):
        self.anim_count += 1
        if self.anim_count < self.speed:
            return
        self.anim_count = 0
        self.index += 1
        if self.index > len(self.buffer[0])-MAX_COL:
            self.index = 0

    def draw(self):
        self.screen.fill(BG_COLOR)
        for line in range(7):
            for col in range(MAX_COL):
                x = col * self.led_w + 1
                y = self.led_h + line * self.led_h + 1
                if self.buffer[line][self.index+col] == '1':
                    self.led.draw(self.screen, x, y, FG_COLOR[self.ind_color])
        self.update()

    def changeColor(self, operator="+"):
        if operator == "+":
            self.ind_color += 1
            if self.ind_color >= len(FG_COLOR):
                self.ind_color = 0
        else:
            self.ind_color -= 1
            if self.ind_color < 0:
                self.ind_color = len(FG_COLOR) - 1

    def changeSpeed(self, operator="+"):
        if operator == "+" and self.speed > 0:
            self.speed -= 1
        elif operator == "-" and self.speed < 15:
            self.speed += 1

    def run(self):
        while True:
            ev = pygame.event.wait()
            if ev.type == pygame.QUIT:
                break
            if ev.type == pygame.USEREVENT:
                self.draw()
                pygame.display.flip()
            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    break
                elif ev.key == pygame.K_UP:
                    self.changeSpeed("+")
                elif ev.key == pygame.K_DOWN:
                    self.changeSpeed("-")
                elif ev.key == pygame.K_LEFT:
                    self.changeColor("-")
                elif ev.key == pygame.K_RIGHT:
                    self.changeColor("+")

if __name__ == "__main__":

    ## model : rect / circle
    model = "circle"
    message = "Raspberry 3.14159265359"
    display_message = Display(message, model) 
    display_message.run()
