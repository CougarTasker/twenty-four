import time 
class TimeHandeler:
	def __init__(self):
		self.playing = True
		self.offset = 0
		self.pausestart = 0
		self.pausehandelers = []

	def addHandel(self,handel):
		self.pausehandelers.append(handel)
	def triggerHandel(self):
		for i in self.pausehandelers:
			i.timeTrigger(self.playing)
	def play(self):
		if not self.playing:
			self.playing = True 
			self.offset+= time.time()-self.pausestart
			self.triggerHandel()
	def pause(self):
		if self.playing:
			self.playing = False
			self.pausestart = time.time()
			self.triggerHandel()
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
