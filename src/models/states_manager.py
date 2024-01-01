import csv
import os
import pickle
import shutil

from src.domain.ui_analyzer import ui_analyzer, UIAnalyzer
from src.models.ui_element import UIElement  # Asegúrate de importar correctamente tu clase UIElement


class State:
    def __init__(self, name, screenshot_path, pkl_path, ui, id_text_in_ui=None):
        print("@@@@@@polisia")
        print(name, screenshot_path, pkl_path, ui, id_text_in_ui)
        self.name = name
        self.screenshot_path = self.move_and_rename_screenshot(screenshot_path, name)
        self.pkl_path = pkl_path
        self.ui = ui
        self.ui_path = self.save_ui()
        self.id_text_in_ui = id_text_in_ui

    def move_and_rename_screenshot(self, screenshot_path, name):
        new_path = f"./src/persistence/state_screenshots/{name}.png"
        os.makedirs(os.path.dirname(new_path), exist_ok=True)
        shutil.move(screenshot_path, new_path)
        return new_path

    def __eq__(self, other):
        # Si other es una cadena de texto, intenta cargar el estado desde un archivo .pkl

        if isinstance(other, str):
            other = State.load_from_pkl(other)

        # Si other no es una instancia de State después de intentar cargar desde .pkl, retorna False
        if not isinstance(other, State):
            return False

        # Realiza la comparación entre los estados
        # TODO: Puedes ajustar la lógica de comparación según tus necesidades
        return self.id_text_in_ui == other.id_text_in_ui or self.pkl_path == other.pkl_path

    def __hash__(self):
        return hash(self.id_text_in_ui)

    def get_ui(self):
        ui_path = f"./src/persistence/uis/{self.name}.pkl"
        if os.path.exists(ui_path):
            with open(ui_path, 'rb') as file:
                ui = pickle.load(file)
            return ui
        else:
            print(f"No se encuentra la UI del estado {self.name} en la ruta: {self.ui_path}")
            return None

    def save_ui(self):
        ui_path = f"./src/persistence/uis/{self.name}.pkl"
        os.makedirs(os.path.dirname(ui_path), exist_ok=True)
        with open(ui_path, 'wb') as file:
            pickle.dump(self.ui, file)
        return ui_path

    def save_to_pkl(self):
        os.makedirs(os.path.dirname(self.pkl_path), exist_ok=True)
        with open(self.pkl_path, 'wb') as pklfile:
            pickle.dump(self, pklfile)
            return self.pkl_path

    @staticmethod
    def load_from_pkl(pkl_path):
        print("·····", pkl_path)
        with open(pkl_path, 'rb') as pklfile:
            state = pickle.load(pklfile)
            print(state)
        return state

    def __repr__(self):
        return f"<State name={self.name}, screenshot={self.screenshot_path}, pkl_path={self.pkl_path}, ui_path={self.ui_path}, id_text_in_ui={self.id_text_in_ui}>"


class StatesManager:
    def __init__(self, filepath='states.csv'):
        self.filepath = filepath
        self.states = []
        self.load_from_csv()

    def find_if_state_already_exists(self, screenshot_path):
        print("aqui el eotro:", screenshot_path)
        ui1 = ui_analyzer.get_ui(screenshot_path)
        for state in self.states:
            if (state.id_text_in_ui != "" and (state.id_text_in_ui[0] == "-" and not UIAnalyzer.ui_contains_text(ui1, state.id_text_in_ui[1:]) or UIAnalyzer.ui_contains_text(ui1, state.id_text_in_ui)) or UIAnalyzer.are_uis_equal(ui1, state.ui)):
                return state
        return None

    def add(self, new_state):
        self.states.append(new_state)

    def add_from_path(self, new_state_path):
        new_state = State.load_from_pkl(new_state_path)
        self.states.append(new_state)
        return new_state.pkl_path

    def add_state_from_screenshot(self, screenshot_path):
        print("eyooooouuuuu")
        already_existing_state = self.find_if_state_already_exists(screenshot_path)
        print("el esatdo dequ :", already_existing_state)
        if already_existing_state is not None:
            print("yalahvitoh")
            return already_existing_state.pkl_path
        state_name = f"state{len(self.states)}"
        pkl_path = f"./src/persistence/state_pkls/{state_name}.pkl"
        ui1 = ui_analyzer.get_ui(screenshot_path)
        new_state = State(state_name, screenshot_path, pkl_path, ui1)

        new_state.id_text_in_ui = ""
        new_state.save_to_pkl()
        self.states.append(new_state)
        self.save_to_csv()
        return new_state.pkl_path

    def save_to_csv(self):
        with open(self.filepath, 'w', newline='') as csvfile:
            fieldnames = ['state_name', 'screenshot_path', 'pkl_path', 'ui_path', 'id_text_in_ui']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for state in self.states:
                writer.writerow({
                    'state_name': state.name,
                    'screenshot_path': state.screenshot_path,
                    'pkl_path': state.pkl_path,
                    'ui_path': state.ui_path,
                    'id_text_in_ui': state.id_text_in_ui
                })

    def load_from_csv(self):
        if not os.path.exists(self.filepath):
            return
        with open(self.filepath, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                ui = UIElement.load_from_pkl(row['ui_path'])
                state = State(row['state_name'], row['screenshot_path'], row['pkl_path'], ui, row.get('id_text_in_ui'))
                self.states.append(state)

    def find_state_with_id_text(self, id_text_in_ui):
        state = [state for state in self.states if state.id_text_in_ui == id_text_in_ui][0]
        print("MECAGONLARAZA", state)
        return state
