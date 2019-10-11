import ffmpeg
from tkinter.filedialog import askopenfilename,askopenfilenames, askdirectory
import os
giffile = None
imageFolder = None
def importFile():
    imageFolder = askdirectory(title="Images' for the gif save location.")
    if (len(os.listdir(imageFolder)) > 0):
        return
    gifFile = askopenfilename(initialdir="~/",title="Open video file", filetypes=(("Gif files","*.gif"),("Gifv files","*.gifv"),("Video files","*.mp4"),("All Files","*.*")))
    print (gifFile)
    if not gifFile:
        return 
    
    (
        ffmpeg
        .input(gifFile)
        .output(imageFolder+'/images%04d.png')
        .run()
    )
def editFractalFile():
    imagesAnimate = askopenfilenames(initialdir=imageFolder,title="Select all the frames",filetypes=(("Images","*.png"),("All Files","*.*")))
    fractalFile = askopenfilename(initialdir="~/",title="Select the fractal settings file you want to add animated frames.",filetypes=(("Fractal file","*.fract"),("All Files","*.*")))
    print (fractalFile)
    if not fractalFile:
        return
    fractalInFileStream = open(fractalFile, 'r')
    fractalSettingObject = fractalInFileStream.readlines()
    fractalInFileStream.close()
    startFlag = False
    lineCount = 0
    currentImageNum = 0
    for i in range(len(fractalSettingObject)):
        linesSplit = fractalSettingObject[i].split(';')
        if linesSplit[0] == "[frames]\n" and not startFlag:
            print ("Start flag change",startFlag)
            startFlag = True
            continue
        if linesSplit[0] == "[keyframes]\n":
            print("Hit keyframe")
            print("Line number",i)
            break
        if startFlag:
            print (linesSplit)
            for line in linesSplit:
                line.rstrip('\n')
                if line == "main_mat1_file_color_texture":
                    print ("Breaking away")
                    break
                lineCount += 1
            startFlag =False
            print ("Linecount is",lineCount)
            continue
        if lineCount != 0:
            newline = ""
            for valindex in range(len(linesSplit)):
                if (valindex == lineCount):
                    if (valindex == len(linesSplit)-1):
                        newline += imagesAnimate[currentImageNum]
                    else:
                        newline += imagesAnimate[currentImageNum] + ';'
                    currentImageNum += 1
                    if (currentImageNum >= len(imagesAnimate)):
                        currentImageNum = 0
                    continue
                if (valindex == (len(linesSplit)-1)):
                    newline += linesSplit[valindex]
                else:
                    newline += linesSplit[valindex] +';'
            fractalSettingObject[i] = newline +'\n'
    print (len(fractalSettingObject))
    fractalOutFileStream = open(fractalFile,'w')
    fractalOutFileStream.writelines(fractalSettingObject)
    fractalOutFileStream.close()
    print("Fractal File is complete.")
def testFractalFile():
    fractalFile = askopenfilename(initialdir="~/",title="Select the fractal settings file you want to add animated frames.",filetypes=(("Fractal file","*.fract"),("All Files","*.*")))
    print (fractalFile)
    fractalFileStream = open(fractalFile)
    fractalSettingObject = fractalFileStream.readlines()
    for i in range(len(fractalSettingObject)):
        linesSplit = fractalSettingObject[i].split(';')
        print(linesSplit)
            
importFile()
editFractalFile()

