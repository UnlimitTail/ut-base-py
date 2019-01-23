# -*- coding: utf-8 -*-

import re

def clean_html(raw_html, pattern = '<.*?>'):
    cleanr = re.compile(pattern)
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext