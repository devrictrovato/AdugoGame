class Piece:
    def __init__(self, position, symbol):
        # A classe `Piece` é a classe base para as peças do jogo, como onça e cachorro
        # Inicializa a posição e o símbolo da peça
        self.position = position  # Posição no tabuleiro, representada como uma tupla (linha, coluna)
        self.symbol = symbol  # Símbolo da peça, por exemplo, 'J' para onça e 'D' para cachorro
