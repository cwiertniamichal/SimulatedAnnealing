import random
import matplotlib.pyplot as plt
import math
import decimal


def swap(board, number1, number2):
    tmp = board[number1[0]][number1[1]]
    board[number1[0]][number1[1]] = board[number2[0]][number2[1]]
    board[number2[0]][number2[1]] = tmp
    return


def count_repeats(board, wrong_elements):
    repeats = 0
    unique = 0
    for i in range(len(board)):
        numbers = {'1':0, '2':0, '3':0, '4':0, '5':0, '6':0, '7':0, '8':0, '9':0}
        for j in range(len(board[i])):
            if numbers[str(board[i][j])] > 0:
                repeats += 1
                numbers[str(board[i][j])] += 1
                wrong_elements.append([i, j])
            else:
                numbers[str(board[i][j])] = 1

        for key in numbers.keys():
            if numbers[key] == 1:
                unique += 1

    for i in range(len(board[0])):
        numbers = {'1':0, '2':0, '3':0, '4':0, '5':0, '6':0, '7':0, '8':0, '9':0}
        for j in range(len(board)):
            if numbers[str(board[j][i])] > 0:
                repeats += 1
                numbers[str(board[j][i])] += 1
                wrong_elements.append([j, i])
            else:
                numbers[str(board[j][i])] = 1
        for key in numbers.keys():
            if numbers[key] == 1:
                unique += 1
    for i in range(1, 4):
        for j in range(1, 4):
            numbers = {'1':0, '2':0, '3':0, '4':0, '5':0, '6':0, '7':0, '8':0, '9':0}
            for i1 in range((i - 1)*3, i*3):
                for j1 in range((j - 1)*3, j*3):
                    if numbers[str(board[j1][i1])] > 0:
                        repeats += 1
                        numbers[str(board[j1][i1])] += 1
                        wrong_elements.append([i1, j1])
                    else:
                        numbers[str(board[j1][i1])] = 1
            for key in numbers.keys():
                if numbers[key] == 1:
                    unique += 1
    return 243 - unique


def fill_random(board):
    for i in range(1, 4):
        for j in range(1, 4):
            numbers = {'1':0, '2':0, '3':0, '4':0, '5':0, '6':0, '7':0, '8':0, '9':0}
            for i1 in range((i - 1)*3, i*3):
                for j1 in range((j - 1)*3, j*3):
                    if board[i1][j1] != ' ':
                        numbers[str(board[i1][j1])] = 1
            for i1 in range((i - 1)*3, i*3):
                for j1 in range((j - 1)*3, j*3):
                    if board[i1][j1] == ' ':
                        k = 1
                        while numbers[str(k)] != 0:
                            k += 1
                        board[i1][j1] = str(k)
                        numbers[str(k)] = 1


def simulated_annealing(board, start_fields):
    start_board = board[:]
    y = []
    i = 0
    T = 0.9
    delta = 0
    wrong_elements = []
    repeats = count_repeats(board, wrong_elements)
    y.append(repeats)
    last_result = repeats
    repeats_curr = 0
    while repeats > 0 and  T > 0:
        number1 = [random.randint(0, len(board) - 1), random.randint(0, len(board) - 1)]
        while number1 in start_fields:
            number1 = [random.randint(0, len(board) - 1), random.randint(0, len(board) - 1)]
        number2 = [random.randint(3*(int(number1[0]/3)), 3*(int(number1[0]/3)) + 2), random.randint(3*(int(number1[1]/3)), 3*(int(number1[1]/3)) + 2)]
        while number2 in start_fields or board[number2[0]][number2[1]] == board[number1[0]][number1[1]]:
            number2 = [random.randint(3*(int(number1[0]/3)), 3*(int(number1[0]/3)) + 2), random.randint(3*(int(number1[1]/3)), 3*(int(number1[1]/3)) + 2)]

        swap(board, number1, number2)
        repeats_curr = count_repeats(board, wrong_elements)

        if repeats_curr < repeats:
            repeats = repeats_curr
            y.append(repeats)
        else:
            if random.uniform(0,1) <  decimal.Decimal((2.72)**(((repeats - repeats_curr))/T)):
                repeats = repeats_curr
                y.append(repeats)
            else:
                swap(board, number1, number2)
                y.append(repeats)

        i += 1
        T *= 0.99999
        delta += abs(last_result - repeats)
        last_result = repeats
        if i%1000 == 0:
            if delta < 1:
                simulated_annealing(start_board, start_fields)
            else:
                delta = 0

    return i


def load_board():
    board = []
    numbers = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0, '8': 0, '9': 0}
    empty_fields = []
    start_fields = []
    with open('sudoku.txt', 'r') as f:
        for line in f.readlines():
            line = line.split()
            board.append(line)
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 'x':
                board[i][j] = ' '
                empty_fields.append([i, j])
            else:
                numbers[board[i][j]] += 1
                start_fields.append([i, j])
    return [board, start_fields]


def main():
    loaded = load_board()
    board = loaded[0]
    start_fields = loaded[1]

    fill_random(board)

    print(simulated_annealing(board, start_fields))

    for i in range(len(board)):
        print(board[i])


main()
