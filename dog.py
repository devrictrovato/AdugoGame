from piece import Piece

class Dog(Piece):
    def __init__(self, board, pos, connections) -> None:
        super().__init__(board, pos, connections)