#!/usr/bin/python3
# -*-coding:utf-8 -*-
"""Constants.

Rename it in consts.py
"""

from utils.post import Post

PID = "XXXX"  # message PID
REF_PID = ""  # message text

VIEW_TOPIC1 = "viewtopic.php?f=XXXX&t=YYYY"
MESSAGE_TOPIC1 = "Le titre du topic f=XXXX&t=YYYY est"

VIEW_TOPIC2 = "viewtopic.php?f=XXXX&t=YYYY"
MESSAGE_TOPIC2 = "Le titre du topic f=XXXX&t=YYYY est"

PAGEURL = "http://HOST/viewtopic.php?f=XXXX&t=YYYY&start=10"

FORUM = 151  # int

POST1 = Post(338068, "Text of message",
             "Human", user="Johndoe", fid=190)
DELETE_POST1 = "http://HOST/posting.php?mode=delete&f=190&p=338068"
