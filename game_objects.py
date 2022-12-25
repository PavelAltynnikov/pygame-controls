import pygame

import settings


class Character:
    def __init__(self, control: settings.UserControlSettings):
        self.surface = pygame.Surface((100, 100))
        self.surface.fill((250, 50, 50))
        self.rect = self.surface.get_rect()
        self.rect.center = (300, 300)
        self._control = control

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[self._control.move_right] and keys[self._control.move_up]:
            self.rect.x += 1
            self.rect.y -= 1
        elif keys[self._control.move_right] and keys[self._control.move_down]:
            self.rect.x += 1
            self.rect.y += 1
        elif keys[self._control.move_left] and keys[self._control.move_up]:
            self.rect.x -= 1
            self.rect.y -= 1
        elif keys[self._control.move_left] and keys[self._control.move_down]:
            self.rect.x -= 1
            self.rect.y += 1
        elif keys[self._control.move_right]:
            self.rect.x += 1
        elif keys[self._control.move_left]:
            self.rect.x -= 1
        elif keys[self._control.move_up]:
            self.rect.y -= 1
        elif keys[self._control.move_down]:
            self.rect.y += 1

    def draw(self, screen):
        screen.blit(self.surface, self.rect)
