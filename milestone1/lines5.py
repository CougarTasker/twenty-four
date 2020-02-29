try:
    import simplegui
except ImportError :
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui


linecount=5
framenumber=0
spead = 30
width=300
height=200
# Handler to draw on canvas
def draw(canvas):
    global linecount 
    global framenumber 
    global spead
    global width
    global height
    canvas.draw_line((0,10), (width,10), 5, 'Yellow')
    canvas.draw_line((0,height-10), (width,height-10), 5, 'Yellow')
    framenumber += 1
    offset = (framenumber%spead)/spead*width/linecount
    for i in range(-1,linecount):
        canvas.draw_line((offset+i*width/linecount, height/2), (offset+i*width/linecount+width/linecount/2, height/2), 5, 'white')
    

# Create a frame and assign callbacks to event handlers
frame = simplegui.create_frame("Home", width, height)
frame.set_draw_handler(draw)

# Start the frame animation
frame.start()