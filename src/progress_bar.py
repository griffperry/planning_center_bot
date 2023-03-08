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

    def check_progress(self):
        current_completed_groups = 0 #len(self.completed_groups)
        while len(self.completed_groups) < self.num_groups:
            time.sleep(1)
            print(len(self.completed_groups))
            if len(self.completed_groups) > current_completed_groups:
                self.progress()
                current_completed_groups += 1
                print(f"updated current count to {current_completed_groups}")
        showinfo(message='The progress completed!')
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

        start_button = ttk.Button(
            self.root,
            text='Start',
            command=self.check_progress
        )
        start_button.grid(column=0, row=2, padx=10, pady=10, sticky=tk.E)

        self.root.mainloop()
