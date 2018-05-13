import webbrowser

class UrlManager:
    def __init__(self):
        self.urlList = []

    @staticmethod
    def isURL(url):
        if url.find("http:") != -1 or \
           url.find("https:") != -1 or \
           url.find("www.") != -1:
           return True
        return False

    @staticmethod
    def openURL(url):
        webbrowser.open_new(url)