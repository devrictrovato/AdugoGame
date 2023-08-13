class Piece:
    def __init__(self, board, pos, connections) -> None:
        # Inicializando a peça no tabuleiro
        self.board = board
        self.pos = pos
        self.board[pos] = self
        self.connections = self.links(connections)

    def links(self, connections):
        # Conectando as posicoes proximas
        c = {}
        for x, y in connections:
           c[(x, y)] = self.board[x][y]
        return c
    
    def evaluate(self, *rewards):
        # Valorizando esta posicao no tabuleiro
        result = 0
        for _, v in self.connections.items():
            result += 1 if isinstance(v, rewards) else -len(self.connections)
        return result
    
    def moves(self, *invalids):
        # Verificando os movimentos validos
        moves = {}
        for k, v in self.connections.items():
            if not isinstance(self.board[k], invalids):
                moves[k] = v
        return moves
    
    def swap(self, other): # Troca a posicao atual com outra
        self.board[self.pos], self.board[other.pos] = other, self
    
    def __repr__(self) -> str: # Visualizacao no tabuleiro
        return str(self.__class__.__name__)
    
    def __lt__(self, other): # Comparador para o algoritmo minimax
        return self.evaluate(Piece) < other.evaluate(Piece)