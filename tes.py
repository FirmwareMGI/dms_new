# import RPi.GPIO as GPIO
# 
# GPIO.setwarnings(False)
# GPIO.setmode(GPIO.BCM)
# 
# GPIO.setup(17,GPIO.OUT)
# GPIO.setup(27,GPIO.OUT)
# # GPIO.setwarnings(False)
# 
# 
# GPIO.output(17,1)
# GPIO.output(27,1)

#tes = [0,1]
#
#
#for i in range(0,2):
#    tes.pop(i)
#    print(tes)

fileNameAsal = 'COMTRADE/D81_RCD_01758_20231219_132443_989.cfg'

rootDir = "/home/pi/Desktop/DMSv1.2/IEC61850/DR_FILES"
dirName = ''
#    if "COMTRADE" in fileNameAsal:
#        dirName = fileNameAsal.replace("COMTRADE", "")
#        print(dirName)
#        localfilename = dirName
#        dirName = dirName[:-4]
#    else:
#        dirName = fileNameAsal[:-4]
#        localfilename = fileNameAsal
#    dirName = rootDir+dirName

if "\\" in fileNameAsal:
    buff = fileNameAsal.split("\\")
    dirName = buff[-1]
    localfilename = dirName
    dirName = dirName[:-4]
elif "/" in fileNameAsal:
    buff = fileNameAsal.split("/")
    dirName = buff[-1]
    localfilename = dirName
    dirName = dirName[:-4]
else:
    dirName = fileNameAsal[:-4]
    localfilename = fileNameAsal
    
dirName = rootDir+"/"+dirName

print(dirName)
    

    
    # localfilename = fileNameAsal.replace('\\', '')
localfilename = localfilename.replace('/', '')
print(dirName+"/"+localfilename)
    #open(dirName+"/"+localfilename, "w").close()  # create an empty file
    # print(dirName+"\\"+localfilename)
    