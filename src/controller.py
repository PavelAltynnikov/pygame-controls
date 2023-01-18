from abc import ABC, abstractmethod
from typing import Sequence

import pygame

import model
import settings


class Control:
    """Представляет один элемент управления на каком либо устройстве ввода.
    Это может быть клавиатура, геймпад, дойстик и т.д.
    """
    def __init__(self, key_number: int):
        self._key_number = key_number
        self._activated = False
        self._value = 0

    @property
    def key_number(self) -> int:
        return self._key_number

    @property
    def activated(self) -> bool:
        return self._activated

    @property
    def value(self) -> float:
        return self._value

    def update_key_number(self, key_number: int) -> None:
        self._key_number = key_number

    def activate(self, value: float = 1):
        """Должен вызываться при нажатии на реальный элемент управления контроллера.

        Args:
            value: Величина с которой произошло нажатие.
            Если не нужно учитывать величину нажатия, то по умолчанию значение 1.
        """
        self._activated = True
        self._value = value

    def deactivate(self):
        """Должен вызываться при отжатии реального элемента управления контроллера.
        """
        self._activated = False
        self._value = 0



class PygameKeyboardController(Controller):
    def __init__(self, settings: settings.ControlSettings):
        self._settings = settings
        self._move_right = Control(settings.right.value)
        self._move_up = Control(settings.up.value)
        self._move_left = Control(settings.left.value)
        self._move_down = Control(settings.down.value)

    @property
    def move_right(self):
        return self._move_right

    @move_right.setter
    def move_right(self, value: Control):
        self._move_right = value

    @property
    def move_left(self):
        return self._move_right

    @move_left.setter
    def move_left(self, value: Control):
        self._move_left = value

    @property
    def move_up(self):
        return self._move_up

    @move_up.setter
    def move_up(self, value: Control):
        self._move_up = value

    @property
    def move_down(self):
        return self._move_down

    @move_down.setter
    def move_down(self, value: Control):
        self._move_down = value

    def get_new_x(self, keys: Sequence[bool], start_x: int, speed: int) -> int:
        if keys[self._move_right.key_number]:
            return start_x + speed
        if keys[self._move_left.key_number]:
            return start_x - speed
        return start_x

    def get_new_y(self, keys: Sequence[bool], start_y: int, speed: int) -> int:
        if keys[self._move_up.key_number]:
            return start_y - speed
        if keys[self._move_down.key_number]:
            return start_y + speed
        return start_y


class Mover:
    def __init__(self, controller: Controller):
        self._controller = controller

    def move_character(self, character: model.Character):
        keys = pygame.key.get_pressed()
        speed = 1

        character.move_to(
            model.Point(
                x=self._controller.get_new_x(
                    keys,
                    character.location.x,
                    speed
                ),
                y=self._controller.get_new_y(
                    keys,
                    character.location.y,
                    speed
                )
            )
        )
