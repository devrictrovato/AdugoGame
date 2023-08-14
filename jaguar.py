from dog import Dog
from piece import Piece
import utils

class Jaguar(Piece):
    def __init__(self, board, pos, connections) -> None:
        super().__init__(board, pos, connections)

    def move_to(self, x, y):
        # Verificando a posicao escolhida
        check = utils.distance(self.pos, (x, y))
        new_pos = self.board[x, y]

        if check < 3:
            # Verificando o pulo do jogador
            jump = utils.middle(self.pos, (x, y))
            dog = self.board[jump]
            if isinstance(dog, Dog) and not isinstance(new_pos, Dog):
                print('Cachorro removido')
                self.board[jump] = Piece(dog.board, dog.pos, dog.connections)
                self.swap(new_pos)
            else:
                print('Movimento invalido')
        # Troca simples sem envolver o pulo
        elif check < 2 and isinstance(new_pos, Piece): 
            self.swap(new_pos)
        else:
            print('Movimento invalido')