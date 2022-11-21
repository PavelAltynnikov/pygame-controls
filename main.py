import pygame

from abc import ABC, abstractmethod

pygame.init()
pygame.key.set_repeat(500)


class Character:
    def __init__(self):
        self.surface = pygame.Surface((100, 100))
        self.surface.fill((250, 50, 50))
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


class Window(ABC):
    def __init__(self, caption, size):
        self._caption = caption
        self._size = size
        self._screen = pygame.display.set_mode(size)
        self._is_showing = True
        pygame.display.set_caption(caption)

    @staticmethod
    def _quit_button_is_pressed(event):
        return (
            event.type == pygame.QUIT
            or (event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_q))
        )

    def _quit_if_user_wants_to_close_window(self, events):
        for event in events:
            if self._quit_button_is_pressed(event):
                self.quit()

    @abstractmethod
    def show(self):
        pass

    def quit(self):
        self._is_showing = False


class GameWindow(Window):
    def __init__(self, caption, size, character):
        super().__init__(caption, size)
        self._character = character

    def _open_settings_window_if_needed(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                settings = SettingWindow(f'{self._caption} | Settings', self._size)
                settings.show()

    def show(self):
        green_color = (30, 89, 89)
        while self._is_showing:
            events = pygame.event.get()
            self._quit_if_user_wants_to_close_window(events)
            self._open_settings_window_if_needed(events)

            self._character.move()

            self._screen.fill(green_color)
            self._character.draw(self._screen)

            pygame.display.update()


class SettingWindow(Window):
    def __init__(self, caption, size):
        super().__init__(caption, size)

    def show(self):
        blue_color = (0, 49, 83)
        while self._is_showing:
            events = pygame.event.get()
            self._quit_if_user_wants_to_close_window(events)

            self._screen.fill(blue_color)

            pygame.display.update()


if __name__ == '__main__':
    window = GameWindow(
        caption='Controls tests',
        size=(1000, 500),
        character=Character()
    )
    window.show()
