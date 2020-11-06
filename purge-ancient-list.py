#!/usr/bin/python3
# -*-coding:utf-8 -*-
"""Delete some messages in a phpbb forum topic."""

import sys
from collections import namedtuple
from utils.phpbb import PhpBB
from utils.post import PostList
from utils.settings import Settings
# from utils.consts import Const

CFG_FILE = ".forum.cfg"
CFG_FORUM = 'dctrad'


Topic = namedtuple('Topic', ['f', 't', 'desc'])
topic_list = [Topic(147, 15066, 'équipe_DC_Hors'),
              Topic(147, 7848, 'équipe_DC'),
              Topic(12, 14511, 'absences'),
              Topic(121, 13388, 'news_média'),
              Topic(119, 13387, "News Comics"),
              ]


try:
    # user = int(sys.argv[2])
    cfg = Settings(CFG_FILE)
    cfg_dict = cfg.read_section(CFG_FORUM)
    phpbb = PhpBB(cfg_dict['host'])
    # forum.setUserAgent(cfg.user_agent)
    if phpbb.login(cfg_dict['username'], cfg_dict['password']):
        print('Login')
        for top in topic_list:
            topic = f'viewtopic.php?f={top.f}&t={top.t}'
            post_list = phpbb.get_topic_posts(topic, int(cfg_dict['max_count']))  # noqa: E501
            n = len(post_list)
            print(f"{n} posts dans ce topic")
            print("===================")

            post_list = PostList([p for p in post_list[1:] if p.old > 365])

            print("===================")
            post_list.print_posts()
            print("===================")
            print("TOUS LES MESSAGES précédents seront SUPPRIMÉS !!!")
            print("Vous pouvez supprimer les messages ?")
            phpbb.delete_post_list(post_list)
    else:
        print('> Login failed')
    phpbb.logout()
    phpbb.close()
except KeyboardInterrupt:
    print("\nAu revoir")
    sys.exit(0)
