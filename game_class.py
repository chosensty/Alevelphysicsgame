import pygame
import math
from particle import Particle
from UI import Container, Button, Header
from particle_sim_functions import collision_handling
from graphing_functions import data_point_gen
class Game:
    def test(self):
        print("HELLOWORLD")
    #initialise variables for the main menu state.
    def initialise_main_menu(self):
        #change the state to main menu
        self.state = "MAINMENU"

        self.options = []
        #every text that must be rendered is added to a list
        self.texts = [
                [self.font.render("PARTICLE COLLISION SIMULATION", True, 'white'), "PARTICLE COLLISION SIMULATION"],
                [self.font.render("GRAPHS", True, 'white'), "GRAPHS"],
                [self.font.render("ELECTRICITY", True, 'white'), "ELECTRICITY"]
        ]
        for i in range(0, len(self.texts)):
            #adding the rectangle of every text that must be rendered to the list.
            self.texts[i].append(pygame.Rect(((self.window_width - self.texts[i][0].get_size()[0]) // 2, 100 + 50 * i), self.texts[i][0].get_size()))
    def __init__(self, window_width=800, window_height=800):
        #this method is called when the game object is created, it does all of the important initialising.
        pygame.init()
        self.window_width = window_width
        self.window_height = window_height
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        self.font = pygame.font.Font('utilities/cunia.ttf', 30)
        self.clock = pygame.time.Clock()

        self.running = True
        self.initialise_main_menu()

        self.ui = Container(500, 100)
        
        self.ui.add_object(Header(200, 20, "MENU", self.ui.move_ui, "#111111"))
        self.ui.add_object(Button(200, 50, "BUTTON", self.test))
        self.ui.add_object(Button(200, 50, "BUTTON2", self.test))

    def initialise_p_col_sim(self, max_speed=100, particle_number=20, particle_radius=30):
        #initialising the particle collision simulation state.
        self.state = "PARTICLE COLLISION SIMULATION"
        self.circle_list = []
        
        #initialising mouse pressed to false.
        self.mouse_pressed = False

        rows = math.ceil(math.sqrt(particle_number))

        #distributing the particles evenly around the space in order to prevent them from spawning with overlaps.
        for i in range(0, particle_number):
            x = (2 * particle_radius) + (i % rows) * math.floor(self.window_width / rows)
            y = (2 * particle_radius) + math.floor(i / rows) * math.floor(self.window_width / rows)
            self.circle_list.append(Particle(x, y, particle_radius, self.window_width, self.window_height))
        
        #the rest of the parameters are saved in case they are used later in the code.
        self.max_speed = max_speed
        self.speed = max_speed * 0.5
        self.particle_number = particle_number
        self.particle_radius = particle_radius
        self.deltaTime = 0
    #checking for a mouse click
    def mouse_click(self, rect):
        #getting the position of the mouse
        pos = pygame.mouse.get_pos()
        #returning whether the mouse overlaps with the rect given in the argument.
        return (pos[0] < rect.right and rect.left < pos[0] and rect.top < pos[1] and rect.bottom > pos[1])
    def draw_graph(self, function, width=700, height=700):
        self.state = "GRAPHS"
        self.data_list = data_point_gen(function, -10, 10, 0.25, width, height, self.window_width, self.window_height)
        self.screen.fill("BLACK")
        pygame.draw.lines(self.screen, 'green', False, self.data_list)
        pygame.draw.line(self.screen, 'white', ((self.window_width - width) // 2, self.window_height // 2), ((self.window_width + width) // 2, self.window_height // 2))
        pygame.draw.line(self.screen, 'white', (self.window_width // 2, (self.window_height - height) // 2), (self.window_width // 2, (self.window_height + height) // 2))
    def main(self):
        #this is the game loop.
        while self.running:
            #if the game is in the main menu state.
            if self.state == "MAINMENU":
                #create a black background
                self.screen.fill("BLACK")
                #blitting all of the texts to the screen.
                for i in range(0, len(self.texts)):
                    self.screen.blit(self.texts[i][0], self.texts[i][2])
                #looping through the events
                for event in pygame.event.get():
                    #if event type is quit, exit the program.
                    if event.type == pygame.QUIT:
                        self.running = False
                        exit()
                    #if event type was mouse click.
                    if event.type == pygame.MOUSEBUTTONDOWN and not self.mouse_click(pygame.Rect((self.ui.x, self.ui.y), self.ui.container.get_size())):
                        #checking if any of the texts for the main menu were clicked.
                        for i in range(0, len(self.texts)):
                            #if any of the texts are clicked, the 
                            if (self.mouse_click(self.texts[i][2])):
                                if self.texts[i][1] == "PARTICLE COLLISION SIMULATION":
                                    self.initialise_p_col_sim()
                                    break
                                if self.texts[i][1] == "GRAPHS":
                                    self.draw_graph("5*x^2")
                                    break
                                if self.texts[i][1] == "ELECTRICITY":
                                    self.state = "ELECTRICITY"
                                    self.circuit_length = 1000
                                    self.circuit_width = 50
                                    self.particle_position = 0
                                    break
                                    
            #if the state is particle collision simulation 
            if self.state == "PARTICLE COLLISION SIMULATION":        
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                        #checking if the mouse is clicked.
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pass

                #looping through the particles and moving them one by one.
                for i in range(0, self.particle_number):
                    self.circle_list[i].move(self.deltaTime, self.speed)

                #calling the collision handling function
                collision_handling(self.deltaTime, self.circle_list)
                
                #Setting the screen to black.
                self.screen.fill("black")

                #looping through the particles and drawing them to the screne.
                for i in range(0, self.particle_number):
                    pygame.draw.circle(self.screen, 'red', (self.circle_list[i].x, self.circle_list[i].y), self.circle_list[i].radius)
                

                

                #moving on to the next frame.
                self.deltaTime = self.clock.tick(60) / 1000


            #if the state is graphs.
            if self.state == "GRAPHS":
                for event in pygame.event.get():
                    #check if the game is being quit, if it is, exit the game.
                    if event.type == pygame.QUIT:
                        self.running = False
                        exit()
            #if the state is electricity.
            if self.state == "ELECTRICITY":
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                        exit()

                #setting the background to solid black.
                self.screen.fill("BLACK")

                #moving the particle position forward.
                self.particle_position += 1
                if self.particle_position >= self.circuit_width:
                    #ensuring that the particle position remains within appropriate range
                    #(0 <= particle position < circuit width)
                    self.particle_position = 0
                #finding the number of particles per row.
                particles_per_row = (self.circuit_length // self.circuit_width) // 4
                #calculating the radius of the particle
                radius = self.circuit_width // 2
                #calculating the width of each wire in the circuit
                width = self.circuit_length // 4
                #finding the top left coordinates
                top_left = (self.window_width // 2 - (width // 2) - (radius), self.window_height // 2 - width // 2 - radius)

                #this for loop displays the circles which represent the current in the circuit (this is only here temporarily for testing purposes).
                for i in range(0, self.circuit_length // self.circuit_width):
                    offset = ((i%particles_per_row) * self.circuit_width)
                    if i >= 0 and i < particles_per_row:
                        x, y  = (math.floor(top_left[0] + radius + self.particle_position + offset), math.floor(top_left[1] + self.circuit_width // 2))
                    elif i>=particles_per_row and i<particles_per_row * 2:
                        x, y= (math.floor(top_left[0] + radius + width), math.floor(top_left[1] + self.particle_position + radius + offset))
                    elif i>=particles_per_row * 2 and i< particles_per_row * 3:
                        x, y = (math.floor(top_left[0] + width + radius - self.particle_position - offset), math.floor(top_left[1] + radius + width))
                    elif i>=particles_per_row * 3 and i< particles_per_row * 4:
                        x, y = (math.floor(top_left[0] + radius), math.floor(top_left[1] - self.particle_position + width + radius - offset))
                    pygame.draw.circle(self.screen, 'yellow', (x, y), self.circuit_width // 2)
                self.clock.tick(10)
                
            pos = pygame.mouse.get_pos()
            self.ui.update(pos, pygame.mouse.get_pressed()[0])

            self.screen.blit(self.ui.container, (self.ui.x, self.ui.y))
            pygame.display.flip()

game = Game()
game.main()