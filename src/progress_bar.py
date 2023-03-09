from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo
import tkinter as tk
import time


class ProgressBar():

    def __init__(self, groups, completed_groups):
        self.completed_groups = completed_groups
        self.num_groups = len(groups)

    def update_progress_label(self):
        return f"Current Progress: {self.pbar['value']}%"

    def progress(self):
        if self.pbar['value'] < 100:
            percent_complete = float(1/self.num_groups)*100
            self.pbar['value'] += percent_complete
            self.value_label['text'] = self.update_progress_label()
            self.value_label.update()

    def check_progress(self):
        current_completed_groups = 0
        while len(self.completed_groups) < self.num_groups+1:
            time.sleep(0.5)
            if len(self.completed_groups) > current_completed_groups:
                self.progress()
                current_completed_groups += 1
                if current_completed_groups == self.num_groups:
                    break
        self.value_label['text'] = "Complete"
        self.value_label.update()
        time.sleep(3)
        self.root.destroy()

    def start_progress(self):
        self.root = Tk()
        self.root.geometry('300x120')
        self.root.title('Progressbar')
        self.pbar = ttk.Progressbar(
            self.root,
            orient='horizontal',
            mode='determinate',
            length=280
        )
        self.pbar.grid(column=0, row=0, columnspan=2, padx=10, pady=20)
        self.value_label = ttk.Label(self.root, text=self.update_progress_label())
        self.value_label.grid(column=0, row=1, columnspan=2)

        self.root.after(1000, self.check_progress)
        self.root.mainloop()
