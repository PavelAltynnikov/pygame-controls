import pygame

import settings
import view


pygame.init()
pygame.key.set_repeat(500)

ui_settings = settings.get_ui_settings()
# window = view.GameWindow(
#     caption='Controls tests',
#     size=(1000, 500),
#     character=view.Character(settings.UserControlSettings()),
#     settings=ui_settings
# )
# window.show()
sw = view.SettingWindow("settings", (1000, 500), ui_settings)
sw.show()
