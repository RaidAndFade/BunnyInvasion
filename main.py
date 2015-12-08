__author__ = 'Sepehr'
import pygame
import sys
from pygame.locals import *

pygame.init()

screen = pygame.display.set_mode((800,600))
clock = pygame.time.Clock()
pygame.font.init()

def drawBunny(x,y,dir):
    if dir == 0:
        pygame.draw.ellipse(screen, (255, 255, 255), (x, 20 + y, 50, 30)) #body
        pygame.draw.line(screen, (255, 255, 255), [6 + x, 35 + y], [6 + x, 60 + y], 3) #leg 1
        pygame.draw.line(screen, (255, 255, 255), [15 + x, 40 + y], [15 + x, 60 + y], 3) #leg 2
        pygame.draw.line(screen, (255, 255, 255), [30 + x, 40 + y], [30 + x, 60 + y], 3) #leg 3
        pygame.draw.line(screen, (255, 255, 255), [39 + x, 35 + y], [39 + x, 60 + y], 3) #leg 4
        pygame.draw.ellipse(screen, (255, 255, 255), (42 + x, 25 + y, 30, 20)) #head
        pygame.draw.circle(screen, (0, 0, 0), (64 + x, 32 + y), 2) #eye will remembr yuuuu
        pygame.draw.ellipse(screen, (255, 255, 255), (50 + x, 10 + y, 12, 20)) #faec
        pygame.draw.line(screen, (0, 0, 0), [60 + x, 40 + y], [69 + x, 40 + y], 1) #mout
    elif dir == 1:
        pygame.draw.ellipse(screen, (255, 255, 255), (x+22, 20 + y, 50, 30))
        pygame.draw.line(screen, (255, 255, 255), [6 + x+22, 35 + y], [6 + x+22, 60 + y], 3)
        pygame.draw.line(screen, (255, 255, 255), [15 + x+22, 40 + y], [15 + x+22, 60 + y], 3)
        pygame.draw.line(screen, (255, 255, 255), [30 + x+22, 40 + y], [30 + x+22, 60 + y], 3)
        pygame.draw.line(screen, (255, 255, 255), [39 + x+22, 35 + y], [39 + x+22, 60 + y], 3)
        pygame.draw.ellipse(screen, (255, 255, 255), (x, 25 + y, 30, 20))
        pygame.draw.circle(screen, (0, 0, 0), (12 + x, 32 + y), 2)
        pygame.draw.ellipse(screen, (255, 255, 255), (12 + x, 10 + y, 12, 20))
        pygame.draw.line(screen, (0, 0, 0), [3+x, 40 + y], [12 + x, 40 + y], 1)
    #pygame.draw.rect(screen,(0,0,0),(x,y,69,60))
    return Rect(x,y,69,60)

def drawLevel(x,level):
    if level == 0:
        pygame.draw.rect(screen,(0,255,0),(0,500,screen.get_width(),screen.get_height()-500))
        pygame.draw.rect(screen,(255,0,0),(400,300,100,10)),
        pygame.draw.rect(screen,(255,0,0),(200,150,100,10)),
        pygame.draw.rect(screen,(255,0,0),(100,400,100,10)),
        pygame.draw.rect(screen,(255,0,0),(600,200,100,10)),

collisions = [
    [
        Rect(0,500,screen.get_width(),screen.get_height()-500),
        Rect(400,300,100,10),
        Rect(200,150,100,10),
        Rect(100,400,100,10),
        Rect(600,200,100,10),
    ] 
]

def checkCollision(player,level):
    global yAccel, bunnyPos;
    colliding = False;
    # pygame.draw.rect(screen,(255,255,255),(bunnyPos[0],bunnyPos[1]-yAccel,player.w,yAccel))
    for collide in collisions[level]:
        print(collide,player)
        if not colliding:
            if yAccel>0:
                if Rect(bunnyPos[0],bunnyPos[1]-yAccel,player.w,yAccel).colliderect(collide):
                    yAccel = 0
                    return False
            else:
                if Rect(bunnyPos[0],bunnyPos[1],player.w,yAccel if yAccel > player.h else player.h).colliderect(collide):
                    yAccel = 0
                    bunnyPos[1] = collide.y-player.h+1
                    return True
    return False

curLevel = 0
bunnyPos = [0,0]
keysDown = [False]*400
yAccel = 0
isOnGround = True
facing = 0

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
        bunnyPos[0] -= 7
        facing = 1
    if keysDown[275]: #right
        bunnyPos[0] += 7
        facing = 0
    if keysDown[32]: #jump
        if isOnGround:
            yAccel = 20

    if yAccel > 0:
        bunnyPos[1] -= yAccel
        yAccel -= 1
    elif yAccel == 0 or yAccel < 0 and not isOnGround:
        bunnyPos[1] -= yAccel
        yAccel -= 1

    # Level(curLevel)



    drawLevel(0,curLevel)
    bunny = drawBunny(bunnyPos[0],bunnyPos[1],facing)

    isOnGround = checkCollision(bunny,curLevel)

    # collidingWith =  checkCollision(bunny,curLevel)
    # isOnGround = not collidingWith == False
    #
    # print(isOnGround)
    #
    # if isOnGround:
    #     yAccel = 0

    pygame.display.update()
