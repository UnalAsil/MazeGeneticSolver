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



class Individual:
    def __init__(self, genNumber):
        self.genes = []
        self.fitnes = 0.0001
        self.visitScore = 0
        self.genNumber = genNumber
      

    def __repr__(self):
        return str(self.fitnes)