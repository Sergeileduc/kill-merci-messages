#!/usr/bin/python3
# -*-coding:utf-8 -*-
"""Purge old messages in 'Sorties VO'."""

import sys
from utils.phpbb import PhpBB
from utils.settings import Settings

CFG_FILE = '.dctrad.cfg'
cfg_forum = 'dctrad'
targeted_user = 'Sergeileduc'

try:
    cfg = Settings(CFG_FILE)
    cfg_dict = cfg.read_section('dctrad')
    phpbb = PhpBB(cfg_dict['host'])

    if phpbb.login(cfg_dict['username'], cfg_dict['password']):
        print('Login')
        f_id = 139
        viewtopics = phpbb.get_forum_view_topics(f_id)
        for t in viewtopics[5:10]:
            postlist = phpbb.get_user_topic_posts(t.urlpart,
                                                  int(cfg_dict['max_count']))
            target = postlist.select_user_list(targeted_user)
            target.print_posts_user()

            phpbb.delete_post_list(target)
        else:
            print('> Login failed')
        phpbb.logout()
        phpbb.close()
except KeyboardInterrupt:
    print("\nAu revoir")
    sys.exit(0)
