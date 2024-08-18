import pygame
import sys
from board import Board
from minmax import get_best_move

# Inicializa o Pygame
pygame.init()

# Dimensões da tela
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 700  # Ajustado para 7 linhas
CELL_SIZE = SCREEN_WIDTH // 5  # Tamanho de cada célula baseado no número de colunas

# Cores (Paleta baseada em tons de amarelo)
YELLOW = (239, 192, 80)  # Cor da onça
DARK_YELLOW = (253, 172, 83)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
TANGO = (221, 65, 36)   # Cor dos cachorros
HIGHLIGHT_COLOR = (154, 139, 79)  # Cor de destaque mais clara
WIN = (0, 161, 112)  # Cor para vitória
LOSE = (210, 56, 108)  # Cor para derrota

# Dicionário de cores para facilitar o acesso
colors = {
    'YELLOW': YELLOW,
    'DARK_YELLOW': DARK_YELLOW,
    'WHITE': WHITE,
    'BLACK': BLACK,
    'TANGO': TANGO,
    'HIGHLIGHT': HIGHLIGHT_COLOR,
    'WIN': WIN,
    'LOSE': LOSE,
}

# Cria a tela do jogo
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Adugo Game")

# Função para desenhar o placar
def draw_score(screen, score):
    font = pygame.font.Font(None, 36)  # Fonte para o texto
    text = font.render(f"Points: {score}", True, colors['HIGHLIGHT'])  # Renderiza o texto do placar
    screen.blit(text, (10, SCREEN_HEIGHT - 40))  # Desenha o placar no canto inferior esquerdo

# Função para desenhar a mensagem de vitória/derrota
def draw_victory_message(screen, message):
    font = pygame.font.Font(None, 36)  # Fonte para o texto
    text = font.render(message, True, colors['WIN' if 'Jaguar' in message else 'LOSE'])
    screen.blit(text, (SCREEN_WIDTH - 200, 20))  # Desenha a mensagem no canto superior direito

# Função de resetar o jogo
def reset_game():
    global board, selected_piece, jaguar_turn, captured_dogs, game_over, victory_message
    board = Board()  # Reinicia o tabuleiro
    selected_piece = None  # Nenhuma peça está selecionada
    jaguar_turn = True  # Reinicia para a vez da onça
    captured_dogs = 0  # Zera o contador de cachorros capturados
    game_over = False  # Reseta o estado de game over
    victory_message = ""  # Limpa a mensagem de vitória/derrota

# Função principal do jogo
def main():
    global selected_piece, jaguar_turn, captured_dogs, game_over, victory_message
    
    running = True  # Variável de controle do loop principal
    reset_game()  # Inicializa o estado do jogo

    # Loop principal do jogo
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Fecha o jogo se o jogador clicar para sair
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:  # Detecta cliques do mouse quando o jogo está ativo
                pos = pygame.mouse.get_pos()  # Obtém a posição do clique
                col = pos[0] // CELL_SIZE  # Converte a posição x em coluna
                row = pos[1] // CELL_SIZE  # Converte a posição y em linha
                
                # Verifica se é a vez da onça jogar
                if jaguar_turn:
                    if selected_piece:  # Se uma peça já estiver selecionada
                        # Verifica se o movimento é válido e aplica-o
                        if (row, col) in board.movement.connections[selected_piece]:
                            if board.grid[row][col] == ' ':  # Movimento para uma célula vazia
                                board.move_jaguar((row, col))  # Move a onça
                                jaguar_turn = False  # Alterna para a vez dos cachorros
                            elif board.grid[row][col] == 'D':  # Captura um cachorro
                                if board.movement.capture_dog(selected_piece, (row, col)):
                                    captured_dogs += 1  # Incrementa o contador de cachorros capturados
                                    jaguar_turn = False  # Alterna para a vez dos cachorros
                        selected_piece = None  # Reseta a peça selecionada
                    elif (row, col) == board.jaguar.position:  # Se a posição clicada for a da onça
                        selected_piece = (row, col)  # Seleciona a onça
                        
            elif event.type == pygame.KEYDOWN and game_over:  # Detecta teclas pressionadas após game over
                if event.key == pygame.K_SPACE:  # Reinicia o jogo ao pressionar a barra de espaço
                    reset_game()  # Chama a função de reset

        # Se for a vez dos cachorros jogarem e o jogo ainda não terminou
        if not jaguar_turn and not game_over:
            best_move = get_best_move(board)  # Obtém o melhor movimento para os cachorros usando o Minimax
            if best_move:  # Se houver um movimento válido
                old_pos, new_pos = best_move  # Divide o movimento em posição antiga e nova
                dog = next(d for d in board.dogs if d.position == old_pos)  # Identifica o cachorro a ser movido
                board.move_dog(dog, new_pos)  # Move o cachorro para a nova posição
            jaguar_turn = True  # Alterna para a vez da onça

        # Verifica as condições de vitória
        if captured_dogs >= 6:  # Se a onça capturou 6 cachorros
            victory_message = "Jaguar Wins!"  # Mensagem de vitória da onça
            game_over = True  # Marca o jogo como terminado
        elif not any(board.movement.is_valid_move(board.jaguar.position, move) for move in board.movement.connections[board.jaguar.position]):
            # Se a onça não puder se mover
            victory_message = "Dogs Win!"  # Mensagem de vitória dos cachorros
            game_over = True  # Marca o jogo como terminado
        
        screen.fill(colors['WHITE'])  # Preenche o fundo da tela com preto

        # Desenha as linhas do tabuleiro e as peças
        board.draw_lines(screen, CELL_SIZE, colors)
        board.draw_board(screen, CELL_SIZE, colors)

        # Desenha o placar e a mensagem de vitória/derrota, se houver
        draw_score(screen, captured_dogs)
        if game_over:
            draw_victory_message(screen, victory_message)
            # Exibe instruções para reiniciar o jogo
            font = pygame.font.Font(None, 36)
            restart_text = font.render("Press SPACE to Restart", True, colors['LOSE'])
            screen.blit(restart_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))

        # Destaque para a peça selecionada
        if selected_piece:
            row, col = selected_piece
            # Desenha um círculo em torno da peça selecionada
            pygame.draw.circle(screen, colors['HIGHLIGHT'], (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)

        pygame.display.flip()  # Atualiza a tela

    # Encerra o Pygame e fecha o jogo
    pygame.quit()
    sys.exit()

# Inicia o jogo se este script for executado diretamente
if __name__ == "__main__":
    main()
