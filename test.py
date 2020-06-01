#!/usr/bin/env python3

import os
import datetime
import time
import sys
from datetime import date
from os import path
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk as ttk
from tkinter import *
import tkinter.font as tkFont
import threading

running = True
pic_index = 0
event = threading.Event()
path = ""
session = 1

def parse_delay():
    args = parse_interval()
    return 5
   # if args[1] == "Minutes":
   #     return str(int(args[0]) * 60)
   # else:
   #     return str(int(args[0]) * 3600)


def pad(value):
    if value < 10:
        return "000" + str(value)
    if value < 100:
        return "00" + str(value)
    if value < 1000:
        return "0" + str(value)
    return str(value)

def p_script(lock, path):
    global pic_index
    lock.acquire()
    file_name = "pic-" + pad(pic_index) + ".jpg"
    pic_index += 1
    lock.release()
    try:
        os.system("fswebcam -r 1280x720 " + file_name)
        os.system("cp pic* " + path)
        os.system("rm pic*")
    except:
        lock.acquire()
        pic_index -= 1
        lock.release()
        return
    total = int(img_total.cget("text"))
    total += 1
    img_total.config(text= str(total))
    window.update()

def take_photo(path):
    lock = threading.Lock()
    pic_thread = threading.Thread(target = p_script, args = (lock, path ))
    pic_thread.start()
    pic_thread.join()

def system_loop(delay):
    global path, running, pic_index
    if path == "":
        path = build_path()
    delay = parse_delay()
    while running:
        take_photo(path)
        event.wait(timeout= delay)


def build_path():
    day = datetime.datetime(date.today().year, date.today().month,  date.today().day)
    day = day.strftime("%d-%b-%Y")
    img_path = "../../../media/usb/Sessions/" + day + "-" + str(session)
    if path.exists(img_path) == False:
        os.system("mkdir " + img_path)
    return img_path


def parse_interval():
    return interval.get().split(" ")
    

def end_session(ignore):
    global running, event, session, build_path
    running = False
    event.set()
    session += 1
    build_path = ""
    result = messagebox.asyesno("Finish", "Would you like to save and shutdown?")
    print("RESULT:", result)
    return


def force(ignore):
    global path
    if path == "":
        path = build_path()
    take_photo(path)
    return

def decrement(ignore):
    val = parse_interval()
    interval.delete(0, 'end')
    if val[0] == "15" and val[1] == "Minutes":
        return
    if val[1] == "Minutes":
        interval.set(0, str(int(val[0]) - 15) + " Minutes")
        return
    if val[0] == "1":
        interval.set(0, "45 Minutes")
        return
    if val[0] == "2":
        interval.set(0, "1 Hour")
    else:
        interval.set(0, str(int(val[0]) - 1) + " Hours") 

def increment(ignore):
    val = parse_interval()
    interval.delete(0, 'end')
    if val[0] == 45 and val[1] == "Minutes":
        interval.set(0, "1 Hour")
        return
    if val[1] == "Minutes":
        interval.set(0, str(int(val[0]) + 15) + " Minutes")
        return
    if val[0] == "1":
        interval.set(0, "2 Hours")
        return
    interval.set(0, str(int(val[0]) + 1) + " Hours")


window = tk.Tk()
window.title("Image Engine")
window.attributes('-zoomed', True)

title = tk.Frame(master= window)
img_num_title = tk.Frame(master= window)
interval_title = tk.Frame(master= window)
total_taken = tk.Frame(master= window)
total_pics = tk.Frame(master= window)
interval_box = tk.Frame(master= window)

interval_dec = tk.Frame(master= window)
interval_inc = tk.Frame(master= window)
take_now = tk.Frame(master= window)
end_now = tk.Frame(master= window)

title.grid(row= 1, column= 3)
interval_title.grid(row= 3, column= 3)
total_pics.grid(row= 6, column= 1)
total_taken.grid(row= 6, column= 3)

interval_box.grid(row= 4, column= 3)

interval_dec.grid(row= 4, column= 1)
interval_dec.grid(row= 4, column= 5)
take_now.grid(row= 5, column = 3)
end_now.grid(row= 6, column = 3)


header = tk.Label(master= title, text= "Timelapse Controller", foreground= "black")
interval = tk.Label(master= interval_title, text= "Interval Between Shots", foreground= "black")
img_total = tk.Label(master= total_taken, text= "0", foreground= "red", font= ("Times", 16))
img_total_label = tk.Label(master= total_pics, text= "Total Images Taken", foreground= "black")

interval = tk.Entry(master= interval_box, justify= "center")
interval.insert(0, "1 Hour")

dec = tk.Button(master= interval_dec, text= "Faster", fg= "red")
inc = tk.Button(master= interval_inc, text= "Slower", fg= "red")
take = tk.Button(master= take_now, text= "Take Photo Now", fg= "red")
end = tk.Button(master= end_now, text= "End Session", fg= "red")

dec.bind("<Button-1>", decrement)
inc.bind("<Button-1>", increment)
take.bind("<Button-1>", force)
end.bind("<Button-1>", end_session)

header.pack()
interval.pack()
img_total.pack()
img_total_label.pack()
interval.pack()
dec.pack()
inc.pack()
end.pack()
take.pack()

window.mainloop()






