import wx
import wx.lib.mixins.listctrl as listmix
import os
import ChoboFileManagerPanel
import ChoboUrlManagerPanel
import UrlManager
import CommandInterpreter
'''
Start  : 2017.05.13
Update : 2018.05.13a
'''

SW_TITLE = "ChoboFileManager2 V0627.0601a"

class ChoboFileManagerFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(ChoboFileManagerFrame, self).__init__(*args, **kw)
        self.Bind(wx.EVT_CLOSE, self.onCloseApp)
        ctrl_D_Id = wx.NewIdRef()
        self.Bind(wx.EVT_MENU, self.onFocusOnFileCMD, id=ctrl_D_Id)
        ctrl_F_Id = wx.NewIdRef()
        self.Bind(wx.EVT_MENU, self.onFind, id=ctrl_F_Id)
        ctrl_G_Id = wx.NewIdRef()
        self.Bind(wx.EVT_MENU, self.onGoFolder, id=ctrl_G_Id)
        ctrl_L_Id = wx.NewIdRef()
        self.Bind(wx.EVT_MENU, self.onFocusOnUrl, id=ctrl_L_Id)
        ctrl_P_Id = wx.NewIdRef()
        self.Bind(wx.EVT_MENU, self.onRunPaint, id=ctrl_P_Id)
        ctrl_R_Id = wx.NewIdRef()
        self.Bind(wx.EVT_MENU, self.onRun, id=ctrl_R_Id)
        ctrl_U_Id = wx.NewIdRef()
        self.Bind(wx.EVT_MENU, self.onFocusOnUrlCMD, id=ctrl_U_Id)
        ctrl_Q_Id = wx.NewIdRef()
        self.Bind(wx.EVT_MENU, self.onClose, id=ctrl_Q_Id)

        alt_F_Id = wx.NewIdRef()
        self.Bind(wx.EVT_MENU, self.onFocusOnFileList, id=alt_F_Id)
        alt_U_Id = wx.NewIdRef()
        self.Bind(wx.EVT_MENU, self.onFocusOnUrlList, id=alt_U_Id)

        accel_tbl = wx.AcceleratorTable([(wx.ACCEL_CTRL,  ord('D'), ctrl_D_Id ),
                                         (wx.ACCEL_CTRL,  ord('F'), ctrl_F_Id ),
                                         (wx.ACCEL_CTRL,  ord('G'), ctrl_G_Id ),
                                         (wx.ACCEL_CTRL,  ord('L'), ctrl_L_Id ),
                                         (wx.ACCEL_CTRL,  ord('P'), ctrl_P_Id ),
                                         (wx.ACCEL_CTRL,  ord('R'), ctrl_R_Id ),
                                         (wx.ACCEL_CTRL,  ord('U'), ctrl_U_Id ),
                                         (wx.ACCEL_CTRL,  ord('Q'), ctrl_Q_Id ),
                                         (wx.ACCEL_ALT,   ord('F'), alt_F_Id ),
                                         (wx.ACCEL_ALT,   ord('U'), alt_U_Id )])
        self.SetAcceleratorTable(accel_tbl)

        self.splitter = wx.SplitterWindow(self, -1, wx.Point(0, 0), wx.Size(800, 800), wx.SP_3D | wx.SP_BORDER)
        self.urlManger = UrlManager.UrlManager()
        self.fileManagerPanel = ChoboFileManagerPanel.ChoboFileManagerPanel(self.splitter)
        self.fileManagerPanel.setUrlManager(self.urlManger)
        self.urlManagerPanel = ChoboUrlManagerPanel.ChoboUrlManagerPanel(self.splitter)
        self.urlManagerPanel.setUrlManager(self.urlManger)
        self.urlManagerPanel.drawUI()
        self.splitter.SplitHorizontally(self.fileManagerPanel, self.urlManagerPanel)
        self.splitter.SetMinimumPaneSize(20)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.splitter, 1, wx.EXPAND)
        self.SetSizer(sizer)

        #ico = wx.Icon('disk.ico', wx.BITMAP_TYPE_ICO)
        #self.SetIcon(ico)

    def onFind(self, event):
        dlg = wx.TextEntryDialog(None, 'Input keyword','Find')
        dlg.SetValue("")

        if dlg.ShowModal() == wx.ID_OK:
            keyword = dlg.GetValue()
            self.fileManagerPanel.onFind(keyword)
            self.urlManagerPanel.onFind(keyword)
        dlg.Destroy()

    def onGoFolder(self, event):
        folder = self.urlManagerPanel.getCurrentURL()
        print ("onGoFolder " + folder)
        if folder.find("://") == -1:
            self.fileManagerPanel.onGoToFolder(folder)
        else:
            print ("onGoFolder : it is not folder " + folder)

    def onRunPaint(self, event):
        print ("onRunPaint")
        ci = CommandInterpreter.CommandInterpreter()
        ci.run("mspaint")

    def onRun(self, event):
        print("onRun")
        dlg = wx.TextEntryDialog(None, 'Input command','Run')
        dlg.SetValue("")

        command = "-1"
        if dlg.ShowModal() == wx.ID_OK:
            command = dlg.GetValue()
        dlg.Destroy()
        print (command)
        if command != "-1":
            ci = CommandInterpreter.CommandInterpreter()
            ci.run(command)

    def onFocusOnUrl(self, event):
        print ("onFocusOnUrl")
        self.fileManagerPanel.setFocusOnUrlText()

    def onFocusOnFileCMD(self, event):
        print ("onFocusOnFileCMD")
        self.fileManagerPanel.setFocusOnCmdText()

    def onFocusOnFileList(self, event):
        print ("onFocusOnFileList")
        self.fileManagerPanel.setFocusOnFileCtrl()

    def onFocusOnUrlCMD(self, event):
        print ("onFocusOnUrlCMD")
        self.urlManagerPanel.setFocusOnCmdText()

    def onFocusOnUrlList(self, event):
        print ("onFocusOnFileList")
        self.urlManagerPanel.setFocusOnUrlCtrl()

    def onClose(self, event):
        self.Close()

    def onCloseApp(self, event):
        if event.CanVeto() and self.urlManagerPanel.needSave():
            try:
               self.urlManagerPanel.saveData()
            except:
               dlg = wx.MessageDialog(self, 'Exception happened during closing CFM!',
                        'ChoboFileManager2', wx.OK | wx.ICON_INFORMATION)
               dlg.ShowModal()
               dlg.Destroy()
        self.Destroy()


def main(): 
    app = wx.App()
    frm = ChoboFileManagerFrame(None, title=SW_TITLE, size=(800,800))
    frm.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()