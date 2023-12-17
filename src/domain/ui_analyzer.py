import easyocr
from src.domain.ui_element import UIElement


class UIAnalyzer:
    def __init__(self, language='es'):
        self.reader = easyocr.Reader([language])

    def get_ui(self, image_path):
        result = self.reader.readtext(image_path)
        ui_elements = [UIElement(coords, text, confidence) for (coords, text, confidence) in result]
        return ui_elements

    @staticmethod
    def find_differences(ui, other_ui):
        differences = []
        # Asegurarse de que ambos UI tienen la misma longitud
        if len(ui) != len(other_ui):
            return "UIs have different lengths"

        for element1, element2 in zip(ui, other_ui):
            if element1 != element2:

                differences.append((element1, element2))
        return differences

    def are_equal(self, screenshot1, screenshot2):
        ui1 = self.get_ui(screenshot1)
        ui2 = self.get_ui(screenshot2)
        return len(UIAnalyzer.find_differences(ui1, ui2)) == 0

    @staticmethod
    def are_uis_equal(ui1, ui2):
        return len(UIAnalyzer.find_differences(ui1, ui2)) == 0

ui_analyzer = UIAnalyzer()
