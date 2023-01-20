import enum
import pygame


class GamePadAxe(enum.Enum):
    LEFT_STICK_X = 0
    LEFT_STICK_Y = 1
    RIGHT_STICK_X = 2
    RIGHT_STICK_Y = 3
    LEFT_TRIGGER = 4
    RIGHT_TRIGGER = 5


class GamePadButton(enum.Enum):
    A = 0
    B = 1
    X = 2
    Y = 3
    LB = 4
    RB = 5
    # элемента с номером 6 на моём геймпаде не оказалось
    START = 7


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


def _main():
    SCREEN_SIZE = (1000, 500)

    pygame.init()
    pygame.joystick.init()

    pygame.key.set_repeat(500)
    screen = pygame.display.set_mode(SCREEN_SIZE)
    blue = (0, 49, 83)

    game_pad = [
        pygame.joystick.Joystick(x)
        for x
        in range(pygame.joystick.get_count())
    ][0]

    _start_loop(screen, blue, game_pad)


def _start_loop(screen, color, game_pad: pygame.joystick.Joystick):
    close_window = False
    clock = pygame.time.Clock()
    fps = 30

    font = pygame.font.SysFont('Consolas', 25)
    black_color = (0, 0, 0)
    text = Text(screen, font, black_color)

    while not close_window:
        events = pygame.event.get()
        close_window = _is_user_wants_to_close_window(events)

        screen.fill(color)
        _render_labels(game_pad, text)

        pygame.display.update()

        clock.tick(fps)


def _render_labels(game_pad: pygame.joystick.Joystick, text):
    text.render(
        f"LSx={round(game_pad.get_axis(GamePadAxe.LEFT_STICK_X.value), 2)}",
        (10, 10)
    )
    text.render(
        f"LSy={round(game_pad.get_axis(GamePadAxe.LEFT_STICK_Y.value), 2)}",
        (10, 35)
    )
    text.render(
        f"RSx={round(game_pad.get_axis(GamePadAxe.RIGHT_STICK_X.value), 2)}",
        (10, 60)
    )
    text.render(
        f"RSy={round(game_pad.get_axis(GamePadAxe.RIGHT_STICK_Y.value), 2)}",
        (10, 85)
    )
    text.render(
        f"LT={round(game_pad.get_axis(GamePadAxe.LEFT_TRIGGER.value), 2)}",
        (10, 110)
    )
    text.render(
        f"RT={round(game_pad.get_axis(GamePadAxe.RIGHT_TRIGGER.value), 2)}",
        (10, 135)
    )
    text.render(f"A={game_pad.get_button(GamePadButton.A.value)}", (10, 160))
    text.render(f"B={game_pad.get_button(GamePadButton.B.value)}", (10, 185))
    text.render(f"X={game_pad.get_button(GamePadButton.X.value)}", (10, 210))
    text.render(f"Y={game_pad.get_button(GamePadButton.Y.value)}", (10, 235))
    text.render(f"LB={game_pad.get_button(GamePadButton.LB.value)}", (10, 260))
    text.render(f"RB={game_pad.get_button(GamePadButton.RB.value)}", (10, 285))
    text.render(f"start={game_pad.get_button(GamePadButton.START.value)}", (10, 310))
    text.render(f"??={game_pad.get_button(8)}", (10, 335))
    text.render(f"??={game_pad.get_button(9)}", (10, 360))
    text.render(f"??={game_pad.get_button(10)}", (10, 385))


def _quit_button_is_pressed(event):
    return (
        event.type == pygame.QUIT
        or (event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, ))
    )


def _is_user_wants_to_close_window(events):
    for event in events:
        if _quit_button_is_pressed(event):
            return True
    return False


if __name__ == '__main__':
    _main()
