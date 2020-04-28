from __future__ import division
import random
import math
import pygame
import numpy as np
import matplotlib.pyplot as plt
import time 
from Individual import Individual

WIDTH = 7
HEIGHT = 7
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0,0,255)
YELLOW = (0,255,255)
MARGIN = 3



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