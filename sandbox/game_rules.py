from .model import Character, Point
from .controllers import Controller


class Mover:
    def __init__(self, controller: Controller):
        self._controller = controller

    def move_character(self, character: Character):
        speed = 0
        character.move_to(
            Point(
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
