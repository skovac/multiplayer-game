#!/usr/bin/python3

import pygame as pg
import json


ship = pg.image.load("media/blueship.png")
oppShip = pg.transform.rotate(ship, 180)
laserPic = pg.image.load("media/laser.png")
laserPic = pg.transform.scale(laserPic, (10, 10))


class LaserBase:
    
    def __init__(self, width=10, height=10, speed=2):
        self.x = 0
        self.y = 0
        self.width = width
        self.height = height
        self.speed = speed
        self.isShot = False


class Projectiles:

    def __init__(self, screen, screenHeight, timeout=60):
        self.lasers = [LaserBase() for i in range(20)]
        self.pic = laserPic
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
    
    def shoot(self, x, y, shipWidth):
        if self.cooldown < self.timeout:
            return
        for laser in self.lasers:
            if laser.isShot == False:
                laser.isShot = True
                laser.x = x - (laser.width / 2) + (shipWidth / 2)
                laser.y = y
                self.cooldown = 0
                return


class PlayerShip:

    def __init__(self, x, y, width, height, screenWidth, screenHeight, speed, screen):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.ship = pg.transform.scale(ship, (self.width, self.height))
        self.disconnected = False
        self.limLowx = 0
        self.limHighx = screenWidth - self.width
        self.limLowy = screenHeight / 2
        self.limHighy = screenHeight - self.height
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.speed = speed
        self.proj = Projectiles(screen, screenHeight)
        self.screen = screen

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

    def invert_values(self):
        self.x = self.screenWidth - self.x - self.width
        self.y = self.screenHeight - self.y - self.height

        for laser in self.proj.lasers:
            if laser.isShot:
                laser.x = self.screenWidth - laser.x - laser.width
                laser.y = self.screenHeight - laser.y - laser.height

    def rotate_pic(self):
        self.ship = pg.transform.rotate(self.ship, 180)

    def draw(self):
        for laser in self.proj.lasers:
            if laser.isShot:
                self.screen.blit(self.proj.pic, (laser.x, laser.y))

        self.screen.blit(self.ship, (self.x, self.y))

    def toJson(self):
        data = {}
        data["x"] = self.x
        data["y"] = self.y

        i = 0
        laserData = [(0, 0) for i in range(20)]
        for laser in self.proj.lasers:
            laserData[i] = (laser.x, laser.y)
            i += 1

        data["nbOfLasers"] = i
        data["lasers"] = laserData

        return json.dumps(data)

    def fromJson(self, jsonString):
        if not jsonString:
            self.disconnected = True
            return

        data = json.loads(jsonString)

        self.x = data["x"]
        self.y = data["y"]

        for i in range(data["nbOfLasers"]):
            self.proj.lasers[i].x, self.proj.lasers[i].y = data["lasers"][i]
            self.proj.lasers[i].isShot = True

        self.invert_values()
