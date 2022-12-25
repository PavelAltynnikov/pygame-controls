from abc import ABC, abstractmethod
from settings import Settings
import pygame


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


class GameWindow(Window):
    def __init__(self, caption, size, character, settings):
        super().__init__(caption, size)
        self._character = character
        self._settings = settings

    def _open_settings_window_if_needed(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                settings = SettingWindow(
                    f'{self._caption} | Settings',
                    self._size,
                    self._settings
                )
                settings.show()

    def show(self):
        green_color = (30, 89, 89)
        while self._is_showing:
            events = pygame.event.get()
            self._quit_if_user_wants_to_close_window(events)
            self._open_settings_window_if_needed(events)

            self._character.move()

            self._screen.fill(green_color)
            self._character.draw(self._screen)

            pygame.display.update()


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
        self._surface: pygame.Surface = font.render(text, antialias, color)
        self.location = location

    def draw(self, screen):
        screen.blit(self._surface, self.location)


class Key(Label):
    def __init__(self, font, text, antialias=False, color=(0, 0, 0), location=(0, 0)):
        super().__init__(font, text, antialias, color, location)

    def change_text(self, value):
        self._surface: pygame.Surface = self._font.render(value, self._antialias, self._color)

    def wait_for_user_input(self, screen):
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
                    self.change_text(pygame.key.name(event.key))
                    return
            self._draw_frame(screen)
            pygame.display.update()

    def activate(self):
        self.is_active = True

    def deactivate(self):
        self.is_active = False

    def _draw_frame(self, screen):
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
    def __init__(self, caption, size, settings: Settings):
        super().__init__(caption, size)
        self._controls: list[RowSetting] = []
        self._settings = settings
        self._initialize_components()

    def _initialize_components(self):
        font = pygame.font.SysFont('Consolas', 25)

        right_setting = RowSetting(
            Label(font, 'right'),
            Key(font, self._settings.right_key),
            location=(50, 50)
        )
        right_setting.activate()

        left_setting = RowSetting(
            Label(font, 'left'),
            Key(font, self._settings.left_key),
            location=(50, 80)
        )

        up_setting = RowSetting(
            Label(font, 'up'),
            Key(font, self._settings.up_key),
            location=(50, 110)
        )

        down_setting = RowSetting(
            Label(font, 'down'),
            Key(font, self._settings.down_key),
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
        key_control.wait_for_user_input(self._screen)
        key_control.deactivate()

    def show(self):
        blue_color = (0, 49, 83)
        while self._is_showing:
            events = pygame.event.get()
            self._quit_if_user_wants_to_close_window(events)
            self._event_handler(events)

            self._screen.fill(blue_color)
            self._draw()

            pygame.display.update()
