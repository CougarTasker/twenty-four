
try:
    import simplegui
except ImportError :
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

def fill_circle(self,point,radius,color):
		self.draw_circle(point,radius/2,radius,color)

# Constants are written in capital letters
WIDTH = 200
HEIGHT = 200

# Handler to draw on canvas :
# this function is called 60 times per second
def draw(canvas):
    fill_circle(canvas,(100, 100), 100, 'Green')
    fill_circle(canvas,(70, 70), 30, 'Red')
# Create a frame and assign the callback to the event handler
frame = simplegui.create_frame("Points", WIDTH , HEIGHT )
frame.set_draw_handler(draw)

# Start the frame animation
frame.start()