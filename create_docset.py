#!/usr/bin/env python

import json
import sqlite3
import os
import glob
import shutil
import re

def prepare_docset():
    os.makedirs('rfc.docset/Contents/Resources/Documents')
    plist = open('rfc.docset/Contents/Info.plist', 'w')
    plist.write('''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleIdentifier</key>
    <string>rfc</string>
    <key>CFBundleName</key>
    <string>RFC</string>
    <key>DocSetPlatformFamily</key>
    <string>rfc</string>
    <key>isDashDocset</key>
    <true/>
    <key>DashDocSetFallbackURL</key>
    <string>https://tools.ietf.org/html/</string>
</dict>
</plist>''')

def copy_rfcs():
    for rfc_file in glob.glob('html/*.html'):
        rfc_original = open(rfc_file)
        rfc_output = open('rfc.docset/Contents/Resources/Documents/%s' % os.path.basename(rfc_file), 'w')
        for l in rfc_original.readlines():
            rfc_output.write(re.sub(r'href="./([^"#]+)', r'href="./\1.html', l))

def create_index():
    conn = sqlite3.connect('rfc.docset/Contents/Resources/docSet.dsidx')
    c = conn.cursor()

    # create table
    c.execute('''CREATE TABLE IF NOT EXISTS searchIndex(id INTEGER PRIMARY KEY, name TEXT, type TEXT, path TEXT);''')

    # avoid duplicates
    c.execute('''CREATE UNIQUE INDEX IF NOT EXISTS anchor ON searchIndex (name, type, path);''')

    # add RFCs
    for rfc_file in glob.glob('rfc.docset/Contents/Resources/Documents/*.html'):
        rfc_content = open(rfc_file).readlines()
        rfc_filename_base = os.path.basename(rfc_file)
        pattern = r'[^\n]*<title>([^\n]+)</title>[^\n]*'
        title = None
        for line in rfc_content:
            m = re.match(pattern, line)
            if m:
                title = m.group(1)
                break

        if title is not None:
            c.execute('''INSERT OR IGNORE INTO searchIndex(name, type, path) VALUES (?,?,?);''', (title, 'File', rfc_filename_base))

    conn.commit()

# scan index
prepare_docset()
copy_rfcs()
create_index()
