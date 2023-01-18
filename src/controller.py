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


class Controller(ABC):
    """Представляет физическое устройство ввода команд."""
    def __init__(self):
        self._move_up = Control(0)
        self._move_right = Control(0)
        self._move_down = Control(0)
        self._move_left = Control(0)

    @property
    def move_right(self):
        return self._move_right

    @move_right.setter
    def move_right(self, value: Control):
        self._move_right = value

    @property
    def move_left(self):
        return self._move_left

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

    @abstractmethod
    def conduct_survey_of_controls(self) -> None:
        '''Метод который нужно вызывать при каждой итерации игрового цикла
        чтобы понять какие котролы на контроллере были активированы.
        '''
        ...

    def deactivate_all_controls(self):
        self._move_right.deactivate()
        self._move_left.deactivate()
        self._move_up.deactivate()
        self._move_down.deactivate()


class Mover:
    def __init__(self, controller: Controller):
        self._controller = controller

    def move_character(self, character: model.Character):
        speed = 0
        character.move_to(
            model.Point(
                x=self._get_new_x(character.location.x, speed),
                y=self._get_new_y(character.location.y, speed)
            )
        )

    def _get_new_x(self, start_x: float, speed: float) -> float:
        if self._controller.move_right.activated:
            return start_x + self._controller.move_right.value + speed
        if self._controller.move_left.activated:
            return start_x - abs(self._controller.move_left.value) - speed
        return start_x

    def _get_new_y(self, start_y: float, speed: float) -> float:
        if self._controller.move_up.activated:
            return start_y - abs(self._controller.move_up.value) - speed
        if self._controller.move_down.activated:
            return start_y + self._controller.move_down.value + speed
        return start_y
