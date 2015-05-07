__author__ = 'Wangj1'
# Written by Junlin Wang

'''
a = '85'
iteration = 10000
b = 0
for i in range(iteration):
    for j in a:
        b = b + int(j)**2
    a = str(b)
    b = 0
    print a
'''
# Logistic Map
# f(x) = R * X * (1 -X)
# 0 <= R <= 4
# 0 <= X <= 1

# when r is less than 1 greater than 0, it converges to fixed point 0
# when r is between 1 and 3, it converges to r-1/r: stable attractive fixed point
# when r is greater than 3, unstable fixed point.

r = 3.1
x = 0.3
iteration = 1000
def logisticmap(x, r, iteration):
    orbit = []
    for i in range(iteration):
        sum = r * x *(1-x)
        x = sum
        orbit.append(sum)
        print x
    return orbit
orbit = logisticmap(x, r, iteration)
# r = 2 is the transition for the slope to get from positive to negative

# f(f(x)) - x
# roots:x, x - (R-1)/R

# derivative of f(f(x))
d = r**2 - 2 * r**3 * x + 6 * r**3 * x**2 - 2 * r**2 * x - 4 * r**3 * x**3
