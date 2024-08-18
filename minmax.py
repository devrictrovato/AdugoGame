import math

def evaluate_board(board):
    # Função de avaliação heurística para o tabuleiro.
    # O objetivo é calcular um valor numérico que represente a "vantagem" do jogador atual.
    
    jaguar_pos = board.jaguar.position  # Posição atual da onça no tabuleiro
    dog_count = len(board.dogs)  # Número total de cachorros restantes
    
    # Ameaça da onça: Aumenta o valor se os cachorros estiverem próximos da onça (mais ameaçados).
    jaguar_threat_score = 0
    for dog in board.dogs:
        # Calcula a distância entre a onça e o cachorro
        distance = abs(dog.position[0] - jaguar_pos[0]) + abs(dog.position[1] - jaguar_pos[1])
        # Aumenta a pontuação da ameaça da onça se o cachorro estiver próximo
        if distance == 1:  # Cachorro adjacente é uma ameaça direta
            jaguar_threat_score += 10
        elif distance == 2:  # Cachorro a dois espaços de distância é uma ameaça potencial
            jaguar_threat_score += 5

    # Segurança dos cachorros: Diminui a pontuação se os cachorros estiverem em posições onde podem ser capturados.
    dog_safety_score = 0
    for dog in board.dogs:
        # Verifica as conexões da posição do cachorro
        for connection in board.movement.connections[dog.position]:
            # Se a onça puder se mover para uma dessas conexões, o cachorro está em perigo
            if board.movement.is_valid_move(jaguar_pos, connection):
                dog_safety_score -= 20

    # Controle central: Incentiva os cachorros a se posicionarem em posições centrais no tabuleiro.
    central_positions = [(2, 2), (3, 2), (4, 2)]  # Posições centrais preferidas
    central_control_score = sum([10 for dog in board.dogs if dog.position in central_positions])

    # Mobilidade da onça: Penaliza estados onde a onça tem muitos movimentos válidos.
    jaguar_moves = len([move for move in board.movement.connections[jaguar_pos]
                        if board.movement.is_valid_move(jaguar_pos, move)])
    jaguar_mobility_penalty = jaguar_moves * 5  # Penaliza a mobilidade da onça

    # Avaliação total: Pontuação maior favorece os cachorros, pontuação menor favorece a onça.
    return (dog_count * 100 + jaguar_threat_score + central_control_score +
            dog_safety_score - jaguar_mobility_penalty)

def get_all_possible_moves(board):
    # Retorna uma lista de todos os movimentos possíveis para os cachorros.
    moves = []
    for dog in board.dogs:
        current_pos = dog.position  # Posição atual do cachorro
        # Para cada conexão da posição atual, verifica se o movimento é válido
        for new_pos in board.movement.connections[current_pos]:
            if board.movement.is_valid_move(current_pos, new_pos):
                moves.append((current_pos, new_pos))  # Adiciona o movimento à lista
    return moves

def minimax(board, depth, maximizing_player):
    # Algoritmo Minimax: Explora as possíveis jogadas até uma certa profundidade.
    
    # Critério de parada: Profundidade atingida ou não há mais cachorros no tabuleiro.
    if depth == 0 or not board.dogs:
        return evaluate_board(board), None  # Avalia o tabuleiro e não retorna nenhum movimento
    
    if maximizing_player:
        # O jogador maximizador (cachorros) tenta maximizar a pontuação.
        max_eval = -math.inf  # Inicia com o pior valor possível
        best_move = None  # Inicializa o melhor movimento
        for move in get_all_possible_moves(board):
            # Aplica o movimento
            dog = next(d for d in board.dogs if d.position == move[0])
            original_pos = dog.position
            board.move_dog(dog, move[1])

            # Recursivamente avalia esse movimento
            eval, _ = minimax(board, depth - 1, False)

            # Desfaz o movimento
            dog.position = original_pos
            board.update_grid()

            # Atualiza a melhor avaliação e movimento
            if eval > max_eval:
                max_eval = eval
                best_move = move
        return max_eval, best_move
    else:
        # O jogador minimizador (onça) tenta minimizar a pontuação.
        min_eval = math.inf  # Inicia com o melhor valor possível
        best_move = None  # Inicializa o melhor movimento
        jaguar_pos = board.jaguar.position
        # Para cada posição conectada à posição atual da onça
        for new_pos in board.movement.connections[jaguar_pos]:
            if board.movement.is_valid_move(jaguar_pos, new_pos):
                # Move a onça
                board.move_jaguar(new_pos)

                # Recursivamente avalia esse movimento
                eval, _ = minimax(board, depth - 1, True)

                # Desfaz o movimento
                board.jaguar.position = jaguar_pos
                board.update_grid()

                # Atualiza a menor avaliação e o melhor movimento
                if eval < min_eval:
                    min_eval = eval
                    best_move = new_pos
        return min_eval, best_move

def get_best_move(board, depth=3):
    # Retorna o melhor movimento encontrado pelo Minimax com uma profundidade definida
    _, best_move = minimax(board, depth, True)
    return best_move
