from flask import Flask, request, jsonify
import config
from src.domain.input_event_manager import EventPlayer
from src.domain.window_manager import WindowManager
from src.models.state_transition_manager import StateTransitionManager
from src.models.states_manager import StatesManager
from src.models.transaction import Transaction, TransactionQueue


app = Flask(__name__)



class Preprocessor:
    @staticmethod
    def get_params_values_in_insertion_order(data):
        # Asumimos que 'data' es un diccionario JSON
        return [str(value) for key, value in data.items()]
    
    @staticmethod
    def get_nif(data):
        # Suponiendo que el NIF está almacenado en la clave 'nif' del diccionario 'data'
        if 'nif' in data:
            return data['nif']
        else:
            return None  # O podrías lanzar una excepción o manejarlo de otra manera según tu lógica de aplicación


    

@app.route('/')
def index():
    return "¡Has conectado con la API de TallerBot!"


@app.route('/add_client', methods=['POST'])
def create_client():
    data = request.get_json()
    params_values = Preprocessor.get_params_values_in_insertion_order(data)
    target_state = states_manager.find_state_with_id_text(config.added_client_id_text_in_ui)
    print("Target state", target_state)
    create_client = Transaction("add_client", window_manager, state_transition_manager, target_state, params_values, data)
    transaction_queue.add_transaction(create_client)
    return jsonify({"message": "Client added successfully"}), 201

@app.route('/edit_client', methods=['POST'])
def edit_client():
    data = request.get_json()
    params_values = Preprocessor.get_params_values_in_insertion_order(data)
    params_values = [params_values[len(params_values)-1]] + params_values
    target_state = states_manager.find_state_with_id_text(config.added_client_id_text_in_ui)
    edit_client = Transaction("edit_client", window_manager, state_transition_manager, target_state, params_values, data)
    transaction_queue.add_transaction(edit_client)
    return jsonify({"message": "Client edited successfully"}), 201


@app.route('/add_vehicle', methods=['POST'])
def create_vehicle():
    data = request.get_json()
    params_values = Preprocessor.get_params_values_in_insertion_order(data)
    target_state = states_manager.find_state_with_id_text(config.added_vehicle_id_text_in_ui)
    print("Target state", target_state)
    create_vehicle = Transaction("edit_vehicle", window_manager, state_transition_manager, target_state, params_values, data)
    transaction_queue.add_transaction(create_vehicle)
    return jsonify({"message": "Vehicle added successfully"}), 201

@app.route('/edit_vehicle', methods=['POST'])
def edit_vehicle():
    data = request.get_json()
    params_values = Preprocessor.get_params_values_in_insertion_order(data)
    target_state = states_manager.find_state_with_id_text(config.added_client_id_text_in_ui)
    edit_vehicle = Transaction("edit_vehicle", window_manager, state_transition_manager, target_state, params_values, data)
    transaction_queue.add_transaction(edit_vehicle)
    return jsonify({"message": "Vehicle edited successfully"}), 201


player = EventPlayer()
window_manager = WindowManager(config.EXECUTABLE_PATH)
states_manager = StatesManager("./src/persistence/states.csv")
state_transition_manager = StateTransitionManager(player, states_manager)
transaction_queue = TransactionQueue()

if __name__ == "__main__":
    app.run(debug=True)
