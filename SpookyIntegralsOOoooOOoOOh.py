# Example file showing a basic pygame "game loop"
import pygame
import sys
import os
import random

from DrawScene import Environment;
from IntegralSolver import IntegralSolver;

# pygame setup
WIDTH, HEIGHT = 800, 600
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True

MAP = Environment("textures/map.png", position=(0,0));
PINS = Environment("textures/pins.png", position=(0, 0));
HQ = Environment("textures/hq.png", position=(WIDTH/2 - 32, HEIGHT/2));
SOLVER = Environment("textures/integralinator.png", position=(WIDTH - 256, HEIGHT - 256));

INTEGRAL_SOLVER = IntegralSolver();
integrals = [[], [], []]
ID = 0
command = ""
i = 0 # quadrant set
randomIntegral = 0
tick = 0

def inputs():
    ID = input() # input id
    for j in range(len(integrals[i])):
        if (integrals[i][j][0] == ID):
            break;

    # int for integrate
    # der for derivative - this will be encrypted until you've integrated and called SolveDerivative()
    command = input() # input command
    if (command == "int"):
        integrals[randomIntegral][i][2].INTEGRAL_SOLVER.SolveIntegral(integrals[randomIntegral][i][1])
        print("Integrated: " + INTEGRAL_SOLVER.MakeReadable(integrals[randomIntegral][i][2]))
    if (command == "der"):
        integrals[randomIntegral][i][3].INTEGRAL_SOLVER.MakeReadable(INTEGRAL_SOLVER.SolveDerivative(integrals[randomIntegral][i][2]))
        integrals[randomIntegral][i][4].INTEGRAL_SOLVER.RateOfChange(integrals[randomIntegral][i][2], tick)
        integrals[randomIntegral][i][4] *= clock.get_fps() # per second
        print("Derivative: " + INTEGRAL_SOLVER.MakeReadable(integrals[randomIntegral][i][3]))
        print("Rate Of Growth at t=" + str(tick) + ": " + str(integrals[randomIntegral][i][4]) + " per second")

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill background
    screen.fill((0, 0, 0))

    # Draw environment texture
    MAP.draw(screen)
    PINS.draw(screen)
    HQ.draw(screen)
    SOLVER.draw(screen)

    randomIntegral = random.randint(0, 1000)
    if (randomIntegral == 0):
        randomIntegral = random.randint(0, 2)
        if (randomIntegral == 0):
            integrals[0].append(INTEGRAL_SOLVER.IntegralTerminal())
            print(INTEGRAL_SOLVER.MakeReadable(integrals[0][len(integrals) - 1][1]) + " - Q1")
        elif (randomIntegral == 1):
            integrals[1].append(INTEGRAL_SOLVER.IntegralTerminal())
            print(INTEGRAL_SOLVER.MakeReadable(integrals[1][len(integrals) - 1][1]) + " - Q2")
        elif (randomIntegral == 2):
            integrals[2].append(INTEGRAL_SOLVER.IntegralTerminal())
            print(INTEGRAL_SOLVER.MakeReadable(integrals[2][len(integrals) - 1][1]) + " - Q3")
    
    keys = pygame.key.get_pressed()
    if (keys[pygame.K_1]):
        print("You selected Q1. Please input the ID of the integral you wish to solve:")
        i = 0
        inputs()
    elif (keys[pygame.K_2]):
        print("You selected Q2. Please input the ID of the integral you wish to solve:")
        i = 1
        inputs()
    elif (keys[pygame.K_3]):
        print("You selected Q3. Please input the ID of the integral you wish to solve:")
        i = 2
        inputs()

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60
    tick += 1

pygame.quit()