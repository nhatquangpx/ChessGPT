
class Piece:

    def __init__(self, name, color, value, texture, texture_rect = None):
        self.name = name
        self.color = color
        self.value = value
        self.texture = texture
        self.texture_rect = texture_rect

class Pawn(Piece):

    def__init__(self, color):
        if color == "white":        