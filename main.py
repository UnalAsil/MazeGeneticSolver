from Maze import Maze
from Individual import Individual
from GA import GA

WIDTH = 7
HEIGHT = 7
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0,0,255)
YELLOW = (0,255,255)
MARGIN = 3


if __name__ == "__main__":
    boyut = int(input("Labirentin boyutlarini giriniz"))
    
    engel = int(input("Engel sayisini giriniz"))

    tempGEN = boyut * 10
    print("After ", tempGEN)
    maze = Maze(boyut+2, engel)
    
    evrim = GA(200,0.1,maze,tempGEN)

    evrim.evrilme()

