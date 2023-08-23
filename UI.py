import pygame
import math

#container class
class Container:
    #function that moves the ui when the move clicks the header.
    def move_ui(self, bool, rel_pos):
        self.move_bool = bool
        if bool:
            self.offset = tuple(rel_pos)
    #function 
    def set_height(self):
        self.height = 0
        for object in self.objects:
            object.set_height()
            self.height += object.height()
        if self.height != self.container.get_size()[1]:
            self.container = pygame.Surface((self.width, self.height))
        return self.height
        
    def update_container(self):
        y = 0
        self.container.fill(self.bg_color)
        for i in range(0, len(self.objects)):
            object = self.objects[i]
            object.update_container()
            self.container.blit(object.container, (0, y))
            object.set_height()
            y += object.height
    def boundary_check(self):
        if self.x < 0:
            self.x = 0
        if self.x > self.w_w - self.width:
            self.x = self.w_w - self.width
        if self.y < 0:
            self.y = 0
        if self.y > self.w_h - self.height:
            self.y = self.w_h - self.height
    def add_object(self, object):
        self.objects.append(object)
        object.set_height()
        self.height += object.height
        self.container = pygame.Surface((self.width, self.height))
    def update(self, mouse_cords, mouse_state):
        if self.move_bool:
            self.x, self.y = mouse_cords[0] - self.offset[0], mouse_cords[1] - self.offset[1]
            self.boundary_check()
        
        rel_mouse_cords = [mouse_cords[0] - self.x, mouse_cords[1] - self.y]
        
        y = 0
        for i in range(0, len(self.objects)):
            rel_mouse_cords[1] = mouse_cords[1] - self.y - y
            object = self.objects[i]
            object.update(rel_mouse_cords, mouse_state)
            object.set_height()
            y += object.height
        self.update_container()

        
    def __init__(self, init_x, init_y, window_width=800, window_height=800, width = 200, bg_color="#111111", button_color="#282828", text_color="#ffffff"):
        self.x = init_x
        self.y = init_y
        self.offset = [0, 0]
        self.visible = True
        self.objects = []
        self.w_w = window_width
        self.w_h = window_height
        self.bg_color = "#111111"
        self.button_color = "#282828"
        self.text_color = "#ffffff"
        self.move_bool = False
        self.height = 0
        self.width = width

#container class
class Button(Container):
    def set_height(self):
        return self.height
    def __init__(self, width, height, string, command, bg_color="#282828", text_color="#ffffff", border_color="#ffffff"):
        self.bg_color = bg_color
        self.width = width
        self.height = height
        self.function = command
        self.container = pygame.Surface((width, height))
        self.outline = pygame.Rect((0, 0, width, height))
        self.font = pygame.font.Font('utilities/cunia.ttf', 16)
        self.text = self.font.render(string, True, text_color)
        self.text_coords = ((width - self.text.get_size()[0])// 2, (height - self.text.get_size()[1]) // 2)
        self.border_color = border_color
        self.string = string
        self.visible = True
        self.state = "inactive"

    def update_container(self):
        self.container.fill(self.bg_color)
        self.container.blit(self.text, self.text_coords)
        if self.state == "active":
            pygame.draw.rect(self.container, "#00ff00", (0, 0, self.width, self.height), 2)
        elif self.state == "hover":
            pygame.draw.rect(self.container, self.border_color, (0, 0, self.width, self.height), 2)
        elif self.state == "inactive":
            pass
    
    def update(self, rel_mouse_cords, mouse_state):
        x, y = rel_mouse_cords
        if x > 0 and x < self.width and y > 0 and y < self.height:
            if mouse_state:
                if self.state != "active":
                    self.function()
                self.state = "active"
            else:
                self.state = "hover"
        else:
            self.state = "inactive"

class Header(Button):
    def update(self, rel_mouse_cords, mouse_state):
        x, y = rel_mouse_cords
        if x > 0 and x < self.width and y > 0 and y < self.height:
            if mouse_state:
                self.state = "active"
                self.function(True, rel_mouse_cords)
            else:
                if self.state == "active":
                    self.function(False, rel_mouse_cords)
                self.state = "hover"
        else:
            self.state = "inactive"
            self.function(False, rel_mouse_cords)
'''
class Option:
    def update_state(self, rel_pos, mouse_state):
        x = rel_pos[0]
        y = rel_pos[1]
        if x < self.width and x > 0 and y > 0 and y < self.height:
            if mouse_state:
                self.state = "active"
                self.function(True, rel_pos)
            else:
                self.state = "hover"
        else:
            self.function(False, rel_pos)
            self.state = "inactive"
        return -1

    def update(self):
        self.container.fill(self.bg_color)
        self.container.blit(self.text, self.text_coords)
        if self.state == "active":
            pygame.draw.rect(self.container, "#00ff00", (0, 0, self.width, self.height), 2)
        elif self.state == "hover":
            pygame.draw.rect(self.container, self.border_color, (0, 0, self.width, self.height), 2)

    def __init__(self, width, height, string, command, index, bg_color="#282828", text_color="#ffffff", border_color="#ffffff"):
        self.bg_color = bg_color
        self.index = index
        self.width = width
        self.height = height
        self.function = command
        self.container = pygame.Surface((width, height))
        self.outline = pygame.Rect((0, 0, width, height))
        self.font = pygame.font.Font('utilities/cunia.ttf', 16)
        self.text = self.font.render(string, True, text_color)
        self.text_coords = ((width - self.text.get_size()[0])// 2, (height - self.text.get_size()[1]) // 2)
        self.border_color = border_color
        self.string = string
        self.state = "inactive"

class Header(Option):
    def update(self, rel_pos, mouse_state):
            x = rel_pos[0]
            y = rel_pos[1]
            if x < self.width and x > 0 and y > 0 and y < self.height:
                if mouse_state:
                    self.state = "active"
                    self.function(True, rel_pos)
                    return self.index
                else:
                    self.state = "hover"
            else:
                self.function(False, rel_pos)
                self.state = "inactive"
            return -1
'''
#slider class
class Slider:
    #called upon initialising
    def __init__(self, x, y, width=240, height=40, bg_color="white", slider_color="green"):
        #creating a background rectangle
        self.backgroundRect = pygame.Rect(x, y, width, height)
        #creating the rect for the slider
        self.sliderRect = pygame.Rect(x + (width - math.floor(height * 0.8)) // 2, y + math.floor(height * 0.1), math.floor(height * 0.8), math.floor(height * 0.8))
        #setting the slider color
        self.slider_color= slider_color
        #setting the background color
        self.bg_color= bg_color
        #initialising active at false
        self.active = False
        self.container = pygame.Surface((width, height))
        self.slider_surface = pygame.Surface((height, height))
    #this method returns the percentage of the slider
    #example:
    '''
    |---------------------------------------|
    |                                       |
    |               |-------|               |   
    |               |-------|               |
    |               |-------|               |           
    |                                       |
    |---------------------------------------|
    '''
    #is around 50% because the slider is at the middle.

    def get_percentage(self):
        percentage = (self.sliderRect.center[0] - self.backgroundRect.left - math.floor(self.sliderRect.width * 0.6)) / (self.backgroundRect.width - math.floor(self.sliderRect.width * 1.2))
        return percentage
    #changes the slider position to a specific percentage.
    def set_percentage(self, percentage):
        self.sliderRect.left = math.floor(percentage * (self.backgroundRect.width - math.floor(self.sliderRect.width * 1.2))) + math.floor(self.sliderRect.width * 0.1) + self.backgroundRect.left
    #get the information regarding the background (color and rect)
    #get the information of the slider (color and rect)
    def get_slider(self):
        return self.slider_color, self.sliderRect
    def get_slider_rect(self):
        return self.sliderRect
    def update(self):
        self.container.fill(self.bg_color)
        self.container.blit(self.slider_surface, ())
    #make the slider active.
    def make_active(self, mouseX):
        #making the slider active.
        self.active = True
        #noting where the slider position was at the begin of the slide.
        self.initial_pos = self.sliderRect.left
        #noting where the mouse position was at the begin of the slider.
        self.mouse_pos = mouseX
    #method which returns the state of the slider.
    def isActive(self):
        return self.active
    def slide(self, mouseX):
        #checking if the slider is active.
        if (self.active):
            #setting the x coordinate of the slider to the initial position of the slider + the distance that the mouse has travelled
            #that distance is calculated by subtracting the current mouse x coordinate but the old x coordinate.
            self.sliderRect.left = self.initial_pos + (mouseX - self.mouse_pos)
            #if the percentage is above 1, set it to 1. if the percentage is below 0, set it to 0.
            if self.get_percentage() > 1:
                self.set_percentage(1)
            elif self.get_percentage() < 0:
                self.set_percentage(0)

    #method that makes the slider inactive.

    def make_inactive(self):
        self.active = False