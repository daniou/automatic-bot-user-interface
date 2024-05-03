import config
from src.domain.input_event_manager import EventRecorder, EventPlayer, DefaultEventStrategy
from src.models.state_transition_manager import StateTransitionManager
from src.domain.window_manager import WindowManager
from src.models.states_manager import StatesManager
from src.views.sequence_recorder_controller import SequenceRecorderController
from src.views.sequence_recorder_ui import GUI


def main():
    recorder = EventRecorder(DefaultEventStrategy())
    player = EventPlayer()
    window_manager = WindowManager(config.EXECUTABLE_PATH)
    states_manager = StatesManager("./src/persistence/states.csv")
    state_transition_manager = StateTransitionManager(player, states_manager)

    controller = SequenceRecorderController(
        recorder,
        player,
        window_manager,
        state_transition_manager
    )
    gui = GUI(controller)

    controller.set_gui(gui)
    controller.run()


if __name__ == "__main__":
    main()
