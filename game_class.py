import pygame
import math
from particle import Particle
from UI import Container, Button, Header, Slider
from particle_sim_functions import collision_handling
from graphing_functions import data_point_gen
from electricity import Electricity

class Game:

    def test(self):
        print("HELLOWORLD")

    #initialise variables for the main menu state.
    def initialise_main_menu(self):

        #change the state to main menu
        self.state = "MAINMENU"
        #creating the UI object then adding each button to it
        #adding the header with width 200 and height 20
        self.ui.reset()
        self.ui.add_object(Header(200, 30, "MENU", self.ui.move_ui, "H","#111111"))
        #adding a button with width 200 and height 50
        self.ui.add_object(Button(200, 50, "BUTTON", self.test, "B1"))
        self.ui.add_object(Button(200, 50, "BUTTON2", self.test, "B2"))

        self.options = []
        #every text that must be rendered is added to a list
        self.texts = [
                [self.font.render("PARTICLE COLLISION SIMULATION", True, 'white'), "PARTICLE COLLISION SIMULATION"],
                [self.font.render("GRAPHS", True, 'white'), "GRAPHS"],
                [self.font.render("ELECTRICITY", True, 'white'), "ELECTRICITY"],
                [self.font.render("MOMENTS", True, 'white'), "MOMENTS"],
        ]
        for i in range(0, len(self.texts)):
            #adding the rectangle of every text that must be rendered to the list.
            self.texts[i].append(pygame.Rect(((self.window_width - self.texts[i][0].get_size()[0]) // 2, 100 + 50 * i), self.texts[i][0].get_size()))

    def __init__(self, window_width=800, window_height=800):

        #this method is called when the game object is created, it does all of the important initialising.
        pygame.init()

        self.ui = Container(500, 100)
        #setting the window width and window height
        self.window_width = window_width
        self.window_height = window_height

        #creating the screen object.
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))

        #loading the font that will be used.
        self.font = pygame.font.Font('utilities/cunia.ttf', 30)
        #creating the clock object
        self.clock = pygame.time.Clock()

        self.running = True
        #initialise for the main menu.
        self.initialise_main_menu()

    def initialise_p_col_sim(self, max_speed=100, particle_number=10, particle_radius=30):
        #initialising the particle collision simulation state.
        self.state = "PARTICLE COLLISION SIMULATION"
        self.ui.reset()
        self.ui.add_object(Header(200, 30, "Collision Sim", self.ui.move_ui,"H", "#111111"))
        self.ui.add_object(Slider("speed", 200, 25))
        self.ui.add_object(Button(200, 20, "Back", self.initialise_main_menu, "B", "#ff4848"))
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
        #drawing the graph.
        self.state = "GRAPHS"
        container = data_point_gen(function, -3, 3, 0.25, width, height)
        self.screen.fill("BLACK")
        w, h = container.get_size()
        self.screen.blit(container, ((self.window_width - w) // 2, (self.window_height - h) // 2))

    def initialise_e_sim(self):
        #initialising electricity simulator.
        self.state = "ELECTRICITY"
        self.electricity = Electricity()

        #initialising the UI with sliders for x, y coordinates to select squares, and options to add components.
        self.ui.reset()
        self.ui.add_object(Header(200, 30, "Electric Simulator", self.ui.move_ui, "H", "#111111"))
        self.ui.add_object(Slider("x",200, 25))
        self.ui.add_object(Slider("y",200, 25))
        self.ui.add_object(Button(200, 25, "TOGGLE WIRE", self.electricity.toggle_wire, "TOGGLE_WIRE", "#000088"))
        self.ui.add_object(Button(200, 25, "Add Resistor", self.electricity.add_resistor, "RES"))
        self.ui.add_object(Button(200, 25, "INSERT COMPONENT", self.electricity.insert_component, "INSERT"))
        self.ui.add_object(Button(200, 25, "Rotate", self.electricity.change_orientation, "ROTATE"))
        self.ui.add_object(Button(200, 20, "Back", self.initialise_main_menu, "B2", "#ff4848"))

    def main(self):
        #this is the game loop.
        while self.running:
            #create a black background
            self.screen.fill("BLACK")
            #if the game is in the main menu state.
            if self.state == "MAINMENU":
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
                                    self.draw_graph(str(math.e)+"^x")
                                    break
                                if self.texts[i][1] == "ELECTRICITY":
                                    self.initialise_e_sim()
                                    break
                                if self.texts[i][1] == "MOMENTS":
                                    self.state = "MOMENTS"
                                    self.initialise_moments()
                                    
            #if the state is particle collision simulation 
            if self.state == "PARTICLE COLLISION SIMULATION":        
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                        #checking if the mouse is clicked.
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pass

                self.speed = self.ui.query("speed") * self.max_speed
                #looping through the particles and moving them one by one.
                for i in range(0, self.particle_number):
                    self.circle_list[i].move(self.deltaTime, self.speed)

                #calling the collision handling function
                collision_handling(self.deltaTime, self.circle_list)
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
            if self.state == "MOMENTS":
                pass
            #if the state is electricity.
            if self.state == "ELECTRICITY":
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                        exit()
            
                #updating the current location of the cursor which is based on the sliders.
                x = self.ui.query("x") * self.window_width
                y = self.ui.query("y") * self.window_height
                self.electricity.update_outline(x, y, True)
                
                #refreshing the canvas
                self.electricity.update_container()

                #putting the canvas on the main screen.
                self.screen.blit(self.electricity.canvas, (0, 0))
                self.clock.tick(60)
            
            if self.state == "MOMENTS":

                #currently unfinished
                dt = self.clock.tick(60)
                self.moments_object.run_physics(dt)
                self.screen.blit(self.moments_object.window, (0, 0))
       
            
            #updating the UI.
            pos = pygame.mouse.get_pos()
            self.ui.update(pos, pygame.mouse.get_pressed()[0])

            
            self.screen.blit(self.ui.container, (self.ui.x, self.ui.y))
            pygame.display.flip()

game = Game()
game.main()
