class UIElement:
    def __init__(self, coordinates, text, confidence):
        self.coordinates = coordinates
        self.text = text
        self.confidence = confidence

    def __str__(self):
        return f"UIElement(coordinates={self.coordinates}, text='{self.text}', confidence={self.confidence})"
