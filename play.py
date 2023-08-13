import math, random
from minimax import minimax

from dog import Dog
from jaguar import Jaguar

def play(board, dogs):
    # Escolhendo a peça disponivel para movimentar
    available = [dog for dog in dogs if dog.moves(Dog, Jaguar)]
    depth = math.log(len(available), 2)
    
    while depth % 1 != 0: # Margem de erro
        available.append(random.choice(available))
        depth = math.log(len(available), 2)

    select = minimax(0, 0, True, available, depth)
    
    # Escolhendo a melhor posicao para a peca escolhida
    moves = [board[m] for m in select.moves(Dog, Jaguar).keys()]
    depth = math.log(len(moves), 2)

    while depth % 1 != 0: # Margem de erro
        moves.append(random.choice(moves))
        depth = math.log(len(moves), 2)
    
    to_move = minimax(0, 0, True, moves, depth)

    select.swap(to_move) # Troca de pecas no tabuleiro