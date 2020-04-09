import time,math
class TimeHandler:
	def __init__(self):
		self.playing = True#is the game paused
		self.offset = 0#the amount of time lost to the game being paused
		self.pausestart = 0#stores when the pause was started
		self.pausehandelers = []# keep refrences to all the pause handelers
		self.incHandel = []#keep a refrace to all the timers
		self.lastproof = -1
	#start time
	def play(self):
		if not self.playing:#only do this if paused
			self.playing = True #set the playing varible
			self.offset+= time.time()-self.pausestart#calcualte offset
			self.triggerHandel()
	#pause time  
	def pause(self):
		if self.playing:# only pause if not already paused 
			self.playing = False #set the playing varible
			self.pausestart = time.time()#record when the pause was started
			self.triggerHandel()
	    #get the current time in seconds since the unix epoch
	def time(self):
		for i in self.incHandel:#check if any timeres have elapsed
			i.check()
		if self.playing:#if playing caluclate the time
			return time.time()-self.offset
		else:
			return self.pausestart-self.offset
			#if paused the time is the time the pause started
	def isPlaying(self):
		return self.playing
	def check_running(self):
		if self.lastproof > 0:
			return time.time()-self.lastproof<2
		return True
	def prove_running(self):
		self.lastproof = time.time()
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
	

	#swaps between states
	def alt(self):
		if self.playing:
			self.pause()
		else:
			self.play()

        #returns time, taking into account pauses/game restarts as the offset

#used to mimic simpleGUI time module
class Increment:
	def __init__(self,length,method):
		self.len = length#how often it should be called
		self.method = method#what should be called
		self.called = 0#number of times it has been called
		self.startTime = time.time()#when did the time start
		self.running = False#is the timer currently running
	def check(self):
		if self.running:
			if (time.time()-self.startTime)//self.len > self.called:
			#if the method hasnt been called enough times
				self.called +=1#increse the number of time called
				self.method()#call the method 
	def start(self):
		#start the timer
		self.running=True
		self.startTime = time.time()
		self.called = 0
	def stop(self):
		#stop the timer
		self.running=False
