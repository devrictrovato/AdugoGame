import pygame

from board import create
from jaguar import Jaguar
from dog import Dog
from piece import Piece
from play import play

class Game:
    def __init__(self, width, height, board) -> None:
        self.width, self.height = width, height
        self.board, self.jaguar, self.dogs = board
        self.pieces = list()
        self.is_select = False
        self.enemy_turn = False
        pygame.init()
        self.screen = pygame.display.set_mode(
            (self.width, self.height)
        )
        self.clock = pygame.time.Clock()
        self.running = True

    def run(self):
        while self.running:
            # Eventos para monitorar
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    self.collisions(pos)

            self.screen.fill("black") # Cor de fundo padrao

            # Atualizacao para cada acao
            if self.enemy_turn:
                play(self.board, self.dogs)
                self.enemy_turn = False

            lose = [isinstance(self.board[i], Dog) for i in self.jaguar.connections.keys()]
            if self.jaguar.score > 4:
                print('You win !')
            elif all(lose):
                print('Game Over !')

            # Renderizando a interface do jogador
            self.lines()
            self.draw(self.board)

            pygame.display.flip()

            self.clock.tick(60) # FPS

    def draw(self, board):
        # Criando a interface grafica do tabuleiro
        piece_size = 30
        offset = self.width // 8
        piece = None
        for x in range(0, len(board)):
            for y in range(0, len(board[0])):
                current = board[x, y]
                position = pygame.Vector2(
                    (self.screen.get_width() / 8) + offset * x, 
                    (self.screen.get_height() / 6) + offset * y
                )
                in_triangle = False
                # Jogador
                if isinstance(current, Jaguar):
                    if x == 6:
                        self.triangle(x, y, current, position, piece_size, offset, "green")
                        in_triangle = True
                    else:
                        if self.is_select:
                            piece = pygame.draw.circle(self.screen, "darkgreen", position, piece_size)
                        else:
                            piece = pygame.draw.circle(self.screen, "green", position, piece_size)
                # Inimigos
                elif isinstance(current, Dog):
                    if x == 6:
                        self.triangle(x, y, current, position, piece_size, offset, "red")
                        in_triangle = True
                    else:
                        piece = pygame.draw.circle(self.screen, "red", position, piece_size)
                # Livres
                elif isinstance(current, Piece):
                    if x == 6:
                        self.triangle(x, y, current, position, piece_size, offset, "blue")
                        in_triangle = True
                    else:
                        piece = pygame.draw.circle(self.screen, "blue", position, piece_size)
                if not in_triangle:
                    self.points(piece, current)
    
    def collisions(self, position):
        for select, piece in self.pieces:
            if select.collidepoint(position):
                if isinstance(piece, Jaguar):
                    self.is_select = not self.is_select
                elif isinstance(piece, Dog):
                    continue
                elif isinstance(piece, Piece):
                    if self.is_select:
                        x, y = piece.pos
                        is_moved = self.jaguar.move(x, y)
                        self.is_select = False
                        if not self.is_select and is_moved:
                            self.enemy_turn = True
        self.pieces.clear()

    def points(self, piece, current):
        if (piece, current) not in self.pieces:
            if isinstance(current, Piece):
                self.pieces.append((piece, current))

    def lines(self):
        # for x, piece in self.pieces:
        #     for y, connection in self.pieces:
        #         if connection in piece.connections.values():
        #             pygame.draw.line(self.screen, "white", x.center, y.center, 5)
        standart = pygame.image.load('.\\imgs\\mesh.png').convert()
        self.screen.blit(standart, (63, 65))

    def triangle(self, x, y, current, position, size, offset, color):
        if x == 6 and y == 1:
            position = pygame.Vector2(position.x, position.y - offset)
            piece = pygame.draw.circle(self.screen, color, position, size)
        elif x == 6 and y == 2:
            position = pygame.Vector2(position.x, position.y)
            piece = pygame.draw.circle(self.screen, color, position, size)
        elif x == 6 and y == 3:
            position = pygame.Vector2(position.x, position.y + offset)
            piece = pygame.draw.circle(self.screen, color, position, size)
        if self.board[x, y] == self.jaguar:
            if self.is_select:
                piece = pygame.draw.circle(self.screen, "darkgreen", position, size)
            else:
                piece = pygame.draw.circle(self.screen, "green", position, size)
        self.points(piece, current)
        

if __name__ == '__main__':
    game = Game(800, 600, create())
    game.run()
    pygame.quit()