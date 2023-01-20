import pygame

import view
from controllers import PygameGamepadController, PygameKeyboardController
from game_rules import Mover
from model import Character, Point
from settings import PygameKeyboardControlSettings, get_ui_settings


SCREEN_SIZE = (1000, 500)

pygame.init()
pygame.key.set_repeat(500)
screen = pygame.display.set_mode(SCREEN_SIZE)

character = Character(Point(300, 300))

controller_settings = get_ui_settings(PygameKeyboardControlSettings)
controller_ = PygameGamepadController()
controller_ = PygameKeyboardController(controller_settings)
mover = Mover(controller_)

settings_window = view.windows.SettingWindow(
    caption="settings",
    size=SCREEN_SIZE,
    settings=controller_settings,
    controller=controller_
)

game_window = view.windows.GameWindow(
    caption='Controls tests',
    size=SCREEN_SIZE,
    sprite=view.sprites.Sprite(character),
    mover=mover,
)

start_window = view.windows.MenuWindow(
    caption='Controls tests | Menu',
    size=SCREEN_SIZE
)
start_window.play_button_handlers.append(game_window.show)
start_window.settings_button_handlers.append(settings_window.show)

start_window.show()
