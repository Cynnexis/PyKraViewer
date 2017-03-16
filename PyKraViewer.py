#!/usr/bin/python3.5
# -*-coding:Utf-8 -*

import sys
import os
import zipfile
from Tkinter import *
from PIL import Image
from PIL import ImageTk

if len(sys.argv) == 0:
	print("Usage: ", sys.argv[0], " File")
	print("       File : KRA File (krita file)")
	sys.exit(0)

filename = str(sys.argv[1])

if filename.split('.')[-1] != "kra" and filename.split('.')[-1] != "zip":
	raise ImportError("Error: \"" + filename + "\" is not a krita file.")

if not zipfile.is_zipfile(filename):
	raise zipfile.BadZipFile("Error: \"" + filename + "\" is not a krita file.")

print("Reading \"", filename, "\" file...")
zf = zipfile.ZipFile(filename)
try:
	print("Decompressing \"preview.png\" from \"", filename, "\"...")
	data = zf.read("preview.png");
except KeyError:
	raise ImportError("Error: Could not decompressed \"preview.png\" from \"" + filename + "\". Is it a krita file?")

tmpname = "PyKraViewer_" + filename.replace(" ", "-") + "_preview.tmp.png"
print("Exporting \"preview.png\" into \"", tmpname,  "\"...")
tmp = open(tmpname, "wb")
tmp.write(data)
tmp.close()
del tmp

img = Image.open(tmpname)
tkimg = ImageTk.PhotoImage(img)

print("Displaying the image with Tkinter and PIL.Image...")
frame = Tk()
frame.title("PyKraViewer - " + filename)

l_filename = Label(frame, text=filename)
l_filename.pack()
l_thumbnail = Label(frame, image=tkimg)
l_thumbnail.pack()

frame.mainloop()

print("Removing \"", tmpname, "\"...")
os.remove(tmpname)
