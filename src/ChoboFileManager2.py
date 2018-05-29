import wx
import wx.lib.mixins.listctrl as listmix
import os
import ChoboFileManagerPanel
import ChoboUrlManagerPanel
import UrlManager
'''
Start  : 2017.05.13
Update : 2018.05.13a
'''

SW_TITLE = "ChoboFileManager2 V0627.0530a"

class ChoboFileManagerFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(ChoboFileManagerFrame, self).__init__(*args, **kw)
        self.Bind(wx.EVT_CLOSE, self.onCloseApp)
        ctrl_F_Id = wx.NewId()
        self.Bind(wx.EVT_MENU, self.onFind, id=ctrl_F_Id)
        ctrl_O_Id = wx.NewId()
        self.Bind(wx.EVT_MENU, self.onFocusOnUrl, id=ctrl_O_Id)
        ctrl_D_Id = wx.NewId()
        self.Bind(wx.EVT_MENU, self.onFocusOnFileCMD, id=ctrl_D_Id)
        ctrl_U_Id = wx.NewId()
        self.Bind(wx.EVT_MENU, self.onFocusOnUrlCMD, id=ctrl_U_Id)
        ctrl_Q_Id = wx.NewId()
        self.Bind(wx.EVT_MENU, self.onClose, id=ctrl_Q_Id)
        accel_tbl = wx.AcceleratorTable([(wx.ACCEL_CTRL,  ord('F'), ctrl_F_Id ),
                                         (wx.ACCEL_CTRL,  ord('O'), ctrl_O_Id ),
                                         (wx.ACCEL_CTRL,  ord('D'), ctrl_D_Id ),
                                         (wx.ACCEL_CTRL,  ord('U'), ctrl_U_Id ),
                                         (wx.ACCEL_CTRL,  ord('Q'), ctrl_Q_Id )])
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


    def onFocusOnUrl(self, event):
        print ("onFocusOnUrl")
        self.fileManagerPanel.setFocusOnUrlText()

    def onFocusOnFileCMD(self, event):
        print ("onFocusOnFileCMD")
        self.fileManagerPanel.setFocusOnCmdText()

    def onFocusOnUrlCMD(self, event):
        print ("onFocusOnUrlCMD")
        self.urlManagerPanel.setFocusOnCmdText()

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