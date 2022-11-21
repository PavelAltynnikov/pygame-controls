import pygame


SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 500
SCREEN_CAPTION = 'Controls tests'
GREEN_COLOR = (30, 89, 89)
RED_COLOR = (250, 50, 50)

pygame.init()
pygame.key.set_repeat(1)
pygame.display.set_caption(SCREEN_CAPTION)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


class Character:
    def __init__(self):
        self.surface = pygame.Surface((100, 100))
        self.surface.fill(RED_COLOR)
        self.rect = self.surface.get_rect()
        self.rect.center = (300, 300)

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and keys[pygame.K_UP]:
            self.rect.x += 1
            self.rect.y -= 1
        elif keys[pygame.K_RIGHT] and keys[pygame.K_DOWN]:
            self.rect.x += 1
            self.rect.y += 1
        elif keys[pygame.K_LEFT] and keys[pygame.K_UP]:
            self.rect.x -= 1
            self.rect.y -= 1
        elif keys[pygame.K_LEFT] and keys[pygame.K_DOWN]:
            self.rect.x -= 1
            self.rect.y += 1
        elif keys[pygame.K_RIGHT]:
            self.rect.x += 1
        elif keys[pygame.K_LEFT]:
            self.rect.x -= 1
        elif keys[pygame.K_UP]:
            self.rect.y -= 1
        elif keys[pygame.K_DOWN]:
            self.rect.y += 1

    def draw(self, screen):
        screen.blit(self.surface, self.rect)


def is_quit(event):
    return (
        event.type == pygame.QUIT
        or (event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_q))
    )


def event_handler():
    events = pygame.event.get()
    for event in events:
        if is_quit(event):
            pygame.display.quit()


def show_window(character):
    while True:
        event_handler()
        character.move()

        screen.fill(GREEN_COLOR)
        character.draw(screen)

        pygame.display.update()


if __name__ == '__main__':
    character = Character()
    show_window(character)
