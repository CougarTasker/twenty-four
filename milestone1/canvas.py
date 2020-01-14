import simplegui

import simplegui , random

def randCol():
    r = random.randrange (0, 256)
    g = random.randrange (0, 256)
    b = random.randrange (0, 256)
    return 'rgb('+str(r)+ ','+str(g)+ ','+str(b)+ ')'

# Drawing handler :
# this function is called 60 times per second
def draw(canvas):
    frame.set_canvas_background(randCol())

# Create a frame and assign the callback to the event handler
frame = simplegui.create_frame(" Colours ", 400 , 200)
frame.set_draw_handler(draw)

# Start the frame animation
frame.start ()