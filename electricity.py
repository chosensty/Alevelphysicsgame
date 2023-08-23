from johnson import simple_cycles
from collections import Counter
import numpy as np
def evaluate_circuit():
    graph = {}
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


class Circuit
    def __init__(self, string):
        self.graph = {
            0:[1, 2],
            1:[0, 3],
            2:[0, 3],
            3:[1, 2]
        }
        self.wires = {
            
        }

class Electrical_Component:
    def __init__(self, component):
        self.component = component
        self.resistance = 0
        if component == 'blank':
            pass
        elif component == 'wire':
            pass
        elif component == 'power_supply':
            self.voltage = 6
        elif component == 'lamp':
            self.resistance = 10             
        


class Edge:
    def __init__(self, component_list, vertices):
        self.component_list = component_list
        self.edge = vertices
    def add_component(self, component):
        self.component_list.push(component)


def load_circuit():
    lamp 
    print(component_list)