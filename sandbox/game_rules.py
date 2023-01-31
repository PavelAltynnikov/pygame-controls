from .model import Character
from .controllers import Controller


class Mover:
    def __init__(self, controller: Controller):
        self._controller = controller
        self._gravitation = 0.005
        self._start_speed = -1.5
        self._current_speed = 0

    def move_character(self, character: Character):
        character.change_x(self._calculate_x(speed=0))
        character.change_y(self._calculate_y(character))

    def reset(self, character: Character):
        self._current_speed = 0
        character.is_jumping = False

    def _calculate_x(self, speed: float) -> float:
        if self._controller.move_right.activated:
            return self._controller.move_right.value + speed
        if self._controller.move_left.activated:
            return self._controller.move_left.value - speed
        return 0

    def _calculate_y(self, character: Character) -> float:
        if self._controller.move_up.activated and not character.is_jumping:
            self._current_speed = self._start_speed
            character.is_jumping = True
        elif character.is_jumping:
            self._current_speed += self._gravitation
        else:
            self._current_speed = 0

        return self._current_speed
