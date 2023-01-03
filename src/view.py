from abc import ABC, abstractmethod

import pygame

import controller
import model
import settings


class Sprite:
    def __init__(self, model: model.Character):
        self.surface = pygame.Surface((100, 100))
        self.surface.fill((250, 50, 50))
        self.rect = self.surface.get_rect()
        self.rect.center = (300, 300)
        self._character = model

    def update(self):
        self.rect.x = self._character.location.x
        self.rect.y = self._character.location.y

    def draw(self, screen):
        screen.blit(self.surface, self.rect)


class Window(ABC):
    def __init__(self, caption, size):
        self._caption = caption
        self._size = size
        self._screen = pygame.display.set_mode(size)
        self._is_showing = True
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


class Control(ABC):
    def __init__(self, location=(0, 0)):
        self.location = location
        self.is_active = False

    @abstractmethod
    def draw(self, screen):
        pass


class Label(Control):
    def __init__(self, font, text, antialias=False, color=(0, 0, 0), location=(0, 0)):
        super().__init__(location)
        self._font = font
        self._antialias = antialias
        self._color = color
        self._surface = None
        self.location = location
        self.update_surface_from_text(text)

    def update_surface_from_text(self, text) -> None:
        self._surface = self._font.render(text, self._antialias, self._color)

    def draw(self, screen):
        screen.blit(self._surface, self.location)


class Key(Label):
    def __init__(
            self,
            font,
            setting: settings.Setting,
            control: controller.Control,
            antialias=False,
            color=(0, 0, 0),
            location=(0, 0)):
        key_value = pygame.key.name(setting.value)
        super().__init__(
            font,
            key_value,
            antialias,
            color,
            location
        )
        self._setting = setting
        self._control = control

    def change_text(self, value):
        self._surface: pygame.Surface = self._font.render(
            value, self._antialias, self._color
        )

    def activate(self):
        self.is_active = True

    def deactivate(self):
        self.is_active = False

    def draw_frame(self, screen):
        rect = self._surface.get_rect()
        rect.topleft = self.location

        pygame.draw.rect(
            surface=screen,
            color=(0, 0, 0),
            rect=rect,
            width=2
        )


class ActiveFlag(Control):
    def __init__(self, location=(0, 0), size=(1, 1), color=(0, 0, 0)):
        super().__init__(location)
        self._surface = pygame.Surface(size)
        self._surface.fill(color)
        self._rect = self._surface.get_rect()
        self._rect.center = location

    def draw(self, screen):
        if self.is_active:
            screen.blit(self._surface, self._rect)


class RowSetting(Control):
    def __init__(self, label: Label, key: Key, location=(0, 0)):
        super().__init__(location)
        flag = ActiveFlag(location=(location[0], location[1] + 10), size=(10, 10))

        label.location = (location[0] + 10, location[1])
        key.location = (location[0] + 150, location[1])

        self.label = label
        self.key = key
        self._controls: list[Control] = [label, key, flag]

    def activate(self):
        self._activation_toggle(True)

    def deactivate(self):
        self._activation_toggle(False)

    def draw(self, screen):
        for component in self._controls:
            component.draw(screen)

    def _activation_toggle(self, is_active):
        self._is_active = is_active
        for component in self._controls:
            if isinstance(component, ActiveFlag):
                component.is_active = is_active


class SettingWindow(Window):
    def __init__(
            self,
            caption,
            size,
            settings: settings.ControlSettings,
            controller: controller.Controller):
        super().__init__(caption, size)
        self._controls: list[RowSetting] = []
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
                if i == self._selected_item_index:
                    setting.activate()
                else:
                    setting.deactivate()

    def _change_key_value(self, event):
        if event.type != pygame.KEYDOWN:
            return
        if event.key != pygame.K_RETURN:
            return

        key_control = self._controls[self._selected_item_index].key
        key_control.activate()

        key_number = self._waiting_for_user_assign_new_key(self._screen, key_control)
        if key_number is None:
            return

        key_control.change_text(pygame.key.name(key_number))
        key_control._control.key_number = key_number

        key_control._setting.value = key_number
        self._settings.save()

        key_control.deactivate()

    def _waiting_for_user_assign_new_key(self, screen, key_control: Key) -> int | None:
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
            sprite: Sprite,
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
        # вот это полная хуйня
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
