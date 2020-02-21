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
    def keyDown(self, key):
        print(key)
        if key == simplegui.KEY_MAP['right'] or key == simplegui.KEY_MAP['d']:
            self.right = True
        if key == simplegui.KEY_MAP['left'] or key == simplegui.KEY_MAP['a']:
            self.left = True
        if key == simplegui.KEY_MAP['down'] or key == simplegui.KEY_MAP['s']:
            self.down = True
        if key == simplegui.KEY_MAP['up'] or key == simplegui.KEY_MAP['w']:
            self.up = True
  
    def keyUp(self, key):
        if key == simplegui.KEY_MAP['right']or key == simplegui.KEY_MAP['d']:
            self.right = False
        if key == simplegui.KEY_MAP['left'] or key == simplegui.KEY_MAP['a']:
            self.left = False
        if key == simplegui.KEY_MAP['down'] or key == simplegui.KEY_MAP['s']:
            self.down = False
        if key == simplegui.KEY_MAP['up'] or key == simplegui.KEY_MAP['w']:
            self.up = False

            
    def isMoving(self):
        return self.moving

