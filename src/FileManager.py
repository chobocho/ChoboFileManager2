import os

class FileManager:
    def __init__(self):
        self.fileList = []
        self.currDir = os.getcwd()
        self.updateFilelist()

    def getCurrentDir(self):
        return self.currDir

    def getFileList(self):        
        return self.fileList

    def updateCurrentFolder(self, newDir):
        prevDir = self.currDir
        nextDir = newDir.strip()
        print ("change currDir enter to " + nextDir)

        if (nextDir != ""):
            try:
                if nextDir == "..":
                    print ("Next : ..")
                    print (os.getcwd())
                    os.chdir("..")
                else:
                    os.chdir(nextDir)
                self.currDir = os.getcwd()
            except:
                print ("Error : Unexpected folder!")
                self.currDir = prevDir
                os.chdir(self.currDir)
                return False
            
            self.updateFilelist()
            return True
        else:
            return False

    def updateFilelist(self):
        self.fileList= [["..", ""]]
        fileList = os.listdir(self.currDir)
        
        for filename in fileList:
            fullfilename = os.path.join(self.currDir, filename)
            tmpFile = []
            if os.path.isdir(fullfilename):
                #print ("[" + filename + "]"
                tmpFile.append("[" + filename + "]")
                tmpFile.append("")
            else:
                #print filename
                tmpFile.append(filename)
                tmpFile.append(str(os.path.getsize(fullfilename)))
            self.fileList.append(tmpFile)
        self.fileList.sort()
