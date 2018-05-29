import sense_hat
import time
import random
#class
class Block:

  def __init__(self):
    self.x = 0
    self.y = 0
    self.isUp = False
    self.isDown = False
    self.isLeft = False
    self.isRight = False
    self.nextIndex = 0
    self.previousIndex = 0

  def isExistWay(self):
    if self.isUp == True:
      return True
    if self.isDown == True:
      return True
    if self.isLeft == True:
      return True
    if self.isRight == True:
      return True
    return False
#!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-
s = sense_hat
hat = sense_hat.SenseHat()
#!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-
#map data, maps length always = 6
directoryMap = 'MapData/'
maps = [('MazeMapa.txt','MazeMapc.txt'),
        ('MazeMa65x65a.txt','MazeMa65x65c.txt'),
        ('MazeMa65x65v02a.txt','MazeMa65x65v02c.txt'),
        ('MazeMapa.txt','MazeMapc.txt'),
        ('MazeMapa.txt','MazeMapc.txt'),
        ('MazeMapa.txt','MazeMapc.txt')]
#editable var
BotDelayMove = 0.2
BotDelayBack = 0.1
PlayerDelay = 0.1
#constant var
Map_a = ''
Map_c = ''
width =  32
height = 32
maze = []
graphicMaze = []
player = []
pixels = []
gameover = False
startPosition = [3,27]
black = (0,0,0)
playerColor = (0,255,255)
isStart = False
#methods
#space = 0, wall = 1, player = 2, goal = 3, border color it 

def InitScreen():
  for i in range(0,64):
    pixels.append(black)

def LoadGame(mapCode):
  #loadMapData
  global Map_a
  global maps
  global Map_c
  global directoryMap
  Map_a = directoryMap + maps[mapCode][0]
  Map_c = directoryMap + maps[mapCode][1]
  fileMapa = open(Map_a,'r')
  fileMapc = open(Map_c,'r')
  global width
  global height
  global playerColor
  global player
  global startPosition
  global maze
  global graphicMaze
  maze = []
  graphicMaze = []
  #set map properties value
  width = int(fileMapa.readline())
  height = int(fileMapa.readline())
  playerColor = ConvertToTuple(fileMapa.readline())
  temp = ConvertIndexFrom2DArrayTo1DArray(int(fileMapa.readline()),width,height)
  player = [temp[0],temp[1]]
  startPosition = [player[0],player[1]]
  #create map
  for i in range(0,height):
    for k in range(0,width):
      maze.append(int(fileMapa.readline()))
      graphicMaze.append(ConvertToTuple(fileMapc.readline()))
  fileMapa.close()
  fileMapc.close()
      
def ConvertToTuple(value):
  temp = str(value).split('(')[1].split(')')[0].split(',')
  return (int(temp[0]),int(temp[1]),int(temp[2]))

def ConvertIndexFrom2DArrayTo1DArray(index1D,Width2D,Height2D):
  x = int(index1D % Width2D)
  y = int((index1D - x)/Height2D)
  return [x,y]

def GetPlayerGraphicPosition():
  result = [0,0,0,0]
  result[0] = player[1] * width + player[0]
  result[1] = player[1] * width + player[0] + 1
  result[2] = (player[1] + 1) * width + player[0]
  result[3] = (player[1] + 1) * width + player[0] + 1
  return result

def SetPlayerValueOnMap(value):
  playerGraphicIndex = GetPlayerGraphicPosition()
  maze[playerGraphicIndex[0]] = value
  maze[playerGraphicIndex[1]] = value
  maze[playerGraphicIndex[2]] = value
  maze[playerGraphicIndex[3]] = value

def CheckAvailableTop():
  v1 = (player[1] -1) * width + player[0]
  v2 = (player[1] -1) * width + player[0] + 1
  if maze[v1] == 0 and maze[v2] == 0:
    return 1
  elif maze[v1] == 3 and maze[v2] == 3:
    return 2
  return 0
  
def CheckAvailableDown():
  v1 = (player[1] + 2) * width + player[0]
  v2 = (player[1] + 2) * width + player[0] + 1
  if maze[v1] == 0 and maze[v2] == 0:
    return 1
  elif maze[v1] == 3 and maze[v2] == 3:
    return 2
  return 0

def CheckAvailableLeft():
  v1 = player[1] * width + player[0] - 1
  v2 = (player[1] + 1) * width + player[0] - 1
  if maze[v1] == 0 and maze[v2] == 0:
    return 1
  elif maze[v1] == 3 and maze[v2] == 3:
    return 2
  return 0
  
def CheckAvailableRight():
  v1 = player[1] * width + player[0] + 2
  v2 = (player[1] + 1) * width + player[0] + 2
  if maze[v1] == 0 and maze[v2] == 0:
    return 1
  elif maze[v1] == 3 and maze[v2] == 3:
    return 2
  return 0

def Render(delayTime):
  for i in range(0,8):
    for k in range(0,8):
      pIndex = i*8 + k
      mIndex = (player[1] - 3 + i)* width + (player[0] - 3) + k 
      pixels[pIndex] = graphicMaze[mIndex]
  
  SetPlayerValueOnMap(2)
  pixels[27] = playerColor
  pixels[28] = playerColor
  pixels[35] = playerColor
  pixels[36] = playerColor
  s.SenseHat().set_pixels(pixels)
  time.sleep(delayTime)

def GetInputCode():
  global hat
  events = hat.stick.get_events()
  if len(events)>0:
    if events[0].action !='release':
      e = events[0]
      if e.direction == 'up':
        return 1
      elif e.direction == 'down':
        return 2
      elif e.direction == 'left':
        return 3
      elif e.direction == 'right':
        return 4
      elif e.direction == 'middle' and events[0].action == 'pressed':
        return 5
  return 0

def GetInputDownCode():
  global hat
  events = hat.stick.get_events()
  if len(events)>0:
    if events[0].action =='pressed':
      e = events[0]
      if e.direction == 'up':
        return 1
      elif e.direction == 'down':
        return 2
      elif e.direction == 'left':
        return 3
      elif e.direction == 'right':
        return 4
      elif e.direction == 'middle':
        return 5
  return 0

def ValidatePlayerPosition():
  if player[1] < 3:
    player[1] = 3
  if player[1] > height - 5:
    player[1] = height - 5
  if player[0] < 3:
    player[0] = 3
  if player[0] > width - 5:
    player[0] = width - 5

def InputProcessing():
  #
  global isStart
  SetPlayerValueOnMap(0)
  #
  inputCode = GetInputCode()
  if inputCode == 1 and CheckAvailableTop() == 1: #UP
    player[1] -= 1
    isStart = True
  elif inputCode == 2 and CheckAvailableDown() == 1: #DOWN
    player[1] += 1
    isStart = True
  elif inputCode == 3 and CheckAvailableLeft() == 1: #LEFT
    player[0] -= 1
    isStart = True
  elif inputCode == 4 and CheckAvailableRight() == 1: #RIGHT
    player[0] += 1
    isStart = True
  elif CheckAvailableTop() == 2 or CheckAvailableDown() == 2 or CheckAvailableLeft() == 2 or CheckAvailableRight() == 2:
    GameOver()
  elif inputCode == 5: #Reset
    ResetLevel()
  #
  ValidatePlayerPosition()
  SetPlayerValueOnMap(2)

def ResetLevel():
  SetPlayerValueOnMap(0)
  global player
  player = [startPosition[0],startPosition[1]]
  ValidatePlayerPosition()
  SetPlayerValueOnMap(2)

def GameOver():
  global gameover
  gameover = True

def ResetGame():
  global gameover
  global player
  global steps
  global isGoal
  global curIndex
  curIndex = 0
  isGoal = False
  steps = []
  gameover = False
  player = []

def DisplaySelectMode():
  displayMatrix = [0,0,0,0,1,0,1,0,
                   0,3,3,0,0,1,0,0,
                   0,3,3,0,1,0,1,0,
                   0,0,0,0,0,0,0,0,
                   0,0,0,0,0,0,0,0,
                   0,4,4,0,0,2,0,0,
                   0,4,4,0,2,0,2,0,
                   0,0,0,0,0,2,0,0]
  for i in range(0,64):
    if displayMatrix[i] == 1:
      pixels[i] = (0,255,0)
    elif displayMatrix[i] == 2:
      pixels[i] = (0,0,255)
    elif displayMatrix[i] == 0:
      pixels[i] = (0,0,0)
  mode = -1
  select = 0
  while mode == -1:
    if select == 0:
      pixels[9] = (255,255,0)
      pixels[10] = (255,255,0)
      pixels[17] = (255,255,0)
      pixels[18] = (255,255,0)
      pixels[41] = (0,0,0)
      pixels[42] = (0,0,0)
      pixels[49] = (0,0,0)
      pixels[50] = (0,0,0)
    else:
      pixels[9] = (0,0,0)
      pixels[10] = (0,0,0)
      pixels[17] = (0,0,0)
      pixels[18] = (0,0,0)
      pixels[41] = (255,255,0)
      pixels[42] = (255,255,0)
      pixels[49] = (255,255,0)
      pixels[50] = (255,255,0)
    inputCode = GetInputDownCode()
    if inputCode == 1:
      select = 0
    elif inputCode == 2:
      select = 1
    elif inputCode == 5:
      mode = select
    hat.set_pixels(pixels)
  return mode
#
def DisplaySelectMap():
  displayMatrix = [0,0,1,1,0,0,4,4,
                   0,0,1,1,0,0,4,4,
                   0,0,0,0,0,0,0,0,
                   0,0,2,2,0,0,5,5,
                   0,0,2,2,0,0,5,5,
                   0,0,0,0,0,0,0,0,
                   0,0,3,3,0,0,6,6,
                   0,0,3,3,0,0,6,6]
  for i in range(0,64):
    if displayMatrix[i] == 1:
      pixels[i] = (255,0,0)
    elif displayMatrix[i] == 2:
      pixels[i] = (255,255,0)
    elif displayMatrix[i] == 3:
      pixels[i] = (0,255,0)
    elif displayMatrix[i] == 4:
      pixels[i] = (0,255,255)
    elif displayMatrix[i] == 5:
      pixels[i] = (0,0,255)
    elif displayMatrix[i] == 6:
      pixels[i] = (255,0,255)
    elif displayMatrix[i] == 0:
      pixels[i] = (0,0,0)
  hat.set_pixels(pixels)
  selectedMap = -1
  select = 0
  while selectedMap == -1:
    if select == 0:
      pixels[9] = (255,128,0)
      pixels[13] = (0,0,0)
      pixels[25] = (0,0,0)
      pixels[29] = (0,0,0)
      pixels[49] = (0,0,0)
      pixels[53] = (0,0,0)
    elif select == 1:
      pixels[9] = (0,0,0)
      pixels[13] = (0,0,0)
      pixels[25] = (255,128,0)
      pixels[29] = (0,0,0)
      pixels[49] = (0,0,0)
      pixels[53] = (0,0,0)
    elif select == 2:
      pixels[9] = (0,0,0)
      pixels[13] = (0,0,0)
      pixels[25] = (0,0,0)
      pixels[29] = (0,0,0)
      pixels[49] = (255,128,0)
      pixels[53] = (0,0,0)
    elif select == 3:
      pixels[9] = (0,0,0)
      pixels[13] = (255,128,0)
      pixels[25] = (0,0,0)
      pixels[29] = (0,0,0)
      pixels[49] = (0,0,0)
      pixels[53] = (0,0,0)
    elif select == 4:
      pixels[9] = (0,0,0)
      pixels[13] = (0,0,0)
      pixels[25] = (0,0,0)
      pixels[29] = (255,128,0)
      pixels[49] = (0,0,0)
      pixels[53] = (0,0,0)
    elif select == 5:
      pixels[9] = (0,0,0)
      pixels[13] = (0,0,0)
      pixels[25] = (0,0,0)
      pixels[29] = (0,0,0)
      pixels[49] = (0,0,0)
      pixels[53] = (255,128,0)

    inputCode = GetInputDownCode()
    if inputCode == 1:
      select -= 1
      if select < 0:
        select = 5
    elif inputCode == 2:
      select += 1
      if select > 5:
        select = 0
    elif inputCode == 5:
      selectedMap = select
    hat.set_pixels(pixels)
  return selectedMap

#Bot Code
steps = []
isGoal = False
curIndex = 0

def Explore():
  global isGoal
  global curIndex
  global steps
  global BotDelayMove
  global BotDelayBack
  if isGoal == True:
    return 0
  if len(steps) < 1:
    b = Block()
    b.isUp = BotCheckUp()
    b.isDown = BotCheckDown()
    b.isLeft = BotCheckLeft()
    b.isRight = BotCheckRight()
    b.x = 0
    b.y = 0
    steps.append(b)
    return 0
  else:
    if steps[curIndex].isExistWay() == False:
      pre = steps[curIndex].previousIndex
      delX = int(steps[pre].x - steps[curIndex].x)
      delY = int(steps[pre].y - steps[curIndex].y)
      if delX > 0:
        MoveRight()
      elif delX < 0:
        MoveLeft()
      elif delY > 0:
        MoveDown()
      elif delY < 0:
        MoveUp()
      curIndex = steps[curIndex].previousIndex
      return BotDelayBack
    #random move
    moves = []
    if steps[curIndex].isRight == True:
      moves.append(1)
      
    if steps[curIndex].isUp == True:
      moves.append(2)
      
    if steps[curIndex].isDown == True:
      moves.append(3)
      
    if steps[curIndex].isLeft == True:
      moves.append(4)
    #
    choice = random.choice(moves)
    # 
    if choice == 1:
      MoveRight()
      steps[curIndex].isRight = False
      tempb = Block()
      steps.append(tempb)
      last = len(steps) - 1
      steps[last].x = steps[curIndex].x + 1
      steps[last].y = steps[curIndex].y
      steps[last].isUp = BotCheckUp()
      steps[last].isRight = BotCheckRight()
      steps[last].isDown = BotCheckDown()
      steps[last].isLeft = False

      steps[curIndex].nextIndex = last
      steps[last].previousIndex = curIndex
      curIndex = steps[curIndex].nextIndex
      return BotDelayMove
    
    if choice == 2:
      MoveUp()
      steps[curIndex].isUp = False
      tempb = Block()
      steps.append(tempb)
      last = len(steps) - 1
      steps[last].x = steps[curIndex].x
      steps[last].y = steps[curIndex].y - 1
      steps[last].isUp = BotCheckUp()
      steps[last].isRight = BotCheckRight()
      steps[last].isLeft = BotCheckLeft()
      steps[last].isDown = False
      steps[curIndex].nextIndex = last
      steps[last].previousIndex = curIndex
      curIndex = steps[curIndex].nextIndex
      return BotDelayMove
    
    if choice == 3:
      MoveDown()
      steps[curIndex].isDown = False
      tempb = Block()
      steps.append(tempb)
      last = len(steps) - 1
      steps[last].x = steps[curIndex].x
      steps[last].y = steps[curIndex].y + 1
      steps[last].isDown = BotCheckDown()
      steps[last].isRight = BotCheckRight()
      steps[last].isLeft = BotCheckLeft()
      steps[last].isUp = False
      steps[curIndex].nextIndex = last
      steps[last].previousIndex = curIndex
      curIndex = steps[curIndex].nextIndex
      return BotDelayMove
    
    if choice == 4:
      MoveLeft()
      steps[curIndex].isLeft = False
      tempb = Block()
      steps.append(tempb)
      last = len(steps) - 1
      steps[last].x = steps[curIndex].x - 1
      steps[last].y = steps[curIndex].y
      steps[last].isUp = BotCheckUp()
      steps[last].isDown = BotCheckDown()
      steps[last].isLeft = BotCheckLeft()
      steps[last].isRight = False
      steps[curIndex].nextIndex = last
      steps[last].previousIndex = curIndex
      curIndex = steps[curIndex].nextIndex
      return BotDelayMove

def MoveUp():
  global player
  SetPlayerValueOnMap(0)
  #
  player[1] -= 1
  #
  SetPlayerValueOnMap(2)

def MoveDown():
  global player
  SetPlayerValueOnMap(0)
  #
  player[1] += 1
  #
  SetPlayerValueOnMap(2)

def MoveLeft():
  global player
  SetPlayerValueOnMap(0)
  #
  player[0] -= 1
  #
  SetPlayerValueOnMap(2)
  
def MoveRight():
  global player
  SetPlayerValueOnMap(0)
  #
  player[0] += 1
  #
  SetPlayerValueOnMap(2)
  
def BotCheckUp():
  result = CheckAvailableTop()
  if result == 2:
    global isGoal
    isGoal = True
    return False
  elif result == 0:
    return False
  length = len(steps) - 2
  last = len(steps) - 1
  for i in range(0,length):
    index = length - i
    if steps[last].x == steps[index].x and steps[last].y - 2 == steps[index].y:
      return False
  return True
  
def BotCheckDown():
  result = CheckAvailableDown()
  if result == 2:
    global isGoal
    isGoal = True
    return False
  elif result == 0:
    return False
  length = len(steps) - 2
  last = len(steps) - 1
  for i in range(0,length):
    index = length - i
    if steps[last].x == steps[index].x and steps[last].y + 2 == steps[index].y:
      return False
  return True
  
def BotCheckRight():
  result = CheckAvailableRight()
  if result == 2:
    global isGoal
    isGoal = True
    return False
  elif result == 0:
    return False
  length = len(steps) - 2
  last = len(steps) - 1
  for i in range(0,length):
    index = length - i
    if steps[last].x + 2 == steps[index].x and steps[last].y == steps[index].y:
      return False
  return True
  
def BotCheckLeft():
  result = CheckAvailableLeft()
  if result == 2:
    global isGoal
    isGoal = True
    return False
  elif result == 0:
    return False
  length = len(steps) - 2
  last = len(steps) - 1
  for i in range(0,length):
    index = length - i
    if steps[last].x -2 == steps[index].x and steps[last].y== steps[index].y:
      return False
  return True

#Game Flow
InitScreen()
while True:
  #menu
  mode = DisplaySelectMode()
  mapID = DisplaySelectMap()
  #loadmap
  LoadGame(mapID)
  #gameplay
  markTime = time.time()
  if mode == 0:
    while gameover == False:
      if(isStart == False):
        markTime = time.time()
      InputProcessing()
      Render(PlayerDelay)
  else:
    markTime = time.time()
    while isGoal == False:
      wait = Explore()
      Render(wait)
  #gameover
  totalTime = int(time.time() - markTime)
  s.SenseHat().show_message('win ' + str(totalTime) + 's')
  ResetValue = 0
  while ResetValue == 0:
    if GetInputCode() == 5:
      ResetGame()
      ResetValue = 5

