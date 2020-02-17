try:
	import simplegui
except ImportError:
	import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

class Keyboard:
    def __init__(self):
        self.right = False
        self.left = False
        self.moving = False

    def keyDown(self, key):
        if key == simplegui.KEY_MAP['right']:
            self.moving = True
            self.right = True
            
        if key == simplegui.KEY_MAP['left']:
            self.moving = True
            self.left = True
  
    def keyUp(self, key):
        if key == simplegui.KEY_MAP['right']:
            self.moving = False
            self.right = False
        if key == simplegui.KEY_MAP['left']:
            self.moving = False
            self.left = False
    def isMoving(self):
        return self.moving

