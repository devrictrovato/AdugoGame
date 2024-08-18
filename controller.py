class Controller:
    def __init__(self, board):
        # Referência ao tabuleiro para acessar suas informações (onça, cachorros, etc.)
        self.board = board
        
        # Dicionário que mapeia as conexões entre as posições no tabuleiro
        self.connections = self.get_connections()

    def get_connections(self):
        # Função que retorna as conexões válidas entre as posições no tabuleiro
        # Cada chave é uma posição (linha, coluna) e cada valor é uma lista de posições conectadas a ela
        connections = {
            (0, 0): [(0, 2), (1, 1)],
            (0, 2): [(0, 0), (0, 4), (1, 2)],
            (0, 4): [(0, 2), (1, 3)],
            
            (1, 1): [(0, 0), (1, 2), (2, 2)],
            (1, 2): [(0, 2), (1, 1), (1, 3), (2, 2)],
            (1, 3): [(0, 4), (1, 2), (2, 2)],
            
            (2, 0): [(2, 1), (3, 0), (3, 1)],
            (2, 1): [(2, 0), (2, 2), (3, 1)],
            (2, 2): [(1, 1), (1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2), (3, 3)],
            (2, 3): [(2, 2), (2, 4), (3, 3)],
            (2, 4): [(2, 3), (3, 3), (3, 4)],
            
            (3, 0): [(2, 0), (3, 1), (4, 0)],
            (3, 1): [(2, 0), (2, 1), (2, 2), (3, 0), (3, 2), (4, 0), (4, 1), (4, 2)],
            (3, 2): [(2, 2), (3, 1), (3, 3), (4, 2)],
            (3, 3): [(2, 2), (2, 3), (2, 4), (3, 2), (3, 4), (4, 2), (4, 3), (4, 4)],
            (3, 4): [(2, 4), (3, 3), (4, 4)],

            (4, 0): [(3, 0), (3, 1), (4, 1), (5, 0), (5, 1)],
            (4, 1): [(3, 1), (4, 0), (4, 2), (5, 1)],
            (4, 2): [(3, 1), (3, 2), (3, 3), (4, 1), (4, 3), (5, 1), (5, 2), (5, 3)],
            (4, 3): [(3, 3), (4, 2), (4, 4), (5, 3)],
            (4, 4): [(3, 3), (3, 4), (4, 3), (5, 3), (5, 4)],
            
            (5, 0): [(4, 0), (5, 1), (5, 0)],
            (5, 1): [(4, 0), (4, 1), (4, 2), (5, 0), (5, 2), (5, 0), (5, 1), (5, 2)],
            (5, 2): [(4, 2), (5, 1), (5, 3), (5, 2)],
            (5, 3): [(4, 2), (4, 3), (4, 4), (5, 2), (5, 4), (5, 2), (5, 3), (5, 4)],
            (5, 4): [(4, 4), (5, 3), (5, 4)],
            
            (6, 0): [(5, 0), (5, 1), (6, 1)],
            (6, 1): [(5, 1), (6, 0), (6, 2)],
            (6, 2): [(5, 1), (5, 2), (5, 3), (6, 1), (6, 3)],
            (6, 3): [(6, 2), (5, 3), (6, 4)],
            (6, 4): [(5, 3), (5, 4), (6, 3)],
        }
        return connections # Retorna o dicionário de conexões

    def is_valid_move(self, old_pos, new_pos):
        # Verifica se a nova posição é uma conexão válida a partir da posição antiga
        if new_pos in self.connections.get(old_pos, []):
            # Verifica se a nova posição está vazia no tabuleiro
            if self.board.grid[new_pos[0]][new_pos[1]] == ' ':
                return True  # Movimento válido
        return False  # Movimento inválido

    def move_piece(self, piece, new_pos):
        # Movimenta a peça (onça ou cachorro) para a nova posição, se for um movimento válido
        if self.is_valid_move(piece.position, new_pos):
            piece.position = new_pos  # Atualiza a posição da peça
            return True  # Movimento bem-sucedido
        return False  # Movimento inválido

    def capture_dog(self, jaguar_pos, dog_pos):
        # Calcula a posição de salto, que é a posição além do cachorro, se a onça pular sobre ele
        jump_pos = (2 * dog_pos[0] - jaguar_pos[0], 2 * dog_pos[1] - jaguar_pos[1])
        
        # Verifica se a posição de salto está dentro dos limites do tabuleiro, se há um cachorro na posição e se a posição de salto está vazia
        if (0 <= jump_pos[0] < 7 and 0 <= jump_pos[1] < 5 and
                self.board.grid[dog_pos[0]][dog_pos[1]] == 'D' and
                self.board.grid[jump_pos[0]][jump_pos[1]] == ' '):
            
            # Atualiza a grade para remover o cachorro capturado e colocar a onça na nova posição de salto
            self.board.grid[jaguar_pos[0]][jaguar_pos[1]] = ' '  # A posição original da onça fica vazia
            self.board.grid[dog_pos[0]][dog_pos[1]] = ' '  # A posição do cachorro capturado fica vazia
            self.board.grid[jump_pos[0]][jump_pos[1]] = 'J'  # A nova posição da onça é atualizada
            
            # Atualiza a posição da onça no objeto
            self.board.jaguar.position = jump_pos
            
            # Remove o cachorro capturado da lista de cachorros
            for dog in self.board.dogs:
                if dog.position == dog_pos:
                    self.board.dogs.remove(dog)
                    break
            
            return True  # Captura bem-sucedida
        return False  # Captura inválida

