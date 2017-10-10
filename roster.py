def printMatrix(matrix):
    s = [[str(e) for e in row] for row in matrix]
    lens = [max(map(len, col)) for col in zip(*s)]
    fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
    table = [fmt.format(*row) for row in s]
    print('\n'.join(table))
    print('_______________')

def isAttacked(x,y,matrix,N):
        if 1 in matrix[x]:
            return True
        if 1 in transpose(matrix)[y]:
            return True
        return False


def isAttacked1(x, y, matrix, N):
    if 1 in matrix[x]:
        return True
    return False



def transpose(matrix):
    trn=[list(x) for x in zip(*matrix)]
    return trn



def roster(matrix,N):
    if N is 0:
        printMatrix(matrix)
        return True
    for i in range(N):
        for j in range(N):
            if isAttacked(i,j,matrix,N):
                continue
            matrix[i][j]=1
            if roster(matrix,N-1):
                return True
            matrix[i][j] = 0

    return False

matrix = [[0 for x in range(4)] for y in range(4)]

roster(matrix,4)
