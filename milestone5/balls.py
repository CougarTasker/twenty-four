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
    def __init__(self, pos, vel, radius, border, color,fixed =False):
        self.pos = pos
        self.vel = vel
        self.fixed = fixed
        self.radius = radius
        self.border = 1
        self.color = color
    def offset(self,direction):
        return self.pos+direction/direction.length()*self.radius
    def update(self):
        if not self.fixed:
            self.pos.add(self.vel)

    def draw(self, canvas):
        canvas.draw_circle(self.pos.get_p(),
                           self.radius,
                           self.border,
                           self.color,
                           self.color)

    def bounce(self, normal):
        self.vel.reflect(normal)
    def hit(self,ball):
        return (self.pos-ball.pos).length()<(self.radius+ball.radius)
    def normal(self,ball):
        return (ball.pos-self.pos).normalize()
class Interaction:
    def __init__(self, walls, balls):
        self.balls = balls
        self.walls = walls
        self.colliding = []
    def update(self):
        for ball in self.balls:
            for wall in self.walls:
                if wall.hit(ball):
                    if not [ball,wall] in self.colliding:
                        ball.bounce(wall.normal)
                    self.colliding.append([ball,wall])
                else: 
                    if [ball,wall] in self.colliding:
                        self.colliding.remove([ball,wall])
            for other in self.balls:
                if other != ball:
                    if ball.hit(other):
                        if not [ball,other] in self.colliding:
                            ball.bounce(other.normal(ball))
                        self.colliding.append([ball,other])
                    else: 
                        if [ball,other] in self.colliding:
                            self.colliding.remove([ball,other])
            ball.update()

    def draw(self, canvas):
        self.update()
        for ball in self.balls:
            ball.draw(canvas)
        for wall in self.walls:
            wall.draw(canvas)

# The canvas dimensions
CANVAS_WIDTH = 600
CANVAS_HEIGHT = 400


# Creating the objects84

ba = Ball(Vector(200,200), Vector(2,-1), 20, 10, 'blue',True)
bb = Ball(Vector(220,200), Vector(-1,-1), 20, 10, 'green')
bc = Ball(Vector(100,100), Vector(2,3), 50, 10, 'purple')
bd = Ball(Vector(300,200), Vector(2,-1), 20, 10, 'blue',True)
be = Ball(Vector(400,100), Vector(2,-1), 50, 10, 'blue',True)
bf = Ball(Vector(500,200), Vector(2,-1), 30, 10, 'blue',True)
bg = Ball(Vector(1500,100), Vector(2,3), 20, 10, 'orange')

wt = Wall(10, 5, 'red',"t")
wb = Wall(CANVAS_HEIGHT-10, 5, 'red',"b")
wl = Wall(10,5,"red","l")
wr = Wall(CANVAS_WIDTH-10,5,"red","r")
i = Interaction([wt,wb,wl,wr], [ba,bb,bc,bd,be,bf,bg])

# Create a frame and assign callbacks to event handlers
frame = simplegui.create_frame("ball-wall", CANVAS_WIDTH, CANVAS_HEIGHT)
frame.set_draw_handler(i.draw)

# Start the frame animation
frame.start()
