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
        self.miss = False
        self.win = False
        self.lose = False
        
        self.offset = self.width // 8
        self.piece_size = self.offset // 4

        self.mesh = None
        self.colors = {
            'jaguar': '#FCBA12',
            'dog': '#9E8E00',
            'free': '#B9B36E',
            'connection': '#E08D2E',
            'select': '#FB8604',
            'bg': '#6D6412',
            'title': '#F0BC00',
            'invalid': '#FFECBD',
            'win': '#FFE70A',
            'lose': '#C1EF1A',
        }

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

            self.screen.fill(self.colors['bg']) # Cor de fundo padrao

            # Atualizacao para cada acao
            if self.enemy_turn:
                play(self.board, self.jaguar, self.dogs)
                self.enemy_turn = False

            lose = [isinstance(self.board[i], Dog) for i in self.jaguar.connections.keys()]
            if self.jaguar.score > 4:
                self.win = True
            elif all(lose):
                self.lose = True

            # Renderizando a interface do jogador
            self.texts()

            if self.mesh is not None: # Renderizando os caminhos no tabuleiro
                for p1, p2 in self.mesh:
                    pygame.draw.line(self.screen, self.colors['connection'], p1, p2, 5)
            
            self.draw() # Renderizando as pecas

            if self.mesh is None: 
                self.mesh = self.lines()

            pygame.display.flip()

            self.clock.tick(60) # FPS

    def texts(self):
        self.text('Adugo Game', self.colors['title'],  self.piece_size * 2, self.width // 3, self.height // 10 )
        if self.win:
            self.text('Voce Venceu !', self.colors['win'], self.piece_size, self.width - (self.offset * 2), self.height // 10)
        elif self.lose:
            self.text('Voce Perdeu !', self.colors['lose'], self.piece_size, self.width - (self.offset * 2), self.height // 10)
        elif self.miss:
            self.text('Movimento invalido', self.colors['invalid'], self.piece_size, self.width - (self.offset * 2), self.height // 10)

    def text(self, phrase, color, size, x, y):
        font = pygame.font.Font('freesansbold.ttf', size)
        text = font.render(phrase, True, color, self.colors['bg'])
        rect = text.get_rect()
        rect.center = (x, y)
        self.screen.blit(text, rect)
        return True

    def draw(self):
        # Criando a interface grafica do tabuleiro
        piece = None
        for x in range(0, len(self.board)):
            for y in range(0, len(self.board[0])):
                current = self.board[x, y]
                position = pygame.Vector2(
                    (self.screen.get_width() / 8) + self.offset * x, 
                    (self.screen.get_height() / 6) + self.offset * y + (self.piece_size * 2)
                )
                in_triangle = False
                # Jogador
                if isinstance(current, Jaguar):
                    if x == 6:
                        self.triangle(x, y, current, position, self.piece_size, self.colors['jaguar'])
                        in_triangle = True
                    else:
                        if self.is_select:
                            piece = pygame.draw.circle(self.screen, self.colors['select'], position, self.piece_size)
                        else:
                            piece = pygame.draw.circle(self.screen, self.colors['jaguar'], position, self.piece_size)
                # Inimigos
                elif isinstance(current, Dog):
                    if x == 6:
                        self.triangle(x, y, current, position, self.piece_size, self.colors['dog'])
                        in_triangle = True
                    else:
                        piece = pygame.draw.circle(self.screen,self.colors['dog'], position, self.piece_size)
                # Livres
                elif isinstance(current, Piece):
                    if x == 6:
                        self.triangle(x, y, current, position, self.piece_size, self.colors['free'])
                        in_triangle = True
                    else:
                        piece = pygame.draw.circle(self.screen, self.colors['free'], position, self.piece_size)
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
                        is_moved, removed = self.jaguar.move(x, y)
                        if removed is not None:
                            self.dogs.remove(removed)
                            print(len(self.dogs))
                        self.is_select = False
                        if not self.is_select and is_moved:
                            self.enemy_turn = True
                            self.miss = False
                        elif not is_moved:
                            self.miss = True
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
                piece = pygame.draw.circle(self.screen, self.colors['select'], position, size)
            else:
                piece = pygame.draw.circle(self.screen, self.colors['jaguar'], position, size)
        self.points(piece, current)
        

if __name__ == '__main__':
    game = Game(800, 600, create())
    game.run()
    pygame.quit()