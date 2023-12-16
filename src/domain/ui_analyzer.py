import easyocr
from src.domain.ui_element import UIElement


class UIAnalyzer:
    def __init__(self, language='es'):
        self.reader = easyocr.Reader([language])
        self.ui_elements = []

    def get_screenshot_state(self, shcreenshot_path):
        return "algo hace"

    def analyze_image(self, image_path):
        # Perform OCR on the image
        result = self.reader.readtext(image_path)

        # Create instances of UIElement based on OCR results
        self.ui_elements = [UIElement(coords, text, confidence) for (coords, text, confidence) in result]

    def get_ui_elements(self):
        return self.ui_elements

    def find_differences(self, other_ui_analyzer):
        differences = []

        # Compare the UI elements of two states
        for element1, element2 in zip(self.ui_elements, other_ui_analyzer.get_ui_elements()):
            if element1.text != element2.text:
                differences.append((element1, element2))

        return differences

    def print_ui_elements(self):
        if not self.ui_elements:
            print("No UIElements detected.")
        else:
            for index, ui_element in enumerate(self.ui_elements, start=1):
                print(f"UIElement {index}:", ui_element)