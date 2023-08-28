from dog import Dog
from piece import Piece
import utils

class Jaguar(Piece):
    def __init__(self, board, pos, connections) -> None:
        super().__init__(board, pos, connections)
        self.score = 0

    def move(self, x, y):
        '''
            2.8 | 2.2 | 2.0 | 2.2 | 2.8
            2.2 | 1.4 | 1.0 | 1.4 | 2.2
            2.0 | 1.0 | Jog | 1.0 | 2.0
            2.2 | 1.4 | 1.0 | 1.4 | 2.2
            2.8 | 2.2 | 2.0 | 2.2 | 2.8
        '''

        # Verificando a posicao escolhida
        check = utils.distance(self.pos, (x, y))
        new_pos = self.board[(x, y)]

        if check < 2:
            # Movimento simples
            avaliable = new_pos.pos in self.connections.keys()
            if avaliable and not isinstance(new_pos, Dog):
                self.swap(new_pos)
                return True, None
        elif check < 3:
            # Verificando o pulo do jogador
            jump = utils.middle(self.pos, (x, y))
            dog = self.board[jump]
            
            # Movimentacao no triangulo
            if type(dog) == int:
                # Movimento simples
                avaliable = new_pos.pos in self.connections.keys()
                if avaliable and not isinstance(new_pos, Dog):
                    self.swap(new_pos)
                    return True, None
                
            # Verificando as posicoes conectadas intermediarias
            try:
                conns = dog.connections.keys()
            except:
                return False, None
            diagonal = not 2.2 < check < 2.3
            avaliable = new_pos.pos in conns and self.pos in conns and diagonal
            # Execucao do pulo
            if avaliable and isinstance(dog, Dog) and not isinstance(new_pos, Dog):
                self.swap(new_pos)
                dog.remove()
                self.score += 1
                return True, dog
        elif check > 3:
            player = self.pos == (6, 0) or self.pos == (6, 4)
            dog = self.board[utils.middle(self.pos, (x, y))]
            adjustdog = dog.pos == (6, 2) and isinstance(dog, Dog)
            if player and adjustdog:
                self.swap(new_pos)
                dog.remove()
                self.score += 1
                return True, dog
        return False, None
        