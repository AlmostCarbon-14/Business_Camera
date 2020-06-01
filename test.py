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


class ImageEngine:
    def __init__(self):
        self.ipath = ""
        self.running = True
        self.event = threading.Event()
        self.session = 1
        self.root = tk.Tk()
        self.root.title("Image Engine")
        self.root.attributes('-zoomed', True)
        #Setting up Grid Layout
        #Labels
        title = tk.Frame(master=self.root)
        img_num_title = tk.Frame(master=self.root)
        interval_title = tk.Frame(master=self.root)
        total_taken = tk.Frame(master=self.root)
        total_pics = tk.Frame(master=self.root)
        #Text Box
        interval_box = tk.Frame(master=self.root)
        #Buttons
        interval_dec = tk.Frame(master=self.root)
        interval_inc = tk.Frame(master=self.root)
        take_now = tk.Frame(master=self.root)
        end_now = tk.Frame(master=self.root)
        #Grid Setup, same format
        title.grid(row= 1, column= 3)
        interval_title.grid(row= 3, column= 3)
        total_pics.grid(row= 7, column= 1)
        total_taken.grid(row= 7, column= 3)

        interval_box.grid(row= 4, column= 3)

        interval_dec.grid(row= 4, column= 1)
        interval_inc.grid(row= 4, column= 6)
        take_now.grid(row= 5, column = 3)
        end_now.grid(row= 6, column = 3)

        #Labels
        header = tk.Label(master= title, text= "Timelapse Controller", foreground= "black")
        interval = tk.Label(master= interval_title, text= "Interval Between Shots", foreground= "black")
        img_total = tk.Label(master= total_taken, text= "0", foreground= "red", font= ("Times", 16))
        img_total_label = tk.Label(master= total_pics, text= "Total Images Taken", foreground= "black")
        #Textbox
        interval = tk.Entry(master= interval_box, justify= "center")
        interval.insert(0, "1 Hour")
        #Buttons
        inc = tk.Button(master= interval_inc, text= "Faster", fg= "red")
        dec = tk.Button(master= interval_dec, text= "Slower", fg= "red")
        take = tk.Button(master= take_now, text= "Take Photo Now", fg= "red")
        end = tk.Button(master= end_now, text= "End Session", fg= "red")
        #Binding Buttons to functions
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
        root.mainloop()


    def parse_delay(self):
        args = parse_interval()
        return 5
       # if args[1] == "Minutes":
       #     return str(int(args[0]) * 60)
       # else:
       #     return str(int(args[0]) * 3600)


    def pad(self, value):
        if value < 10:
            return "000" + str(value)
        if value < 100:
            return "00" + str(value)
        if value < 1000:
            return "0" + str(value)
        return str(value)

    def p_script(self, lock, m_path):
        lock.acquire()
        file_name = "pic-" + pad(self.pic_index) + ".jpg"
        self.pic_index += 1
        lock.release()
        try:
            os.system("fswebcam -r 1280x720 " + file_name)
            os.system("cp pic* " + m_path)
            os.system("rm pic*")
            total = int(img_total.cget("text"))
            print("Total", total)
            total += 1
            img_total.config(text= str(total))
           self.root.update()
        except:
            print("EXCEPTION OCCURED")
            lock.acquire()
            pic_index -= 1
            lock.release()
            return

    def take_photo(self,m_path):
        lock = threading.Lock()
        pic_thread = threading.Thread(target = p_script, args = (lock, m_path ))
        pic_thread.start()
        pic_thread.join()

    def system_loop(self, delay):
        if self.i_path == "":
            self.i_path = build_path()
        delay = parse_delay()
        while self.running:
            take_photo(self.i_path)
            event.wait(timeout= delay)

    def build_path(self):
        day = datetime.datetime(date.today().year, date.today().month,  date.today().day)
        day = day.strftime("%d-%b-%Y")
        img_path = "../../../../media/usb/Sessions/" + day + "-" + str(session)
        if path.exists(img_path) == False:
            os.system("mkdir " + img_path)
        return img_path


    def parse_interval(self):
        return interval.get().split(" ")
    
    def end_session(self, ignore):
        self.running = False
        self.event.set()
        self.session += 1
        self.i_path = ""
        if messagebox.askyesno("Finish", "Would you like to save and shutdown?"):
            os.system("sudo shutdown -h now")
        return


    def force(self, ignore):
        if self.i_path == "":
            self.i_path = build_path()
        take_photo(self.i_path)
        return

    def decrement(self, ignore):
        val = parse_interval()
        interval.delete(0, 'end')
        if val[0] == "15" and val[1] == "Minutes":
            interval.insert(0, "15 Minutes")
            return
        if val[1] == "Minutes":
            interval.insert(0, str(int(val[0]) - 15) + " Minutes")
            return
        if val[0] == "1":
            interval.insert(0, "45 Minutes")
            return
        if val[0] == "2":
            interval.insert(0, "1 Hour")
        else:
            interval.insert(0, str(int(val[0]) - 1) + " Hours") 

    def increment(self, ignore):
        val = parse_interval()
        interval.delete(0, 'end')
        if val[0] == "45" and val[1] == "Minutes":
            interval.insert(0, "1 Hour")
            return
        if val[1] == "Minutes":
            interval.insert(0, str(int(val[0]) + 15) + " Minutes")
            return
        if val[0] == "1":
            interval.insert(0, "2 Hours")
            return
        interval.insert(0, str(int(val[0]) + 1) + " Hours")



