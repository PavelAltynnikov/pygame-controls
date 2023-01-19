import pygame

import controller
import game_rules
import model
import settings
import view


SCREEN_SIZE = (1000, 500)

pygame.init()
pygame.key.set_repeat(500)
screen = pygame.display.set_mode(SCREEN_SIZE)

character = model.Character(model.Point(300, 300))

controller_settings = settings.get_ui_settings(settings.PygameKeyboardControlSettings)
# controller_ = controller.PygameKeyboardController(controller_settings)
controller_ = controller.PygameGamepadController()
mover = game_rules.Mover(controller_)

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
