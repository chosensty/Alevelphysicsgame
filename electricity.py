import pygame
from PySpice.Probe.Plot import plot
from PySpice.Spice.Netlist import Circuit
from PySpice.Spice.Parser import SpiceParser
from PySpice.Spice.Library import SpiceLibrary
from PySpice.Unit import *
from PySpice.Logging.Logging import setup_logging

setup_logging()#loading every wire type.
vertical_wire = pygame.image.load("utilities/vertical_wire.png")
horizontal_wire = pygame.image.load("utilities/horizontal_wire.png")
cell = pygame.image.load("utilities/cell.png")
resistor_img = pygame.image.load("utilities/resistor.png")
n_wire = pygame.image.load("utilities/n_wire.png")
s_wire = pygame.image.load("utilities/s_wire.png")
e_wire = pygame.image.load("utilities/e_wire.png")
w_wire = pygame.image.load("utilities/w_wire.png")

#dictionary containing every wire and junction type.
wire_dict = {
    "V":vertical_wire,
    "H":horizontal_wire,
    "N":n_wire,
    "E":e_wire,
    "S":s_wire,
    "W":w_wire,
}

class Junctions:
    
    
    def __init__(self):
        self.j_list = [] 
        
        
    def item_exists(self, new_j):
        for junction in self.j_list:
            if new_j == junction:
                return True    
        return False
    
    
    def add_item(self, new_j):
        if not self.item_exists(new_j):
            self.j_list.append(new_j)





class Electricity:
        
    e_grid_coords = {}
    def insert_component(self):
        # changing the outline back to the white outline.
        self.outline_square.fill((0, 0, 0, 0))
        pygame.draw.rect(self.outline_square, "white", (0, 0, self.square_width, self.square_width), 1)


    def add_resistor(self):
        coords = (int(self.x_outline), int(self.y_outline))
        self.e_grid_coords[coords] = "R"
        schem_string = "RESISTOR "
        
        if self.orientation % 2 == 0:
            
            schem_string += f'{coords[0]} {coords[1]} {coords[0] + self.square_width} {coords[1]}\n'
            coords = (self.x_outline + self.square_width, self.y_outline)
            self.e_grid_coords[coords] = "R"
            
        elif self.orientation % 2== 1:
            
            schem_string += f'{coords[0]} {coords[1]} {coords[0]} {coords[1] + self.square_width}\n'
            coords = (self.x_outline, self.y_outline + self.square_width)
            self.e_grid_coords[coords] = "R"

        self.asc_string += schem_string
            
    def add_cell(self):
        coords = (int(self.x_outline), int(self.y_outline))
        self.e_grid_coords[coords] = "C"
        polarity = "S"
        if self.orientation > 1:
            polarity = "N"
       
        schem_string = "CELL" + polarity + " "

        if self.orientation% 2 == 0:
            schem_string += f'{coords[0]} {coords[1]} {coords[0] + self.square_width} {coords[1]}\n'
            coords = (self.x_outline + self.square_width, self.y_outline)
            self.e_grid_coords[coords] = "C"
        elif self.orientation % 2 == 1:
            schem_string += f'{coords[0]} {coords[1]} {coords[0]} {coords[1] + self.square_width}\n'
            coords = (self.x_outline, self.y_outline + self.square_width)
            self.e_grid_coords[coords] = "C"

        self.asc_string += schem_string


    def select_cell(self):
        # changing the outline to the resistor.
        if self.cursor_state != "inserting_cell":
            self.cursor_state = "inserting_cell"
        else:
            self.add_cell()
            self.cursor_state = "navigating"
            self.update_wire()



    def select_resistor(self):
        # changing the outline to the resistor.
        if self.cursor_state != "inserting_resistor":
            self.cursor_state = "inserting_resistor"
        else:
            self.add_resistor()
            self.cursor_state = "navigating"
            self.update_wire()

        
    #updating the outline around the square.
    def update_outline(self, x_pos, y_pos, outline_bool=False):
        #getting the top left coordinates of the square.
        self.x_outline = x_pos // self.square_width * self.square_width
        self.y_outline = y_pos // self.square_width * self.square_width
        #making sure that the coordinates are within the grids range.
        if self.x_outline == self.width:
            self.x_outline -= self.square_width
        if self.y_outline == self.height:
            self.y_outline -= self.square_width

        #updating the outline boolean, it can be turned to false by the user if they don't want an outline.
        self.outline_bool = outline_bool

        
    
    def add_wire(self, coords1, coords2):
        junction_coords = [coords2[0], coords1[1]]
        
        string1 = f'WIRE {int(coords1[0])} {int(coords1[1])} {int(junction_coords[0])} {int(junction_coords[1])}'
        self.asc_string += string1 + "\n"
        if not(coords2[0] == junction_coords[0] and coords2[1] == junction_coords[1]):
            string2 = f'WIRE {int(junction_coords[0])} {int(junction_coords[1])} {int(coords2[0])} {int(coords2[1])}'
            self.asc_string += string2 + "\n"


        

    def draw_wire(self, coords, direction, canvas_w=800, canvas_h=800):
        #initialising width, height, x and y coordinates to empty variables. 
        width = 0
        height = 0
        x = 0
        y = 0
        max_count = 0
        surface = None
        
        #getting the coordinates and width based on the parameters.
        #if the wire is in the 'x' direction, then the top left x coordinate is the second index of the 'coords' parameter.
        #the height is just one square, the width is the difference between the leftmost and rightmost part of the wire.
        #we add one more square to this to ensure that the wire isn't cut off.
        if direction == "x":
            height = self.square_width                
            width = abs(coords[2] - coords[1]) + self.square_width
            max_count = int(width // self.square_width)
            wire_img = wire_dict["H"]
            x = coords[1]
            y = coords[0]
            surface = pygame.Surface((width, height), pygame.SRCALPHA)

            surface.blit(wire_dict["E"], (0, 0))
            for i in range(1, max_count):
                if i != max_count - 1:
                    surface.blit(wire_img, (self.square_width * i, 0))
                else:
                    surface.blit(wire_dict["W"], (self.square_width  * i, 0))






        #same concept now just in the y direction
        elif direction == "y":
            width = self.square_width
            height = abs(coords[2] - coords[1]) + self.square_width
            wire_img = wire_dict["V"]
            y = coords[1]
            x = coords[0]
            max_count = int(height // self.square_width)
            surface = pygame.Surface((width, height), pygame.SRCALPHA)

            surface.blit(wire_dict["S"], (0, 0))

            for i in range(1, max_count):
                if i != max_count - 1:
                    surface.blit(wire_img, (0, self.square_width *  i))
                else:
                    surface.blit(wire_dict["N"], (0, self.square_width  * i))
                


        
        larger_surface = pygame.Surface((canvas_w, canvas_h), pygame.SRCALPHA)
        larger_surface.fill((0, 0, 0, 0))
        larger_surface.blit(surface, (x, y))
        return larger_surface


    def add_wires_to_grid(self, coords, direction):
        if direction == "x":
            for x in range(coords[1], coords[2] + self.square_width, self.square_width):
                self.e_grid_coords[(x, coords[0])] = "W"
        elif direction == "y":
            for y in range(coords[1], coords[2] + self.square_width, self.square_width):
                self.e_grid_coords[(coords[0], y)] = "W"

    def remove_schem_redundancies(self):
        components = self.asc_string.split('\n')
        y_wire_list = []
        x_wire_list = []
        
        i = 0
        while i < len(components):
            component = components[i]
            array = component.split(" ")
           
            if array[0] == "WIRE":
                if array[1] == array[3] and array[2] == array[4]:
                    pass
                elif array[1] == array[3]:
                    y_range = [int(array[2]), int(array[4])]
                    y_range.sort()
                    y_wire_list.append([int(array[1]), y_range[0], y_range[1]])
                elif array[2] == array[4]:
                    x_range = [int(array[1]), int(array[3])]
                    x_range.sort()
                    x_wire_list.append([int(array[2]), x_range[0], x_range[1]])
                del components[i]
            else:
                i+=1

        x_wire_list.sort(key=lambda x: x[0])
        y_wire_list.sort(key=lambda x: x[0])
        
        i1 = 0
        while (i1 < len(x_wire_list)):
            i2 = i1 + 1
            while (i2 <  len(x_wire_list)):
                if x_wire_list[i1][0] == x_wire_list[i2][0]:
                    a1, b1 = x_wire_list[i1][1:]
                    a2, b2 = x_wire_list[i2][1:]
                    if not (b1 < a2 or b2 < a1):
                        del x_wire_list[i2]
                        x_wire_list[i1][1] = min(a1, a2)
                        x_wire_list[i1][2] = max(b1, b2)
                else:
                    break
                i2+= 1
            i1 += 1

        i1 = 0
        while i1 < len(y_wire_list):
            i2 = i1 + 1
            while i2 < len(y_wire_list):
                if y_wire_list[i1][0] == y_wire_list[i2][0]:
                    a1, b1 = y_wire_list[i1][1:]
                    a2, b2 = y_wire_list[i2][1:]
                    if not (b1 < a2 or b2 < a1):
                        del y_wire_list[i2]
                        y_wire_list[i1][1] = min(a1, a2)
                        y_wire_list[i1][2] = max(b1, b2)
                else:
                    break
                i2+=1 
            i1 += 1


        for x_wire in x_wire_list:
            string = f'WIRE {x_wire[1]} {x_wire[0]} {x_wire[2]} {x_wire[0]}'
            components.append(string)

        for y_wire in y_wire_list:
            string = f'WIRE {y_wire[0]} {y_wire[1]} {y_wire[0]} {y_wire[2]}'
            components.append(string)


        self.asc_string = "\n".join(components)





    def update_wire(self):
        
        components = self.asc_string.split('\n')
        y_wire_list = []
        x_wire_list = []
        
        self.circuit.fill((0, 0, 0, 0))
        
        for component in components:
            array = component.split(" ")

            if array[0][:4] == "CELL":
                x1, y1, x2, y2 = array[1:]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                width = abs(x2 - x1)
                height = abs(y2 - y1)
                cell_img = cell
                small_x = x1
                small_y = y1
                rotation_factor = 0
                if array[0][4] == "N":
                    rotation_factor += 180
                cell_img = pygame.transform.rotate(cell, -rotation_factor)
                if x1 == x2:
                    rotation_factor += 90
                    cell_img = pygame.transform.rotate(cell, -rotation_factor)
                    self.circuit.blit(cell_img, (small_x, small_y + (self.square_width // 2)))
                if y1 == y2:
                    self.circuit.blit(cell_img, (small_x + (self.square_width // 2), small_y)) 
 

            if array[0] == "RESISTOR":
                x1, y1, x2, y2 = array[1:]
                print(array[1:])
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                width = abs(x2 - x1)
                height = abs(y2 - y1)
                res_img = resistor_img
                small_x = x1
                small_y = y1
                if x1 == x2:
                    res_img = pygame.transform.rotate(resistor_img, -90)
                    self.circuit.blit(res_img, (small_x, small_y + (self.square_width // 2)))
                if y1 == y2:
                    self.circuit.blit(res_img, (small_x + (self.square_width // 2), small_y)) 

            if array[0] == "WIRE":
                if array[1] == array[3] and array[2] == array[4]:
                    continue
                if array[1] == array[3]:
                    y_range = [int(array[2]), int(array[4])]
                    y_range.sort()
                    self.add_wires_to_grid((int(array[1]), y_range[0], y_range[1]), "y")
                    y_wire_list.append([int(array[1]), y_range[0], y_range[1]])
                if array[2] == array[4]:
                    x_range = [int(array[1]), int(array[3])]
                    x_range.sort()
                    self.add_wires_to_grid((int(array[2]), x_range[0], x_range[1]), "x")
                    x_wire_list.append([int(array[2]), x_range[0], x_range[1]])



        

        #drawing the horizontal wire, vertical wiers then junctions.
        for x_wire in x_wire_list:
            wire_surface = self.draw_wire(x_wire, "x")
            self.circuit.blit(wire_surface, (0, 0))
            
        for y_wire in y_wire_list:
            wire_surface = self.draw_wire(y_wire, "y")
            self.circuit.blit(wire_surface, (0, 0))
            


    def toggle_wire(self): #toggling the wire 
        self.wire_toggled = not self.wire_toggled #getting the coordinates and putting it into an array.
        coords = [self.x_outline, self.y_outline]
        if self.wire_toggled:
            self.cursor_state = "inserting_wire"
            #if the wire has just been toggled, the initial coordinates are taken
            self.init_wire_coords = coords
        else:
            self.cursor_state = "navigating"
            self.add_wire(self.init_wire_coords, coords)
            self.update_wire()

            
        # Function to parse the schematic file and generate a netlist
    def generate_netlist(self):
        # Dictionary to store components and their connections
        components = []
        nodes = {}  # To map coordinates to node numbers
        wire_connections = []  # To track wire connections (start, end)

        # Initialize node counter
        node_counter = 1
        
        self.remove_schem_redundancies()

        lines = self.asc_string.split("\n")
        lines = [line for line in lines if line] 
        # First pass: Identify and assign nodes
        for line in lines:
            tokens = line.split()
            component_name = tokens[0]
            x1, y1, x2, y2 = int(tokens[1]), int(tokens[2]), int(tokens[3]), int(tokens[4])

            if component_name == "WIRE":
                wire_connections.append(((x1, y1), (x2, y2)))

            # Assign nodes for components if not already assigned
            if component_name in ["RESISTOR", "CELL"]:
                if (x1, y1) not in nodes:
                    nodes[(x1, y1)] = node_counter
                    node_counter += 1
                if (x2, y2) not in nodes:
                    nodes[(x2, y2)] = node_counter
                    node_counter += 1

        # Second pass: Handle wire connections and merge nodes
        for (start, end) in wire_connections:
            if start in nodes and end in nodes:
                # Merge nodes by updating the end node to be the same as the start node
                end_node = nodes[end]
                start_node = nodes[start]

                # Replace all instances of end_node with start_node
                for key in nodes:
                    if nodes[key] == end_node:
                        nodes[key] = start_node
            elif start in nodes:
                nodes[end] = nodes[start]
            elif end in nodes:
                nodes[start] = nodes[end]
            else:
                # Both are new, assign the same node
                nodes[start] = node_counter
                nodes[end] = node_counter
                node_counter += 1

        first_cell_found = False
        gnd_node = 0
        # Third pass: Generate component entries
        for line in lines:
            tokens = line.split()
            component_name = tokens[0]
            x1, y1, x2, y2 = int(tokens[1]), int(tokens[2]), int(tokens[3]), int(tokens[4])

            if component_name == "RESISTOR":
                node1 = nodes[(x1, y1)]
                node2 = nodes[(x2, y2)]
                components.append(f"R{len(components) + 1} N{node1} N{node2} 1k")
            if component_name[:4] == "CELL" and first_cell_found:
                node1 = nodes[(x1, y1)]
                node2 = nodes[(x2, y2)]
                
                if component_name[4] == "S":
                    components.append(f"V{len(components) + 1} N{node2} N{node1} DC 5")
                else:
                    components.append(f"V{len(components) + 1} N{node1} N{node2} DC 5")
            elif not first_cell_found and component_name[:4] == "CELL":
                node1 = nodes[(x1, y1)]
                node2 = nodes[(x2, y2)]

                
                if component_name[4] == "S":
                    components.append(f"V{len(components) + 1} N{node2} 0 DC 5")
                    gnd_node = node1
                    #components.append(f'R{len(components) + 1} N{node1} 0 0')
                else:
                    components.append(f"V{len(components) + 1} N{node1} 0 DC 5")
                    gnd_node = node2
                    #components.append(f'R{len(components) + 1} N{node1} 0 0')
                first_cell_found = True

        for x in range(0, len(components)):
            data = components[x].split()
            for y in range(0, len(data)):
                if data[y] == f'N{gnd_node}':
                    data[y] = '0'
                    components[x] = ' '.join(data)

        # Generate the netlist
        netlist = ".title Generated Netlist\n"
        for component in components:
            netlist += component + "\n"
        netlist += ".op\n"
        netlist += ".end"

        f = open("demo_file.txt", "w")
        f.write(netlist)
        f.close()
        parser = SpiceParser("demo_file.txt")
        circuit = parser.build_circuit()
        
        simulator = circuit.simulator()
        analysis = simulator.operating_point()
        
            # Extract and print all node voltages
        print("DC Node Voltages:")
        for node in analysis.nodes.values():
            print(f'{str(node):>5}: {float(node):>6} V')

# Extract and print all branch currents
        print("\nDC Branch Currents:")
        for branch in analysis.branches.values():
            print(f'{str(branch):>5}: {float(branch):>6} A')

    #updating the container.
    def update_container(self):
        #resetting the canvas
        self.canvas.fill("black")
        #starting by drawing the grid, then the circuit, then the outline.
        self.canvas.blit(self.grid, (0, 0))
        self.canvas.blit(self.circuit, (0, 0))
        if self.cursor_state == "navigating" or True:
            self.canvas.blit(self.outline_square, (self.x_outline, self.y_outline))

        if self.cursor_state == "inserting_wire":
            #getting the coordinates of the inserting wire.
            x_coords = [self.init_wire_coords[0], self.x_outline]
            x_coords.sort()
            y_coords = [self.init_wire_coords[1], self.y_outline]
            y_coords.sort()
            # coordinates must be sorted so they are drawn correctly.
            x_coord_set = [self.init_wire_coords[1], x_coords[0], x_coords[1]]
            y_coord_set = [self.x_outline, y_coords[0], y_coords[1]] 
            if self.orientation % 2 ==0:
                x_coord_set[0] = self.y_outline
                y_coord_set[0] = self.init_wire_coords[0]

            if x_coords[0] != x_coords[1]:
                surface = self.draw_wire(x_coord_set, "x")
                self.canvas.blit(surface, (0, 0))
            if y_coords[0] != y_coords[1]:
                surface = self.draw_wire(y_coord_set, "y")
                self.canvas.blit(surface, (0, 0))
                
        if self.cursor_state == "inserting_cell":
            cell_img = cell
            if self.orientation != 0:
                cell_img = pygame.transform.rotate(cell, -90 * self.orientation)
           

            if self.orientation % 2 == 0:
                self.canvas.blit(cell_img, (self.x_outline + (self.square_width// 2), self.y_outline))
            elif self.orientation % 2 == 1:
                self.canvas.blit(cell_img, (self.x_outline, self.y_outline + (self.square_width //2)))


        if self.cursor_state == "inserting_resistor":
            resistor = resistor_img
            if self.orientation% 2 != 0:
                resistor = pygame.transform.rotate(resistor_img, 90 * self.orientation)
           

            if self.orientation % 2 == 0:
                self.canvas.blit(resistor, (self.x_outline + (self.square_width// 2), self.y_outline))
            elif self.orientation % 2 == 1:
                self.canvas.blit(resistor, (self.x_outline, self.y_outline + (self.square_width //2)))


    def change_orientation(self):
        self.orientation += 1
        if self.orientation == 4:
            self.orientation = 0


    def __init__(self, width=800, height=800, s_width=40):
        #initialising all of the variables.
        self.wire_toggled = False
        self.components = []
        self.outline_bool = False
        self.init_wire_coords =  []
        self.asc_string = ""
        self.canvas = pygame.Surface((width, height))
        self.grid = pygame.Surface((width, height))
        self.square = pygame.Surface((s_width, s_width))
        self.circuit = pygame.Surface((width, height), pygame.SRCALPHA)
        self.circuit.fill((0, 0, 0, 0))
        self.square_width = s_width
        self.width = width
        self.height = height
        self.square_count = (width // s_width) * (height // s_width)
        self.orientation = 0 
        
        for i in range(0, self.square_count):
            color = ""
            if (i % 2 == 0 and (i // (self.square_width // 2)) % 2 == 0) or (i % 2 != 0 and (i // (self.square_width // 2)) % 2 != 0):
                color = "#8f8f8f"
            else:
                color = "#525252"
            self.square.fill(color)
            self.grid.blit(self.square, ((i%(self.square_width // 2))* self.square_width, (i//(self.square_width // 2))*self.square_width))
            
            
        self.outline_square = pygame.Surface((self.square_width, self.square_width), pygame.SRCALPHA)
        self.outline_square.fill((0, 0, 0, 0))
        pygame.draw.rect(self.outline_square, "white", (0, 0, self.square_width, self.square_width), 1)
        
        # N = navigating with cursor
        self.cursor_state = "navigating"
        
        for x in range(0, width, self.square_width):
            for y in range(0, height, self.square_width):
                self.e_grid_coords[(x, y)] = "B"
    
