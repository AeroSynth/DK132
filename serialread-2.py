import serial
import serial.tools.list_ports
from tkinter import *
#import sys

import time
#import re

WIDTH = 1024#512
HEIGHT = 512#256
xDelta =5
COMPORT = 'COM48'
SCALE = 0 #4 #amount of bits to shift right (division)
RADIUS = 10 #readius of XY ball
XOFFSET = -5
YOFFSET = -9

def close_ser():
    global ser
    print("Closing Serial Port")
    ser.close() #fix this
    #tk.destroy()
    print(ser)
    quit();
    #sys.exit()

def open_ser(comPort):
    ser = serial.Serial()
    ser.baudrate = 115200 #9600
    ser.port = comPort
    #time.sleep(.5)
    ser.open()
    return ser

def linegraph():
    global gdisplay_type
    global canvas
    global x0
    print("Line Graph")
    gdisplay_type = "Line"
    canvas.delete("all")
    canvas.create_line(0,HEIGHT/2,WIDTH,HEIGHT/2) #redraw horizontal
    #x0=0
    return

def xygraph():
    global gdisplay_type
    global canvas
    global x0
    global ball
    print("XY Graph")
    gdisplay_type="XY"
    #canvas.delete("all")
    canvas.create_line(0,HEIGHT/2,WIDTH,HEIGHT/2) #redraw horizontal
    canvas.create_line(WIDTH/2,0,WIDTH/2,HEIGHT) #redraw vertical
    ball = canvas.create_oval(WIDTH/2-RADIUS,HEIGHT/2-RADIUS,WIDTH/2+RADIUS,HEIGHT/2+RADIUS,fill="red")
    #x0=0
    return

def main():
    global gdisplay_type
    global canvas
    global ball
    global ser
    gdisplay_type = "Line"
    
        # get a list of all com ports
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        print(p)

    print (gdisplay_type)
#open com ports
    #comPort = 'COM48'
    ser= open_ser(COMPORT)
    print(ser)

#create objects
    tk = Tk()
    tk.protocol("WM_DELETE_WINDOW", close_ser) #exit clicked
    #tk.protocol('WM_DELETE_WINDOW', command=lambda: close_ser)
    
    canvas = Canvas(tk, width=WIDTH, height=HEIGHT,bg="white")
    tk.title("JoyStick")
    
    canvas.create_line(0,HEIGHT/2,WIDTH,HEIGHT/2) #horizontal grid line
    plot=canvas.create_line(0,HEIGHT/2,0,HEIGHT/2,fill="red",width=3 )
    plot1=canvas.create_line(0,HEIGHT/2,0,HEIGHT/2,fill="blue",width=3 )
    canvas.pack()
    
    #menu contruction
    menubar = Menu(tk)
    filemenu = Menu(menubar,tearoff = 0) #tearoff allows you to tear out the menu, so disable it
    filemenu.add_command(label="Line Graph", command=linegraph)#,command = mNew)
    filemenu.add_command(label="X-Y Graph",command=xygraph)
    #cascade items to list
    menubar.add_cascade(label="Display",menu=filemenu)
    tk.config(menu=menubar)
    
    #setup labels on bottom of screen to display values
    var = StringVar()
    var.set("Label")
    mlabel = Label(tk,textvariable=var,fg='blue').pack()#grid(row=0,column=0,sticky=W)

    #initialize plot points
    x0=0
    y0=HEIGHT/2
    x1=x0
    y1=y0
    yy1=y0
    yy0=y0
    xx0=0

#main loop
    while True:        
        line=ser.readline()     #read in a line of data
        data = [int(val) for val in line.split()] #get values in the string

        #scale the data
        for i in range(0, 2):
            data[i] = data[i]>>SCALE
    
        #print(data[0],data[1],data[2],gdisplay_type) #print values to console
                
        var.set("x="+str(-data[0])+"      y="+str(-data[1])) #update label with value
        data[0] = data[0] + XOFFSET
        data[1] = data[1] + YOFFSET
        
        if gdisplay_type == "Line":
                       #calculate next point to draw to/from
            y1=data[1] + HEIGHT/2
            yy1=data[0] +HEIGHT/2
            x1=x0+xDelta
            plot = canvas.create_line(x0,y0,x1,y1,fill="red",width=3)
            plot1= canvas.create_line(x0,yy0,x1,yy1,fill="blue",width=3)
            y0=y1
            yy0=yy1
            x0=x0+xDelta

            #check if past right edge
            pos = canvas.coords(plot) #get coordinates
            if pos[2] >= WIDTH:  #check if past right edge of canvas
                x0=0
                canvas.delete("all") #clear the screen
                canvas.create_line(0,HEIGHT/2,WIDTH,HEIGHT/2) #redraw horizontal grid line
        else:
            #animate the ball depending on x and y
                        
            x0=data[0] + WIDTH/2 -RADIUS
            x1=x0+RADIUS*2
            y0=data[1] + HEIGHT/2 -RADIUS
            y1=y0+RADIUS*2
            canvas.delete("all")
            canvas.create_line(0,HEIGHT/2,WIDTH,HEIGHT/2) #redraw horizontal
            canvas.create_line(WIDTH/2,0,WIDTH/2,HEIGHT) #redraw vertical
            ball = canvas.create_oval(x0,y0,x1,y1,fill="red")
    #        print(pos,x0,y0,x1,y1)
            
            
        
            
        tk.update()   
        
   # ser.close()
    #tk.destroy()



if __name__ == '__main__':
    main()
    
    

