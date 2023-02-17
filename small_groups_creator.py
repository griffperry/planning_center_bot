#!/usr/bin/env python3

from src.main_process import main_func
from tkinter import *
import sys


def upload_data():
    global upload_screen
    upload_screen = Toplevel(main_screen)
    upload_screen.title("Upload Small Group Data")
    upload_screen.geometry("300x250")
    global file
    global file_entry
    file = StringVar()
    file_lable = Label(upload_screen, text="")
    file_lable.pack()
    file_entry = Entry(upload_screen, textvariable=file)
    file_entry.pack()
    Label(upload_screen, text="").pack()
    Button(upload_screen, text="Upload", width=10, height=1, bg="green", command=upload_button).pack()

def upload_button():
    file_info = file.get()
    data = open(file_info, "w")
    data.write(file_info + "\n")
    data.close()
    file_entry.delete(0, END)
    Label(upload_screen, text="Small Groups uploaded", fg="green", font=("calibri", 11)).pack()

def login():
    global login_screen
    login_screen = Toplevel(main_screen)
    login_screen.title("Login to Planning Center")
    login_screen.geometry("300x300")
    Label(login_screen, text="Please enter details below to begin").pack()
    Label(login_screen, text="").pack()
    global username_verify
    global password_verify
    global demo_verify
    username_verify = StringVar()
    password_verify = StringVar()
    demo_verify = StringVar()
    global username_login_entry
    global password_login_entry
    global demo_entry

    Label(login_screen, text="Username * ").pack()
    username_login_entry = Entry(login_screen, textvariable=username_verify)
    username_login_entry.pack()
    Label(login_screen, text="").pack()

    Label(login_screen, text="Password * ").pack()
    password_login_entry = Entry(login_screen, textvariable=password_verify, show= '*')
    password_login_entry.pack()
    Label(login_screen, text="").pack()

    Label(login_screen, text="Demo mode will delete groups at the end.\nWould you like to demo? [yes/no].").pack()
    demo_entry = Entry(login_screen, textvariable=demo_verify)
    demo_entry.pack()
    Label(login_screen, text="").pack()

    Button(login_screen, text="Login and Start", width=18, height=1, command=login_verify).pack()

def login_verify():
    username1 = username_verify.get()
    password1 = password_verify.get()
    demo1 = demo_verify.get().lower()
    username_login_entry.delete(0, END)
    password_login_entry.delete(0, END)
    demo_entry.delete(0, END)
    demo_flag = True if "y" in demo1 else False
    success = main_func(username1, password1, demo=demo_flag, app_run=True)
    if success:
        report_sucess()
    else:
        report_failure()

def report_sucess():
    global login_success_screen
    login_success_screen = Toplevel(login_screen)
    login_success_screen.title("Success")
    login_success_screen.geometry("250x100")
    Label(login_success_screen, text="Groups were created").pack()
    Label(login_success_screen, text="Hit OK to finish").pack()
    Button(login_success_screen, text="OK", command=exit_program).pack()

def report_failure():
    global failure_screen
    failure_screen = Toplevel(login_screen)
    failure_screen.title("Success")
    failure_screen.geometry("150x100")
    Label(failure_screen, text="Login failed").pack()
    Button(failure_screen, text="OK", command=delete_failure).pack()

def exit_program():
    login_success_screen.destroy()
    login_screen.destroy()
    main_screen.destroy()
    sys.exit(1)

def delete_failure():
    failure_screen.destroy()

def main_account_screen():
    global main_screen
    main_screen = Tk()
    main_screen.geometry("300x250")
    main_screen.title("Small Group Creator")
    Label(text="").pack()
    Button(text="Upload Small Group Data", height="2", width="30", command=upload_data).pack()
    Label(text="").pack()
    Button(text="Login", height="2", width="30", command=login).pack()
    main_screen.mainloop()

if __name__ == "__main__":
    cmd_line = sys.argv[-1]
    if "create_groups" == cmd_line or "delete_groups" == cmd_line:
        main_func()
    else:
        main_account_screen()
