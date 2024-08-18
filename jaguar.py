from piece import Piece

class Jaguar(Piece):
    def __init__(self, position):
        # Inicializa a onça usando o construtor da classe base `Piece`
        # A posição é definida e o símbolo 'J' é atribuído para representar a onça no tabuleiro
        super().__init__(position, 'J')

    def move(self, new_position, controller):
        # Verifica se o movimento da onça é válido usando o controlador
        if controller.is_valid_move(self.position, new_position):
            # Se válido, atualiza a posição da onça
            self.position = new_position
            return True  # Retorna True para indicar que o movimento foi bem-sucedido
        return False  # Movimento inválido
