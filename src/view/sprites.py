import pygame

# сомневаюсь что тут должна быть эта зависимость
import model


class Sprite:
    def __init__(self, model: model.Character):
        self.surface = pygame.Surface((100, 100))
        self.surface.fill((250, 50, 50))
        self.rect = self.surface.get_rect()
        self.rect.center = (300, 300)
        self._character = model

    def update(self):
        self.rect.x = self._character.location.x  # type: ignore
        self.rect.y = self._character.location.y  # type: ignore

    def draw(self, screen):
        screen.blit(self.surface, self.rect)
