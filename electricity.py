import pygame

vertical_wire = pygame.image.load("utilities/vertical_wire.png")
horizontal_wire = pygame.image.load("utilities/horizontal_wire.png")
cell = pygame.image.load("utilities/cell.png")
resistor = pygame.image.load("utilities/resistor.png")
n_wire = pygame.image.load("utilities/n_wire.png")
s_wire = pygame.image.load("utilities/s_wire.png")
e_wire = pygame.image.load("utilities/e_wire.png")
w_wire = pygame.image.load("utilities/w_wire.png")

#dictionary containing every wire and junction type.
wire_dict = {
    "U":vertical_wire,
    "D":vertical_wire,
    "R":horizontal_wire,
    "L":horizontal_wire,
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
        # changing the outline to the resistor.
        self.outline_square.fill((0, 0, 0, 0))
        self.outline_square.blit(resistor, (0, 0))
        

        
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
        #getting the width after the wire has been toggled two times.
        wire_width = abs(coords1[0] - coords2[0]) 
        wire_height = abs(coords1[1] - coords2[1]) 
        #creating a horizontal and vertical strip.
        

        
        string1 = f'WIRE {int(coords1[0])} {int(coords1[1])} {int(junction_coords[0])} {int(junction_coords[1])}'
        self.asc_string += string1 + "\n"
        if not(coords2[0] == junction_coords[0] and coords2[1] == junction_coords[1]):
            string2 = f'WIRE {int(junction_coords[0])} {int(junction_coords[1])} {int(coords2[0])} {int(coords2[1])}'
            self.asc_string += string2 + "\n"

        


    def get_junctions(self, x_list, y_list):
        intersections = Junctions()

        for h_line in x_list:
            h_y, h_x1, h_x2 = h_line
            
            for v_line in y_list:
                v_x, v_y1, v_y2 = v_line
                
                # Check if the vertical line's x-coordinate is within the horizontal line's x-range
                if h_x1 <= v_x <= h_x2:
                    # Check if the horizontal line's y-coordinate is within the vertical line's y-range
                    if v_y1 <= h_y <= v_y2:
                        coordinates = (v_x, h_y)
                        intersections.add_item(coordinates)
                

        for h_line in x_list:
            h_y, h_x1, h_x2 = h_line
            intersections.add_item((h_x1, h_y))
            intersections.add_item((h_x2, h_y))
            

        for v_line in y_list:
            v_x, v_y1, v_y2 = v_line
            intersections.add_item((v_x, v_y1))
            intersections.add_item((v_x, v_y2))

        
        return intersections

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
            width = coords[2] - coords[1] - self.square_width
            max_count = width // self.square_width
            wire_img = wire_dict["R"]
            x = coords[1] + self.square_width
            y = coords[0]
            surface = pygame.Surface((width, height), pygame.SRCALPHA)
            for i in range(0, max_count):
                surface.blit(wire_img, (self.square_width * i, 0))




        #same concept now just in the y direction
        elif direction == "y":
            width = self.square_width
            height = coords[2] - coords[1] - self.square_width
            wire_img = wire_dict["U"]
            y = coords[1] + self.square_width
            x = coords[0]
            max_count = height // self.square_width
            surface = pygame.Surface((width, height), pygame.SRCALPHA)
            for i in range(0, max_count):
                surface.blit(wire_img, (0, self.square_width * i))
                



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

    def get_junction_type(self, coords):
        j_type = ""
        n_coords = (coords[0], coords[1] - self.square_width)
        s_coords = (coords[0], coords[1] + self.square_width)
        e_coords = (coords[0] + self.square_width, coords[1])
        w_coords = (coords[0] - self.square_width, coords[1])
        
        if n_coords in self.e_grid_coords and self.e_grid_coords[n_coords] == "W":
            j_type += "N"
        if e_coords in self.e_grid_coords and self.e_grid_coords[e_coords] == "W":
            j_type += "E"
        if s_coords in self.e_grid_coords and self.e_grid_coords[s_coords] == "W":
            j_type += "S"
        if w_coords in self.e_grid_coords and self.e_grid_coords[w_coords] == "W":
            j_type += "W"
            
        return j_type

    
    def get_junction_surface(self, j_type):
        surface = pygame.Surface((self.square_width, self.square_width), pygame.SRCALPHA)
        surface.fill((0, 0, 0, 0))
        if "N" in j_type:
            surface.blit(wire_dict["N"], (0, 0))
        if "E" in j_type:
            surface.blit(wire_dict["E"], (0, 0))
        if "S" in j_type:
            surface.blit(wire_dict["S"], (0, 0))
        if "W" in j_type:
            surface.blit(wire_dict["W"], (0, 0))
        return surface


    def update_wire(self):
        components = self.asc_string.split('\n')
        y_wire_list = []
        x_wire_list = []
        for component in components:
            array = component.split(" ")
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

        junction_list = self.get_junctions(x_wire_list, y_wire_list)
        
        self.circuit.fill((0, 0, 0, 0))

        
        empty_square = pygame.Surface((self.square_width, self.square_width), pygame.SRCALPHA)

        #drawing the horizontal wire, vertical wiers then junctions.
        for x_wire in x_wire_list:
            wire_surface = self.draw_wire(x_wire, "x")
            self.circuit.blit(wire_surface, (0, 0))
            
        for y_wire in y_wire_list:
            wire_surface = self.draw_wire(y_wire, "y")
            self.circuit.blit(wire_surface, (0, 0))
            
        
        for junction in junction_list.j_list:
            j_type = self.get_junction_type(junction)
            junction_surface = self.get_junction_surface(j_type)
            self.circuit.blit(junction_surface, (junction[0], junction[1]))



    def toggle_wire(self):

        #toggling the wire
        self.wire_toggled = not self.wire_toggled
        #getting the coordinates and putting it into an array.
        coords = [self.x_outline, self.y_outline]
        if self.wire_toggled:
            #if the wire has just been toggled, the initial coordinates are taken
            self.init_wire_coords = coords
        else:
            self.add_wire(self.init_wire_coords, coords)
            self.update_wire()


    #updating the container.
    def update_container(self):
        #resetting the canvas
        self.canvas.fill("black")
        #starting by drawing the grid, then the circuit, then the outline.
        self.canvas.blit(self.grid, (0, 0))
        self.canvas.blit(self.circuit, (0, 0))
        if self.outline_bool:
            self.canvas.blit(self.outline_square, (self.x_outline, self.y_outline))


    def __init__(self, width=800, height=800, s_width=40):
        #initialising all of the variables.
        self.wire_toggled = False
        self.components = []
        self.outline_bool = False
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
        
        for x in range(0, width, self.square_width):
            for y in range(0, height, self.square_width):
                self.e_grid_coords[(x, y)] = "B"
    
