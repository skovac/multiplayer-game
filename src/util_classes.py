#!/usr/bin/python3

import pygame as pg


class LaserBase:
    
    def __init__(self, laserPic, width=10, height=10, speed=2):
        self.pic = pg.transform.scale(laserPic, (width, height))
        self.x = 0
        self.y = 0
        self.width = width
        self.height = height
        self.speed = speed
        self.isShot = False


class Projectiles:

    def __init__(self, laserPic, screen, screenHeight, timeout=60):
        self.lasers = [LaserBase(laserPic) for i in range(20)]
        self.screen = screen
        self.screenHeight = screenHeight
        self.timeout = timeout
        self.cooldown = timeout

    def refresh_position(self):
        self.cooldown += 1
        for laser in self.lasers:
            if laser.isShot and laser.y > 0 - laser.height:
                laser.y -= laser.speed
            else:
                laser.isShot = False
    
    def shoot(self, x, y):
        if self.cooldown < self.timeout:
            return
        for laser in self.lasers:
            if laser.isShot == False:
                laser.isShot = True
                laser.x = x - (laser.width / 2)
                laser.y = y
                self.cooldown = 0
                return

    def draw(self):
        for laser in self.lasers:
            if laser.isShot:
                self.screen.blit(laser.pic, (laser.x, laser.y))


class PlayerInfo:

    def __init__(self, screen, laserPic, ship, playerID="", x=0, y=0):
        self.screen = screen
        self.playerID = playerID
        self.x = x
        self.y = y
        self.lasers = [LaserBase(laserPic) for i in range(20)]
        self.lim = -50
        self.ship = pg.transform.scale(ship, (35, 35))

    def invert_values(self, WIDTH, HEIGHT, plW, plH):
        self.x = WIDTH - self.x - plW
        self.y = HEIGHT - self.y - plH

    def refresh_lasers(self):
        for laser in lasers:
            if laser.y < self.lim and laser.isShot:
                laser.isShot = False

    def draw(self):
        for laser in self.lasers:
            if laser.isShot:
                self.screen.blit(laser.pic, (laser.x, laser.y))

        self.screen.blit(self.ship, (self.x, self.y))



class PlayerShip:

    def __init__(self, pic, x, y, width, height, screenWidth, screenHeight, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.pic = pg.transform.scale(pic, (self.width, self.height))
        self.limLowx = 0
        self.limHighx = screenWidth - self.width
        self.limLowy = screenHeight / 2
        self.limHighy = screenHeight - self.height
        self.speed = speed

    def move(self, arg, distance, lim, isHigh):
        if isHigh and arg + distance > lim:
            return lim
        elif not isHigh and arg + distance < lim:
            return lim
        return arg + distance

    def move_left(self):
        self.x = self.move(self.x, self.speed * (-1), self.limLowx, 0)
    
    def move_right(self):
        self.x = self.move(self.x, self.speed, self.limHighx, 1)

    def move_up(self):
        self.y = self.move(self.y, self.speed * (-1), self.limLowy, 0)

    def move_down(self):
        self.y = self.move(self.y, self.speed, self.limHighy, 1)


