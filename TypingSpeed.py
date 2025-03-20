from tkinter import *
import ctypes
import random
import time
import tkinter

ctypes.windll.shcore.SetProcessDpiAwareness(1)

root = Tk()
root.title('Type Speed Test')
root.geometry('2160x1080')
root.option_add("*Label.Font", "consolas 30")
root.option_add("*Button.Font", "consolas 30")

# Variables
writeAble = False
passedSeconds = 0
start_time = 0
correct_chars = 0
total_chars = 0

# Functions
def keyPress(event=None):
    global correct_chars, total_chars
    if not writeAble:
        return
    try:
        expected_char = labelRight.cget('text')[0].lower()
        typed_char = event.char.lower()
        if typed_char == expected_char:
            labelLeft.configure(text=labelLeft.cget('text') + typed_char)
            labelRight.configure(text=labelRight.cget('text')[1:])
            correct_chars += 1
            if labelRight.cget('text'):
                currentLetterLabel.configure(text=labelRight.cget('text')[0])
            else:
                stopTest()
        total_chars += 1
        updateStats()
    except tkinter.TclError:
        pass

def updateStats():
    wpm = (correct_chars / 5) / (max(passedSeconds, 1) / 60)
    accuracy = (correct_chars / max(1, total_chars)) * 100
    statsLabel.configure(text=f'WPM: {int(wpm)} | Accuracy: {int(accuracy)}%')

def resetWritingLabels():
    possibleTexts = [
        'For writers, a random sentence can help them get their creative juices flowing...',
        'The goal of Python Code is to provide Python tutorials, recipes, problem fixes...',
        'As always, we start with the imports. Because we make the UI with tkinter...'
    ]
    text = random.choice(possibleTexts).lower()
    splitPoint = 0

    global labelLeft
    labelLeft = Label(root, text=text[0:splitPoint], fg='grey')
    labelLeft.place(relx=0.5, rely=0.5, anchor=E)

    global labelRight
    labelRight = Label(root, text=text[splitPoint:])
    labelRight.place(relx=0.5, rely=0.5, anchor=W)

    global currentLetterLabel
    currentLetterLabel = Label(root, text=text[splitPoint], fg='grey')
    currentLetterLabel.place(relx=0.5, rely=0.6, anchor=N)

    global timeleftLabel
    timeleftLabel = Label(root, text=f'0 Seconds', fg='grey')
    timeleftLabel.place(relx=0.5, rely=0.4, anchor=S)

    global statsLabel
    statsLabel = Label(root, text='WPM: 0 | Accuracy: 0%', fg='black')
    statsLabel.place(relx=0.5, rely=0.3, anchor=S)

    global writeAble, passedSeconds, correct_chars, total_chars, start_time
    writeAble = True
    passedSeconds = 0
    correct_chars = 0
    total_chars = 0
    start_time = time.time()

    root.bind('<Key>', keyPress)
    root.after(60000, stopTest)
    root.after(1000, addSecond)

def stopTest():
    global writeAble
    writeAble = False

    amountWords = len(labelLeft.cget('text').split(' '))

    timeleftLabel.destroy()
    currentLetterLabel.destroy()
    labelRight.destroy()
    labelLeft.destroy()
    statsLabel.destroy()

    global ResultLabel
    ResultLabel = Label(root, text=f'Words per Minute: {amountWords}', fg='black')
    ResultLabel.place(relx=0.5, rely=0.4, anchor=CENTER)

    global ResultButton
    ResultButton = Button(root, text=f'Retry', command=restart)
    ResultButton.place(relx=0.5, rely=0.6, anchor=CENTER)

def restart():
    ResultLabel.destroy()
    ResultButton.destroy()
    resetWritingLabels()

def addSecond():
    global passedSeconds
    passedSeconds += 1
    timeleftLabel.configure(text=f'{passedSeconds} Seconds')
    updateStats()
    if writeAble:
        root.after(1000, addSecond)

resetWritingLabels()
root.mainloop()
