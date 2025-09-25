import pygame
import sys

class Video:
    def __init__(self, screen, cutscene):
        self.clock = pygame.time.Clock()
        self.spritesheet = pygame.image.load(cutscene).convert_alpha()
        self.FRAME_WIDTH, self.FRAME_HEIGHT = 800, 600
        self.NUM_FRAMES = 85
        self.frames = [
            self.spritesheet.subsurface(
                (i * self.FRAME_WIDTH, 0, self.FRAME_WIDTH, self.FRAME_HEIGHT)
            )
            for i in range(self.NUM_FRAMES)
        ]

    def play_cutscene(self, screen):
        for frame in self.frames:
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    pygame.quit()
                    sys.exit()

            screen.blit(frame, (0, 0))   # draw at top-left
            pygame.display.flip()
            self.clock.tick(10)          # 30 FPS

        # hold last frame for a bit before exiting
        pygame.time.wait(1000)
