import random, math, os,time
try:
	import simplegui
except ImportError:
	import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

#this class handles the soundtracks and sound effects used in the game
class Snd:
	def __init__(self,time,sound,volume=1,length = -1):
		self.time = time
		self.time.addHandel(self)
		addr = os.getcwd()
		self.name = sound
		self.sound = simplegui.load_sound("file:///"+addr+"/sounds/"+sound)
		self.sound.set_volume(volume)
		self.length = length# if greater than one the sound will loop
		self.playing = False#is the sound currently being played
		self.volume = volume
		self.timepaused = False#whether the sound has just been paused becuase the time has been paused
		if self.length > 0:
			self.timer = time.create_timer(self.length, self.play)
			
	def timeTrigger(self,play):
		if play:
			if self.timepaused:
				self.play()
		else:
			if self.playing: 
				self.pause()
				self.timepaused = True

	def setVol(self,vol):
		self.sound.set_volume(self.volume*vol)

	#plays sound, method called by other classes
	def play(self):
		if self.time.isPlaying():
			if self.length >0:
				self.timer.start()
			self.sound.play()
			self.sound.rewind()
			self.sound.play()
			self.playing = True
	#pauses track 
	def pause(self):
		if self.playing:
			if self.length >0:
				self.timer.stop()
			self.playing = False
			self.sound.pause()


