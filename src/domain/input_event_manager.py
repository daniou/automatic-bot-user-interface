from abc import ABC, abstractmethod
import csv
import time
import keyboard
import pyautogui

import config 


class EventRecorder:
    def __init__(self, strategy):
        self.strategy = strategy

    def record_events(self):
        try:
            recorded = keyboard.record(until='enter')
            simplified_events = self.strategy.simplify_events(recorded)
            # Calcular la duración entre el evento actual y el próximo en la última columna
            simplified_events = self.strategy.calculate_durations(simplified_events)

            # Guardar en formato CSV
            return simplified_events
        except Exception as e:
            print("Error al guardar la secuencia", str(e))

    def record_and_save_events(self, filename):
        try:
            events = self.record_events()
            return self.strategy.save_to_csv(filename, events)

        except Exception as e:
            raise e


class EventStrategy(ABC):
    @abstractmethod
    def simplify_events(self, recorded):
        pass

    @abstractmethod
    def calculate_durations(self, simplified_events):
        pass

    @abstractmethod
    def save_to_csv(self, filename, simplified_events):
        pass


class DefaultEventStrategy(EventStrategy):
    def simplify_events(self, recorded):
        return [(event.event_type, event.name, event.scan_code, event.time) for event in recorded if
                not event.event_type.startswith('up')]

    def calculate_durations(self, simplified_events):
        return [
            (*e[:-1], simplified_events[i + 1][-1] - e[-1]) if i < len(simplified_events) - 1 else (*e[:-1], 0)
            for i, e in enumerate(simplified_events)
        ]

    def save_to_csv(self, filename, simplified_events):
        with open(filename, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerows(simplified_events[:-1])
            return filename


class PlayerCommand:
    def __init__(self, param, event_type):
        self.param = param
        self.event_type = event_type

    def execute(self):
        if self.event_type == 'down':
            keyboard.press_and_release(self.param)
        elif self.event_type == 'write':
            KeyboardTypist.type_text_in_keyboard(self.param)
        elif self.event_type == "insert":
            KeyboardTypist.type_text_in_keyboard(self.param)
        elif self.event_type == "right_click":
            x_str, y_str = self.param.split(",")
            x = int(x_str)
            y = int(y_str)
            pyautogui.click(x, y)
        elif self.event_type == "hotkey":
            special_key, key = self.param.split("+")
            pyautogui.hotkey(special_key, key)

        else:
            raise Exception("The event in the csv cant be reproduced.")


class EventPlayer:
    def __init__(self, wait_interval=config.WAIT_BETWEEN_INPUT_INERACTIONS_PERIOD):
        if wait_interval <= 0:
            self.play_speed = 1.0  # Default or maximum speed
        else:
            self.play_speed = 1.0 / wait_interval  # Calculated play speed based on the interval

    def play_events(self, csv_file, ordered_params=None):
        parameters_inserted = 0
        try:
            with open(csv_file, newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                for row_number, row in enumerate(reader, start=1):
                    if len(row) != 4:
                        raise ValueError(
                            f"Invalid CSV format at row {row_number}. Each row should have 4 columns. Row content: {row}")

                    event_type, csv_param, _, duration = row

                    try:
                        #print("Aqui la duracion:", duration)
                        if duration:
                            duration = float(duration)
                        else:
                            duration = 0
                    except ValueError as e:
                        print(f"Warning: Invalid duration format in row {row_number}, setting duration to 0.")
                        duration = 0

                    if self.play_speed > 0:
                        time.sleep(duration / self.play_speed)  # Wait until the specified timestamp
                    param = csv_param
                    if event_type == "insert":
                        #print("ENTERED INSEERT EVENT;: ",ordered_params)
                        param = ordered_params[parameters_inserted]
                        parameters_inserted += 1
                        #print("INSERT TYPE EVENT:", param)


                    command = PlayerCommand(param, event_type)
                    command.execute()

        except FileNotFoundError as e:
            print(f"Error: File '{csv_file}' not found.")
        except Exception as e:
            print(f"An error occurred: {e}")
            raise e


class KeyboardTypist:
    @staticmethod
    def type_text_in_keyboard(text, wait_interval=config.WAIT_BETWEEN_INPUT_INERACTIONS_PERIOD):
        pyautogui.typewrite(text, interval=wait_interval)
