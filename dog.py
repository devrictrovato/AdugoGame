from piece import Piece

class Dog(Piece):
    def __init__(self, position):
        # Inicializa o cachorro usando o construtor da classe base `Piece`
        # A posição é definida e o símbolo 'D' é atribuído para representar o cachorro no tabuleiro
        super().__init__(position, 'D')

    def move(self, new_position, controller):
        # Verifica se o movimento do cachorro é válido usando o controlador
        if controller.is_valid_move(self.position, new_position):
            # Se válido, atualiza a posição do cachorro
            self.position = new_position
            return True  # Retorna True para indicar que o movimento foi bem-sucedido
        return False  # Movimento inválido
