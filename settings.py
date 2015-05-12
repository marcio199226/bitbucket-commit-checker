#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, gettext

_ = gettext.gettext

OS_WINDOWS = (sys.platform == 'win32')

DEFAULT_LANG = "en_US"

LOCALE_DIR = os.getcwd() + "\\data\\locale\\"
 
AVAILABLE_LANGUAGES = [ "Polish", "Italian", "English" ]

l = [ "Polish", "Italian", "English" ]
                      
AVAILABLE_LOCALES = [ "en_US", "it_IT", "pl_PL" ]

LOCALE_TO_LANGUAGE = {
                        "pl_PL": "Polish",
                        "it_IT": "Italian",
                        "en_US": "English"
                     }
                     
LANGUAGE_TO_LOCALE = {
                        "Polish": "pl_PL",
                        "Italian": "it_IT",
                        "English": "en_US"
                     }                    
       
#change all keys or values to respective translated values       
def translate_all_languages_data():
    loc_to_lang_tmp = dict([(loc, _(lang)) for loc,lang in LOCALE_TO_LANGUAGE.iteritems()])
    LOCALE_TO_LANGUAGE.update(loc_to_lang_tmp)
    lang_to_loc_tmp = dict([(_(lang), loc) for lang, loc in LANGUAGE_TO_LOCALE.iteritems()])
    LANGUAGE_TO_LOCALE.update(lang_to_loc_tmp)
    for i, lang in enumerate(AVAILABLE_LANGUAGES):
        AVAILABLE_LANGUAGES[i] = _(lang)
        
def translate_available_languages():
    for i, lang in enumerate(AVAILABLE_LANGUAGES):
        AVAILABLE_LANGUAGES[i] = _(lang)