import random
import time
import tkinter
from tkinter import *
import threading
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import math

queue = []
newCustomerProbability = 2
gameSpeed = 0.1
startTime = 8 * 60  # 8.00
endTime = 9 * 60  # 9.00
clock = 0
customersServed = 0
customers = 0
waitingTime = 0
mu = 4
sigma = 1

# Lists to store data for plotting
time_points = []
customers_in_queue = []


def format_time(minutes):
    time = datetime(1, 1, 1) + timedelta(minutes=minutes)
    return time.strftime("%H:%M")


def newCustomer(clock, servers):
    global customers
    global mu
    global sigma
    s = random.randint(0, 10)
    if s <= newCustomerProbability:
        servingTime = random.gauss(mu, sigma)
        if servingTime < 0:
            servingTime = 0.5
        queue.append([1, servingTime, 0])
        customers += 1
        if len(queue) <= servers:
            text = (f"{format_time(clock)} customer {customers} comes in and is immediately served")
            texts.insert("1.0", text + "\n")
        else:
            text = (f"{format_time(clock)} customer {customers} comes in and stands in queue nr {len(queue) - servers}")
            texts.insert("1.0", text + "\n")


def server(servers):
    global customersServed
    if queue == []:
        return ("no Queue")
    for n in range(servers):
        if n <= len(queue) - 1:
            servingTime = round(queue[n][1])
            if queue[n][0] == 1:
                queue[n][0] = "#"
                queue[n][2] = 0

            if queue[n][2] < servingTime and queue[n][0] == "#":
                queue[n][2] += 1

            if queue[n][2] == servingTime and queue[n][0] == "#":
                queue.pop(n)
                customersServed += 1
        else:
            return


def mainLoop(clock, waitingTime):
    global customersServed
    while True:
        servers = int(servers_entry.get())
        gameSpeed = slider_scale.get()
        newCustomer(clock, servers)
        server(servers)
        time.sleep(2.5 - gameSpeed * 0.05)
        clock += 1
        print(clock)
        print(endTime)
        time_points.append(clock)
        customers_in_queue.append(len(queue))
        print(queue)
        for n in range(len(queue)):
            waitingTime += 1
        if clock == endTime:
            queuePerCustomer = str(round(waitingTime / customersServed, 2))
            text = "shop closing"
            texts.insert("1.0", text + "\n")
            text = (f"{customersServed} customers served")
            texts.insert("1.0", text + "\n")
            text = (f"{customers} customers in total visited")
            texts.insert("1.0", text + "\n")
            text = (f"waitingtime = {waitingTime} min = {(queuePerCustomer)} min/kund")
            texts.insert("1.0", text + "\n")
            break


# tkinter

def startSim():
    global newCustomerProbability
    global startTime
    global endTime
    global mu
    global sigma
    global clock
    # define variables from gui
    newCustomerProbability = int(newCustomerProbability_entry.get())
    startTimeHour = math.floor(float(startTime_entry.get()))
    startTimeMinute = float(startTime_entry.get()) - startTimeHour
    startTime = int(startTimeHour * 60 + startTimeMinute * 100)
    endTimeHour = math.floor(float(endTime_entry.get()))
    endTimeMinute = float(endTime_entry.get()) - endTimeHour
    endTime = int(endTimeHour * 60 + endTimeMinute * 100)
    print("starthour")
    print(startTimeHour)
    print("startmin")
    print(startTimeMinute)
    print("starttime")
    print(startTime)
    mu = int(mu_entry.get())
    sigma = int(sigma_entry.get())
    print(newCustomerProbability)
    print(startTime)
    print(endTime)
    print(mu)
    print(sigma)
    # disable gui entries
    start_button["state"] = tkinter.DISABLED
    newCustomerProbability_entry["state"] = tkinter.DISABLED
    startTime_entry["state"] = tkinter.DISABLED
    endTime_entry["state"] = tkinter.DISABLED
    mu_entry["state"] = tkinter.DISABLED
    sigma_entry["state"] = tkinter.DISABLED
    servers_entry["state"] = tkinter.DISABLED
    clock = startTime
    # start separate thread for mainloop, otherwise the gui will freeze
    t = threading.Thread(target=mainLoop, args=(clock, waitingTime))
    t.start()


def showGraph():
    # Plotting the results (only the Customers in Queue graph)
    plt.figure(figsize=(12, 6))
    plt.plot(time_points, customers_in_queue, label="Customers in Queue")
    plt.title("Customers in Queue Over Time")
    plt.xlabel("Time (minutes)")
    plt.ylabel("Number of Customers")
    plt.legend()
    plt.show()


# creates a gui window
window = Tk()

# newCustomerProbability
newCustomerProbability_entry = Entry(window, )
newCustomerProbability_label = Label(window, text="New customer probability (1-10)")

# startTime
startTime_entry = Entry(window)
startTime_label = Label(window, text="Start time (H.Min)")

# endTime
endTime_entry = Entry(window)
endTime_label = Label(window, text="End time (H.min)")

# servingtime
mu_entry = Entry(window)
sigma_entry = Entry(window)
mu_label = Label(window, text="mean serving time")
sigma_label = Label(window, text="sigma serving time (gauss distribution)")

# start button
start_button = Button(window, text="start simulation", command=startSim)

# text field
texts = Text(window)

# slider
slider_scale = Scale(window, from_=0, to=48, orient=HORIZONTAL)
slider_label = Label(window, text="simulation speed")

# graph button
button2 = Button(window, text="show graph", command=showGraph)

# servers
servers_entry = Entry(window)
servers_label = Label(window, text="servers")
# grid placement
newCustomerProbability_label.grid(row=0, column=0)
newCustomerProbability_entry.grid(row=0, column=1)
startTime_label.grid(row=0, column=2)
startTime_entry.grid(row=0, column=3)
endTime_label.grid(row=0, column=4)
endTime_entry.grid(row=0, column=5)
mu_label.grid(row=1, column=0)
mu_entry.grid(row=1, column=1)
sigma_label.grid(row=1, column=2)
sigma_entry.grid(row=1, column=3)
slider_label.grid(row=1, column=4)
slider_scale.grid(row=1, column=5)
start_button.grid(row=2, column=0)
texts.grid(row=3, column=0)
button2.grid(row=2, column=3)
servers_label.grid(row=2, column=1)
servers_entry.grid(row=2, column=2)
# loads the screen ui
window.mainloop()
