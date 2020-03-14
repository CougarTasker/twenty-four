import random, math, os,time
try:
	import simplegui
except ImportError:
	import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

class Snd:
	def __init__(self,time,sound,volume=1,length = -1):
		self.time = time
		self.time.addHandel(self)
		addr = os.getcwd()
		self.name = sound
		self.sound = simplegui.load_sound("file:///"+addr+"/sounds/"+sound)
		self.sound.set_volume(volume)
		self.length = length# if greater than one the sound will loop
		self.playing = False
		self.volume = volume
		if self.length > 0:
			self.timer = simplegui.create_timer(self.length*1000, self.play)
	def timeTrigger(self,playing):
		if playing:
			if self.length > 0:
				self.play()
		else:
			self.pause()
	def setVol(self,vol):
		self.sound.set_volume(self.volume*vol)
	def play(self):
		#print("playing "+self.name)
		if self.time.isPlaying():
			if self.length >0:
				self.timer.start()
			self.sound.play()
			self.sound.rewind()
			self.sound.play()
			self.playing = True
	def pause(self):
		#print("pausing "+self.name)
		if self.playing:
			if self.length >0:
				self.timer.stop()
			self.playing = False
			self.sound.pause()


