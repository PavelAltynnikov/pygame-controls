import pygame

import view
from controllers import (
    PygameGamepad, PygameIntermittentGamepad,
    PygameKeyboard, PygameIntermittentKeyboard
)
from game_rules import Mover
from model import Character, Point
from settings import PygameKeyboardSettings, get_ui_settings


SCREEN_SIZE = (1000, 500)

pygame.init()
pygame.key.set_repeat(500)
screen = pygame.display.set_mode(SCREEN_SIZE)

character = Character(Point(300, 300))

controller = PygameGamepad()
# intermittent_controller = controller
intermittent_controller = PygameIntermittentGamepad()

controller_settings = get_ui_settings(PygameKeyboardSettings)
# controller = PygameKeyboard(controller_settings)
# intermittent_controller = PygameIntermittentKeyboard(controller_settings)
# тут может быть проблема в том, что у одного из контроллеров не изменятся настройки
# при изменении через свойства.
# Да, проблема подтвердилась(.

mover = Mover(controller)

settings_window = view.windows.SettingsWindow(
    caption="settings",
    size=SCREEN_SIZE,
    settings=controller_settings,
    controller=intermittent_controller
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
    controller=intermittent_controller
)
start_window.play_button_handlers.append(game_window.show)
start_window.settings_button_handlers.append(settings_window.show)

start_window.show()
