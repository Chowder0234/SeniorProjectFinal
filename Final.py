#imports
from tkinter import *
from tkinter import ttk
import statistics

#begin backend work

import csv
  
with open('GVSplit.csv') as infile:
  # read the file as a dictionary for each row ({header : value})
  reader = csv.DictReader(infile)
  data = {}
  for row in reader:
    for header, value in row.items():
      try:
        data[header].append(value)
      except KeyError:
        data[header] = [value]

#Entire Data -> Course Code -> Course Number -> Instructor -> Grade Info
courseDict = {}

#Creating a series of dictionaries for each layer of the search
def createCourseList():
    #turning data into lists
    courseCode = data['Course Code']
    courseNumber = data['Course Number']
    instructor = data['Instructor']
    for code in courseCode:
        for key in courseDict:
            if key == code:
                break
        else:
            courseDict[code] = {}
    count = 0
    while count < len(courseCode):
        for key in courseDict[courseCode[count]]:
            if key == courseNumber[count]:
                break
        else:
            courseDict[courseCode[count]][courseNumber[count]] = {}
        count += 1
    count = 0
    while count < len(courseNumber):
        for key in courseDict[courseCode[count]][courseNumber[count]]:
            if key == instructor[count]:
                break
        else:
            courseDict[courseCode[count]][courseNumber[count]][instructor[count]] = []
        count += 1
    
def addCourseList():
   courseCode = data['Course Code']
   courseNumber = data['Course Number']
   instructor = data['Instructor']
   count = 0
   while count < len(courseCode):
      header = ["A","A-","B+","B","B-","C+","C","C-","D+","D","F","I","W","AU","CR","NC","X","NR","IP","Total","GPA"]
      grades = []
      for i in header:
         grades.append(data[i][count])
      courseDict[courseCode[count]][courseNumber[count]][instructor[count]] = grades
      count += 1

createCourseList()
addCourseList()

#printing a list to show dictionary layers & grade distribs 
#(can be removed if you want to speed up final product, but kept for clarity)
for x in courseDict:
    print("|--- " + x)
    for y in courseDict[x]:
        print("| |--- " + y)
        for z in courseDict[x][y]:
            print("| | |--- " + z + " = ", courseDict[x][y][z])

#begin frontend work

#creating the frame
root = Tk()
root.geometry("400x600+750+250")
frame = Frame(root)
frame.pack()
c_width = 400  # Define its width
c_height = 250  # Define its height
c = Canvas(root, width=c_width, height=c_height, bg='white')
c.pack()

leftframe = Frame(root)
leftframe.pack(side=LEFT)
 
rightframe = Frame(root)
rightframe.pack(side=RIGHT)

#initial welcome text at the top
label = Label(frame, text = "Grade Distribution Finder", font = "Helvetica 20 bold", fg = "dark blue")
label.pack(padx = 5, pady = 15)

##current values
majorCB = "Select Major ID"
courseCB = "Select Course Number"
professorCB = "Select Professor"

#creating drop down boxes
majorCombo = ttk.Combobox(frame, values = list(courseDict.keys()))
majorCombo.set(majorCB)
majorCombo.pack(padx = 5, pady = 5)

courseCombo = ttk.Combobox(frame)
courseCombo.set(courseCB)
courseCombo.pack(padx = 5, pady = 5)

professorCombo = ttk.Combobox(frame)
professorCombo.set(professorCB)
professorCombo.pack(padx = 5, pady = 5)

#updating combo boxes 
def majorComboUpdate(event):
   majorCB = majorCombo.get()
   courseCB = "Select Course Number"
   courseCombo.set(courseCB)
   courseCombo['values'] = []
   professorCB = "Select Professor"
   professorCombo.set(professorCB)
   professorCombo['values'] = []
   if majorCB in courseDict:
      courseCombo['values'] = list(courseDict[majorCB].keys())
majorCombo.bind("<<ComboboxSelected>>", majorComboUpdate)

def courseComboUpdate(event):
   majorCB = majorCombo.get()
   courseCB = courseCombo.get()
   professorCB = "Select Professor"
   professorCombo.set(professorCB)
   professorCombo['values'] = []
   if majorCB in courseDict:
      if courseCB in courseDict[majorCB]:
         professorCombo['values'] = list(courseDict[majorCB][courseCB].keys())
courseCombo.bind("<<ComboboxSelected>>", courseComboUpdate)

#printing results (averages, totals and bar graph)

#["A","A-","B+","B","B-","C+","C","C-","D+","D","F","I","W","AU","CR","NC","X","NR","IP","Total","GPA"]
def printResults():
   majorCB = majorCombo.get()
   courseCB = courseCombo.get()
   professorCB = professorCombo.get()
   c.delete("all")
   grades = ["A","A-","B+","B","B-","C+","C","C-","D+","D","F"]
   if majorCB in courseDict and courseCB in courseDict[majorCB] and professorCB in courseDict[majorCB][courseCB]:
      avglabel['text'] = courseDict[majorCB][courseCB][professorCB][20]
      totallabel['text'] = courseDict[majorCB][courseCB][professorCB][19]
      bargraphData = []
      for i in range(0,11):
         bargraphData.append(int(courseDict[majorCB][courseCB][professorCB][i]))
      for x, y in enumerate(bargraphData):
         w = y / max(bargraphData) * 340

         x0 = 50
         y0 = x * 250 / 12
         x1 = 50 + w
         y1 = (x + 1) * 250 / 12
         c.create_rectangle(x0, y0, x1, y1, fill="black")
         c.create_text(30, y1, anchor=SW, text=str(y))
         c.create_text(10, y1, anchor=SW, text=grades[x])
   else:
      avglabel['text'] = "Invalid Input"
      totallabel['text'] = "Invalid Input"

#search button
Button = Button(frame, text = "Search", command = printResults)
Button.pack(padx = 5, pady = 15)

#creating labels that indicate intended outputs
label = Label(frame, text = "Average GPA:", font = "Helvetica 16 bold")
label.pack()

avglabel = Label(frame, text = "Press Search", fg = "red")
avglabel.pack()

label = Label(frame, text = "Total Students:", font = "Helvetica 16 bold")
label.pack()

totallabel = Label(frame, text = "Press Search", fg = "red")
totallabel.pack()

label = Label(frame, text = "Grade Distribution:", font = "Helvetica 16 bold")
label.pack()

#program title and ending mainloop
root.title("Grade Distribution Finder")
root.mainloop()