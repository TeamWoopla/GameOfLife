import pyglet
from pyglet.window import key


""" Main Features :
  * Press right mouse btn to create life and left btn to destroy life
  * Press enter or middle mouse btn(M3) to stop/start the simulation
  * Press P or Hold down the middle mouse btn(M3) to clear the board
  * Window side(pixels) is in line 20
  * Grid size is in line 26
  * Refresh rate(seconds) is in line 28
  * Enjoy! - OrCohen&ElamarKadosh 7.2018
"""


# Window Settings
window = pyglet.window.Window()
keys = key.KeyStateHandler()
window.push_handlers(keys)
WindowSize = 500  # Change this for different window side
window.set_caption("Game Of Life")
window.set_size(WindowSize, WindowSize)


# Data Board Creation
size = 25  # Change this for smaller or lager grid
DataBoard = [[0] * size for i1 in range(size)]
RefreshRate = 0.1  # Change this for slower or faster generation speed
RefreshRateMax = 0.1


# Maualy Creating Life
DataBoard[10][10] = 1
DataBoard[9][10] = 1
DataBoard[8][10] = 1
DataBoard[9][9] = 1
DataBoard[8][11] = 1

# Variables
BTNDelay = 1
DELWait = 0
Work = False
MMid = False


# Updating The Data Board
def LogicUpdate(Board):
    size = len(Board)
    NewBoard = [[0] * size for i1 in range(size)]
    for y in range(size):
        for x in range(size):
            Alives = 0
            for CheckY in range(-1, 2):
                for CheckX in range(-1, 2):
                    if not (CheckX == 0 and CheckY == 0):
                        if -1 < y + CheckY < size and -1 < x + CheckX < size:
                            Alives += Board[y + CheckY][x + CheckX]
            if Board[y][x] == 0:
                if Alives == 3:
                    NewBoard[y][x] = 1
            else:
                if Alives not in [2, 3]:
                    NewBoard[y][x] = 0
                else:
                    NewBoard[y][x] = 1
    return NewBoard


# Rectangle Update
def RectangleUpdate():
    global DataBoard, DrawBoard, Work
    Stop = True
    for x in range(size):
        for y in range(size):
            if DataBoard[y][x] == 0:
                DrawBoard[y][x].Update((0, 0, 0))
            else:
                Stop = False
                DrawBoard[y][x].Update((255, 255, 255))
    if Stop:
        Work = False


# Rectangle Class
class Rectangle:
    def __init__(self, x, y, width, height, color=(26, 255, 26)):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.color = color

    def Draw(self):
        pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f',
                                                     [self.x, self.y, self.x + self.width, self.y, self.x + self.width,
                                                      self.y + self.height, self.x, self.y + self.height]),
                             ('c3B', (self.color * 4)))

    def Update(self, color=(26, 255, 26)):
        self.color = color


# Creation Of the Rectangle Board
DrawBoard = [[Rectangle(x*(WindowSize/size), y*(WindowSize/size), WindowSize/size, WindowSize/size, (0, 0, 0)) for y in range(size)] for x in range(size)]
RectangleUpdate()

# Drawing The Rectangles
@window.event
def on_draw():
    window.clear()
    for Line in DrawBoard:
        for Obj in Line:
            if not Obj.color == (0, 0, 0):
                Obj.Draw()


# Creating && Destroying Life
@window.event
def on_mouse_press(x, y, button, modifiers):
    global MMid
    x, y = int(x/(WindowSize/size)), int(y/(WindowSize/size))
    if -1 < x < size and -1 < y < size:
        if button == pyglet.window.mouse.LEFT:
            DataBoard[x][y] = 1
        elif button == pyglet.window.mouse.RIGHT:
            DataBoard[x][y] = 0
        RectangleUpdate()
    if button == pyglet.window.mouse.MIDDLE:
        MMid = True
    pass


@window.event
def on_mouse_release(x, y, button, modifiers):
    global MMid
    if button == pyglet.window.mouse.MIDDLE:
        MMid = False


@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    x, y = int(x/(WindowSize/size)), int(y/(WindowSize/size))
    if -1 < x < size and -1 < y < size:
        if buttons & pyglet.window.mouse.LEFT:
            DataBoard[x][y] = 1
        elif buttons & pyglet.window.mouse.RIGHT:
            DataBoard[x][y] = 0
        RectangleUpdate()
    pass


# Updates
@window.event
def update(dt):
    global DataBoard, DrawBoard, Work, BTNDelay, MMid, DELWait, RefreshRateMax, RefreshRate

    # Stopping BTN && Logic
    BTNDelay += dt
    if BTNDelay > 0.2: BTNDelay = 0.2
    if (keys[key.ENTER] or MMid) and BTNDelay == 0.2:
        Work = not Work
        BTNDelay = 0
    if MMid:
        DELWait += dt
        if DELWait > 0.5: DELWait = 0.5
    else:
        DELWait = 0
    if keys[key.P] or DELWait == 0.5:
        DataBoard = [[0] * size for i1 in range(size)]
        RectangleUpdate()
        BTNDelay = 0
        DELWait = 0

    # Updating The Data Board & The Rectangles Color
    RefreshRate += dt
    if RefreshRate > RefreshRateMax:
        RefreshRate = RefreshRateMax
    if Work and RefreshRate == RefreshRateMax:
        DataBoard = LogicUpdate(DataBoard)
        RectangleUpdate()
        RefreshRate = 0


# Stating The Program
if __name__ == "__main__":
    # Starting the main loop
    pyglet.clock.schedule_interval(update, 1 / 100)  # Loop speed
    pyglet.app.run()
