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

surface = pygame.Surface((100, 100))
surface.fill(RED_COLOR)
rect = surface.get_rect()
rect.center = (300, 300)


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


def user_moving():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT] and keys[pygame.K_UP]:
        rect.x += 1
        rect.y -= 1
    elif keys[pygame.K_RIGHT] and keys[pygame.K_DOWN]:
        rect.x += 1
        rect.y += 1
    elif keys[pygame.K_LEFT] and keys[pygame.K_UP]:
        rect.x -= 1
        rect.y -= 1
    elif keys[pygame.K_LEFT] and keys[pygame.K_DOWN]:
        rect.x -= 1
        rect.y += 1
    elif keys[pygame.K_RIGHT]:
        rect.x += 1
    elif keys[pygame.K_LEFT]:
        rect.x -= 1
    elif keys[pygame.K_UP]:
        rect.y -= 1
    elif keys[pygame.K_DOWN]:
        rect.y += 1


def show_window():
    while True:
        event_handler()
        user_moving()
        screen.fill(GREEN_COLOR)
        screen.blit(surface, rect)
        pygame.display.update()


if __name__ == '__main__':
    show_window()
