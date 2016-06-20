#!/usr/bin/env python

import os, json, signal, sys, urllib, urllib2, time, subprocess, hashlib
from random import *

CONFIG_FILE = 'config.json'

"""
Open and load a file at the json format
"""

def open_and_load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as config_file:
            return json.loads(config_file.read())
    else:
        print "File [%s] doesn't exist, aborting." % (CONFIG_FILE)
        sys.exit(1)

def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)

def say(txt, lang):
    t = txt.encode('utf-8')
    hash = hashlib.md5(txt.encode('ascii', 'replace') + " / " + lang).hexdigest()
    fname = "cache/" + hash + ".mp3"
    if ((os.path.isfile(fname) == False) or (os.stat(fname).st_size == 0)):
        urltts = config["tts"] + "?" + urllib.urlencode({'t':t, 'l':lang})
        print urltts
        urllib.urlretrieve(urltts, fname)
    subprocess.call([config["player"], fname])

def welcome(login, prenom):
    msg = ""
    mp3 = ""
    lang = "fr"
    jname = "custom/" + login + ".json"
    if (os.path.isfile(jname)):
        with open(jname, 'r') as custom_file:
            print jname
            try:
                j = json.loads(custom_file.read())
                if (m  in j.keys()):
                    j = j[m]
                print j
                if ("txt" in j.keys()):
                    msg = j["txt"]
                if ("lang" in j.keys()):
                    lang = j["lang"]
                if ("mp3" in j.keys()):
                    mp3 = j["mp3"]
            except:
                print "cannot load json"
    else:
        msg = choice(config["msgs"][m]) + " " + prenom
    if (msg != ""):
        print msg
        say(msg, lang)
    if (mp3 != ""):
        subprocess.call([config["player"], "mp3/" + mp3])
    
"""
Main
"""

if __name__ == "__main__":
    porte = sys.argv[1]
    m = sys.argv[2]
    signal.signal(signal.SIGINT, signal_handler)
    config = open_and_load_config()
    last_id = ""
    url = config["host"] + "?pid=" + config["doors"][porte] + "&eid=0"
    while 1:
        res = json.loads(urllib2.urlopen(url).read())
        if (res["id"] != last_id):
            welcome(res["login"], res["firstname"])
            last_id = res["id"]
        time.sleep(1)