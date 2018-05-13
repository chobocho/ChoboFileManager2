import unittest
import os
import ChoboFileManager2
import UrlManager

class TestStringMethods(unittest.TestCase):
    def test_urlManager(self):
        urlSavedFileName = "cfm20180514.cfm"
        if (os.path.isfile(urlSavedFileName)):
           urlmanager = UrlManager.UrlManager()
           urlmanager.urlSavedFileName = urlSavedFileName
           urlmanager.loadURL()
           self.assertTrue(urlmanager.hasUrl("www.google.com"))
           self.assertFalse(urlmanager.hasUrl("www.yahoo.com"))

if __name__ == '__main__':
    unittest.main()