import time,math
class TimeHandeler:
	def __init__(self):
		self.playing = True
		self.offset = 0
		self.pausestart = 0
		self.pausehandelers = []
		self.incHandel = []

	def create_timer(self,length,method):
		out = Increment(length,method)
		self.incHandel.append(out)
		return out
	def addHandel(self,handel):
		self.pausehandelers.append(handel)
	def triggerHandel(self):
		for i in self.pausehandelers:
			i.timeTrigger(self.playing)

	#plays timer and increments to offset var the time spent paused
	def play(self):
		if not self.playing:
			self.playing = True 
			self.offset+= time.time()-self.pausestart
			self.triggerHandel()

	#when timer is paused this is recorded as an offset in the ongoing timer
	def pause(self):
		if self.playing:
			self.playing = False
			self.pausestart = time.time()
			self.triggerHandel()
	def isPlaying(self):
		return self.playing

	#swaps between states
	def alt(self):
		if self.playing:
			self.pause()
		else:
			self.play()

        #returns time, taking into account pauses/game restarts as the offset
	def time(self):
		for i in self.incHandel:
			i.check()
		if self.playing:
			return time.time()-self.offset
		else:
			return self.pausestart-self.offset
#used to mimic simpleGUI time module
class Increment:
	def __init__(self,length,method):
		self.len = length
		self.method = method
		self.called = 0#number of times it has been called
		self.startTime = time.time()
		self.running = False
	def check(self):
		if self.running:
			if (time.time()-self.startTime)//self.len > self.called:
				self.called +=1
				self.method()
	def start(self):
		self.running=True
		self.startTime = time.time()
		self.called = 0
	def stop(self):
		self.running=False
