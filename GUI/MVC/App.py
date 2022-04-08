import tkinter as tk
from tkinter import *

from MVC.Model import Model
from MVC.View import View
from MVC.Controller import Controller




class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Tkinter MVC Demo')

        # create a model
        model = Model('hello@pythontutorial.net')

        # create a view and place it on the root window
        view = View(self)
        view.grid(row=0, column=0, padx=10, pady=10)

        # create a controller
        controller = Controller(model, view)

        # set the controller to view
        view.set_controller(controller)

        def returnFileName():
            return view.fileName

        icn = PhotoImage(file = 'icn.png')
        self.iconphoto(False,icn)
