#!/usr/bin/env python3
import serial

import threading

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

#style.use('fivethirtyeight') #plot 

#fig = plt.figure()
#ax1 = fig.add_subplot(1,1,1)




#read text file
f = open("COM_PORT.txt", "r")
com_port = f.read()
print("In COM_PORT.txt: " + str(com_port))


#Get time and date <---- If something breaks here, attempt Try-Catch to install the python lib. If already installed, nothing bad will happen. 

import datetime
 
# using now() to get current time
current_time = datetime.datetime.now() #get current time 
temp = str(current_time) #get 
temp = temp[0:10] + "_" +temp[11:13] + "-" + temp[14:16] + "-" + temp[17:19]


#com_port = #"COM17" #'/dev/ttyACM0'
baud = 9600
filename = temp + ".csv" #"test.csv"

#fig = plt.figure()
#ax1 = fig.add_subplot(1,1,1)




'''
Author: Nicholas Chorette
Date Created: 8/18/2023
Purpose: Log Circuits lab data (automate it and log it to a csv file). If I desire (prob not) I can attempt to implement this code in MATLAB. Students can use MATLAB themselves reguardless of what I do :) 

Doing this for fun. 

Ref. Links: 
https://www.geeksforgeeks.org/writing-csv-files-in-python/

'''



            

#def setUpFile(fileName): 

def animate(i): #for the plot 
    graph_data = open(filename,'r').read() #this will get progressively slower and slower the more and more data that gets logged 0_0  (and may actually SLOW DOWN datalogging if it is bad enough 0_0. Smart person would use asynch or something... but. we dont do that here B) ) 
    lines = graph_data.split('\n')
    xs = []
    ys = []
    for line in lines:
        if len(line) > 1:
            x, y = line.split(',')
            xs.append(float(x))
            ys.append(float(y))
    ax1.clear()
    ax1.plot(xs, ys)
    

def extractNumber(dataInput): 
    bruteForceCheck = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.'] #quick and dirty. get the job done (cringe, but it will work )
    #filter out lables
    temp = ""
    i = str(i)

    for j in dataInput: 
        if j  in bruteForceCheck: #only rip out numbers please 
            temp += j
    return temp
            
        


def writeLog(filename, fields): #may need to just delete later idk 
    #use this to log data into a CSV file. If it is NOT too resource intensive, you can attemp to plot this data as well. ____KEEP THE NAMING SCHEME CONSISTENT 
    bruteForceCheck = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.'] #quick and dirty. get the job done (cringe, but it will work )
    with open(filename, 'a') as csvfile: 
        # creating a csv dict writer object 
        for i in fields:

            #filter out lables
            temp = ""
            i = str(i)

            for j in i: 
                if j  in bruteForceCheck: #only rip out numbers please 
                    temp += j
            
            csvfile.write(str(temp) + ",")#csv.DictWriter(csvfile, fieldnames = fields)


             
            
        # writing headers (field names) 
        csvfile.write("\n")
            
        # writing headers (field names) 
        # writer.writeheader() 
            
        # writing data rows 
        #writer.writerows(fields) 
#'''
plotCounter = [0] 
plotData = [0]

def updatePlot(): 

    ax1.clear() #clear plot to make way for NEW DATA! 


    print("plotCounter = " + str(plotCounter))
    print("plotData = " + str(plotData))
    ax1.plot(plotCounter, plotData)


   # fig = plt.figure()
    #ax1 = fig.add_subplot(1,1,1)

    


def trueUpdate(): 
    ani = animation.FuncAnimation(fig, updatePlot, interval=1)#ani = animation.FuncAnimation(fig, animate, interval=1)
    plt.show()
    

if __name__ == '__main__': #core part of the pgm
    ser = serial.Serial(com_port, baud, timeout=1)
    ser.reset_input_buffer()
    counter = 0 
    fields = [0]*5 #this will be the input data, just replace each one with it's respective item 
    #filename = "test.csv"
    fields = [ 'rpm', 'N-m', 'deg', 'KW'] #removed time logging, b/c nobody (at the moment) needs that information 

    

   # t1 = threading.Thread(target=trueUpdate, name='t2')
   # t1.start()



    with open(filename, 'w') as csvfile: 
        # creating a csv dict writer object 

        for i in fields: 
            csvfile.write(i + ",")#csv.DictWriter(csvfile, fieldnames = fields) 
            
        # writing headers (field names) 
        csvfile.write("\n")
         

    while True:
        if ser.in_waiting > 0:
            
            line = ser.readline().decode('utf-8').rstrip()

            print(line)
            #print("Line: " + str(line))
            #print( "Counter: " + str(counter))

            #find where the START of a log is
            if((line == "****************") or (counter >=5)): 
                counter = -1 #NOTE This is done to compensate for the end of the loop, resulting in start of a new time around still being zero  
                # field names 
                writeLog(filename, fields)
                for i in range(len(fields)): 
                    fields[i] = 0 #just clear em all outta there (do not want data getting cross-contaminated potentially
                #plot the data HERE

                #plotData.append(extractNumber(fields[3]))
                #plotData.append(fields[3]) #<----------PICK WHICH ONE YOU WANT TO PLOT HERE (unless you decide to plot them all. in that case idk )
                #plotCounter.append(plotCounter[len(plotCounter)-1] + 1) #incriment the next item added to the array by 1 
                #t1.join()




            else: 
                fields[counter] = line 
                #you will need to filter out specific character length. This may be unique to every single one. If this is the case, you may consider using a switch statement, or a looping IF statement till the end of the string (for i in stringName -> if number append, else ignore -> convert to int), may be more processing power than its worth
            

            #----------Attempting to make plot for ONLY the RPM (for an initial test here, might be able to crank out other plots depending on how well this one works... )
            
            

            #ani = animation.FuncAnimation(fig, animate, interval=1)
            plt.show()



            counter +=1 #put at end of the loop code 

            
                 
           # if(counter >= 3 ): #this is when we want to ALSO log the data ____this might need to be sat to 4, idk 
                






















    '''
    there were 4 parameters there. And, if we want to, we can add time to this to make it 5 parameters. 

    I do not recall what aditional sensors could read DC voltage that high other than those super cheap sensors, and for AC we got smart plugs, but like, realistically thats kinda...idk how to export that data (and it would be exclusively 120v probs... but reguardless, you could use a transformer for that and step it down & log the data accordingly tbh... (making sure you know all the parameters of the measurement tool's transformer and take them into account,... reguardless... moving on))...

    Under the assumption that more data can be automatically logged, I do not see why it is unreasonable to make this log all data, and matlab just analyze the CSV :P

    yeah yeah, it would be nice if you didnt have to use 2 seporate programs, idc im doing this for fun. 

    -NIC_ 8/18/2023 @ 2:26pm
    
    '''

