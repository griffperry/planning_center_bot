from tkinter import *
from tkinter import ttk
import time


class ProgressBar():

    def __init__(self, root, completed_groups, num_groups):
        self.root = root
        self.completed_groups = completed_groups
        self.num_groups = num_groups

        self.pb = ttk.Progressbar(
            root,
            orient='horizontal',
            mode='indeterminate',
            length=280
        )
        self.pb.pack()
        self.value_label = ttk.Label(root, text="")
        self.value_label.pack()

    def update_progress_label(self):
        return f"Current Progress: {self.pb['value']}%"

    def progress(self):
        if self.pb['value'] < 100:
            percent_complete = float(1/self.num_groups)*100
            self.pb['value'] += percent_complete
            self.value_label['text'] = self.update_progress_label()
            self.value_label.update()

    def check_progress(self):
        breakpoint()
        self.value_label.configure(text=self.update_progress_label())
        self.pb.start()
        current_completed_groups = 0
        while len(self.completed_groups) < self.num_groups+1:
            time.sleep(0.5)
            print(self.completed_groups)
            if len(self.completed_groups) > current_completed_groups:
                self.progress()
                current_completed_groups += 1
                if current_completed_groups == self.num_groups:
                    self.pb.stop()
                    break
        self.value_label['text'] = "Complete"
        self.value_label.update()
        time.sleep(3)

    def start_progress(self):
        self.root = Tk()
        self.root.geometry('300x120')
        self.root.title('Progressbar')
        self.pb = ttk.Progressbar(
            self.root,
            orient='horizontal',
            mode='determinate',
            length=280
        )
        self.pb.grid(column=0, row=0, columnspan=2, padx=10, pady=20)
        self.value_label = ttk.Label(self.root, text=self.update_progress_label())
        self.value_label.grid(column=0, row=1, columnspan=2)

        self.check_progress()
