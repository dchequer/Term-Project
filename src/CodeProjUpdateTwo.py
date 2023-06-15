from tkinter import *
from tkinter import filedialog
from tkinter.ttk import Combobox
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
import pandas as pd

root = Tk()
root.title("CSE 350 Project")
root.geometry("1325x700")
root.resizable(False, False)

lengthOfHeaders = 0; timeName = "Local"; timeCounter = 0; rowCount = 1; fileCounter = 0; numberOfXTicks = 0; timeCount = 0; countOnce = 0; tempOneValueScaleOne = 0; tempTwoValueScaleTwo = 0; flag = 0
userEnterStartDate = StringVar(); userEnterEndDate = StringVar(); scaleOne = IntVar(); scaleTwo = IntVar(); scaleThree = IntVar(); s = Scale()
valueOfCheckList = []; valueOfComboList = []; buttonsAndChecksList = []; timeValues = []; userTimeValuesOptions = []; userTimeButtons = []; df = pd.DataFrame

def getCSVFile():
    global df
    root.filename = filedialog.askopenfilename(title="Select A CSV File", filetypes=[("CSV Files", "*.csv")])

    # catch if user doesn't select a file
    if root.filename == "":
        return
    
    df = pd.read_csv(root.filename)
    getCSVHeaders(df)
    placeButtons(69)
    tb = Button(root, text = "Change to " + timeName + " time", command = changeToLocalOrUTCTime)
    tb.grid(column=0, row=(6+lengthOfHeaders))
    buttonsAndChecksList.append(tb)
    gg = Button(root, text = "Get Graphs & Data", command=lambda: getGraphs(df))
    gg.grid(column=1, row=(6+lengthOfHeaders))
    buttonsAndChecksList.append(gg)
    setUserDefaultTime(df)

def getCSVHeaders(df: pd.DataFrame):
    global lengthOfHeaders, valueOfCheckList, buttonsAndChecksList, valueOfComboList
    valueOfCheckList.clear()
    valueOfComboList.clear()
    lengthOfHeaders = 0
    for chcb in buttonsAndChecksList:
        chcb.destroy()
    for h in df.head(0):
        lengthOfHeaders += 1
        valueOfCheckList.append(IntVar())
        valueOfComboList.append(StringVar())
    c = 0
    for h in df.head(0):
        ch = Checkbutton(root, text=h, variable=valueOfCheckList[c], onvalue=1, offvalue=0, width=20, anchor="w")
        ch.grid(column=0, row=(6+c))
        buttonsAndChecksList.append(ch)
        cb = Combobox(root, text="Select Graph Format", values=['Line', 'Scatter', 'Histogram', 'Bar'], textvariable=valueOfComboList[c])
        cb.current(0)
        cb.grid(column=1, row=(6+c))
        buttonsAndChecksList.append(cb)
        c += 1

def changeToLocalOrUTCTime():
    global timeName, timeCounter
    if timeCounter == 1:
        timeName = " UTC "; timeCounter = 0
    else:
        timeName = "Local"; timeCounter = 1
    tb = Button(root, text = "Change to " + timeName + " time", command = changeToLocalOrUTCTime)
    tb.grid(column=0, row=(6+lengthOfHeaders))
    setUserDefaultTime(df)
    getGraphs(df)

def getGraphs(df: pd.DataFrame):
    global rightFrame, rowCount, fileCounter, flag, s
    rowCount = 1; c = 0; headerList = []; flag = 0
    rightFrame.destroy()
    rightFrame = Frame(root)
    rightFrame.grid(column=2, row=0, rowspan=100)
    fileCounter = 1
    for ss in valueOfCheckList:
        if ss.get() == 1:
            flag = 1
    if scaleThree.get() < 100:
        getTimeBox(df)
    elif scaleThree.get() > 700: rowCount = -6
    elif scaleThree.get() > 600: rowCount = -5
    elif scaleThree.get() > 500: rowCount = -4
    elif scaleThree.get() > 400: rowCount = -3
    elif scaleThree.get() > 300: rowCount = -2
    elif scaleThree.get() > 200: rowCount = -1
    else: rowCount = 0
    getTimeFrame(df)
    scatterSize = getScatterSize()
    for h in df.head(0):
        headerList.append(h)
    for ss in valueOfCheckList:
        if ss.get() == 1:
            if rowCount >= 0:
                Fig = Figure(figsize = (10, 2), dpi = 100)
                Plot = Fig.add_subplot(111)
                if valueOfComboList[c].get() == 'Scatter':#hist(Histogram), bar(Bar), scatter(Scatter), plot(line)
                    Plot.scatter(timeValues[scaleOne.get():scaleTwo.get()], df[headerList[c]][scaleOne.get():scaleTwo.get()], s=scatterSize)
                elif valueOfComboList[c].get() == 'Bar':
                    Plot.bar(timeValues[scaleOne.get():scaleTwo.get()], df[headerList[c]][scaleOne.get():scaleTwo.get()])
                elif valueOfComboList[c].get() == 'Histogram':
                    Plot.hist(df[headerList[c]][scaleOne.get():scaleTwo.get()])
                else:#default graph if not picked or not spelled correctly
                    Plot.plot(timeValues[scaleOne.get():scaleTwo.get()], df[headerList[c]][scaleOne.get():scaleTwo.get()])
                Plot.set_title(headerList[c])
                Plot.set_xticks(Plot.get_xticks()[::numberOfXTicks])
                Plot.tick_params(axis='x', which='major', labelsize=10)
                Plot.tick_params(axis='y')

                canvas = FigureCanvasTkAgg(Fig,rightFrame)
                canvas.draw()
                canvas.get_tk_widget().grid(column=2, row=(6*rowCount), rowspan=6)
            rowCount += 1
        c += 1
    if flag == 1:
        s = Scale(root, from_=0, to=timeCount, length=700, variable=scaleThree, bd=0, showvalue=False, command=changeInScale)
        s.place(x=1305, y=0)
        placeButtons(75)
    else: scaleThree.set(0); s.destroy()
    if rowCount != 1 or scaleThree.get() > 100:
        getStats(df)

def getScatterSize():
    if int((scaleTwo.get()-scaleOne.get()) < int(timeCount/2.5)): return 10
    if int((scaleTwo.get()-scaleOne.get()) < int(timeCount/2.3)): return 9
    if int((scaleTwo.get()-scaleOne.get()) < int(timeCount/2.1)): return 8
    if int((scaleTwo.get()-scaleOne.get()) < int(timeCount/1.9)): return 7
    if int((scaleTwo.get()-scaleOne.get()) < int(timeCount/1.8)): return 6
    if int((scaleTwo.get()-scaleOne.get()) < int(timeCount/1.6)): return 5
    if int((scaleTwo.get()-scaleOne.get()) < int(timeCount/1.4)): return 4
    if int((scaleTwo.get()-scaleOne.get()) < int(timeCount/1.2)): return 3
    return 2

def getStats(df: pd.DataFrame):
    c = 0; seriesList = []; headerList = []; completeStatsList = []; statsNamesList = ['Count', 'Mean', 'STD', 'Min', '25%', '50%', '75%', 'Max']
    for h in df.head(0):
        if valueOfCheckList[c].get() == 1:
            seriesList.append(df[h].describe())
            headerList.append(h)
        c += 1
    for seary in seriesList:
        f = 0
        secondPartOfText = ''
        for data in seary:
            try:
                secondPartOfText += statsNamesList[f] + ': ' + str(round(data, 2)) + "        "
            except TypeError:
                secondPartOfText += statsNamesList[f] + ': ' + str(data) + "        "
            f += 1
        completeStatsList.append(secondPartOfText)
    c = 0
    for s in completeStatsList:
        Label(rightFrame, text=headerList[c] + ':\t\t\t' + s, width=130, anchor="w").grid(column=2, row=((rowCount*6)+1+c))
        c += 1

def getTimeBox(df: pd.DataFrame):
    global fileCounter, timeCount, countOnce, numberOfXTicks, timeCounter
    placeOnce = 0; c = 0; headerList = []
    for h in df.head(0):
        headerList.append(h)
    for ss in valueOfCheckList:
        if ss.get() == 1 and placeOnce == 0:
            Fig = Figure(figsize = (10, 2), dpi = 100)
            Plot = Fig.add_subplot(111)
            Plot.plot(df['Datetime (UTC)'], df[headerList[c]])
            Plot.set_title('Time Box of ' + headerList[c])
            Plot.axis('off')
            canvas = FigureCanvasTkAgg(Fig,rightFrame)
            canvas.draw()
            canvas.get_tk_widget().grid(column=2, row=0, rowspan=6)
            placeOnce += 1
        c += 1

    countTimeString = (str(df['Datetime (UTC)'].describe())).replace(" ", "")
    timeCount = int(countTimeString[(countTimeString.index('count')+5):(countTimeString.index('unique'))])
    if fileCounter == 1:
        Scale(rightFrame, from_=0, to=timeCount, length=400, orient=HORIZONTAL, variable=scaleOne, bd=0, showvalue=False, command=changeInScale).place(x=120, y=180)
        Scale(rightFrame, from_=0, to=timeCount, length=400, orient=HORIZONTAL, variable=scaleTwo, bd=0, showvalue=False, command=changeInScale).place(x=530, y=180)
        if countOnce == 0:
            scaleOne.set(userTimeValuesOptions.index(userEnterStartDate.get()))
            scaleTwo.set(userTimeValuesOptions.index(userEnterEndDate.get())+1)
            countOnce += 1
            numberOfXTicks = int(timeCount/4)
        if flag == 0:
            placeButtons(69)
        else:
            placeButtons(62)
        if timeCounter == 0:
            Label(rightFrame, text=datetime.utcfromtimestamp((df['Unix Timestamp (UTC)'].values[scaleOne.get()])/1000)).place(x=15, y=155)
            Label(rightFrame, text=datetime.utcfromtimestamp((df['Unix Timestamp (UTC)'].values[(scaleTwo.get()-1)])/1000)).place(x=885, y=155)
        else:
            Label(rightFrame, text=datetime.utcfromtimestamp(((df['Unix Timestamp (UTC)'].values[scaleOne.get()]+(df['Timezone (minutes)'].values[(scaleTwo.get()-1)]*60000)))/1000)).place(x=15, y=155)
            Label(rightFrame, text=datetime.utcfromtimestamp(((df['Unix Timestamp (UTC)'].values[(scaleTwo.get()-1)]+(df['Timezone (minutes)'].values[(scaleTwo.get()-1)]*60000)))/1000)).place(x=885, y=155)
        distCount = 1
        if timeCount > 730:
            distCount = 2
        lengthOfLabelLeft = 140+(scaleOne.get()/distCount)
        lengthOfLabelRight = 870-((timeCount-scaleTwo.get())/distCount)
        Label(rightFrame, text='', height=10, width=1).place(x=lengthOfLabelLeft, y=20)
        Label(rightFrame, text='', height=10, width=1).place(x=lengthOfLabelRight, y=20)
        lengthOfDottedLines = lengthOfLabelRight-lengthOfLabelLeft+10
        C1 = Canvas(rightFrame, width=lengthOfDottedLines, height=8)
        C1.create_line(10,5,lengthOfDottedLines,5, dash=(5,1))
        C1.place(x=lengthOfLabelLeft, y=20)
        C2 = Canvas(rightFrame, width=lengthOfDottedLines, height=8)
        C2.create_line(10,5,lengthOfDottedLines,5, dash=(5,1))
        C2.place(x=lengthOfLabelLeft, y=165)
        fileCounter += 1

def changeInScale(var):
    global tempOneValueScaleOne, tempTwoValueScaleTwo, numberOfXTicks
    c = 0
    if scaleOne.get() == 0 and scaleTwo.get() == timeCount:
        tempOneValueScaleOne = 0
        tempTwoValueScaleTwo = timeCount
    elif tempOneValueScaleOne != scaleOne.get() or tempTwoValueScaleTwo != scaleTwo.get():
        if scaleOne.get() >= scaleTwo.get(): 
            scaleOne.set((scaleTwo.get()-1))
        if scaleTwo.get() <= scaleOne.get():
            scaleTwo.set((scaleOne.get()-1))
        numberOfXTicks = int((scaleTwo.get()-scaleOne.get())/4)
        if numberOfXTicks == 0:
            numberOfXTicks = 1
        getGraphs(df)
        c += 1
    if c == 0:
        getGraphs(df)

def getTimeFrame(df: pd.DataFrame):
    global timeValues
    timeValues = []
    for i in range(timeCount):
        if timeCounter == 0:
            timeValues.append(str((datetime.utcfromtimestamp((df['Unix Timestamp (UTC)'].values[i])/1000))))
        else:
            timeValues.append(str((datetime.utcfromtimestamp(((df['Unix Timestamp (UTC)'].values[i])+(df['Timezone (minutes)'].values[i]*60000))/1000))))

def setUserDefaultTime(df: pd.DataFrame):
    global userTimeValuesOptions, timeCounter
    userTimeValuesOptions = []
    for i in range(len(df)):
        if timeCounter == 0:
            userTimeValuesOptions.append(str((datetime.utcfromtimestamp((df['Unix Timestamp (UTC)'].values[i])/1000))))
        else:
            userTimeValuesOptions.append(str((datetime.utcfromtimestamp(((df['Unix Timestamp (UTC)'].values[i])+(df['Timezone (minutes)'].values[i]*60000))/1000))))
    userEnterStartDate.set(userTimeValuesOptions[0])
    userEnterEndDate.set(userTimeValuesOptions[len(userTimeValuesOptions)-1])

def placeButtons(y1):
    global userTimeButtons
    for b in userTimeButtons:
        b.destroy()
    userTimeButtons = []; boost = 0
    if rowCount > 6: boost = ((rowCount-2)*5)+19
    elif rowCount > 5: boost = ((rowCount-2)*5)+14
    elif rowCount > 4: boost = ((rowCount-2)*5)+9
    elif rowCount > 3: boost = ((rowCount-2)*5)+4
    elif rowCount > 2: boost = ((rowCount-2)*5)
    elif rowCount > 1: boost = ((rowCount-2)*5)-5
    b1 = Button(root, text='▲', command=increaseUserTimeInputsLeft, width=1, height=1); b1.place(x=130, y=y1+boost)
    b2 = Button(root, text='▼', command=decreaseUserTimeInputsLeft, width=1, height=1); b2.place(x=130, y=y1+20+boost)
    b3 = Button(root, text='▲', command=increaseUserTimeInputsRight, width=1, height=1); b3.place(x=284, y=y1+boost)
    b4 = Button(root, text='▼', command=decreaseUserTimeInputsRight, width=1, height=1); b4.place(x=284, y=y1+20+boost)
    userTimeButtons.append(b1); userTimeButtons.append(b2); userTimeButtons.append(b3); userTimeButtons.append(b4)

def increaseUserTimeInputsLeft():
    global countOnce
    try:
        if userTimeValuesOptions.index(userEnterStartDate.get())+1 < len(userTimeValuesOptions):
            userEnterStartDate.set(userTimeValuesOptions[userTimeValuesOptions.index(userEnterStartDate.get())+1])
            countOnce = 0
    except:
        userEnterStartDate.set(userTimeValuesOptions[0])

def decreaseUserTimeInputsLeft():
    global countOnce
    try:
        if userTimeValuesOptions.index(userEnterStartDate.get())-1 > 0:
            userEnterStartDate.set(userTimeValuesOptions[userTimeValuesOptions.index(userEnterStartDate.get())-1])
            countOnce = 0
    except:
        userEnterStartDate.set(userTimeValuesOptions[0])

def increaseUserTimeInputsRight():
    global countOnce
    try:
        if userTimeValuesOptions.index(userEnterEndDate.get())+1 < len(userTimeValuesOptions):
            userEnterEndDate.set(userTimeValuesOptions[userTimeValuesOptions.index(userEnterEndDate.get())+1])
            countOnce = 0
    except:
        userEnterEndDate.set(userTimeValuesOptions[len(userTimeValuesOptions)-1])

def decreaseUserTimeInputsRight():
    global countOnce
    try:
        if userTimeValuesOptions.index(userEnterEndDate.get())-1 > 0:
            userEnterEndDate.set(userTimeValuesOptions[userTimeValuesOptions.index(userEnterEndDate.get())-1])
            countOnce = 0
    except:
        userEnterEndDate.set(userTimeValuesOptions[len(userTimeValuesOptions)-1])
    
titleLabel = Label(root, text="CSE 350 Data Visualization Project").grid(column=0, row=0, columnspan=2)
filebutton = Button(root, text = "Upload CSV File", command = getCSVFile)
filebutton.grid(column=0, row=1, columnspan=2)
dateLabel1 = Label(root, text="Select Start Date: ").grid(column=0, row=3)
dateLabel2 = Label(root, text="Select End Date: ").grid(column=1, row=3)
userEntryStartTime = Entry(root, textvariable=userEnterStartDate).grid(column=0, row=4, ipady=15)
userEntryEndTime = Entry(root, textvariable=userEnterEndDate).grid(column=1, row=4, ipady=15)
headerLabel = Label(root, text="Select Headers to Graph").grid(column=0, row=5)
pickGraphForHeaderLabel = Label(root, text="Select Graph Format").grid(column=1, row=5)
rightFrame = Frame(root)
rightFrame.grid(column=2, row=0)

root.mainloop()