#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __init__ import *
from settings import *

_ = gettext.gettext

class BitbucketRun(Thread):
    def __init__(self, **args):
        self._login = args['login']
        self._pwd = args['pwd']
        self._owner = args['owner']
        self._repo = args['repo']
        self._sleep = args['sleep']
        self._sound = args['sound']
        self.queue = args['queue']
        self._wxFrame = args['wx']
        self.interrupt = Event()
        Thread.__init__(self)

    def run(self):
        messages = (_("New revision is available"), _("No revision available"))
        while not self.interrupt.isSet():
            bitbucket = BitBucketApi()
            bitbucket.setLogin(self._login)
            bitbucket.setPassword(self._pwd)
            bitbucket.setOwnerRepo(self._owner)
            bitbucket.setRepoName(self._repo)
            update = bitbucket.checkLastUpdate()

            if update == True:
                msg = messages[0]
            elif update == False:
                msg = messages[1]
            elif isinstance(update, BitBucketApiException):
                msg = "%s" % update
            
            self.queue.put(msg)
            self._wxFrame.text_ctrl_5.SetValue(msg)
            
            if msg == messages[0]:
                self._wxFrame.text_ctrl_5.SetBackgroundColour('Green')
                if self._sound:
                    winsound.MessageBeep()
            else:
                self._wxFrame.text_ctrl_5.SetBackgroundColour('Red')
            time.sleep(self._sleep)


class BitbucketCheckerMyFrameEvent(MyFrame):
   
    def __init__(self, *args, **kwds):
        self._thread = None
        self._appName = "bitbucket"
        self._localeDir = os.getcwd() + "\\data\\locale\\"
        self._profileDir = os.getcwd() + "\\data\\"
        self._languageDir = os.getcwd() + "\\modal\\data\\"
        self._profileFile = self._profileDir + "profile.txt"
        self._revisionFile = os.getcwd() + "\\data\\revision.txt"
        self._languageFile = self._languageDir + "language.txt"
        self._result = (_("New revision is available"), _("No revision available"))
        
        #set locale and translations' language
        self._setLocaleAndLanguage()
            
        MyFrame.__init__(self, *args, **kwds)
        
        #show dialog windows for choosing language if program starts first time, this dialog destroy itself when user choose the language
        if not self._hasLanguage():
            modalDialogChooseLang = ChooseLanguage(self)
            #user wx.ID_APPLY instead wx.ID_OK for check if user clicked on button and then destroy a dialog frame
            modalDialogChooseLang.ShowModal()
            #when we has chose a language should set the proper item checked in menubar for first time
            self._setProperLanguageMenubar()
        
        #global function from settings.py
        translate_all_languages_data()
        #set the proper language in menu
        self._setProperLanguageMenubar()
        
    def bitbucket_run_checker(self, event):
        queue = Queue.Queue()
        login = self.text_ctrl_1.GetValue()
        pwd = self.text_ctrl_2.GetValue()
        owner = self.text_ctrl_4.GetValue()
        repository = self.text_ctrl_3.GetValue()
        sleep = self._minutes_to_seconds(self.spin_ctrl_1.GetValue())
        playSound = self._isPlaySoundEnable()
        self._thread = BitbucketRun(login=login, pwd=pwd, owner=owner, repo=repository, queue=queue, sleep=sleep, sound=playSound, wx=self)
        self._thread.deamon = True
        self._thread.start()
        msg = queue.get()
        self.text_ctrl_5.SetValue(msg)

        if self._isDataToSave() and not self._hasEmptyInputText():
            data = (login, pwd, owner, repository)
            self._saveDataToFile(data)
        
        if msg in self._result:
            self._toggleInputText(self.grid_sizer_1, False)
            self.button_1.Enable(False)
            self.button_2.Enable(True)
        
        event.Skip()

    def bitbucket_stop_checker(self, event):
        self._thread.interrupt.set()
        self._toggleInputText(self.grid_sizer_1)
        self.button_1.Enable(True)
        self.button_2.Enable(False)
        event.Skip()
        
    def bitbucket_load_data(self, event):
        if self.checkbox_2.IsChecked():
            self._getProfileData()
            if self.checkbox_3.IsChecked():
                self.checkbox_3.SetValue(False)
        else:
            childrens = self.grid_sizer_1.GetChildren()
            for children in childrens:
                widget = children.GetWindow()
                if isinstance(widget, wx.TextCtrl):
                    if not widget.IsEditable():
                        continue
                    elif widget.GetValue() != "":
                        widget.SetValue("")
        event.Skip()
                        
    def choose_language(self, label, event):     
        try:
            profile_data = open(self._languageFile, "w")
            profile_data.write(LANGUAGE_TO_LOCALE[label]) # or _(label)
            wx.MessageBox(_('Restart application to change language definitely'), 'Info', wx.OK | wx.ICON_INFORMATION)
            profile_data.close()
        except IOError:
            wx.MessageBox(_('An error occured'), 'Error', wx.OK | wx.ICON_EXCLAMATION)
        event.Skip()
                        
    def on_close(self, event):
        if self._thread is not None and self._thread.isAlive():
            #self._thread.join(5)
            self._thread.interrupt.set()
        self.Destroy()
        #self.Close()
        event.Skip()
                    
                    
    def _setLocaleAndLanguage(self):
        locale.setlocale(locale.LC_ALL, "")
        
        #if system's language is available in translations set it otherwise set to default language (en_US)
        if gettext_windows.get_language()[0] in AVAILABLE_LOCALES:
            system_lang = gettext_windows.get_language()[0]
            if self._hasLanguage():
                os.environ['LANGUAGE'] = self._getLocale()
        else: 
            system_lang = DEFAULT_LANG
            os.environ['LANGUAGE'] = DEFAULT_LANG
            
        #for unix system
        try:
            self._translation = gettext.translation(self._appName, self._localeDir, system_lang)
            self._translation.install(unicode=True)
            #if exception has thrown then load translation for windows
        except IOError:
            gettext.bindtextdomain(self._appName, self._localeDir)
            gettext.textdomain(self._appName)
            gettext.install(self._appName, unicode=True)
            
    def _setProperLanguageMenubar(self):                   
        locale = self._getLocale()
        items = self.submenu_lang.GetMenuItems()
        if locale is not None:
            for item in items:
                if locale in LOCALE_TO_LANGUAGE and LOCALE_TO_LANGUAGE[locale] in AVAILABLE_LANGUAGES:
                    if item.GetLabel() == LOCALE_TO_LANGUAGE[locale]:
                        item.Check(check=True)
                        break;
                else:
                    if item.GetLabel() == _("English"):
                        item.Check(check=True)
                        break
        else:
            system_lang = os.getenv("Language")
            if system_lang in LOCALE_TO_LANGUAGE:
                for item in items:
                    if item.GetLabel() == LOCALE_TO_LANGUAGE[system_lang]:
                        item.Check(check=True)
                        break;
            else:
                for item in items:
                    if item.GetLabel() == _("English"):
                        item.Check(check=True)
                        break;  
            
                 
    def _getLocale(self):
        if self._hasLanguage():
            return open(self._languageFile, "r").read()
        else:
            return None

    def _toggleInputText(self, parent, disable=True):
        childrens = parent.GetChildren()
        for children in childrens:
            widget = children.GetWindow()
            if isinstance(widget, wx.TextCtrl):
                widget.SetEditable(disable)
        
    def _minutes_to_seconds(self, minutes):
        if minutes > 0:
            return minutes * 60
        return 30
        
    def _saveDataToFile(self, data):
        if not os.path.isdir(self._profileDir):
            os.makedirs(self._profileDir)
            
        try:
            profile_data = open(self._profileFile, "w")
            profile_data.write('::'.join(map(str, data)))
            profile_data.close()
        except IOError:
            wx.MessageBox(_('Directory is not writable or it does not exist'), 'Error', wx.OK | wx.ICON_EXCLAMATION)
        
    def _getProfileData(self):
        try:
            profile_data = open(self._profileFile, "r")
            data = profile_data.read().split("::")
            self.text_ctrl_1.SetValue(data[0])
            self.text_ctrl_2.SetValue(data[1])
            self.text_ctrl_4.SetValue(data[2])
            self.text_ctrl_3.SetValue(data[3])
            profile_data.close()
        except IOError:
            wx.MessageBox(_('Directory is not writable or it does not exist'), 'Error', wx.OK | wx.ICON_EXCLAMATION)

    def _hasEmptyInputText(self):
        empty = True
        childrens = self.grid_sizer_1.GetChildren()
        for children in childrens:
            widget = children.GetWindow()
            if isinstance(widget, wx.TextCtrl):
                if not widget.IsEditable():
                    continue
                elif widget.GetValue() != "":
                    empty = False
                else:
                    empty = True
        return empty
        
    def _hasLanguage(self):
        if os.path.exists(self._languageFile):
            return True
        return False
        
    def _isPlaySoundEnable(self):
        if self.checkbox_1.IsChecked():
            return True
        return False
        
    def _isDataToSave(self):
        if self.checkbox_3.IsChecked():
            return True
        return False
            

class BitbucketChecker(wx.App):
    def OnInit(self):
        wx.InitAllImageHandlers()
        frame_1 = BitbucketCheckerMyFrameEvent(None, -1, "")
        self.SetTopWindow(frame_1)
        frame_1.Show()
        return 1

if __name__ == "__main__":
    git = BitbucketChecker(0)
    git.MainLoop()
