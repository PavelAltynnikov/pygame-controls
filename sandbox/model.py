class Point:
    def __init__(self, x: float = 0, y: float = 0):
        self.x = x
        self.y = y


class Character:
    def __init__(self, start_point: Point):
        self._location = start_point
        self.is_jumping = False

    @property
    def location(self) -> Point:
        return self._location

    def move_to(self, point: Point) -> None:
        """Кардинально изменить точку расположения объекта"""
        self._location = point

    def change_x(self, dx: float) -> None:
        """Изменить часть текущей координаты"""
        self._location.x += dx

    def change_y(self, dy: float) -> None:
        """Изменить часть текущей координаты"""
        self._location.y += dy
