from vect import Vector
import random,math
try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

class Wall:
    def __init__(self, x, border, color,direction = "t"):

        directions = ["r","l","t","b"]
        if(not direction in directions):
            direction = directions[0]
            print("error incorrect direction given")
        if(direction == "r"):
            self.normal = Vector(-1,0)
        elif(direction == "l"):
            self.normal  = Vector(1,0)
        elif(direction == "t"):
            self.normal = Vector(0,1)
        else:
            self.normal = Vector(0,-1)     
        if self.vert():
            self.y = x 
        else:
            self.x =x    
        self.direction = direction
        self.border = border
        self.color = color
    def vert(self):
        return abs(self.normal.y) > 0
    def draw(self, canvas):
        if self.vert():
            canvas.draw_line((0, self.y),
                         (CANVAS_WIDTH, self.y),
                         self.border*2+1,
                         self.color)            
        else:
            canvas.draw_line((self.x, 0),
                         (self.x, CANVAS_HEIGHT),
                         self.border*2+1,
                         self.color)

    def hit(self, ball):
        if self.vert():
            return abs(ball.offset(self.normal*-1).y-self.y)<=self.border
        else:
            return abs(ball.offset(self.normal*-1).x-self.x)<=self.border

class Ball:
    def __init__(self, pos, vel, radius, border, color):
        self.pos = pos
        self.vel = vel
        self.radius = radius
        self.border = 1
        self.color = color
    def offset(self,direction):
        return self.pos+direction/direction.length()*self.radius
    def update(self):
        self.pos.add(self.vel)

    def draw(self, canvas):
        canvas.draw_circle(self.pos.get_p(),
                           self.radius,
                           self.border,
                           self.color,
                           self.color)

    def bounce(self, normal):
        self.vel.reflect(normal)

class Interaction:
    def __init__(self, walls, ball):
        self.ball = ball
        self.walls = walls
        self.colliding = []
    def update(self):
        for wall in self.walls:
            if wall.hit(self.ball):
                if not wall in self.colliding:
                    self.ball.bounce(wall.normal)
                self.colliding.append(wall)
            else: 
                if wall in self.colliding:
                    self.colliding.remove(wall)
        self.ball.update()

    def draw(self, canvas):
        self.update()
        self.ball.draw(canvas)
        for wall in self.walls:
            wall.draw(canvas)

# The canvas dimensions
CANVAS_WIDTH = 600
CANVAS_HEIGHT = 400

# Initial position and velocity of the ball
p = Vector(200,200)
v = Vector(2,-1)

# Creating the objects
b = Ball(p, v, 20, 50, 'blue')
wt = Wall(10, 5, 'red',"t")
wb = Wall(CANVAS_HEIGHT-10, 5, 'red',"b")
wl = Wall(10,5,"red","l")
wr = Wall(CANVAS_WIDTH-10,5,"red","r")
i = Interaction([wt,wb,wl,wr], b)

# Create a frame and assign callbacks to event handlers
frame = simplegui.create_frame("ball-wall", CANVAS_WIDTH, CANVAS_HEIGHT)
frame.set_draw_handler(i.draw)

# Start the frame animation
frame.start()
