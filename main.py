#!/usr/bin/python

import tkinter
import os
import PyPDF2
from os import walk
from tkinter import filedialog
from tkinter import *
import re
import csv


def browse_button(T):
    mypath = filedialog.askdirectory()
    with open(os.path.join(mypath, 'salla.csv'), 'w') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_MINIMAL)
        for (dirpath, dirnames, filenames) in walk(mypath):
            for filename in filenames:
                name, file_extension = os.path.splitext(os.path.join(dirpath, filename))
                if file_extension == ".pdf":
                    T.insert(INSERT, name + "\n")
                    pdfFileObj = open(os.path.join(dirpath, filename),'rb')
                    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
                    page = pdfReader.getPage(0)

                    PUC = ""
                    try:
                        result = re.search('\(PUC\)(.*)Data', page.extractText())
                        PUC = result.group(1)
                    except Exception as e:
                        T.insert(INSERT,"Errore in lettura PUC\n")
                    VISIT = ""
                    try:
                        result = re.search('Data visita (.*)DATI DEL MEDICO', page.extractText())
                        VISIT = result.group(1)
                    except Exception as e:
                        T.insert(INSERT,"Errore in lettura VISITA\n")
                    IN = ""
                    try:
                        result = re.search('i essere ammalato dal(.*)Viene assegnata prognosi', page.extractText())
                        IN = result.group(1)
                    except Exception as e:
                        T.insert(INSERT,"Errore in lettura DATA IN\n")
                    OUT = ""
                    try:
                        result = re.search('clinica a tutto il(.*)Il lavoratore dichiara di aver comp', page.extractText())
                        OUT = result.group(1)
                    except Exception as e:
                        T.insert(INSERT,"Errore in lettura DATA OUT\n")
                    CF = ""
                    try:
                        result = re.search('C\.F\.(.*)Nato', page.extractText())
                        CF = result.group(1)
                    except Exception as e:
                        T.insert(INSERT,"Errore in lettura CF\n")
                    NOME = ""
                    COGNOME = ""
                    try:
                        result = re.search('Cognome e nome(.*)Opera', page.extractText())
                        NOME = result.group(1).split()[0]
                        COGNOME = result.group(1).split()[1]
                    except Exception as e:
                        T.insert(INSERT,"Errore in lettura NOME e COGNOME\n")
                    spamwriter.writerow([PUC,VISIT,IN,OUT,NOME,COGNOME,CF])

            
    return


root = Tk()
root.wm_iconbitmap('transparent.ico')
root.title("LAMT")

bottomframe = Frame(root)
bottomframe.pack( side = BOTTOM )

#v = StringVar()
#T = Text(root, width=40, height=10).grid(row=0, column=3)
#Button(text="Scegli cartella", command=lambda: browse_button(T)).grid(row=1, column=3)

T = Text(root)
T.insert(INSERT, "Benvenuto in LAMT\n")
T.insert(INSERT, "Benvenuto in Lettore multiplo di Attestati di Malattia Telematica\n")
ActionButton =Button(bottomframe, text="Scegli cartella", command=lambda: browse_button(T))
ActionButton.pack( side = BOTTOM)

T.pack()
root.mainloop()
