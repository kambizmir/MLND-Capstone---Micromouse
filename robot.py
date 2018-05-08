import numpy as np
from maze import Maze
import turtle
import sys

from collections import deque
from random import randint

import time

class Robot(object):
    def __init__(self, maze_dim):
        '''
        Use the initialization function to set up attributes that your robot
        will use to learn and navigate the maze. Some initial attributes are
        provided based on common information, including the size of the maze
        the robot is placed in.
        '''

        self.discoveryDone = False
        self.shortestPathSearchStarted = False
        self.shortestPathSearchDone = False
        self.shortestPath = []

        self.location = [0, 0]
        self.heading = 'up'
        self.maze_dim = maze_dim

        self.allBordersData = {}
        self.allWalls = {}

        self.bordersStack = []
        self.cellsStack = []

        self.passedBorders = {}
        self.visitedCells = {}

        self.steps = 0

        self.sq_size = 0
        self.origin = 0
        
        self.wally = None

        self.buildAllBordersData()        

        self.cellsGraph = {}

        self.currentShortestPathIndex = 1

        window = turtle.Screen()       
        self.wally = turtle.Turtle()        
        self.wally.color("grey")
        self.wally.speed(0)
        self.wally.hideturtle()
        self.wally.penup()
        self.sq_size = 20
        self.origin = self.maze_dim * self.sq_size / -2

        

    def next_move(self, sensors):
        '''
        Use this function to determine the next move the robot should make,
        based on the input from the sensors after its previous move. Sensor
        inputs are a list of three distances from the robot's left, front, and
        right-facing sensors, in that order.

        Outputs should be a tuple of two values. The first value indicates
        robot rotation (if any), as a number: 0 for no rotation, +90 for a
        90-degree rotation clockwise, and -90 for a 90-degree rotation
        counterclockwise. Other values will result in no rotation. The second
        value indicates robot movement, and the robot will attempt to move the
        number of indicated squares: a positive number indicates forwards
        movement, while a negative number indicates backwards movement. The
        robot may move a maximum of three units per turn. Any excess movement
        is ignored.

        If the robot wants to end a run (e.g. during the first training run in
        the maze) then returing the tuple ('Reset', 'Reset') will indicate to
        the tester to end the run and return the robot to the start.
        '''

        rotation =0
        movement = 0
        #time.sleep(.01)
        self.steps += 1
        
        if self.discoveryDone == True and self.shortestPathSearchStarted == False:                        
            #print len(self.allBordersData) , self.allWalls.keys() , len(self.allWalls.keys())
            self.shortestPathSearchStarted = True
            self.heading = "up"
            self.location = (0,0)
            self.wally.penup()
            self.wally.setpos(self.origin + self.sq_size * self.location[0] + self.sq_size/2, self.origin + self.sq_size * (self.location[1]) + self.sq_size/2)
            self.buildGraph()
            self.findShortestPath()
            self.shortestPathSearchDone = True
                                    
            return ('Reset', 'Reset')
       
        if self.shortestPathSearchDone == True:
            
            self.wally.width(3) 
            self.wally.pendown()            
            time.sleep(1)            
            self.wally.color("blue")
            self.wally.setpos(self.origin + self.sq_size * self.location[0] + self.sq_size/2, self.origin + self.sq_size * (self.location[1]) + self.sq_size/2)
            self.wally.dot()
            #print self.location
            
            currentCellCode = self.shortestPath[self.currentShortestPathIndex]
            x1 = int(currentCellCode[0:2])
            y1 = int(currentCellCode[2:4]) 
            previousCellCode = self.shortestPath[self.currentShortestPathIndex-1]
            x0 = int(previousCellCode[0:2])
            y0 = int(previousCellCode[2:4]) 

            ydif = 0
            xdif = 0

            if x1 == x0:
                ydif = y1 - y0
            elif y1 == y0: 
                xdif = x1 - x0

            #print "DIFFS = " , xdif , ydif

            # go based on xdif and y dif
            if self.heading == 'up':
                if ydif != 0 :
                    rotation = 0
                    movement = ydif     
                    self.heading = 'up'
                    self.location = (x1,y1)    
                elif xdif > 0:
                    rotation = 90
                    movement = xdif
                    self.heading = 'right'
                    self.location = (x1,y1)
                elif xdif < 0:
                    rotation = -90
                    movement = -xdif
                    self.heading = 'left'
                    self.location = (x1,y1)
            elif self.heading == 'down':
                if ydif != 0 :
                    rotation = 0
                    movement = -ydif  
                    self.heading = 'down'
                    self.location = (x1,y1)                      
                elif xdif > 0:
                    rotation = -90
                    movement = xdif
                    self.heading = 'right'
                    self.location = (x1,y1)
                elif xdif < 0:
                    rotation = 90
                    movement = -xdif
                    self.heading = 'left'
                    self.location = (x1,y1)
            elif self.heading == 'right':
                if xdif != 0 :
                    rotation = 0
                    movement = xdif  
                    self.heading = 'right'
                    self.location = (x1,y1)                      
                elif ydif > 0:
                    rotation = -90
                    movement = ydif
                    self.heading = 'up'
                    self.location = (x1,y1)
                elif ydif < 0:
                    rotation = 90
                    movement = -ydif
                    self.heading = 'down'
                    self.location = (x1,y1)
            elif self.heading == 'left':
                if xdif != 0 :
                    rotation = 0
                    movement = -xdif  
                    self.heading = 'left'
                    self.location = (x1,y1)                      
                elif ydif > 0:
                    rotation = 90
                    movement = ydif
                    self.heading = 'up'
                    self.location = (x1,y1)
                elif ydif < 0:
                    rotation = -90
                    movement = -ydif
                    self.heading = 'down'
                    self.location = (x1,y1)

            #print rotation, movement, self.heading,self.location

            self.currentShortestPathIndex += 1
                
            if self.currentShortestPathIndex == len(self.shortestPath) :     
                time.sleep(1)                   
                self.location =( int(self.shortestPath[-1][0:2]) ,  int(self.shortestPath[-1][2:4]) )                
                self.wally.setpos(self.origin + self.sq_size * self.location[0] + self.sq_size/2, self.origin + self.sq_size * (self.location[1]) + self.sq_size/2)

                turtle.Screen().exitonclick()

            return (rotation,movement)



        leftOpen = sensors[0]
        frontOpen = sensors[1]
        rightOpen = sensors[2]
        locationX = self.location[0]
        locationY = self.location[1]

        '''
        print "\n"
        print "steps = ",self.steps
        print "location = " , locationX, locationY
        print "heading = " , self.heading
        print "left open = ",leftOpen
        print "front open = ",frontOpen
        print "right open = ", rightOpen
        '''

        self.wally.setpos(self.origin + self.sq_size * locationX + self.sq_size/2, self.origin + self.sq_size * (locationY) + self.sq_size/2)
        self.wally.dot()

        self.drawDiscoveredBorders(sensors)

        nextForwardMoves = []

        leftCellCode = ""
        frontCellCode = ""
        rightCellCode = ""

        leftBorderCode = ""
        frontBorderCode = ""
        rightBorderCode = ""            

        if self.heading == "up":              
            leftCellCode = str(locationX-1).zfill(2) + str(locationY).zfill(2)
            leftBorderCode = str(locationX).zfill(2) + str(locationY).zfill(2) + str(locationX-1).zfill(2) + str(locationY).zfill(2)
            frontCellCode = str(locationX).zfill(2) + str(locationY+1).zfill(2)
            frontBorderCode = str(locationX).zfill(2) + str(locationY).zfill(2) + str(locationX).zfill(2) + str(locationY+1).zfill(2)
            rightCellCode = str(locationX+1).zfill(2) + str(locationY).zfill(2)
            rightBorderCode = str(locationX).zfill(2) + str(locationY).zfill(2) + str(locationX+1).zfill(2) + str(locationY).zfill(2)
        elif self.heading == "right":
            leftCellCode = str(locationX).zfill(2) + str(locationY+1).zfill(2) 
            leftBorderCode = str(locationX).zfill(2) + str(locationY).zfill(2) + str(locationX).zfill(2) + str(locationY+1).zfill(2)
            frontCellCode = str(locationX+1).zfill(2) + str(locationY).zfill(2)
            frontBorderCode = str(locationX).zfill(2) + str(locationY).zfill(2) + str(locationX+1).zfill(2)+ str(locationY).zfill(2)
            rightCellCode = str(locationX).zfill(2) + str(locationY-1).zfill(2)
            rightBorderCode = str(locationX).zfill(2) + str(locationY).zfill(2) + str(locationX).zfill(2) + str(locationY-1).zfill(2)
        elif self.heading == "left":
            leftCellCode = str(locationX).zfill(2) + str(locationY-1).zfill(2) 
            leftBorderCode = str(locationX).zfill(2) + str(locationY).zfill(2) + str(locationX).zfill(2) + str(locationY-1).zfill(2)
            frontCellCode = str(locationX-1).zfill(2) + str(locationY).zfill(2)
            frontBorderCode = str(locationX).zfill(2) + str(locationY).zfill(2) + str(locationX-1).zfill(2) + str(locationY).zfill(2)
            rightCellCode = str(locationX).zfill(2) + str(locationY+1).zfill(2)
            rightBorderCode = str(locationX).zfill(2) + str(locationY).zfill(2) + str(locationX).zfill(2) + str(locationY+1).zfill(2)
        elif self.heading == "down":
            leftCellCode = str(locationX+1).zfill(2) + str(locationY).zfill(2) 
            leftBorderCode = str(locationX).zfill(2) + str(locationY).zfill(2) + str(locationX+1).zfill(2) + str(locationY).zfill(2)
            frontCellCode = str(locationX).zfill(2) + str(locationY-1).zfill(2)
            frontBorderCode = str(locationX).zfill(2) + str(locationY).zfill(2) + str(locationX).zfill(2) + str(locationY-1).zfill(2)
            rightCellCode = str(locationX-1).zfill(2) + str(locationY).zfill(2)
            rightBorderCode = str(locationX).zfill(2) + str(locationY).zfill(2) + str(locationX-1).zfill(2) + str(locationY).zfill(2)

        
        if leftOpen>0  and (not leftCellCode in self.visitedCells):
            nextForwardMoves.append("left")
        if frontOpen>0  and (not frontCellCode in self.visitedCells):
            nextForwardMoves.append("front")
        if rightOpen>0 and (not rightCellCode in self.visitedCells):
            nextForwardMoves.append("right")
        
        #print nextForwardMoves

        if len(nextForwardMoves) >0:
            nextMove = nextForwardMoves[randint(0, len(nextForwardMoves) -1 )]  # Make it random
            if nextMove == "left":
                rotation = -90
                movement = 1
                self.passedBorders[leftBorderCode] = leftBorderCode
                self.visitedCells[leftCellCode] = leftCellCode
                self.cellsStack.append(leftCellCode)
                if self.heading == "up":
                    self.heading = "left"
                    self.location = (locationX-1,locationY)
                elif self.heading == "left":
                    self.heading = "down"
                    self.location = (locationX,locationY-1)
                elif self.heading == "right":
                    self.heading = "up"
                    self.location = (locationX,locationY+1)
                elif self.heading == "down":
                    self.heading = "right"
                    self.location = (locationX+1,locationY)
                
            elif nextMove == "front":
                rotation = 0
                movement = 1
                self.passedBorders[frontBorderCode] = frontBorderCode
                self.visitedCells[frontCellCode] = frontCellCode
                self.cellsStack.append(frontCellCode)
                if self.heading == "up":
                    self.heading = "up"
                    self.location = (locationX,locationY+1)
                elif self.heading == "left":
                    self.heading = "left"
                    self.location = (locationX-1,locationY)
                elif self.heading == "right":
                    self.heading = "right"
                    self.location = (locationX+1,locationY)
                elif self.heading == "down":
                    self.heading = "down"
                    self.location = (locationX,locationY-1)

            elif nextMove == "right":                
                rotation = 90
                movement = 1
                self.passedBorders[rightBorderCode] = rightBorderCode
                self.visitedCells[rightCellCode] = rightCellCode
                self.cellsStack.append(rightCellCode)
                if self.heading == "up":
                    self.heading = "right"
                    self.location = (locationX+1,locationY)
                elif self.heading == "left":
                    self.heading = "up"
                    self.location = (locationX,locationY+1)
                elif self.heading == "right":
                    self.heading = "down"
                    self.location = (locationX,locationY-1)
                elif self.heading == "down":
                    self.heading = "left"
                    self.location = (locationX-1,locationY)
        
        else:
            
            currentCellCode = self.cellsStack[-1]
            returnCellCode = self.cellsStack[-2]

            currentLocation = (int(currentCellCode[0:2]) ,  int(currentCellCode[2:4]) )
            returnLocation = (int(returnCellCode[0:2]) ,  int(returnCellCode[2:4]) )

            #print currentLocation, returnLocation

            if currentLocation[0] == returnLocation[0]:
                if currentLocation[1]>returnLocation[1]:
                    if self.heading == "down":
                        rotation = 0
                        movement = 1          
                        self.heading = "down"
                        self.location = (locationX, locationY-1)                           
                        self.passedBorders[frontBorderCode] = frontBorderCode     
                        self.cellsStack.pop()                                           
                    elif self.heading == "left":
                        rotation = -90
                        movement = 1
                        self.heading = "down"
                        self.location = (locationX, locationY-1)      
                        self.passedBorders[leftBorderCode] = leftBorderCode     
                        self.cellsStack.pop()           
                    elif self.heading == "right":
                        rotation = 90
                        movement = 1
                        self.heading = "down"
                        self.location = (locationX, locationY-1)  
                        self.passedBorders[rightBorderCode] = rightBorderCode     
                        self.cellsStack.pop()    
                    elif self.heading == "up":
                        rotation = 90
                        movement = 0
                        self.heading = "right"
                        self.location = (locationX, locationY)                                     
                else: #currentLocation[1]<returnLocation[1]
                    if self.heading == "up":
                        rotation = 0
                        movement = 1          
                        self.heading = "up"
                        self.location = (locationX, locationY+1)                           
                        self.passedBorders[frontBorderCode] = frontBorderCode     
                        self.cellsStack.pop()                                           
                    elif self.heading == "left":
                        rotation = 90
                        movement = 1
                        self.heading = "up"
                        self.location = (locationX, locationY+1)      
                        self.passedBorders[rightBorderCode] = rightBorderCode     
                        self.cellsStack.pop()           
                    elif self.heading == "right":
                        rotation = -90
                        movement = 1
                        self.heading = "up"
                        self.location = (locationX, locationY+1)  
                        self.passedBorders[leftBorderCode] = leftBorderCode     
                        self.cellsStack.pop()    
                    elif self.heading == "down":
                        rotation = 90
                        movement = 0
                        self.heading = "left"
                        self.location = (locationX, locationY)   
            elif currentLocation[1] == returnLocation[1]:
                if currentLocation[0]>returnLocation[0]:
                    if self.heading == "left":
                        rotation = 0
                        movement = 1          
                        self.heading = "left"
                        self.location = (locationX-1, locationY)  
                        self.passedBorders[frontBorderCode] = frontBorderCode     
                        self.cellsStack.pop()                                           
                    elif self.heading == "up":
                        rotation = -90
                        movement = 1
                        self.heading = "left"
                        self.location = (locationX-1, locationY)
                        self.passedBorders[leftBorderCode] = leftBorderCode     
                        self.cellsStack.pop()           
                    elif self.heading == "down":
                        rotation = 90
                        movement = 1
                        self.heading = "left"
                        self.location = (locationX-1, locationY)
                        self.passedBorders[rightBorderCode] = rightBorderCode     
                        self.cellsStack.pop()    
                    elif self.heading == "right":
                        rotation = 90
                        movement = 0
                        self.heading = "down"
                        self.location = (locationX, locationY)   
                else: #currentLocation[0]<returnLocation[0]
                    if self.heading == "right":
                        rotation = 0
                        movement = 1          
                        self.heading = "right"
                        self.location = (locationX+1, locationY)  
                        self.passedBorders[frontBorderCode] = frontBorderCode     
                        self.cellsStack.pop()                                           
                    elif self.heading == "down":
                        rotation = -90
                        movement = 1
                        self.heading = "right"
                        self.location = (locationX+1, locationY)
                        self.passedBorders[leftBorderCode] = leftBorderCode     
                        self.cellsStack.pop()           
                    elif self.heading == "up":
                        rotation = 90
                        movement = 1
                        self.heading = "right"
                        self.location = (locationX+1, locationY)
                        self.passedBorders[rightBorderCode] = rightBorderCode     
                        self.cellsStack.pop()    
                    elif self.heading == "left":
                        rotation = 90
                        movement = 0
                        self.heading = "up"
                        self.location = (locationX, locationY)   
        
        return rotation, movement

    def buildAllBordersData(self):
        
        for x in range(self.maze_dim - 1):
            for y in range(self.maze_dim ):
                borderCode =  str(x).zfill(2) + str(y).zfill(2) + str(x+1).zfill(2) + str(y).zfill(2)
                self.allBordersData[borderCode] = borderCode

        for y in range(self.maze_dim - 1):
            for x in range(self.maze_dim ):
                borderCode =  str(x).zfill(2) + str(y).zfill(2) + str(x).zfill(2) + str(y+1).zfill(2)
                self.allBordersData[borderCode] = borderCode

        #print self.allBordersData.keys() , len(self.allBordersData)
        

    def drawDiscoveredBorders(self,sensors):

        self.wally.color("red")

        leftOpen = sensors[0]
        frontOpen = sensors[1]
        rightOpen = sensors[2]
        locationX = self.location[0]
        locationY = self.location[1]

        #print locationX,locationY,leftOpen,frontOpen,rightOpen, self.heading
        #print(self.wally.position())

        temp = self.wally.position()

        self.wally.hideturtle()  

        if self.heading == "up":

            self.wally.penup()                        
            self.wally.setpos(temp[0]-self.sq_size/2, temp[1] +  (frontOpen) * self.sq_size + self.sq_size/2 )
            self.wally.pendown()
            self.wally.setpos(temp[0]+self.sq_size/2, temp[1] + (frontOpen) * self.sq_size + self.sq_size/2 )

            self.wally.penup() 
            self.wally.goto(temp[0]+ (rightOpen) * self.sq_size + self.sq_size/2 , temp[1] + self.sq_size/2 )
            self.wally.pendown()
            self.wally.goto(temp[0]+ (rightOpen) * self.sq_size + self.sq_size/2 , temp[1] - self.sq_size/2 )
            
            self.wally.penup() 
            self.wally.goto(temp[0]- (leftOpen) * self.sq_size - self.sq_size/2 , temp[1] + self.sq_size/2 )
            self.wally.pendown()
            self.wally.goto(temp[0]- (leftOpen) * self.sq_size - self.sq_size/2 , temp[1] - self.sq_size/2 )
                    
            self.wally.penup()
            self.wally.goto(temp)

            for x in range(leftOpen+1):
                b = str(locationX - x - 1).zfill(2) + str(locationY).zfill(2) +  str(locationX - x ).zfill(2) + str(locationY).zfill(2) 
                self.allBordersData.pop(b, None)                
                if x == leftOpen and locationX - leftOpen >0:
                    self.allWalls[b] = b
            for x in range(rightOpen+1):
                b = str(locationX + x ).zfill(2) + str(locationY).zfill(2) +  str(locationX + x + 1).zfill(2) + str(locationY).zfill(2) 
                self.allBordersData.pop(b, None)
                if x == rightOpen and locationX + rightOpen < self.maze_dim - 1 :
                    self.allWalls[b] = b
            for y in range(frontOpen+1):
                b = str(locationX).zfill(2) + str(locationY + y).zfill(2) +  str(locationX).zfill(2) + str(locationY + y + 1).zfill(2) 
                self.allBordersData.pop(b, None)
                if y == frontOpen  and locationY + frontOpen < self.maze_dim - 1:
                    self.allWalls[b] = b

             
        
        elif self.heading == "right":

            self.wally.penup() 
            self.wally.goto(temp[0]+ (frontOpen) * self.sq_size + self.sq_size/2 , temp[1] + self.sq_size/2 )
            self.wally.pendown()
            self.wally.goto(temp[0]+ (frontOpen) * self.sq_size + self.sq_size/2 , temp[1] - self.sq_size/2 )

            self.wally.penup()                        
            self.wally.setpos(temp[0]-self.sq_size/2, temp[1] - (rightOpen) * self.sq_size - self.sq_size/2 )
            self.wally.pendown()
            self.wally.setpos(temp[0]+self.sq_size/2, temp[1] - (rightOpen) * self.sq_size - self.sq_size/2 )

            self.wally.penup()                        
            self.wally.setpos(temp[0]-self.sq_size/2, temp[1] + (leftOpen) * self.sq_size + self.sq_size/2 )
            self.wally.pendown()
            self.wally.setpos(temp[0]+self.sq_size/2, temp[1] + (leftOpen) * self.sq_size + self.sq_size/2 )

            self.wally.penup()
            self.wally.goto(temp)

            for y in range(leftOpen+1):
                b = str(locationX).zfill(2) + str(locationY + y).zfill(2) +  str(locationX).zfill(2) + str(locationY + y + 1).zfill(2) 
                self.allBordersData.pop(b, None)
                if y == leftOpen and locationY + leftOpen < self.maze_dim-1:
                    self.allWalls[b] = b                
            for y in range(rightOpen+1):
                b = str(locationX).zfill(2) + str(locationY - y -1).zfill(2) +  str(locationX).zfill(2) + str(locationY - y).zfill(2) 
                self.allBordersData.pop(b, None)
                if y == rightOpen and locationY - rightOpen > 0 :
                    self.allWalls[b] = b                
            for x in range(frontOpen+1):
                b = str(locationX + x ).zfill(2) + str(locationY).zfill(2) +  str(locationX + x + 1).zfill(2) + str(locationY).zfill(2) 
                self.allBordersData.pop(b, None)
                if x == frontOpen and locationX + frontOpen < self.maze_dim - 1:
                    self.allWalls[b] = b
                
        
        elif self.heading == "down":
            self.wally.penup()                        
            self.wally.setpos(temp[0]-self.sq_size/2, temp[1] -  (frontOpen) * self.sq_size - self.sq_size/2 )
            self.wally.pendown()
            self.wally.setpos(temp[0]+self.sq_size/2, temp[1] - (frontOpen) * self.sq_size - self.sq_size/2 )

            self.wally.penup() 
            self.wally.goto(temp[0]- (rightOpen) * self.sq_size - self.sq_size/2 , temp[1] + self.sq_size/2 )
            self.wally.pendown()
            self.wally.goto(temp[0]- (rightOpen) * self.sq_size - self.sq_size/2 , temp[1] - self.sq_size/2 )
            
            self.wally.penup() 
            self.wally.goto(temp[0]+ (leftOpen) * self.sq_size + self.sq_size/2 , temp[1] + self.sq_size/2 )
            self.wally.pendown()
            self.wally.goto(temp[0]+ (leftOpen) * self.sq_size + self.sq_size/2 , temp[1] - self.sq_size/2 )
                                        
            self.wally.penup()
            self.wally.goto(temp)

            for x in range(leftOpen+1):
                b = str(locationX + x).zfill(2) + str(locationY).zfill(2) +  str(locationX + x + 1).zfill(2) + str(locationY).zfill(2) 
                self.allBordersData.pop(b, None)
                if x == leftOpen and locationX + leftOpen < self.maze_dim - 1:
                    self.allWalls[b] = b                
            for x in range(rightOpen+1):
                b = str(locationX - x -1).zfill(2) + str(locationY).zfill(2) +  str(locationX - x).zfill(2) + str(locationY).zfill(2) 
                self.allBordersData.pop(b, None)
                if x == rightOpen and locationX - rightOpen > 0:
                    self.allWalls[b] = b                
            for y in range(frontOpen+1):
                b = str(locationX).zfill(2) + str(locationY - y - 1).zfill(2) +  str(locationX).zfill(2) + str(locationY - y).zfill(2) 
                self.allBordersData.pop(b, None)
                if y == frontOpen and locationY - frontOpen > 0 :
                    self.allWalls[b] = b                

        elif self.heading == "left":

            self.wally.penup() 
            self.wally.goto(temp[0]- (frontOpen) * self.sq_size - self.sq_size/2 , temp[1] + self.sq_size/2 )
            self.wally.pendown()
            self.wally.goto(temp[0]- (frontOpen) * self.sq_size - self.sq_size/2 , temp[1] - self.sq_size/2 )

            self.wally.penup()                        
            self.wally.setpos(temp[0]-self.sq_size/2, temp[1] + (rightOpen) * self.sq_size + self.sq_size/2 )
            self.wally.pendown()
            self.wally.setpos(temp[0]+self.sq_size/2, temp[1] + (rightOpen) * self.sq_size + self.sq_size/2 )

            self.wally.penup()                        
            self.wally.setpos(temp[0]-self.sq_size/2, temp[1] - (leftOpen) * self.sq_size - self.sq_size/2 )
            self.wally.pendown()
            self.wally.setpos(temp[0]+self.sq_size/2, temp[1] - (leftOpen) * self.sq_size - self.sq_size/2 )

            self.wally.penup()
            self.wally.goto(temp)

            for y in range(leftOpen+1):
                b = str(locationX).zfill(2) + str(locationY - y - 1).zfill(2) +  str(locationX).zfill(2) + str(locationY - y).zfill(2) 
                self.allBordersData.pop(b, None)
                if y == leftOpen and locationY - leftOpen > 0 :
                    self.allWalls[b] = b                
            for y in range(rightOpen+1):
                b = str(locationX).zfill(2) + str(locationY + y).zfill(2) +  str(locationX).zfill(2) + str(locationY +y + 1).zfill(2) 
                self.allBordersData.pop(b, None)
                if y == rightOpen and locationY + rightOpen < self.maze_dim - 1:
                    self.allWalls[b] = b                
            for x in range(frontOpen+1):
                b = str(locationX - x - 1).zfill(2) + str(locationY).zfill(2) +  str(locationX - x ).zfill(2) + str(locationY).zfill(2) 
                self.allBordersData.pop(b, None)
                if x == frontOpen and locationX - frontOpen > 0:
                    self.allWalls[b] = b
                
        if len(self.allBordersData) == 0:
            self.discoveryDone = True

        self.wally.pendown()
        self.wally.showturtle()
        self.wally.color("grey")
        

    def buildGraph(self):
        print "BUILD THE SHORTEST PATH NOW ..."
        for x in range(self.maze_dim):
            for y in range(self.maze_dim):
                cellCode = str(x).zfill(2) + str(y).zfill(2)
                self.cellsGraph[cellCode] = {}
                for rc in self.findRightCells(cellCode):
                    self.cellsGraph[cellCode][rc] = rc
                for lc in self.findLeftCells(cellCode):
                    self.cellsGraph[cellCode][lc] = lc
                for uc in self.findUpCells(cellCode):
                    self.cellsGraph[cellCode][uc] = uc
                for dc in self.findDownCells(cellCode):
                    self.cellsGraph[cellCode][dc] = dc                        
    
    def findRightCells(self,cellCode):        
        result =  []
        x = int(cellCode[0:2])
        y= int(cellCode[2:4])
        
        c1 = str(x+1).zfill(2) + str(y).zfill(2)
        c2 = str(x+2).zfill(2) + str(y).zfill(2)
        c3 = str(x+3).zfill(2) + str(y).zfill(2)

        b1 = cellCode + c1
        b2 = c1 + c2
        b3 = c2 + c3

        if b1 not in self.allWalls and x<self.maze_dim-1:
            result.append(c1)
            if b2 not in self.allWalls and x<self.maze_dim-2:
                result.append(c2)
                if b3 not in self.allWalls and x<self.maze_dim-3:
                    result.append(c3)
        
        return result


    def findLeftCells(self,cellCode):
        result =  []
        x = int(cellCode[0:2])
        y= int(cellCode[2:4])
        
        c1 = str(x-1).zfill(2) + str(y).zfill(2)
        c2 = str(x-2).zfill(2) + str(y).zfill(2)
        c3 = str(x-3).zfill(2) + str(y).zfill(2)

        b1 = c1 + cellCode  
        b2 = c2 + c1
        b3 = c3 + c2

        if b1 not in self.allWalls and x>0:
            result.append(c1)
            if b2 not in self.allWalls and x>1:
                result.append(c2)
                if b3 not in self.allWalls and x>2:
                    result.append(c3)
        
        return result


    def findUpCells(self,cellCode):
        result =  []
        x = int(cellCode[0:2])
        y= int(cellCode[2:4])
        
        c1 = str(x).zfill(2) + str(y+1).zfill(2)
        c2 = str(x).zfill(2) + str(y+2).zfill(2)
        c3 = str(x).zfill(2) + str(y+3).zfill(2)

        b1 = cellCode + c1
        b2 = c1 + c2
        b3 = c2 + c3

        if b1 not in self.allWalls and y<self.maze_dim-1:
            result.append(c1)
            if b2 not in self.allWalls and y<self.maze_dim-2:
                result.append(c2)
                if b3 not in self.allWalls and y<self.maze_dim-3:
                    result.append(c3)
        
        return result


    def findDownCells(self,cellCode):
        result =  []
        x = int(cellCode[0:2])
        y= int(cellCode[2:4])
        
        c1 = str(x).zfill(2) + str(y-1).zfill(2)
        c2 = str(x).zfill(2) + str(y-2).zfill(2)
        c3 = str(x).zfill(2) + str(y-3).zfill(2)

        b1 = c1 + cellCode 
        b2 = c2 + c1
        b3 = c3 + c2

        if b1 not in self.allWalls and y>0:
            result.append(c1)
            if b2 not in self.allWalls and y>1:
                result.append(c2)
                if b3 not in self.allWalls and y>2:
                    result.append(c3)
        
        return result

        
    def findShortestPath(self):   
        x1 = self.maze_dim/2
        x2 = x1 - 1

        center1 = str(x1).zfill(2) + str(x1).zfill(2)
        center2 = str(x1).zfill(2) + str(x2).zfill(2)
        center3 = str(x2).zfill(2) + str(x2).zfill(2)
        center4 = str(x2).zfill(2) + str(x1).zfill(2)
        centers = [center1,center2,center3,center4]

        bfsSearchDone = False
        target = None
        bfsVisitedCells = {}
        bfsDistances = {}
        q = deque([])

        for x in self.cellsGraph:
            bfsVisitedCells[x] = False
            bfsDistances[x] =10000
        
        q.append('0000')
        bfsVisitedCells ['0000'] = True
        bfsDistances ['0000'] = 0

        while len(q)>0:
            if bfsSearchDone ==True:
                break
            x = q.popleft()
            currentDistance = bfsDistances[x]
            neighbors = self.cellsGraph[x]
            for n in neighbors:
                if bfsVisitedCells[n] == False:
                    bfsVisitedCells[n] = True
                    bfsDistances[n] = currentDistance + 1                     
                    q.append(n)
                    if n in centers:
                        bfsSearchDone = True
                        target = n
                        break
            
        self.shortestPath =[target]

        currntNode = target
        while True:
            if currntNode == '0000':
                break
            neighbors = self.cellsGraph[currntNode]
            for n in neighbors:
                if bfsDistances[n] == bfsDistances[currntNode] - 1:
                    currntNode = n
                    self.shortestPath.append(currntNode)
                    break
            

        self.shortestPath.reverse()


        #print "GRAPH = " , self.cellsGraph
        #print "CENTERS = ", center1,center2,center3,center4
        #print "VISITED CELLS = ", bfsVisitedCells
        #print "DISTANCES = ", bfsDistances
        #print "QUEUE = ", q
        #print "Target = ", target
        print "SHORTEST PATH = " , self.shortestPath
        