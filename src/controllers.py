from abc import ABC, abstractmethod
from enum import Enum

import pygame

from .settings import ControllerSettings


class Control:
    """Представляет один элемент управления на каком либо устройстве ввода.
    Это может быть клавиатура, геймпад, джойстик и т.д.
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
        self._accept = Control(0)
        self._quit = Control(0)

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

    @property
    def accept(self):
        return self._accept

    @property
    def quit(self):
        return self._quit

    @abstractmethod
    def conduct_survey_of_controls(self, events: list[pygame.event.Event]) -> None:
        '''Метод который нужно вызывать при каждой итерации игрового цикла
        чтобы понять какие котролы на контроллере были активированы.
        Получение значений c физического устройства осуществляется только после
        получения событий pygame.
        '''
        ...

    def deactivate_all_controls(self):
        self._move_right.deactivate()
        self._move_left.deactivate()
        self._move_up.deactivate()
        self._move_down.deactivate()
        self._accept.deactivate()
        self._quit.deactivate()


class PygameKeyboard(Controller):
    def __init__(self, settings: ControllerSettings):
        self._settings = settings
        self._move_right = Control(settings.right.value)
        self._move_up = Control(settings.up.value)
        self._move_left = Control(settings.left.value)
        self._move_down = Control(settings.down.value)
        self._accept = Control(pygame.K_RETURN)
        self._quit = Control(pygame.K_ESCAPE)

    def conduct_survey_of_controls(self, events) -> None:
        keys = pygame.key.get_pressed()
        if keys[self._move_right.key_number]:
            self._move_right.activate()
        if keys[self._move_left.key_number]:
            self._move_left.activate()
        if keys[self._move_up.key_number]:
            self._move_up.activate()
        if keys[self._move_down.key_number]:
            self._move_down.activate()
        if keys[self._accept.key_number]:
            self._accept.activate()
        if keys[self._quit.key_number]:
            self._quit.activate()

    def __str__(self):
        return "Keyboard"


class PygameIntermittentKeyboard(PygameKeyboard):
    def __init__(self, settings: ControllerSettings):
        super().__init__(settings)

    def conduct_survey_of_controls(self, events) -> None:
        for event in events:
            if event.type != pygame.KEYDOWN:
                continue
            if self._move_right.key_number == event.key:
                self._move_right.activate()
            elif self._move_left.key_number == event.key:
                self._move_left.activate()
            elif self._move_up.key_number == event.key:
                self._move_up.activate()
            elif self._move_down.key_number == event.key:
                self._move_down.activate()
            if self._accept.key_number == event.key:
                self._accept.activate()
            elif self._quit.key_number == event.key:
                self._quit.activate()

    def __str__(self):
        return "Intermittent Keyboard"


class GamePadAxe(Enum):
    LEFT_STICK_X = 0
    LEFT_STICK_Y = 1
    RIGHT_STICK_X = 2
    RIGHT_STICK_Y = 3
    LEFT_TRIGGER = 4
    RIGHT_TRIGGER = 5


class GamePadButton(Enum):
    A = 0
    B = 1
    X = 2
    Y = 3
    LB = 4
    RB = 5
    # элемента с номером 6 на моём Logitech F310 не оказалось
    START = 7
    LS = 8
    RS = 9


class PygameGamepad(Controller):
    def __init__(self):
        # Конструктор должен принимать геймпад, потому что играть можно на нескольких
        # геймпадах одновременно.
        self._game_pad = [
            pygame.joystick.Joystick(x)
            for x
            in range(pygame.joystick.get_count())
        ][0]
        self._dead_zone = 0.05
        self._move_up = Control(GamePadAxe.LEFT_STICK_Y.value)
        self._move_right = Control(GamePadAxe.LEFT_STICK_X.value)
        self._move_down = Control(GamePadAxe.LEFT_STICK_Y.value)
        self._move_left = Control(GamePadAxe.LEFT_STICK_X.value)
        self._accept = Control(GamePadButton.A.value)
        self._quit = Control(GamePadButton.B.value)

    def conduct_survey_of_controls(self, events) -> None:
        self._try_to_activate_stick_directions(
            axe=GamePadAxe.LEFT_STICK_X,
            positive_direction=self._move_right,
            negative_direction=self._move_left
        )
        self._try_to_activate_stick_directions(
            axe=GamePadAxe.LEFT_STICK_Y,
            positive_direction=self._move_down,
            negative_direction=self._move_up
        )
        self._try_to_activate_button(self._accept)
        self._try_to_activate_button(self._quit)

    def _try_to_activate_stick_directions(
        self,
        axe: GamePadAxe,
        positive_direction: Control,
        negative_direction: Control
    ) -> None:
        """Метод активирует одно из направлений выбранной оси стика
        если стик физического устройства был активирован.

        Args:
            axe: Одна из осей стика.
            positive_direction: Элемент управления контроллера,
            отвечающий за позитивное направление выбранной оси.
            negative_direction: Элемент управления контроллера,
            отвечающий за отрицательное направление выбранной оси.
        """
        value = self._game_pad.get_axis(axe.value)
        if not value:
            return

        if abs(value) <= self._dead_zone:
            return

        if value > 0:
            positive_direction.activate(value)
        else:
            negative_direction.activate(value)

    def _try_to_activate_button(self, button: Control) -> None:
        if self._game_pad.get_button(button.key_number):
            button.activate()

    def __str__(self):
        return self._game_pad.get_name()
