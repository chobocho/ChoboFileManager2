import wx
import wx.lib.mixins.listctrl as listmix

class FileListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
    def __init__(self, parent, ID, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        listmix.ListCtrlAutoWidthMixin.__init__(self)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onItemSelected)
        self.Bind(wx.EVT_LEFT_DCLICK, self.onDoubleClick)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.onDoubleClick)
        self.addColumn()
        self.selectedFile = ""

    def setPanel(self, panel):
        self.panel = panel

    def addColumn(self):
        self.InsertColumn(0, "FileName", width=400)
        self.InsertColumn(1, "Size", width=100)
        self.currentItem = -1

    def getFileInfo(self, idx):
        file = []
        file.append(self.GetItem(idx, 0).GetText())
        file.append(self.GetItem(idx, 1).GetText())
        return file

    def getSelectedFile(self):
        return self.selectedFile

    def onItemSelected(self, evt):
        self.currentItem = evt.Index
        if (self.currentItem != -1) and wx.TheClipboard.Open():
            self.selectedFile = self.GetItem(self.currentItem, 0).GetText()
            wx.TheClipboard.SetData(wx.TextDataObject(self.selectedFile))
            wx.TheClipboard.Close()

    def onDoubleClick(self, evt):
        if (self.currentItem != -1):
            print ("DK: " + self.getFileInfo(self.currentItem)[0])
            self.panel.handleFileListEvnet(self.getFileInfo(self.currentItem)[0])
            
    def update(self, fileList):
        self.DeleteAllItems()
        for file in fileList:
            index = self.InsertItem(self.GetItemCount(), file[0])
            self.SetItem(index, 0, file[0])
            self.SetItem(index, 1, file[1])

            if "exe." == file[0][:-5:-1] or \
               "tab." == file[0][:-5:-1]:
                self.SetItemBackgroundColour(index, "LIGHT BLUE")
            elif "yp." == file[0][:-4:-1] or \
               "wyp." == file[0][:-5:-1]:
                self.SetItemBackgroundColour(index, "GREEN YELLOW")
            elif "[" == file[0][0] and "]" == file[0][-1]:
                self.SetItemBackgroundColour(index, "GOLDENROD")

    def filteredUpdate(self, fileList, filters):
        print(filters)
        self.DeleteAllItems()

        for file in fileList:
            if filters.lower() in file[0].lower() or ".." == file[0]:
                index = self.InsertItem(self.GetItemCount(), file[0])
                self.SetItem(index, 0, file[0])
                self.SetItem(index, 1, file[1])
                
                if "exe." == file[0][:-5:-1] or \
                   "tab." == file[0][:-5:-1]:
                    self.SetItemBackgroundColour(index, "LIGHT BLUE")
                elif "yp." == file[0][:-4:-1] or \
                   "wyp." == file[0][:-5:-1]:
                    self.SetItemBackgroundColour(index, "GREEN YELLOW")
                elif "[" == file[0][0] and "]" == file[0][-1]:
                    self.SetItemBackgroundColour(index, "GOLDENROD")



 