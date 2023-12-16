import pyautogui
import time


def capture_state(self, screenshot_path):
    self.window_manager.window_screenshot(screenshot_path)
    return self.ui_analyzer.get_screenshot_state(screenshot_path)

class WindowStateDetector:
    def __init__(self, window_title):
        self.window_title = window_title

    def get_state(self):
        pass

    def capture_state(self, screenshot):
        pass




# Ejemplo de uso
if __name__ == "__main__":
    detector = WindowStateDetector(
        "Título de la Ventana")  # Reemplaza "Título de la Ventana" por el título de la ventana que deseas detectar

    while True:
        if detector.is_window_open():
            print("La ventana está abierta.")
        else:
            print("La ventana está cerrada.")
        time.sleep(1)  # Puedes ajustar el intervalo de verificación según tus necesidades
