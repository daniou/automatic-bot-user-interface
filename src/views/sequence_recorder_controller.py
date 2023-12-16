import threading
from tkinter import filedialog
import json
import os

class SequenceRecorderController:
    def __init__(self, recorder, player, window_manager, ui_analyzer):
        self.gui = None
        self.recorder = recorder
        self.player = player
        self.window_manager = window_manager
        self.ui_analyzer = ui_analyzer

    def set_gui(self, gui):
        self.gui = gui

    def capture_initial_state(self):
        # Capturar y guardar el estado inicial
        self.window_manager.capture_initial_screenshot("initial_screenshot.png")
        initial_state = self.ui_analyzer.get_screenshot_state("initial_screenshot.png")
        return initial_state

    def capture_final_state_and_save(self, filename):
        # Capturar y guardar el estado final
        final_screenshot_path = "final_screenshot.png"
        self.window_manager.window_screenshot(final_screenshot_path)
        final_state = self.ui_analyzer.get_screenshot_state(final_screenshot_path)

        # Guardar la relación entre estados y comandos
        data = {
            "initial_state": self.capture_initial_state(),
            "commands": filename,
            "final_state": final_state
        }
        with open(f"{os.path.splitext(filename)[0]}_data.json", 'w') as f:
            json.dump(data, f)

        self.show_info("¡Guardado correctamente!", "La secuencia y los estados se han guardado correctamente.")

    def save_file(self):
        try:
            filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
            if filename:
                # Iniciar la grabación y capturar el estado inicial
                initial_state = self.capture_initial_state()

                # Crear el hilo y almacenar una referencia
                thread = threading.Thread(target=self.recorder.record_events, args=(filename,))
                # Configurar el hilo para que, al finalizar, llame a show_info
                thread.daemon = True
                thread.start()
                thread.join()  # Esperar a que el hilo termine

                # Capturar el estado final y guardar la relación
                self.capture_final_state_and_save(filename)

        except Exception as e:
            self.show_error("Error al abrir el cuadro de diálogo de guardar", str(e))


    def load_file(self):
        try:
            filename = filedialog.askopenfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
            if filename:
                threading.Thread(target=self.player.play_events, args=(filename,)).start()
        except Exception as e:
            self.show_error("Error reproducción sequencia", "Ha habido un error al intentar reproducir una sequencia",
                            str(e))

    def show_error(self, title, text):
        self.gui.info_message_box(title=title, text=text)

    def show_info(self, title, text):
        self.gui.info_message_box(title=title, text=text)

    def run(self):
        self.window_manager.open_and_initialize_window()
        self.gui.run()
