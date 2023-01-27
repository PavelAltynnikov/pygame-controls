from abc import ABC
import os
import json


SETTINGS_FILE_PATH = os.path.join(os.path.dirname(__file__), 'settings.json')


class Setting:
    def __init__(self, value: int):
        self.value = value

    def __str__(self):
        return str(self.value)


class ControllerSettings(ABC):
    def __init__(self, right: Setting, left: Setting, up: Setting, down: Setting):
        self.right = right
        self.left = left
        self.up = up
        self.down = down

    def save(self):
        with open(SETTINGS_FILE_PATH, 'w') as file:
            file.write(json.dumps(self.__dict__, default=lambda o: o.__dict__))


class PygameKeyboardSettings(ControllerSettings):
    def __init__(self, right, left, up, down):
        super().__init__(right, left, up, down)


def get_ui_settings(settings_type: type[ControllerSettings]) -> ControllerSettings:
    with open(SETTINGS_FILE_PATH, 'r') as file:
        data = json.loads(''.join(file.readlines()))
        return settings_type(**{k: Setting(v["value"]) for k, v in data.items()})
