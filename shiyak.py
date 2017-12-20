# file: runFile.py
# author: Jack Dunbar
# date: 11/19/2017
# Controls user interaction with the program as well as display

from tkinter import *
from airplaneData import *
from airportMap import *
import string

def init(data):
    # Initialize graph
    data.airports = getMap()
    data.cost = 0

    # To keep track of mouse position
    data.curX = 0
    data.curY = 0

    # Initialize all images
    data.background = PhotoImage(file="images/MapOfUS.png")
    data.smallBackground = PhotoImage(file = "images/smallBackground.png")
    data.northeast = PhotoImage(file="images/Northeast.png")
    data.smallNortheast = PhotoImage(file = "images/smallNortheast.png")
    data.airplane = PhotoImage(file="images/Airplane_Image.png")
    data.back = PhotoImage(file="images/Back button.png")
    data.swap = PhotoImage(file="images/arrows.png")

    # Dialogue box
    data.start = None
    data.inStartBox = False
    data.finish = None
    data.inFinishBox = False

    # Modes
    data.help = False
    data.search = False
    data.searched = False

    # View modes
    data.allUS = True

def keyPressed(event, data):
    # On help screen
    if (data.help == True):
        if(event.keysym == "BackSpace"):
            data.help = False

    # On search screen
    elif (data.search == True):
        if(event.keysym == "BackSpace"):
            data.search = False
            data.searched = False
            data.start = None
            data.finish = None

    # Interacting with start dialogue box
    elif(data.inStartBox == True):
        if(data.start == None):
            data.start = ""
        if(len(data.start) <= 21):
            if(event.keysym in string.ascii_letters or event.char in string.punctuation):
                data.start += event.char
            elif(event.keysym == "space"):
                data.start += " "
        if(event.keysym == "BackSpace"):
            data.start = data.start[:-1]
        elif(event.keysym == "Tab" or event.keysym == "Return"):
            data.inStartBox = False
            data.inFinishBox = True
        if(len(data.start) == 0):
            data.start = None

    # Interacting with finish dialogue box
    elif(data.inFinishBox == True):
        if (data.finish == None):
            data.finish = ""
        if (len(data.finish) <= 21):
            if (event.keysym in string.ascii_letters or event.char in string.punctuation):
                data.finish += event.char
            elif (event.keysym == "space"):
                data.finish += " "
        if (event.keysym == "BackSpace"):
            data.finish = data.finish[:-1]
        elif(event.keysym == "Return"):
            data.search = True
        if(len(data.finish) == 0):
            data.finish = None

    # Basic interaction
    else:
        if(event.keysym == "BackSpace"):
            if(data.finish == None):
                data.start = None
            else:
                data.finish = None
        elif(event.keysym == "Return"):
            data.search = True

def mousePressed(event, data):
    #print(event.x, event.y)
    # Help screen
    if(data.help == True):
        # Back button
        if(event.x >= data.width-180 and event.x <= data.width - 100 and event.y >= data.height-140
           and event.y <= data.height-100):
            data.help = False

    # Search screen
    elif(data.search == True):
        # Back button5i
        if(event.y >= 140-15 and event.y <= 175-15 and event.x >= 820 and event.x <= 900):
            data.search = False
            data.searched = False
            data.start = None
            data.finish = None
        # Help button
        elif(event.x >= 285 and event.x <= 355 and event.y >= 140 and event.y <= 176):
            data.help = True
            data.search = False
            data.searched = False
        # Switch View
        elif(event.x >= data.width - 123 and event.x <= data.width - 10 and event.y >= data.height - 84 and
                event.y <= data.height - 10):
            data.allUS = not data.allUS

    # Basic interaction
    else:
        # Clicking on airports to toggle start and finish
        if(data.allUS == True):
            count = 0
            # If on airport
            for location in data.airports.airportLocations:
                tempX, tempY = data.airports.airportLocations[location]
                if(abs(tempX - event.x) <= 9 and abs(tempY - event.y) <= 9 and data.start == None and count == 0):
                    data.start = location
                    count += 1
                elif(abs(tempX - event.x) <= 9 and abs(tempY - event.y) <= 9 and data.start != None and count == 0):
                    data.finish = location
                    count += 1
        else:
            count = 0
            # If on airport
            for location in data.airports.northeastLocations:
                tempX, tempY = data.airports.northeastLocations[location]
                if (abs(tempX - event.x) <= 9 and abs(tempY - event.y) <= 9 and data.start == None and count == 0):
                    data.start = location
                    count += 1
                elif (abs(tempX - event.x) <= 9 and abs(tempY - event.y) <= 9 and data.start != None and count == 0):
                    data.finish = location
                    count += 1

        # Toggle start box
        if(event.x >= 280 and event.x <= 540 and event.y >= 40 and event.y <= 80):
            data.inStartBox = True
        else:
            data.inStartBox = False

        # Toggle finish box
        if(event.x >= 280 and event.x <= 540 and event.y >= 90 and event.y <= 130):
            data.inFinishBox = True
        else:
            data.inFinishBox = False

        # Search
        if(event.x >= 390 and event.x <= 470 and event.y >= 140 and event.y <= 176):
            data.search = True

        # Help
        elif(event.x >= 285 and event.x <= 355 and event.y >= 140 and event.y <= 176):
            data.help = True

        # Swap start and finish
        elif(event.x >= 545 and event.x <= 595 and event.y >= 60 and event.y <= 110):
            tempFinish = data.start
            data.start = data.finish
            data.finish = tempFinish

        # Switch View
        elif (event.x >= data.width - 123 and event.x <= data.width - 10 and event.y >= data.height - 84 and
                event.y <= data.height - 10):
            data.allUS = not data.allUS


def timerFired(data, root):
    # Uses Dijkstra's to find the minimum cost of flying between airports
    if(data.search == True and data.searched == False):
        if(data.start == None or data.finish == None):
            data.search = False
        elif(data.start in data.airports.airportLocations):
            minList, data.cost = data.airports.minCost(data.start, data.finish)
            if(len(minList) == 0 or minList[-1] != data.finish):
                data.search = False
            else:
                data.searched = True

    # Found on stackoverflow: https://stackoverflow.com/questions/22925599/mouse-position-python-tkinter
    # Keeps track of cursor
    data.curX = root.winfo_pointerx() - root.winfo_rootx()
    data.curY = root.winfo_pointery() - root.winfo_rooty()

def redrawAll(canvas, data):
    def drawPath(canvas, data):
        if(data.allUS == True):
            for node in range(1, len(data.airports.minList)):
                tempX1, tempY1 = data.airports.airportLocations[data.airports.minList[node]]
                tempX2, tempY2 = data.airports.airportLocations[data.airports.minList[node - 1]]
                canvas.create_line(tempX2, tempY2, tempX1, tempY1, fill="black", width=2)
                meanX = (tempX1+tempX2)/2
                meanY = (tempY1+tempY2)/2
                canvas.create_rectangle(meanX-30, meanY-10, meanX+30, meanY+10, fill="snow")
                canvas.create_text(meanX, meanY, text = "Cost: $" +
                                   str(data.airports.map[data.airports.minList[node-1]][data.airports.minList[node]]),
                                   font = "arial 8")
        else:
            for node in range(1, len(data.airports.minList)):
                tempX1, tempY1 = data.airports.northeastLocations[data.airports.minList[node]]
                tempX2, tempY2 = data.airports.northeastLocations[data.airports.minList[node - 1]]
                canvas.create_line(tempX2, tempY2, tempX1, tempY1, fill="black", width=2)
                meanX = (tempX1+tempX2)/2
                meanY = (tempY1+tempY2)/2
                canvas.create_rectangle(meanX-30, meanY-10, meanX+30, meanY+10, fill="snow")
                canvas.create_text(meanX, meanY, text = "Cost: $" +
                                   str(data.airports.map[data.airports.minList[node-1]][data.airports.minList[node]]),
                                   font = "arial 8")

    def drawCost(canvas, data):
        canvas.create_rectangle(750, 60, 900, 175-15, fill = "navajo white")

        canvas.create_text(760, 100, anchor = "w", text = "Cost:", fill = "black", font = "arial 15 underline")
        canvas.create_rectangle(815, 80, 890, 120, fill = "snow")
        canvas.create_text(853, 100, text = "$" + str(data.cost), fill = "black", font = "arial 15")

        canvas.create_image(820, 160-15, image = data.back, anchor = "w")
        canvas.create_text(850, 158-15, anchor = "w", text = "Back", fill = "black", font = "arial 15")

    def drawAirports(canvas, data):
        if(data.allUS == True):
            for location in data.airports.airportLocations:
                tempX, tempY = data.airports.airportLocations[location]
                canvas.create_image(tempX, tempY, image=data.airplane)
        else:
            for location in data.airports.northeastLocations:
                tempX, tempY = data.airports.northeastLocations[location]
                canvas.create_image(tempX, tempY, image=data.airplane)

    def drawDialogueBoxes(canvas, data):
        # Big box
        canvas.create_rectangle(200, 25, 600, 185, fill="navajo white")
        # Departure
        canvas.create_text(207, 60, text="Depart:", anchor="w", fill="black", font="arial 15 underline")
        canvas.create_rectangle(280, 40, 540, 80, fill="snow")
        canvas.create_text(285, 60, text=data.start, anchor="w", fill="black", font="arial 15")
        # Arrival
        canvas.create_text(207, 110, text="Arrive:", anchor="w", fill="black", font="arial 15 underline")
        canvas.create_rectangle(280, 90, 540, 130, fill="snow")
        canvas.create_text(285, 110, text=data.finish, anchor="w", fill="black", font="arial 15")
        # Help
        canvas.create_rectangle(285, 140, 355, 176, fill="snow")
        canvas.create_text(320, 158, text="Help", fill="black", font="arial 15 underline")
        # Search
        canvas.create_rectangle(390, 140, 470, 176, fill="snow")
        canvas.create_text(430, 158, text="Search", fill="black", font="arial 15 underline")
        # Swap
        canvas.create_image(545, 85, anchor = "w", image = data.swap)

    def drawCityName(canvas, data):
        if(data.allUS == True):
            for location in data.airports.airportLocations:
                tempX, tempY = data.airports.airportLocations[location]
                if (abs(tempX - data.curX) <= 9 and abs(tempY - data.curY) <= 9):
                    canvas.create_rectangle(tempX + 8, tempY - 24, tempX + 135, tempY - 8, fill="snow")
                    canvas.create_text(tempX + 11, tempY - 16, anchor="w", text = location,
                                       font="arial 8")
                    break
        else:
            for location in data.airports.northeastLocations:
                tempX, tempY = data.airports.northeastLocations[location]
                if (abs(tempX - data.curX) <= 9 and abs(tempY - data.curY) <= 9):
                    canvas.create_rectangle(tempX + 8, tempY - 24, tempX + 135, tempY - 8, fill="snow")
                    canvas.create_text(tempX + 11, tempY - 16, anchor="w", text = location,
                                       font="arial 8")
                    break

    def drawSwapView(canvas, data):
        canvas.create_rectangle(data.width - 124, data.height - 85, data.width - 10, data.height - 10, width = 1)
        if(data.allUS == True):
            canvas.create_image(data.width-10, data.height-10, anchor = "se", image = data.smallNortheast)
        else:
            canvas.create_image(data.width-10, data.height-10, anchor  = "se", image = data.smallBackground)

    def drawHelp(canvas, data):
        canvas.create_rectangle(100, 50, data.width - 100, data.height - 100, fill = "navajo white")
        canvas.create_text(120, 65, anchor = "nw", text = "How to use Shiyak:", fill = "black",
                           font = "arial 24 underline")
        canvas.create_rectangle(120, 115, data.width-120, data.height-140, fill = "white")
        canvas.create_text(data.width-110, data.height - 122, anchor = "e", text = "Back", fill = "black",
                           font = "arial 15")
        canvas.create_image(data.width-150, data.height-120, anchor = "e", image = data.back)
        help = readFile("help.txt")
        canvas.create_text(125, 120, anchor = "nw", text = help, fill = "black", font = "arial 15")

    # Which map to draw
    if(data.allUS == True):
        canvas.create_image(0, 0, image = data.background, anchor = "nw")
    else:
        canvas.create_image(0, 0, image=data.northeast, anchor="nw")

    if(data.search == True and data.searched == True):
        drawPath(canvas, data)
        drawCost(canvas, data)

    drawAirports(canvas, data)

    drawDialogueBoxes(canvas, data)

    drawSwapView(canvas, data)

    if (data.help == True):
        drawHelp(canvas, data)
    else:
        drawCityName(canvas, data)

# Altered run function from 15-112 course notes: http://www.cs.cmu.edu/~112/notes
def runShiyak(width, height):
    root = Tk()

    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data, root):
        timerFired(data, root)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data, root)

    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100  # milliseconds
    init(data)

    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()

    # set up events
    root.bind("<Button-1>", lambda event:
    mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
    keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data, root)
    # and launch the app
    root.mainloop()  # blocks until window is closed

def main():
    runShiyak(1130, 742)
    #testDijkstras()

if __name__ == '__main__':
    main()