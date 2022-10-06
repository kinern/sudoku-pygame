import pygame
from pygame.locals import *

class AlertBox():
    def __init__(self, pos, text, size, fontSize, bgColor=(255,255,255), fontColor=(80,80,80)):
        self.x, self.y = pos
        self.active = False
        self.bgColor = bgColor
        self.fontColor = fontColor
        self.font = pygame.font.SysFont("Verdana", fontSize)
        self.text = self.font.render(text, 1, pygame.Color(self.fontColor))
        self.size = size
        self.surface = pygame.Surface(self.size)
        self.surface.fill(self.bgColor)
        self.surface.blit(self.text, (int(self.size[0]/2)-int(self.text.get_rect().width/2), int(self.size[1]/2)-int(self.text.get_rect().height/2)))
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])

    def show(self):
        self.active = True
    
    def hide(self):
        self.active = False

    def click(self, event):
        x, y = pygame.mouse.get_pos()
        if (not self.rect.collidepoint(x, y)):
            self.hide()