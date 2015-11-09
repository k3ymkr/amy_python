#!/usr/bin/env python
import curses,time,random,sys,os

height, width = os.popen('stty size', 'r').read().split()
height=int(height)
width=int(width)-1

text=[72, 101, 121, 32, 116, 104, 101, 114, 101, 44, 32, 65, 109, 121, 33, 33, 33]

if width<len(text):
        print "Please make your console bigger"
        sys.exit(0)
else:
        width=len(text)


x=0
y=0
v='<'

stdscr=curses.initscr()
curses.noecho()
curses.cbreak()
curses.curs_set(0)

stdscr.keypad(1)

ans=[]
for a in range(0,width):
	ans.append([])
	for b in range(0,height):
		ans[a].append(' ')

midh=height/2
midw=width/2-len(text)/2
for a in range(midw,midw+len(text)):
	ans[a][midh]=chr(text[a-midw])




disp=[]
for a in range(0,width):
	disp.append([])
	for b in range(0,height):
		r=chr(random.randrange(32,123))
		disp[a].append(r)
		stdscr.addstr(b,a,chr(random.randrange(32,123)))

disp[x][y]=ans[x][y]
stdscr.addstr(y,x,v)
stdscr.refresh()
try:
	while True:
		c=stdscr.getch()
		stdscr.addch(y,x,disp[x][y])
		if c==curses.KEY_RIGHT:
			if x<width-1:
				x+=1
			v='<'
		elif c==curses.KEY_LEFT:
			if x>0:
				x-=1
			v='>'
		elif c==curses.KEY_UP:
			if y>0:
				y-=1
			v='v'
		elif c==curses.KEY_DOWN:
			if y<height-1:
				y+=1
			v='^'
		disp[x][y]=ans[x][y]
		stdscr.addch(y,x,v)
		stdscr.refresh()
except:
	curses.nocbreak()
	stdscr.keypad(0);
	curses.echo();
	curses.endwin()
	curses.curs_set(1)
	sys.exit(0)


