#!/usr/bin/python3
# -*-coding:utf-8 -*-
"""This program deletes dummy messages "merci" in a phpbb forum."""

import json
from utils.phpbb import PhpBB
from utils.settings import Settings
from bs4 import BeautifulSoup

CFG_FILE = ".forum.cfg"
CFG_FORUM = "dctrad"
URL = "https://www.dctrad.fr/app.php/picsbox/image"

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"}  # noqa: E501

# Config
cfg = Settings(CFG_FILE)
cfg_dict = cfg.read_section(CFG_FORUM)
forum_dict = cfg.read_section("forums")
phpbb = PhpBB(cfg_dict["host"])

files = {'file': open('12.jpg', 'rb')}

if phpbb.login(cfg_dict["username"], cfg_dict["password"]):
    print("Login")
    for c in phpbb.browser.list_cookies():
        print(c)
    sid = phpbb._get_sid()
    print(f"post login get with sid {sid}")
    r1 = phpbb.browser.session.get(f"https://dctrad.fr/index.php?sid={sid}")
    print(r1.status_code)
    for c in phpbb.browser.list_cookies():
        print(c)
    print("simple get")
    r2 = phpbb.browser.session.get("https://www.dctrad.fr/viewtopic.php?p=396660")  # noqa: E501
    for c in phpbb.browser.list_cookies():
        print(c)
    print("POST")
    r = phpbb.browser.session.post(URL,
                                   headers=headers,
                                   files=files)
    print("endPOST")
    # for c in phpbb.browser.list_cookies():
    #     print(c)
    soup = BeautifulSoup(r.text, 'html.parser')
    print(r.status_code)
    headers_json = json.dumps(dict(r.headers), indent=2)
    print(headers_json)

    print("-------------------------------------------------------------")
    # print(soup.prettify())
    print("-------------------------------------------------------------")
