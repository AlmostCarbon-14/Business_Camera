#!/usr/bin/env python

from PIL import Image, ImageTk
import Tkinter as tk
import tkMessageBox as messagebox
import threading
import datetime
import imutils
import cv2
import os
print "-" * 25 + "Imports Complete" + "-" * 25


class ImagePreview:
    def __init__(self, vs):
        self.vs = vs
        self.frame = None
        self.thread = None
        self.stopEvent = None

        self.root = tk.Tk()
        self.panel = None

        button = tk.Button(self.root, text = "Confirm Focus", command = self.activate_GUI)
        button.pack(side = "bottom", fill = "both", expand = "yes", padx = 10, pady = 10)

        self.stopEvent = threading.Event()
        self.thread = threading.Thread(target = self.videoLoop, args= ())
        self.thread.start()

        self.root.wm_title("Image Preview and Validation")
        self.root.wm_protocol("WM_DELETE_WINDOW", self.onClose)

    def videoLoop(self):
        try:
            while not self.stopEvent.is_set():
                self.frame = self.vs.read()
                self.frame = imutils.resize(self.frame, width = 300)
                image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(image)
                image = ImageTk.PhotoImage(image)

                if self.panel is None:
                    self.panel = tk.Label(image = image)
                    self.panel.image = image
                    self.panel.pack(side = "left", padx = 10, pady = 10)
                else:
                    self.panel.configure(image = image)
                    self.panel.image = image
        except RuntimeError, e:
            print("[ERR] Caught Runtime Error")

    def activate_GUI(self):
        if messagebox.askyesno("Validate", "Are you sure the camera is properly aimed and focused?"):
            self.onClose()
            os.system("./test.py")

    def onClose(self):
        self.stopEvent.set()
        self.vs.stop()
        self.root.quit()

