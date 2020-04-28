from __future__ import division
import random
import math
import pygame
import numpy as np
import matplotlib.pyplot as plt
import time 

WIDTH = 7
HEIGHT = 7
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0,0,255)
YELLOW = (0,255,255)
MARGIN = 3

class Maze:
    def __init__(self,boyut, engel):

        self.engel = engel
        self.boyut = boyut
        self.bestIndiv = None
        self.bestFinessValues = []

        grid = []
        for row in range(boyut):
            grid.append(["#"])
            for column in range(boyut-2):
                if row == 0 or row == boyut-1:
                    grid[row].append("#")
                else :
                     grid[row].append("-") 
            grid[row].append("#")
        
        tempGrid = grid

        for i in range(engel):
            x = int(random.uniform(5,self.boyut-5))
            z = int(random.uniform(5,self.boyut-5))
            y = random.uniform(0,1)
            if y > 0.5: # yukardan asagiya
                grid[x][z]= "#"
                grid[x+1][z]="#"
                grid[x+2][z]="#"
                grid[x+3][z]="#"
            else :
                grid[x][z]= "#"
                grid[x][z+1]="#"
                grid[x][z+2]="#"
                grid[x][z+3]="#"

        self.maze = grid

        self.maze[1][1] = "S"
        self.maze[boyut-2][boyut-2] = "E"


        self.MazeVisual = self.maze
        
        self.startCell = self.findCords("S");
    
        self.currentCell = self.startCell;
        self.endCell = self.findCords("E");

        self.visual()
        self.PRINTMAZE=0

    def findCords(self,targetChar):
        for x in range(len(self.maze)):
            for y in range(len(self.maze[x])):
                if self.maze[x][y] == targetChar:
                    return [x, y]
        return None
    

    def visual(self):
        pygame.init()

        WINDOW_SIZE = [self.boyut*(WIDTH+MARGIN), self.boyut*(WIDTH+MARGIN)]
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption("Array Backed Grid")

        clock = pygame.time.Clock()

        for row in range(self.boyut):
            for column in range(self.boyut):
                color = WHITE
                if self.MazeVisual[row][column] == '#':
                    color = GREEN
                elif self.MazeVisual[row][column] == "E":
                    color = BLUE
                elif self.MazeVisual[row][column] == "S":
                    color= YELLOW
                pygame.draw.rect(self.screen,
                                color,
                                [(MARGIN + WIDTH) * column + MARGIN,
                                (MARGIN + HEIGHT) * row + MARGIN,
                                WIDTH,
                                HEIGHT])
        pygame.display.flip()

    def fillMove(self, renk):
        color = renk
        pygame.draw.rect(self.screen,
                            color,
                            [(MARGIN + WIDTH) * self.currentCell[1] + MARGIN,
                            (MARGIN + HEIGHT) * self.currentCell[0] + MARGIN,
                            WIDTH,
                            HEIGHT])
        pygame.display.flip()
    
    def resetMaze(self):
        # time.sleep(0.1)
        for row in range(self.boyut):
            for column in range(self.boyut):
                color = WHITE
                if self.MazeVisual[row][column] == '#':
                    color = GREEN
                elif self.MazeVisual[row][column] == "E":
                    color = BLUE
                elif self.MazeVisual[row][column] == "S":
                    color= YELLOW
                pygame.draw.rect(self.screen,
                                color,
                                [(MARGIN + WIDTH) * column + MARGIN,
                                (MARGIN + HEIGHT) * row + MARGIN,
                                WIDTH,
                                HEIGHT])
        pygame.display.flip()


    def calcFit(self,indiv):
 
        cikisaUzunlukX = abs(self.currentCell[0] - self.endCell[0]) #
        cikisaUzunlukY = abs(self.currentCell[1] - self.endCell[1]) # 

        indiv.fitnes = 500000 -  10* math.sqrt(cikisaUzunlukX **2 + cikisaUzunlukY **2) - indiv.visitScore 

   
    
    def walkInMaze(self, indiv):
        indiv.visitScore = 0
        tempMaze = np.zeros([self.boyut, self.boyut]) 
        self.currentCell = self.startCell
        carpmadanGittigi = 0
        if(indiv == self.bestIndiv):
            self.resetMaze()
            self.bestFinessValues.append(indiv.fitnes)
        for gen in indiv.genes:
            posibleMove = None
            if gen == "U" :
                posibleMove = [self.currentCell[0] - 1, self.currentCell[1]]
            elif gen == "D":
                posibleMove = [self.currentCell[0] + 1, self.currentCell[1]]
            elif gen == "R":
                posibleMove = [self.currentCell[0], self.currentCell[1] + 1]
            elif gen == "L":
                posibleMove = [self.currentCell[0], self.currentCell[1] -1]

            if self.CheckForVaildMove(posibleMove):
                self.currentCell = posibleMove
                
                tempMaze[self.currentCell[0]][self.currentCell[1]] += +1

                if(indiv == self.bestIndiv):
                    self.fillMove(RED)
                if self.maze[self.currentCell[0]][self.currentCell[1]] == "E":
                    print("Yol bulundu")
                    print(indiv.genes)
                    print ("Gen number", indiv.genNumber)
                    self.visualSolution(indiv)
                    count = indiv.genNumber
                    self.makeTable(count)
                    quit()
            else:
                indiv.visitScore = self.totalScore(tempMaze)
                self.calcFit(indiv)
                break;

    
    def visualSolution(self,solutionIndiv):
        self.resetMaze()
        self.currentCell = self.startCell
        for gen in solutionIndiv.genes:
            posibleMove = None
            if gen == "U" :
                posibleMove = [self.currentCell[0] - 1, self.currentCell[1]]
            elif gen == "D":
                posibleMove = [self.currentCell[0] + 1, self.currentCell[1]]
            elif gen == "R":
                posibleMove = [self.currentCell[0], self.currentCell[1] + 1]
            elif gen == "L":
                posibleMove = [self.currentCell[0], self.currentCell[1] -1]
            
            self.currentCell = posibleMove
            self.fillMove(RED)
            if self.maze[self.currentCell[0]][self.currentCell[1]] == "E":
                break


    def makeTable(self, count):
        array = [i for i in range(count)]
        plt.plot(array, self.bestFinessValues)
        plt.show()
    
    def totalScore(self,tempMaze):
        return np.sum(tempMaze)


    def CheckForVaildMove(self, posibleMove):

        if (posibleMove[0] >= 0 and posibleMove[0] < len(self.maze) and
                posibleMove[1] >= 0 and posibleMove[1] < len(self.maze[0])):

            if self.maze[posibleMove[0]][posibleMove[1]] != "#":
                return True

        return False
