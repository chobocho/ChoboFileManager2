import wx
import wx.lib.mixins.listctrl as listmix
import FileListCtrl
import UrlListCtrl
import FileManager
import UrlManager
import random
import os

class ChoboFileManagerPanel(wx.Panel):
    def __init__(self, *args, **kw):
        super(ChoboFileManagerPanel, self).__init__(*args, **kw)
        self.fileManager = FileManager.FileManager()
        self.drawUI()

    def setUrlManager(self, urlmanager):
        self.urlManger = urlmanager

    def setFocusOnUrlText(self):
        self.urlText.SetFocus()

    def setFocusOnFileCtrl(self):
        self.fileList.SetFocus()

    def setFocusOnCmdText(self):
        self.cmdText.SetFocus()

    def onUrlGo(self, evt):
        strUrl = self.urlText.GetValue()

        print ("onUrlGo: " + strUrl)

        if strUrl[:2] == "u:" or \
             strUrl[:2] == "U:":
            print("u :" + strUrl[2:])
            self.urlManger.openURL(strUrl[2:])

        elif UrlManager.UrlManager.isURL(strUrl):
            self.urlManger.openURL(strUrl)

        elif strUrl[:2] == "f:" or \
           strUrl[:2] == "F:":
            print("f :" + strUrl[2:])
            self.fileManager.updateCurrentFolder(strUrl[2:])

        elif self.fileManager.updateCurrentFolder(strUrl) == True:
            self.fileList.update(self.fileManager.getFileList())

        else:
            UrlManager.UrlManager.openURL2(strUrl)

        self.urlText.SetValue(self.fileManager.getCurrentDir())

    def onRunCmd(self, evt):
        tmpCmd = self.cmdText.GetValue().strip()
        self.cmdText.SetValue("")

        if len(tmpCmd) == 0:
           self.fileList.update(self.fileManager.getFileList())
           return
        print (tmpCmd)

        if (tmpCmd.lower() == "update") or (tmpCmd.lower() == "up"):
            self.fileManager.updateFilelist()
            self.fileList.update(self.fileManager.getFileList())
        elif (tmpCmd.lower() == "ex" or tmpCmd.lower() == "explore"):
           os.system("explorer " + self.fileManager.getCurrentDir())
        elif '/' in tmpCmd[0].lower():
            if len(tmpCmd) > 1:
                self.fileList.filteredUpdate(self.fileManager.getFileList(), tmpCmd[1:])
            else:
                self.fileList.update(self.fileManager.getFileList())
        else:
            os.system("start " + tmpCmd)

    def onFind(self, keyword):
        if len(keyword) > 0:
            self.fileList.filteredUpdate(self.fileManager.getFileList(), keyword)
        else:
            self.fileList.update(self.fileManager.getFileList())

    def onGoToFolder(self, folder):
        if self.fileManager.updateCurrentFolder(folder) == True:
            self.fileList.update(self.fileManager.getFileList())
        else:
            print("onGoToFolder failed")

    def on_runexe(self, exefile):
        print ("run " + exefile)
        os.system("start " + exefile)

    def on_runPython(sefl, pythonFile):
        print ("run python " + pythonFile)
        os.system("start python " + pythonFile)

    def on_runtxt(self, txtfile):
        print ("run " + txtfile)
        os.system("start notepad " + txtfile)

    def OnFileRename(self, evt):
        selectedFile = self.fileList.getSelectedFile()
        if '[' == selectedFile[0] and ']' == selectedFile[-1]:
            selectedFile = selectedFile[1:-1]
       
        print ("OnFileRename: " + selectedFile)
        if len(selectedFile) == 0:
            return

        newFileName = ""
        dlg = wx.TextEntryDialog(None, 'Input new fild name','Rename')
        dlg.SetValue(selectedFile)

        if dlg.ShowModal() == wx.ID_OK:
            newFileName = dlg.GetValue()
            print (selectedFile + " -> " + newFileName)
        dlg.Destroy()
        
        if newFileName.lower() == selectedFile.lower():
            print ("OnFileRename: It is same filename!")
            return

        try:
            os.rename(selectedFile, newFileName)
            self.fileManager.updateFilelist()
            self.fileList.update(self.fileManager.getFileList())
        except:
            print ("OnFileRename: It is failed to rename!")

    def OnNewFolder(self, evt):
        print ("OnNewFolder")
        defaultFolderName = "cfm0627_" + str(int(random.random()*100000)+1)
        newfolder = ""
        dlg = wx.TextEntryDialog(None, 'Input new folder name','New folder')
        dlg.SetValue(defaultFolderName)

        if dlg.ShowModal() == wx.ID_OK:
            newfolder = dlg.GetValue()
            print (newfolder)
        dlg.Destroy()

        try:
           if len(newfolder) > 1:
               os.mkdir(newfolder)
               self.fileManager.updateFilelist()
               self.fileList.update(self.fileManager.getFileList())
        except:
           print("it is failed to make a new folder!")


    def OnRunExplore(self, evt):
        os.system("explorer " + self.fileManager.getCurrentDir())
        print ("OnRunExplore")

    def OnRunNotepad(self, evt):
        print ("OnRunNotepad")
        os.system("start notepad")

    def handleFileListEvnet(self, url):
        print ("Event")

        currdir = self.fileManager.getCurrentDir()
        filename = url[1:-1]
        fullfilename = os.path.join(currdir, filename)
        isFolder = os.path.isdir(fullfilename)

        if (url == ".."):
            if self.fileManager.updateCurrentFolder(url) == True:
                self.fileList.update(self.fileManager.getFileList())

        elif (url[0] == '[' and isFolder == True):
            if self.fileManager.updateCurrentFolder(fullfilename) == True:
                self.fileList.update(self.fileManager.getFileList())
 
        elif "exe." == url[:-5:-1].lower() or \
             "tab." == url[:-5:-1].lower() or \
             "fdp." == url[:-5:-1].lower() or \
             "mth." == url[:-5:-1].lower() or \
             "lmth." == url[:-6:-1].lower():
            self.on_runexe(url)
     
        elif ("yp." == url[:-4:-1].lower() or \
              "wyp." == url[:-5:-1].lower()):
            self.on_runPython(url)

        elif ("txt." == url[:-5:-1].lower() or \
              "pac." == url[:-5:-1].lower() or \
              "ppc." == url[:-5:-1].lower() or \
              "lmx." == url[:-5:-1].lower() or \
              "gol." == url[:-5:-1].lower()):
            self.on_runtxt(url)
        self.urlText.SetValue(self.fileManager.getCurrentDir())
        self.fileManager.updateFilelist()
        self.fileList.update(self.fileManager.getFileList())


    def drawUI(self):
        print ("ChoboFileManagerPanel::drawUI")
        sizer = wx.BoxSizer(wx.VERTICAL)

        urlBox = wx.BoxSizer(wx.HORIZONTAL)

        self.urlText = wx.TextCtrl(self,style = wx.TE_PROCESS_ENTER,size=(500,25))
        self.urlText.Bind(wx.EVT_TEXT_ENTER, self.onUrlGo)
        self.urlText.SetValue(self.fileManager.getCurrentDir())
        urlBox.Add(self.urlText, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        sizer.Add(urlBox, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        ## FileListCtrl
        fileListID = wx.NewId()
        self.fileList = FileListCtrl.FileListCtrl(self, fileListID,
                                 style=wx.LC_REPORT
                                 | wx.BORDER_NONE
                                 | wx.LC_EDIT_LABELS
                                 )
        self.fileList.update(self.fileManager.getFileList())
        self.fileList.setPanel(self)
        sizer.Add(self.fileList, 1, wx.EXPAND)

        ##
        fileCmdBox = wx.BoxSizer(wx.HORIZONTAL)

        
        self.cmdLbl = wx.StaticText(self, -1, "File cmd")
        fileCmdBox.Add(self.cmdLbl, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.cmdText = wx.TextCtrl(self, style = wx.TE_PROCESS_ENTER,size=(500,25))
        self.cmdText.Bind(wx.EVT_TEXT_ENTER, self.onRunCmd)
        self.cmdText.SetValue("")
        fileCmdBox.Add(self.cmdText, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        
        sizer.Add(fileCmdBox, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        ##
        fileMngBtnBox = wx.BoxSizer(wx.HORIZONTAL)

        self.fileRenameBtn = wx.Button(self, 10, "Rename", size=(30,30))
        self.fileRenameBtn.Bind(wx.EVT_BUTTON, self.OnFileRename)
        fileMngBtnBox.Add(self.fileRenameBtn, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        self.newFolderBtn = wx.Button(self, 10, "New Folder", size=(30,30))
        self.newFolderBtn.Bind(wx.EVT_BUTTON, self.OnNewFolder)
        fileMngBtnBox.Add(self.newFolderBtn, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        self.exploreBtn = wx.Button(self, 10, "Explore", size=(30,30))
        self.exploreBtn.Bind(wx.EVT_BUTTON, self.OnRunExplore)
        fileMngBtnBox.Add(self.exploreBtn, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        self.notePadBtn = wx.Button(self, 10, "Notepad", size=(30,30))
        self.notePadBtn.Bind(wx.EVT_BUTTON, self.OnRunNotepad)
        fileMngBtnBox.Add(self.notePadBtn, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        sizer.Add(fileMngBtnBox, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        self.SetSizer(sizer)
        self.SetAutoLayout(True)
