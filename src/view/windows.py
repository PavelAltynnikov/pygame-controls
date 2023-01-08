from abc import ABC, abstractmethod

import pygame

import controller
import settings
from . import sprites
from . import controls
# TODO Нужно отказаться от зависимости одного окна от другого окна.


class Window(ABC):
    def __init__(self, caption: str, size: tuple[int, int]):
        self._caption = caption
        self._size = size
        self._screen = pygame.display.set_mode(size)
        self._is_showing = True
        self._controls: list[controls.Control] = []
        pygame.display.set_caption(caption)

    @staticmethod
    def _quit_button_is_pressed(event):
        return (
            event.type == pygame.QUIT
            or (event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, ))
        )

    def _quit_if_user_wants_to_close_window(self, events):
        for event in events:
            if self._quit_button_is_pressed(event):
                self.quit()

    @abstractmethod
    def show(self):
        pass

    def quit(self):
        self._is_showing = False


class SettingWindow(Window):
    def __init__(
            self,
            caption,
            size,
            settings: settings.ControlSettings,
            controller: controller.Controller):
        super().__init__(caption, size)
        self._settings = settings
        self._controller = controller
        self._initialize_components()

    def _initialize_components(self):
        font = pygame.font.SysFont('Consolas', 25)
        right_setting = controls.RowSetting(
            controls.Label(font, 'right'),
            controls.Key(
                font=font,
                setting=self._settings.right,
                control=self._controller.move_right
            ),
            location=(50, 50)
        )
        right_setting.activate()

        left_setting = controls.RowSetting(
            controls.Label(font, 'left'),
            controls.Key(
                font=font,
                setting=self._settings.left,
                control=self._controller.move_left
            ),
            location=(50, 80)
        )

        up_setting = controls.RowSetting(
            controls.Label(font, 'up'),
            controls.Key(
                font=font,
                setting=self._settings.up,
                control=self._controller.move_up
            ),
            location=(50, 110)
        )

        down_setting = controls.RowSetting(
            controls.Label(font, 'down'),
            controls.Key(
                font=font,
                setting=self._settings.down,
                control=self._controller.move_down
            ),
            location=(50, 140)
        )

        self._controls.append(right_setting)
        self._controls.append(left_setting)
        self._controls.append(up_setting)
        self._controls.append(down_setting)

        self._selected_item_index = 0

    def _draw(self):
        for control in self._controls:
            control.draw(self._screen)

    def _event_handler(self, events):
        for event in events:
            self._change_active_setting(event)
            self._change_key_value(event)

    def _change_active_setting(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self._selected_item_index += 1
                if self._selected_item_index >= len(self._controls):
                    self._selected_item_index = 0
            elif event.key == pygame.K_UP:
                self._selected_item_index -= 1
                if self._selected_item_index < 0:
                    self._selected_item_index = len(self._controls) - 1
            else:
                return
            for i, setting in enumerate(self._controls):
                if not isinstance(setting, controls.RowSetting):
                    continue
                if i == self._selected_item_index:
                    setting.activate()
                else:
                    setting.deactivate()

    def _change_key_value(self, event):
        if event.type != pygame.KEYDOWN:
            return
        if event.key != pygame.K_RETURN:
            return
        control = self._controls[self._selected_item_index]
        if not isinstance(control, controls.RowSetting):
            return

        key_control = control.key
        key_control.activate()

        key_number = self._waiting_for_user_assign_new_key(self._screen, key_control)
        if key_number is None:
            return

        key_control.change_text(pygame.key.name(key_number))
        key_control._control.key_number = key_number

        key_control._setting.value = key_number
        self._settings.save()

        key_control.deactivate()

    def _waiting_for_user_assign_new_key(
            self, screen, key_control: controls.Key) -> int | None:
        # TODO: тут дохера логики,
        # и ивенты, и черчение рамки и апдейт экрана.
        # Надо подумать как это сделать лаконичней.
        while True:
            for event in pygame.event.get():
                if event.type != pygame.KEYDOWN:
                    continue
                if event.key == pygame.K_ESCAPE:
                    return
                # TODO: Добавить список возможных клавиш для назначения
                else:
                    return event.key
            key_control.draw_frame(screen)
            pygame.display.update()

    def show(self):
        blue_color = (0, 49, 83)
        while self._is_showing:
            events = pygame.event.get()
            self._quit_if_user_wants_to_close_window(events)
            self._event_handler(events)

            self._screen.fill(blue_color)
            self._draw()

            pygame.display.update()
        self._is_showing = True


class GameWindow(Window):
    def __init__(
            self,
            caption: str,
            size: tuple[int, int],
            sprite: sprites.Sprite,
            mover: controller.Mover,
            settings_window: SettingWindow):
        super().__init__(caption, size)
        self._sprite = sprite
        self._mover = mover
        self._settings_window = settings_window

    def _open_settings_window_if_needed(self, events):
        for event in events:
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_s:
                self._settings_window.show()

    def _move_all_objects(self):
        # вот это полная хуйня из-за _sprite._character
        self._mover.move_character(character=self._sprite._character)

    def _update_all_objects(self):
        self._sprite.update()

    def _draw_all(self, background_color):
        self._screen.fill(background_color)
        self._sprite.draw(self._screen)

    def show(self):
        green = (30, 89, 89)
        while self._is_showing:
            events = pygame.event.get()

            self._quit_if_user_wants_to_close_window(events)
            self._open_settings_window_if_needed(events)

            self._move_all_objects()
            self._update_all_objects()
            self._draw_all(background_color=green)

            pygame.display.update()
