from tkinter import *
from tkinter import ttk
import time


class ProgressBar():

    def __init__(self, root, completed_groups, num_groups):
        self.main_root = root
        self.completed_groups = completed_groups
        self.num_groups = num_groups

    def update_progress_label(self):
        return f"Current Progress: {self.pb['value']: .2f}%"

    def progress(self):
        if self.pb['value'] < 100:
            percent_complete = float(1/self.num_groups*100)
            self.pb['value'] += percent_complete
            self.value_label['text'] = self.update_progress_label()
            self.value_label.update()

    def check_progress(self):
        self.value_label.update()
        current_completed_groups = 0
        while current_completed_groups < self.num_groups:
            time.sleep(0.1)
            if len(self.completed_groups) > current_completed_groups:
                self.progress()
                current_completed_groups += 1
        self.value_label['text'] = "Complete"
        self.value_label.update()
        time.sleep(3)

    def start_progress_bar(self):
        self.root = Toplevel(self.main_root)
        self.root.geometry('300x120')
        self.root.title('Progressbar')
        self.pb = ttk.Progressbar(
            self.root,
            orient='horizontal',
            mode='determinate',
            length=280
        )
        Label(self.root, text="").pack()
        self.pb.pack()
        self.value_label = ttk.Label(self.root, text=self.update_progress_label())
        Label(self.root, text="").pack()
        self.value_label.pack()
        self.check_progress()
