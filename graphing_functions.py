import numpy as np

#this function can evaluate expressions (using recursion)
def eval_exp(exp):
    #making a copy of the expression
    expression = exp
    #checking to see if there are brackets at the start and end of the expression
    if (exp[0] == '(' and exp[len(exp) - 1] == ')'):
        #if there are brackets at the start and end of the expression, get rid of them 
        #example, (3+(3+3)+3) becomes 3+(3+3)+3
        expression = exp[1:len(exp)-1]


    #the find method returns -1 if the given argument is not found.
    #for example, "helloworld".find("a") will return -1
    #the find method in other cases returns the index of the argument
    #for example, "helloworld".find("w") will return 5

    #checking if there is an open bracket in the expression
    index = expression.find('(')
    if index == -1:
        
        #checking for exponents
        index = expression.find('^')
        if index == -1:
            #checking for division
            index = expression.find('/')
            if index == -1:
                #checking for multiplication
                index = expression.find('*')
                if index == -1:
                    #checking for addition
                    index = expression.find('+')
                    if index == -1:
                        #checking for subtraction
                        index = expression.find('-')
                        if index == -1:
                            #in this case, there are no longer any symbols in the expression and therefore the number is returned.
                            return expression
                        else:
                            #checking if the expression is just a negative number
                            if expression[:index] != '':
                                #if it isn't just a negative number, subtract the left side from the right side
                                return str(float(expression[:index]) - float(expression[index + 1:]))
                            else:
                                #return the negative number.
                                return float(expression)
                    else:
                        #add the left expression to the right expression
                        return str(float(eval_exp(expression[:index])) + float(eval_exp(expression[index + 1:])))
                else:
                    #add the left expression to the right expression
                    return str(float(eval_exp(expression[:index])) * float(eval_exp(expression[index + 1:])))
            else:
                #divide the left expression by the right expression.
                return str(float(eval_exp(expression[:index])) / float(eval_exp(expression[index + 1:])))
        else:
            #raise the left expression to the right expression.
            return str(float(eval_exp(expression[:index])) ** float(eval_exp(expression[index+1:])))
    else:
        #dealing with brackets.
        #variable which stores the index for the closed bracket
        other_index = 0
        #variable that stores the number of extra brackets
        extra_brackets = 0

        #this for loop finds the correct closed bracket ')'.
        for i in range(index+1, len(expression)):
            #if the current index is an open bracket, add 1 to the extra brackets
            if expression[i] == '(':
                extra_brackets += 1
            #if the closed bracket is closing the initial open bracket, other index is set to the index of that closed bracket
            #this is found by skipping all of the closed brackets which close previous open brackets.
            #for example, let's say ((3)*(4)) is being checked
            #index for the first open bracket is 0, so index = 0 and extra_brackets = 0
            #we loop through the next characters and find ( at index 1
            #therefore extrabrackets = 1
            #then we find ) at index 3
            #therefore extrabrackets = 0
            #we find ( at index 5
            #therefore extrabrackets = 1
            #we find ) at index 7
            #therefore extrabrackets = 0
            #we find ) at index 8
            #other_index = 8, we have now found the close bracket that closes the initial open brackets.
            elif expression[i] == ')':
                if extra_brackets == 0:
                    other_index = i
                    break
                else:
                    extra_brackets -= 1

        #expression = (whatever is on the left of the brackets) + content inside the brackets + (whatever is on the right of the brackets)
        expression = expression[:index] + eval_exp(expression[index+1:other_index]) + expression[other_index+1:]
        #return expression
        return eval_exp(expression)


#generating the coordinates of the graph
def data_point_gen(exp, minimum=0, maximum=10, step=1, width=800, height=800, window_width=800, window_height=800):
    #getting rid of any spaces
    expression = exp.replace(" ", "")
    #finding the number of coordinates in the graph
    length = int((maximum - minimum) / step) + 1
    #creating the initial list array
    initial_list = np.zeros((2, length))
    for i in range(0, length):
        #generating all of the x, y coordinates for that graph
        x = minimum + i * step
        y = expression.replace("x", str(x))
        y = eval_exp(y)
        y = (float(y))
        initial_list[0][i] = x
        initial_list[1][i] = y


    #finding the minimum and maximum y coordinates for that graph
    min_y = initial_list[1].min()
    max_y = initial_list[1].max()

    #using the minimum and maximum x and y coordinates to find the correct scale for the graph
    y_scale = abs(max_y)
    if abs(min_y) > abs(max_y):
        y_scale = abs(min_y)

    x_scale = abs(maximum)
    if abs(minimum) > abs(maximum):
        x_scale = abs(minimum)

    #creating the transformation matrix that will scale every coordinate using the scale variables.
    transformation_matrix = np.array(([  
        [(width / x_scale) / 2, 0.0],
        [0.0, (height / y_scale) / -2]
        ]))
    
    #creating the translation matrix to adjust the coordinates such that they start at the correct origin
    translation_matrix = np.full((length, 2), (window_width // 2, 400))


    #perform the transformation and then the translation, then return the coordinate list.
    initial_list = np.matmul(transformation_matrix, initial_list).transpose().astype(int)
    initial_list = np.add(initial_list, translation_matrix)
    return list(map(tuple, initial_list))
