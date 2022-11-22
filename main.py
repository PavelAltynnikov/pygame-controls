import pygame
import settings

from abc import ABC, abstractmethod

pygame.init()
pygame.key.set_repeat(500)


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


class Control(ABC):
    def __init__(self, location=(0, 0)):
        self.location = location
        self.is_active = False

    @abstractmethod
    def draw(self, screen):
        pass


class Label(Control):
    def __init__(self, font, text, antialias=False, color=(0, 0, 0), location=(0, 0)):
        super().__init__(location)
        self._surface = font.render(text, antialias, color)
        self.location = location

    def draw(self, screen):
        screen.blit(self._surface, self.location)


class Key(Label):
    def __init__(self, font, text, antialias=False, color=(0, 0, 0), location=(0, 0)):
        super().__init__(font, text, antialias, color, location)


class ActiveFlag(Control):
    def __init__(self, location=(0, 0), size=(1, 1), color=(0, 0, 0)):
        super().__init__(location)
        self._surface = pygame.Surface(size)
        self._surface.fill(color)
        self._rect = self._surface.get_rect()
        self._rect.center = location

    def draw(self, screen):
        if self.is_active:
            screen.blit(self._surface, self._rect)


class RowSetting(Control):
    def __init__(self, label: Control, key: Control, location=(0, 0)):
        super().__init__(location)
        flag = ActiveFlag(location=(location[0], location[1] + 10), size=(10, 10))

        label.location = (location[0] + 10, location[1])
        key.location = (location[0] + 150, location[1])

        self._controls: list[Control] = [label, key, flag]

    def activate(self, is_active):
        self._is_active = is_active
        for component in self._controls:
            component.is_active = is_active

    def draw(self, screen):
        for component in self._controls:
            component.draw(screen)


class SettingWindow(Window):
    def __init__(self, caption, size):
        super().__init__(caption, size)
        self._controls: list[RowSetting] = []
        self._initialize_components()

    def _initialize_components(self):
        font = pygame.font.SysFont('Consolas', 25)

        right_setting = RowSetting(Label(font, 'right'), Key(font, ">"), location=(50, 50))
        right_setting.activate(True)
        self._controls.append(right_setting)

        left_setting = RowSetting(Label(font, 'left'), Key(font, "<"), location=(50, 80))
        self._controls.append(left_setting)

        up_setting = RowSetting(Label(font, 'up'), Key(font, "^"), location=(50, 110))
        self._controls.append(up_setting)

        down_setting = RowSetting(Label(font, 'down'), Key(font, "v"), location=(50, 140))
        self._controls.append(down_setting)

        self._selected_item_index = 0

    def _draw(self):
        for control in self._controls:
            control.draw(self._screen)

    def show(self):
        blue_color = (0, 49, 83)
        while self._is_showing:
            events = pygame.event.get()
            self._quit_if_user_wants_to_close_window(events)

            self._screen.fill(blue_color)
            self._draw()

            pygame.display.update()


if __name__ == '__main__':
    window = GameWindow(
        caption='Controls tests',
        size=(1000, 500),
        character=Character(settings.UserControlSettings())
    )
    window.show()
