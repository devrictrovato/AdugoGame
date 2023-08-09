from piece import Piece

class Jaguar(Piece):
    def __init__(self, board, pos, connections) -> None:
        super().__init__(board, pos, connections)