import random
import matplotlib.pyplot as plt


def count_neighbours_black(picture, n):
    if n == 8:
        n_max = 2
    if n == 16:
        n_max = 3
    neighbourhood = []
    for i in range(len(picture)):
        neighbourhood.append([])
        for j in range(len(picture)):
            neighbourhood[i].append(0)
    for i in range(len(picture)):
        neighbourhood.append([])
        for j in range(len(picture)):
            for k in range(i, i + n_max):
                if k >= 0 and k < len(picture):
                    for l in range(j, j + n_max):
                        if l >= 0 and l < len(picture):
                            if k != i or l != j:
                                if picture[k][l] == picture[i][j] and picture[k][l] == 1:
                                    neighbourhood[i][j] -= 1 / (abs(k - i) + abs(l - j))
                                    neighbourhood[k][l] -= 1 / (abs(k - i) + abs(l - j))
                                else:
                                    neighbourhood[i][j] += 1 / (abs(k - i) + abs(l - j))
                                    neighbourhood[k][l] += 1 / (abs(k - i) + abs(l - j))
    return neighbourhood


def generate_image(n, delta):
    black_points = n * n * delta
    white_points = n * n - black_points
    picture = []
    for i in range(0, n):
        picture.append([])
        for j in range(0, n):
            if black_points > 0 and white_points > 0:
                if random.uniform(0, 1) < delta:
                    picture[i].append(1)
                    black_points -= 1
                else:
                    picture[i].append(0)
                    white_points -= 1
            else:
                if black_points > 0:
                    picture[i].append(1)
                    black_points -= 1
                else:
                    picture[i].append(0)
                    white_points -= 1
    return picture


def count_neighbours_4(picture):
    neighbourhood = []
    for i in range(len(picture)):
        neighbourhood.append([])
        for j in range(len(picture)):
            neighbourhood[i].append(0)
    for i in range(len(picture)):
        neighbourhood.append([])
        for j in range(len(picture)):
            if i + 1 < len(picture) and picture[i][j] == picture[i + 1][j]:
                neighbourhood[i][j] += 1
                neighbourhood[i + 1][j] += 1
            else:
                if i + 1 < len(picture) and picture[i][j] != picture[i + 1][j]:
                    neighbourhood[i][j] -= 1
                    neighbourhood[i + 1][j] -= 1
            if j + 1 < len(picture) and picture[i][j] == picture[i][j + 1]:
                neighbourhood[i][j] += 1
                neighbourhood[i][j + 1] += 1
            else:
                if j + 1 < len(picture) and picture[i][j] != picture[i][j + 1]:
                    neighbourhood[i][j] -= 1
                    neighbourhood[i][j + 1] -= 1
    return neighbourhood


def count_neighbours(picture, n):
    if n == 8:
        n_max = 2
    if n == 16:
        n_max = 3
    neighbourhood = []
    for i in range(len(picture)):
        neighbourhood.append([])
        for j in range(len(picture)):
            neighbourhood[i].append(0)
    for i in range(len(picture)):
        neighbourhood.append([])
        for j in range(len(picture)):
            for k in range(i, i + n_max):
                if k >= 0 and k < len(picture):
                    for l in range(j, j + n_max):
                        if l >= 0 and l < len(picture):
                            if k != i or l != j:
                                if picture[k][l] == picture[i][j]:
                                    neighbourhood[i][j] += 1 / (abs(k - i) + abs(l - j))
                                    neighbourhood[k][l] += 1 / (abs(k - i) + abs(l - j))
                                else:
                                    neighbourhood[i][j] -= 1 / (abs(k - i) + abs(l - j))
                                    neighbourhood[k][l] -= 1 / (abs(k - i) + abs(l - j))
    return neighbourhood


def count_neighbours_4_black(picture):
    neighbourhood = []
    for i in range(len(picture)):
        neighbourhood.append([])
        for j in range(len(picture)):
            neighbourhood[i].append(0)

    for i in range(len(picture)):
        for j in range(len(picture)):
            if i + 1 < len(picture) and picture[i][j] == picture[i + 1][j] and picture[i][j] == 1:
                neighbourhood[i][j] -= 1
                neighbourhood[i + 1][j] -= 1
            else:
                if i + 1 < len(picture):
                    neighbourhood[i][j] += 1
                    neighbourhood[i + 1][j] += 1
            if j + 1 < len(picture) and picture[i][j] == picture[i][j + 1] and picture[i][j] == 1:
                neighbourhood[i][j] -= 1
                neighbourhood[i][j + 1] -= 1
            else:
                if j + 1 < len(picture):
                    neighbourhood[i][j] += 1
                    neighbourhood[i][j + 1] += 1

    return neighbourhood


def sum_energy(neighbourhood):
    energy = 0
    for i in range(len(neighbourhood)):
        for j in range(len(neighbourhood[i])):
            energy += neighbourhood[i][j]
    return energy


def swap(x, y, picture):
    tmp = picture[x[0]][x[1]]
    picture[x[0]][x[1]] = picture[y[0]][y[1]]
    picture[y[0]][y[1]] = tmp
    return


def simulated_annealing(picture):
    i = 0
    T = 100
    neighbourhood = count_neighbours(picture, 16)
    curr_neighbourhood = []
    energy = sum_energy(neighbourhood)
    curr_energy = 0
    energy_values = []
    energy_values.append(energy)
    delta = 0
    last_result = energy
    best = []
    best_ene = energy
    while T > 0 and i < 50000:
        x = [random.randint(0, len(picture) - 1), random.randint(0, len(picture) - 1)]
        y = [random.randint(0, len(picture) - 1), random.randint(0, len(picture) - 1)]
        swap(x, y, picture)
        curr_neighbourhood = count_neighbours(picture, 16)
        curr_energy = sum_energy(curr_neighbourhood)
        if curr_energy < energy:
                energy = curr_energy
                neighbourhood = curr_neighbourhood[:]
                if best_ene > energy:
                    best_ene = energy
                    best = picture
        else:
            if random.uniform(0, 1) < (2.72)**(((energy - curr_energy)/T)):
                energy = curr_energy
                neighbourhood = curr_neighbourhood[:]
            else:
                swap(x, y, picture)
        energy_values.append(energy)
        i += 1
        T *= 0.9999
        delta += abs(last_result - energy)
        last_result = energy
        if i%1000 == 0:
            if delta < 2:
                plt.plot(energy_values)
                plt.savefig('example.png')
                plt.close()
                return best
            else:
                delta = 0

    plt.plot(energy_values)
    plt.savefig('example.png')
    plt.close()
    return best


def main():
    picture = generate_image(10, 0.4)

    for i in range(len(picture)):
        print(picture[i])
    with open("example_sol.txt", "w") as f:
        for i in range(len(picture)):
            for j in range(len(picture)):
                f.write(str(picture[i][j]))
            f.write('\n')
    sol = simulated_annealing(picture)

    print()

    with open("example_sol.txt", "a") as f:
        f.write('\n')
        f.write('\n')
        f.write('Solution:\n')
        for i in range(len(sol)):
            for j in range(len(sol)):
                f.write(str(sol[i][j]))
            f.write('\n')

    for i in range(len(sol)):
        print(sol[i])

main()





























