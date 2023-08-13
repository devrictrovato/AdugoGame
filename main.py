# Importando as bibliotecas
import numpy as np

from piece import Piece
from dog import Dog
from jaguar import Jaguar

from play import play

def main():
    board = np.zeros((7, 5), dtype=Piece) # Inicializando o tabuleiro
    
    dogs = [] # Armazenamento dos inimigos

    dogs.append(Dog(board, (0, 0), (
        (0, 1), (1, 0), (1, 1),
    )))
    dogs.append(Dog(board, (0, 1), (
        (0, 0), (0, 2), (1, 1),
    )))
    dogs.append(Dog(board, (0, 2), (
        (0, 1), (0, 3),
        (1, 1), (1, 2), (1, 3),
    )))
    dogs.append(Dog(board, (0, 3), (
        (0, 2), (0, 4), (1, 3),
    )))
    dogs.append(Dog(board, (0, 4), (
        (0, 3), (1, 3), (1, 4),
    )))

    dogs.append(Dog(board, (1, 0), (
        (0, 0), (1, 1), (2, 0),
    )))
    dogs.append(Dog(board, (1, 1), (
        (0, 0), (0, 1), (0, 2),
        (1, 0), (1, 2),
        (2, 0), (2, 1), (2, 2),
    )))
    dogs.append(Dog(board, (1, 2), (
        (0, 2), (1, 1), (1, 3), (2, 2),
    )))
    dogs.append(Dog(board, (1, 3), (
        (0, 2), (0, 3), (0, 4),
        (1, 2), (1, 4),
        (2, 2), (2, 3), (2, 4),
    )))
    dogs.append(Dog(board, (1, 4), (
        (0, 4), (1, 3), (2, 4)
    )))

    dogs.append(Dog(board, (2, 0), (
        (1, 0), (1, 1),
        (2, 1),
        (3, 0), (3, 1),
    )))
    dogs.append(Dog(board, (2, 1), (
        (2, 0), (2, 2), (1, 1), (3, 1),
    )))

    jaguar = Jaguar(board, (2, 2), ( # Referencia do jogador
        (1, 1), (1, 2), (1, 3),
        (2, 1), (2, 3),
        (3, 1), (3, 2), (3, 3),
    ))

    dogs.append(Dog(board, (2, 3), (
        (1, 3), (2, 2), (2, 4), (3, 3),
    )))
    dogs.append(Dog(board, (2, 4), (
        (1, 3), (1, 4),
        (2, 3),
        (3, 3), (3, 4),
    )))

    Piece(board, (3, 0), (
        (2, 0), (3, 1), (4, 0)
    ))
    Piece(board, (3, 1), (
        (2, 0), (2, 1), (2, 2),
        (3, 0), (3, 2),
        (4, 0), (4, 1), (4, 2),
    ))
    Piece(board, (3, 2), (
        (2, 2), (3, 1), (3, 3), (4, 2)
    ))
    Piece(board, (3, 3), (
        (2, 2), (2, 3), (2, 4),
        (3, 2), (3, 4),
        (4, 2), (4, 3), (4, 4),
    ))
    Piece(board, (3, 4), (
        (2, 4), (3, 3), (4, 4),
    ))

    Piece(board, (4, 0), (
        (3, 0), (3, 1), (4, 1),
    ))
    Piece(board, (4, 1), (
        (3, 1), (4, 0), (4, 2)
    ))
    Piece(board, (4, 2), (
        (3, 1), (3, 2), (3, 3), 
        (4, 1), (4, 3),
        (5, 1), (5, 2), (5, 3)
    ))
    Piece(board, (4, 3), (
        (3, 3), (4, 2), (4, 4),
    ))
    Piece(board, (4, 4), (
        (3, 3), (4, 3), (3, 4)
    ))

    Piece(board, (5, 1), (
        (4, 2), (5, 2), (6, 1),
    ))
    Piece(board, (5, 2), (
        (4, 2), (5, 1), (5, 3), (6, 2),
    ))
    Piece(board, (5, 3), (
        (4, 2), (5, 2), (6, 3),
    ))

    Piece(board, (6, 1), (
        (5, 1), (6, 2),
    ))
    Piece(board, (6, 2), (
        (5, 2), (6, 1), (6, 3),
    ))
    Piece(board, (6, 3), (
        (5, 3), (6, 2),
    ))

    print(board) # Mostrando o tabuleiro inicial
    for _ in range(0, 10): # Simulando 10 jogadas dos inimigos
        play(board, dogs)
    print(board) # Mostrando o tabuleiro final
    
if __name__ == '__main__': # Execução no módulo
    main()