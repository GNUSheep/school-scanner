import tkinter as tk
from tkinter import messagebox
from app import connector
from functools import partial
import login

import os
import sys

import server

def unborrow(tool_id, frame):
    req = server.Request(str(tool_id))
    tool = req.tl

    tool.unborrow(connector.con)

    for widget in frame.winfo_children():
        widget.destroy()
    frame.pack_forget()

def get_tools():
    tools = login.user.get_borrowed_tools(login.user.get_name(connector.con), connector.con)

    for widget in frame_borrowed_tools.winfo_children():
        widget.destroy()
    frame_borrowed_tools.pack_forget()

    for tool in tools:
        frame_tool = tk.Frame(master=frame_borrowed_tools)

        tool_name = tk.Label(frame_tool, text=tool[1])

        action_with_arg = partial(unborrow, tool[0], frame_tool)
        unborrow_btn = tk.Button(frame_tool, text="Oddaj", command=action_with_arg)
        
        tool_name.pack(side=tk.LEFT, padx=10)
        unborrow_btn.pack(side=tk.RIGHT, padx=10)

        frame_tool.pack()
    frame_borrowed_tools.pack(pady=10)

def handleReturn(e):
    magic_function(entry.get())


def show_user(user):
    username.config(text=user.get_name(connector.con))
    logout.pack(side=tk.RIGHT, padx=15)
    username.pack(side=tk.RIGHT, padx=15)

def restart():
    os.execv(sys.executable, ['python']+sys.argv)

def log_out(widget, button, userbar):
    widget.pack_forget()
    button.pack_forget()

def magic_function(request):
    req = server.Request(request)
    tool = req.tl
    if tool.isExist(connector.con):
        if tool.isBorrowed(connector.con):
            tk.messagebox.showinfo(None, "Narzedzie jest wypożyczone")
        else:
            tool.borrow(login.user.get_name(connector.con), connector.con)
            get_tools()

    else:
        tk.messagebox.showerror(
            "Error", "Nie odnaleziono narzędzia o podanym numerze :(("
        )
        entry.select_range(0, "end")


def button_clicked(txt):
    entry.focus()
    if entry.get() == "Podaj kod artykułu...":
        temporary()
    if txt > -1 and txt < 10:
        entry.insert(tk.END, txt)
    else:
        if txt == -10:
            entry.delete(len(entry.get()) - 1, tk.END)
        if txt == 10:
            magic_function(entry.get())


def temp_text(e):
    if entry.get() == "Podaj kod artykułu...":
        entry.delete(0, "end")


def temporary():
    if entry.get() == "Podaj kod artykułu...":
        entry.delete(0, "end")


def siema(key):
    entry.focus()
    if entry.get() == "Podaj kod artykułu...":
        entry.delete(0, "end")
        entry.insert(0, key.char)


def whatever():
    exit()


def main(my_root):
    my_root.mainloop()


window = tk.Tk()
window.geometry("1000x670")
window.minsize(420, 640)
window.title("SIEMA")


main_frame_left = tk.Frame(bg="#ffdd03", width=420)
main_frame_right = tk.Frame(bg="#252525")
keyboard = tk.Frame(master=main_frame_left, bg="#ffdd03")

frame_enter = tk.Frame(
    relief=tk.RIDGE, borderwidth=10, master=main_frame_left, background="#202020"
)

skanuj = tk.Label(
    master=main_frame_left,
    text="Skanuj kod:",
    font="Kefa 40 bold",
    fg="#252525",
    bg="#ffdd03",
)
skanuj.pack(ipady=70, ipadx=100, side=tk.TOP)

userbar = tk.Frame(master=main_frame_right, bg="#1A1A1A")

username = tk.Label(
    master=userbar,
    text=login.user.get_name(connector.con),
    font="Monaco 20",
    fg="#ffdd03",
    bg="#1A1A1A",
    pady=10,
)
logout = tk.Button(
    master=userbar,
    text="Log Out",
    padx=15,
    pady=5,
    command=lambda: log_out(username, logout, userbar),
)
refresh = tk.Button(
    master=userbar,
    text="refresh",
    padx=15,
    pady=5,
    command=restart,
)
logout.pack(side=tk.RIGHT, padx=15)
username.pack(side=tk.RIGHT, padx=15)
refresh.pack(side=tk.LEFT, padx=15, pady=10)
userbar.pack(side=tk.TOP, fill=tk.X)

frame_borrowed_tools = tk.Frame(master=main_frame_right, bg="#252525")

get_tools()

entry = tk.Entry(
    master=frame_enter,
    fg="black",
)
entry.insert(0, "Podaj kod artykułu...")
entry.pack(fill=tk.X)

guzik = 1
mozna = 0

for i in range(4):
    for j in range(3):
        ramka = tk.Frame(
            master=keyboard,
            relief=tk.RAISED,
            borderwidth=5,
            background="#202020",
        )
        ramka.grid(
            row=i,
            column=j,
            padx=5,
            pady=5,
        )
        klawisz = tk.Button(
            master=ramka,
            text=guzik,
            command=lambda button_text=guzik: button_clicked(button_text),
            width=3,
            height=2,
            font="Helvetica 20 bold",
        )
        klawisz.pack(padx=5, pady=5, fill=tk.BOTH)
        if guzik == -10:
            klawisz.config(text="C")
        if guzik == 10:
            klawisz.config(text="E")
        if mozna == 1:
            guzik += 10
        if guzik < 9 and guzik > 0:
            guzik += 1
        elif guzik == 9:
            guzik = -10
            mozna = 1


keyboard.pack(side=tk.BOTTOM, pady=20)
frame_enter.pack(side=tk.TOP, padx=50, fill=tk.X)
main_frame_left.pack(fill=tk.Y, side=tk.LEFT)
main_frame_right.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

window.bind("<Key>", siema)
entry.bind("<FocusIn>", temp_text)
entry.bind("<Return>", handleReturn)

window.protocol("WM_DELETE_WINDOW", whatever)
window.mainloop()
