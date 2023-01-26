import pygame

import setup  # noqa
from src.controllers import GamePadAxe, GamePadButton  # type: ignore


class Text:
    def __init__(self, screen, font, color: tuple[int, int, int]):
        self._screen = screen
        self._font = font
        self._color = color

    def render(self, value: str, location: tuple[int, int]):
        self._screen.blit(
            self._font.render(value, False, self._color),
            location
        )


class Test:
    def __init__(self, screen, gamepad):
        self._screen = screen
        self._gamepad = gamepad

    def start(self):
        blue = (0, 49, 83)

        close_window = False
        clock = pygame.time.Clock()
        fps = 30

        font = pygame.font.SysFont('Consolas', 25)
        black_color = (0, 0, 0)
        text = Text(screen, font, black_color)

        while not close_window:
            events = pygame.event.get()
            close_window = self._is_user_wants_to_close_window(events)

            screen.fill(blue)
            self._render_labels(text)

            pygame.display.update()

            clock.tick(fps)

    def _render_labels(self, text):
        text.render(
            f"LSx={round(self._gamepad.get_axis(GamePadAxe.LEFT_STICK_X.value), 2)}",
            (10, 10)
        )
        text.render(
            f"LSy={round(self._gamepad.get_axis(GamePadAxe.LEFT_STICK_Y.value), 2)}",
            (10, 35)
        )
        text.render(
            f"RSx={round(self._gamepad.get_axis(GamePadAxe.RIGHT_STICK_X.value), 2)}",
            (10, 60)
        )
        text.render(
            f"RSy={round(self._gamepad.get_axis(GamePadAxe.RIGHT_STICK_Y.value), 2)}",
            (10, 85)
        )
        text.render(
            f"LT={round(self._gamepad.get_axis(GamePadAxe.LEFT_TRIGGER.value), 2)}",
            (10, 110)
        )
        text.render(
            f"RT={round(self._gamepad.get_axis(GamePadAxe.RIGHT_TRIGGER.value), 2)}",
            (10, 135)
        )
        text.render(
            f"A={self._gamepad.get_button(GamePadButton.A.value)}",
            (10, 160)
        )
        text.render(
            f"B={self._gamepad.get_button(GamePadButton.B.value)}",
            (10, 185)
        )
        text.render(
            f"X={self._gamepad.get_button(GamePadButton.X.value)}",
            (10, 210)
        )
        text.render(
            f"Y={self._gamepad.get_button(GamePadButton.Y.value)}",
            (10, 235)
        )
        text.render(
            f"LB={self._gamepad.get_button(GamePadButton.LB.value)}",
            (10, 260)
        )
        text.render(
            f"RB={self._gamepad.get_button(GamePadButton.RB.value)}",
            (10, 285)
        )
        text.render(
            f"start={self._gamepad.get_button(GamePadButton.START.value)}",
            (10, 310)
        )
        text.render(
            f"LS_push={self._gamepad.get_button(GamePadButton.LS.value)}",
            (10, 335)
        )
        text.render(
            f"RS_push={self._gamepad.get_button(GamePadButton.RS.value)}",
            (10, 360)
        )
        text.render(
            f"??={self._gamepad.get_button(10)}",
            (10, 385)
        )

    def _quit_button_is_pressed(self, event):
        return (
            event.type == pygame.QUIT
            or (event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, ))
        )

    def _is_user_wants_to_close_window(self, events):
        for event in events:
            if self._quit_button_is_pressed(event):
                return True
        return False


if __name__ == '__main__':
    SCREEN_SIZE = (1000, 500)

    pygame.init()
    pygame.joystick.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)

    gamepad = [
        pygame.joystick.Joystick(x)
        for x
        in range(pygame.joystick.get_count())
    ][0]

    t = Test(screen, gamepad)
    t.start()
