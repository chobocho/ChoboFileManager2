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

SW_TITLE = "ChoboFileManager2 V0627.0528a"

class ChoboFileManagerFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(ChoboFileManagerFrame, self).__init__(*args, **kw)
        self.Bind(wx.EVT_CLOSE, self.onCloseApp)

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