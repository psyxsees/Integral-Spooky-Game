import pygame
import random
from sympy import sympify
from DrawScene import Environment
from IntegralSolver import IntegralSolver

# pygame setup
WIDTH, HEIGHT = 800, 600
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True
font = pygame.font.SysFont("consolas", 20)

MAP = Environment("textures/map.png", position=(0, 0))
PINS = Environment("textures/pins.png", position=(0, 0))
HQ = Environment("textures/hq.png", position=(WIDTH/2 - 32, HEIGHT/2))
SOLVER = Environment("textures/integralinator.png", position=(WIDTH - 256, HEIGHT - 256))

INTEGRAL_SOLVER = IntegralSolver()
integrals = [None, None, None]  # 3 quadrants
QUADRANT_AREA = 1000000  # area for each quadrant
CORRUPTED = [0, 0, 0]  # corruption level for each quadrant, when it reaches a threshold(QUADRANT_AREA), game over
NUM_PINS = [50, 50, 50] # number of pins alive in each quadrant
tick = 0

# input system
input_text = ""

print("Welcome to Spooky Integrals OOoOOoOOoOoh!")
print("Press ~ for commands / help.")

def help():
    print ("Press: 1,2,3 inside window to access quadrant commands")
    print ("Commands:")
    print ("int - Integrate the equation")
    print ("der - Differentiate the integrated equation and get rate of change at current time")

def spawnIntegral():
    quadrant = random.randint(0, 2)
    newIntegral = INTEGRAL_SOLVER.IntegralTerminal()
    integrals[quadrant] = newIntegral
    print(INTEGRAL_SOLVER.MakeReadable(newIntegral["equation"]), "- Q" + str(quadrant + 1))

def handleCommand(active_quadrant):
    global tick
    cmd = input("cmd- ")

    eq = integrals[active_quadrant]

    if cmd == "int":
        result = INTEGRAL_SOLVER.SolveIntegral(eq["equation"])
        eq["int"] = result
        print("Integrated:", INTEGRAL_SOLVER.MakeReadable(result))
    elif cmd == "der":
        if eq["int"] is None:
            print("You must integrate before differentiating.")
            return
        deriv = INTEGRAL_SOLVER.SolveDerivative(eq["int"])
        eq["der"] = deriv
        print("Derivative:", INTEGRAL_SOLVER.MakeReadable(deriv))

        rate = INTEGRAL_SOLVER.RateOfChange(deriv, tick)
        eq["rate"] = rate
        print(f"Rate at t={tick}: {rate}")
    else:
        print("Unknown command. Use int or der.")

def addCorruption():
    for i in range(3):
        if integrals[i] is not None:
            if INTEGRAL_SOLVER.RateOfChange(integrals[i]["derivative"], tick) >= 0:
                print ("add corruption")
                CORRUPTED[i] += float(INTEGRAL_SOLVER.RateOfChange(integrals[i]["derivative"], tick))
            if (CORRUPTED[i] >= QUADRANT_AREA):
                print(f"Game Over! Quadrant {i+1} is fully corrupted.")
                running = False
                return
            # draw corruption bar
            pygame.draw.rect(screen, (255, 0, 0), (10 + i*260, HEIGHT - 30, (CORRUPTED[i]/QUADRANT_AREA)*250, 20))
            pygame.draw.rect(screen, (255, 255, 255), (10 + i*260, HEIGHT - 30, 250, 20), 2)
            # draw number of pins
            pin_text = font.render("Pins: " + str(NUM_PINS[i]), True, (255, 255, 255))
            screen.blit(pin_text, (10 + i*260, HEIGHT - 60))
        else:
            # no active integral in this quadrant
            pygame.draw.rect(screen, (100, 100, 100), (10 + i*260, HEIGHT - 30, 250, 20), 2)
            pin_text = font.render("Pins: " + str(NUM_PINS[i]), True, (255, 255, 255))
            screen.blit(pin_text, (10 + i*260, HEIGHT - 60))
        
        # reduce pins based on corruption
        if CORRUPTED[i] > 0:
            NUM_PINS[i] = 50 - (50 / (CORRUPTED[i] / QUADRANT_AREA))
        else:
            NUM_PINS[i] = 50

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                print("Selected Q1")
                handleCommand(0)
            elif event.key == pygame.K_2:
                print("Selected Q2")
                handleCommand(1)
            elif event.key == pygame.K_3:
                print("Selected Q3")
                handleCommand(2)
            elif event.key == pygame.K_BACKQUOTE:
                help()
            else:
                input_text += event.unicode

    # draw scene
    screen.fill((0, 0, 0))
    MAP.draw(screen)
    PINS.draw(screen)
    HQ.draw(screen)
    SOLVER.draw(screen)

    # add corruption over time
    addCorruption()

    # occasionally spawn new integrals
    if random.randint(0, 500) == 0:
        spawnIntegral()

    pygame.display.flip()
    clock.tick(60)
    tick += 1

pygame.quit()
