try:
    import simplegui
except ImportError :
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

# Constants are written in capital letters
WIDTH = 700
HEIGHT = 500

# Handler to draw on canvas :
# this function is called 60 times per second
def draw(canvas):
    canvas.draw_point ([WIDTH /2, HEIGHT /2] , 'Yellow')

    offset = 1
    canvas.draw_point ([WIDTH-offset , HEIGHT-offset] , 'Red')
    canvas.draw_point ([WIDTH-offset, offset] , 'Red')
    canvas.draw_point ([offset, HEIGHT-offset] , 'Red')
    canvas.draw_point ([offset, offset] , 'Red')

# Create a frame and assign the callback to the event handler
frame = simplegui.create_frame("Points", WIDTH , HEIGHT )
frame.set_draw_handler(draw)

# Start the frame animation
frame.start()