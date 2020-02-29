from vect import Vector
from spritesheet import SpriteSheet as SS
import random,math
try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

WIDTH = 500
HEIGHT = 500

exp =[]
def draw(canvas):
	for anim in exp:
		if anim.done():
			exp.remove(anim)
		else:
			anim.draw(canvas)

	if random.random() < 1/80:
		add()

def add():
	exp.append(SS("file:///C:/Users/Couga/Documents/repos/twenty-four/milestone4/explosion-spritesheet.png",(9,9),Vector(random.randrange(100,400),random.randrange(100,400)),72,random.randrange(500,2000),random.uniform(0.1,0.4)))

frame = simplegui.create_frame('Explosion', WIDTH, HEIGHT)
frame.set_canvas_background("black")
frame.set_draw_handler(draw)
frame.start()