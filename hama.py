# Tk8.0 style top-level window menus

import sys



import os
from stat import *

import Tkinter


from Tkinter import *                              # get widget classes
from tkMessageBox import *                         # get standard dialogs
from tkFileDialog import askopenfilename	   # get standart dialogs
from tkSimpleDialog import askinteger
import string
import re
import Numeric
from Numeric import *
import Image, ImageTk, ImageFilter

from types import *
##############################################
#            GLOBAL names list:
##############################################

spectrumName='Model'	#%s
weight=0	#%x
FlagMWL=0
MWLparameter1=0
MWLparameter2=0
workingDir=''
PyDir=''
spectrumDir=''
spectrumDataDir=''
xwindowsize=0
ywindowsize=0

##############################################

MyDictionary = {
    'File name': askopenfilename,
    'k-weight' : lambda: askinteger('Entry', 'Enter weight'),
          'Fourier'  :'' }

fields = 'centrum1', 'centrum2', 'sigma1', 'sigma2', 'ampli1', 'ampli2', 'frequency1', 'frequency2', 'phase1', 'phase2'
Morletparameters = 'kappa', 'sigma'
Cauchyparameters = 'nResolution'
Rvalues = 'Rmin', 'Rmax', 'Raxis'
windowDictionary = {
            'SNW' : 'windowSNW',
            'FW'  : 'windowFW',
            'FTW' : 'windowFTW',
            'MFW' : 'windowMFW',
            'FMFW': 'windowFMFW',
            'MW'  : 'windowMW',
            'GW'  : 'windowGW'}
windowPlacementDictionary = {
            'SNW' :  str(xwindowsize/3)+'x'+str(ywindowsize/3)+'+'+str(xwindowsize/3)+'+'+str(ywindowsize/3)}
###########################################################

################Signaldone############Signaldone###########
def Signaldone():
    global MyDictionary
    global spectrumName, weight
    global FlagMWL, MWLparameter1, MWLparameter2
    global workingDir, PyDir, spectrumDataDir
    global root
                              
#    signalname=askopenfilename(),

                                
    class Signal(Frame):   
        def __init__(self, parent=None):
            Frame.__init__(self, parent)
            self.pack(side=LEFT)
            Label(self, text="Signal").pack(side=TOP)
            self.var = StringVar()
            for (key, value) in MyDictionary.items():
                Radiobutton(self, text=key, command=self.onPress, variable=self.var, value=key).pack(anchor=NW)
            return
      
        def onPress(self):
            global spectrumName, weight
            global root, parentWidget
            global workingDir, PyDir, spectrumDataDir, DirectoryName

            pick = self.var.get()
                     
            if pick == 'File name':
                spectrumName=MyDictionary[pick]()
                spectrumDir=os.path.dirname(spectrumName)
                os.chdir(spectrumDir)
                DirectoryName1=os.path.basename(spectrumName)
                DirectoryName2=os.path.splitext(spectrumName)[1]
                LenDirectoryName2=len(DirectoryName2)
                DirectoryName=DirectoryName1[:-LenDirectoryName2]
                                    

                ListDir=os.listdir(os.getcwd())
                LenListDir=len(ListDir)

                KeyDir=0
                for i in range(LenListDir):
                    if ListDir[i] == DirectoryName:
                        mode=os.stat(DirectoryName)[ST_MODE]
                        if mode & S_IFDIR:
                            KeyDir=1
                if KeyDir == 0:
                    os.mkdir( DirectoryName)
                                    
    #                         print DirectoryName
                spectrumDataDir=spectrumDir+os.altsep+DirectoryName
    #                         print spectrumDataDir
                                    
    #			drawPlot(spectrumName,"Initial spectrum")
                parentWidget=root
                Picture(spectrumName, "Initial spectrum", "k", "Chi",'SNW')
    
            elif pick == 'k-weight':
                weight=MyDictionary[pick]()
                SpectrumFunction=workingDir+os.altsep+'SpectrumFunction.txt'
                outputFile = open (SpectrumFunction, 'w')
                outputFile.write("%s\n" %(spectrumName))
                outputFile.write("%x" %(weight))
                outputFile.close()
                        
                os.chdir(workingDir)
                os.system("spectrum.exe")   
    #                         print 'spectrum.exe worked'                     
                Function=workingDir+os.altsep+'function.txt'
                Picture(Function, "Weighted spectrum", "k", "Chi*weigth", 'FW')

            elif pick == 'Fourier':
                os.chdir(workingDir)
                os.system("fourier.exe")
                Fourier=workingDir+os.altsep+'Fourier.txt'
                Picture(Fourier, "Fourier transform of the spectrum", "r", "Fourier", 'FTW') 
                      
                              
    Signal().mainloop()
###################Signaldone########end##########Signaldone#####################
###################Modeldone#########start########Modeldone######################
def Modeldone():
    global fields
    global spectrumName, weight
    global workingDir, PyDir, spectrumDataDir, DirectoryName

    spectrumName='Model'
    weight=0
                    
    def fetch(entries,root1):
                    
        outputFile = open ('ModelFunction.txt', 'w')
        for entry in entries:
            printValue=float(entry.get())
            outputFile.write("%g\n" %(printValue))
        outputFile.close()
        root1.destroy()

                    
        DirectoryName="Model"
        ListDir=os.listdir(os.getcwd())
        LenListDir=len(ListDir)
        KeyDir=0
        for i in range(LenListDir):
            if ListDir[i] == DirectoryName:
                mode=os.stat(DirectoryName)[ST_MODE]
                if mode & S_IFDIR:
                    KeyDir=1
                if KeyDir == 0:
                    os.mkdir( DirectoryName)    
#                   print DirectoryName   
                spectrumDataDir=workingDir+os.altsep+DirectoryName  
#                   print spectrumDataDir       

        os.chdir(workingDir)
        os.system("model.exe")
        Function=workingDir+os.altsep+'function.txt'
        Picture(Function, "Model function", "k", "Chi", 'MFW')
#		    drawPlot('function.txt',"Model Function")
        
        os.chdir(workingDir)
        os.system("fourier.exe")
        Fourier=workingDir+os.altsep+'Fourier.txt'
        Picture(Fourier, "Fourier transform of the spectrum", "r", "Fourier",'FMFW')
                    
        return

    def makeform(root1, fields):
           
        entries = []
        for field in fields:
            row = Frame(root1)	#make a new row
            lab = Label(row, width=10, text=field)      # add to columns
            ent=Entry(row)
            row.pack(side=TOP, fill=X)
            lab.pack(side=LEFT)
            ent.pack(side=RIGHT, expand=YES, fill=X)  
            entries.append(ent)
        return entries
    
    root1=Tk()
                                              
    root1.title('Model Parameters')   
    vars = makeform(root1, fields)

    Button(root1, text='Accept',
                         command=(lambda v=vars: fetch(v,root1))).pack(side=LEFT)
        
    root1.bind('<Return>', (lambda event, v=vars: fetch(v,root1)))
    root1.mainloop()

###################Modeldone#########end########Modeldone######################
###################Morletdone#######start#######Morletdone#####################
def Morletdone():
    global Morletparameters
    global FlagMWL, MWLparameter1, MWLparameter2
    global workingDir
    FlagMWL=1 
    
    def fetchM(entries, root2):
        global MWLparameter1, MWLparameter2
        global workingDir
                      
        os.chdir(workingDir)
        outputFile = open ('Motherparam.txt', 'w')
        i=1
        for entry in entries:
#       	 	  print 'Input => "%s"' % entry.get()      # get text
            printValue=float(entry.get())
            outputFile.write("%g\n" %(printValue))
          
            if i ==1:
                MWLparameter1=printValue
            else:
                MWLparameter2=printValue
            i=i+1 
             
            outputFile.write("%g\n" %(0))
        outputFile.close()
        root2.destroy()

        os.system("morlet.exe")
        Morlet=workingDir+os.altsep+'mother.txt'
        Picture(Morlet, "Morlet wavelet", "r", "Morlet",'MW')
                              
        return

    def makeform(root2, Morletparameters):
           
        entries = []
        for Morletparameter in Morletparameters:
            row = Frame(root2)	#make a new row
            lab = Label(row, width=10, text=Morletparameter)      # add to columns
            ent=Entry(row)
            row.pack(side=TOP, fill=X)
            lab.pack(side=LEFT)
            ent.pack(side=RIGHT, expand=YES, fill=X)  
            entries.append(ent)
        return entries
    
    root2=Tk()
    root2.title('Morlet Parameters')   
    vars = makeform(root2, Morletparameters)

    Button(root2, text='Accept',
                        command=(lambda v=vars: fetchM(v, root2))).pack(side=LEFT)
    root2.bind('<Return>', (lambda event, v=vars: fetchM(v,root2)))

    root2.mainloop()
###################Morletdone########end########Morletdone#####################
###################Cauchydone#######start#######Cauchydone#####################
def Cauchydone():
    global Cauchyparameters
    global FlagMWL, MWLparameter1, MWLparameter2
    global workingDir
    FlagMWL=2 
        
    def fetchC(entries, root3):
        global MWLparameter1, MWLparameter2
        global workingDir

        os.chdir(workingDir)
        outputFile = open ('Motherparam.txt', 'w')
        outputFile.write("%g\n" %(0))
        outputFile.write("%g\n" %(0))
        i=1
        for entry in entries:
            printValue=float(entry.get())
            outputFile.write("%g\n" %(printValue))
            if i ==1:
                MWLparameter1=printValue
            else:
                MWLparameter2=printValue
            i=i+1

        outputFile.close()
        root3.destroy()

                    
        os.system("cauchy.exe")
        Cauchy=workingDir+os.altsep+'mother.txt'
        Picture(Cauchy, "Cauchy wavelet", "r", "Cauchy", 'GW')
        return

    def makeform(root3, Cauchyparameters):
        
        entries = []
        row = Frame(root3)	#make a new row
        lab = Label(row, width=10, text=Cauchyparameters)      # add to columns
        ent=Entry(row)
        row.pack(side=TOP, fill=X)
        lab.pack(side=LEFT)
        ent.pack(side=RIGHT, expand=YES, fill=X)  
        entries.append(ent)
        return entries
    
    root3=Tk()
    root3.title('Cauchy Parameters')   
    vars = makeform(root3, Cauchyparameters)

    Button(root3, text='Accept',
                    command=(lambda v=vars: fetchC(v, root3))).pack(side=LEFT)
    root3.bind('<Return>', (lambda event, v=vars: fetchC(v,root3)))

    root3.mainloop()
###################Cauchydone########end########Cauchydone#####################
def notdone():  
    showerror('Not implemented', 'Not yet available')

################################################################################
def drawPlot(spectrumName, text):
    global xx,yy
 
    iFilefirst = open(spectrumName, "r")

    datafirst=iFilefirst.read() 
    splfirst=re.split("\n",datafirst)
    Npfirst=len(splfirst)-1
    iFilefirst.close()

    iFile = open(spectrumName, "r")

    X=[]
    Y=[]
    for j in range(Npfirst):

        datas=iFile.readline()          
        datasrem=datas.strip()
        spl=re.split("\s",datasrem)
        Np=len(spl)
    
        sFlo=[0,0]
        k=0
        for i in range(Np):
            if spl[i] !='':
                sFlo[k]=string.atof(spl[i])

                k=+1
        X.append(sFlo[0])
        Y.append(sFlo[1])

    iFile.close()

    xx=Numeric.array(X, typecode=Float)
    yy=Numeric.array(Y, typecode=Float)

    g = Gnuplot.Gnuplot(debug=1)
    d = Gnuplot.Data(xx, yy,
                        text, "lines")
  
 
    g.title(text)
    g.xlabel('k')
    g.ylabel('Chi')

    g.plot(d)


    raw_input('Please press Enter to continue...\n')
        

###############################################################################
def WLDrawdone():
    cColor=Button(root, text='Color image', command=keyModeCI).pack(side=LEFT) 
    cColor=Button(root, text='Black&White image', command=keyModeBW).pack(side=LEFT) 
 

def keyModeCI():
    global keyMode
    keyMode=0
    WLDrawdoneColor()

def keyModeBW():
    global keyMode
    keyMode=1
    WLDrawdoneColor()

def WLDrawdoneColor():
    global root, c, msg
    global xwindowsize, ywindowsize
    global nwb, nwc2, nhb, nhc2
    global nx, ny, kmin1, kmax1, rmin1, rmax1
    global c2, xxBW, rx,ry, img1
    global keyMode
 
    FileParam = open('parameters.txt', "r")
    for j in range(21):
        Param=FileParam.readline()
        Paramrem=Param.strip()
        Par=re.split("\s",Paramrem)

    if j == 14:
        nx = string.atoi(Par[-1])
    if j == 15:
        ny = string.atoi(Par[-1])
    if j == 17:
        kmin1 = string.atof(Par[-1])
    if j == 18:
        kmax1 = string.atof(Par[-1])
    if j == 19:
        rmin1 = string.atof(Par[-1])
    if j == 20:
        rmax1 = string.atof(Par[-1])
    FileParam.close()


    iFilefirst = open('OutputFile', "r")

    datafirst=iFilefirst.read() 
    splfirst=re.split("\n",datafirst)
    Npfirst=len(splfirst)-1
    iFilefirst.close()
    iFile = open('OutputFile', "r") 

    X=[]

    for j in range(Npfirst):
        datas=iFile.readline()      
        spl=datas.strip()
        sFlo=[0]
        sFlo[0]=string.atof(spl)
        X.append(sFlo[0])
    iFile.close()

    xx=Numeric.array(X, typecode=Float)

# Y=xx
# print type(Y)

# for j in range (Npfirst):
#  Y[Npfirst-j]=xx[j]

# xx=Y

    xmin=min(xx)
    xmax=max(xx)
    xxBW=xx
    delx=xmax-xmin
    xstep=255/delx
 
    for j in range(Npfirst):
        xxBW[j]=(xx[j]-xmin)*xstep


    nwc2=1*xwindowsize/3
    nhc2=1*ywindowsize/3
    nwb=20
    nhb=20
    img=ImageColorBW(nx,1,nx,1,ny,nx-1,ny-1,xxBW,keyMode)
    img.rotate(180).filter(ImageFilter.DETAIL).save("OutputFile.jpg","JPEG")
    
    c2 = Canvas(width=nwc2+2*nwb, height=nhc2+2*nhb,bg="white")
    c2.pack(side=TOP) 

# img1=ImageTk.PhotoImage(img.rotate(180).resize((nwc2,nhc2),Image.BICUBIC).filter(ImageFilter.SHARPEN))

    img1=ImageTk.PhotoImage(img.rotate(180).resize((nwc2,nhc2),Image.BICUBIC).filter(ImageFilter.DETAIL))
    #  img1=ImageTk.PhotoImage(img.rotate(180).resize((nwc2,nhc2),Image.BICUBIC).filter(ImageFilter.CONTOUR))
    c2.create_image(1.5*nwb,nhb,image=img1,anchor='nw')

    axistitles(c2, 1.5*nwb, nhb, 1.5*nwb, nwc2+1.5*nwb,nhb, nhc2+nhb, kmin1, kmax1, rmin1, rmax1, "k", "WL transform")
    
    c2.bind("<ButtonPress>", give_info)
    b2=Label(root,background="beige", text="Mouse cliking on the image to start zoom ").pack()
    c2.mainloop()

def ImageColorBW(nx,nx1,nx2,ny1,ny2,nix,niy,xxBW1,keyMode1):
    yy=0
    XYString=''
    strX=''
    if keyMode1 == 1:    
        for j in range (ny1,ny2):
            for i in range (nx1,nx2):
                if 195 <= xxBW[(j-1)*nx+i]  <=200:
                    yy=255
                    strX=chr(yy)
                    XYString = XYString + strX
                else:
                    yy=xxBW[(j-1)*nx+i]
                    strX=chr(yy)
                    XYString = XYString + strX
        mode = "L" 
    else: ####################################################
        XXYYString=''
        for j in range (ny1,ny2):
            for i in range (nx1,nx2):
                if 195 <= xxBW[(j-1)*nx+i]  <=200:
                    yy=chr(0)
                    XXYYString=XXYYString + yy
                    yy=255
                    yy=chr(yy)	
                    XXYYString=XXYYString + yy
                    yy=chr(0)
                    XXYYString=XXYYString + yy
                else:  
                    yy=chr(0)
                    XXYYString=XXYYString + yy
                    XXYYString=XXYYString + yy
                    yy=xxBW[(j-1)*nx+i]
                    yy=chr(yy)	
                    XXYYString=XXYYString + yy
        mode = "RGB"
        XYString=XXYYString 
#  print nx2,ny2,nix,niy
    img=Image.fromstring(mode,(nix,niy),XYString)
    return img
################################end WL Image draw#####################################
def give_info(event):
    global xinfo, yinfo
    global nwb, nwc2, nhb, nhc2
    global nx, ny, kmin1, kmax1, rmin1, rmax1
    global idcc3, xxBW, rx, ry, img1
 
 
    xx=event.x
    yy=event.y
 
    zoomimage(xx,yy) 

def zoomimage(xx,yy):
    global nwb, nwc2, nhb, nhc2
    global nx, ny, kmin1, kmax1, rmin1, rmax1
    global xxBW, idcc3, cc3
    global keyMode
    str1=str(root.winfo_children())
    str2=string.count(str1, "Tkinter.Canvas")
    if str2 == 2:
        cc3.destroy()
 
    cc3 = Canvas(width=nwc2+2*nwb, height=nhc2+2*nhb,bg="white")
    cc3.pack(side=TOP)


    imymax=nhb+nhc2
    imymin=nhb
    imxmin=1.5*nwb
    imxmax=1.5*nwb+nwc2

    jy=int(ny*(imymax-yy)/nhc2) 
    jx=int(nx*(xx-imxmin)/nwc2)
    
    yy=0
    XYString=''
    strX=''
    nny=int(ny/10)
    rdel=(rmax1-rmin1)/(ny-1)
    rmin1nny=rmin1+(jy-nny)*rdel
    rmax1nny=rmin1+(jy+nny)*rdel
    nnx=int(nx/10)
    kdel=(kmax1-kmin1)/(nx-1)
    kmin1nnx=kmin1+(jx-nnx)*kdel
    kmax1nnx=kmin1+(jx+nnx)*kdel

    imgevent=ImageColorBW(nx,jx-nnx,jx+nnx,jy-nny,jy+nny, 2*nnx,2*nny,xxBW,keyMode)

    img1event=ImageTk.PhotoImage(imgevent.rotate(180).resize((nwc2,nhc2),Image.BICUBIC).filter(ImageFilter.SHARPEN))
    cc3.create_image(1.5*nwb,nhb,image=img1event,anchor='nw')

    axistitles(cc3,nwb , nhb, imxmin, imxmax, imymin, imymax, 
                    kmin1nnx, kmax1nnx, rmin1nny, rmax1nny, "k", "WL zoom" )
 
    cc3.mainloop()
######################################################################################
     
def axistitles(cc2,nw_border ,nh_border , xwinmin, xwinmax, ywinmin, ywinmax, 
                    xmin, xmax, ymin, ymax, paramx, param1):


    cc2.create_line(xwinmin,ywinmax,xwinmax,ywinmax,fill="red", width=2, arrow="last")
    cc2.create_line(xwinmin,ywinmin,xwinmin,ywinmax, fill="red", width=2, arrow="first")
    cc2.create_line(xwinmin,ywinmin,xwinmax,ywinmin,fill="green")
    cc2.create_line(xwinmax,ywinmin,xwinmax,ywinmax, fill="blue")

    nyy=7  
    
    stepgridyy=(ywinmin-ywinmax)/(nyy-1)
    stepgridxx=(xwinmax-xwinmin)/(nyy-1)
    iy=1
    strY=''
    stepy=(ymax-ymin)/(nyy-1)
    oyy=ywinmax
    while oyy > ywinmin - stepgridyy:   
        oyy = oyy + stepgridyy
        cc2.create_line(xwinmin,oyy,xwinmax,oyy, fill="green")
        strY=ymin+iy*stepy
        strstrY=str(strY)
        cc2.create_text(xwinmin-nw_border/4,oyy, text=strstrY[0:4], anchor=NE)
        iy=iy+1

    oxx=xwinmin
    ix=0
    strX=''
    stepx=(xmax-xmin)/(nyy-1)
    while oxx < xwinmax - stepgridxx:   
        oxx = oxx + stepgridxx
        cc2.create_line(oxx,ywinmin,oxx,ywinmax, fill="blue")
        strX=xmin+ix*stepx
        strstrX=str(strX)
        cc2.create_text(oxx-stepgridxx,ywinmax+3, text=strstrX[0:4], anchor=NW)
        ix=ix+1
     
    strX=xmin+ix*stepx
    strstrX=str(strX)
    cc2.create_text(oxx,ywinmax+3, text=strstrX[0:4], anchor=NW)
    cc2.create_text(xwinmax,ywinmax+3, text=paramx, anchor=NW)    
    cc2.create_text((xwinmax),ywinmin,text=param1,anchor=SE, fill="red")

##############################start R values, WL calculation ################################# 
def Rparameters():
    global spectrumName, weight
    global FlagMWL, MWLparameter1, MWLparameter2
    global Rvalues, root4
 
    def WriteParameters(Rmin,Rmax,Raxis):
        global spectrumName, weight
        global FlagMWL, MWLparameter1, MWLparameter2
        global root4

        OutputFile='OutputFile'
        paramFile = open('inpParam.txt', 'w')
        paramFile.write("%s\n" %(OutputFile))
        paramFile.write("%s\n" %(spectrumName))
        paramFile.write("%i\n" %(weight))
        paramFile.write("%f\n" %(Rmin))
        paramFile.write("%f\n" %(Rmax))
        paramFile.write("%i\n" %(Raxis))
        paramFile.write("%i\n" %(FlagMWL))
        paramFile.write("%i\n" %(MWLparameter1))
        paramFile.write("%i\n" %(MWLparameter2))
        paramFile.close()
        root4.destroy()
 
    def fetchD(entries):
        global Rmin, Rmax, Raxis
        i=1
        for entry in entries:
            printValue=float(entry.get())
            if i ==1:
                Rmin = printValue
            if i ==2:
                Rmax = printValue
            if i== 3:
                Raxis = printValue
            i=i+1
        Raxis=int(Raxis) 
        WriteParameters(Rmin,Rmax,Raxis)
        return

    def makeform(root4, Rvalues):
        entries = []

        for Rvalue in Rvalues:
            row = Frame(root4)	#make a new row
            lab = Label(row, width=10, text=Rvalue)      # add to columns
            ent=Entry(row)
            row.pack(side=TOP, fill=X)
            lab.pack(side=LEFT)
            ent.pack(side=RIGHT, expand=YES, fill=X)  
            entries.append(ent)
        return entries
    

    root4=Tk()
    root4.title('R - Parameters')  

    vars = makeform(root4, Rvalues)
    Button(root4, text='Accept',
    command=(lambda v=vars: fetchD(v))).pack(side=LEFT)
    root4.mainloop()

###############################end  R values, WL calculation ################################# 
def WLdone(): 
    global workingDir, root
    global DirectoryName, spectrumDataDir, MWLparameter1, MWLparameter2
    import shutil
    
    os.system("WL.exe")
    
    iMWLparameter1=int(MWLparameter1)
    iMWLparameter2=int(MWLparameter2) 

    sMWLparameter1=str(iMWLparameter1)
    sMWLparameter2=str(iMWLparameter2)

    FileName="WL_"+DirectoryName+"_"+sMWLparameter1+"_"+sMWLparameter2+".txt"
    #  print FileName

    OutFileNAme=spectrumDataDir+os.altsep+FileName

    ParamName="Param_"+DirectoryName+"_"+sMWLparameter1+"_"+sMWLparameter2+".txt"


    OutParamNAme=spectrumDataDir+os.altsep+ParamName
    #  print OutParamNAme

    shutil.copy("OutputFile",OutFileNAme)
    shutil.copy("parameters.txt",OutParamNAme)
    return

##########################################start makemenu######################################

def makemenu():   
    global root
    

    top = Menu(root)                                # win=top-level window
    root.config(menu=top)                           # set its menu option
    
    column1 = Menu(top, tearoff=0)
    top.add_cascade(label='File', menu=column1,underline=0)
    column1.add_command(label='Signal',  command=Signaldone,  underline=0) 
    column1.add_separator()
    column1.add_command(label='Model', command=Modeldone,  underline=0)

    column2 = Menu(top, tearoff=0)
    column2.add_command(label='Morlet',     command=Morletdone,  underline=0)
    column2.add_separator()
#    column2.add_command(label='Cauchy',   command=Cauchydone,  underline=0)
    column2.add_separator()
    top.add_cascade(label='Mother Wavelet',     menu=column2,        underline=0)

    column3 = Menu(top, tearoff=0)
    column3.add_command(label='R-parameters',  command=Rparameters,  underline=0) 
    column3.add_separator()
    column3.add_command(label='WL calculation', command=WLdone, underline=0) 
    column3.add_separator()
    column3.add_command(label='WL draw', command=WLDrawdone,  underline=0)
    top.add_cascade(label='WL_calculations',     menu=column3,        underline=0)

    
    top.add_command(label='Quit', command=quitProgram)    
##########################################end makemenu######################################
def quitProgram():
    global windowDictionary
    
    root.destroy()
    windowDictionary['SNW']
    if type(windowDictionary['SNW']) != StringType:
        windowDictionary['SNW'].destroy()
    if type(windowDictionary['FW']) != StringType:
        windowDictionary['FW'].destroy()
    if type(windowDictionary['FTW']) != StringType:
        windowDictionary['FTW'].destroy()
    if type(windowDictionary['MFW']) != StringType:
        windowDictionary['MFW'].destroy()
    if type(windowDictionary['FMFW']) != StringType:
        windowDictionary['FMFW'].destroy()
    if type(windowDictionary['MW']) != StringType:
        windowDictionary['MW'].destroy()
    if type(windowDictionary['GW']) != StringType:
        windowDictionary['GW'].destroy()

############################################################################################
def Picture(spectrumName, param1, paramx, paramy, keyRoot): 
    global xx,yy
    global xwindowsize, ywindowsize
    global root, c, windowDictionary, windowPlacementDictionary
    
    iFilefirst = open(spectrumName, "r")

    datafirst=iFilefirst.read() 
    splfirst=re.split("\n",datafirst)
    Npfirst=len(splfirst)-1
    iFilefirst.close()

    iFile = open(spectrumName, "r")

    X=[]
    Y=[]
    for j in range(Npfirst):

        datas=iFile.readline()          
        datasrem=datas.strip()
        spl=re.split("\s",datasrem)
        Np=len(spl)
        
        sFlo=[0,0]
        k=0
        for i in range(Np):
            if spl[i] !='':
                sFlo[k]=string.atof(spl[i])

                k=+1
        X.append(sFlo[0])
        Y.append(sFlo[1])

    iFile.close()

    xx=Numeric.array(X, typecode=Float)
    yy=Numeric.array(Y, typecode=Float)

    nw=xwindowsize/3
    nh=ywindowsize/3
    nwstr=str(nw)
    nhstr=str(nh)
    nh0=str(0)
    
    if keyRoot == 'SNW':    
        geoWin=nwstr+'x'+nhstr+'+'+nwstr+'+'+nh0  
    if keyRoot == 'MFW':    
        geoWin=nwstr+'x'+nhstr+'+'+nwstr+'+'+nh0  
    if keyRoot == 'FW':  
        nwstr1=str(2*nw)
        geoWin=nwstr+'x'+nhstr+'+'+nwstr1+'+'+nh0  
    if keyRoot == 'FMFW':  
        nwstr1=str(2*nw)      
        geoWin=nwstr+'x'+nhstr+'+'+nwstr1+'+'+nh0 
    if keyRoot == 'FTW':     
        geoWin=nwstr+'x'+nhstr+'+'+nwstr+'+'+nhstr
    if keyRoot == 'MW': 
        nwstr1=str(2*nw)
        geoWin=nwstr+'x'+nhstr+'+'+nwstr1+'+'+nhstr
    if keyRoot == 'GW': 
        nwstr1=str(2*nw)
        geoWin=nwstr+'x'+nhstr+'+'+nwstr1+'+'+nhstr


    windowDictionary[keyRoot]=Tk()
    windowDictionary[keyRoot].geometry(geoWin)
    windowDictionary[keyRoot].title(param1) 

    c=Canvas(windowDictionary[keyRoot],bg="White",width=nw,height=nh)
    c.config(relief=RAISED, highlightthickness=5 )
    c.pack()

    
    nw_border=nw/15
    nh_border=nh/10
    
    lenx=len(xx)
    xmax=max(xx)
    xmin=min(xx)
    ymax=max(yy)
    ymin=min(yy)
    xwinmin=2*nw_border
    xwinmax=nw-nw_border/2
    ywinmin=nh_border
    ywinmax=nh-nh_border

    x_ratio=(xwinmax-xwinmin)/(xmax-xmin)

    y_ratio=(ywinmin-ywinmax)/(ymax-ymin)
    
    line=[]
    for i in range(0,lenx-1):
        xw=xwinmin+(xx[i]-xmin)*x_ratio
        yw=ywinmax+(yy[i]-ymin)*y_ratio
        line.extend([xw,yw])
    c.create_line(line, fill="red", width=2)
    oy=ywinmin-ymin*y_ratio

    axistitles(c, nw_border, nh_border, xwinmin, xwinmax, 
               ywinmin, ywinmax, xmin, xmax, ymin, ymax, paramx, param1)

    windowDictionary[keyRoot].mainloop()
    
############################################################################################
############################################################################################

if __name__ == '__main__':

    workingDir=os.getcwd()
    
    PyDir=sys.path[5]

    os.chdir(PyDir)
 
 
    root=Tk()
    xwindowsize=root.winfo_screenwidth()
    ywindowsize=root.winfo_screenheight()
# root.geometry('200x160+20+20')
# root.resizable()
    root.title('Wavelet Transform Calculation')                             # set window-mgr info
 
    makemenu()                                     # associate a menu bar
    msg = Label(root, text='Wavelet Transform Calculation ') 

    msg.pack(expand=YES, fill=BOTH)
    msg.config(relief=SUNKEN, width=50, height=2, bg='beige')
    root.mainloop()

