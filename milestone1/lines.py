try:
    import simplegui
except ImportError :
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

width = 100
height=100

def draw_handler(canvas):
    global width
    global height
    canvas.set_canvas_background("White")
    canvas.draw_line((0, 0), (width, height), 5, 'Blue')
    canvas.draw_line([0, height], [width, 0], 5, 'Blue')

frame = simplegui.create_frame('Testing', width, height)
frame.set_draw_handler(draw_handler)
frame.start()