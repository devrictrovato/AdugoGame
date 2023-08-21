from math import log
from random import randint
from minimax import minimax

from dog import Dog
from jaguar import Jaguar

def play(board, jaguar, dogs):
    # Escolhendo a peça disponivel para movimentar
    available = [dog for dog in dogs if dog.moves(Dog, Jaguar)]
    depth = log(len(available), 2)
    
    while depth % 1 != 0: # Margem de erro
        del available[randint(0, len(available) - 1)]
        depth = log(len(available), 2)

    select = minimax(0, 0, True, available, depth)
    
    # Escolhendo a melhor posicao para a peca escolhida
    moves = [board[m] for m in select.moves(Dog, Jaguar).keys()]
    depth = log(len(moves), 2)

    while depth % 1 != 0: # Margem de erro
        del moves[randint(0, len(moves) - 1)]
        depth = log(len(moves), 2)
    
    to_move = minimax(0, 0, True, moves, depth)

    if to_move.pos != jaguar.pos:
        select.swap(to_move) # Troca de pecas no tabuleiro
    else:
        play(board, jaguar, dogs)