__author__ = 'Sepehr'
import pygame
import sys
from pygame.locals import *

pygame.init()

screen = pygame.display.set_mode((800,600))
clock = pygame.time.Clock()
pygame.font.init()
FontMono = pygame.font.SysFont("monospace", 15)
FontTitle = pygame.font.SysFont("monospace", 25)

#Things that are required for every level
def notify(msg,time):
    global notifmsg,notifTicks
    notifmsg = msg
    notifTicks = time*60

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
    #return bounding box of the bunny
    return Rect(x,y,69,60)

def drawPlatformer():
    global deathCount, score, bunnyPos, facing, levelXOff, isOnGround, furthest, canFall, yAccel, dead
    dead = False
    for checkpoint in checkPoints:
        if startPos[0]<checkpoint[0]:
            pygame.draw.line(screen,c[0],[checkpoint[0]-levelXOff,0],[checkpoint[0]-levelXOff,screen.get_height()])
    for rect in collisions:
        pygame.draw.rect(screen,rect[0],(rect[1].x-levelXOff,rect[1].y,rect[1].w,rect[1].h))
    if keysDown[276]: #Left
        if bunnyPos[0] < screen.get_width()/2 and levelXOff > 0:
            levelXOff -= 7
        else:
            bunnyPos[0] -= 7
        facing = 1
    if keysDown[275]: #right
        if bunnyPos[0] > screen.get_width()/2:
            levelXOff += 7
        else:
            bunnyPos[0] += 7
        if levelXOff+bunnyPos[0] > furthest:
            score+=14
            furthest = levelXOff+bunnyPos[0]
        facing = 0
    if keysDown[32]: #jump
        if isOnGround:
            yAccel = 20
    if keysDown[96+24]:
        canFall = not canFall
        keysDown[120] = False

    if yAccel > 0:
        bunnyPos[1] -= yAccel
        yAccel -= 1
    elif yAccel == 0 or yAccel < 0 and not isOnGround and canFall:
        bunnyPos[1] -= yAccel
        yAccel -= 1
        #print("lel")

    if bunnyPos[1] > screen.get_height():
        dead=True
    if dead:
        yAccel = 0
        levelXOff = 0 if startPos[0] < screen.get_width()/2 else int(startPos[0]-screen.get_width()/2)
        bunnyPos[0] = startPos[0] if startPos[0] < screen.get_width()/2 else int(screen.get_width()/2)
        bunnyPos[1] = startPos[1]
        deathCount+=1
        score-=(deathCount**2)
    bunny = drawBunny(bunnyPos[0],bunnyPos[1],facing)
    isOnGround = checkCollision(bunny,levelXOff)

#colors. to shorten the collisions code. sorry fam

#level 1 [Platformer]
c = [
    (255,0,0), #red = 0
    (0,255,0), #green 1
    (0,0,255), #blue 2
    (0,255,255), #skyblue 3
    (255,255,0), #yellow 4
    (255,255,255), #white 5
    (0,0,0), #black 6
    (255,0,255), #purple?
]

#color, Rectangle, CanColide
collisions = [
    [c[4],Rect(0,300,100,10),True],
    [c[2],Rect(400,400,100,10),True],
    [c[2],Rect(500,300,100,10),True],
    [c[2],Rect(600,100,20,10),True],
    [c[2],Rect(800,200,10,10),True],
    [c[2],Rect(1000,400,2,2),True],
    [c[2],Rect(1200,400,2,2),True],
    [c[2],Rect(1500,400,2,2),True],
    [c[2],Rect(1800,400,2,2),True],
    [c[4],Rect(2000,200,100,10),True],
    [c[1],Rect(2200,300,10,10),True],
    [c[1],Rect(2300,300,100,10),False],
    [c[1],Rect(2400,300,10,10),True],
    [c[1],Rect(2500,300,100,10),False],
    [c[1],Rect(2600,300,10,10),True],
    [c[1],Rect(2700,300,100,10),False],
    [c[1],Rect(2800,300,10,10),False],
    [c[1],Rect(2900,400,10,10),True],
    [c[1],Rect(3000,300,100,10),True],
    [c[1],Rect(3400,400,100,10),True],
    [c[1],Rect(3400,400,100,10),True],
    [c[1],Rect(3400,400,100,10),True],
    [c[1],Rect(3400,400,100,10),True],

    [c[3],Rect(5000,400,100,10),True],

    [c[4],Rect(10000,200,100,10),True],
    [c[2],Rect(10400,300,100,10),True],
    [c[3],Rect(10800,300,100,10),True],
    [c[2],Rect(10900,100,100,10),True],
    [c[0],Rect(11200,500,60,10),True],
    [c[1],Rect(11400,400,10,5),True],
    [c[1],Rect(11600,300,100,5),True],
    [c[1],Rect(11800,100,3,4),True],
    [c[1],Rect(12000,100,9,4),True],
    [c[1],Rect(12200,100,12,4),True],
    [c[1],Rect(12400,100,15,4),True],
    [c[2],Rect(12800,300,10,10),True],
    [c[2],Rect(12900,150,100,2),True],
    [c[2],Rect(13100,50,100,2),True],
    [c[2],Rect(13300,500,100,2),True],
    [c[2],Rect(13600,300,10,2),True],
    [c[2],Rect(13650,150,100,2),True],
    [c[1],Rect(13700,50,50,2),True],
    [c[1],Rect(13900,50,50,2),True],
    [c[0],Rect(14200,500,50,2),True],
    [c[0],Rect(14500,300,50,2),True],
    [c[0],Rect(14800,100,50,2),True],
    [c[4],Rect(15100,50,50,2),True],
    [c[1],Rect(15300,400,100,2),True],
    [c[2],Rect(15500,300,10,2),True],
    [c[1],Rect(15700,200,10,2),True],
    [c[0],Rect(15900,200,10,2),True],
    [c[1],Rect(16100,100,100,10),True],
]
checkPoints = [
    [2000,170,"Not all things are real"],
    #5000
    [10000,200,"Sometimes, you just don't know."],
    [15100,40,"If you're lost... I'll find you."]
]

def checkCollision(player,xOff):
    global yAccel, bunnyPos, startPos;
    colliding = False;
    # pygame.draw.rect(screen,(255,255,255),(bunnyPos[0],bunnyPos[1]-yAccel,player.w,yAccel))
    for checkpoint in checkPoints:
        if bunnyPos[0]+xOff > checkpoint[0]:
            if startPos[0] < checkpoint[0]:
                startPos = checkpoint
                notify(checkpoint[2],3)
    for rect in collisions:
        collide = Rect(rect[1].x-xOff,rect[1].y,rect[1].w,rect[1].h)
        if not colliding and rect[2]:
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
startPos = [0,0]
bunnyPos = [startPos[0],startPos[1]]
keysDown = [False]*400
dead = False
yAccel = 0
isOnGround = True
facing = 0
levelXOff = 0
deathCount = 0
score = 0
frames = 0
furthest = 0
canFall = True
notifmsg = ""
notifTicks = 0

notify("Arrow Keys to move, Spacebar to Jump",5)

while True :
    clock.tick(60)
    frames += 1
    if frames >= 60:
        frames = 0
    if frames % 60 == 0:
        score -= 20
    screen.fill((0,255,255))
    #events
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            keysDown[event.key] = True
        if event.type == KEYUP:
            keysDown[event.key] = False

    #game 0...
     # Level(curLevel)

    drawPlatformer()

    scoreLabel = FontMono.render("Score : "+str(score),5,c[6])
    deathCountLabel = FontMono.render("Deaths : "+str(deathCount),5,c[6])
    screen.blit(scoreLabel,(0,0))
    screen.blit(deathCountLabel,(0,20))
    if notifTicks > 0:
        notifTicks-=1
        notification = FontTitle.render(notifmsg, 15, c[6])
        screen.blit(notification,(screen.get_width()/2-len(notifmsg)*25/3.5,screen.get_height()/2))

    # print(bunny,bunnyPos,dead,isOnGround)


    pygame.display.update()
