import threading
import time
from queue import Queue
import os
import csv
import pickle
import datetime
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
        while init_state != target_state:
            try:
                path = self.state_transition_manager.find_path(init_state, target_state)
                if path:
                    path[0].execute(self.params_values)
                    retries = 0
                else:
                    time.sleep(3)
                    if retries > config.MAX_RETRY_NUMBER_FINDING_PATH:
                        self.log_failure_details()
                        break
                    retries += 1
                init_state = self.get_current_state()
            except Exception as e:
                self.log_failure_details()
                raise e
        print("Transacción completada")


    def log_failure_details(self):
        print("GUARDANDO LOGS DE ERROR")
        csv_file = "src/persistence/failure_log.csv"
        if not os.path.exists(csv_file):
            with open(csv_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Name", "Init State", "Target State", "Timestamp", "Params Values"])
        with open(csv_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([self.name, self.init_state, self.target_state, datetime.datetime.now(), self.params_values])

# Ejemplo de uso:
# retry_failed_transactions()

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