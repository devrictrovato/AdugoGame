# Importando as bibliotecas
import numpy as np

def main():
    board = np.zeros((9, 7)) # Inicializando o tabuleiro
    board[1:-5, 1:-1] = -1 # Inimigos
    board[3, 3] = 1 # Jogador
    board[0] = board[:,0] = board[:,-1] = board[-1:] = None # Bordas de ajuste
    board[-3,-2] = board[-2,-3] = board[-2,2] = board[-3, 1] = None # Triângulo abaixo
    print(board) # Mostrando o tabuleiro inicial

if __name__ == '__main__': # Execução no módulo
    main()