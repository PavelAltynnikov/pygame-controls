from abc import ABC, abstractmethod
from typing import Sequence

import pygame

import model
import settings


class Control:
    def __init__(self, key_number):
        self.key_number = key_number


class Controller(ABC):
    @property
    @abstractmethod
    def move_right(self) -> Control:
        ...

    @move_right.setter
    @abstractmethod
    def move_right(self, value: Control):
        ...

    @property
    @abstractmethod
    def move_left(self) -> Control:
        pass

    @move_left.setter
    @abstractmethod
    def move_left(self, value: Control):
        ...

    @property
    @abstractmethod
    def move_up(self) -> Control:
        ...

    @move_up.setter
    @abstractmethod
    def move_up(self, value: Control):
        ...

    @property
    @abstractmethod
    def move_down(self) -> Control:
        pass

    @move_down.setter
    @abstractmethod
    def move_down(self, value: Control):
        ...

    @abstractmethod
    def get_new_x(self, keys: Sequence[bool], start_x: int, speed: int) -> int:
        pass

    @abstractmethod
    def get_new_y(self, keys: Sequence[bool], start_y: int, speed: int) -> int:
        pass


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
