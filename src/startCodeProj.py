from tkinter import *
from tkinter import filedialog
from tkinter.ttk import Combobox
import pandas as pd

root = Tk()
root.title("CSE 350 Project")
root.geometry("1325x700")
root.resizable(False, False)

lengthOfHeaders = 0; valueOfCheckList = []; valueOfComboList = []; buttonsAndChecksList = []; df = pd.DataFrame

def getCSVFile() -> None:
    global df
    root.filename = filedialog.askopenfilename(title="Select A CSV File", filetypes=[("CSV Files", "*.csv")])
    df = pd.read_csv(root.filename)
    getCSVHeaders(df)
    gg = Button(root, text = "Get Graphs & Data")
    gg.grid(column=0, row=(6+lengthOfHeaders), columnspan=2)
    buttonsAndChecksList.append(gg)

def getCSVHeaders(df: pd.DataFrame) -> None:
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
        ch = Checkbutton(root, text=h, variable=valueOfCheckList[c], onvalue=1, offvalue=0, width=20)
        ch.grid(column=0, row=(6+c))
        buttonsAndChecksList.append(ch)
        cb = Combobox(root, text="Select Graph Format", values=['Line', 'Scatter', 'Histogram', 'Bar'], textvariable=valueOfComboList[c])
        cb.current(0)
        cb.grid(column=1, row=(6+c))
        buttonsAndChecksList.append(cb)
        c += 1
    
titleLabel = Label(root, text="CSE 350 Data Visualization Project").grid(column=0, row=0, columnspan=2)
filebutton = Button(root, text = "Upload CSV File", command = getCSVFile).grid(column=0, row=1, columnspan=2)
headerLabel = Label(root, text="Select Headers to Graph").grid(column=0, row=5)
pickGraphForHeaderLabel = Label(root, text="Select Graph Format").grid(column=1, row=5)

root.mainloop()