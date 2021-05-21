import tkinter as tk
import threading
import time
import random

delta=10
left=False
right=False
startFieldX=delta
startFieldY=delta
fieldWidth=400+delta
fieldHeight=250+delta
countOfBlocksHorizontaly=10
countOfBlocksVerticaly=6
blockHeight=int(((fieldHeight-delta)/3)/countOfBlocksVerticaly)
blockWidth=int((fieldWidth-delta)/countOfBlocksHorizontaly)

blocksChanged=False

i=1
j=1
k=0

ballWidth=6
ballRadius=ballWidth/2
ballStep=1
boardStep=2
boardWidth=60
boardHeight=4
currentBoardX = ((fieldWidth)/2)+startFieldX

currentX=currentBoardX
currentY=fieldHeight-boardHeight-ballRadius
blocks=[]
blockItems=[]
koeff=1
event=threading.Event()
gameOwer=False

def main():
    global delta, fieldWidth, fieldHeight, thread, object, blocks
    createBlocks(2)
    root = tk.Tk()
    root.geometry(str(fieldWidth+delta*2)+"x"+str(fieldHeight+delta*2))
    canvas = tk.Canvas(root,width=fieldWidth,height=fieldHeight)
    canvas.create_rectangle(startFieldX, startFieldY, fieldWidth, fieldHeight)

    for b in blocks:
        b.drawBlock(canvas)
    canvas.pack()

    key_tracker = KeyTracker()
    root.bind_all('<KeyPress>', key_tracker.report_key_press)
    root.bind_all('<KeyRelease>', key_tracker.report_key_release)
    key_tracker.track('space')
    root.focus()

    btnPause=tk.Button(root,text="pause")
    btnPause.config(command=lambda : event.clear())
    btnContinue=tk.Button(root,text="continue")
    btnContinue.config(command=lambda : event.set())
    btnStart=tk.Button(root,text="start")
    btnStart.config(command=lambda : startt())
    btnRestart=tk.Button(root,text="restart")
    btnRestart.config(command=lambda : restart(canvas))
    btnStart.pack(side=tk.LEFT)
    btnPause.pack(side=tk.LEFT)
    btnContinue.pack(side=tk.LEFT)
    btnRestart.pack(side=tk.LEFT)
    event.clear()
    thread = MyThread(canvas,event)
    thread.setDaemon(True)
    thread.start()
    root.mainloop()

def restart(canvas):

    global blocks, blockItems, currentX, currentY, currentBoardX, labelGameOwer, koeff, ball, board, ballColor, boardColor
    event.clear()
    blocks.clear()
    for b in blockItems:
        canvas.delete(b)
    createBlocks(2)
    for b in blocks:
        b.drawBlock(canvas)

    canvas.delete(ball)
    canvas.delete(board)

    currentBoardX = ((fieldWidth) / 2) + startFieldX
    currentX = currentBoardX
    currentY = fieldHeight - boardHeight - ballRadius
    ball = canvas.create_oval(currentX + i * koeff * ballStep - ballRadius, currentY + j * ballStep - ballRadius,
                                   currentX + i * koeff * ballStep + ballRadius, currentY + j * ballStep + ballRadius,
                                   fill=ballColor)
    board = canvas.create_rectangle(currentBoardX - boardWidth / 2 + k * boardStep, fieldHeight - boardHeight,
                                         currentBoardX + boardWidth / 2 + k * boardStep, fieldHeight, fill=boardColor)

    canvas.delete(labelGameOwer)
    koeff=1


def startt():
    global j
    j=-1
    event.set()


def createBlocks(mod):
    global blocks
    if mod==1:
        for i in range(countOfBlocksHorizontaly):
            x = delta + blockWidth * i
            for j in range(countOfBlocksVerticaly):
                y=delta+blockHeight*j
                block =Block(x,y)
                blocks.append(block)
    elif mod==2:
        for i in range(1,countOfBlocksHorizontaly):
            x = delta + blockWidth * i
            for j in range(1,countOfBlocksVerticaly):
                y=delta+blockHeight*j
                block =Block(x,y)
                blocks.append(block)


class MyThread(threading.Thread):
    def __init__(self, canvas, event):
        super().__init__()
        self.canvas=canvas
        self.event=event

    def run(self):
        global left,right,i,j,k,currentX,currentY,ballWidth,ballStep,boardWidth,boardStep,currentBoardX,boardHeight, blocksChanged, blockItems,koeff, labelGameOwer, ball, board, ballColor, boardColor
        ballColor = hex_code_colors()
        boardColor = hex_code_colors()
        while True:
            ball = self.canvas.create_oval(currentX+i*koeff*ballStep-ballRadius, currentY+j*ballStep-ballRadius, currentX+i*koeff*ballStep+ballRadius, currentY+j*ballStep+ballRadius, fill=ballColor)
            board = self.canvas.create_rectangle(currentBoardX-boardWidth/2+k*boardStep, fieldHeight-boardHeight, currentBoardX+boardWidth/2+k*boardStep, fieldHeight, fill=boardColor)
            if blocksChanged:
                blocksChanged=False
                for it in blockItems:
                    self.canvas.delete(it)
                for b in blocks:
                    b.drawBlock(self.canvas)

            event.wait()
            time.sleep(0.01)
            self.canvas.delete(ball)
            self.canvas.delete(board)
            currentX=currentX+i*koeff*ballStep
            currentY=currentY+j*ballStep

            currentBoardX=currentBoardX+k*boardStep

            if right==True and currentBoardX+boardWidth/2<fieldWidth:
                k=1
            elif left==True and currentBoardX-boardWidth/2>startFieldX:
                k=-1
            else:
                k=0

            if currentX>fieldWidth-ballRadius:
                i=-1
            if currentX<startFieldX+ballRadius:
                i=1
            if currentY>fieldHeight-ballRadius:
                labelGameOwer=self.canvas.create_text((fieldWidth/2,fieldHeight/2),text="game ower")
                event.clear()
            if currentY<startFieldY+ballRadius:
                j=1

            if blocksChanged==False:
                for block in blocks:
                    if (j==-1 and block.y+blockHeight-ballRadius<=currentY-ballRadius<=block.y+blockHeight and block.x+blockWidth+ballRadius>currentX>block.x-ballRadius):
                        blocks.remove(block)
                        blocksChanged=True
                        j=1
                        break
                    if (j==1 and block.y<=currentY+ballRadius<=block.y+ballRadius and block.x+blockWidth+ballRadius>currentX>block.x-ballRadius):
                        blocks.remove(block)
                        blocksChanged=True
                        j=-1
                        break
                    if (i==-1 and block.x+blockWidth-ballRadius<=currentX-ballRadius<=block.x+blockWidth and block.y+blockHeight+ballRadius>currentY>block.y-ballRadius):
                        blocks.remove(block)
                        blocksChanged = True
                        i = 1
                        break
                    if (i==1 and block.x<=currentX+ballRadius<=block.x+ballRadius and block.y+blockHeight+ballRadius>currentY>block.y-ballRadius):
                        blocks.remove(block)
                        blocksChanged = True
                        i = -1
                        break

            if (currentY>fieldHeight-ballWidth/2-boardHeight and currentX+ballWidth/2>currentBoardX-boardWidth/2 and currentX-ballWidth/2<currentBoardX+boardWidth/2):
                part1=currentX-(currentBoardX-boardWidth/2)
                part2=(currentBoardX+boardWidth/2)-currentX
                if part1>part2:
                    koeff=1-part2/part1
                if part2>part1:
                    koeff=1-part1/part2
                if koeff > 0.5:
                    koeff = 0.5
                j=-1


class Block:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.color=hex_code_colors()

    def drawBlock(self,canvas):
        global blockHeight,blockWidth,blockItems
        item = canvas.create_rectangle(self.x,self.y, self.x+blockWidth,self.y+blockHeight,fill=self.color,outline="black")
        blockItems.append(item)

def keyup(e):
    global right, left
    if e.keysym=='Right':
        right=False
        print("right",right)
    if e.keysym=='Left':
        left=False
        print('left',left)

def keydown(e):
    global right, left
    if e.keysym=='Right':
        right=True
        print("right",right)
    if (e.keysym == 'Left'):
        left = True
        print('left', left)

class KeyTracker():
    key = ''
    last_press_time = 0
    last_release_time = 0
    waiting_to_test_release = False

    def track(self, key):
        self.key = key

    def is_pressed(self):
      return time.time() - self.last_press_time < .1

    def report_key_press(self, event):
        #if event.keysym == self.key:
            if not self.is_pressed():
                print('press')
                keydown(event)
            self.last_press_time = time.time()

    def report_key_release(self, event):
        #if event.keysym == self.key:
            if not self.waiting_to_test_release:
                timer = threading.Timer(.1, self.report_key_release_callback, args=[event])
                timer.start()
                print(time.time())

    def report_key_release_callback(self, event):
        print(time.time())
        print()
        if not self.is_pressed():
            print('rel')
            keyup(event)
        self.last_release_time = time.time()

def hex_code_colors():
    a = hex(random.randrange(0, 256))
    b = hex(random.randrange(0, 256))
    c = hex(random.randrange(0, 256))
    a = a[2:]
    b = b[2:]
    c = c[2:]
    if len(a) < 2:
        a = "0" + a
    if len(b) < 2:
        b = "0" + b
    if len(c) < 2:
        c = "0" + c
    z = a + b + c
    return "#" + z.upper()

if __name__=="__main__":
    main()