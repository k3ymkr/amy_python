#!/usr/bin/env python
import sys,random

min=1
max=100
onumber=random.randint(min,max)

guess=-1
while int(guess)!=onumber:
	print "Pick a number from %d to %d:"%(min,max),
	guess=raw_input()
	try:
		if (int(guess)<onumber):
			print "Too low.  Guess Higher"
		elif (int(guess)>onumber):
			print "Too high.  Guess Lower"
		else:
			print "You win!!!"
	except ValueError:
		print "Please enter a number"
		guess=-1
	



