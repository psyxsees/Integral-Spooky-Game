import pygame

class Environment:
    def __init__(self, image_path, position=(0, 0)):
        # Load the texture
        self.texture = pygame.image.load(image_path).convert_alpha()
        self.rect = self.texture.get_rect(topleft=position)

    def draw(self, surface):
        surface.blit(self.texture, self.rect)
