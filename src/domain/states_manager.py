import csv


class StatesManager:
    def __init__(self):
        self.states = []

    def add_state(self, screenshot_path, name=None):
        for state in self.states:
            if state.screenshot_path == screenshot_path:
                return state

        new_state = State(name, screenshot_path)
        self.states.append(new_state)
        self.save_to_csv()
        return new_state

    def save_to_csv(self, filepath='states.csv'):
        with open(filepath, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Name', 'Screenshot Path'])
            for state in self.states:
                writer.writerow([state.name, state.screenshot_path])


class State:
    def __init__(self, name, screenshot_path):
        self.name = name
        self.screenshot_path = screenshot_path

    def __repr__(self):
        return f"<State name={self.name}, screenshot={self.screenshot_path}>"


states_manager = StatesManager()
