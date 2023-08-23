from johnson import simple_cycles
from collections import Counter
import numpy as np



    

class Component:
    def __init__(self, character):
        if character == "L":
            self.resistance = 10
            self.type = "LAMP"
        if character == "P":
            self.voltage = 6
            self.type = "POWERSUPPLY"

class Circuit:
    def evaluate_circuit(self, graph):
        cycles = list(simple_cycles(graph))
        length = len(cycles)
        i = 0
        while i<length:
            if len(cycles[i]) == 2:
                cycles.pop(i)
                length = len(cycles)
            else:
                x = i + 1
                while x < length:
                    if Counter(cycles[x]) == Counter(cycles[i]):
                        cycles.pop(x)
                        length = len(cycles)
                        break
                    else:
                        x += 1
                i += 1

    def build_graph(self):    
        nodes = {
        }
        def check_junction(index):
            return (self.grid[index+1] == "W" or self.grid[index-1] == "W") and (self.grid[index + self.rows] == "W" or self.grid[index - self.rows] == "W")
        
        def find_junction(index, direction):
            if direction == "E":
                for i in range(1, self.cols - (index)%self.cols):
                    if check_junction(index + i):
                        return index + i
            elif direction == "W":
                for i in range(1, (index)%self.cols):
                    if check_junction(index - i):
                        return index - i
            elif direction == "N":
                for i in range(1, index // self.cols):
                    if check_junction(index - i * self.cols):
                        return index - i * self.cols
            elif direction == "S":
                for i in range(1, self.cols - index // self.cols):
                    if check_junction(index + i * self.cols):
                        return index + i * self.cols

        index = 0
        
        for index in range(0, self.rows * self.cols):
            if self.grid[index] == "W":
                connections = []

                if check_junction(index):
                    if self.grid[index - 1] == "W":
                        connections.append(find_junction(index, "W"))
                    if self.grid[index + 1] == "W":
                        connections.append(find_junction(index, "E"))
                    if self.grid[index - self.rows] == "W":
                        connections.append(find_junction(index, "N"))
                    if self.grid[index + self.rows] == "W":
                        connections.append(find_junction(index, "S"))
                    nodes[index] = connections

        
        self.graph = nodes


    def __init__(self, filename):
        f = open(filename, 'r')
        self.grid = f.read().replace("\n", "")
        self.rows = 10
        self.cols = 10
        self.build_graph()
        self.evaluate_circuit(self.graph)



circuit = Circuit('utilities/circuit1.txt')


'''
class Vertice:
    def __init__(self, x, y,)

KEY:

W = wire
L = lightbulb
B = blank
P = power_supply

GRID:
BBBBBBBBBB
BBBBBBBBBB
BBWWPWWBBB
BBWBBBWBBB
BBWBBBWBBB
BBWWLWWBBB
BBBBBBBBBB
BBBBBBBBBB
BBBBBBBBBB
BBBBBBBBBB

'''