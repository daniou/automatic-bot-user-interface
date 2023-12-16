import tkinter as tk
from tkinter import messagebox


class GUI:
    def __init__(self, controller):
        self.controller = controller

        self.root = tk.Tk()
        self.root.title("Grabador y Reproductor de Secuencias de Teclado")

        save_button = tk.Button(self.root, text="Grabar y Guardar", command=self.controller.record_and_save_input_events)
        save_button.pack(pady=20, padx=100)

        load_button = tk.Button(self.root, text="Reproducir", command=self.controller.load_and_play_input_events)
        load_button.pack(pady=20, padx=100)

    def info_message_box(self, title, text):
        messagebox.showinfo(title, text)

    def error_message_box(self, title, text):
        messagebox.showerror(title, text)

    def run(self):
        self.root.mainloop()
