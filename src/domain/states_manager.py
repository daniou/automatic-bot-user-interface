import os
import pickle
import shutil


class State:
    def __init__(self, name, screenshot_path, pkl_path):
        self.name = name
        self.screenshot_path = self.move_and_rename_screenshot(screenshot_path, name)
        self.pkl_path = pkl_path

    def move_and_rename_screenshot(self, screenshot_path, name):
        new_path = f"state_screenshots/{name}.png"
        os.makedirs(os.path.dirname(new_path), exist_ok=True)
        shutil.move(screenshot_path, new_path)
        return new_path

    def save_to_pkl(self):
        os.makedirs(os.path.dirname(self.pkl_path), exist_ok=True)
        with open(self.pkl_path, 'wb') as pklfile:
            pickle.dump(self, pklfile)

    def __repr__(self):
        return f"<State name={self.name}, screenshot={self.screenshot_path}, pkl_path={self.pkl_path}>"


class StatesManager:
    def __init__(self, filepath='states.pkl'):
        self.filepath = filepath
        self.states = []
        self.load_from_pkl()

    def add_state(self, screenshot_path):
        for state in self.states:
            if state.screenshot_path == screenshot_path:
                return state.pkl_path
        print(f"states len: {len(self.states)}, states: {self.states}")
        state_name = f"state{len(self.states)}"
        pkl_path = f"state_pkls/{state_name}.pkl"
        new_state = State(state_name, screenshot_path, pkl_path)
        self.states.append(new_state)
        new_state.save_to_pkl()
        self.save_to_pkl()
        return new_state.pkl_path

    def save_to_pkl(self):
        with open(self.filepath, 'wb') as pklfile:
            pickle.dump(self.states, pklfile)

    def load_from_pkl(self):
        try:
            with open(self.filepath, 'rb') as pklfile:
                self.states = pickle.load(pklfile)
        except (FileNotFoundError, EOFError, pickle.UnpicklingError):
            print("Pickle file not found, empty, or corrupted. Starting with an empty list.")


# Primero, creamos una instancia de StatesManager
states_manager = StatesManager("states.pkl")
