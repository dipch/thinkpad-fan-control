#!/usr/bin/python3
import tkinter as tk
import subprocess
import shlex
from tkinter import *


def set_speed(speed=None):
    """Set fan speed level at /proc/acpi/ibm/fan. speed: 0-7, auto, disengaged, full-speed"""
    safe = shlex.quote(str(speed))
    return subprocess.check_output(
        f'echo level {safe} | sudo tee "/proc/acpi/ibm/fan"',
        shell=True
    ).decode()


def get_info():
    info_lines = subprocess.check_output("sensors").decode("utf-8").split("\n")
    result = []
    core_count = 0
    fan_count = 0
    for line in info_lines:
        if "Core" in line:
            result.append("Core %d: " % core_count + line.split(":")[-1].split("(")[0].strip())
            core_count += 1
        if "fan" in line:
            result.append("Fan %d: " % fan_count + line.split(":")[-1].split("(")[0].strip())
            fan_count += 1
    return result


def get_level():
    with open('/proc/acpi/ibm/fan', 'r') as f:
        lines = f.read().split("\n")
    return ["Level : " + line.split(":")[-1].strip() for line in lines if "level:" in line]


is_on = True


class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.parent.minsize(width=100, height=100)
        self.configure(background="black", width=10, height=10)

        level_label = tk.Label(parent, text="", bg='black', fg='white',
                               pady=0, highlightthickness=0, borderwidth=0)
        level_label.grid(row=2, column=0, pady=(0, 10))

        main_label = tk.Label(parent, text="", bg='black', fg='white')
        main_label.grid(row=1, column=0)

        btn_style = dict(highlightbackground="#6F7170", bg="#000000", fg="#FFFFFF",
                         highlightcolor="#6F7170", highlightthickness=1, bd=0,
                         activebackground="#e60012", activeforeground="white")

        row1 = tk.Frame()
        row1.grid()

        speed_buttons = []
        for i in range(8):
            btn = tk.Button(row1, text=str(i), **btn_style, command=lambda s=str(i): set_speed(s))
            btn.grid(row=0, column=i)
            speed_buttons.append(btn)

        row2 = tk.Frame()
        row2.grid()

        buttonA = tk.Button(row2, text="Auto", **btn_style, command=lambda: set_speed("auto"))
        buttonA.grid(row=0, column=1)

        buttonF = tk.Button(row2, text="Full", **btn_style, command=lambda: set_speed("full-speed"))
        buttonF.grid(row=0, column=2)

        row3 = tk.Frame()
        row3.grid(sticky=E)

        all_buttons = speed_buttons + [buttonA, buttonF]

        def button_mode():
            global is_on
            if is_on:
                new_bg, new_fg, img, btn_bg = 'white', 'black', off, "#FFFFFF"
                is_on = False
            else:
                new_bg, new_fg, img, btn_bg = 'black', 'white', on, "#000000"
                is_on = True

            on_.config(image=img, borderwidth=0, bg=btn_bg, activebackground=btn_bg)
            main_label.config(bg=new_bg, fg=new_fg)
            level_label.config(bg=new_bg, fg=new_fg)
            for btn in all_buttons:
                btn.config(bg=new_bg, fg=new_fg)
            self.config(bg=new_bg)
            self.master.configure(background=new_bg)

        on = PhotoImage(file="/opt/fancontrol/Resources/on.png")
        off = PhotoImage(file="/opt/fancontrol/Resources/off.png")

        on_ = Button(row3, image=on, bd=0, highlightthickness=0, borderwidth=0,
                     bg="#000000", activebackground="#000000", command=button_mode)
        on_.pack()

        def update_labels():
            try:
                main_label["text"] = "\n".join(get_info())
                level_label["text"] = "\n".join(get_level())
            except Exception:
                pass
            self.parent.after(500, update_labels)

        self.parent.after(500, update_labels)


if __name__ == "__main__":
    root = tk.Tk(className='ThinkFan Control')
    root.bind('<Control-q>', lambda e: root.destroy())
    root.configure(background='black')
    img = tk.Image("photo", file='/opt/fancontrol/Resources/icon.png')
    root.protocol('WM_DELETE_WINDOW', root.destroy)
    root.resizable(False, False)
    root.tk.call('wm', 'iconphoto', root._w, img)
    root.title("ThinkFan Control")
    MainApplication(root).grid()
    root.mainloop()
