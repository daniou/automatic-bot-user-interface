import pygetwindow as gw
import pyautogui
import subprocess
import time
import config
import os

pyautogui.FAILSAFE = True

class WindowManager:
    def __init__(self, executable_path):
        self.executable_path = executable_path
        self.window_title = None
        self.window = None
        self.default_x = 0
        self.default_y = 0
        self.default_width = 2000
        self.default_height = 900

    def restart_window(self):
        self.close_application()
        self.open_and_initialize_window()

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
            print("aqui esta el problema",self.window)
            self.window.activate()
            self.window.moveTo(new_x, new_y)

            # Cambiar el tamaño de la ventana a las nuevas dimensiones
            #self.window.resizeTo(new_width, new_height)

    def window_screenshot(self, screenshot_path):
        while not self.window:
            self.open_and_initialize_window()
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
        return screenshot_path

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
        time.sleep(1)
        print("Se ha abierto la interfaz python")
        self.window_title = gw.getActiveWindow().title
        self.window = self.find_window()
        return self.initialize_window()
    
    def close_application(self):
        if self.window is not None:
            self.window.close()
        else:
            print("No se ha encontrado ninguna ")

    def open_application(self, executable_path, window_title=config.EXECUTABLE_WINDOW_TITLE, window_class=None):
        try:
            # Intenta abrir la aplicación
            #subprocess.Popen(["start", executable_path], shell=True)
            #TODO: MOVER ESTO A UN CSV
            pyautogui.hotkey('winleft', 'd')
            time.sleep(1)
            pyautogui.doubleClick(1873, 42)
            time.sleep(3)
            pyautogui.write("SUPERVISOR")
            pyautogui.press('tab')
            pyautogui.write("4169")
            pyautogui.press('tab')
            pyautogui.press('enter')
            time.sleep(1)
            pyautogui.press('enter')
            #os.system(f"start {executable_path}")

            # Espera hasta que la ventana de la aplicación esté disponible durante un tiempo limitado
            timeout = 30  # Puedes ajustar este valor según tus necesidades
            start_time = time.time()

            while time.time() - start_time < timeout:
                windows = gw.getAllWindows()
                wtitles = gw.getAllTitles()
                print(wtitles)
                target_window = None
                for window in windows:
                    if (window_title and window.title.startswith(window_title)) or \
                            (window_class and window._program.startswith(window_class)):
                        target_window = window
                        break

                if target_window:
                    break

            if target_window:
                # Activar la ventana de la aplicación
                target_window.activate()
            else:
                print("No se pudo encontrar la ventana de la aplicación después de esperar.")

        except FileNotFoundError:
            print(f"Application not found at the specified path: {executable_path}")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
