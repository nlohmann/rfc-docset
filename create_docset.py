#!/usr/bin/env python

import json
import sqlite3
import os
import glob
import re
from bs4 import BeautifulSoup
import lxml
import urllib

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
    <key>DashDocSetFamily</key>
    <string>dashtoc</string>
</dict>
</plist>''')

def create_index():
    conn = sqlite3.connect('rfc.docset/Contents/Resources/docSet.dsidx')
    c = conn.cursor()

    # create table
    c.execute('''CREATE TABLE IF NOT EXISTS searchIndex(id INTEGER PRIMARY KEY, name TEXT, type TEXT, path TEXT);''')

    # avoid duplicates
    c.execute('''CREATE UNIQUE INDEX IF NOT EXISTS anchor ON searchIndex (name, type, path);''')

    # add RFCs
    for rfc_file in glob.glob('html/*.html'):
        rfc_filename_base = os.path.basename(rfc_file)
        print 'processing %s...' % rfc_filename_base

        # add database entry; use title
        soup = BeautifulSoup(open(rfc_file), 'lxml')
        try:
            title = soup.title.string
            c.execute('''INSERT OR IGNORE INTO searchIndex(name, type, path) VALUES (?,?,?);''', (title, 'File', rfc_filename_base))
        except AttributeError:
            pass

        # add dash anchor to headings
        for span in soup.find_all('span'):
            if len(set(span.get('class', [])).intersection(set(['h2', 'h3', 'h4', 'h5', 'h6']))) > 0:
                span.insert(0, BeautifulSoup('<a name="//apple_ref/cpp/Shortcut/%s" class="dashAnchor"></a>' % urllib.quote(span.text.replace(u'\xa0', u' ')), 'lxml'))

        content = str(soup)

        # fix links
        content = re.sub(r'href="./([^"#]+)', r'href="./\1.html', content)
        # emphasize RFC2119 keywords
        content = re.sub(r'MUST', '<em>MUST</em>', content)
        content = re.sub(r'<em>MUST</em> NOT', '<em>MUST NOT</em>', content)
        content = re.sub(r'SHALL', '<em>SHALL</em>', content)
        content = re.sub(r'<em>SHALL</em> NOT', '<em>SHALL NOT</em>', content)
        content = re.sub(r'SHOULD', '<em>SHOULD</em>', content)
        content = re.sub(r'<em>SHOULD</em> NOT', '<em>SHOULD NOT</em>', content)
        content = re.sub(r'RECOMMENDED', '<em>RECOMMENDED</em>', content)
        content = re.sub(r'MAY', '<em>MAY</em>', content)
        content = re.sub(r'OPTIONAL', '<em>OPTIONAL</em>', content)
        content = re.sub(r'REQUIRED', '<em>REQUIRED</em>', content)

        open('rfc.docset/Contents/Resources/Documents/' + rfc_filename_base, 'w').write(content)

    conn.commit()

# scan index
prepare_docset()
create_index()
