import threading
import time
from queue import Queue

import config


class Transaction:
    def __init__(self, name, window_manager, state_transition_manager, target_state, params_values):
        print("Param values------->", params_values)
        self.name = name
        self.window_manager = window_manager
        self.state_transition_manager = state_transition_manager
        self.init_state = self.get_current_state()
        self.target_state = target_state
        self.params_values = params_values

    def get_current_state(self):
        screenshot_path = self.window_manager.window_screenshot("temp_screenshot.png")
        state = self.state_transition_manager.states_manager.find_if_state_already_exists(screenshot_path)
        if state is None:
            print("No se ha encontrado ningun estado mapeado que coincida con la UI.")

        return state

    def get_target_state(self):
        print("SE PIDE EL TARGET STATE", self.target_state)
        return self.target_state

    def execute(self):
        print("Executing transaction")
        retries = 0
        init_state = self.get_current_state()
        target_state = self.get_target_state()
        print("{{{{{", init_state)
        print("{{{{{", target_state)
        while init_state != target_state:
            path = self.state_transition_manager.find_path(init_state, target_state)
            print("#####AUQI EL PATH:", path)
            if path:
                path[0].execute(self.params_values)
                retries = 0
            else:
                time.sleep(3)
                print("############################################################",retries,"NO HA ENCONTRADO PATH")
                if retries > config.MAX_RETRY_NUMBER_FINDING_PATH:
                    raise Exception("There wasn't a viable path of comands programmed in order to arrive to"
                                    "the desired state")
                retries += 1
                print("No se ha encontrado un path")
            init_state = self.get_current_state()
        print("cliente añadidio")


class TransactionQueue:
    def __init__(self):
        self.queue = Queue()
        self.lock = threading.Lock()
        self.thread = threading.Thread(target=self._run_transactions)
        self.thread.daemon = True  # Hace que el hilo se cierre si el programa principal termina
        self.thread.start()

    def add_transaction(self, transaction):
        """
        Agrega una transacción a la cola.
        """
        with self.lock:
            self.queue.put(transaction)

    def consume_transaction(self):
        """
        Consume la transacción más antigua de la cola y la ejecuta.
        """
        if not self.queue.empty():
            transaction = self.queue.get()
            try:
                transaction.execute()
            except Exception as e:
                print(f"Error al ejecutar la transacción: {e}")
                raise e
            finally:
                self.queue.task_done()

    def _run_transactions(self):
        """
        Función auxiliar para ejecutar transacciones de forma secuencial.
        """
        while True:
            self.consume_transaction()
            time.sleep(2)
