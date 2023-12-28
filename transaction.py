import threading
import time
from queue import Queue


class Transaction:
    def __init__(self, name, window_manager, state_transition_manager, target_state):
        self.name = name
        self.window_manager = window_manager
        self.state_transition_manager = state_transition_manager
        self.init_state = self.get_init_state()
        self.current_state_transition = self.get_current_state_transition()
        self.target_state = target_state
        print("Target state------->", target_state)

    def get_init_state(self):
        screenshot_path = self.window_manager.window_screenshot("temp_screenshot.png")
        state = self.state_transition_manager.states_manager.find_if_state_already_exists(screenshot_path)
        if state is None:
            print("No se ha encontrado ningun estado mapeado que coincida con la UI.")

        return state


    def get_target_state(self):
        return self.target_state

    def get_current_state_transition(self):
        pass

    def execute(self):
        # Check state
        # Find path
        # Execute orders
        # Check state
        # Get next orders
        print("Executing transaction")

        path = self.state_transition_manager.find_path(self.get_init_state(), self.get_target_state())
        #self.state_transition_manager[0].execute()
        print(path, "cliente añadidio")


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
            finally:
                self.queue.task_done()

    def _run_transactions(self):
        """
        Función auxiliar para ejecutar transacciones de forma secuencial.
        """
        while True:
            self.consume_transaction()
            time.sleep(2)
