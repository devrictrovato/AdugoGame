# Algoritmo Min-Max
def minimax (current, initial, end, heuristics, target):
 
    if (current == target):
        return heuristics[initial]
     
    if (end):
        return max(minimax(current + 1, initial * 2,
                           False, heuristics, target),
                   minimax(current + 1, initial * 2 + 1,
                           False, heuristics, target))
     
    else:
        return min(minimax(current + 1, initial * 2,
                           True, heuristics, target),
                   minimax(current + 1, initial * 2 + 1,
                           True, heuristics, target))