"""
Snipp - A simple snippingtool made by AsinusGrandus

Name: Snipp
Version: 1.0.0
Last update: November 7, 2021

Author: AsinusGrandus
"""

__version__ = "1.0.0"

import win32clipboard as clip
from io import BytesIO
from tkinter import *
from PIL import ImageTk, ImageDraw, Image
import pyautogui
import win32con
import base64
import json
import time
import io

root=Tk()
root.title(f"Snipp - {__version__}")

#Get assets from assets.json
def getAsset(assetName):
    with open("assets.json", "r") as file:
        assetDict = json.load(file)
    IMAGE_DATA = assetDict[assetName].encode("utf-8")
    f = base64.b64decode(IMAGE_DATA)
    return Image.open(io.BytesIO(f))

#Resize the image
def resizeImage(image):
    newHeight = 200
    height_percent = (newHeight / float(image.size[1]))
    width_size = int((float(image.size[0]) * float(height_percent)))

    #Returning the resized image
    return ImageTk.PhotoImage(image.resize((width_size, newHeight)))

appImage = resizeImage(getAsset("startScreen"))
imageLabel = Label(root, image=appImage)
imageLabel.image = appImage
imageLabel.grid(row=1, column=1)

#Selected values can't be negative, so they are negatively defined to check if they are valid later
postitions = {
    "left": -1,
    "top": -1,
    "right": -1,
    "bottom": -1
}

#Function to copy the screenshot to the clipboard: https://clay-atlas.com/us/blog/2020/10/30/python-en-pillow-screenshot-copy-clipboard/
def copyClipboard(image):
    output = BytesIO()
    image.convert('RGB').save(output, 'BMP')
    data = output.getvalue()[14:]
    output.close()
    clip.OpenClipboard()
    clip.EmptyClipboard()
    clip.SetClipboardData(win32con.CF_DIB, data)
    clip.CloseClipboard()

#Runs when a key is pressed
def key_pressed(event):
    #Get the dictionary with all positions
    global postitions

    #If the character is ctrl, set postion left and top
    if event.keysym == 'Control_L':
        postitions["left"], postitions["top"] = pyautogui.position()

    #If the character is ctrl, set postion left and top
    elif event.keysym == 'Alt_L':
        postitions["right"], postitions["bottom"] = pyautogui.position()

    #If the character is shift, make the screenshot with the postions from the dictionary, if they are valid
    elif event.keysym == 'Tab':
        #Check if positions are valid
        if all(x >= 0 for x in list(postitions.values())):
            #Set width and heigth
            width =  postitions["right"] - postitions["left"]
            heigth =  postitions["bottom"] - postitions["top"]
            #Check if the width and highth are real (not lower then 0)
            if width > 0 and heigth > 0:
                #Take the screenshot
                img = pyautogui.screenshot(region=(postitions["left"] , postitions["top"], width, heigth))
                filename = f"{round(time.time())}.png"
                img.save(filename)
                copyClipboard(img)

    #Get the image ready to show
    screen = pyautogui.screenshot()

    #If there is a valid lefttop point, draw it
    if postitions["left"] > 0 and postitions["top"] > 0:
        ImageDraw.Draw(screen).ellipse((postitions["left"]-15, postitions["top"]-15, postitions["left"]+15, postitions["top"]+15), fill = 'red', outline ='red')

    #If there is a valid rightbottom point, draw it
    if postitions["right"] > 0 and postitions["bottom"] > 0:
        ImageDraw.Draw(screen).ellipse((postitions["right"]-15, postitions["bottom"]-15, postitions["right"]+15, postitions["bottom"]+15), fill = 'red', outline ='red')

    #Put label on the screen
    appImage = resizeImage(screen)
    imageLabel = Label(root, image=appImage)
    imageLabel.image = appImage
    imageLabel.grid(row=1, column=1)

#Binds the keys to their function
root.bind("<Control_L>", key_pressed)
root.bind("<Alt_L>", key_pressed)
root.bind("<Tab>", key_pressed)

root.mainloop()