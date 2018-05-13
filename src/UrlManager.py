import webbrowser
import UrlListCtrl

class UrlManager:
    def __init__(self):
        self.urlList = []
        self.initUrlList()

    def initUrlList(self):
        self.urlList = []
        self.urlList.append(["www.chobocho.com", "Home"])
        self.urlList.append(["www.google.com", "구글"])
        self.urlList.append(["www.daum.net", "다음"])
        self.urlList.append(["www.naver.com", "네이버"])

    def setCtrlList(self, list):
        self.ctrlList = list
        self.ctrlList.update(self.urlList)

    def addUrl(self, url):
        newUrl = []
        newUrl.append(url)
        newUrl.append("")
        self.urlList.append(newUrl)
        self.ctrlList.update(self.urlList)

    def clearAll(self):
        self.initUrlList()
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
            else:
                print ("Error! URL data is mismatch!")

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
        self.addUrl(url)
 