from random import randint
class River:
  def __init__(self, riverS, bearS, fishS):
    
    self.population = 0
    self.num_bears = bearS
    self.num_fish = fishS
    self.animals = []
    self.size = riverS
    self.babies = []
    self.river = [["🟦" for b in range(riverS)] for a in range(riverS)]
    self.__init_population()


  def __init_population(self):
    for a in range(self.num_fish):
      self.__place_baby(Fish)
    for b in range(self.num_bears):
      self.__place_baby(Bear)
    

  def __place_baby(self,A):
    x = randint(0,len(self.river)-1)
    y = randint(0,len(self.river)-1)
    while self.river[y][x] != "🟦":
      x = randint(0,len(self.river)-1)
      y = randint(0,len(self.river)-1)
    aN = A(y,x)
    print(f"\nA {aN.type}  has been born")
    self.river[y][x] = aN
    self.animals.append(aN)
    self.population += 1
  
  
  def redraw_cells(self,animal,x,y):
    if self.river[animal.y+y][animal.x+x] == "🟦":
      self.river[animal.y+y][animal.x+x] = animal
      self.river[animal.y][animal.x] = "🟦"
      if animal.type == "🐻":
        animal.starve(self)
      animal.y = animal.y+y
      animal.x = animal.x+x
    else:
      flag = animal.collision(self, animal.x+x,animal.y+y)
      if flag == "Continue":
        self.river[animal.y+y][animal.x+x] = animal
        self.river[animal.y][animal.x] = "🟦"
        animal.y = animal.y+y
        animal.x = animal.x+x #check these and check if move yes no maybe because breed
      elif flag == "Birth":
        if animal.type == "🐻":
          self.babies.append(Bear)
        else:
          self.babies.append(Fish)

  def animal_death(self,other):
    print(f"\nA {other.type}  has died") ############ Disappearing Bears magic trick
    self.river[other.y][other.x] = "🟦"
    self.animals.remove(other)
    self.population -= 1

    


  def new_day(self):
    filledFlag = 0
    freeSpace = 0
    for a in self.river:
      for b in a:
        if b != "🟦":
          filledFlag += 1
        else:
          freeSpace += 1

    flagFish = "No fishies?"
    flagBear = "No bears, bro?"
    flagFishamount = 0
    flagBearamount = 0


    for a in self.animals:
      a.bred_today = False
      if a.type == "🐟":
        flagFish = True
        flagFishamount += 1 
      elif a.type == "🐻":
        flagBear = True
        flagBearamount += 1

        #-------
    if flagFish != True or flagBear != True:
      return True, "one or more of the animals have gone extinct in this river."
    if flagFishamount <= 1 or flagBearamount <= 1: 
      return True, "one or more of the animals can no longer breed."
    if filledFlag+10 == len(self.river)*len(self.river):
      return True, "the board has been filled."
        #
    for a in self.animals:
      if a.bred_today == False:
        a.move(self)
    
    babyAmount = 0
    for a in self.babies:
      babyAmount += 1
    if freeSpace < len(self.babies):
      return True, "the babies have exceeded the rivers size, they have overrun the population."
    for a in self.babies:
      self.__place_baby(a)

    return False, "There was once a boy on some road in illinois, his name was marvin, marvin had crappy shoes because he forgot his at the bottom of a river, that river had a few bears, and a few fish, some of them occasionally disappears, but marvin didn't mind."
  
  
  def __getitem__(self,i):
    return self.river[i]


  def __str__(self):
    temp = ''
    for a in self.river:
      temp += "\n  "
      for b in a:
        temp += str(b)+" "
    return temp
  def __repr__(self):
    return self.river

class Animal:
  def __init__(self, ym, xm):
    self.x = xm
    self.y = ym
    self.bred_today = False
  
  def death(self,board):
    board.animal_death(self)

  def move(self,board):
    x = randint(-1,1)
    y = randint(-1,1)
    while self.x + x == -1 or self.y + y == -1 or self.x+x >= board.size or self.y+y >= board.size:
      x = randint(-1,1)
      y = randint(-1,1)

    print(f"{self}  moved from ({self.x}, {self.y}) to ({self.x + x}, {self.y + y})")
    board.redraw_cells(self, x, y)


  def collision(self,board, x, y):  
    if self.type == board[y][x].type:
      if self.bred_today == True or board[y][x].bred_today == True:
        print(f"\nThe creation of a {self.type}  was attempted but failed!")
        return "This project gave me a headache!"
      else:
        self.bred_today = True
        board[y][x].bred_today = True
        return "Birth"
    elif self.type == "🐟":
      print(f"\nA {self.type} has ran into a bear!\n")
      board[y][x].consume(self,board)
      return "Hows it going"
    elif board[y][x].type == "🐟":
      print(f"\nA {self.type} has ran into a fish!\n")
      self.consume(board[y][x],board)
      return "Continue"

      
  def __str__(self):
    return self.type
  def __repr__(self):
    return self.type

class Fish(Animal):
  def __init__(self,y,x):
    super().__init__(y, x)
    self.type = "🐟"

class Bear(Animal):
  def __init__(self,y,x):
    super().__init__(y, x)
    self.type = "🐻"
    self.lives = 10
    self.max_lives = 5
    self.eaten_today = False
    self.days_starved = 0

  def starve(self,board):
    self.days_starved += 1
    if self.days_starved == self.max_lives:
      self.death(board)
    self.lives -= 1
    if self.lives == 0:
      self.death(board)
  def consume(self,other,board):
    self.days_starved = 0 
    other.death(board)
    self.lives -= 1
    if self.lives == 0:
      self.death(board)