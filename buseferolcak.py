from __future__ import division
import random
import math
import pygame
import numpy as np
##

WIDTH = 20
HEIGHT = 20
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0,0,255)
YELLOW = (0,255,255)
MARGIN = 5

###
class Maze:
    def __init__(self,boyut, engel):

        self.engel = engel
        self.boyut = boyut

        grid = []
        for row in range(boyut):
            # Add an empty array that will hold each cell
            # in this row
            grid.append(["#"])
            for column in range(boyut-2):
                if row == 0 or row == boyut-1:
                    grid[row].append("#")
                else :
                     grid[row].append("-")  # Append a cel
            grid[row].append("#")
        

        # for row in range(6,self.boyut-5,4):
        #     for col in range(6, self.boyut-5, 4):
        #         x = random.uniform(0,1)
        #         print("PATIR PATIR PATLIYOR",row,col)
        #         if x > 0.5:# yukardan asagiya
        #             # grid[row].append("#")
        #             y = random.uniform(0,1)
        #             if y<0.25:
        #                 grid[row][col]= "#"
        #                 grid[row+1][col]="#"
        #                 grid[row+2][col]="#"
        #                 grid[row+3][col]="#"
        #             elif y<0.5:
        #                 grid[row][col+1]= "#"
        #                 grid[row+1][col+1]="#"
        #                 grid[row+2][col+1]="#"
        #                 grid[row+3][col+1]="#"
        #             elif y<0.75:
        #                 grid[row][col+2]= "#"
        #                 grid[row+1][col+2]="#"
        #                 grid[row+2][col+2]="#"
        #                 grid[row+3][col+2]="#"
        #             else:
        #                 grid[row][col+3]= "#"
        #                 grid[row+1][col+3]="#"
        #                 grid[row+2][col+3]="#"
        #                 grid[row+3][col+3]="#"
        #         else:# yatay
        #             y = random.uniform(0,1)
        #             if y<0.25:
        #                 grid[row][col]= "#"
        #                 grid[row][col+1]="#"
        #                 grid[row][col+2]="#"
        #                 grid[row][col+3]="#"
        #             elif y<0.5:
        #                 grid[row+1][col]= "#"
        #                 grid[row+1][col+1]="#"
        #                 grid[row+1][col+2]="#"
        #                 grid[row+1][col+3]="#"
        #             elif y<0.75:
        #                 grid[row+2][col]= "#"
        #                 grid[row+2][col+1]="#"
        #                 grid[row+2][col+2]="#"
        #                 grid[row+2][col+3]="#"
        #             else:
        #                 grid[row+3][col]= "#"
        #                 grid[row+3][col+1]="#"
        #                 grid[row+3][col+2]="#"
        #                 grid[row+3][col+3]="#"
        self.maze = grid

        self.maze[3][3] = "S"
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

        WINDOW_SIZE = [500, 500]
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption("Array Backed Grid")

        clock = pygame.time.Clock()

        MARGIN = 5
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
    # Cikisi uzunluk +
    # Baslangica uzaklik +
    # 

    def fillMove(self):
        color = RED
        pygame.draw.rect(self.screen,
                            color,
                            [(MARGIN + WIDTH) * self.currentCell[1] + MARGIN,
                            (MARGIN + HEIGHT) * self.currentCell[0] + MARGIN,
                            WIDTH,
                            HEIGHT])
        pygame.display.flip()
    
    def resetMaze(self):
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


    def calcFit(self,indiv,carpmadanGittigi):
        # indiv.visitScore = self.maze

        cikisaUzunlukX = abs(self.currentCell[0] - self.endCell[0]) #
        cikisaUzunlukY = abs(self.currentCell[1] - self.endCell[1]) # EKSI

        baslangicaUzaklikX = abs(self.currentCell[0] - self.startCell[0]) 
        baslangicaUzaklikY = abs(self.currentCell[1] - self.startCell[1]) # ARTI


        # indiv.fitnes =  (baslangicaUzaklikX+ baslangicaUzaklikY) / (carpmadanGittigi+1) + 2* 20 - (cikisaUzunlukX + cikisaUzunlukY)
        # a = abs(self.currentCell[0] + self.currentCell[1] ) / math.sqrt(2)
        # indiv.fitnes = 100 - cikisaUzunlukX **2 + cikisaUzunlukY **2 - a*a*a + (baslangicaUzaklikX**2+baslangicaUzaklikY**2)
        # indiv.fitnes = 200 - math.sqrt(cikisaUzunlukX **2 + cikisaUzunlukY **2) + indiv.visitScore  + carpmadanGittigi
        # indiv.fitnes = 200 - cikisaUzunlukX + cikisaUzunlukY
        # indiv.fitnes = 200 - math.sqrt(cikisaUzunlukX **2 + cikisaUzunlukY **2)
        # indiv.fitnes = (math.sqrt(baslangicaUzaklikX **2 + baslangicaUzaklikY **2))/(math.sqrt(cikisaUzunlukX **2 + cikisaUzunlukY **2))*100
        # indiv.fitnes = 200 - math.sqrt(cikisaUzunlukX **2 + cikisaUzunlukY **2) - indiv.visitScore + carpmadanGittigi
        indiv.fitnes = 500000 - (cikisaUzunlukX **2 + cikisaUzunlukY **2) - indiv.visitScore 
        # indiv.fitnes = 200 - math.sqrt(cikisaUzunlukX **2 + cikisaUzunlukY **2) - indiv.visitScore
    
    def walkInMaze(self, indiv):
        # tempMaze = np.zeros([20, 20]) 
        # indiv.visitScore = 0


        self.currentCell = self.startCell
        carpmadanGittigi = 0
        # print("\n**")
        # if self.PRINTMAZE > 100 :
        #     self.resetMaze()
        #     self.PRINTMAZE /=100
        # self.PRINTMAZE+=1
        self.resetMaze()
        # print(indiv.genes)
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
            # print(self.maze[posibleMove[0]][posibleMove[1]])
            # print(posibleMove, self.currentCell)
            if self.CheckForVaildMove(posibleMove):
                self.currentCell = posibleMove

                #
                # tempMaze[self.currentCell[0]][self.currentCell[1]] += -1

                #BURDA MAZEI BOYA
                self.fillMove()
                # print(self.maze[self.currentCell[0]][self.currentCell[1]])
                if indiv.visitScore == 0 and self.maze[self.currentCell[0]][self.currentCell[1]] == "E":
                    print("Bulduk canim.")
                    print(indiv.genes)
                    # print(self.maze, sep='\n')
                    print ("Gen number", indiv.genNumber)
                    quit()
                carpmadanGittigi+=1
            # else:
            #     indiv.visitScore = self.totalScore(tempMaze)
            #     self.calcFit(indiv, carpmadanGittigi)
            #     break;
            else:
                indiv.visitScore += 1
                continue
            self.calcFit(indiv,carpmadanGittigi)


    
    def totalScore(self,tempMaze):
        print (np.sum(tempMaze))
        return np.sum(tempMaze)


    def CheckForVaildMove(self, posibleMove):

        if (posibleMove[0] >= 0 and posibleMove[0] < len(self.maze) and
                posibleMove[1] >= 0 and posibleMove[1] < len(self.maze[0])):

            if self.maze[posibleMove[0]][posibleMove[1]] != "#":
                return True

        return False


class Individual:
    GEN_LENGTH = 300
    def __init__(self, genNumber):
        self.genes = []
        self.fitnes = 0.0001
        self.visitScore = 0
        self.genNumber = genNumber

    def __repr__(self):
        return str(self.fitnes)

class GA:

    genGenarationSource = ["U", "D", "R", "L"]

    def __init__(self, populationSize, mutotianRate,maze):
        self.populationSize = populationSize
        self.mutotianRate = mutotianRate
        self.maze = maze
        self.population  = []

        for i in range(self.populationSize):
            indiv = Individual(0)
            for j in range (Individual.GEN_LENGTH):
                indiv.genes.append(random.choice(GA.genGenarationSource))
            self.population.append(indiv)
    
   
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
        #Populasyonun her bireyi, labirente yollanmali.
        for indiv in self.population:
            # print(indiv.genes)
            self.maze.walkInMaze(indiv)

    def evrilme(self):
        count = 0
        MAXGEN = 10000000
        print("Populasyon uzunlugu: ", len(self.population))


        while count < MAXGEN:
            # print(count)
            count += 1
            nextPopulation = []
            self.Fitness()
            self.Normalize() # Siralanmis dizi var normalizedda
            # print("MAKSFIT ", self.population[0].fitnes)
            self.population[len(self.population)-1].visitScore = 0
            self.population[len(self.population)-2].visitScore = 0
            nextPopulation.append(self.population[len(self.population)-1]) # -> Elite child.
            nextPopulation.append(self.population[len(self.population)-2])
            
            AKUM = []
            AKUM.append(self.population[0].fitnes)
            # # print("AKUM HESABINDA INDIV.FIT", self.population[0].fitnes )
            for i in range (1,self.populationSize):
                # print("AKUM HESABINDA INDIV.FIT", self.population[i].fitnes )
                AKUM.append(AKUM[i-1] + self.population[i].fitnes)

            # # print("AKUM:" , AKUM[len(self.population)-1] )
            for i in range (self.populationSize-2):
                parent1 = self.randomSelect(AKUM)
                parent2 = self.randomSelect(AKUM)
                child = self.CrossOver(parent1,parent2)
                child.genNumber = count
                if random.uniform(0,1) < 0.1:
                    child = self.mutateChild(child)
                
                nextPopulation.append(child)
            self.population = nextPopulation
            # print("Populasyon uzunlugu: ", len(self.population))

    def randomSelect(self, AKUM):
        uyg = random.uniform(0,1)
 
        for j in range(len(AKUM)):
            if uyg <= AKUM[j]:
                # print(self.population[j])
                return self.population[j]



    def CrossOver(self, parent1, parent2):

        child = Individual(0)
        crossPoint1 = random.randint(0, Individual.GEN_LENGTH - 1)

        crossPoint2 = random.randint(0, Individual.GEN_LENGTH - 1)

        crossPoint23 = random.randint(0, Individual.GEN_LENGTH - 1)

        if crossPoint1<crossPoint2 :

            child.genes = parent1.genes[:crossPoint1] + parent2.genes[crossPoint1:crossPoint2] + parent1.genes[crossPoint2:]
        
        else :
            child.genes = parent1.genes[:crossPoint2] + parent2.genes[crossPoint2:crossPoint1] + parent1.genes[crossPoint1:]


        # child.genes = parent1.genes[:crossPoint1] + parent2.genes[crossPoint1:crossPoint2] + parent1.genes[crossPoint2:]
        print(len(child.genes))

        # child.genes = parent1.genes[:crossPoint1] + parent2.genes[crossPoint1:]

        return child


    def mutateChild(self,child):
        for i in range(2):
            mutaionPoint = random.randint(0, Individual.GEN_LENGTH - 1)

            child.genes[mutaionPoint] = random.choice(GA.genGenarationSource)

        return child

    def printPop(self):
        for indiv in self.population:
            print("\nIndiv :", indiv.genes)             


if __name__ == "__main__":

    boyut = int(input("Labirentin boyutlarini giriniz"))
    
    
    Engel = int(input("Engel sayisini giriniz"))

    maze = Maze(boyut, Engel)
    
    evrim = GA(20,0.05,maze)
    # input("AAA")
    # for i in range(10):
    #     print(evrim.population[i].genes)
    evrim.evrilme()

