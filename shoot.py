#!/usr/bin/env python
import curses,time,random,sys,os

height, width = os.popen('stty size', 'r').read().split()
height=int(height)
width=int(width)-1

text=[72, 101, 121, 32, 116, 104, 101, 114, 101, 44, 32, 65, 109, 121, 33, 33, 33]
if width<len(text)+1:
	print "Please make your console bigger"
	sys.exit(0)
else:
	width=len(text)
shootfield=[]
for a in range(0,width):
	shootfield.append([' ',0])
midw=width/2-len(text)/2
for a in range(midw,midw+len(text)):
	shootfield[a][0]=text[a-midw]



#logfh=open("shoot.log","w")






x=width/2
y=height-1
v='^'



class badguy:
	def __init__(self,s,x,y,goal):
		self.x=x
		self.y=y
		self.s=s
		self.alive=2
		self.goal=goal
		self.type=random.randint(0,1)
		self.id=random.randint(0,10000)
		#logfh.write("Created BG: %d\n"%self.id)
		

	def disp(self):
		if self.alive==1:
			if (int(self.y)>0):
				self.s.addch(int(self.y),self.x,' ')
			self.alive=0
		elif (self.y<self.goal):
			if (int(self.y)>0) or shootfield[self.x][1]==0:
				self.s.addch(int(self.y),self.x,' ')
			else:
				self.s.addch(0,self.x,shootfield[self.x][0])
			if (self.type==0):
				self.y+=.05
				self.s.addch(int(self.y),self.x,'X')
			else:
				self.y+=.128
				self.s.addch(int(self.y),self.x,'x')

	def gothit(self):
		self.s.addch(int(self.y),self.x,'*')
		self.s.addch(0,self.x,shootfield[self.x][0])
		shootfield[self.x][1]=1
		self.alive=1
		return self.type*10+10

	def isalive(self):
		return self.alive > 0


	def victory(self):
		if self.y>=self.goal and self.alive != 0:
			self.s.addch(int(self.y),self.x,' ')
			shootfield[self.x][1]=0
			self.s.addch(0,self.x,' ')
			return True

	def getloc(self):
		return [self.x,int(self.y)]
			
	def getid(self):
		return self.id
			


		

				

class shot:
	def __init__(self,s,x,y):
		self.x=x
		self.y=y
		self.s=s
		self.id=random.randint(0,10000)
		#logfh.write("Created Shot: %d\n"%self.id)

	def disp(self):
		if (self.y>=0):
			if (int(self.y)>0) or shootfield[self.x][1]==0:
				self.s.addch(self.y,self.x,' ')
			else:
				self.s.addch(0,self.x,shootfield[self.x][0])
			self.y-=1
			if (self.y>-1):
				self.s.addch(self.y,self.x,'|')
		return self.y

	def ontarget(self,bg):
		b=bg.getloc()
		if self.x==b[0] and self.y<=b[1]:
			#logfh.write("Shot %d hit BG %d"%(self.id,bg.getid()))
			if (self.y>-1):
				self.s.addch(self.y,self.x,' ')
			a=bg.gothit()
			return a 
	
	def getid(self):
		return self.id
		
		

class goodguy:
	v='^'
	def __init__(self,s,x,y):
		self.x=x
		self.y=y
		self.s=s
		self.s.addch(self.y,self.x,goodguy.v)
		self.shots=[]
		self.score=0


	def mover(self):
		self.s.addch(self.y,self.x,' ')
		if self.x<width-1:
			self.x+=1
		else:
			self.x=0
		self.s.addch(self.y,self.x,goodguy.v)
		
	def movel(self):
		self.s.addch(self.y,self.x,' ')
		if self.x>0:
			self.x-=1
		else:
			self.x=width-1
		self.s.addch(self.y,self.x,goodguy.v)

	def shoot(self):
		self.shots.append(shot(self.s,self.x,self.y-1))

	def update(self):
		#self.s.addstr(0,0,str(self.score))
		for a in self.shots:
			b=a.disp()
			if b<0:
				#logfh.write("shot removed end: %d\n"%a.getid())
				self.shots.remove(a)
		
	def gotem(self,bg):
		hit=0
		for a in self.shots:
			c=a.ontarget(bg)
			if c>0:
				self.score+=c
				hit=1
				#logfh.write("shot removed hit: %d\n"%a.getid())
				self.shots.remove(a)
		return hit==1

	def getscore(self):
		return self.score
		
		


stdscr=curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.nodelay(True)
curses.curs_set(0)

stdscr.keypad(1)


for a in range(0,height-1):
	stdscr.addch(a,width+1,'|')

gg=goodguy(stdscr,width/2,height-1)
bgs=[]
stdscr.refresh()
try:
	while True:
		c=stdscr.getch()
		if c==curses.KEY_RIGHT:
			gg.mover()
		elif c==curses.KEY_LEFT:
			gg.movel()
		elif c==curses.KEY_UP:
			gg.shoot()
		if (random.randint(0,width)==1):
			bgs.append(badguy(stdscr,random.randint(0,width-1),0,y))
		for a in bgs:
			a.disp()
		gg.update()
		for a in bgs:
			gg.gotem(a)
			if not a.isalive():
				#logfh.write("BG shot removed: %d\n"%a.getid())
				bgs.remove(a)
			if a.victory():
				#logfh.write("BG victory removed: %d\n"%a.getid())
				bgs.remove(a)
		stdscr.refresh()
		#logfh.flush()
		time.sleep(.05)
except:
	curses.nocbreak()
	stdscr.keypad(0);
	curses.echo();
	curses.endwin()
	curses.curs_set(1)
	#logfh.close()
	sys.exit(0)


