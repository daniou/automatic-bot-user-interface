class UIElement:
    def __init__(self, coordinates, text, confidence):
        self.coordinates = coordinates
        self.text = text
        self.confidence = confidence

    def __str__(self):
        return f"UIElement(coordinates={self.coordinates}, text='{self.text}', confidence={self.confidence})"

    def __eq__(self, other):
        if not isinstance(other, UIElement):
            return False
        return (self.coordinates == other.coordinates) and (self.text == other.text) and (self.confidence == other.confidence)

    def __ne__(self, other):
        return not self.__eq__(other)
