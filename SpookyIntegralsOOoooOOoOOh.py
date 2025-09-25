import pygame
import random
import math
from CutscenePlayer import Video
from sympy import sympify
from DrawScene import Environment
from IntegralSolver import IntegralSolver

# pygame setup
fps = 60
WIDTH, HEIGHT = 800, 600
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
clock.tick(fps)
running = True
dead = False
END_TIME = (60 * fps) * 1  # 1 minute = 3600 ticks at 60 FPS, 5 minutes to win
won = False
font = pygame.font.SysFont("consolas", 20)

DEATH_CUTSCENE = Video(screen, "cutscenes/death/monsterkill.png")

PINS = Environment("textures/pins.png", position=(0, 0))
DEATH_OVERLAY = Environment("textures/blood.png", position=(0, 0))
MAP = Environment("textures/map.png", position=(0, 0))
HQ = Environment("textures/hq.png", position=(WIDTH/2 - 32, HEIGHT/2))
SOLVER = Environment("textures/integralinator.png", position=(WIDTH - 256, HEIGHT - 256))
EXCLAMATION = Environment("textures/exclamation.png", position=(0, 0))
CHARGES = Environment("textures/charge.png", position=(WIDTH - 200, 10))
CORRUPTING = Environment("textures/Corrupting.png", position=(32, 0))

INTEGRAL_SOLVER = IntegralSolver()
integrals = [None, None, None]  # 3 quadrants

STORE_START_TICK = [0, 0, 0]  # tick when integral was spawned in each quadrant, meant to offset the tick for rate of change calculations
QUADRANT_AREA = 1000000  # area for each quadrant
CORRUPTED = [0, 0, 0]  # corruption level for each quadrant, when it reaches a threshold(QUADRANT_AREA), game over
MOST_CORRUPTED = 0 # index of most corrupted quadrant in CORRUPTED
SEC_PER_COOLDOWN = 10  # seconds before corruption starts adding
COOLDOWN = [60 * SEC_PER_COOLDOWN, 60 * SEC_PER_COOLDOWN, 60 * SEC_PER_COOLDOWN]# cooldown timer for each quadrant before CORRUPTION starts adding
DISAPATE = [60 * SEC_PER_COOLDOWN, 60 * SEC_PER_COOLDOWN, 60 * SEC_PER_COOLDOWN]# cooldown until Intgral goes away on its own
NUM_PINS = [50, 50, 50] # number of pins alive in each quadrant
tick = 0

charges = 3  # number of electric shocks available
online = True  # whether you have power or not, if false you can't input commands
rechargeTime = 60 * (SEC_PER_COOLDOWN * 2)  # time until you get another electric shock charge

# input system
input_text = ""

print("Welcome to Spooky Integrals OOoOOoOOoOoh!")
print("Press ~ for commands / help.")

def help():
    print("Press: 1,2,3 inside window to access quadrant commands")
    print("Commands:")
    print("int - Integrate the equation")
    print("der - Differentiate the integrated equation and get rate of change at current time")
    print()
    print("Space - Use electric shock to clear a quadrant of its integral (resets corruption cooldown)")
    print("And input into the console which quadrant to shock (1,2,3)")
    print()
    print("press k to give up")

def spawnIntegral(i):
    quadrant = random.randint(0, 2)
    for i in range(3):
        if integrals[i] is None:
            quadrant = i
            break
    newIntegral = INTEGRAL_SOLVER.IntegralTerminal()
    integrals[quadrant] = newIntegral
    print(INTEGRAL_SOLVER.MakeReadable(newIntegral["equation"]), "- Q" + str(quadrant + 1))

    # store the tick when the integral was spawned to offset rate of change calculations
    STORE_START_TICK[quadrant] = tick

def handleCommand(activeQuadrant):
    cmd = input("cmd- ")

    eq = integrals[activeQuadrant]

    if (cmd == "int"):
        if (eq is None):
            print("No active integral in this quadrant.")
            return
        result = INTEGRAL_SOLVER.SolveIntegral(eq["equation"])
        eq["int"] = result
        print("Integrated:", INTEGRAL_SOLVER.MakeReadable(result))
    elif (cmd == "der"):
        if (eq["int"] is None):
            print("You must integrate before differentiating.")
            return
        deriv = INTEGRAL_SOLVER.SolveDerivative(eq["int"])
        eq["der"] = deriv
        print("Derivative:", INTEGRAL_SOLVER.MakeReadable(deriv))

        rate = INTEGRAL_SOLVER.RateOfChange(deriv, tick)
        eq["rate"] = rate
        print("Rate at t=" + str(tick) + ": " + str(rate))
    else:
        print("Unknown command. Use int or der.")

def addCorruption():
    global running
    global dead

    for i in range(3):
        if integrals[i] is not None:
            rate = INTEGRAL_SOLVER.RateOfChange(integrals[i]["derivative"], tick)
            if rate.is_real and rate >= 0:
                # proceed
                # doesn't start adding until cooldown is over, this allows the player time to react to a rate that is too high to counteract within one tick
                if (COOLDOWN[i] <= 0 and DISAPATE[i] > 0):
                    CORRUPTED[i] += max(float(INTEGRAL_SOLVER.RateOfChange(integrals[i]["derivative"], tick - STORE_START_TICK[i])), 0)
                    DISAPATE[i] -= 1
                elif (DISAPATE[i] <= 0):
                    integrals[i] = None
                    COOLDOWN[i] = (60 * SEC_PER_COOLDOWN) * 10
                    DISAPATE[i] = (60 * SEC_PER_COOLDOWN) * random.randint(10, 20)
                else:
                    COOLDOWN[i] -= 1
                    # add exclamation marks over corrupted quadrants while in cooldown
                    EXCLAMATION.draw(screen)
            if (CORRUPTED[i] >= QUADRANT_AREA):
                print("Game Over! Quadrant" + str(i+1) + "is fully corrupted.")
                running = False
                dead = True
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
        if (CORRUPTED[i] > 0):
            NUM_PINS[i] = max(0, int(50 * (1 - (CORRUPTED[i] / QUADRANT_AREA))))
        else:
            NUM_PINS[i] = 50

def electricShock():
    global charges
    global online

    activeQuadrant = 0
    print("* Select Quadrant to Shock *")
    activeQuadrant = int(input("Input Quadrant- "))

    if (activeQuadrant >= 1 and activeQuadrant <= 3):
        integrals[activeQuadrant - 1] = None
        COOLDOWN[activeQuadrant - 1] = (60 * SEC_PER_COOLDOWN) * 10
        charges -= 1
        if (charges < 0):
            charges = 0
            print("No charges left!")
            online = False

def pulseBloodOverlay():
    global MOST_CORRUPTED

    MOST_CORRUPTED = CORRUPTED.index(max(CORRUPTED))

    alpha = ((CORRUPTED[MOST_CORRUPTED] / QUADRANT_AREA) * 255)
    alpha = alpha * (abs(math.sin(tick / 10)))  # pulse effect
    alpha = max(0, min(255, alpha))  # clamp between 0 and 255
    CORRUPTING.setAlpha(alpha)
    DEATH_OVERLAY.setAlpha(alpha)

def intro_cutscene():
    intro_lines = [
        "A strange entity in the caverns of a National Park is spreading.",
        "Electric Fields seem to keep it at bay.",
        "Your goal is to study its rate of growth...",
        "and make calculated decisions...",
        "on when to suppress the entity, and when to hold back.",
        "You have unlimited power, but it takes time to recharge.",
        "And your boss has a stick up his ass today",
        "so he's turned all of the data...",
        "INTO INTEGRALS!!!",
        "Use your handy dandy Integral-inator to do a little cheating...",
        "because Integration by parts is TOO HARD!",
        "And what we need is a derivative to calculate the Change.",
        "BTW",
        "Try not to die :)"
    ]

    screen.fill((0, 0, 0))
    pygame.display.flip()
    pygame.time.wait(1000)

    for line in intro_lines:
        screen.fill((0, 0, 0))
        text = font.render(line, True, (255, 255, 255))
        screen.blit(text, ((WIDTH/2) - (text.get_width()/2), HEIGHT/2))
        pygame.display.flip()
        pygame.time.wait(2500)  # show each line for 2.5 seconds

    # final wait and clear
    screen.fill((0, 0, 0))
    cont_text = font.render("Press any key to continue...", True, (200, 200, 200))
    screen.blit(cont_text, ((WIDTH/2) - (cont_text.get_width()/2), HEIGHT/2))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False

intro_cutscene()

while running:
    clock.tick(fps)

    if tick >= END_TIME and not dead:
        print("I was gonna make a cutscene for the win state but didn't feel like it. You win!")
        running = False
        won = True

    if (online):
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
                elif event.key == pygame.K_SPACE:
                    electricShock()
                elif event.key == pygame.K_k:
                    running = False
                    dead = True
                else:
                    input_text += event.unicode

    if (charges < 3):
        rechargeTime -= 1
    if (rechargeTime <= 0):
        charges += 1
        rechargeTime = 60 * (SEC_PER_COOLDOWN * 2)

    # draw scene
    screen.fill((0, 0, 0))
    PINS.draw(screen)
    DEATH_OVERLAY.draw(screen)
    MAP.draw(screen)
    HQ.draw(screen)
    CORRUPTING.draw(screen)
    SOLVER.draw(screen)

    # draw charges
    for i in range (charges):
        CHARGES.rect.topleft = (WIDTH/2 - 16, (HEIGHT / 2) + (i * 50) + 80)
        CHARGES.draw(screen)

    # add corruption over time
    addCorruption()
    pulseBloodOverlay()

    # occasionally spawn new integrals
    if (random.randint(0, 1000) == 0):
        spawnIntegral(3)

    pygame.display.flip()
    tick += 1

if dead:
    DEATH_CUTSCENE.play_cutscene(screen)
    # simple win screen
    screen.fill((0, 0, 0))
    fail_text = font.render("YOU DEAD!", True, (255, 0, 0))
    screen.blit(fail_text, ((WIDTH/2) - (fail_text.get_width()/2), HEIGHT/2))
    pygame.display.flip()
    pygame.time.wait(5000)  # show for 5 seconds
elif won:
    # simple win screen
    screen.fill((0, 0, 0))
    win_text = font.render("YOU WIN!", True, (0, 255, 0))
    screen.blit(win_text, (WIDTH/2 - win_text.get_width()//2, HEIGHT/2))
    pygame.display.flip()
    pygame.time.wait(5000)  # show for 5 seconds
else:
    print("Game exited.")

pygame.quit()