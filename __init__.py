#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx, os, time, Queue, winsound, gettext, gettext_windows, locale, sys
#sys.path.append(os.getcwd() + "\\modal\\")
#from ModalLanguage import *
from modal.ModalLanguage import *
from MyFrame import MyFrame
from BitBucketApi import *
from threading import Thread, Event

gettext_windows.setup_env()