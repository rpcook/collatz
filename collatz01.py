# Rob Cook's attempt to visualise the Collatz conjecture as inspired by a numberphile video
# inspiration here: https://www.youtube.com/watch?v=LqKpkdRRLZw
#
# Consider the following rules for an arbitrary chosen positive integer:
#   - If the number is EVEN, half it
#   - If the number is ODD, triple it and add one
# Repeat this set of rules indefinitely.
#
# The Collatz conjecture states that this sequence will (for any integer input) finish with 1.
#
# It remains an unproven conjecture.
#

import pygame
import pygame.gfxdraw
import sys
import math
from random import randint

def hotpo(x): # Half Or Triple Plus One
	if x % 2 == 0:
		return x/2
	else:
		return x*3+1

# take the maximum integer to test from console input, if provided
if len(sys.argv) < 2:
	setSize = 10 # largest integer to test
else:
	setSize = int(sys.argv[1])

# output array to store collatz paths
collatzPaths = []
# loop through each of the integers to test
for i in range(2, setSize+1):
	collatzPath = "" # string to hold the recorded path
	while i > 1:
		if i % 2 == 0: # even number
			collatzPath = collatzPath + "E"
		else: # odd number
			collatzPath = collatzPath + "O"
		i = hotpo(i) # pass through hotpo iteration
	collatzPaths.append(collatzPath) # when you're at 1, record path to output array

# the following line displays the array of results from the above iterative loop.
# it's a bunch of "E"s and "O"s in case you hadn't guessed.
#print (collatzPaths)

# at this point, we have an array (collatzPaths) containing all of the paths of the
# integers that we're interested in. Now just a matter of visualising them.

# graphic definitions:
bgColour = 255,255,255
lineColour = 255,0,0

# drawing function definitions
# rounded flat line (pretty anti-aliasing)
def roundedFatLine(Surface, colour, startposF, endposF, width):
	# convert input floating points to integers
	startpos=[0,0]
	endpos=[0,0]
	startpos[0] = int(startposF[0])
	startpos[1] = int(startposF[1])
	endpos[0] = int(endposF[0])
	endpos[1] = int(endposF[1])
	# filled circle at start position
	pygame.gfxdraw.filled_circle(Surface, startpos[0], startpos[1], int(width/2), colour)
	pygame.gfxdraw.aacircle(Surface, startpos[0], startpos[1], int(width/2), colour)
	# filled circle at end position
	pygame.gfxdraw.filled_circle(Surface, endpos[0], endpos[1], int(width/2), colour)
	pygame.gfxdraw.aacircle(Surface, endpos[0], endpos[1], int(width/2), colour)
	# draw fat line between points
	# first compute angle between the points
	lineAngle = math.atan2(endpos[0]-startpos[0], endpos[1]-startpos[1])
	# make an array of the points bounding the rectangle
	points = []
	points.append([startpos[0]-math.cos(lineAngle)*width/2,startpos[1]+math.sin(lineAngle)*width/2])
	points.append([startpos[0]+math.cos(lineAngle)*width/2,startpos[1]-math.sin(lineAngle)*width/2])
	points.append([endpos[0]+math.cos(lineAngle)*width/2,endpos[1]-math.sin(lineAngle)*width/2])
	points.append([endpos[0]-math.cos(lineAngle)*width/2,endpos[1]+math.sin(lineAngle)*width/2])
	# draw the filled anti-aliased polygon
	pygame.gfxdraw.filled_polygon(Surface, points, colour)
	pygame.gfxdraw.aapolygon(Surface, points, colour)
	return
def roundedFatLines(Surface, colour, points, width):
	for i in range(len(points)-1):
		roundedFatLine(Surface, colour, points[i], points[i+1], width)
	return
def drawCollatzPath(Surface, colour, width, cPath):
	currentAngle = startAngle
	# reverse path Collatz path order (so that it starts at unity, rather than ends there)
	cPathRev = cPath[::-1]
	# make an empty points list
	pathPoints = [unityPosition]
	# loop through cPath (in reverse order)
	#print(cPathRev)
	for turn in cPathRev:
		# turn the path trajectory according to the new turn
		if turn == "E": # even turn
			currentAngle = currentAngle + evenStepAngle
		else: # odd turn
			currentAngle = currentAngle + oddStepAngle
		newStepX = stepLength * math.cos(currentAngle)
		newStepY = stepLength * math.sin(currentAngle)
		# append new points to pathPoints list
		pathPoints.append([pathPoints[-1][0]+newStepX, pathPoints[-1][1]+newStepY])
	# draw Collatz path
	roundedFatLines(Surface, colour, pathPoints, width)
	return
	
# setup the screen mode
screen = pygame.display.set_mode((600, 800))
unityPosition = [200,600] # position in the drawing area where unity (1) should be
evenStepAngle = 0.05 # angle to turn if the current path step is even
oddStepAngle = -0.05 # angle to turn if the current path step is odd
startAngle = -90 # direction that the path starts off with (0 being up)
cPathWidth = 4 # Collatz path width (pixels)
stepLength = 2 # step length along Collatz path

finishedDrawing = False

running = True
while running == True:
	# capture an event
	event = pygame.event.poll()
	
	# if the user clicks a button, stop execution
	if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
		running = False

	if finishedDrawing == False:
		# draw the background
		screen.fill(bgColour)
		
		# draw all Collatz paths
		for eachPath in collatzPaths:
			drawCollatzPath(screen, lineColour, cPathWidth, eachPath)

		# update the display
		pygame.display.flip()
		
		finishedDrawing = True