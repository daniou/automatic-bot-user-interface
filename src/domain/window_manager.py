import pygetwindow as gw
import pyautogui
import subprocess
import time
import config

pyautogui.FAILSAFE = True

class WindowManager:
    def __init__(self, executable_path):
        self.executable_path = executable_path
        self.window_title = None
        self.window = None
        self.default_x = 0
        self.default_y = 0
        self.default_width = 800
        self.default_height = 600

    def is_in_default_coords_and_shape(self):
        if not self.window:
            return False

        current_x, current_y, current_width, current_height = (
            self.window.left,
            self.window.top,
            self.window.width,
            self.window.height,
        )

        return (
            current_x == self.default_x and
            current_y == self.default_y and
            current_width == self.default_width and
            current_height == self.default_height
        )

    def find_window(self):
        try:
            return gw.getWindowsWithTitle(self.window_title)[0]
        except IndexError:
            print(f"No se encontró la ventana con el título '{self.window_title}'")
            return None

    def activate_and_restore_window(self):
        if self.window:
            # Asegurarse de que la ventana no esté minimizada
            if self.window.isMinimized:
                self.window.restore()

            # Asegurarse de que la ventana esté en primer plano y activa
            self.window.activate()
            self.window.restore()
            return True
        else:
            print(f"No se encontró la ventana con el título '{self.window_title}'.")
            return False

    def move_and_scale_window(self, new_x, new_y, new_width, new_height):
        if self.window:
            # Mover la ventana a la nueva posición
            self.window.moveTo(new_x, new_y)

            # Cambiar el tamaño de la ventana a las nuevas dimensiones
            self.window.resizeTo(new_width, new_height)

    def window_screenshot(self, screenshot_path):
        if self.window:
            current_x, current_y, current_width, current_height = (
                self.window.left,
                self.window.top,
                self.window.width,
                self.window.height,
            )

            # Capturar un screenshot de la ventana
            screenshot = pyautogui.screenshot(
                region=(
                    current_x + 8,
                    current_y,
                    current_width - 16,
                    current_height - 8,
                )
            )
            screenshot.save(screenshot_path)
            print(f"Screenshot guardado en: {screenshot_path}")

    # Nueva función para capturar el screenshot inicial
    def capture_initial_screenshot(self, save_path="initial_screenshot.png"):
        if self.window:
            self.window_screenshot(save_path)
            print(f"Screenshot inicial guardado en: {save_path}")

    def initialize_window(self):
        if not self.activate_and_restore_window():
            return False

        new_x = self.default_x
        new_y = self.default_y
        new_width = self.default_width
        new_height = self.default_height

        self.move_and_scale_window(new_x, new_y, new_width, new_height)
        return True

    def open_and_initialize_window(self):
        self.open_application(self.executable_path)
        # Esperar un tiempo para que la ventana se abra completamente
        time.sleep(2)
        print("se ha abierto")
        self.window_title = gw.getActiveWindow().title
        self.window = self.find_window()
        return self.initialize_window()

    def open_application(self, executable_path, window_title=config.EXECUTABLE_WINDOW_TITLE, window_class=None):
        try:
            subprocess.Popen([executable_path])

            # Esperar hasta que la ventana de la aplicación esté disponible
            while True:
                windows = gw.getAllWindows()
                target_window = None
                for window in windows:
                    if (window_title and window.title.startswith(window_title)) or \
                            (window_class and window._program.startswith(window_class)):
                        target_window = window
                        break

                if target_window:
                    break

                time.sleep(1)

            # Activar la ventana de la aplicación
            target_window.activate()

        except FileNotFoundError:
            print(f"Application not found at the specified path: {executable_path}")
