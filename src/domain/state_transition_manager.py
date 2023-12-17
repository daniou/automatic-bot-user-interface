import csv
from src.domain.states_manager import states_manager


class StateTransitionManager:
    def __init__(self):
        self.state_transitions = []
        self.load_from_csv()
        self.loaded = False

    def add_state_transition(self, init_state_screenshot_path, actions_path, final_state_screenshot_path):

        state_transition = StateTransition(
            init_state_screenshot_path,
            actions_path,
            final_state_screenshot_path
        )
        self.state_transitions.append(state_transition)
        if self.loaded:
            self.save_to_csv()
        print(self.state_transitions)

    def save_to_csv(self, filepath='state_transitions.csv'):
        with open(filepath, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Initial State', 'Actions', 'Final State'])
            for transition in self.state_transitions:
                for action in transition.actions_paths_list:
                    for final_state in transition.final_states:
                        writer.writerow([
                            transition.initial_state,
                            action,
                            final_state
                        ])

    def load_from_csv(self, filepath='state_transitions.csv'):
        try:
            with open(filepath, 'r', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    self.add_state_transition(row['Initial State'], row['Actions'], row['Final State'])
                self.loaded = True
        except FileNotFoundError:
            print("CSV file not found. Starting with an empty list.")

    def __repr__(self):
        return f"<TransitionActionsManager transitions={self.state_transitions}>"


class StateTransition:
    def __init__(self, initial_state_screenshot_path, actions_path, final_state_screenshot_path):
        self.initial_state = states_manager.add_state(initial_state_screenshot_path)
        self.final_states = [states_manager.add_state(final_state_screenshot_path)]
        self.actions_paths_list = [actions_path]

    def add_final_state_screenshot(self, screenshot_path):
        self.final_states.append(states_manager.add_state(screenshot_path))

    def get_final_states(self):
        return self.final_states

    def get_init_states(self):
        return self.initial_state

    def __repr__(self):
        return (f"<TransitionAction initial={self.initial_state}, "
                f"actions={self.actions_paths_list}, finals={self.final_states}>")
