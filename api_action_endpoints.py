from flask import Flask, request, jsonify
import config
from src.domain.input_event_manager import EventPlayer
from src.domain.window_manager import WindowManager
from src.models.state_transition_manager import StateTransitionManager
from src.models.states_manager import StatesManager
from transaction import Transaction, TransactionQueue

app = Flask(__name__)


class Preprocessor:
    @staticmethod
    def get_params_values_in_insertion_order(data):
        # Asumimos que 'data' es un diccionario JSON
        return [str(value) for key, value in data.items()]


@app.route('/clients', methods=['POST'])
def create_client():
    data = request.get_json()
    params_values = Preprocessor.get_params_values_in_insertion_order(data)
    target_state = states_manager.find_state_with_id_text(config.added_client_id_text_in_ui)
    create_client = Transaction("add_client", window_manager, state_transition_manager, target_state, params_values)
    transaction_queue.add_transaction(create_client)
    return jsonify({"message": "Client added successfully"}), 201


@app.route('/vehicles', methods=['POST'])
def create_vehicle():
    data = request.get_json()
    # add_vehicle(data)
    return jsonify({"message": "Vehicle added successfully"}), 201


@app.route('/clients/<int:client_id>', methods=['PUT'])
def update_client(client_id):
    return jsonify({"message": "Client added successfully"}), 201
    data = request.get_json()
    result, status_code = edit_client(client_id, data)
    return jsonify(result), status_code


@app.route('/vehicles/<int:vehicle_id>', methods=['PUT'])
def update_vehicle(vehicle_id):
    return jsonify({"message": "Client added successfully"}), 201
    data = request.get_json()
    result, status_code = edit_vehicle(vehicle_id, data)
    return jsonify(result), status_code


if __name__ == '__main__':
    player = EventPlayer()
    window_manager = WindowManager(config.EXECUTABLE_PATH)
    states_manager = StatesManager("./src/persistence/states.csv")
    state_transition_manager = StateTransitionManager(player, states_manager)
    transaction_queue = TransactionQueue()
    app.run(debug=True)
