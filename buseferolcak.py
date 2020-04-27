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
        # indiv.visitScore = self.maze

        cikisaUzunlukX = abs(self.currentCell[0] - self.endCell[0]) #
        cikisaUzunlukY = abs(self.currentCell[1] - self.endCell[1]) # EKSI

        # baslangicaUzaklikX = abs(self.currentCell[0] - self.startCell[0]) 
        # baslangicaUzaklikY = abs(self.currentCell[1] - self.startCell[1]) # ARTI

        indiv.fitnes = 500000 -  10* math.sqrt(cikisaUzunlukX **2 + cikisaUzunlukY **2) - indiv.visitScore 
        # indiv.fitnes = 500000 -  cikisaUzunlukX **2 + cikisaUzunlukY **2 - indiv.visitScore 

   
    
    def walkInMaze(self, indiv):
        indiv.visitScore = 0
        tempMaze = np.zeros([self.boyut, self.boyut]) 
        self.currentCell = self.startCell
        carpmadanGittigi = 0
        # print(len(indiv.genes))
        if(indiv == self.bestIndiv):
            self.resetMaze()
            self.bestFinessValues.append(indiv.fitnes)
        for gen in indiv.genes:
            # print(gen)
            posibleMove = None
            if gen == "U" :
                posibleMove = [self.currentCell[0] - 1, self.currentCell[1]]
            elif gen == "D":
                posibleMove = [self.currentCell[0] + 1, self.currentCell[1]]
            elif gen == "R":
                posibleMove = [self.currentCell[0], self.currentCell[1] + 1]
            elif gen == "L":
                posibleMove = [self.currentCell[0], self.currentCell[1] -1]
            else:
                print("Warning! Invalid gene detected: " + gen)

            if self.CheckForVaildMove(posibleMove):
                self.currentCell = posibleMove
                
                tempMaze[self.currentCell[0]][self.currentCell[1]] += +1

                if(indiv == self.bestIndiv):
                    self.fillMove(RED)
                if self.maze[self.currentCell[0]][self.currentCell[1]] == "E":
                    print("Bulduk canim.")
                    print(indiv.genes)
                    # print(self.maze, sep='\n')
                    print ("Gen number", indiv.genNumber)
                    # self.fillMove(RED)
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
            # print(gen)
            posibleMove = None
            if gen == "U" :
                posibleMove = [self.currentCell[0] - 1, self.currentCell[1]]
            elif gen == "D":
                posibleMove = [self.currentCell[0] + 1, self.currentCell[1]]
            elif gen == "R":
                posibleMove = [self.currentCell[0], self.currentCell[1] + 1]
            elif gen == "L":
                posibleMove = [self.currentCell[0], self.currentCell[1] -1]
            else:
                print("Warning! Invalid gene detected: " + gen)
            
            self.currentCell = posibleMove
            self.fillMove(RED)
            if self.maze[self.currentCell[0]][self.currentCell[1]] == "E":
                break


    def makeTable(self, count):
        # array = list(range(0, count))
        # plt.plot(array, self.bestFinessValues, "ro")
        # plt.show
        array = [i for i in range(count)]
        plt.plot(array, self.bestFinessValues)
        # plt.axis([0, count, 0, self.bestIndiv.fitnes])
        plt.show()
        # input("Bitmesi icin basiniz")
    
    def totalScore(self,tempMaze):
        return np.sum(tempMaze)


    def CheckForVaildMove(self, posibleMove):

        if (posibleMove[0] >= 0 and posibleMove[0] < len(self.maze) and
                posibleMove[1] >= 0 and posibleMove[1] < len(self.maze[0])):

            if self.maze[posibleMove[0]][posibleMove[1]] != "#":
                return True

        return False


class Individual:
    def __init__(self, genNumber):
        self.genes = []
        self.fitnes = 0.0001
        self.visitScore = 0
        self.genNumber = genNumber
      

    def __repr__(self):
        return str(self.fitnes)

class GA:

    genGenarationSource = ["U", "D", "R", "L"]

    def __init__(self, populationSize, mutotianRate,maze,GEN_LENGTH):
        self.populationSize = populationSize
        self.mutotianRate = mutotianRate
        self.maze = maze
        self.population  = []
        self.GEN_LENGTH = GEN_LENGTH
        self.yuzde = int(populationSize/20)
        self.fitnessValues = []
        for i in range(self.populationSize):
            indiv = Individual(0)
            for j in range (self.GEN_LENGTH):
                indiv.genes.append(random.choice(GA.genGenarationSource))
            self.population.append(indiv)
        # print(self.yuzde)
   
    def Normalize(self):
        sum = 0
        isEqual1= 0
        for i in self.population:
            sum += i.fitnes

        for i in self.population:
            i.fitnes /= sum
            isEqual1 += i.fitnes
            
        self.population.sort(key = lambda a : a.fitnes )
        
        
    def Fitness(self):
        for indiv in self.population:
            self.maze.walkInMaze(indiv)

    def evrilme(self):
        count = 0
        MAXGEN = 10000000
        while count < MAXGEN :
            print(count)
            count += 1
            nextPopulation = []
            self.Fitness()
            self.Normalize() # Siralanmis dizi var normalizedda
            bestIndivForVisual = self.population[len(self.population)-1]
            # print(bestIndivForVisual)
            self.maze.bestIndiv = bestIndivForVisual

            # self.population[len(self.population)-1].visitScore = 0
            # self.population[len(self.population)-2].visitScore = 0
            # nextPopulation.append(self.population[len(self.population)-1]) # -> Elite child.
            # nextPopulation.append(self.population[len(self.population)-2])

            for i in range(self.yuzde):
                nextPopulation.append(self.population[len(self.population)-i-1])
            
            AKUM = []
            AKUM.append(self.population[0].fitnes)
            for i in range (1,self.populationSize):
                AKUM.append(AKUM[i-1] + self.population[i].fitnes)

            for i in range (self.populationSize - self.yuzde):
                parent1 = self.randomSelect(AKUM)
                parent2 = self.randomSelect(AKUM)
                child = self.CrossOver(parent1,parent2)
                child.genNumber = count
                if random.uniform(0,1) < self.mutotianRate:
                    child = self.mutateChild(child)
                
                nextPopulation.append(child)
            self.population = nextPopulation

    def randomSelect(self, AKUM):
        uyg = random.uniform(0,1)
 
        for j in range(len(AKUM)):
            if uyg <= AKUM[j]:
                return self.population[j]



    def CrossOver(self, parent1, parent2):

        child = Individual(0)
        crossPoint1 = random.randint(0, self.GEN_LENGTH - 1)

        crossPoint2 = random.randint(0, self.GEN_LENGTH - 1)

        crossPoint23 = random.randint(0, self.GEN_LENGTH - 1)

        if crossPoint1<crossPoint2 :

            child.genes = parent1.genes[:crossPoint1] + parent2.genes[crossPoint1:crossPoint2] + parent1.genes[crossPoint2:]
        
        else :
            child.genes = parent1.genes[:crossPoint2] + parent2.genes[crossPoint2:crossPoint1] + parent1.genes[crossPoint1:]

        return child


    def mutateChild(self,child):
        temp = int(self.GEN_LENGTH / 10)
        dummy = []
        for i in range(temp):
            dummy.append(random.choice(GA.genGenarationSource))


        mutaionPoint = random.randint(0, self.GEN_LENGTH - temp-1)

        for i in range(temp):
            child.genes[mutaionPoint+i] = dummy[i]
        return child

    def printPop(self):
        for indiv in self.population:
            print("\nIndiv :", indiv.genes)             



if __name__ == "__main__":
    boyut = int(input("Labirentin boyutlarini giriniz"))
    
    engel = int(input("Engel sayisini giriniz"))

    tempGEN = boyut * 10
    print("After ", tempGEN)
    maze = Maze(boyut+2, engel)
    
    evrim = GA(200,0.1,maze,tempGEN)

    evrim.evrilme()

