import json
import types

import pygame

import view


pygame.init()
pygame.key.set_repeat(500)

with open('settings.json', 'r') as file:
    ui_settings = json.loads(
        ''.join(file.readlines()),
        object_hook=lambda d: types.SimpleNamespace(**d)
    )

# window = GameWindow(
#     caption='Controls tests',
#     size=(1000, 500),
#     character=Character(settings.UserControlSettings()),
#     settings=ui_settings
# )
# window.show()
sw = view.SettingWindow("settings", (1000, 500), ui_settings)
sw.show()
