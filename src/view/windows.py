from abc import ABC, abstractmethod

import pygame

from controllers import Controller
from settings import ControllerSettings
from game_rules import Mover
from .sprites import Sprite
from .controls import Button, Control, Key, Label, RowSetting


class Window(ABC):
    def __init__(self, caption: str, size: tuple[int, int], controller: Controller):
        self._background_color: tuple[int, int, int] = (80, 80, 80)
        self._caption = caption
        self._controls: list[Control] = []
        self._controller = controller
        self._is_showing = True
        self._screen = pygame.display.set_mode(size)
        self._size = size
        pygame.display.set_caption(caption)

    @abstractmethod
    def show(self):
        ...

    def quit(self):
        self._is_showing = False

    def _events_handler(self):
        self._quit_if_user_wants_to_close_window()

    def _quit_if_user_wants_to_close_window(self):
        if not self._controller.quit.activated:
            return
        self.quit()


class SettingsWindow(Window):
    def __init__(
            self,
            caption,
            size,
            settings: ControllerSettings,
            controller: Controller):
        super().__init__(caption, size, controller)
        self._background_color = (0, 49, 83)
        self._settings = settings
        self._initialize_components()

    def show(self):
        fps = 30
        clock = pygame.time.Clock()

        while self._is_showing:
            events = pygame.event.get()
            self._controller.conduct_survey_of_controls(events)
            self._events_handler()

            self._draw_all_components()

            self._controller.deactivate_all_controls()
            clock.tick(fps)

        self._is_showing = True

    def _initialize_components(self):
        font = pygame.font.SysFont('Consolas', 25)
        right_setting = RowSetting(
            Label(font, 'right'),
            Key(
                font=font,
                setting=self._settings.right,
                control=self._controller.move_right
            ),
            location=(50, 50)
        )
        right_setting.activate()

        left_setting = RowSetting(
            Label(font, 'left'),
            Key(
                font=font,
                setting=self._settings.left,
                control=self._controller.move_left
            ),
            location=(50, 80)
        )

        up_setting = RowSetting(
            Label(font, 'up'),
            Key(
                font=font,
                setting=self._settings.up,
                control=self._controller.move_up
            ),
            location=(50, 110)
        )

        down_setting = RowSetting(
            Label(font, 'down'),
            Key(
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

    def _events_handler(self):
        super()._events_handler()
        self._change_active_setting()
        self._change_key_value()

    def _draw_all_components(self):
        self._screen.fill(self._background_color)
        for control in self._controls:
            control.draw(self._screen)
        pygame.display.update()

    def _change_active_setting(self):
        if self._controller.move_up.activated:
            self._selected_item_index -= 1
            if self._selected_item_index < 0:
                self._selected_item_index = len(self._controls) - 1
        elif self._controller.move_down.activated:
            self._selected_item_index += 1
            if self._selected_item_index >= len(self._controls):
                self._selected_item_index = 0
        else:
            return

        for i, setting in enumerate(self._controls):
            if not isinstance(setting, RowSetting):
                continue
            if i == self._selected_item_index:
                setting.activate()
            else:
                setting.deactivate()

    def _change_key_value(self):
        if self._controller.accept.activated:
            control = self._controls[self._selected_item_index]
            if not isinstance(control, RowSetting):
                return

            key_control = control.key
            key_control.activate()

            key_number = self._waiting_for_user_assign_new_key(key_control)
            if key_number is None:
                return

            key_control.change_text(pygame.key.name(key_number))
            key_control._control.update_key_number(key_number)

            key_control._setting.value = key_number
            self._settings.save()

            key_control.deactivate()

    def _waiting_for_user_assign_new_key(self, key_control: Key) -> int | None:
        # TODO: Тут дохера логики,
        # и ивенты, и черчение рамки и апдейт экрана.
        # Надо подумать как это сделать лаконичней.
        while True:
            # TODO: Использовать контроллер.
            # Но чтобы это сделать,
            # нужно чтобы контроллер смог отдать любую нажатую клавишу.
            for event in pygame.event.get():
                if event.type != pygame.KEYDOWN:
                    continue
                if event.key == pygame.K_ESCAPE:
                    return
                # TODO: Добавить список возможных клавиш для назначения
                else:
                    return event.key
            key_control.draw_frame(self._screen)
            pygame.display.update()


class GameWindow(Window):
    def __init__(
            self,
            caption: str,
            size: tuple[int, int],
            sprite: Sprite,
            mover: Mover,
            controller: Controller):
        super().__init__(caption, size, controller)
        self._background_color = (30, 89, 89)
        self._sprite = sprite
        self._mover = mover

    def show(self):
        while self._is_showing:
            events = pygame.event.get()
            self._mover._controller.conduct_survey_of_controls(events)
            self._events_handler()

            self._move_all_objects()
            self._update_all_objects()
            self._draw_all_components()

            self._mover._controller.deactivate_all_controls()

        self._is_showing = True

    def _move_all_objects(self):
        # TODO: вот это полная хуйня из-за _sprite._character
        self._mover.move_character(character=self._sprite._character)

    def _update_all_objects(self):
        self._sprite.update()

    def _draw_all_components(self):
        self._screen.fill(self._background_color)
        self._sprite.draw(self._screen)
        pygame.display.update()


class MenuWindow(Window):
    def __init__(self, caption, size, controller: Controller):
        super().__init__(caption, size, controller)
        self._background_color = (156, 156, 156)
        self.play_button_handlers = []
        self.settings_button_handlers = []
        self._initialize_components()

    def show(self):
        fps = 30
        clock = pygame.time.Clock()

        while self._is_showing:
            events = pygame.event.get()
            self._controller.conduct_survey_of_controls(events)
            self._events_handler()

            self._draw_all_components()

            self._controller.deactivate_all_controls()
            clock.tick(fps)

        self._is_showing = True

    def _initialize_components(self):
        font = pygame.font.SysFont('Consolas', 25)

        button_play = Button(
            font=font,
            text="play",
            antialias=False,
            color=(0, 0, 0),
            location=(100, 100),
        )
        button_play.add_click_handler(self._on_play_button_click)
        button_play.activate()

        button_settings = Button(
            font=font,
            text="settings",
            antialias=False,
            color=(0, 0, 0),
            location=(100, 200),
        )
        button_settings.add_click_handler(self._on_settings_button_click)

        button_quit = Button(
            font=font,
            text="quit",
            antialias=False,
            color=(0, 0, 0),
            location=(100, 300),
        )
        button_quit.add_click_handler(self._on_quit_button_click_handler)

        self._selected_item_index = 0
        self._controls.append(button_play)
        self._controls.append(button_settings)
        self._controls.append(button_quit)

    def _events_handler(self):
        super()._events_handler()
        self._change_active_button()
        self._click_on_button()

    def _click_on_button(self):
        if not self._controller.accept.activated:
            return

        control = self._controls[self._selected_item_index]
        if not isinstance(control, Button):
            return

        control.click()

    def _change_active_button(self):
        if self._controller.move_up.activated:
            self._selected_item_index -= 1
            if self._selected_item_index < 0:
                self._selected_item_index = len(self._controls) - 1
        elif self._controller.move_down.activated:
            self._selected_item_index += 1
            if self._selected_item_index >= len(self._controls):
                self._selected_item_index = 0
        else:
            return

        for i, control in enumerate(self._controls):
            if not isinstance(control, Button):
                continue
            if i == self._selected_item_index:
                control.activate()
            else:
                control.deactivate()

    def _draw_all_components(self):
        self._screen.fill(self._background_color)
        for control in self._controls:
            control.draw(self._screen)
        pygame.display.update()

    def _on_play_button_click(self):
        self._controller.deactivate_all_controls()
        for handler in self.play_button_handlers:
            handler()

    def _on_settings_button_click(self):
        self._controller.deactivate_all_controls()
        for handler in self.settings_button_handlers:
            handler()

    def _on_quit_button_click_handler(self):
        self.quit()
