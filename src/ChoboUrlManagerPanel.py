import wx
import wx.lib.mixins.listctrl as listmix
import UrlListCtrl
import FileManager
import UrlManager
import os

class ChoboUrlManagerPanel(wx.Panel):
    def __init__(self, *args, **kw):
        super(ChoboUrlManagerPanel, self).__init__(*args, **kw)
        self.fileManager = FileManager.FileManager()

    def setUrlManager(self, urlmanager):
        self.urlManger = urlmanager

    def OnSaveURL(self, evt):
        print ("OnSaveURL")
        self.urlManger.saveURL()
        
    def OnExportUrlToHtml(self, evt):
        print ("OnExportUrlToHtml")
        htmlFilePath = ""
        dlg = wx.FileDialog(
            self, message="Save file as ...", defaultDir=os.getcwd(),
            defaultFile="", wildcard="Html file (*.html)|*.htm", style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
            )
        dlg.SetFilterIndex(2)

        if dlg.ShowModal() == wx.ID_OK:
            htmlFilePath = dlg.GetPath()
        dlg.Destroy()

        if len(htmlFilePath) > 0:
            self.urlManger.exportToHtml("", htmlFilePath)

    def OnClearURL(self, evt):
        self.urlManger.clearAll()

    def OnDeleteURL(self, evt):
        self.urlManger.deleteUrl()

    def onRunCmd(self, evt):
        tmpCmd = self.cmdText.GetValue().strip()
        self.cmdText.SetValue("")

        if len(tmpCmd) == 0:
           self.urlManger.update()
           return
        print (tmpCmd)

        if '/' in tmpCmd[0].lower():
            if len(tmpCmd) > 1:
                self.urlManger.updateWithFilter(tmpCmd[1:])
            else:
                self.urlManger.update()
        elif UrlManager.UrlManager.isURL(tmpCmd):
            self.urlManger.openURL(tmpCmd)

    def onFind(self, keyword):
        if len(keyword) > 0:
            self.urlManger.updateWithFilter(keyword)
        else:
            self.urlManger.update()

    def on_runexe(self, exefile):
        print ("run " + exefile)
        os.system("start " + exefile)

    def needSave(self):
        return self.urlManger.needSave()

    def saveData(self):
        self.urlManger.saveURL()

    def drawUI(self):
        print ("drawUI")
        self.SetBackgroundColour('LIGHT GREY')
        sizer = wx.BoxSizer(wx.VERTICAL)

        ##
        fileMngBtnBox = wx.BoxSizer(wx.HORIZONTAL)

        
        self.cmdLbl = wx.StaticText(self, -1, "Url cmd")
        fileMngBtnBox.Add(self.cmdLbl, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.cmdText = wx.TextCtrl(self, style = wx.TE_PROCESS_ENTER,size=(500,25))
        self.cmdText.Bind(wx.EVT_TEXT_ENTER, self.onRunCmd)
        self.cmdText.SetValue("")
        fileMngBtnBox.Add(self.cmdText, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        
        sizer.Add(fileMngBtnBox, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        ## UrlListCtrl
        urlListID = wx.NewId()
        self.urlList = UrlListCtrl.UrlListCtrl(self, urlListID,
                                 style=wx.LC_REPORT
                                 | wx.BORDER_NONE
                                 | wx.LC_EDIT_LABELS
                                 )
        self.urlManger.setCtrlList(self.urlList)
        sizer.Add(self.urlList, 1, wx.EXPAND)

        ##
        urlMngBtnBox = wx.BoxSizer(wx.HORIZONTAL)

        self.urlSaveBtn = wx.Button(self, 10, "Save URL", size=(30,30))
        self.urlSaveBtn.Bind(wx.EVT_BUTTON, self.OnSaveURL)
        urlMngBtnBox.Add(self.urlSaveBtn, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        self.urlExportBtn = wx.Button(self, 10, "Export", size=(30,30))
        self.urlExportBtn.Bind(wx.EVT_BUTTON, self.OnExportUrlToHtml)
        urlMngBtnBox.Add(self.urlExportBtn, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        self.urlDeleteBtn = wx.Button(self, 10, "Delete", size=(30,30))
        self.urlDeleteBtn.Bind(wx.EVT_BUTTON, self.OnDeleteURL)
        urlMngBtnBox.Add(self.urlDeleteBtn, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        self.urlClearBtn = wx.Button(self, 10, "Clear", size=(30,30))
        self.urlClearBtn.Bind(wx.EVT_BUTTON, self.OnClearURL)
        urlMngBtnBox.Add(self.urlClearBtn, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        sizer.Add(urlMngBtnBox, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        
        ##
        self.SetSizer(sizer)
        self.SetAutoLayout(True)
