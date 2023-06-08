from tkinter import *
from tkinter import filedialog
from tkinter.ttk import Combobox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

root = Tk()
root.title("CSE 350 Project")
root.geometry("1325x700")
root.resizable(False, False)

lengthOfHeaders = 0; timeName = "Local"; timeCounter = 1; rowCount = 1; numberOfXTicks = 0
userEnterStartDate = StringVar(); userEnterEndDate = StringVar()
valueOfCheckList = []; valueOfComboList = []; buttonsAndChecksList = []; df = pd.DataFrame

def getCSVFile():
    global df, numberOfXTicks
    root.filename = filedialog.askopenfilename(title="Select A CSV File", filetypes=[("CSV Files", "*.csv")])
    df = pd.read_csv(root.filename)
    getCSVHeaders(df)
    tb = Button(root, text = "Change to " + timeName + " time", command = changeToLocalOrUTCTime)
    tb.grid(column=0, row=(6+lengthOfHeaders))
    buttonsAndChecksList.append(tb)
    gg = Button(root, text = "Get Graphs & Data", command=lambda: getGraphs(df))
    gg.grid(column=1, row=(6+lengthOfHeaders))
    buttonsAndChecksList.append(gg)
    countTimeString = (str(df['Datetime (UTC)'].describe())).replace(" ", "")
    timeCount = int(countTimeString[(countTimeString.index('count')+5):(countTimeString.index('unique'))])
    numberOfXTicks = int(timeCount/4)

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
        ch = Checkbutton(root, text=h, variable=valueOfCheckList[c], onvalue=1, offvalue=0)
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
    Button(root, text = "Change to " + timeName + " time", command = changeToLocalOrUTCTime).grid(column=0, row=(6+lengthOfHeaders))

def getGraphs(df: pd.DataFrame):
    global rightFrame, rowCount
    rowCount = 1; c = 0; headerList = []
    rightFrame.destroy()
    rightFrame = Frame(root)
    rightFrame.grid(column=2, row=0, rowspan=100)
    for h in df.head(0):
        headerList.append(h)
    for ss in valueOfCheckList:
        if ss.get() == 1:
            if rowCount >= 0:
                Fig = Figure(figsize = (10, 2), dpi = 100)
                Plot = Fig.add_subplot(111)
                if valueOfComboList[c].get() == 'Scatter':#hist(Histogram), bar(Bar), scatter(Scatter), plot(line)
                    Plot.scatter(df['Datetime (UTC)'], df[headerList[c]])
                elif valueOfComboList[c].get() == 'Bar':
                    Plot.bar(df['Datetime (UTC)'], df[headerList[c]])
                elif valueOfComboList[c].get() == 'Histogram':
                    Plot.hist(df[headerList[c]])
                else:#default graph if not picked or not spelled correctly
                    Plot.plot(df['Datetime (UTC)'], df[headerList[c]])
                Plot.set_title(headerList[c])
                Plot.set_xticks(Plot.get_xticks()[::numberOfXTicks])
                Plot.tick_params(axis='x', which='major', labelsize=10)

                canvas = FigureCanvasTkAgg(Fig,rightFrame)
                canvas.draw()
                canvas.get_tk_widget().grid(column=2, row=(6*rowCount), rowspan=6)
            rowCount += 1
        c += 1

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