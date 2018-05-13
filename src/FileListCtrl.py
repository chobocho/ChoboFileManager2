import wx
import wx.lib.mixins.listctrl as listmix

class FileListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
    def __init__(self, parent, ID, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        listmix.ListCtrlAutoWidthMixin.__init__(self)
        self.addColumn()

    def addColumn(self):
        self.InsertColumn(0, "FileName", width=400)
        self.InsertColumn(1, "Size", width=100)

    def update(self, fileList):
        self.DeleteAllItems()
        for file in fileList:
            index = self.InsertItem(self.GetItemCount(), file[0])
            self.SetItem(index, 0, file[0])
            self.SetItem(index, 1, file[1])
            if index % 2 == 1:
                self.SetItemBackgroundColour(index, "Light gray")

 