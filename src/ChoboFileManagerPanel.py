import wx
import wx.lib.mixins.listctrl as listmix
import FileListCtrl
import UrlListCtrl
import FileManager
import UrlManager
import os

class ChoboFileManagerPanel(wx.Panel):
    def __init__(self, *args, **kw):
        super(ChoboFileManagerPanel, self).__init__(*args, **kw)
        self.fileManager = FileManager.FileManager()
        self.urlManger = UrlManager.UrlManager()
        self.drawUI()

    def OnSaveURL(self, evt):
        print ("OnSaveURL")
        
    def OnClearURL(self, evt):
        self.urlManger.clearAll()

    def OnDeleteURL(self, evt):
        self.urlManger.deleteUrl()

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

        print ("run cmd " + tmpCmd)
        if (tmpCmd.lower() == "update"):
            self.fileList.update(self.fileManager.getFileList())
        elif (tmpCmd.lower() == "explore"):
           os.system("explorer " + self.fileManager.getCurrentDir())
        else:
            os.system("start " + tmpCmd)
        self.cmdText.SetValue("")

    def on_runexe(self, exefile):
        print ("run " + exefile)
        os.system("start " + exefile)

    def on_runPython(sefl, pythonFile):
        print ("run python " + pythonFile)
        os.system("start python " + pythonFile)

    def on_runtxt(self, txtfile):
        print ("run " + txtfile)
        os.system("start notepad " + txtfile)

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
 
        elif "exe." == url[:-5:-1] or \
             "tab." == url[:-5:-1]:
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

    def drawUI(self):
        print ("drawUI")
        sizer = wx.BoxSizer(wx.VERTICAL)

        ##
        urlBox = wx.BoxSizer(wx.HORIZONTAL)

        self.urlText = wx.TextCtrl(self,style = wx.TE_PROCESS_ENTER|wx.TE_MULTILINE,size=(500,25))
        self.urlText.Bind(wx.EVT_TEXT_ENTER, self.onUrlGo)
        urlBox.Add(self.urlText, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        #self.urlText = wx.TextCtrl(self, -1, " ",size=(400,-1))
        #urlBox.Add(self.urlText, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        #self.urlGoBtn = wx.Button(self, 10, "Go", size=(30,30))
        #self.urlGoBtn.Bind(wx.EVT_BUTTON, self.OnClickGo)
        #urlBox.Add(self.urlGoBtn, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        #
        #self.urlClearBtn = wx.Button(self, 10, "Clear", size=(30,30))
        #self.urlClearBtn.Bind(wx.EVT_BUTTON, self.OnClickGo)
        #urlBox.Add(self.urlClearBtn, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        sizer.Add(urlBox, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        ## FileListCtrl
        fileListID = wx.NewId()
        self.fileList = FileListCtrl.FileListCtrl(self, fileListID,
                                 style=wx.LC_REPORT
                                 #| wx.BORDER_SUNKEN
                                 | wx.BORDER_NONE
                                 | wx.LC_EDIT_LABELS
                                 #| wx.LC_SORT_ASCENDING    # disabling initial auto sort gives a
                                 #| wx.LC_NO_HEADER         # better illustration of col-click sorting
                                 #| wx.LC_VRULES
                                 #| wx.LC_HRULES
                                 #| wx.LC_SINGLE_SEL
                                 )
        self.fileList.update(self.fileManager.getFileList())
        self.fileList.setPanel(self)
        sizer.Add(self.fileList, 1, wx.EXPAND)

        ##
        fileMngBtnBox = wx.BoxSizer(wx.HORIZONTAL)

        
        self.cmdLbl = wx.StaticText(self, -1, "Cmd")
        fileMngBtnBox.Add(self.cmdLbl, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.cmdText = wx.TextCtrl(self, style = wx.TE_PROCESS_ENTER|wx.TE_MULTILINE,size=(500,25))
        self.cmdText.Bind(wx.EVT_TEXT_ENTER, self.onRunCmd)
        #self.cmdText = wx.TextCtrl(self, -1, " ",size=(400,-1))
        fileMngBtnBox.Add(self.cmdText, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        #
        #self.cmdBtn = wx.Button(self, 10, "Run", size=(30,30))
        #self.cmdBtn.Bind(wx.EVT_BUTTON, self.OnClickGo)
        #fileMngBtnBox.Add(self.cmdBtn, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        #
        #self.cmdClearBtn = wx.Button(self, 10, "Clear", size=(30,30))
        #self.cmdClearBtn.Bind(wx.EVT_BUTTON, self.OnClickGo)
        #fileMngBtnBox.Add(self.cmdClearBtn, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        sizer.Add(fileMngBtnBox, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)


        ## UrlListCtrl
        urlListID = wx.NewId()
        self.urlList = UrlListCtrl.UrlListCtrl(self, urlListID,
                                 style=wx.LC_REPORT
                                 #| wx.BORDER_SUNKEN
                                 | wx.BORDER_NONE
                                 | wx.LC_EDIT_LABELS
                                 #| wx.LC_SORT_ASCENDING    # disabling initial auto sort gives a
                                 #| wx.LC_NO_HEADER         # better illustration of col-click sorting
                                 #| wx.LC_VRULES
                                 #| wx.LC_HRULES
                                 #| wx.LC_SINGLE_SEL
                                 )
        self.urlManger.setCtrlList(self.urlList)
        sizer.Add(self.urlList, 1, wx.EXPAND)

        ##
        urlMngBtnBox = wx.BoxSizer(wx.HORIZONTAL)

        self.urlSaveBtn = wx.Button(self, 10, "Save URL", size=(30,30))
        self.urlSaveBtn.Bind(wx.EVT_BUTTON, self.OnSaveURL)
        urlMngBtnBox.Add(self.urlSaveBtn, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        #self.urlExportBtn = wx.Button(self, 10, "Export", size=(30,30))
        #self.urlExportBtn.Bind(wx.EVT_BUTTON, self.OnClickGo)
        #urlMngBtnBox.Add(self.urlExportBtn, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        self.urlDeleteBtn = wx.Button(self, 10, "Delete", size=(30,30))
        self.urlDeleteBtn.Bind(wx.EVT_BUTTON, self.OnDeleteURL)
        urlMngBtnBox.Add(self.urlDeleteBtn, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        self.urlClearBtn = wx.Button(self, 10, "Clear", size=(30,30))
        self.urlClearBtn.Bind(wx.EVT_BUTTON, self.OnClearURL)
        urlMngBtnBox.Add(self.urlClearBtn, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        sizer.Add(urlMngBtnBox, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        self.SetSizer(sizer)
        self.SetAutoLayout(True)
