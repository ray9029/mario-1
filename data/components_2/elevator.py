import pygame as pg
from .. import setup
from .. import constants as c

class Elevator(pg.sprite.Sprite):
    def __init__(self, x, y, width, height, min_y, max_y, speed):
        pg.sprite.Sprite.__init__(self)
        self.image = setup.GFX['elevator']
        self.image = pg.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.min_y = min_y
        self.max_y = max_y
        self.speed = speed
        self.direction = 1

    def update(self, *args):
        self.rect.y += self.speed * self.direction
        if self.rect.y <= self.min_y or self.rect.y >= self.max_y:
            self.direction *= -1
