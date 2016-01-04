__author__ = 'Sepehr'
import pygame
import sys
from pygame.locals import *
from random import randint

pygame.init()

screen = pygame.display.set_mode((800,900))
clock = pygame.time.Clock()
pygame.font.init()
# Fill background

i = 1

target = [600,500]
rocket = [50,20]

while True :
    clock.tick(60)

    #events
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            target[0] = event.pos[0]
            target[1] = event.pos[1]
    #game state
    surf = pygame.Surface((20,75))
    surf.fill((255,255,255))
    #pygame.draw.rect(surf,(0,0,0))
    pygame.draw.polygon(surf,(150,0,0),((0,25),(10,0),(20,25),(20,75),(0,75)))
    pygame.draw.rect(surf,(50,50,50),(0,25,20,50))

    blittedRect = screen.blit(surf, rocket)
    oldCenter = blittedRect.center
    rotatedSurf = pygame.transform.rotate(surf,270)
    rotRect = rotatedSurf.get_rect()
    rotRect.center = oldCenter

    screen.fill((255,255,255))
    screen.blit(rotatedSurf, rotRect)

    pygame.draw.circle(screen,(255,0,0),target,10)

    if rocket[0] < target[0]:
        rocket[0] += 4
    if rocket[0] > target[0]:
        rocket[0] -= 4

    if rocket[1] < target[1]:
        rocket[1] += 4
    if rocket[1] > target[1]:
        rocket[1] -= 4

    if pygame.Rect(rocket[0],rocket[1],20,75).collidepoint(target[0],target[1]):
        print("FUKING HIM RN BOIZ")

    pygame.display.update()
