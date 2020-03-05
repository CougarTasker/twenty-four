from vect import Vector
class Score:
	def __init__(self,time,pos,die):
		self.score = 0
		self.time = time
		self.maxtime = 99
		self.starttime = self.time.time()
		self.pos = pos
		self.die = die
		self.size = Vector(160,60)
	def timeleft(self):
		t = self.maxtime - (self.time.time() - self.starttime)
		if t <= 0:
			t = 0
			self.die.gameover()
		return round(t)
	def resetScore(self):
		self.score = 0
	def incScore(self,score):
		self.score+= score
	def draw(self,canvas):
		canvas.draw_polygon((self.pos.get_p(),(self.pos+self.size.x*Vector(1,0)).get_p(),(self.pos+self.size).get_p(),(self.pos+self.size.y*Vector(0,1)).get_p()),1,"rgba(255,255,255,0)","rgba(100,100,100,0.5)")
		canvas.draw_text("Score: "+'{:04d}'.format(self.score), (self.pos+Vector(5,25)).get_p(), 30, "orange")
		canvas.draw_text("time: "+'{:02d}'.format(self.timeleft()), (self.pos+Vector(5,30+25)).get_p(), 25, "red")
