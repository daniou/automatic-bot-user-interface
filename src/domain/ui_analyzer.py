import easyocr
from src.models.ui_element import UIElement


class UIAnalyzer:
    def __init__(self, language='es'):
        self.reader = easyocr.Reader([language])

    def get_ui(self, image_path):
        print("Image path:", image_path)
        result = self.reader.readtext(image_path)
        ui_elements = [UIElement(coords, text, confidence) for (coords, text, confidence) in result]
        return ui_elements

    @staticmethod
    def ui_contains_text(ui, text):
        ui_text = UIAnalyzer.get_text(ui)
        return text in ui_text

    @staticmethod
    def get_text(ui):
        texts = [element.text for element in ui]
        full_text = ' '.join(texts)
        return full_text

    @staticmethod
    def find_differences(ui, other_ui):
        # Extract text from both UIElement lists
        ui_text = UIAnalyzer.get_text(ui)
        other_ui_text = UIAnalyzer.get_text(other_ui)

        # Find the differences between the two texts
        differences = set(ui_text.split()) ^ set(other_ui_text.split())
        print(f"-------------{differences}")

        return list(differences)

    def are_equal(self, screenshot1, screenshot2):
        ui1 = self.get_ui(screenshot1)
        ui2 = self.get_ui(screenshot2)

        return self.are_uis_equal(ui1, ui2)

    @staticmethod
    def are_uis_equal(ui1, ui2):
        are_equal = len(UIAnalyzer.find_differences(ui1, ui2)) == 0
        print(f"@@@END OF PIFOUSTIOU: {are_equal} -> {ui1} == {ui2}")
        return are_equal





ui_analyzer = UIAnalyzer()
