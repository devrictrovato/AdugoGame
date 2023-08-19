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
        self.piece_size = 30
        self.offset = self.width // 8
        self.mesh = None
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
            if self.mesh is not None: # Renderizando os caminhos no tabuleiro
                for p1, p2 in self.mesh:
                    pygame.draw.line(self.screen, "white", p1, p2, 5)
            
            self.draw() # Renderizando as pecas

            if self.mesh is None: 
                self.mesh = self.lines()
                

            pygame.display.flip()

            self.clock.tick(60) # FPS

    def draw(self):
        # Criando a interface grafica do tabuleiro
        piece = None
        for x in range(0, len(self.board)):
            for y in range(0, len(self.board[0])):
                current = self.board[x, y]
                position = pygame.Vector2(
                    (self.screen.get_width() / 8) + self.offset * x, 
                    (self.screen.get_height() / 6) + self.offset * y
                )
                in_triangle = False
                # Jogador
                if isinstance(current, Jaguar):
                    if x == 6:
                        self.triangle(x, y, current, position, self.piece_size, "green")
                        in_triangle = True
                    else:
                        if self.is_select:
                            piece = pygame.draw.circle(self.screen, "darkgreen", position, self.piece_size)
                        else:
                            piece = pygame.draw.circle(self.screen, "green", position, self.piece_size)
                # Inimigos
                elif isinstance(current, Dog):
                    if x == 6:
                        self.triangle(x, y, current, position, self.piece_size, "red")
                        in_triangle = True
                    else:
                        piece = pygame.draw.circle(self.screen, "red", position, self.piece_size)
                # Livres
                elif isinstance(current, Piece):
                    if x == 6:
                        self.triangle(x, y, current, position, self.piece_size, "blue")
                        in_triangle = True
                    else:
                        piece = pygame.draw.circle(self.screen, "blue", position, self.piece_size)
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
        lines = []
        for x, piece in self.pieces:
            for y, connection in self.pieces:
                if connection in piece.connections.values():
                    lines.append((x.center, y.center))
        return lines

    def triangle(self, x, y, current, position, size, color):
        if x == 6 and y == 1:
            position = pygame.Vector2(position.x, position.y - self.offset)
            piece = pygame.draw.circle(self.screen, color, position, size)
        elif x == 6 and y == 2:
            position = pygame.Vector2(position.x, position.y)
            piece = pygame.draw.circle(self.screen, color, position, size)
        elif x == 6 and y == 3:
            position = pygame.Vector2(position.x, position.y + self.offset)
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