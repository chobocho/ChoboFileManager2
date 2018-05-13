import webbrowser
import UrlListCtrl

class UrlManager:
    def __init__(self):
        self.urlList = []

    def setCtrlList(self, list):
        self.ctrlList = list

    def addUrl(self, url):
        newUrl = []
        newUrl.append(url)
        newUrl.append("")
        self.urlList.append(newUrl)
        self.ctrlList.update(self.urlList)

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
 