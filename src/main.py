import pygame

import controller
import model
import settings
import view


SCREEN_SIZE = (1000, 500)

pygame.init()
pygame.key.set_repeat(500)
screen = pygame.display.set_mode(SCREEN_SIZE)

character = model.Character(model.Point(300, 300))

control_settings = settings.get_ui_settings(settings.PygameKeyboardControlSettings)
keyboard = controller.PygameKeyboardController(control_settings)
mover = controller.Mover(keyboard)

settings_window = view.windows.SettingWindow(
    caption="settings",
    size=SCREEN_SIZE,
    settings=control_settings,
    controller=keyboard
)

game_window = view.windows.GameWindow(
    caption='Controls tests',
    size=SCREEN_SIZE,
    sprite=view.sprites.Sprite(character),
    mover=mover,
)

start_window = view.windows.MenuWindow(
    caption='Controls tests | Menu',
    size=SCREEN_SIZE,
    game_window=game_window,
    settings_window=settings_window
)

start_window.show()
