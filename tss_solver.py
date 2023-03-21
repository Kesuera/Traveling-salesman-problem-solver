# Author: Samuel Hetteš, ID: 110968
# Subject: Artificial Intelligence
# Assignment: Travelling Salesman Problem Solver using Simulated Annealing
# IDE: PyCharm 2021.2.3
# Programming language: Python 3.9
# Date: 14.11.2021

import random  # generating random numbers
import math  # calculating distance
import matplotlib.pyplot as plt  # plotting results
from timeit import default_timer as timer  # measuring time


# city class
class City:
    # constructor, each city has its x, y coordinate and a name
    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.name = name

    # returns the coordinates as a tuple
    def coords(self):
        return self.x, self.y

    # returns the randomly generated cities
    @staticmethod
    def generate_cities(height, width, count, random_bool):
        cities = []
        for i in range(count):  # based on count, generate cities
            if random_bool == 1:
                city = City(random.randrange(width + 1), random.randrange(height + 1), i + 1)  # generate city with random coordinates
            else:
                print("City", i + 1, "(x y):", end=' ')
                x, y = map(int, input().split())
                city = City(x, y, i + 1)
            cities.append(city)
        return cities

    # plot the cities
    @staticmethod
    def plot_cities(cities):
        for i in range(len(cities)):
            x_coord, y_coord = cities[i].coords()
            plt.plot(x_coord, y_coord, 'ro')
            plt.annotate(cities[i].name, (x_coord, y_coord))
        plt.xlabel("Width")
        plt.ylabel("Height")
        plt.title("Cities")
        plt.show()


# solver class
class Solver:
    # constructor, solver has to know the initial route, initial temperature, minimal temperature, cooling factor and the number of neighbors
    def __init__(self, init_route, initial_temp, minimal_temp, factor):
        self.init_route = init_route
        self.init_temp = initial_temp
        self.min_temp = minimal_temp
        self.cooling_factor = factor
        self.neighbors = int(len(init_route.cities) * (len(init_route.cities) - 1) / 2)

    # returns True of False if the new route is accepted
    @staticmethod
    def accept(current_route, neighbor_route, temp):
        diff = current_route.distance - neighbor_route.distance
        rand_num = random.uniform(0, 1)
        probability = math.exp(diff/temp)  # boltzmann distribution equation
        # if the distance is better or the generated number is from the range of probability return True
        if (diff > 0) or (probability >= rand_num):
            return True
        else:
            return False

    # return the shortest route (simulated annealing)
    def solve(self, animation):
        start_time = timer()  # starting time
        best_route = self.init_route
        current_route = best_route
        T = self.init_temp
        distances = []  # for saving the distances so we can plot the process
        cities_count = len(current_route.cities)
        while T > self.min_temp:  # while the minimal temperature is not reached
            if animation == 1:
                current_route.plot_route()
            index_from, index_to = 0, 1
            for i in range(self.neighbors):  # cycle to generate neighbors
                neighbor_route = current_route.generate_neighbor_route(index_from, index_to)  # generate neighbor
                if Solver.accept(current_route, neighbor_route, T):  # if the neighbor is accepted, select this neighbor as current route
                    current_route = neighbor_route
                    if current_route.distance < best_route.distance:  # save the current route as the best route if the distance is better
                        best_route = current_route
                index_to += 1
                if index_to == cities_count:
                    index_from += 1
                    index_to = index_from + 1
            distances.append(current_route.distance)
            T *= self.cooling_factor  # lower the temperature
        end_time = timer()  # ending time
        best_route.plot_route()
        return best_route, distances, end_time-start_time


# route class
class Route:
    def __init__(self, cities):
        self.cities = cities
        self.distance = self.get_distance()

    # returns a random route with given cities
    @staticmethod
    def generate_init_route(cities):
        return Route(random.sample(cities, len(cities)))  # generating a random sample

    # returns the euclid distance
    @staticmethod
    def euclid_distance(coords_from, coords_to):
        return math.sqrt((coords_from[0] - coords_to[0]) ** 2 + (coords_from[1] - coords_to[1]) ** 2)

    # returns a neighbor route by swapping two elements from the original route
    def generate_neighbor_route(self, index_from, index_to):
        new_cities = self.cities[:]   # copying the route
        new_cities[index_from], new_cities[index_to] = new_cities[index_to], new_cities[index_from]  # swapping cities
        return Route(new_cities)

    # returns the total distance of a route
    def get_distance(self):
        dist = 0
        for i in range(len(self.cities)-1):  # for each couple of cities calculate the distance
            dist += Route.euclid_distance(self.cities[i].coords(), self.cities[i+1].coords())
        dist += Route.euclid_distance(self.cities[-1].coords(), self.cities[0].coords())
        return dist

    # plots the route
    def plot_route(self):
        x, y = [], []
        plt.cla()
        for i in range(len(self.cities)):
            x_coord, y_coord = self.cities[i].coords()
            x.append(x_coord), y.append(y_coord)
            plt.plot(x_coord, y_coord, 'ro')
            plt.annotate(self.cities[i].name, (x_coord, y_coord))
        plt.plot(x, y, 'b')
        plt.plot([x[-1], x[0]], [y[-1], y[0]], 'b')
        plt.xlabel("Width")
        plt.ylabel("Height")
        plt.title("Shortest route found")
        plt.pause(0.0001)


print("****************************************************")
print(">>>      TRAVELLING SALESMAN PROBLEM SOLVER      <<<")
print(">>>             SIMULATED ANNEALING              <<<")
print("****************************************************\n")

print("--- Map configuration ---")
map_height = int(input("Enter the map height: "))  # map height input
map_width = int(input("Enter the map width: "))  # map width input
city_count = int(input("Enter the number of cities: "))  # number of cities input
bool_random = int(input("Enter '1' to generate random cities or '0' to enter coordinates: "))
print()

while True:
    cities_generated = City.generate_cities(map_height, map_width, city_count, bool_random)  # generated cities
    City.plot_cities(cities_generated)  # plot cities
    if bool_random == 0:  # if coords were selected by user break
        break
    else:  # else ask him whether to generate cities again
        generate_again = int(input("Enter '1' to generate again or '0' to continue: "))
    if generate_again == 0:
        break

initial_route = Route.generate_init_route(cities_generated)  # generated initial route

while True:
    print("\n--- Simulated annealing algorithm configuration ---")
    init_temp = float(input("Enter the initial temperature: "))  # initial temperature input
    min_temp = float(input("Enter the minimal temperature: "))  # minimal temperature input
    cooling_factor = float(input("Enter the cooling factor: "))  # cooling factor input
    animate = int(input("Enter '1' for live animation or '0' for no animation: "))  # animate bool input

    solver = Solver(initial_route, init_temp, min_temp, cooling_factor)  # solver class initialization
    shortest_route, route_distances, time_taken = solver.solve(animate)  # actual solving

    print("\n--- Summary ---")
    print("Shortest route:", end=' ')
    for point in shortest_route.cities:  # printing the route
        print(point.name, end=' ')
    print("\nTotal distance:", round(shortest_route.distance, 2))  # total distance
    print("Time taken:", round(time_taken, 2), "sec")  # time taken
    plt.show()
    stages = []
    for stage in range(len(route_distances)):
        stages.append(stage + 1)
    # plotting the process
    plt.plot(stages, route_distances, 'b')
    plt.xlabel("Stage")
    plt.ylabel("Distance")
    plt.title("Distances across stages")
    plt.show()

    # run again with different settings or end the program
    run_again = int(input("\nEnter '1' to run again with different settings or '0' to end: "))
    if run_again == 0:
        break
