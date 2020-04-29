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

    genGenarationSource = ["U", "D", "R", "L"] # Bireyin sahip olabilecegi genler.

    def __init__(self, populationSize, mutotianRate,maze,GEN_LENGTH):
        self.populationSize = populationSize #Nesilin populasyon buyuklugu.
        self.mutotianRate = mutotianRate # Mutasyon orani
        self.maze = maze 
        self.population  = []
        self.GEN_LENGTH = GEN_LENGTH # Bireyin gen uzunlugu.
        self.yuzde = int(populationSize/20) # Yuzde degiskeninde her populasyonun en iyi %5 ini elit child yapip gelecek nesle direkt aktarmak amaciyla kullanildi.
        self.fitnessValues = []
        for i in range(self.populationSize): # Ilk populasyon random olusturuluyor.
            indiv = Individual(0)
            for j in range (self.GEN_LENGTH):
                indiv.genes.append(random.choice(GA.genGenarationSource))
            self.population.append(indiv)
   
    def Normalize(self): #Fitness degelerini normalize edip siralayan fonksiyon.
        sum = 0
        isEqual1= 0
        for i in self.population:
            sum += i.fitnes

        for i in self.population:
            i.fitnes /= sum
            isEqual1 += i.fitnes
            
        self.population.sort(key = lambda a : a.fitnes )
        
        
    def Fitness(self): # Populasyondaki bireyler teker teker labirentte yurutulup fitness puanlari hesaplaniyor.
        for indiv in self.population:
            self.maze.walkInMaze(indiv)

    def evrilme(self): # MAXGEN den kucuk oldugu surece genetik algoritma calisiyor. Calisma suresince bir yol bulursa cikis yapiyor.
        count = 0
        MAXGEN = 10000000
        while count < MAXGEN :
            print(count)
            count += 1
            nextPopulation = [] # Gelecek populasyon,
            self.Fitness()  # Mevcut popualsyonun fitness degerler hesaplaniyor.
            self.Normalize() # Hesaplanan fitness degerleri normalize ediliyor.
            bestIndivForVisual = self.population[len(self.population)-1]
            self.maze.bestIndiv = bestIndivForVisual

            for i in range(self.yuzde): # %5 lik kisim elit child olup, gelecek populasyona direkt aktariliyor.
                nextPopulation.append(self.population[len(self.population)-i-1])
            
            AKUM = []
            AKUM.append(self.population[0].fitnes)
            for i in range (1,self.populationSize): # Akumulatif degerleri hesaplaniyor.
                AKUM.append(AKUM[i-1] + self.population[i].fitnes)

            for i in range (self.populationSize - self.yuzde):  # Cross over vu mutasyon islemleri gerceklestiriliyor.
                parent1 = self.randomSelect(AKUM) # Rulet carki yapiliyor, fitnes degeri yuksek olanin secilme sansi daha yukek.
                parent2 = self.randomSelect(AKUM)
                child = self.CrossOver(parent1,parent2)
                child.genNumber = count
                if random.uniform(0,1) < self.mutotianRate: 
                    child = self.mutateChild(child)
                
                nextPopulation.append(child) # olusturulan child gelecek populasyona ekleniyor.
            self.population = nextPopulation

    def randomSelect(self, AKUM): # Rulet carki, fitness degeri ne kadar yuksekse o kadar cok secilme ihtimali var.
        uyg = random.uniform(0,1)
 
        for j in range(len(AKUM)):
            if uyg <= AKUM[j]:
                return self.population[j]



    def CrossOver(self, parent1, parent2): #Cross over rastgele iki yerden kesilip carplazlaniyor.

        child = Individual(0)
        crossPoint1 = random.randint(0, self.GEN_LENGTH - 1)

        crossPoint2 = random.randint(0, self.GEN_LENGTH - 1)

        crossPoint23 = random.randint(0, self.GEN_LENGTH - 1)

        if crossPoint1<crossPoint2 :

            child.genes = parent1.genes[:crossPoint1] + parent2.genes[crossPoint1:crossPoint2] + parent1.genes[crossPoint2:]
        
        else :
            child.genes = parent1.genes[:crossPoint2] + parent2.genes[crossPoint2:crossPoint1] + parent1.genes[crossPoint1:]

        return child


    def mutateChild(self,child): # Gen uzunlugunun %10 u kadar rastgele bir gen parcasi olusturulup, childin secilen rastgele noktasina yerlestiriliyor.
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