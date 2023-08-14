import math

distance = lambda pointA, pointB: math.dist(pointA, pointB)

middle = lambda posA, posB: (
    int(((posA[0] + posB[0]) / 2)),
    int(((posA[1] + posB[1]) / 2)),
)