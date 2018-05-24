import wx
import wx.lib.mixins.listctrl as listmix
import os
import ChoboFileManagerPanel
'''
Start  : 2017.05.13
Update : 2018.05.13a
'''

SW_TITLE = "ChoboFileManager2 V0627.0524a"

class ChoboFileManagerFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(ChoboFileManagerFrame, self).__init__(*args, **kw)
        self.Bind(wx.EVT_CLOSE, self.onCloseApp)
        self.panel = ChoboFileManagerPanel.ChoboFileManagerPanel(self)
        #ico = wx.Icon('disk.ico', wx.BITMAP_TYPE_ICO)
        #self.SetIcon(ico)

    def onCloseApp(self, event):
        if event.CanVeto() and self.panel.needSave():
            try:
               self.panel.saveData()
            except:
               dlg = wx.MessageDialog(self, 'Exception happened during closing CFM!',
                        'ChoboFileManager2', wx.OK | wx.ICON_INFORMATION)
               dlg.ShowModal()
               dlg.Destroy()
        self.Destroy()


def main(): 
    app = wx.App()
    frm = ChoboFileManagerFrame(None, title=SW_TITLE, size=(600,600))
    frm.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()