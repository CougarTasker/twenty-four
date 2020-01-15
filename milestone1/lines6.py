try:
    import simplegui
except ImportError :
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui


linecount=5
framenumber=0
spead = 30
width=300
# Handler to draw on canvas
def draw(canvas):
    global linecount 
    global framenumber 
    global spead
    global width
    height = 100
    framenumber += 1
    offset = (framenumber%spead)/spead*width/linecount
    for i in range(-1,linecount+1):
        canvas.draw_line((offset+i*width/linecount, 100-height/2), (offset+i*width/linecount, 100+height/2), width/linecount/2, 'Blue')
    

# Create a frame and assign callbacks to event handlers
frame = simplegui.create_frame("Home", width, 200)
frame.set_draw_handler(draw)

# Start the frame animation
frame.start()
