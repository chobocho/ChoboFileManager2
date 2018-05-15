import webbrowser
import UrlListCtrl
import os
import wx

class UrlManager:
    def __init__(self):
        self.urlList = []
        self.urlSavedFileName = "d:\cfm20180514.cfm"
        self.loadURL()
        self.hasUnSaveData = False

    def loadURL(self):
        try:
            if (os.path.isfile(self.urlSavedFileName)):
                f = open(self.urlSavedFileName,'r')
                for url in f:
                    tmpUrl = url.strip().split("(..)")
                    print(tmpUrl)
                    self.urlList.append(tmpUrl)
                f.close()
            else:
                self.initUrlList()
        except:
            dlg = wx.MessageDialog(None, 'Exception happened during closing CFM!',
                     'ChoboFileManager2', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()
            self.initUrlList()

    def saveURL(self):
        f = open(self.urlSavedFileName,'w')
        for url in self.urlList:
            tmpUrl = "(..)".join(url) + "\n"
            f.write(tmpUrl)
        f.close()
        self.hasUnSaveData = False

    def initUrlList(self):
        self.urlList = []
        self.urlList.append(["www.chobocho.com", "Home"])
        self.urlList.append(["www.google.com", "구글"])
        self.urlList.append(["www.daum.net", "다음"])
        self.urlList.append(["www.naver.com", "네이버"])

    def needSave(self):
        return self.hasUnSaveData

    def hasUrl(self, url):
        if (url != ""):
            for u in self.urlList:
                if (url == u[0]):
                    return True
        return False

    def setCtrlList(self, list):
        self.ctrlList = list
        self.ctrlList.setUrlManager(self)
        self.ctrlList.update(self.urlList)

    def addUrl(self, url):
        newUrl = []
        newUrl.append(url)
        newUrl.append("")
        self.urlList.append(newUrl)
        self.ctrlList.update(self.urlList)
        self.hasUnSaveData = True

    def clearAll(self):
        self.urlList = []
        self.ctrlList.update(self.urlList)

    def deleteUrl(self):
        url = self.ctrlList.getSelectedUrl()
        deleteUrl = []
        if (url != ""):
            for u in self.urlList:
                if (url == u[0]):
                   deleteUrl = u
                   break
            if len(deleteUrl) > 0:
                self.urlList.remove(deleteUrl)
                self.ctrlList.update(self.urlList)
                self.hasUnSaveData = True
            else:
                print ("Error! URL data is mismatch!")

    def modifyUrl(self, url):
        if (url != ""):
            for u in self.urlList:
                if (url[0] == u[0]):
                   print("Find")
                   u[1] = url[1]
                   self.hasUnSaveData = True
                   break
            self.ctrlList.update(self.urlList)

    def exportToHtml(self, filters, filePath):
        try:
            htmlHead='''
            <html>
            <head>
            <title>ChoboFileManager2 URL list</title>
            <style>
            td {
                text-align:center
            }
            
            h10 {
                color:white;
            }
            
            a:link {
                text-decoration: none;
            }
            
            a:link, a:visited {
                color: blue;
            }
            </style>
            </head>
            <body>
            <center>
            <table border="1" style="border-collapse:collapse; border:1px gray solid;">
                <tr>
                <td bgcolor=#00bfff>id</td>
                <td bgcolor=#00bfff>URL</td>
                <td bgcolor=#00bfff>Memo</td>
                </tr>
            '''
            htmlTail='''
            </table>
            </body>
            </html>
            '''
            f = open(filePath,'w')
            f.write(htmlHead)
            idx = 1
            for url in self.urlList:
                if len(filters) == 0 or filters.lower() in url[0].lower() or filters.lower() in url[1].lower(): 
                    f.write("<tr>")
                    bgcolor = ""
                    if idx % 2 == 0:
                        bgcolor = "bgcolor=#e6f2ff"
                    tmpHtml = "<td {0}>&nbsp;{1}&nbsp;</td><td {0}><a href={2}>&nbsp;{2}&nbsp;</a></td><td {0}>&nbsp;{3}&nbsp;</td>".format(bgcolor, idx, url[0], url[1])
                    print(tmpHtml)
                    f.write(tmpHtml)
                    f.write("</tr>")
                    idx = idx + 1
            f.write(htmlTail)
            f.close()
        except:
            dlg = wx.MessageDialog(None, 'Exception happened during export to HTML!',
                     'ChoboFileManager2', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()

    def updateUrl(self):
        print ("updateUrl")
        url = self.ctrlList.getSelectedUrlItem()
        if len(url) > 0:
            dlg = wx.TextEntryDialog(None, 'Please edit memo',url[0], 'Python')
            dlg.SetValue(url[1])

            if dlg.ShowModal() == wx.ID_OK:
                url[1] = dlg.GetValue()
                self.modifyUrl(url)
            dlg.Destroy()

    def update(self):
        self.ctrlList.update(self.urlList)

    def updateWithFilter(self, filters):
        self.ctrlList.updateWithFilter(self.urlList, filters)

    @staticmethod
    def isURL(url):
        if url.find("http:") != -1 or \
           url.find("https:") != -1 or \
           url.find("www.") != -1:
           return True
        return False
    
    @staticmethod
    def openURL2(url):
        webbrowser.open_new(url)
 
    def openURL(self,url):
        webbrowser.open_new(url)
        if self.hasUrl(url) == False:
            self.addUrl(url)
 