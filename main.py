__author__ = 'Sepehr'
import pygame
import sys
from pygame.locals import *

pygame.init()

screen = pygame.display.set_mode((800,600))
clock = pygame.time.Clock()
pygame.font.init()

def drawBunny(x,y):
    pygame.draw.ellipse(screen, (255, 255, 255), (x, 20 + y, 50, 30))
    pygame.draw.line(screen, (255, 255, 255), [6 + x, 35 + y], [6 + x, 60 + y], 3)
    pygame.draw.line(screen, (255, 255, 255), [15 + x, 40 + y], [15 + x, 60 + y], 3)
    pygame.draw.line(screen, (255, 255, 255), [30 + x, 40 + y], [30 + x, 60 + y], 3)
    pygame.draw.line(screen, (255, 255, 255), [39 + x, 35 + y], [39 + x, 60 + y], 3)
    pygame.draw.ellipse(screen, (255, 255, 255), (42 + x, 25 + y, 30, 20))
    pygame.draw.circle(screen, (0, 0, 0), (64 + x, 32 + y), 2)
    pygame.draw.ellipse(screen, (255, 255, 255), (50 + x, 10 + y, 12, 20))
    pygame.draw.line(screen, (0, 0, 0), [60 + x, 40 + y], [69 + x, 40 + y], 1)
    #pygame.draw.rect(screen,(0,0,0),(x,y,69,60))
    return Rect(x,y,69,60)

def drawLevel(x,level):
    if level == 0:
        pygame.draw.rect(screen,(0,255,0),(0,500,screen.get_width(),screen.get_height()-500))

collisions = [
    [
        Rect(0,500,screen.get_width(),screen.get_height()-500)
    ]
]

def checkCollision(player,level):
    colliding = False;
    for collide in collisions[level]:
        print(collide,player)
        if not colliding:
            colliding = collide.colliderect(player)
            # pygame.draw.rect(screen,(0,0,0),collide);
            if colliding and not player.y == collide.y-player.h:
                bunnyPos[1] = collide.y-player.h
                return colliding

    return colliding

curLevel = 0
bunnyPos = [0,0]
keysDown = [False]*400
yAccel = 0
isOnGround = True

while True :
    clock.tick(60)
    screen.fill((0,255,255))

    #events
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            print(event.key)
            keysDown[event.key] = True
        if event.type == KEYUP:
            keysDown[event.key] = False

    #game state
    if keysDown[276]: #Left
        bunnyPos[0] -= 2
    if keysDown[275]: #right
        bunnyPos[0] += 2
    if keysDown[32]: #jump
        if isOnGround:
            yAccel = 20

    if yAccel > 0:
        bunnyPos[1] -= yAccel
        yAccel -= 1
    elif yAccel == 0 or yAccel < 0 and not isOnGround:
        bunnyPos[1] -= yAccel
        yAccel -= 1

    drawLevel(0,curLevel)
    bunny = drawBunny(bunnyPos[0],bunnyPos[1])

    isOnGround = checkCollision(bunny,curLevel)

    if isOnGround:
        yAccel = 0

    pygame.display.update()
