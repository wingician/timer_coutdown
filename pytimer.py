import sys, time
from Tkinter import *
import tkMessageBox
curtime = 10
altime = time.time() + 1e8
run = False
setrun = False
msg = False
defaultMins = 50

def start(s = ''):
    global altime ,run ,curtime,msg,defaultMins
    
    if run :
        if curtime < 1:
            curtime = 10       
            run = False
            msg = False

    if not run:
        run = True
        but.config(background = "green")
        a = tt.get()
        try:
            mins = int(a)
        except:
            mins = defaultMins  # default: one-minute countdown
            #altime = 60 * mins + time.time()
        altime = mins * 60 + time.time()
        #altime = 4 + time.time()     ## for debug
        tt.config(justify = "right",state = "disabled")
        msg = True

def showtime():
    global altime ,curtime,run,msg,defaultMins
    curtime = max(0, int(altime - time.time()))
    if run:
        tt.config(state = "normal")
        tt.delete(0, END)
        tt.insert(0, "%u:%02u" % (curtime // 60, curtime % 60))
        if curtime < 30:
            but.config(background = "yellow")
        if curtime < 2:
            but.config(background = "red")
        tt.config(state="disabled")
    if curtime > 0:
        master.after(1000, showtime)
        master.wm_attributes('-topmost',0)
    else:
        master.wm_attributes('-topmost',1)
        tt.config(state = "normal")
        tt.delete(0, END)
        tt.insert(0, defaultMins)
        but.config(background = "green")
        if msg:
            tkMessageBox.showinfo('time up','have a rest!')
            msg = False
        master.after(50, showtime)
        run = False
        master.update()
        master.deiconify()

def stop(s = ''):
    global altime ,run ,curtime,msg,defMin,defaultMins
    if run :
        run = False
        curtime = 0
        tt.config(state = "normal")
        tt.delete(0, END)
        tt.insert(0, defaultMins)
        master.after(50, showtime)
        but.config(background = "green")
        msg = False
    
def hideframe(s = ''):
    master.withdraw()
    master.update()

def hidesetting(s = ''):
    global settingLable
    settingLable.update()
    settingLable.withdraw()

def setting(s = ''):
    global defaultMins ,setrun,defMin,settingLable
    settingLable = Tk()
    settingLable.geometry("200x60")
    f3 = Frame(settingLable)
    f4 = Frame(settingLable)
    f3.pack(side = TOP, fill = Y)
    f4.pack(side = TOP, fill = Y)
    setMsg = Label(f3,text='set default minutes:')
    setMsg.pack(side = LEFT)
    defMin = Entry(f3,width = 8)
    settingLable.title("setting")
    defMin.pack(side = RIGHT)
    defMin.delete(0, END)
    defMin.focus()
    defMin.insert(0, defaultMins)

    butclose = Button(f4, text = "  Close   ", command = hidesetting)
    butclose.pack(side = RIGHT)

    butset = Button(f4, text = "  OK   ", command = setdone)
    butset.pack(side = RIGHT)
    
def setdone(s = ''):
    global defaultMins,setrun ,defMin
    d = defMin.get()
    try:
        defaultMins = int(d)
    except:
        defaultMins = 50

master = Tk()
master.geometry("200x60")
f1 = Frame(master)
f1.pack(side = TOP, fill = Y)
f2 = Frame(master)
f2.pack(side = TOP, fill = Y)

#input& show time
tt = Entry(f2, width = 8)
tt.pack(side = RIGHT)
tt.delete(0, END)
tt.bind('<Return>', start)
tt.bind('<F2>', stop)
tt.bind('<F3>', hideframe)
tt.focus()

#button
but = Button(f1, text = "  Start  ", command = start)
but2 = Button(f1, text = "  Stop  ", command = stop)
but2.config(background = "red")
but3 = Button(f1, text = "  Hide  ", command = hideframe)
but.pack(side = LEFT)
but3.pack(side = RIGHT)
but2.pack(side = RIGHT)

#menu
menubar = Menu(master)
fmenu = Menu(menubar)
fmenu.add_command(label = 'Start<Enter>',command = start)
fmenu.add_command(label = 'Stop<F2>',command = stop)
fmenu.add_command(label = 'Hide<F3>',command = hideframe)

smenu = Menu(menubar)
smenu.add_command(label = 'setting',command = setting)
amenu = Menu(menubar)
for each in ['ver0.1','by scs']:
    amenu.add_command(label = each)

menubar.add_cascade(label = 'setting',menu = smenu)
menubar.add_cascade(label = 'shortcut',menu = fmenu)

menubar.add_cascade(label = 'about',menu = amenu)

master['menu'] = menubar
master.title("PyTimer")
master.after(1000, showtime)
mainloop()
