import tkinter as tk
from tkinter import messagebox as msg
from tkinter import ttk
import os
from PIL import ImageTk, Image

win = tk.Tk()
win.title("星月书店v1.0")
win.geometry("600x600")
icon_path = os.getcwd()+"\\resource\\paul.ico"
win.iconbitmap(icon_path)

canvas = tk.Canvas(master=win, bg='gray', width=600, height=400)
image_path = os.getcwd() + "\\resource\\flower.png"
login_image = ImageTk.PhotoImage(Image.open(image_path))
image = canvas.create_image(0,0,image=login_image,anchor='nw')
canvas.grid(row=0,column=0,columnspan=2,)

login_frame = ttk.LabelFrame(win, text=" 登录窗口 ")
login_frame.grid(row=1, column=0, columnspan=2, pady=20)


tk.Label(login_frame, text="PIN").grid(row=2,column=0, pady=50, padx=50, sticky="E")
entry_pin = tk.StringVar()
tk.Entry(login_frame, textvariable=entry_pin).grid(row=2, column=1, padx=10)

def adm_long():
    if entry_pin.get()=="990902":
        pass
    else:
        msg.showerror(title="密码错误", message="密码错误，请重新输入")

btn_login = tk.Button(login_frame, text='登录', command=adm_long, bg="gray")
btn_login.grid(row=3, column=0, columnspan=2, sticky="WE")

win.mainloop()