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

        self.engel = engel #Engel sayisi
        self.boyut = boyut #labirentin boyutu
        self.bestIndiv = None # En iyi fitness degerine sahip bireyi saklamak amaciyla kullanildi.
        self.bestFinessValues = [] # En iyi fitness degerine sahip bireyleri gorsellestirmek amaciyla kullanildi

        grid = []
        for row in range(boyut): ## Labirent olusturuluyor ve etrafi duvarlarla cevriliyor.
            grid.append(["#"])
            for column in range(boyut-2):
                if row == 0 or row == boyut-1:
                    grid[row].append("#")
                else :
                     grid[row].append("-") 
            grid[row].append("#")
        
        tempGrid = grid

        for i in range(engel): ## Istenen engel sayisi kadar rastgele engel olustruluyor.
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
        self.maze[boyut-2][boyut-2] = "E" ## Baslangic ve bitis noktalari veriliyor.


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
    

    def visual(self): # Labirenti bastirmak amaciyla kullanilan fonksiyon.
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

    def fillMove(self, renk): # Bireyin yaptigi hareketleri gostermek amaciyla kullanildi.
        color = renk
        pygame.draw.rect(self.screen,
                            color,
                            [(MARGIN + WIDTH) * self.currentCell[1] + MARGIN,
                            (MARGIN + HEIGHT) * self.currentCell[0] + MARGIN,
                            WIDTH,
                            HEIGHT])
        pygame.display.flip()
    
    def resetMaze(self): # Her bireyde labirent ilk haline geri dondruluyor.
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


    def calcFit(self,indiv): # Bireyin fitness puanini hesaplayan fonksiyon.
 
        cikisaUzunlukX = abs(self.currentCell[0] - self.endCell[0]) #
        cikisaUzunlukY = abs(self.currentCell[1] - self.endCell[1]) # 
        #indiv.visitScorede, bireyin yapmis oldugu looplar ve cikisa olan uzunlugu cezalandirici oluyor.
        #Boylece en az loop yapan ve cikisa en yakin birey en iyi birey oluyor.
        indiv.fitnes = 500000 -  10* math.sqrt(cikisaUzunlukX **2 + cikisaUzunlukY **2) - indiv.visitScore 

   
    def walkInMaze(self, indiv):
        indiv.visitScore = 0
        tempMaze = np.zeros([self.boyut, self.boyut]) # Yapmis oldugu looplari yakalamak amaciyla tutuldu.
        self.currentCell = self.startCell
        carpmadanGittigi = 0
        if(indiv == self.bestIndiv): # En iyi bireyi ekrana basiyor.
            self.resetMaze()
            self.bestFinessValues.append(indiv.fitnes)
        for gen in indiv.genes: # Birey, labirent icinde geziyor, sinirlari asarsa yahut bir engele carparsa birey oldurulup fitness degeri hesaplaniyor.
            posibleMove = None
            if gen == "U" :
                posibleMove = [self.currentCell[0] - 1, self.currentCell[1]]
            elif gen == "D":
                posibleMove = [self.currentCell[0] + 1, self.currentCell[1]]
            elif gen == "R":
                posibleMove = [self.currentCell[0], self.currentCell[1] + 1]
            elif gen == "L":
                posibleMove = [self.currentCell[0], self.currentCell[1] -1]

            if self.CheckForVaildMove(posibleMove): # Hareketin uygunlugu test ediliyor.
                self.currentCell = posibleMove
                
                tempMaze[self.currentCell[0]][self.currentCell[1]] += +1

                if(indiv == self.bestIndiv): # Hareket ekranda gosteriliyor.
                    self.fillMove(RED)
                if self.maze[self.currentCell[0]][self.currentCell[1]] == "E": # Eger cikisa gelmisse, gorsellestiriliyor, tablosu hazirlaninip cikis yapiliyor.
                    print("Yol bulundu")
                    print(indiv.genes)
                    print ("Gen number", indiv.genNumber)
                    self.visualSolution(indiv)
                    count = indiv.genNumber
                    self.makeTable(count)
                    quit()
            else: # Birey oldu fitness degeri hesaplaniyor.
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


    def makeTable(self, count): # nesillere gore sahip olunan en iyi fitnes degerleri ekrana basiliyor.
        array = [i for i in range(count)]
        plt.plot(array, self.bestFinessValues)
        plt.show()
    
    def totalScore(self,tempMaze):
        return np.sum(tempMaze)


    def CheckForVaildMove(self, posibleMove): # Hareketin uygunluguna bakiliyor.

        if (posibleMove[0] >= 0 and posibleMove[0] < len(self.maze) and
                posibleMove[1] >= 0 and posibleMove[1] < len(self.maze[0])):

            if self.maze[posibleMove[0]][posibleMove[1]] != "#":
                return True

        return False
