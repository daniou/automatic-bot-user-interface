import csv
from collections import deque


class StateTransitionManager:
    def __init__(self, action_executioner, states_manager):
        self.state_transitions = []
        self.states_manager = states_manager
        self.loaded = False
        self.load_from_csv()
        self.action_executioner = action_executioner
        self.graph = {}

    def add(self, init_state_screenshot_path, actions_path, final_state_screenshot_path):
        state_transition = StateTransition(
            self.action_executioner,
            init_state_screenshot_path,
            actions_path,
            final_state_screenshot_path,
            self.states_manager
        )
        self.state_transitions.append(state_transition)
        if self.loaded:
            self.save_to_csv()
        init_state = state_transition.get_init_states()
        if init_state not in self.graph:
            self.graph[init_state] = []
        self.graph[init_state].append(state_transition)
        print(self.state_transitions)

    def find_path(self, start_state, goal_state):
        try:
            print("---SALSEO GRAFERO---")
            print(start_state)
            print(goal_state)
            print("-------------------")

            visited = set()
            queue = deque([(start_state, [])])

            while queue:
                current_state, path = queue.popleft()
                if current_state == goal_state:
                    return path

                print(f"HASTAA QUI3 {type(current_state)}: {current_state},\n {type(visited)}: {visited} ")
                if current_state in visited:
                    continue

                visited.add(current_state)

                # Ahora, verifica las transiciones desde el estado actual
                transitions = self.graph.get(current_state, [])
                for transition in transitions:
                    next_state = transition.final_states
                    if next_state not in visited:
                        new_path = path + [transition]
                        queue.append((next_state, new_path))
            return None

        except Exception as e:
            # Manejar cualquier excepción no especificada
            print(f"Error al buscar path de ejecución para transicionar de estado: {str(e)}")
            return None


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
                    self.add(row['Initial State'], row['Actions'], row['Final State'])
                self.loaded = True
        except FileNotFoundError:
            print("CSV file not found. Starting with an empty list.")

    def __repr__(self):
        return f"<TransitionActionsManager transitions={self.state_transitions}>"


class StateTransition:
    def __init__(self, action_executioner, initial_state_screenshot_path, actions_path, final_state_screenshot_path,
                 states_manager):
        self.action_executioner = action_executioner
        self.states_manager = states_manager
        self.initial_state = self.states_manager.add(initial_state_screenshot_path)
        self.final_states = [self.states_manager.add(final_state_screenshot_path)]
        self.actions_paths_list = [actions_path]

    def add_final_state_screenshot(self, screenshot_path):
        self.final_states.append(self.states_manager.add(screenshot_path))

    def get_final_states(self):
        return self.final_states

    def get_init_states(self):
        return self.initial_state

    def execute(self):
        self.action_executioner.play_events("src/persistence/add_client.csv")

    def __repr__(self):
        return (f"<TransitionAction initial={self.initial_state}, "
                f"actions={self.actions_paths_list}, finals={self.final_states}>")
