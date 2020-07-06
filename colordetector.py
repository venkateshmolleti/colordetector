import cv2
import numpy as np
import pandas as pd
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from PIL import ImageTk,Image
#from win32com.client import Dispatch
#s=Dispatch("SAPI.Spvoice")
import pyttsx3
s=pyttsx3.init()
w=Tk()
w.title("color detector")
w.iconbitmap("palicon.ico")

def chk():
    global img_path
    filename=filedialog.askopenfilename(initialdir="F:\venpro",title="select file",filetypes=(("jpg files","*.jpg"),("all files","*.*")))
    img_path = filename
    p = ttk.Progressbar(w, orient="horizontal", length=400, maximum=100, mode="determinate")
    p.pack()

    L = Label(w, text="uploading image...")
    L.pack()

    def fun():
        import time
        p['value'] = 10
        w.update_idletasks()
        time.sleep(1)
        p['value'] = 20
        w.update_idletasks()
        time.sleep(1)
        p['value'] = 30
        w.update_idletasks()
        time.sleep(1)
        p['value'] = 50
        w.update_idletasks()
        time.sleep(1)
        p['value'] = 70
        w.update_idletasks()
        time.sleep(1)
        p['value'] = 100
    p.pack(pady=10)
    fun()
    L.config(text="image uploaded.")


bt=Button(w,text="upload image.",command=chk,borderwidth=10,padx=360,pady=20,fg="blue").pack()
myi=ImageTk.PhotoImage(Image.open("bg1.jpg"))

myl=Label(image=myi).pack()
btt=Button(w,text="detect colors",command=w.destroy,borderwidth=10,padx=360,pady=20,fg="green").pack()


w.mainloop()
img = cv2.imread(img_path)

clicked = False
r = g = b = xpos = ypos = 0
index=["color","color_name","hex","R","G","B"]
csv = pd.read_csv('colors.csv', names=index, header=None)
def getColorName(R,G,B):
    minimum = 10000
    for i in range(len(csv)):
        d = abs(R- int(csv.loc[i,"R"])) + abs(G- int(csv.loc[i,"G"]))+ abs(B- int(csv.loc[i,"B"]))
        if(d<=minimum):
            minimum = d
            cname = csv.loc[i,"color_name"]
    return cname

def draw_function(event, x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b,g,r,xpos,ypos, clicked
        clicked = True
        xpos = x
        ypos = y
        b,g,r = img[y,x]
        b = int(b)
        g = int(g)
        r = int(r)

cv2.namedWindow('image')
cv2.setMouseCallback('image',draw_function)

while(1):

    cv2.imshow("image",img)
    if (clicked):
        cv2.rectangle(img,(20,20), (500,60), (b,g,r), -1)
        text = getColorName(r,g,b)
        s.say(text)
        s.runAndWait()
        cv2.putText(img, text,(50,50),2,0.8,(255,255,255),2,cv2.LINE_AA)
        if(r+g+b>=600):
            cv2.putText(img, text,(50,50),2,0.8,(0,0,0),2,cv2.LINE_AA)
        
        
        clicked=False
    if cv2.waitKey(20) & 0xFF ==ord("q"):
        break

cv2.destroyAllWindows()
