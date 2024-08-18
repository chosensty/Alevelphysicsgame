import pymunk
import pygame
import pymunk.pygame_util

class Moments:
    def __init__(self, width, height):
        self.WIDTH, self.HEIGHT = width, height
        self.window = pygame.Surface((self.WIDTH, self.HEIGHT))

    # #game state
    # game_state = "menu"

    # def draw_text(text, font, text_col, x, y):
    #      img = font.render(text, True, text_col)
    #      window.blit(img, (x, y))



    def draw(self, space, draw_options):
        self.window.fill("white")
        space.debug_draw(draw_options)

    # def create_box(space, size, mass):
    #      body = pymunk.Body()
    #      body.posistion = (,300)
    #      shape = pymunk.Poly.create_box(body, size, radius=2)
    #      shape.mass = mass
    #      shape.color = (0, 255, 0, 100) #rgb a, a is opacity
    #      space.add(body, shape)
    #      return shape

    def create_ball(self, space, radius, mass, position):
        self.body = pymunk.Body()
        self.body.position = position
        shape = pymunk.Circle(self.body, radius)
        shape.mass = mass
        shape.color = (255, 0, 0, 100)  # rgb alpha values hence 4 fields where alpha is the opacity/ transparency (100 is opaque af)
        shape.friction = 10
        space.add(self.body, self.shape)



    def create_seesaw(self, space):
        rotation_center_body =pymunk.Body(body_type=pymunk.Body.STATIC)
        rotation_center_body.position = (500, 97)
        
        body = pymunk.Body()
        body.position = (500, 97)

        # left_rect = pymunk.Poly.create_box(body, (30,20))
        # left_rect.friction = 1
        # left_rect.elasticity = 0.95
        # left_rect.mass = 100 



        rect = pymunk.Poly.create_box(body, (700,30))
        rect.friction = 1
        rect.elasticity= 0.95
        rect.mass = 300

    

        # # container = pymunk.Poly(body, vertices=[
        # #      (150, 82),
        # #      (150, 152),
        # #      (180, 152),
        # #      (180, 112),
        # #      (850, 82),
        # #      (850, 152),
        # #      (830, 152),
        # #      (830, 112)      
        # # ])
        # container.friction = 1
        # container.elasticity = 0.95
        # container.mass = 300

        circle = pymunk.Circle(body, 10, (0, 0))
        circle.friction = 1
        circle.mass = 50

        rotation_center_joint = pymunk.PinJoint(body, rotation_center_body, (0,0), (0,0))
        
        triangle = pymunk.Poly(space.static_body, [(self.WIDTH/2 -20, 20 ),(self.WIDTH/2 + 20, 20 ), (self.WIDTH /2, 80) ])

        space.add(rect, circle, body, rotation_center_joint, triangle)

    def create_boundaries(self, space, width, height):
        rects = [
            [(width/2, height - 10), (width, 20)],
            [(width / 2, 10), (width, 20)],
            [(10, height/2), (20, height)],
            [(width - 10, height / 2), (20, height)]
        ]
        for pos, size in rects:
            body = pymunk.Body(body_type=pymunk.Body.STATIC)
            body.position = pos
            shape = pymunk.Poly.create_box(body, size)
            shape.elasticity = 0.4
            shape.friction = 0.5
            space.add(body, shape)

    def load_physics(self):
        space = pymunk.Space()
        space.gravity = (0,-981)  #x and y gravity

        self.draw_options = pymunk.pygame_util.DrawOptions(self.window)

        #box = create_box(space,size=(100,100), mass=100)
        #create_ball(space, 30, 10, (200, 200))
        #create_ball(space, 30, 10, (800, 200))
        self.create_boundaries(space, self.WIDTH, self.HEIGHT)
        self.create_seesaw(space)

    def run_physics(self, dt):
        self.draw(self.space, self.window, self.draw_options)
        self.space.step(dt)       
        return self.window
