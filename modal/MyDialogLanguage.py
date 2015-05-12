#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx, os, sys
sys.path.append(os.getcwd() + "..\\")
from settings import AVAILABLE_LANGUAGES


class MyDialogLanguage(wx.Dialog):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER | wx.THICK_FRAME | wx.STAY_ON_TOP
        wx.Dialog.__init__(self, *args, **kwds)
        self.combo_box_1 = wx.ComboBox(self, -1, choices=[], style=wx.CB_DROPDOWN)
        for language in AVAILABLE_LANGUAGES:
            self.combo_box_1.Append(language)
        self.combo_box_1.SetValue("English")
        self.button_1 = wx.Button(self, wx.ID_APPLY, "Apply")
        self.sizer_1_staticbox = wx.StaticBox(self, -1, "Language:")

        self.__set_properties()
        self.__do_layout()
        
        self.Bind(wx.EVT_BUTTON, self.save_language, self.button_1)

    def __set_properties(self):
        self.SetTitle("Choose language")
        _icon = wx.EmptyIcon()
        _icon.CopyFromBitmap(wx.Bitmap("C:\\Users\\marcio\\Desktop\\coding\\python\\wxGlade\\icon\\bitbucket_small.ico", wx.BITMAP_TYPE_ANY))
        self.SetIcon(_icon)
        self.SetSize((200, 120))

    def __do_layout(self):
        self.sizer_1_staticbox.Lower()
        sizer_1 = wx.StaticBoxSizer(self.sizer_1_staticbox, wx.VERTICAL)
        sizer_1.Add(self.combo_box_1, 0, wx.EXPAND, 0)
        sizer_1.Add(self.button_1, 0, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        self.Layout()
        
    def save_language(self, event):
        print "Event handler `save_language' not implemented"
        event.Skip()