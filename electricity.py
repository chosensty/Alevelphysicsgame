from johnson import simple_cycles
from collections import Counter
import numpy as np

class Component:

    def __init__(self, character):
        if character == "L":
            self.resistance = 10
            self.component = "LAMP"
            self.type = "RESISTANCE"
        if character == "P":
            self.voltage = 6
            self.component = "POWERSUPPLY"
            self.type = "POWERSUPPLY"



class Edge_List:
    def return_equation(self, cycle):
        sum_of_emfs = 0
        sum_of_voltages = np.zeros((len(self.currents)))
        number_of_nodes = len(cycle)
        for i in range(0, number_of_nodes):
            edge = cycle[i:i+2]
            if i == number_of_nodes-1:
                edge = [cycle[i], cycle[0]]

            sorted_edge = edge
            curr_dir = 1
            if edge[1] < edge[0]:
                sorted_edge = [edge[1], edge[0]]
                curr_dir = -1
            index = self.find_edge(sorted_edge)
            self.list[index].current_direction = curr_dir            
            data = self.list[index].return_data(edge)
            c_i = self.find_current(self.list[index].current_index)
                
            sum_of_emfs += data[0]
            sum_of_voltages[c_i] += data[1]
        return sum_of_voltages, sum_of_emfs
    
    def assign_current_values(self, values):
        for edge in self.list:
            c_i = self.find_current(edge.current_index)
            edge.current = values[c_i]

    def return_edges(self, node):
        indexes = []
        for i in range(0, len(self.list)):
            if self.list[i].edge[0] == node or self.list[i].edge[1] == node:
                indexes.append(i)
        return indexes

    def return_current_equation(self, node):
        indexes = self.return_edges(node)
        data = np.zeros((len(self.currents)))
        for i in range(0, len(indexes)):
            index = indexes[i]
            c_i = self.find_current(self.list[index].current_index)
            data[c_i] = self.list[i].current_direction
        return data



    def find_edge(self, edge):
        for i in range(0, len(self.list)):
            if self.list[i].edge == edge:
                return i
        return -1

    def find_current(self, index):
        for i in range(0, len(self.currents)):
            if self.currents[i] == index:
                return i
        return -1

    def assign_current(self, edge, index, current_dir=1):
        sorted_edge = edge
        curr_dir = current_dir
        if edge[0] > edge[1]:
            sorted_edge = [edge[1], edge[0]]
            curr_dir *= -1
        position = self.find_edge(sorted_edge) 
        if position == -1:
            return
        self.list[position].assign_current(index, curr_dir)
        i = self.find_current(index)
        if i == -1:
            self.currents.append(index)

    def add_edge(self, new_edge):
        index = self.find_edge(new_edge)
        if index == -1:
            self.list.append(new_edge)
        
    def __init__(self):
        self.list = []
        self.currents = []
        
class Edge:

    def assign_current(self, index, curr_dir):
        self.current_index = index
        self.current_direction = curr_dir
        print("EDGE: " + str(self.edge) + " HAS BEEN ASSIGNED INDEX: " + str(index))

    def return_data(self, edge):
        sign = 1
        if edge[0] == self.edge[1]:
            sign = -1
        total_resistance = 0
        total_voltage = 0
        for component in self.component_list:
            if component.type == "POWERSUPPLY":
                total_voltage += component.voltage
            else:
                total_resistance += component.resistance
        return sign * self.current_direction * total_voltage, sign * self.current_direction * total_resistance

    def __init__(self, string, edge, step):
        self.component_list = []
        self.edge = edge
        self.string = string
        self.current_index = 0
        for i in range(edge[0], edge[1]+1, step):
            if string[i] != "W":
                self.component_list.append(Electrical_Component(string[i]))


class Electrical_Component:

    def __init__(self, type):
        if type == "L":
            self.type = "LAMP"
            self.resistance = 10
        elif type == "P":
            self.type = "POWERSUPPLY"
            self.voltage = 6


class Circuit:

    def evaluate_circuit(self):
        cycles = list(simple_cycles(self.graph))
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
        
        visited_edges = []

        def find(list, item):
            for i in range(0, len(list)):
                if item == list[i]:
                    return i
                
            return -1



        def current_assignment(node, neighbour, index, stop=False, dir=1):
            edge = [node, neighbour]
            if node > neighbour:
                edge = [neighbour, node]
            if find(visited_edges, edge) != -1:
                return 
            self.edge_list.assign_current([node, neighbour], index, dir)
            visited_edges.append(edge)
            no_of_neighbours = len(self.graph[neighbour])
            if no_of_neighbours == 2:
                i = 0
                if find(self.graph[neighbour], (node)) == i:
                    i = 1
                current_assignment(neighbour, self.graph[neighbour][i],index, stop, dir)
            if no_of_neighbours > 2:
                if stop:
                    return
                previous_node_index = find(self.graph[neighbour], node)
                new_index = 1
                for i in range(0, no_of_neighbours):
                    if previous_node_index == i:
                        continue
                    current_assignment(neighbour, self.graph[neighbour][i], index+new_index, stop, dir)
                    new_index += 1

        #for item in self.edge_list.list:
        #    print(item.edge)

        for node in self.graph:
            if len(self.graph[node]) == 2:
                neighbour = self.graph[node][1]
                current_assignment(node, neighbour, 1, True, -1)
                neighbour = self.graph[node][0]
                current_assignment(node, neighbour, 1)
                break
        
        orders = len(self.edge_list.currents)
        resistances_matrix = []
        emfs_matrix = []
        for i in range(0, len(cycles)):
            row = self.edge_list.return_equation(cycles[i])
            resistances_matrix.append(list(row[0]))
            emfs_matrix.append(row[1])
        
        for vertice in self.graph:
            edges = len(self.graph[vertice])
            if edges > 2:
                row = self.edge_list.return_current_equation(vertice)
                resistances_matrix.append(list(row))
                emfs_matrix.append(0)
        
        if len(resistances_matrix) > 1:
            index = 0
            left_matrix = []
            right_matrix = []
            while index < len(resistances_matrix):
                if find(left_matrix, resistances_matrix[index]) == -1:
                    left_matrix.append(resistances_matrix[index])
                    right_matrix.append(emfs_matrix[index])
                
                index += 1
    

            left_matrix = np.array(left_matrix[1:])
            right_matrix = np.array(right_matrix[1:])
            result = np.linalg.solve(left_matrix, right_matrix)
            print(left_matrix)
            print(right_matrix)
            print(result)
        else:
            result = [emfs_matrix[0] / resistances_matrix[0][0]]

        self.edge_list.assign_current_values(result)
        for edge in self.edge_list.list:
            print(edge.current)  

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

        self.edge_list = Edge_List()
        for key in nodes:
            for i in range(0, len(nodes[key])):
                start = key
                end = nodes[key][i]
                edge = [start, end]
                if start < end:
                    if (edge[1] - edge[0])%self.cols == 0:
                        self.edge_list.add_edge(Edge(self.grid, edge, self.cols))
                    else:
                        self.edge_list.add_edge(Edge(self.grid, edge, 1))

        self.graph = nodes


    def __init__(self, filename, rows=10, cols=10):
        f = open(filename, 'r')
        self.grid = f.read().replace("\n", "")
        self.rows = rows
        self.cols = cols
        self.build_graph()
        self.evaluate_circuit()



circuit = Circuit('utilities/circuit2.txt')


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