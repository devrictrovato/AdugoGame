import pygame
from jaguar import Jaguar
from dog import Dog
from controller import Controller  # Gerencia a lógica do jogo

class Board:
    def __init__(self):
        # Inicializa uma grade 7x5 vazia (representada por espaços)
        self.grid = [[' ' for _ in range(5)] for _ in range(7)]
        
        # Posiciona a onça na posição inicial (linha 4, coluna 2)
        self.jaguar = Jaguar((4, 2))
        
        # Coloca os cachorros em suas posições iniciais
        self.dogs = [
            Dog((4, 0)), Dog((4, 1)), Dog((4, 3)), Dog((4, 4)),
            Dog((5, 0)), Dog((5, 1)), Dog((5, 2)), Dog((5, 3)), Dog((5, 4)),
            Dog((6, 0)), Dog((6, 1)), Dog((6, 2)), Dog((6, 3)), Dog((6, 4)),
        ]
        
        # Instancia a classe Controller, que gerencia as regras de movimentação e lógica do jogo
        self.movement = Controller(self)
        
        # Atualiza a grade inicial com as posições da onça e dos cachorros
        self.update_grid()

    def update_grid(self):
        # Reseta a grade e coloca os símbolos dos cachorros e da onça nas posições atuais
        self.grid = [[' ' for _ in range(5)] for _ in range(7)]
        self.grid[self.jaguar.position[0]][self.jaguar.position[1]] = self.jaguar.symbol
        for dog in self.dogs:
            self.grid[dog.position[0]][dog.position[1]] = dog.symbol

    def move_jaguar(self, new_pos):
        # Move a onça para a nova posição se o movimento for válido
        if self.jaguar.move(new_pos, self.movement):
            self.update_grid()  # Atualiza a grade com a nova posição

    def move_dog(self, dog, new_pos):
        # Move um cachorro para a nova posição se o movimento for válido
        if dog.move(new_pos, self.movement):
            self.update_grid()  # Atualiza a grade com a nova posição

    def get_dog_positions(self):
        # Retorna uma lista com as posições atuais de todos os cachorros
        return [dog.position for dog in self.dogs]

    def get_jaguar_position(self):
        # Retorna a posição atual da onça
        return self.jaguar.position

    def draw_board(self, screen, cell_size, colors):
        # Desenha o tabuleiro e as peças (onça e cachorros) no jogo
        for row in range(7):
            for col in range(5):
                # Define os pontos onde as peças podem ser desenhadas
                if (row, col) in [
                    (0, 0), (0, 2), (0, 4),
                    (1, 1), (1, 2), (1, 3), 
                    (2, 0), (2, 1), (2, 2), (2, 3), (2, 4),
                    (3, 0), (3, 1), (3, 2), (3, 3), (3, 4),
                    (4, 0), (4, 1), (4, 2), (4, 3), (4, 4),
                    (5, 0), (5, 1), (5, 2), (5, 3), (5, 4),
                    (6, 0), (6, 1), (6, 2), (6, 3), (6, 4),
                ]:
                    # Desenha a onça com a cor amarela
                    if self.grid[row][col] == 'J':
                        pygame.draw.circle(screen, colors['YELLOW'], (col * cell_size + cell_size // 2, row * cell_size + cell_size // 2), cell_size // 3)
                    # Desenha os cachorros com a cor "TANGO"
                    elif self.grid[row][col] == 'D':
                        pygame.draw.circle(screen, colors['TANGO'], (col * cell_size + cell_size // 2, row * cell_size + cell_size // 2), cell_size // 3)

    def draw_lines(self, screen, cell_size, colors):
        # Desenha as linhas de conexão entre as posições no tabuleiro
        for (start, ends) in self.movement.connections.items():
            start_pos = (start[1] * cell_size + cell_size // 2, start[0] * cell_size + cell_size // 2)
            for end in ends:
                end_pos = (end[1] * cell_size + cell_size // 2, end[0] * cell_size + cell_size // 2)
                pygame.draw.line(screen, colors['BLACK'], start_pos, end_pos, 1)  # Desenha uma linha branca entre as posições conectadas
