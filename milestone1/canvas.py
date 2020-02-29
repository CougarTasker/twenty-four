import random
try:
    import simplegui
except ImportError :
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

def randCol():
    r = random.randrange(0, 256)
    g = random.randrange(0, 256)
    b = random.randrange(0, 256)
    return 'rgb('+str(r)+ ','+str(g)+ ','+str(b)+ ')'

# Drawing handler :
# this function is called 60 times per second
count = 0

def draw(canvas):
    global count
    count+=1
    if(count%60 == 0):
        frame.set_canvas_background(randCol())

# Create a frame and assign the callback to the event handler
frame = simplegui.create_frame(" Colours ", 400 , 200)
frame.set_draw_handler(draw)

# Start the frame animation
frame.start()