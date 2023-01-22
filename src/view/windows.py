from abc import ABC, abstractmethod

import pygame

from controllers import Controller
from settings import ControllerSettings
from game_rules import Mover
from .sprites import Sprite
from .controls import Button, Control, Key, Label, RowSetting


class Window(ABC):
    def __init__(self, caption: str, size: tuple[int, int]):
        self._caption = caption
        self._size = size
        self._screen = pygame.display.set_mode(size)
        self._is_showing = True
        self._controls: list[Control] = []
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


class SettingsWindow(Window):
    def __init__(
            self,
            caption,
            size,
            settings: ControllerSettings,
            controller: Controller):
        super().__init__(caption, size)
        self._settings = settings
        self._controller = controller
        self._initialize_components()

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

    def _draw(self):
        for control in self._controls:
            control.draw(self._screen)

    def _events_handler(self):
        self._quit_if_user_wants_to_close_window()
        self._change_active_setting()
        self._change_key_value()

    def _quit_if_user_wants_to_close_window(self):
        if not self._controller.quit.activated:
            return
        self.quit()

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

            key_number = self._waiting_for_user_assign_new_key(
                self._screen,
                key_control
            )
            if key_number is None:
                return

            key_control.change_text(pygame.key.name(key_number))
            key_control._control.update_key_number(key_number)

            key_control._setting.value = key_number
            self._settings.save()

            key_control.deactivate()

    def _waiting_for_user_assign_new_key(
            self, screen, key_control: Key) -> int | None:
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
            key_control.draw_frame(screen)
            pygame.display.update()

    def show(self):
        blue_color = (0, 49, 83)
        while self._is_showing:
            events = pygame.event.get()
            self._controller.conduct_survey_of_controls(events)
            self._events_handler()

            self._screen.fill(blue_color)
            self._draw()
            pygame.display.update()

            self._controller.deactivate_all_controls()

        self._is_showing = True


class GameWindow(Window):
    def __init__(
            self,
            caption: str,
            size: tuple[int, int],
            sprite: Sprite,
            mover: Mover):
        super().__init__(caption, size)
        self._sprite = sprite
        self._mover = mover

    def _quit(self):
        self._is_showing = False

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
            self._mover._controller.conduct_survey_of_controls(events)

            self._move_all_objects()
            self._update_all_objects()
            self._draw_all(background_color=green)

            self._mover._controller.deactivate_all_controls()
            pygame.display.update()

        self._is_showing = True


class MenuWindow(Window):
    def __init__(self, caption, size, controller: Controller):
        super().__init__(caption, size)
        self._controller = controller
        self.play_button_handlers = []
        self.settings_button_handlers = []
        self._initialize_components()

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
        self._quit_if_user_wants_to_close_window()
        self._change_active_button()
        self._click_on_button()

    def _quit_if_user_wants_to_close_window(self):
        if not self._controller.quit.activated:
            return
        self.quit()

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

    def _draw(self):
        for control in self._controls:
            control.draw(self._screen)

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

    def show(self):
        gray_color = (156, 156, 156)
        fps = 30
        clock = pygame.time.Clock()

        while self._is_showing:
            events = pygame.event.get()
            self._controller.conduct_survey_of_controls(events)
            self._events_handler()

            self._screen.fill(gray_color)
            self._draw()

            pygame.display.update()

            self._controller.deactivate_all_controls()
            clock.tick(fps)

        self._is_showing = True
