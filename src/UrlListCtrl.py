import wx
import wx.lib.mixins.listctrl as listmix

class UrlListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
    def __init__(self, parent, ID, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        listmix.ListCtrlAutoWidthMixin.__init__(self)
        self.addColumn()

    def addColumn(self):
        self.InsertColumn(0, "ID", width=30)
        self.InsertColumn(1, "URL", width=170)
        self.InsertColumn(2, "Memo", width=200)
