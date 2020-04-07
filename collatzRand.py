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

# import libraries
import pygame
import pygame.gfxdraw
import sys
import math
import time as timer
from random import randint

# print instructions
print ("collatzRand.py\n\ncollatzRand [n] - where 'n' is an optional argument to define the maximum integer to evaluate (default n=1000)")
print ("controls:\nESC          Quits\nDrag Mouse   Pan view\nup/dn/l/r    Fiddle display parameters")
print ("Return       Print display parameters to console\nR            Pretty render\nA            Animate things")

def hotpo(x): # Half Or Triple Plus One
	if x % 2 == 0:
		return x/2
	else:
		return x*3+1

# TODO: make the length of the collatzPath list variable during execution?
		
# take the maximum integer to test from console input, if provided
if len(sys.argv) < 2:
	setSize = 1000 # largest integer to test
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

# at this point, we have an array (collatzPaths) containing all of the paths of the
# integers that we're interested in. Now just a matter of visualising them.

# reverse all Collatz paths (easiest to do this once now)
collatzPathsReversed = []
for eachPath in collatzPaths:
	collatzPathsReversed.append(eachPath[::-1])

# graphic definitions:
bgColour = 255,255,255
#lineColour = 255,0,0
lineColourLBound = 64,200,200
lineColourUBound = 128,255,255

# pre-populate random colour array
randomLineColours = []
for idx in range(len(collatzPaths)):
	randomLineColours.append([randint(lineColourLBound[0], lineColourUBound[0]),
	  randint(lineColourLBound[1], lineColourUBound[1]),
	  randint(lineColourLBound[2], lineColourUBound[2])])

# drawing function definitions
def filledAliasedCircle(Surface, colour, startposF, width): # rounded flat line (pretty anti-aliasing)
	# convert input floating points to integers
	startpos=[0,0]
	startpos[0] = int(startposF[0])
	startpos[1] = int(startposF[1])
	# filled circle at start position
	pygame.gfxdraw.aacircle(Surface, startpos[0], startpos[1], int(width/2), colour)
	pygame.gfxdraw.filled_circle(Surface, startpos[0], startpos[1], int(width/2), colour)
	return
def drawCollatzPathBlobs(Surface, colour, width, cPath):
	currentAngle = startAngle
	# reverse Collatz path order (so that it starts at unity, rather than ends there)
	#cPathRev = cPath[::-1]
	# make an empty points list
	pathPoints = [unityPosition]
	# loop through cPath (in reverse order)
	#print(cPathRev)
	for turn in cPath:
		# turn the path trajectory according to the new turn
		if turn == "E": # even turn
			currentAngle += evenStepAngle
		else: # odd turn
			currentAngle += oddStepAngle
		newStepX = stepLength * math.cos(currentAngle)
		newStepY = stepLength * math.sin(currentAngle)
		# append new points to pathPoints list
		pathPoints.append([pathPoints[-1][0]+newStepX, pathPoints[-1][1]+newStepY])
	# draw Collatz path (blobs)
	for eachPoint in pathPoints:
		filledAliasedCircle(Surface, colour, eachPoint, width)
	return
def drawCollatzPathQuick(Surface, colour, width, cPath):
	currentAngle = startAngle
	# reverse Collatz path order (so that it starts at unity, rather than ends there)
	#cPathRev = cPath[::-1]
	# make an empty points list
	pathPoints = [unityPosition]
	# loop through cPath (in reverse order)
	#print(cPathRev)
	for turn in cPath:
		# turn the path trajectory according to the new turn
		if turn == "E": # even turn
			currentAngle += evenStepAngle
		else: # odd turn
			currentAngle += oddStepAngle
		newStepX = stepLength * math.cos(currentAngle)
		newStepY = stepLength * math.sin(currentAngle)
		# append new points to pathPoints list
		pathPoints.append([pathPoints[-1][0]+newStepX, pathPoints[-1][1]+newStepY])
	# draw Collatz path
	pygame.draw.lines(Surface, colour, False, pathPoints, width+1)
	return

# TODO: different tack on drawing function to minimise the amount of over-draw needed
	
# setup the screen mode
baseRes = [1080,720]
screen = pygame.display.set_mode(baseRes, pygame.RESIZABLE)
unityPosition = [300,baseRes[1]-50] # position in the drawing area where unity (1) should be
baseEvenAngle = 0.125
baseOddAngle = -0.225
evenStepAngle = 0.125 # angle to turn if the current path step is even
oddStepAngle = -0.225 # angle to turn if the current path step is odd
baseGain = 0.003 # 1% step change when user hits arrow keys
oldEvenStep = evenStepAngle
oldOddStep = oddStepAngle

startAngle = -90 # direction that the path starts off with (0 being up)
cPathWidth = 4 # Collatz path width (pixels)
stepLength = 2.5 # step length along Collatz path
drawnIndex = 0 # log of last drawn path
drawingStep = 300 # number of paths to draw at a time
drawRendered = False
drawAnimated = False
time = 0 # "time" variable for animation

finishedDrawing = False
mouseButtonHeld = False
pygame.event.poll() # throwaway first event

running = True
while running == True:
	# capture an event
	event = pygame.event.poll()
	timer.sleep(0.001)
	
	# if the user quits stop execution
	if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]==True:
		running = False
	
	if pygame.key.get_pressed()[pygame.K_a]==True:
		# set everything moving (hopefully)
		drawRendered = False
		drawAnimated = True
		finishedDrawing = False
	
	# if user presses the "r" key, render the paths using a neater code
	if pygame.key.get_pressed()[pygame.K_r]==True:
		# set rendered drawing flag
		drawRendered = True
		drawAnimated = False
		drawnIndex = 0
		finishedDrawing = False
		
	if pygame.key.get_pressed()[pygame.K_UP]==True:
		# press "up" arrow, increase odd angle
		baseOddAngle *= (1+baseGain)
		finishedDrawing = False
		drawnIndex = 0
		
	if pygame.key.get_pressed()[pygame.K_DOWN]==True:
		# press "down" arrow, decrease odd angle
		baseOddAngle /= (1+baseGain)
		finishedDrawing = False
		drawnIndex = 0
		
	if pygame.key.get_pressed()[pygame.K_RIGHT]==True:
		# press "right" arrow, increase even angle
		baseEvenAngle *= (1+baseGain)
		finishedDrawing = False
		drawnIndex = 0
		
	if pygame.key.get_pressed()[pygame.K_LEFT]==True:
		# press "left" arrow, decrease even angle
		baseEvenAngle /= (1+baseGain)
		finishedDrawing = False
		drawnIndex = 0
		
	if pygame.key.get_pressed()[pygame.K_RETURN]==True:
		# print the current values of odd and even step to the console
		if oldEvenStep != evenStepAngle or oldOddStep != oddStepAngle:
			print("oddStep = " + str(oddStepAngle) + ", evenStep = " + str(evenStepAngle))
		oldEvenStep = evenStepAngle
		oldOddStep = oddStepAngle
	
	# if the window is resized, draw stuff again.
	if event.type == pygame.VIDEORESIZE:
		pygame.display.set_mode(event.dict['size'], pygame.RESIZABLE)
		drawnIndex = 0
		finishedDrawing = False
		
	# catch mouse button clicks
	if event.type == pygame.MOUSEBUTTONDOWN:
		pygame.mouse.get_rel() # throwaway initial mouse jump
		mouseButtonHeld = True
	
	# drag events
	if mouseButtonHeld == True and pygame.mouse.get_pressed()[0] == True:
		mouseDragCoords = pygame.mouse.get_rel()
		if mouseDragCoords[0] != 0 or mouseDragCoords[1] != 0:
			unityPosition[0] += mouseDragCoords[0]
			unityPosition[1] += mouseDragCoords[1]
			# draw the display again
			finishedDrawing = False
	
	# catch released mouse buttons
	if event.type == pygame.MOUSEBUTTONUP:
		mouseButtonHeld = False
		finishedDrawing = False
		
	if finishedDrawing == False:
		evenStepAngle = baseEvenAngle
		oddStepAngle = baseOddAngle
		# draw all Collatz paths
		if mouseButtonHeld == True:
			# draw the background
			screen.fill(bgColour)
			# if the mouse button's held, only draw (up to) the first 1000 paths
			for idx in range(min(len(collatzPathsReversed),1000)):
				drawCollatzPathQuick(screen, randomLineColours[idx], cPathWidth, collatzPathsReversed[idx])
				drawnIndex = 0
				finishedDrawing = True
			drawRendered = False
			drawAnimated = False
		elif drawRendered == True:
			# if asked to render view, draw full set of paths (aliased blobs)
			if drawnIndex == 0:
				# draw the background
				screen.fill(bgColour)
			# draw the paths a few at a time, to allow user events to be captured
			for idx in range(drawnIndex, min(len(collatzPathsReversed), int(drawnIndex+drawingStep/4))):
				drawCollatzPathBlobs(screen, randomLineColours[idx], cPathWidth, collatzPathsReversed[idx])
			drawnIndex += int(drawingStep / 4)
			if drawnIndex > len(collatzPathsReversed):
				finishedDrawing = True
		elif drawAnimated == True:
			# render view but smoothly vary the angles
			evenStepAngle = baseEvenAngle * (1+0.004*math.sin(time/19))
			oddStepAngle = baseOddAngle * (1+0.01*math.sin(time/17))
			# draw the background
			screen.fill(bgColour)
			# if the mouse button's held, only draw (up to) the first 1000 paths
			for idx in range(len(collatzPathsReversed)):
				drawCollatzPathQuick(screen, randomLineColours[idx], cPathWidth, collatzPathsReversed[idx])
				drawnIndex = 0
			time += 1
			if time > 360*19*17:
				time = 0
		else:
			# if mouse button released, draw full set of paths
			if drawnIndex == 0:
				# draw the background
				screen.fill(bgColour)
			# draw the paths a few at a time, to allow user events to be captured
			for idx in range(drawnIndex, min(len(collatzPathsReversed), drawnIndex+drawingStep)):
				drawCollatzPathQuick(screen, randomLineColours[idx], cPathWidth, collatzPathsReversed[idx])
			drawnIndex += drawingStep
			if drawnIndex > len(collatzPathsReversed):
				finishedDrawing = True

		# update the display
		pygame.display.flip()
		
pygame.quit()