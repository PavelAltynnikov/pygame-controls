import json

import pygame


def get_ui_settings():
    with open('settings.json', 'r') as file:
        return json.loads(
            ''.join(file.readlines()),
            object_hook=lambda d: Settings(**d)
        )


class UserControlSettings:
    def __init__(self):
        self.move_right = pygame.K_RIGHT
        self.move_up = pygame.K_UP
        self.move_left = pygame.K_LEFT
        self.move_down = pygame.K_DOWN


class Settings:
    def __init__(self, right_key, left_key, up_key, down_key):
        self.right_key = right_key
        self.left_key = left_key
        self.up_key = up_key
        self.down_key = down_key
