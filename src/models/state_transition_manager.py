import csv
from collections import deque

from src.models.states_manager import State


class StateTransitionManager:
    def __init__(self, action_executioner, states_manager):
        print(action_executioner, states_manager)
        self.state_transitions = []
        self.states_manager = states_manager
        self.loaded = False
        self.action_executioner = action_executioner
        self.load_from_csv()
        self.graph = {}

    def add(self, init_state_path, actions_path, final_state_path, name):
        state_transition = StateTransition(
            self.action_executioner,
            init_state_path,
            actions_path,
            [final_state_path],
            self.states_manager,
            name=name
        )

        self.state_transitions.append(state_transition)
        #self.save_to_csv() #TODO: OJO DE VERDAS SE PUEDE CQAUITAR?

    def add_using_screenshots(self, init_state_screenshot_path, actions_path, final_state_screenshot_path):
        init_state = self.states_manager.add_state_from_screenshot(init_state_screenshot_path)
        final_state = self.states_manager.add_state_from_screenshot(final_state_screenshot_path)
        state_transition = StateTransition(
            self.action_executioner,
            init_state,
            actions_path,
            [final_state],
            self.states_manager
        )
        self.state_transitions.append(state_transition)
        self.save_to_csv()

#TODO: AQUI ESTA EL PROBLEMAAAA SE COMPARA PATH CON STATE
    def get_by_start_state(self, start_state):
        for state_transition in self.state_transitions:
            if start_state == state_transition.get_init_states():
                return [state_transition]

        return None

    # TODO: MEJORAR ALGORITMO Y GRAFO, ACTUALMENTE SE CONTEMPLA SOLO UN ESTADO INICIAL POSIBLE

    from collections import deque

    def get_fixed_path(self, transaction_name):
        for transition in self.state_transitions:
            if transition.name == transaction_name:
                return transition


    def find_path(self, start_state, goal_state):
        print("---Búsqueda en grafo de estados---")
        print("Estado inicial:", start_state)
        print("Estado objetivo:", goal_state)
        print("-------------------")

        visited = set()
        queue = deque([(start_state, [])])

        while queue:
            current_state, current_path = queue.popleft()
            print("Estado actual:", current_state, "| Camino actual:", current_path)

            if current_state == goal_state:
                print("Estado objetivo alcanzado. Camino:", current_path)
                return current_path

            if current_state not in visited:
                visited.add(current_state)
                transitions = self.get_by_start_state(current_state)##################

                if transitions is not None:
                    for transition in transitions:
                        print("Transición encontrada:", transition)
                        for final_state in transition.get_final_states():
                            print("Añadiendo al estado final a la cola:", final_state)
                            queue.append((final_state, current_path + [transition]))
                else:
                    print("No se encontraron transiciones para el estado:", current_state)
            else:
                print("Estado ya visitado:", current_state)

        print("No se encontró un camino.")
        return None


    def save_to_csv(self, filepath='src/persistence/state_transitions.csv'):
        with open(filepath, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Initial State', 'Actions', 'Final State', 'Name'])
            for transition in self.state_transitions:
                for action in transition.actions_paths_list:
                    for final_state in transition.final_states:
                        print("-------------", transition.initial_state,
                            action,
                            final_state)
                        writer.writerow([
                            transition.initial_state,
                            action,
                            final_state
                        ])

    def load_from_csv(self, filepath='src/persistence/state_transitions.csv'):
        try:
            with open(filepath, 'r', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    self.add(row['Initial State'], row['Actions'], row['Final State'], row['Name'])
                self.loaded = True
        except FileNotFoundError:
            print("CSV file not found. Starting with an empty list.")

    def __repr__(self):
        return f"<TransitionActionsManager transitions={self.state_transitions}>"


class StateTransition:
    def __init__(self, action_executioner, initial_state, actions_path, final_states,
                 states_manager, name=""):
        self.action_executioner = action_executioner
        self.states_manager = states_manager
        self.initial_state = initial_state
        for final_state in final_states:
            final_states = self.states_manager.add_from_path(final_state)
        self.final_states = [final_states]
        self.actions_paths_list = [actions_path]
        self.name = name

    def get_final_states(self):
        states = []
        for state_path in self.final_states:
            state = State.load_from_pkl(state_path)
            states.append(state)
        return states

    def get_init_states(self):
        state = State.load_from_pkl(self.initial_state)
        return state

    def execute(self, ordered_params):
        #TODO: HACER QUE EJECUTE LA SECUENCIA DE ACCIONES PROPIA DE LA TRANSICION NO HARDCODED
        self.action_executioner.play_events(self.actions_paths_list[0], ordered_params)

    def __repr__(self):
        return (f"<TransitionAction initial={self.initial_state}, "
                f"actions={self.actions_paths_list}, finals={self.final_states}>")
