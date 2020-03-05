import time 
class TimeHandeler:
	def __init__(self):
		self.playing = True
		self.offset = 0
		self.pausestart = 0
	def play(self):
		if not self.playing:
			self.playing = True 
			self.offset+= time.time()-self.pausestart
	def pause(self):
		if self.playing:
			self.playing = False
			self.pausestart = time.time()
	def isPlaying(self):
		return self.playing
	def alt(self):
		if self.playing:
			self.pause()
		else:
			self.play()
	def time(self):
		if self.playing:
			return time.time()-self.offset
		else:
			return self.pausestart-self.offset
