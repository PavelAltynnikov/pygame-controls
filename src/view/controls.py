from abc import ABC, abstractmethod
from typing import Callable

import pygame

# Эти зависимости мешают тестировать модуль
import settings
import controllers


class Control(ABC):
    def __init__(self, location: tuple[int, int] = (0, 0)):
        self.location = location
        self.is_active = False  # переименовать в is_focused

    @abstractmethod
    def draw(self, screen):
        pass


class Label(Control):
    def __init__(
            self,
            font: pygame.font.Font,
            text: str,
            antialias=False,
            color: tuple[int, int, int] = (0, 0, 0),
            location=(0, 0)):
        super().__init__(location)
        self._font = font
        self._antialias = antialias
        self._color = color
        self._surface = None
        self.location = location
        self.update_surface_from_text(text)

    def update_surface_from_text(self, text) -> None:
        self._surface = self._font.render(text, self._antialias, self._color)

    def draw(self, screen):
        screen.blit(self._surface, self.location)


class Key(Label):
    def __init__(
            self,
            font,
            setting: settings.Setting,
            control: controllers.Control,
            antialias=False,
            color=(0, 0, 0),
            location=(0, 0)):
        key_value = pygame.key.name(setting.value)
        super().__init__(
            font,
            key_value,
            antialias,
            color,
            location
        )
        self._setting = setting
        self._control = control

    def change_text(self, value):
        self._surface: pygame.surface.Surface = self._font.render(
            value, self._antialias, self._color
        )

    def activate(self):
        self.is_active = True

    def deactivate(self):
        self.is_active = False

    def draw_frame(self, screen):
        rect = self._surface.get_rect()
        rect.topleft = self.location

        pygame.draw.rect(
            surface=screen,
            color=(0, 0, 0),
            rect=rect,
            width=2
        )


class Button(Label):
    def __init__(self, font, text, antialias, color, location):
        super().__init__(font, text, antialias, color, location)
        self._handlers = []

    def add_click_handler(self, handler: Callable) -> None:
        self._handlers.append(handler)

    def click(self) -> None:
        for handler in self._handlers:
            handler()

    def activate(self):
        self.is_active = True

    def deactivate(self):
        self.is_active = False

    def draw_frame(self, screen):
        rect = self._surface.get_rect()  # type: ignore
        rect.topleft = self.location

        pygame.draw.rect(
            surface=screen,
            color=(0, 0, 0),
            rect=rect,
            width=2
        )

    def draw(self, screen):
        super().draw(screen)
        if self.is_active:
            self.draw_frame(screen)


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
    def __init__(self, label: Label, key: Key, location=(0, 0)):
        super().__init__(location)
        flag = ActiveFlag(location=(location[0], location[1] + 10), size=(10, 10))

        label.location = (location[0] + 10, location[1])
        key.location = (location[0] + 150, location[1])

        self.label = label
        self.key = key
        self._controls: list[Control] = [label, key, flag]

    def activate(self):
        self._activation_toggle(True)

    def deactivate(self):
        self._activation_toggle(False)

    def draw(self, screen):
        for component in self._controls:
            component.draw(screen)

    def _activation_toggle(self, is_active):
        self._is_active = is_active
        for component in self._controls:
            if isinstance(component, ActiveFlag):
                component.is_active = is_active
