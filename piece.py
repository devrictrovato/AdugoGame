class Piece:
    def __init__(self, board, pos, connections) -> None:
        # Inicializando a peça no tabuleiro
        self.board = board
        self.pos = pos
        self.board[pos] = self
        self.connections = self.set_connections(connections)

    def set_connections(self, connections):
        # Conectando os espaços proximos
        c = {}
        for x, y in connections:
           c[(x, y)] = self.board[x][y]
        return c
    
    def evaluate(self, penality):
        # Avaliando o local deste ponto no tabuleiro
        result = 0
        for _, v in self.connections.items():
            result += 1 if isinstance(v, penality) else -len(self.connections)
        return result
    
    def get_moves(self, invalids):
        # Verificando os movimentos validos
        moves = {}
        for k, v in self.connections.items():
            if not isinstance(self.board[k], invalids):
                moves[k] = v
        return moves
    
    def __repr__(self) -> str: # Representação no tabuleiro
        return str(self.__class__.__name__)