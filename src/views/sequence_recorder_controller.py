import queue
import threading
from tkinter import filedialog
import os


class SequenceRecorderController:
    def __init__(self, recorder, player, window_manager, transition_actions_manager):
        self.transition_actions_manager = transition_actions_manager
        self.gui = None
        self.recorder = recorder
        self.player = player
        self.window_manager = window_manager

    def set_gui(self, gui):
        if gui is None:
            raise ValueError("GUI cannot be None")
        self.gui = gui

    def record_and_save_input_events(self):
        try:
            filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
            if filename:
                init_state_screenshot_path = self.window_manager.window_screenshot("init_screenshot.png")

                result_queue = queue.Queue()  # Crear una cola para almacenar el resultado
                def worker_function():
                    actions_path = self.recorder.record_and_save_events(filename)
                    result_queue.put(actions_path)  # Poner el resultado en la cola
                thread = threading.Thread(target=worker_function)
                thread.daemon = True
                thread.start()
                thread.join()

                final_state_screenshot_path = self.window_manager.window_screenshot("final_screenshot.png")

                self.transition_actions_manager.add_state_transition(
                    init_state_screenshot_path,
                    result_queue.get(),
                    final_state_screenshot_path
                )
                self.show_info("¡Guardado correctamente!", "La secuencia y los estados se han guardado correctamente.")
        except Exception as e:
            self.show_error("Error al abrir el cuadro de diálogo de guardar", str(e))
            raise e

    def load_and_play_input_events(self):
        try:
            filename = filedialog.askopenfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
            if filename:
                threading.Thread(target=self.player.play_events, args=(filename,)).start()
        except Exception as e:
            self.show_error("Error reproducción sequencia", str(e))

    def show_error(self, title, text):
        if self.gui:
            self.gui.info_message_box(title=title, text=text)
        else:
            print(f"Error: {title} - {text}")

    def show_info(self, title, text):
        if self.gui:
            self.gui.info_message_box(title=title, text=text)
        else:
            print(f"Info: {title} - {text}")

    def run(self):
        if not self.window_manager.open_and_initialize_window():
            self.show_error("Error de ventana", "No se pudo abrir o inicializar la ventana.")
            return
        if self.gui:
            self.gui.run()
        else:
            print("No GUI to run.")
