#!/bin/python3
 
from os import listdir
from os.path import isfile, join
import plotly.offline as py
import plotly.graph_objs as go
from tkinter import *
from tkinter import filedialog
import time
import webbrowser
 
# GUI Class
 
class Window(Frame):
 
    # Initializes the frame
 
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()
 
    # Initializes buttons and labels
 
    def init_window(self):
        self.master.title("Data Visualizer")
        self.pack(fill=BOTH, expand=1)
        label = Label(self, wraplength=350, text="Click start to browse to the folder where the Nessus scans are stored and begin analysis")
        label.pack(pady=50, padx=10)
        label.place(x=20,y=30)
        startButton = Button(self, text="Start",command=self.start)
        startButton.place(x=165, y=85)
 
    # This function is called when the Start button is clicked
 
    def start(self):
        foldername = filedialog.askdirectory()
        self.visualize(foldername)
        Frame.quit(self)
 
    # Analyzes a folder for vulnerability counts and visualizes the data
 
    def visualize(self, folder):
        vulns = [0,0,0,0,0] # Stores vulnerabiliy counts. From left to right: Critical, High, Medium, Low, None
        colors = ['#E51016', '#F17E12', '#FAF128', '#24D313', '#0F97E5'] # Specifies hex codes for colors that represent each vulnerability
        onlyfiles = [f for f in listdir(folder) if isfile(join(folder, f))]
        count = 0
 
        # Read and store the data from each file
 
        for i in onlyfiles:
            currfile = open(folder + '/' + i,'r')
            lines = currfile.readlines()
            num = 0
            for k in lines:
                if 'Risk Factor' in k:
                    vulntype = lines[num + 2] # The line specifying the risk factor type is exactly 2 lines after the line containing "Risk Factor"
                    if 'Critical' in vulntype:
                        vulns[0] += 1
                    elif 'High' in vulntype:
                        vulns[1] += 1
                    elif 'Medium' in vulntype:
                        vulns[2] += 1
                    elif 'Low' in vulntype:
                        vulns[3] += 1
                    elif 'None' in vulntype:
                        vulns[4] +=1
                num += 1
            count += 1
            print("Finished file: " + str(count))
            currfile.close()
 
        # Custom HTML/CSS to inject into the generated graph file
 
        injectedText = '''<html>
        <head><meta charset="utf-8" />
        <style>
 
        #vulns {
          display:inline;
        }
 
        #vulns font {
          padding-left:10px;
        }
 
        </style>
        </head>
        <body>
          <h3>Vulnerabilities By Risk Factor</h3>
          <h4>Visual generated on '''  + str(time.strftime("%a %b %d, %Y")) + '''&nbsp
          <div id = "vulns">
           - <font color = "#E51016">Critical Count: ''' + str(vulns[0]) + ''' </font>
          <font color = "#F17E12">High Count: ''' + str(vulns[1]) + ''' </font>
          <font color = "#e1ad01">Medium Count: ''' + str(vulns[2]) + ''' </font>
          <font color = "#24D313">Low Count: ''' + str(vulns[3]) + ''' </font>
          <font color = "#0F97E5">None Count: ''' + str(vulns[4]) + ''' </font>
        </div></h4>'''
 
 
        labels = ['Critical','High','Medium','Low','None']
 
        # Generate the graph
 
        trace = go.Pie(labels=labels, values=vulns, marker=dict(colors=colors,
                                   line=dict(color='#000000', width=2)))
        py.plot([trace], filename='scanchart.html', auto_open=False)      
 
 
        # Inject the custom HTML/CSS
 
        scanfile = open("scanchart.html",'r')
        lines = scanfile.readlines()
        writelines = lines[3:]
        scanfile.close()
        scanfile = open("scanchart.html", 'w')
        scanfile.write(injectedText)
        for k in writelines:
            scanfile.write(k)
        scanfile.close()
        webbrowser.open("scanchart.html")
 
# Instantiate, set the size, and run a new instance of the GUI
 
root = Tk()
root.geometry("400x140")
app = Window(root)
root.mainloop()
