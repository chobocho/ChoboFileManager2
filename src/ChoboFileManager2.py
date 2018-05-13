import wx
import os

'''
Start  : 2017.05.13
Update : 2018.05.13a
'''

SW_TITLE = "ChoboFileManager2 V0627.0513a"

class FileManager:
    def __init__(self):
        self.fileList = []
        self.currdir = os.getcwd()

    def getFileList(self):        
        tmpfileList = os.listdir(self.currdir)
        self.fileList = [".."]
        for filename in tmpfileList:
            fullfilename = os.path.join(currdir, filename)
            if os.path.isdir(fullfilename):
                fileList.append("[" + filename + "]")
            else:
                fileList.append(filename)
        return self.fileList


class ChoboFileManagerPanel(wx.Panel):
    def __init__(self, *args, **kw):
        super(ChoboFileManagerPanel, self).__init__(*args, **kw)
        self.fileManager = FileManager()
        self.drawUI()

    def drawUI(self):
        pass


class ChoboFileManagerFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(ChoboFileManagerFrame, self).__init__(*args, **kw)
        self.Bind(wx.EVT_CLOSE, self.onCloseApp)
        self.panel = ChoboFileManagerPanel(self)
        ico = wx.Icon('disk.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(ico)

    def onCloseApp(self, event):
        if event.CanVeto():
            if wx.MessageBox("Continue closing?",
                "Please confirm",
                wx.ICON_QUESTION | wx.YES_NO) != wx.YES:
                event.Veto()
                return
        self.Destroy()


def main(): 
    app = wx.App()
    frm = ChoboFileManagerFrame(None, title=SW_TITLE)
    frm.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()