from src import config
from src.domain.input_event_manager import EventRecorder, EventPlayer, DefaultEventStrategy
from src.domain.window_manager import WindowManager
from src.views.sequence_recorder_controller import SequenceRecorderController
from src.views.sequence_recorder_ui import GUI
from src.domain.ui_analyzer import UIAnalyzer


def main():
    recorder = EventRecorder(DefaultEventStrategy())
    player = EventPlayer()
    window_manager = WindowManager(config.EXECUTABLE_PATH)
    ui_analyzer = UIAnalyzer()

    controller = SequenceRecorderController(
        recorder,
        player,
        window_manager,
        ui_analyzer
    )
    gui = GUI(controller)

    controller.set_gui(gui)
    controller.run()


if __name__ == "__main__":
    main()
