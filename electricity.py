import pygame

vertical_wire = pygame.image.load("utilities/vertical_wire.png")
horizontal_wire = pygame.image.load("utilities/horizontal_wire.png")
cell = pygame.image.load("utilities/cell.png")
resistor = pygame.image.load("utilities/resistor.png")
up_left = pygame.image.load("utilities/up_left_wire.png")
up_right = pygame.image.load("utilities/up_right_wire.png")
down_left = pygame.image.load("utilities/down_left_wire.png")
down_right = pygame.image.load("utilities/down_right_wire.png")

wire_dict = {
    "DL":down_left,
    "DR":down_right,
    "UL":up_left,
    "UR":up_right,
    "U":vertical_wire,
    "D":vertical_wire,
    "R":horizontal_wire,
    "L":horizontal_wire
}

class Electricity:
        
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
        horizontal_strip = pygame.Surface((wire_width, self.square_width), pygame.SRCALPHA)
        max_count = int(wire_width // self.square_width)
        
        #blitting the resistor image across the horizontal strip.
        for i in range(0, max_count):
            horizontal_strip.blit(horizontal_wire, (self.square_width * i, 0))

        vertical_strip = pygame.Surface((self.square_width, wire_height), pygame.SRCALPHA)
        max_count = int(wire_height // self.square_width)

        #blitting the resistor image across the vertical strip.
        for i in range(0, max_count):
            vertical_strip.blit(vertical_wire, (0, i * self.square_width))
        #drawing the two strips.
        if coords2[0] > coords1[0]:
            self.circuit.blit(horizontal_strip, (coords1[0], coords1[1]))
            if coords2[1] > coords1[1]:
                self.circuit.blit(down_left, junction_coords)
                self.circuit.blit(vertical_strip, (coords2[0], junction_coords[1] + self.square_width))

            else:
                self.circuit.blit(up_left, junction_coords)
                self.circuit.blit(vertical_strip, (coords2[0], junction_coords[1] - wire_height))
        else:
            self.circuit.blit(horizontal_strip, (coords1[0] - wire_width + self.square_width, coords1[1]))
            if coords2[1] > coords1[1]:
                self.circuit.blit(down_right, junction_coords)
                self.circuit.blit(vertical_strip, (coords2[0], junction_coords[1] + self.square_width))
            else:
                self.circuit.blit(up_right, junction_coords)
                self.circuit.blit(vertical_strip, (coords2[0], junction_coords[1] - wire_height))
        string1 = f'WIRE {int(coords1[0])} {int(coords1[1])} {int(junction_coords[0])} {int(junction_coords[1])}'
        print(string1)
        self.asc_string += string1
        if not(coords2[0] == junction_coords[0] and coords2[1] == junction_coords[1]):
            string2 = f'WIRE {int(junction_coords[0])} {int(junction_coords[1])} {int(coords2[0])} {int(coords2[1])}'
            self.asc_string += string2

        
    def get_junctions(self, x_list, y_list):
        intersections = []

        for h_line in x_list:
            h_y, h_x1, h_x2 = h_line
            
            for v_line in y_list:
                v_x, v_y1, v_y2 = v_line
                
                # Check if the vertical line's x-coordinate is within the horizontal line's x-range
                if h_x1 <= v_x <= h_x2:
                    # Check if the horizontal line's y-coordinate is within the vertical line's y-range
                    if v_y1 <= h_y <= v_y2:
                        type = ""
                        # An intersection is found
                        if h_y == v_y1:
                            if v_y2 > h_y:
                                type += "D"
                            else:
                                type += "U"
                        elif h_y == v_y2:
                            if v_y1 > h_y:
                                type += "D"
                            else:
                                type += "U"
                        if v_x == h_x1:
                            if h_x2 > v_x:
                                type += "R"
                            else:
                                type += "L"
                        elif v_x == h_x2:
                            if h_x1 > v_x:
                                type += "R"
                            else:
                                type += "L"
                        
                        intersections.append((v_x, h_y, type))



        
        return intersections



    def update_wire(self):
        components = self.asc_string.split('\n')
        y_wire_list = []
        x_wire_list = []
        for component in components:
            array = component.split(" ")
            if array[0] == "WIRE":
                if array[1] == array[3]:
                    y_wire_list.append([array[1], array[2], array[4]])
                if array[2] == array[4]:
                    x_wire_list.append([array[2], array[1], array[3]])
        

        junction_list = self.get_junctions(x_wire_list, y_wire_list)
        self.circuit.fill((0, 0, 0, 0))
        for junction in junction_list:
            wire = wire_dict[junction[2]]
            self.circuit.blit(wire, (junction[0], junction[1]))




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
    
