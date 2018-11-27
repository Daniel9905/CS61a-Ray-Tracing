
from turtle import *
from tkinter import *
from math import sin, sqrt

# print(Screen().screensize())
print(Screen().screensize())
canvas = getcanvas()
width = canvas.winfo_width()
height = canvas.winfo_height()
print(width, height)
image = PhotoImage(width = width, height = height)
canvas.create_image((0, 0), image = image, state = "normal")
bgcolor("#000000")

def pixel(position, color):
    '''
    draw a pixel with POS and COLOR
    POSITION: a tuple of x and y
    COLOR: a triple of num from 0 to 1 (RGB)
    '''
    x, y = position
    right, down = x, height - y
    position = (right, down)
    rgb_to_hex_scaled = tuple(int(i * 255) for i in color)
    color = "#%02x%02x%02x" % rgb_to_hex_scaled
    image.put(color, position)

def pixel_block(position, color, size):
    x, y = position
    for dx in range(size):
        for dy in range(size):
            pixel((x + dx, y + dy), color)

def add(a, b):
    '''
    Adding two points in 3D space
    '''
    return a[0] + b[0], a[1] + b[1], a[2] + b[2]

def substract(a, b):
    return a[0] - b[0], a[1] - b[1], a[2] - b[2]

def dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]

def scale(a, k):
    '''Transform the vector A to the scale of K'''
    return k * a[0], k * a[1], k * a[2]

def normalize(a):
    '''Get the unit vector of A'''
    magnitutde = sqrt(dot(a, a))
    return scale(a, 1/magnitutde)

def length(a):
    '''Get the length of vector A'''
    return sqrt(dot(a, a))

#Color
black = (0, 0, 0)
white = (1, 1, 1)

red = (1, 0, 0)
green = (0, 1, 0)
blue = (0, 0, 1)
yellow = (1, 1, 0)
teal = (0, 0.63, 0.63)
orange = (1, 0.39, 0)
orange_red = (1, 0.27, 0)
light_blue = (0, 0.8, 1)
light_green = (0.31, 1, 0.31)

#Scene
origin = (0, 0, 0)
camera = (0, 1, 0)
light = (2, 2, 0)
black = (0, 0, 0)
ambient = 0.2
sphere = (1, (0, 1, 3), light_blue) # radius, position, color
spheres = [
    (100, (0, -100, 0), (1, 1, 0)),
    (1,   (0,    0, 3), orange), # Red sphere
    (1,   (-2,   1, 4), light_green), # Green sphere
    (1,   (2,    1, 4), light_blue) # Blue sphere
]

# Render the image
def render():
    '''Paint the image'''
    block = 1
    new_width, new_height = width//block, height//block
    size = min(new_width, new_height)
    for x in range(size):
        for y in range(size):
            direction = normalize((x/size - 0.5, y/size - 0.5, 1)) #scale it down to [0,1] range and remap so that (0,0) is in the center
            color = scale(ray_trace(camera, direction, 0, float('inf')), 0.95)
            pixel_block((x*block, y*block), color, block)

def canvasToViewport(position):
    x, y = position
    return (x, y)

def ray_trace(camera, direction, min_t, max_t):
    '''Return the color of each pixel'''
    distances = [intersect(camera, direction, sphere) for sphere in spheres]
    hits = [(d, s) for d, s in zip(distances, spheres) if d] #filter out the spheres not in the line of sight
    if not hits: #no sphere in the line of sight
        return black
    distance, new_sphere = min(hits)
    _, center, color = new_sphere
    surface = add(camera, scale(direction, distance))
    return illumimnation(surface, center, color)

def illumimnation(surface, center, color):
    '''Return the color given the angle of light and surface'''
    surface_normal = normalize(substract(surface, center))
    surface_to_light = normalize(substract(light, surface))
    intensity = max(ambient, dot(surface_normal, surface_to_light))
    return scale(color, intensity)

def intersect(camera, direction, sphere):
    '''Return the distance of a point on a sphere'''
    radius, center, color = sphere
    v = substract(camera, center)
    a = dot(direction, direction)
    b = dot(direction, v)
    c = dot(v, v) - radius * radius
    delta_square = b*b - c
    if delta_square < 0:
        return None
    elif delta_square >= 0:
        t1 = (-b - sqrt(delta_square))/length(direction)
        t2 = (-b + sqrt(delta_square))/length(direction)
        for t in (t1, t2):
            if t>0:
                return t
    

render()
exitonclick()