#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx, os, sys, gettext
sys.path.append(os.getcwd() + "..\\")
from MyDialogLanguage import MyDialogLanguage
from settings import LANGUAGE_TO_LOCALE

_ = gettext.gettext

class ChooseLanguage(MyDialogLanguage):
    def save_language(self, event):
        dir = os.getcwd() + "\\modal\\data\\"
        
        if not os.path.isdir(dir):
            os.makedirs(dir)
            
        try:
            key = LANGUAGE_TO_LOCALE[self.combo_box_1.GetValue()]
            file = open(dir + "language.txt", "w").write(key)
            #del file
            self.Destroy()
        except IOError:
            wx.MessageBox(_("Directory {0} is not writable or it does not exist").format(dir), 'Error', wx.OK | wx.ICON_EXCLAMATION)
        

if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    dialog_1 = ChooseLanguage(None, -1, "")
    app.SetTopWindow(dialog_1)
    dialog_1.Show()
    app.MainLoop()
