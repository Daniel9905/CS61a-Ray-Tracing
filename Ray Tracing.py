
from turtle import *
from tkinter import *
from math import sin, sqrt, cos, pi


canvas = getcanvas()
width = canvas.winfo_width()
height = canvas.winfo_height()
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
    Adding two vectors in 3D space
    '''
    return a[0] + b[0], a[1] + b[1], a[2] + b[2]

def substract(a, b):
    '''Substracting two vectors in 3D space'''
    return a[0] - b[0], a[1] - b[1], a[2] - b[2]

def dot(a, b):
    '''Dot product of two vectors'''
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
color = {
    'black': (0, 0, 0),
    'white': (1, 1, 1),
    'red' : (1, 0, 0),
    'green' : (0, 1, 0),
    'blue' : (0, 0, 1),
    'yellow' : (1, 1, 0),
    'teal' : (0, 0.63, 0.63),
    'orange' : (1, 0.39, 0),
    'orange_red' : (1, 0.27, 0),
    'light_blue' : (0, 0.8, 1),
    'light_green' : (0.31, 1, 0.31),
    'violet' : (0.93, 0.51, 0.93),
    'table_brown' : (0.57, 0.43, 0.24),
}

def bright_color(amount):
    global brighten_color
    brighten_color = { 'black': (0, 0, 0), 'white': (1, 1, 1)}
    for i in list(color.keys())[2:]:
        x, y, z = color[i]
        # r = 1 + cos((x + y + z)*pi/6)
        brighten_color[i] = tuple(min(i*(1-amount) + amount, 1) for i in color[i])

def color_palette():

    def new_line():
        nonlocal pos_x, pos_y, size
        pos_x, pos_y = 0, pos_y + size  
    def check_EOF():
        nonlocal pos_x
        if pos_x > width:
            new_line()
        else:
            pos_x += size

    pos_x, pos_y = 0, 0
    size = 50
    for key in color:
        pixel_block((pos_x, pos_y), color[key], size)
        check_EOF()
    new_line()
    for key in brighten_color:
        pixel_block((pos_x, pos_y), brighten_color[key], size)
        check_EOF()


bright_color(0.2)
# color_palette()
# use brighten_color sets
color = brighten_color


black = color['black']
white = color['white']
red = color['red']
green = color['green']
blue = color['blue']
yellow = color['yellow']
teal = color['teal']
orange = color['orange']
orange_red = color['orange_red']
light_blue = color['light_blue']
light_green = color['light_green']
violet = color['violet']
table_brown = color['table_brown']



#Scene
scene = {
    'origin' : (0, 0, 0),
    'light' : (2, 2, 0),
}

camera = (0, 1, 0)
origin = scene['origin']
light = scene['light']
ambient = 0.2
spheres = [
    (500, (0, -500, 0), table_brown), # radius, position, color
    (2, (0,    2,  10), orange), 
    (0.8, (-1, 1, 3**0.5 + 3), light_green),
    (1, (-2, 1, 2 * 3**0.5 + 3), red),
    (0.8, (1, 1, 3**0.5 + 3), light_blue),
    (1, (2, 1, 2 * 3**0.5 + 3), violet),
]

# rotate the scene
def rotation_yzplane(pos, angle):
    x, y, z = pos
    y, z = cos(angle) * y - sin(angle) * z, sin(angle) * y + cos(angle) * z 
    return (x, y, z)

def rotation_xzplane(pos, angle):
    x, y, z = pos
    x, z = cos(angle) * x - sin(angle) * z, sin(angle) * x + cos(angle) * z 
    return (x, y, z)

def rotate_scene():
    for setup in scene:
        scene[setup] = rotation_yzplane(scene[setup], -pi/6)
    for index in range(len(spheres)):
        center, pos, color = spheres[index]
        spheres[index] = center, rotation_yzplane(pos, -pi/6), color

rotate_scene()

def adjust_camera(x, y, z):
    global camera
    camera = camera[0] + x, camera[1] + y, camera[2] + z

adjust_camera(0, 4, 0)


# Render the image
def render():
    '''Paint the image'''
    block = 1
    new_width, new_height = width//block, height//block
    size = min(new_width, new_height)
    for x in range(size):
        for y in range(size):
            direction = normalize((x/size - 0.5, y/size - 0.5, 1)) #scale it down to [0,1] range and remap so that (0,0) is in the center
            color = scale(ray_trace(camera, direction), 1)
            pixel_block((x*block, y*block), color, block)

# def canvasToViewport(position):
#     x, y = position
#     return (x, y)

def ray_trace(source, direction, depth = 2):
    '''Return the color of each pixel'''
    distances = [intersect(source, direction, sphere) for sphere in spheres]
    hits = [(d, s) for d, s in zip(distances, spheres) if d] # filter out the spheres not in the line of sight
    if not hits: # if there's no sphere in the line of sight
        return black
    distance, new_sphere = min(hits)
    _, center, color = new_sphere
    surface = add(source, scale(direction, distance))
    return illumimnation(surface, center, direction, color, depth)

def illumimnation(surface, center, direction, color, depth):
    '''Return the color given the angle of light and surface'''
    surface_normal = normalize(substract(surface, center))
    surface_to_light = normalize(substract(light, surface))
    intensity = max(ambient, dot(surface_normal, surface_to_light))
    direct_light = scale(color, intensity)
    if depth == 1:
        return direct_light
    else: 
        # cosine = dot(direction, surface_normal)
        # bounce = substract(direction, scale(surface_normal, 2 * cosine))
        y_comp = scale(surface_normal, dot(direction, surface_normal))
        bounce = substract(direction, scale(y_comp, 2))
        reflected_light = ray_trace(surface, bounce, depth-1)
        ratio = 0.5 + 0.5 * intensity ** 40
        return mix(direct_light, reflected_light, ratio)


def mix(direct_light, reflected_light, r):
    return add(scale(direct_light, r), scale(reflected_light, 1-r))
        
def intersect(source, direction, sphere, min_dis = 0.001):
    '''Return the distance of a point on a sphere'''
    radius, center, color = sphere
    v = substract(source, center)
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
            if t>min_dis:
                return t
    

render()
print("Done!")
exitonclick()