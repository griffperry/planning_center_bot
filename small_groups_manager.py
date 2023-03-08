#!/usr/bin/env python3

from src.main_process import main_func
from src.data_generator import DataGenerator
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import sys
import time
import tkinter as tk


class UserInterface():

    def main_account_screen(self):
        self.main_screen = Tk()
        self.main_screen.geometry("300x120")
        self.main_screen.title("Small Groups Manager")
        Label(text="").pack()
        ttk.Button(self.main_screen, text="Upload Small Groups", command=self.upload_data).pack()
        Label(text="").pack()
        ttk.Button(self.main_screen, text="Login", command=self.login).pack()

    def upload_data(self):
        self.upload_screen = Toplevel(self.main_screen)
        self.upload_screen.title("Upload Small Group Data")
        self.upload_screen.geometry("325x175")
        Label(self.upload_screen, text="").pack()

        self.filename = StringVar()
        self.file_entry = Entry(self.upload_screen, textvariable=self.filename)
        self.file_entry.pack()

        self.browser_used = False
        browse_button = ttk.Button(self.upload_screen, text="Browse", command=self.browse)
        browse_button.pack()
        Label(self.upload_screen, text="").pack()

        self.upload_success = False
        verify_button = ttk.Button(self.upload_screen, text="Submit Small Groups", command=self.verify)
        verify_button.pack()
        self.status_label = Label(self.upload_screen, text="")
        self.status_label.pack()

    def browse(self):
        self.browser_used = True
        self.status_label.configure(text="")
        self.filename = filedialog.askopenfilename(initialdir = "/",
                                                   title = "Select a File",
                                                   filetypes = (("Excel files", "*.xlsx*"),)
                                                )
        self.file_entry.delete(0, END)
        self.file_entry.insert(0, self.filename)

    def verify(self):
        filename = self.filename if self.browser_used else self.filename.get()
        if filename:
            dg = DataGenerator()
            if dg.submit_data(filename):
                self.file_entry.delete(0, END)
                self.upload_success = True
                self.set_upload_status("Small Groups Verified")
            else:
                self.set_upload_status("Error with Small Group Data")
        else:
            self.set_upload_status("Please Submit Small Group Data")

    def set_upload_status(self, text):
        color = "green" if self.upload_success else "red"
        self.status_label.configure(text=text, fg=color, font=("calibri", 11))
        if self.upload_success:
            self.upload_screen.update()
            time.sleep(3)
            self.upload_screen.destroy()

    def login(self):
        self.main_screen.destroy()
        self.login_screen = Tk()
        self.login_screen.title("Login to Planning Center")
        self.login_screen.geometry("300x300")
        Label(self.login_screen, text="").pack()

        Label(self.login_screen, text="Username * ").pack()
        self.username_verify = StringVar()
        self.username_login_entry = Entry(self.login_screen, textvariable=self.username_verify)
        self.username_login_entry.pack()
        Label(self.login_screen, text="").pack()

        Label(self.login_screen, text="Password * ").pack()
        self.password_verify = StringVar()
        self.password_login_entry = Entry(self.login_screen, textvariable=self.password_verify, show= '*')
        self.password_login_entry.pack()
        Label(self.login_screen, text="").pack()

        Label(self.login_screen, text="Would you like to demo? [yes/no].").pack()
        self.demo_verify = StringVar()
        self.demo_entry = Entry(self.login_screen, textvariable=self.demo_verify)
        self.demo_entry.pack()
        Label(self.login_screen, text="").pack()

        ttk.Button(self.login_screen, text="Create Groups", command=self.create_groups).pack()
        Label(self.login_screen, text="").pack()
        ttk.Button(self.login_screen, text="Delete Groups", command=self.delete_groups).pack()

    def create_groups(self):
        username1 = self.username_verify.get()
        self.username_login_entry.delete(0, END)
        password1 = self.password_verify.get()
        self.password_login_entry.delete(0, END)
        demo1 = self.demo_verify.get().lower()
        self.demo_entry.delete(0, END)
        demo_flag = True if "y" in demo1 else False

        self.login_screen.destroy()
        success = main_func(
                        username1,
                        password1,
                        demo=demo_flag,
                        app_run=True,
                        command="create_groups",
                    )
        if success:
            self.report_sucess()
        else:
            self.report_failure()

    def delete_groups(self):
        username1 = self.username_verify.get()
        self.username_login_entry.delete(0, END)
        password1 = self.password_verify.get()
        self.password_login_entry.delete(0, END)
        demo1 = self.demo_verify.get().lower()
        self.demo_entry.delete(0, END)
        demo_flag = True if "y" in demo1 else False

        self.login_screen.destroy()
        success = main_func(username1, password1, demo=demo_flag, app_run=True, command="delete_groups")
        if success:
            self.report_sucess()
        else:
            self.report_failure()

    def report_sucess(self):
        self.login_success_screen = Tk()
        self.login_success_screen.title("Success")
        self.login_success_screen.geometry("250x100")
        Label(self.login_success_screen, text="All done!").pack()
        Label(self.login_success_screen, text="Hit OK to exit").pack()
        ttk.Button(self.login_success_screen, text="OK", command=self.exit_program).pack()

    def exit_program(self):
        self.login_success_screen.destroy()
        self.main_screen.destroy()
        sys.exit(1)

    def report_failure(self):
        self.failure_screen = Tk()
        self.failure_screen.title("Success")
        self.failure_screen.geometry("150x100")
        Label(self.failure_screen, text="Login failed").pack()
        ttk.Button(self.failure_screen, text="OK", command=self.delete_failure).pack()

    def delete_failure(self):
        self.failure_screen.destroy()

if __name__ == "__main__":
    cmd_line = sys.argv[-1]
    if "create_groups" == cmd_line or "delete_groups" == cmd_line:
        main_func()
    else:
        ui = UserInterface()
        ui.main_account_screen()
