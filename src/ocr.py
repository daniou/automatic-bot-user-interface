import easyocr

from src.models.ui_element import UIElement

# Initialize the OCR reader
reader = easyocr.Reader(['es'])

# Perform OCR on the image
result = reader.readtext('login.png')

# Create instances of UIElement based on OCR results
ui_elements = [UIElement(coords, text, confidence) for (coords, text, confidence) in result]


# Print the text of the first UIElement
if ui_elements:
    print("Text from the first UIElement:", ui_elements[0].text)
else:
    print("No UIElements detected.")

# You might also want to capture the screen using the Screen class
# For example, if the Screen class has a method like capture_screen()
# screen.capture_screen()
