import wx
import wx.lib.mixins.listctrl as listmix
import UrlManager

class UrlListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
    def __init__(self, parent, ID, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        listmix.ListCtrlAutoWidthMixin.__init__(self)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onItemSelected)
        self.Bind(wx.EVT_RIGHT_UP, self.onRightClick)
        self.Bind(wx.EVT_LEFT_DCLICK, self.onDoubleClick)
        self.addColumn()

    def setUrlManager(self, urlManager):
        self.urlManager = urlManager

    def addColumn(self):
        self.InsertColumn(0, "ID", width=30)
        self.InsertColumn(1, "URL", width=170)
        self.InsertColumn(2, "Memo", width=200)
        self.currentItem = -1

    def getUrlInfo(self, idx):
        url = []
        #url.append(self.GetItem(idx, 0).GetText())
        url.append(self.GetItem(idx, 1).GetText())
        url.append(self.GetItem(idx, 2).GetText())
        return url
  
    def getSelectedUrlItem(self):
        url = []
        if (self.currentItem != -1):
            idx = self.currentItem
            url.append(self.GetItem(idx, 1).GetText())
            url.append(self.GetItem(idx, 2).GetText())
        return url

    def getSelectedUrl(self):
        if (self.currentItem != -1):
            return self.getUrlInfo(self.currentItem)[0]
        else: 
            return ""

    def onDoubleClick(self, evt):
        if (self.currentItem != -1):
            print ("DK: " + self.getUrlInfo(self.currentItem)[0])
            UrlManager.UrlManager.openURL2(self.getUrlInfo(self.currentItem)[0])

    def onRightClick(self, evt):
        self.urlManager.updateUrl()

    def onItemSelected(self, evt):
        self.currentItem = evt.Index
        if (self.currentItem != -1) and wx.TheClipboard.Open():
            wx.TheClipboard.SetData(wx.TextDataObject(self.GetItem(self.currentItem, 1).GetText()))
            wx.TheClipboard.Close()
 
    def update(self, urlList):
        self.DeleteAllItems()
        for url in urlList:
            index = self.InsertItem(self.GetItemCount(), url[0])
            self.SetItem(index, 0, str(index+1))
            self.SetItem(index, 1, url[0])
            self.SetItem(index, 2, url[1])
            if index % 2 == 0:
                self.SetItemBackgroundColour(index, "Light blue")
        self.currentItem = -1

    def updateWithFilter(self, urlList, filters):
        self.DeleteAllItems()
        urlCount = 0
        for url in urlList:
            if filters.lower() in url[0].lower() or filters.lower() in url[1].lower():
                index = self.InsertItem(self.GetItemCount(), url[0])
                self.SetItem(index, 0, str(urlCount+1))
                self.SetItem(index, 1, url[0])
                self.SetItem(index, 2, url[1])
                if index % 2 == 0:
                    self.SetItemBackgroundColour(index, "Light blue")
            urlCount = urlCount + 1
        self.currentItem = -1