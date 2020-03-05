try:
	import simplegui
except ImportError:
	import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

class Keyboard:
#class used for recognising keyboard events, these events are handled in sub.py
    def __init__(self):
        self.right = False
        self.left = False
        self.down= False 
        self.up = False
        self.p = False
        self.r = False
    def keyDown(self, key):
        #print(key)
        if key == simplegui.KEY_MAP['right'] or key == simplegui.KEY_MAP['d']:
            self.right = True
        if key == simplegui.KEY_MAP['left'] or key == simplegui.KEY_MAP['a']:
            self.left = True
        if key == simplegui.KEY_MAP['down'] or key == simplegui.KEY_MAP['s']:
            self.down = True
        if key == simplegui.KEY_MAP['up'] or key == simplegui.KEY_MAP['w']:
            self.up = True
        if key == simplegui.KEY_MAP['p']:
            self.p = True
        if key == simplegui.KEY_MAP['r']:
            self.r = True
    def keyUp(self, key):
        if key == simplegui.KEY_MAP['right']or key == simplegui.KEY_MAP['d']:
            self.right = False
        if key == simplegui.KEY_MAP['left'] or key == simplegui.KEY_MAP['a']:
            self.left = False
        if key == simplegui.KEY_MAP['down'] or key == simplegui.KEY_MAP['s']:
            self.down = False
        if key == simplegui.KEY_MAP['p'] :
            self.p = False
        if key == simplegui.KEY_MAP['r']:
            self.r = False
