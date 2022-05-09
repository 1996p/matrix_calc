"""LOGIC is HERE"""

A = [[1, 2],
     [-1, -2],
     [-3, -4],
     [-5, -6]
     ]

B = [[3, 4],
     [5, 6],
     [7, 8],
     [9, 10]
     ]



def matrix_multiplier(matrix_a, matrix_b):
    result = []
    if len(matrix_a) == 1 and len(matrix_a[0]) == 1:
        print(7)
        for n in range(0, len(matrix_b)):
            list_of_s = []
            for i in matrix_b[n]:
                s = matrix_a[0][0] * i
                list_of_s.append(s)
            result.append(list_of_s)
    else:
        for i in range(0, len(matrix_a)):
            list_of_s = []
            for n in range(0, len(matrix_b)):
                s = 0
                for e in range(0, len(matrix_a[i])):
                    s += matrix_a[i][e] * matrix_b[n][e]
                list_of_s.append(s)
            result.append(list_of_s)
    return result


def matrix_sum(matrix_a, matrix_b):
    result = []
    for i in range(0, len(matrix_a)):
        list_of_s = []
        for n in range(0, len(matrix_b[1])):
            list_of_s.append(matrix_a[i][n] + matrix_b[i][n])
        result.append(list_of_s)
    return result
if __name__ == '__main__':
    matrix_sum(A, B)
