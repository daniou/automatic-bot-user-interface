from abc import ABC, abstractmethod
import csv
import time
import keyboard
import pyautogui

from config import WAIT_BETWEEN_INPUT_INERACTIONS_PERIOD


class EventRecorder:
    def __init__(self, strategy):
        self.strategy = strategy

    def record_events(self, filename):
        try:
            recorded = keyboard.record(until='enter')
            simplified_events = self.strategy.simplify_events(recorded)
            # Calcular la duración entre el evento actual y el próximo en la última columna
            simplified_events = self.strategy.calculate_durations(simplified_events)

            # Guardar en formato CSV
            self.strategy.save_to_csv(filename, simplified_events)
        except Exception as e:
            print("Error al guardar la secuencia", str(e))


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


class PlayerCommand:
    def __init__(self, key_name, event_type):
        self.key_name = key_name
        self.event_type = event_type

    def execute(self):
        if self.event_type == 'down':
            keyboard.press_and_release(self.key_name)


class EventPlayer:
    def __init__(self, play_speed=1.0/WAIT_BETWEEN_INPUT_INERACTIONS_PERIOD):
        self.play_speed = play_speed

    def play_events(self, csv_file):
        try:
            with open(csv_file, newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                for row_number, row in enumerate(reader, start=1):
                    if len(row) != 4:
                        raise ValueError(
                            f"Invalid CSV format at row {row_number}. Each row should have 4 columns. Row content: {row}")

                    event_type, key_name, _, duration = row

                    try:
                        duration = float(duration)
                    except ValueError as e:
                        raise ValueError(f"Error parsing timestamp in row {row_number}: {row}") from e

                    if self.play_speed > 0:
                        time.sleep(duration / self.play_speed)  # Wait until the specified timestamp

                    command = PlayerCommand(key_name, event_type)
                    command.execute()

        except FileNotFoundError as e:
            print(f"Error: File '{csv_file}' not found.")
        except Exception as e:
            print(f"An error occurred: {e}")


class KeyboardTypist:
    def type_text_in_keyboard(self, text, wait_interval=WAIT_BETWEEN_INPUT_INERACTIONS_PERIOD):
        for character in text:
            wait_interval = 0 if wait_interval <= 0 else wait_interval
            pyautogui.typewrite(character, interval=wait_interval)
