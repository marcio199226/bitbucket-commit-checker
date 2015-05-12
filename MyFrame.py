#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx, os, gettext
from settings import AVAILABLE_LANGUAGES
from functools import partial

_ = gettext.gettext

class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):     
        kwds["style"] = wx.CAPTION | wx.SYSTEM_MENU | wx.TAB_TRAVERSAL | wx.CLOSE_BOX | wx.MINIMIZE_BOX | wx.ICONIZE
        wx.Frame.__init__(self, *args, **kwds)
        favicon = wx.Icon(os.getcwd() + "\\icon\\bitbucket_small.ico", wx.BITMAP_TYPE_ICO, 16, 16)
        self.SetIcon(favicon)
        
        #menubar
        self.frame_1_menubar = wx.MenuBar()
        self.Menu = wx.Menu()
        #submenu
        self.submenu_lang = wx.Menu()
        for lang in AVAILABLE_LANGUAGES:
            self.submenu_lang.Append(wx.NewId(), _(lang), kind=wx.ITEM_RADIO)
        self.Menu.AppendMenu(wx.NewId(), _("Language"), self.submenu_lang)
        self.Menu.AppendSeparator()
        self.submenu = wx.MenuItem(self.Menu, wx.NewId(), _("About"))
        self.Menu.AppendItem(self.submenu)
        #menubar
        self.frame_1_menubar.Append(self.Menu, _("Menu"))
        self.SetMenuBar(self.frame_1_menubar)
        
        #other widgets
        self.label_7 = wx.StaticText(self, -1, _("Notification:"))
        self.checkbox_1 = wx.CheckBox(self, -1, _("Play sound"))
        self.label_8 = wx.StaticText(self, -1, _("Profile:"))
        self.checkbox_2 = wx.CheckBox(self, -1, _("Load last data profile"))
        self.label_9 = wx.StaticText(self, -1, _("Settings:"))
        self.checkbox_3 = wx.CheckBox(self, -1, _("Save data"))
        self.label_6 = wx.StaticText(self, -1, _("Req. minutes"))
        self.spin_ctrl_1 = wx.SpinCtrl(self, -1, "10", min=0, max=100)
        self.label_1 = wx.StaticText(self, -1, _("Login:"))
        self.text_ctrl_1 = wx.TextCtrl(self, -1, "")
        self.label_2 = wx.StaticText(self, -1, _("Password"))
        self.text_ctrl_2 = wx.TextCtrl(self, -1, "", style=wx.TE_PASSWORD)
        self.label_5 = wx.StaticText(self, -1, _("Owner:"))
        self.text_ctrl_4 = wx.TextCtrl(self, -1, "")
        self.label_3 = wx.StaticText(self, -1, _("Repository:"))
        self.text_ctrl_3 = wx.TextCtrl(self, -1, "")
        self.label_4 = wx.StaticText(self, -1, _("Message:"))
        self.text_ctrl_5 = wx.TextCtrl(self, -1, "", style=wx.TE_READONLY)
        self.button_1 = wx.Button(self, -1, _("Run"))
        self.button_2 = wx.Button(self, -1, _("Stop"))

        #get all menubar item for the later setting of their events
        self._items = self.submenu_lang.GetMenuItems()
        for item in self._items:
            self.Bind(wx.EVT_MENU, partial(self.choose_language, item.GetText()), item, id=item.GetId())
        
        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_CLOSE, self.on_close)
        self.Bind(wx.EVT_BUTTON, self.bitbucket_run_checker, self.button_1)
        self.Bind(wx.EVT_BUTTON, self.bitbucket_stop_checker, self.button_2)
        self.Bind(wx.EVT_CHECKBOX, self.bitbucket_load_data, self.checkbox_2)
        self.Bind(wx.EVT_MENU, self.about, self.submenu)

    def __set_properties(self):
        self.SetTitle("Bitbucker commit checker")
        self.SetSize((350, 260))
        self.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_3DLIGHT))
        self.label_7.SetMinSize((80, 20))
        self.checkbox_1.SetMinSize((180, 20))
        self.label_8.SetMinSize((80, 20))
        self.checkbox_2.SetMinSize((180, 20))
        self.label_9.SetMinSize((80, 20))
        self.checkbox_3.SetMinSize((180, 20))
        self.label_6.SetMinSize((80, 20))
        self.spin_ctrl_1.SetMinSize((180, 20))
        self.label_1.SetMinSize((80, 20))
        self.text_ctrl_1.SetMinSize((180, 20))
        self.label_2.SetMinSize((80, 20))
        self.text_ctrl_2.SetMinSize((180, 20))
        self.label_5.SetMinSize((80, 20))
        self.text_ctrl_4.SetMinSize((180, 20))
        self.label_3.SetMinSize((80, 20))
        self.text_ctrl_3.SetMinSize((180, 20))
        self.label_4.SetMinSize((80, 20))
        self.text_ctrl_5.SetMinSize((180, 20))
        self.button_1.SetMinSize((80, 20))
        self.button_2.SetMinSize((180, 20))
        self.button_2.Enable(False)

    def __do_layout(self):
        self.sizer_1 = wx.BoxSizer(wx.VERTICAL)
        self.grid_sizer_1 = wx.FlexGridSizer(9, 2, 0, 0)
        self.grid_sizer_1.Add(self.label_7, 0, 0, 0)
        self.grid_sizer_1.Add(self.checkbox_1, 0, 0, 0)
        self.grid_sizer_1.Add(self.label_8, 0, 0, 0)
        self.grid_sizer_1.Add(self.checkbox_2, 0, 0, 0)
        self.grid_sizer_1.Add(self.label_9, 0, 0, 0)
        self.grid_sizer_1.Add(self.checkbox_3, 0, 0, 0)
        self.grid_sizer_1.Add(self.label_6, 0, 0, 0)
        self.grid_sizer_1.Add(self.spin_ctrl_1, 0, 0, 0)
        self.grid_sizer_1.Add(self.label_1, 0, 0, 0)
        self.grid_sizer_1.Add(self.text_ctrl_1, 0, 0, 0)
        self.grid_sizer_1.Add(self.label_2, 0, 0, 0)
        self.grid_sizer_1.Add(self.text_ctrl_2, 0, 0, 0)
        self.grid_sizer_1.Add(self.label_5, 0, 0, 0)
        self.grid_sizer_1.Add(self.text_ctrl_4, 0, 0, 0)
        self.grid_sizer_1.Add(self.label_3, 0, 0, 0)
        self.grid_sizer_1.Add(self.text_ctrl_3, 0, 0, 0)
        self.grid_sizer_1.Add(self.label_4, 0, 0, 0)
        self.grid_sizer_1.Add(self.text_ctrl_5, 0, 0, 0)
        self.grid_sizer_1.Add(self.button_1, 0, 0, 0)
        self.grid_sizer_1.Add(self.button_2, 0, 0, 0)
        self.sizer_1.Add(self.grid_sizer_1, 1, wx.ALIGN_CENTER_HORIZONTAL, 0)
        self.SetSizer(self.sizer_1)
        self.Layout()

    def bitbucket_run_checker(self, event):
        print "Event handler `bitbucket_run_checker' not implemented"
        event.Skip()

    def bitbucket_stop_checker(self, event):
        print "Event handler `bitbucket_stop_checker' not implemented"
        event.Skip()
        
    def bitbucket_load_data(self, event):
        print "Event handler `bitbucket_save_data' not implemented"
        event.Skip()
        
    def choose_language(self, label, event):
        print "Event handler `choose_language' not implemented"
        event.Skip()
        
    def about(self, event):
        print "Event handler `about' not implemented"
        event.Skip()
        
    def on_close(self, event):
        print "Event handler `on_close' not implemented"
        event.Skip()

# end of class MyFrame
