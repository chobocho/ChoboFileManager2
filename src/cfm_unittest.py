import unittest
import os
import ChoboFileManager2
import UrlManager
import FileManager

class TestStringMethods(unittest.TestCase):
    def test_urlManager(self):
        urlSavedFileName = "cfm20180514.cfm"
        if (os.path.isfile(urlSavedFileName)):
           urlmanager = UrlManager.UrlManager()
           urlmanager.urlSavedFileName = urlSavedFileName
           urlmanager.loadURL()
           self.assertTrue(urlmanager.hasUrl("www.google.com"))
           self.assertFalse(urlmanager.hasUrl("www.yahoo.com"))

    def test_urlManager_exportHtml(self):
        urlmanager = UrlManager.UrlManager()
        urlmanager.exportToHtml("","test1.htm")
        self.assertTrue(os.path.isfile("test1.htm"))

    def test_urlManager_exportHtmlWithFilter(self):
        urlmanager = UrlManager.UrlManager()
        urlmanager.exportToHtml("com","test2.htm")
        self.assertTrue(os.path.isfile("test2.htm"))

    def test_urlManager_updateWithFilteR(self):
        urlmanager = UrlManager.UrlManager()

if __name__ == '__main__':
    unittest.main()