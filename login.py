import tkinter as tk
from tkinter import messagebox

import server
from app import connector


def siema(key):
    kod.focus()
    if kod.get() == "Skanuj kartę użytkownika...":
        kod.delete(0, "end")
        kod.insert(0, key.char)


def handleReturn(e):
    print(kod.get())
    req = server.Request(kod.get())
    global user
    user = req.usr
    if user.isExist(connector.con):
        log.destroy()
    elif kod.get() == "admin":
        return
    else:
        tk.messagebox.showerror(
            "Error", "Nie odnaleziono użytkownika o podanym numerze :(("
        )
        kod.select_range(0, "end")


def temp_text(e):
    if kod.get() == "Skanuj kartę użytkownika...":
        kod.delete(0, "end")


log = tk.Tk()
log.geometry("250x80")
log.resizable(False, False)
log.title("LOGIN")

tlo = tk.Frame(
    bg="#ffdd03",
    master=log,
)
kod = tk.Entry(master=tlo)
kod.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=15)
kod.insert(0, "Skanuj kartę użytkownika...")

tlo.pack(
    fill=tk.BOTH,
    expand=True,
)

log.bind("<Key>", siema)
kod.bind("<FocusIn>", temp_text)
kod.bind("<Return>", handleReturn)


log.mainloop()
