from vect import Vector 
try:
	import simplegui
except ImportError:
	import SimpleGUICS2Pygame.simpleguics2pygame as simplegui


class Player:
    def __init__(self, dimensions):
            self.canvas_dim = dimensions

            ##image info + dimensions (constants)
            self.img = simplegui.load_image("file:///Users/tiger-lily-goldsmith/Documents/RHUL/gitStuff/twenty-four/proto/boat.png")
            #self.img = simplegui.load_image("https://i.ya-webdesign.com/images/cartoon-sailboat-png-1.png")
            self.dim = (1961, 1703)
            self.cen = (self.dim[0]/2, self.dim[1]/2)
            self.draw_dim = (190, 170)

            ##player position and other attributes (variables)
            self.pos = Vector(self.draw_dim[0]/2,self.draw_dim[1]/2)
            self.vel = Vector(0,0)

        
        
    def draw(self,canvas):
        canvas.draw_image(self.img, self.cen, self.dim, self.pos.get_p(), self.draw_dim) 
        #canvas.draw_image(image, center_source, width_height_source, center_dest, width_height_dest)
        
                
def draw(canvas):
    play = Player((600,400))

    play.draw(canvas)

frame = simplegui.create_frame("ship test", 600,400)


frame.set_draw_handler(draw)
# Start the frame animation
frame.start()
