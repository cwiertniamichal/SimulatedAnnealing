import City
import random
import matplotlib.pyplot as plt


def arbitrary_swap(world):
    city1 = random.randint(0, (len(world) - 1))
    city2 = random.randint(0, (len(world) - 1))
    while city1 == city2:
        city2 = random.randint(0, (len(world) - 1))
    return [city1, city2]


def consecutive_swap(world):
    city1 = random.randint(0, (len(world) - 2))
    city2 = city1 + 1
    return [city1, city2]


def swap(list, index1, index2):
    tmp = list[index1]
    list[index1] = list[index2]
    list[index2] = tmp


def count_distance(world):
    dist = 0
    for i in range(len(world) - 1):
        dist += world[i].distance(world[(i + 1) % (len(world) - 1)])
    return dist


def simulated_annealing(world):
    best_dist = count_distance(world)
    dist = count_distance(world)
    best = []
    last_result = dist
    delta = 0
    curr_dist = 0
    T = 200
    i = 0
    t = [T]
    y = []
    while T > 0 and i < 50000:
        cities = arbitrary_swap(world)
        city1 = cities[0]
        city2 = cities[1]
        swap(world, city1, city2)
        curr_dist = count_distance(world)
        if curr_dist < dist:
            y.append(curr_dist)
            dist = curr_dist
            if dist < best_dist:
                best_dist = dist
                best = world[:]
        else:
            if random.uniform(0,1) <  (2.72)**(((dist - curr_dist)/T)):
                dist = curr_dist
                y.append(dist)
            else:
                swap(world, city1, city2)
                y.append(dist)
        T *= 0.9999
        t.append(T)
        i += 1
        delta += abs(last_result - dist)
        last_result = dist
        if i%100 == 0:
            if delta < 5:
                plt.plot(t)
                plt.savefig('ene.png')
                plt.close()
                plt.plot(y)
                plt.savefig('example.png')
                plt.close()
                for j in range(len(best) - 1):
                    plt.scatter(best[j].x,best[j].y)
                   # plt.annotate(j, xy=(best[j].x, best[j].y))
                    plt.plot([best[j].x, best[j + 1].x], [best[j].y, best[j + 1].y])
                plt.scatter(best[len(best) - 1].x,best[len(best) - 1].y)
                #plt.annotate(len(best) - 1, xy=(best[len(best) - 1].x, best[len(best) - 1].y))
                plt.savefig('path_example.png')
                plt.close()
                return best
            else:
                delta = 0



    plt.plot(t)
    plt.savefig('ene.png')
    plt.close()
    plt.plot(y)
    plt.savefig('example.png')
    plt.close()
    for i in range(len(best) - 1):
        plt.scatter(best[i].x,best[i].y)
        #plt.annotate(i, xy=(best[i].x, best[i].y))
        plt.plot([best[i].x, best[i + 1].x], [best[i].y, best[i + 1].y])

    plt.scatter(best[len(best) - 1].x,best[len(best) - 1].y)
    #plt.annotate(len(best) - 1, xy=(best[len(best) - 1].x, best[len(best) - 1].y))
    plt.savefig('path_example.png')
    plt.close()
    return best


def generate_world(n):
    world = []
    for i in range(0, n):
        world.append(City.City(random.randint(0, 100), random.randint(0, 100), i))
    return world


def generate_world_normal(n):
    world = []
    for i in range(0, n):
        world.append(City.City(random.normalvariate(20, 10), random.normalvariate(20, 10), i)) #20 10 30 5 30 10 20 15
    return world


def generate_world_seperated(n):
    world = []
    for i in range(0, n):
        if i % 9 == 0:
            world.append(City.City(random.randint(0, 30), random.randint(0, 30), i))
        if i % 9 == 1:
                world.append(City.City(random.randint(0, 30), random.randint(50, 80), i))
        if i % 9 == 2:
            world.append(City.City(random.randint(0, 30), random.randint(100, 130), i))
        if i % 9 == 3:
            world.append(City.City(random.randint(50, 80), random.randint(0, 30), i))
        if i % 9 == 4:
            world.append(City.City(random.randint(50, 80), random.randint(50, 80), i))
        if i % 9 == 5:
            world.append(City.City(random.randint(50, 80), random.randint(100, 130), i))
        if i % 9 == 6:
            world.append(City.City(random.randint(100, 130), random.randint(0, 30), i))
        if i % 9 == 7:
            world.append(City.City(random.randint(100, 130), random.randint(50, 80), i))
        if i % 9 == 8:
            world.append(City.City(random.randint(100, 130), random.randint(100, 130), i))
    return world


def main():
    n = 50
    world = generate_world(n)
    best = simulated_annealing(world)
    print()

    sum = 0
    for i in range(0, n):
        sum += best[i].distance(best[(i + 1) % n])
    print(sum)


main()
