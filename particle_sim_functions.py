import math

#finding the magnitude of a 2D vector.
def magnitude_squared(vector):
    magnitude = vector[0] ** 2 + vector[1] ** 2
    return magnitude

#calculating the velocities of two particles which have just collided.
def calculate_velocities(c1, c2, t):

    mp1 = [c1.x + c1.radius, c1.y + c1.radius]
    mp2 = [c2.x + c2.radius, c2.y + c2.radius]

    n = [mp2[0] - mp1[0], mp2[1] - mp1[1]]

    magn_sqrd = magnitude_squared(n)

    diff_v1 = [c1.x_vel - c2.x_vel, c1.y_vel - c2.y_vel]
    diff_mp1 = [mp1[0] - mp2[0], mp1[1] - mp2[1]]
    
    diff_v2 = [c2.x_vel - c1.x_vel, c2.y_vel - c1.y_vel]
    diff_mp2 = [mp2[0] - mp1[0], mp2[1] - mp1[1]]


    dot_prod1 = diff_v1[0] * diff_mp1[0] + diff_v1[1] * diff_mp1[1];
    dot_prod2 = diff_v2[0] * diff_mp2[0] + diff_v2[1] * diff_mp2[1];

    c1.x_vel -= (((2 * c2.mass) * dot_prod1 * diff_mp1[0] )/((c1.mass + c2.mass) * magn_sqrd));
    c1.y_vel -= (((2 * c2.mass) * dot_prod1 * diff_mp1[1] )  / ((c1.mass + c2.mass) * magn_sqrd));
    
    
    c2.x_vel -= (((2 * c1.mass) * dot_prod2 * diff_mp2[0] )/((c1.mass + c2.mass) * magn_sqrd));
    c2.y_vel -= (((2 * c1.mass) * dot_prod2 * diff_mp2[1] )  / ((c1.mass + c2.mass) * magn_sqrd));
    
    c1.move(t, 1)
    c2.move(t, 1)


#finding the negative solution to a quadratic formula.
def quadratic_formula_negative(a, b, c):
    result = (-b + math.sqrt(b**2 - 4 * a * c))/(2*a)
    return result

#finding the time at which a collision occured, then putting the particles back to that time period.
def time_of_collision(c1, c2):
    mp1x = c1.x + c1.radius
    mp1y = c1.y + c1.radius
    mp2x = c2.x + c2.radius
    mp2y = c2.y + c2.radius    
    s_x = mp2x - mp1x
    s_y = mp2y - mp1y
    v_x = c2.x_vel - c1.x_vel
    v_y  = c2.y_vel - c1.y_vel    
    a = v_x * v_x + v_y * v_y
    b = -2 * (s_x * v_x + s_y * v_y)
    c = s_x * s_x + s_y * s_y - math.pow((c1.radius + c2.radius), 2)
    t = quadratic_formula_negative(a, b, c)
    #  putting the particles back in time using the time of collision value.
    c1.move(t, 1, -1)
    c2.move(t, 1, -1)
    # return the time at which the collision occured.  
    return t

def collision_handling(dt, p_list):

    #sorting the particles. (using quick sort)
    for i in range(1, len(p_list)):
        insert_val = p_list[i]
        free_pos = i

        while(free_pos > 0 and p_list[free_pos - 1].x > insert_val.x):
            p_list[free_pos] = p_list[free_pos - 1]
            free_pos -= 1
        p_list[free_pos] = insert_val

    i = 0
    y = 1
    #using the sweep and prune algorithm to check for collisions
    while (i < len(p_list)- y):
        if ((p_list[i].x +p_list[i].radius) > p_list[i + y].x -p_list[i + y].radius):
            distance = math.sqrt((p_list[i].x + p_list[i].radius - (p_list[i + y].x + p_list[i + y].radius)) ** 2 + (p_list[i + y].y + p_list[i + y].radius - (p_list[i].y + p_list[i].radius)) ** 2)
            if (distance < p_list[i].radius + p_list[i + y].radius):
                #if a collision has occured, put the particles back in time to the exact time of the collisions
                t = time_of_collision(p_list[i], p_list[i + y])
                #perform collision calculations then put the particle forward in time (back to the present)
                calculate_velocities(p_list[i], p_list[i + y], t)
                i += 1
                y = 1
            else:
                y += 1
                if (i + y == len(p_list)):
                    y = 1
                    i += 1
        else:
            i += 1
            y = 1
    

