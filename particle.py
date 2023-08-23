import random

#class for an individual particle.
class Particle:
    #initialising basic data.
    def __init__(self, x, y, radius, window_width, window_height):
        self.x = x
        self.y = y
        self.radius = radius
        self.mass = 1
        self.x_vel = random.uniform(-1, 1)
        self.y_vel = random.uniform(-1, 1)
        self.w_w = window_width
        self.w_h = window_height
    def move(self, dt, speed, direction=1):
        #adding to the x and y coordinate using the velocities.
        self.x += self.x_vel * dt * speed * direction
        self.y += self.y_vel * dt * speed * direction

        #ensuring that the x and y coordinates remain within the correct boundaries.
        #if they go outside those boundaries, correct the x and y coordinates and reverse their velocity variables.
        if (self.x - self.radius < 0):
            self.x = self.radius * 2 - self.x
            self.x_vel *= -1
        if (self.y - self.radius < 0):
            self.y = self.radius * 2 - self.y
            self.y_vel *= -1
        if (self.x + self.radius >= self.w_w):
            self.x = 2 * self.w_w - (self.x + self.radius * 2)
            self.x_vel *= -1
        if (self.y + self.radius >= self.w_h):
            self.y = 2 * self.w_h - (self.y + self.radius * 2)
            self.y_vel *= -1