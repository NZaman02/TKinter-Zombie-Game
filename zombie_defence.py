from tkinter import *
import random
import time
import os

# screen resolution is 1440x900


def drawGrid(canvas):
    # creates rows
    for i in range(0, 30):
        canvas.create_line(
            (0),
            (i * 30),
            1440,
            (i * 30),
            fill="grey",
            tags="lines")

    # creates collumns
    for i in range(0, 48):
        canvas.create_line(
            (i * 30),
            (0),
            (i * 30),
            900,
            fill="grey",
            tags="lines")
    # each square 30*30 meaning amount of squares = 48*30


# checks if 2 objects collide
def overlapping(item1, item2):
    CoOr1 = canvas.coords(item1)
    CoOr2 = canvas.coords(item2)
    # checks coordinates of each point on the rectangle
    if CoOr1[0] < CoOr2[2] and CoOr1[2] > CoOr2[0]:
        if CoOr1[1] < CoOr2[3] and CoOr1[3] > CoOr2[1]:
            return True
    return False


def createLaser(event):
    canvas.delete("laser")
    playerPos = canvas.coords(player[0])
    # size of the laser
    global laserLength

    # decides direction of laser and creates it
    global Ldirection
    if (Ldirection == "left"):
        laser = canvas.create_rectangle(
            playerPos[0] - laserLength,
            playerPos[1],
            playerPos[2] - 30,
            playerPos[3],
            fill="red",
            tags="laser")
    if (Ldirection == "right"):
        laser = canvas.create_rectangle(
            playerPos[0] + 30,
            playerPos[1],
            playerPos[2] + laserLength,
            playerPos[3],
            fill="red",
            tags="laser")
    if (Ldirection == "down"):
        laser = canvas.create_rectangle(
            playerPos[0],
            playerPos[1] +
            laserLength,
            playerPos[2],
            playerPos[3],
            fill="red",
            tags="laser")
    if (Ldirection == "up"):
        laser = canvas.create_rectangle(
            playerPos[0],
            playerPos[1],
            playerPos[2],
            playerPos[3] -
            laserLength,
            fill="red",
            tags="laser")

    # makes so laser is only on screen temporarily
    var = IntVar()
    window.after(200, var.set, 1)
    global numOfZ
    # kills zombie when laser touches it
    z = 0
    while z < numOfZ:
        if overlapping(laser, zombie[z]):
            numOfZ -= 1
            canvas.delete(zombie[z])
            zombie.remove(zombie[z])
            global score
            score += 1
            txt = "score:" + str(score)
            canvas.itemconfigure(scoreText, text=txt)
        z += 1
    window.wait_variable(var)
    canvas.delete(laser)


def movePlayer():
    canvas.pack()
    global direction, Ldirection
    # moves player by 1 block based on keypress
    if direction == "left":
        canvas.move(player[0], -30, 0)
        Ldirection = direction
        direction = "stop"
    elif direction == "right":
        canvas.move(player[0], 30, 0)
        Ldirection = direction
        direction = "stop"
    elif direction == "up":
        canvas.move(player[0], 0, -30)
        Ldirection = direction
        direction = "stop"
    elif direction == "down":
        canvas.move(player[0], 0, 30)
        Ldirection = direction
        direction = "stop"

    # checks if zombie touches player
    overlapped = False
    x = 0
    while (not overlapped) and (x < (numOfZ - 1)):
        if overlapping(player, zombie[x]):
            canvas.move(player, 1000, 1000)
            overlapped = True
            LostGame()
        else:
            x += 1
    global GameOver
    if not GameOver:
        window.after(70, movePlayer)

# chooses the direction


def leftKey(event):
    global direction
    direction = "left"
    return direction


def upKey(event):
    global direction
    direction = "up"
    return direction


def rightKey(event):
    global direction
    direction = "right"
    return direction


def downKey(event):
    global direction
    direction = "down"
    return direction


# initialises num of zombies
zombie = []
numOfZ = 0


def createZombie(numOfZ):
    # choose where zombie spawns
    side = random.randint(0, 3)

    # top side
    if side == 0:
        x1 = 30 * random.randint(0, 48)
        y1 = 0
    # right side
    if side == 1:
        x1 = 1410
        y1 = 30 * random.randint(0, 30)
    # bottom side
    if side == 2:
        x1 = 30 * random.randint(0, 48)
        y1 = 870
    # left side
    elif side == 3:
        x1 = 0
        y1 = 30 * random.randint(0, 30)
    y2 = y1 + 30
    x2 = x1 + 30
    # creates the zombie at random edge of the map
    global canvas
    zombie.append(
        canvas.create_rectangle(
            x1,
            y1,
            x2,
            y2,
            fill="green",
            tags="rect"))
    numOfZ += 1
    return numOfZ


def moveZombie(speed, player, window):
    global numOfZ, GameOver
    if not GameOver:
        for x in range(0, numOfZ):
            if x >= len(zombie):
                break
            else:
                # works out where both are
                playerPos = canvas.coords(player[0])
                zombiePos = canvas.coords(zombie[x])

                # zombie chooses either to go left or right to player
                if zombiePos[0] < playerPos[0]:
                    canvas.move(zombie[x], 30, 0)
                elif zombiePos[0] > playerPos[0]:
                    canvas.move(zombie[x], -30, 0)
                # zombie chooses whether to go up or down
                if zombiePos[1] < playerPos[1]:
                    canvas.move(zombie[x], 0, 30)
                elif zombiePos[1] > playerPos[1]:
                    canvas.move(zombie[x], 0, -30)
                x += 1
        # bigger speed = slower movement - means the delay
        var = IntVar()
        window.after(speed, var.set, 1)
        window.wait_variable(var)


def difficultyCurve(currentScore):
    # makes game more difficult over time
    global numOfZ, delay, GameOver

    if not GameOver:
        # speed and amount spawning depends on score
        if currentScore > 55:
            for x in range(0, 4):
                numOfZ = createZombie(numOfZ)
                delay = 600

        elif currentScore > 45:
            for x in range(0, 3):
                numOfZ = createZombie(numOfZ)
                delay = 700

        elif currentScore > 35:
            for x in range(0, 3):
                numOfZ = createZombie(numOfZ)
                delay = 800

        elif currentScore > 25:
            for x in range(0, 3):
                numOfZ = createZombie(numOfZ)
                delay = 900

        elif currentScore > 15:
            for x in range(0, 2):
                numOfZ = createZombie(numOfZ)
                delay = 1000

        elif currentScore > 5:
            for x in range(0, 2):
                numOfZ = createZombie(numOfZ)
                delay = 1100
        else:
            numOfZ = createZombie(numOfZ)


def showLeaderboard(
        playButton,
        boardButton,
        custButtons,
        exitButtons,
        loadButtons):
    # clears screen
    clearMenuButtons(
        playButton,
        boardButton,
        custButtons,
        exitButtons,
        loadButtons)

    canvas.delete("rect")
    canvas.delete("images")
    canvas.delete("laser")
    # makes file if does not exist
    if not os.path.exists("./leaderboard.txt"):
        file = open("leaderboard.txt", "w")
        # allows you to return to main menu when ready
        var2 = IntVar()
        recontinueButton = Button(
            canvas,
            text="Leaderboard doesn't exist.Start a new game in the menu",
            command=lambda: var2.set(1))
        recontinueButton.place(x=450, y=250)
        recontinueButton.wait_variable(var2)
        recontinueButton.destroy()
        mainMenu()
    # warns player if leaderboard empty
    elif os.stat("leaderboard.txt").st_size == 0:
        var3 = IntVar()
        recontinueButton = Button(
            canvas,
            text="No entries in leaderboard. Try starting a new game instead",
            command=lambda: var3.set(1))
        recontinueButton.place(x=450, y=250)
        recontinueButton.wait_variable(var3)
        recontinueButton.destroy()
        mainMenu()
    else:
        # reads in values for leaderboard
        scoreboard = []
        nameboard = []
        x = 0

        trophyImage = canvas.create_image(
            480, 70, anchor=NW, image=trophyPic, tags="images")
        trophyImage2 = canvas.create_image(
            970, 70, anchor=NW, image=trophyPic, tags="images")
        leaderboardImage = canvas.create_image(
            100, 750, anchor=NW, image=leaderboardPic, tags="images")

        file = open("leaderboard.txt", "r")
        for line in file:
            if x % 2:
                scoreboard.append(int(line.rstrip()))
            else:
                nameboard.append(line.rstrip())
            x += 1
        file.close()

        # bubble sort for leaderboard keeps the names
        for oLoop in range(0, len(scoreboard) - 1):
            for y in range(0, len(scoreboard) - 1):
                if scoreboard[y] < scoreboard[y + 1]:
                    temp = scoreboard[y + 1]
                    scoreboard[y + 1] = scoreboard[y]
                    scoreboard[y] = temp

                    temp2 = nameboard[y + 1]
                    nameboard[y + 1] = nameboard[y]
                    nameboard[y] = temp2
                    y = 0

        # writes out top 10 players
        txt1 = "The Leader: " + \
            str(nameboard[0]) + " Score: " + str(scoreboard[0])
        scoreText = canvas.create_text(
            750,
            100,
            fill="gold",
            font="Times 20 bold",
            text=txt1,
            tags="board")
        txts = []
        if len(nameboard) > 10:
            length = 9
        else:
            length = len(nameboard)
        for x in range(1, length):
            txts.append("POSTION " +
                        str(x) +
                        " = " +
                        str(nameboard[x]) +
                        "  SCORE: " +
                        str(scoreboard[x]))
            scoreText = canvas.create_text(750,
                                           (100 + (x * 50)),
                                           fill="white",
                                           font="Times 16 ",
                                           text=txts[x - 1],
                                           tags="board")

        # allows you to return to main menu when ready
        var = IntVar()
        recontinueButton = Button(
            canvas,
            text="Press me to return to the main menu",
            command=lambda: var.set(1))
        recontinueButton.place(x=1000, y=750)
        recontinueButton.wait_variable(var)
        recontinueButton.destroy()
        canvas.delete("board")
        canvas.delete("images")
        mainMenu()


def addScoreToBoard():
    # allows you to submit your score after end of game
    scoreText = canvas.create_text(
        (750,
         100),
        fill="white",
        font="Times 16 ",
        text="Enter the name you want on the leaderboard",
        tags="text")
    inputtxt = Text(window, height=5, width=100)
    inputtxt.place(x=300, y=300)

    var = IntVar()
    recontinueButton = Button(
        canvas,
        text="Press submit your name",
        command=lambda: var.set(1))
    recontinueButton.place(x=100, y=250)
    recontinueButton.wait_variable(var)
    canvas.pack()

    inputName = inputtxt.get(1.0, "end-1c")
    inputName = inputName.rstrip()
    inputName = inputName.lstrip()

    # reads in file then writes new result
    # write chosen over append to ensure format is kept consistent
    scoreboard = []
    nameboard = []
    x = 0
    file = open("leaderboard.txt", "r")
    for line in file:
        if x % 2:
            scoreboard.append(line.rstrip())
        else:
            nameboard.append(line.rstrip())
        x += 1
    file.close()

    nameboard.append(inputName)
    scoreboard.append(score)

    file = open("leaderboard.txt", "w")
    for x in range(0, len(nameboard)):
        file.write(str(nameboard[x]) + "\n")
        file.write(str(scoreboard[x]) + "\n")
    file.close()

    recontinueButton.destroy()
    inputtxt.destroy()
    canvas.delete("text")

    mainMenu()


def pauseGame(event):
    global pauseCopies, GameOver
    pauseCopies += 1

    if pauseCopies == 1 and (not GameOver):
        # pauses game until continue button is pressed
        pausedLabel = Label(
            canvas,
            text="Game is paused",
            font="Times 35 bold",
            bg="black",
            fg="white")
        pausedLabel.place(x=350, y=200)
        pvar = IntVar()
        recontinueButton = Button(
            canvas,
            text="Press me when you're ready to continue",
            command=lambda: pvar.set(1))
        recontinueButton.place(x=350, y=250)
        # allows you to save game after pause
        saveButton = Button(
            canvas,
            text="Press me to save game and exit",
            command=lambda: saveGame(
                saveButton,
                recontinueButton,
                pausedLabel))
        saveButton.place(x=350, y=300)
        GameOver = True
        recontinueButton.wait_variable(pvar)
        pausedLabel.destroy()
        saveButton.destroy()
        recontinueButton.destroy()
        GameOver = False
        movePlayer()
        pauseCopies = 0


def saveGame(saveButton, recontinueButton, pausedLabel):
    global numOfZ, delay, GameOver

    saveButton.destroy()
    recontinueButton.destroy()
    pausedLabel.destroy()
    # saves the position of the player, the score,the time delay (speed of
    # zombies) and position of all zombies to a text file
    playerPos = canvas.coords(player[0])
    zombiePos = []
    for x in range(0, numOfZ):
        zombiePos.append(canvas.coords(zombie[x]))

    file = open("saveGameInfo.txt", "w")
    file.write(str(playerPos) + "\n")
    file.write(str(score) + "\n")
    file.write(str(delay) + "\n")
    for x in range(0, numOfZ):
        file.write(str(zombiePos[x]) + "\n")
    file.close()

    numOfZ = 0
    zombie.clear()
    canvas.delete("rect")
    canvas.delete("lines")
    canvas.delete("theScore")

    GameOver = True

    mainMenu()


def loadGame(playButton, boardButton, custButtons, exitButtons, loadButtons):
    global score, delay, GameOver
    GameOver = True

    clearMenuButtons(
        playButton,
        boardButton,
        custButtons,
        exitButtons,
        loadButtons)
    canvas.pack()
    time.sleep(0.1)

    if os.path.exists("./saveGameInfo.txt"):
        file = open("saveGameInfo.txt", "r")

        # reformats text in file so that it can be used for loading
        rawPlayerPos = (file.readline()).rstrip()
        disallowed_characters = "[]"
        for character in disallowed_characters:
            rawPlayerPos = rawPlayerPos.replace(character, "")
        playerPos = rawPlayerPos.split(",")

        score = int(file.readline())
        delay = int(file.readline())
        zombiePos = []
        x = 0
        for line in file:
            format1 = line.rstrip()
            format2 = format1.replace("[", "")
            format3 = format2.replace("]", "")
            format4 = format3.split(",")
            map_object = map(float, format4)
            format5 = list(map_object)
            zombiePos.append(format5)
        file.close()

        canvas.delete("images")

        canvas.pack()
        drawGrid(canvas)

        # sets up where player saved
        global player, scoreText, laserLength
        laserLength = 150
        # uses the the position of the player,
        # the score,the time delay (speed of
        # zombies) and position of all zombies to recreate where the player was
        player = []
        GameOver = False
        player.append(
            canvas.create_rectangle(
                playerPos[0],
                playerPos[1],
                playerPos[2],
                playerPos[3],
                fill="blue",
                tags="player"))

        # readys keyboard input
        global direction
        canvas.bind("<Left>", leftKey)
        canvas.bind("<Right>", rightKey)
        canvas.bind("<Up>", upKey)
        canvas.bind("<Down>", downKey)
        canvas.bind("<space>", createLaser)
        canvas.bind("p", pauseGame)
        canvas.bind("o", bossKey)
        canvas.bind("j", laserCheat)
        canvas.focus_set()
        direction = "stop"

        Ldirection = "intialised"
        direction = movePlayer()

        global numOfZ
        numOfZ = len(zombiePos) - 1
        for x in range(0, len(zombiePos)):
            zombie.append(
                canvas.create_rectangle(
                    zombiePos[x][0],
                    zombiePos[x][1],
                    zombiePos[x][2],
                    zombiePos[x][3],
                    fill="green",
                    tags="rect"))

        txt = "Score:" + str(score)
        scoreText = canvas.create_text(
            750,
            20,
            fill="white",
            font="Times 20 bold",
            text=txt,
            tags="theScore")

        while not GameOver:
            difficultyCurve(score)
            moveZombie(delay, player, window)
            canvas.pack()

    else:
        var3 = IntVar()
        recontinueButton = Button(
            canvas,
            text="No save game found. Click to go to menu",
            command=lambda: var3.set(1))
        recontinueButton.place(x=450, y=250)
        recontinueButton.wait_variable(var3)
        recontinueButton.destroy()
        mainMenu()


def LostGame():
    # shown after game ends
    endScore = ("Your end score was " + str(score))
    endScoreLabel = Label(
        canvas,
        text=endScore,
        bg="black",
        font="Arial 30 bold",
        fg="white")
    endScoreLabel.place(x=500, y=400)

    var = IntVar()
    finishButton = Button(
        canvas,
        text="Press me to continue",
        command=lambda: var.set(1))
    finishButton.place(x=500, y=450)
    finishButton.wait_variable(var)
    finishButton.destroy()

    # restarts game
    global numOfZ
    numOfZ = 0

    zombie.clear()
    canvas.delete("rect")
    canvas.delete("lines")
    canvas.delete("theScore")
    endScoreLabel.destroy()

    global GameOver
    GameOver = True
    addScoreToBoard()


def bossKey(event):
    global bossCopies
    bossCopies += 1

    if bossCopies == 1 and (not GameOver):
        # boss key that gives image until button is clicked
        workImage = PhotoImage(file="workImage.png")
        var = IntVar()
        bossImage = canvas.create_image(0, 0, anchor=NW, image=workImage)
        workButton = Button(
            canvas,
            text="Press me to continue",
            command=lambda: var.set(1))
        workButton.place(x=25, y=865)

        workButton.wait_variable(var)
        workButton.destroy()
        canvas.delete(bossImage)
        bossCopies = 0


def laserCheat(event):
    global laserLength
    # increases the length of the rectangle allowing player to kill more
    # zombies
    laserLength += 90

# creates player character


def createPlayer(canvas):
    global player
    player = []
    player.append(
        canvas.create_rectangle(
            990,
            540,
            1020,
            570,
            fill="blue",
            tags="player"))

    # takes keyboard input
    global direction, pauseK, bossK, laserK
    canvas.bind("<Left>", leftKey)
    canvas.bind("<Right>", rightKey)
    canvas.bind("<Up>", upKey)
    canvas.bind("<Down>", downKey)
    canvas.bind("<space>", createLaser)
    canvas.bind(pauseK, pauseGame)
    canvas.bind(bossK, bossKey)
    canvas.bind(laserK, laserCheat)
    canvas.focus_set()
    direction = "stop"
    return player


def chooseButtonToChange(
        playButton,
        boardButton,
        custButtons,
        exitButtons,
        loadButtons):
    clearMenuButtons(
        playButton,
        boardButton,
        custButtons,
        exitButtons,
        loadButtons)
    canvas.delete("images")
    # allows user to pick which button they want to change
    canvas.create_text(
        (275,
         100),
        fill="white",
        font="Times 16",
        text="Only the first letter of your input will be taken",
        tags="text")
    canvas.create_text(
        (340,
         200),
        fill="white",
        font="Times 16",
        text="Movement will stay as the arrows.Shooting will stay as spacebar",
        tags="text")
    bossButton = Button(
        canvas,
        text="Click This To Change the Boss Key From the Default <o>",
        command=lambda: changeKey(
            "boss",
            bossButton,
            pauseButton,
            cheatButton,
            recontinueButton))
    bossButton.place(x=100, y=250)
    pauseButton = Button(
        canvas,
        text="Click This To Change the Pause Key From the Default <p>",
        command=lambda: changeKey(
            "pause",
            bossButton,
            pauseButton,
            cheatButton,
            recontinueButton))
    pauseButton.place(x=100, y=350)
    cheatButton = Button(
        canvas,
        text="Click This To Change the Cheat Key From the Default <j>",
        command=lambda: changeKey(
            "cheat",
            bossButton,
            pauseButton,
            cheatButton,
            recontinueButton))
    cheatButton.place(x=100, y=450)

    var = IntVar()
    recontinueButton = Button(
        canvas,
        text="Return To Menu",
        command=lambda: var.set(1))
    recontinueButton.place(x=200, y=550)

    recontinueButton.wait_variable(var)

    bossButton.destroy()
    pauseButton.destroy()
    cheatButton.destroy()
    recontinueButton.destroy()
    canvas.delete("text")

    mainMenu()


def changeKey(type, bossButton, pauseButton, cheatButton, recontinueButton):
    bossButton.destroy()
    pauseButton.destroy()
    cheatButton.destroy()
    recontinueButton.destroy()
    # allows user to input the key want to use
    enterText = canvas.create_text(
        (200,
         150),
        fill="white",
        font="Times 16 ",
        text="Enter the keybind you want",
        tags="text")
    inputtxt = Text(window, height=5, width=100)
    inputtxt.place(x=350, y=300)

    var = IntVar()
    submitButton = Button(canvas, text="Submit", command=lambda: var.set(1))
    submitButton.place(x=100, y=250)

    submitButton.wait_variable(var)
    canvas.pack()

    inputLetter = inputtxt.get(1.0, "end-1c")

    if inputLetter == "":
        inputLetter = "a"
    inputLetter = inputLetter.rstrip()
    inputLetter = inputLetter.lstrip()
    inputLetter = inputLetter[0]

    submitButton.destroy()
    canvas.delete("text")
    inputtxt.destroy()
    global pauseK, bossK, laserK
    # changes the controls
    if type == "boss":
        bossK = inputLetter
    elif type == "pause":
        pauseK = inputLetter
    elif type == "cheat":
        laserK = inputLetter

    changeText = "You changed your keybind to " + inputLetter
    enterText = canvas.create_text(
        (600,
         200),
        fill="white",
        font="Times 16 ",
        text=changeText,
        tags="text")
    time.sleep(1.5)
    canvas.delete("text")

    mainMenu()


def startGame(playButton, boardButton, custButtons, exitButtons, loadButtons):
    # prepares game
    global score, delay, GameOver, laserLength
    laserLength = 150
    score = 0
    delay = 1200
    GameOver = False

    clearMenuButtons(
        playButton,
        boardButton,
        custButtons,
        exitButtons,
        loadButtons)

    canvas.pack()
    drawGrid(canvas)
    player = createPlayer(canvas)
    Ldirection = "intialised"
    direction = movePlayer()
    canvas.delete("rect")
    canvas.delete("images")

    global scoreText
    txt = "Score:" + str(score)
    scoreText = canvas.create_text(
        750,
        20,
        fill="white",
        font="Times 20 bold",
        text=txt,
        tags="theScore")

    while not GameOver:
        # the game loop
        difficultyCurve(score)
        moveZombie(delay, player, window)
        canvas.pack()


def clearMenuButtons(
        playButton,
        boardButton,
        custButtons,
        exitButtons,
        loadButtons):
    # deletes menu buttons when transitioning
    playButton.destroy()
    boardButton.destroy()
    custButtons.destroy()
    loadButtons.destroy()
    exitButtons.destroy()
    canvas.delete("text")


def endGame():
    window.destroy()
    sys.exit()


def mainMenu():
    global GameOver, numOfZ, pauseCopies, bossCopies
    # prepares main menu
    GameOver = True
    numOfZ = 0
    pauseCopies = 0
    bossCopies = 0

    canvas.delete("player")
    canvas.delete("rect")

    bgImage = canvas.create_image(0, 0, anchor=NW, image=bgPic, tags="images")
    zombieImage1 = canvas.create_image(
        50, 450, anchor=NW, image=zombiePic, tags="images")
    zombieImage2 = canvas.create_image(
        150, 450, anchor=NW, image=zombiePic, tags="images")
    zombieImage3 = canvas.create_image(
        300, 450, anchor=NW, image=zombiePic, tags="images")
    zombieImage4 = canvas.create_image(
        600, 450, anchor=NW, image=zombiePic, tags="images")
    zombieImage5 = canvas.create_image(
        700, 450, anchor=NW, image=zombiePic, tags="images")

    titleImage = canvas.create_image(
        450, 0, anchor=NW, image=titlePic, tags="images")

    # creates main menu buttons
    playButton = Button(
        canvas, text='Start a New Game', font=(
            "Times New Roman", 20), command=lambda: startGame(
            playButton, boardButton, custButtons, exitButtons, loadButtons))
    playButton.place(x=900, y=100)
    boardButton = Button(
        canvas, text='Show Leaderboard', font=(
            "Times New Roman", 20), command=lambda: showLeaderboard(
            playButton, boardButton, custButtons, exitButtons, loadButtons))
    boardButton.place(x=900, y=150)
    custButtons = Button(
        canvas, text='Customise Controls', font=(
            "Times New Roman", 20), command=lambda: chooseButtonToChange(
            playButton, boardButton, custButtons, exitButtons, loadButtons))
    custButtons.place(x=900, y=200)
    loadButtons = Button(
        canvas, text='Load The Last Saved Game', font=(
            "Times New Roman", 20), command=lambda: loadGame(
            playButton, boardButton, custButtons, exitButtons, loadButtons))
    loadButtons.place(x=900, y=250)
    exitButtons = Button(
        canvas,
        text='Exit Game',
        font=(
            "Times New Roman",
            20),
        command=lambda: endGame())
    exitButtons.place(x=900, y=300)
    controls = canvas.create_text(
        300,
        200,
        text="Default Controls: Arrow Keys = Movement, Space = Laser",
        fill="white",
        font="Times 12",
        tags="text")
    controls2 = canvas.create_text(
        300,
        220,
        text="P = Pause, O = Boss Key, J = [REDACTED]",
        fill="white",
        font="Times 12",
        tags="text")

    canvas.pack()


pauseK = "p"
bossK = "o"
laserK = "j"

pauseCopies = 0
bossCopies = 0

GameOver = True
window = Tk()
window.title("Zombie Survival Game")
window.geometry("1440x900")
canvas = Canvas(window, bg="black", width=1440, height=900)

# prepares all the images

# https://www.1001fonts.com/thedeadarecoming-font.html
titlePic = PhotoImage(file="title.png")
# https://www.maxpixel.net/Running-Zombies-Scary-Male-Creepy-Zombie-3118441
zombiePic = PhotoImage(file="runningZombie.png")
# https://www.shutterstock.com/video/clip-31566124-spooky-forest-loop--3d-animation-endless
bgPic = PhotoImage(file="forest.png")
# https://www.freeiconspng.com/img/30572
trophyPic = PhotoImage(file="trophy.png")
# https://badgeos.org/downloads/leaderboards/
leaderboardPic = PhotoImage(file="leaderboard.png")

mainMenu()

window.mainloop()
