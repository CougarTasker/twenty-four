try:
	import simplegui
except ImportError:
	import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
class Keyboard:
#class used for recognising keyboard events, these events are handled in inter.py/overlay.py
    def __init__(self):
        self.space  = False
        self.right = False
        self.left = False
        self.down= False 
        self.p = False

    def keyDown(self, key):
        if key == simplegui.KEY_MAP['right'] or key == simplegui.KEY_MAP['d']:
            self.right = True
        if key == simplegui.KEY_MAP['left'] or key == simplegui.KEY_MAP['a']:
            self.left = True
        if key == simplegui.KEY_MAP['down'] or key == simplegui.KEY_MAP['s']:
            self.down = True
        if key == simplegui.KEY_MAP['p']:
            self.p = True
        if key == simplegui.KEY_MAP['space']:
            self.space = True
    def keyUp(self, key):
        if key == simplegui.KEY_MAP['right']or key == simplegui.KEY_MAP['d']:
            self.right = False
        if key == simplegui.KEY_MAP['left'] or key == simplegui.KEY_MAP['a']:
            self.left = False
        if key == simplegui.KEY_MAP['down'] or key == simplegui.KEY_MAP['s']:
            self.down = False
        if key == simplegui.KEY_MAP['p']:
            self.p = False
        if key == simplegui.KEY_MAP['space']:
            self.space = False

