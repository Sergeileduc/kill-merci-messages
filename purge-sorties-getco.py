#!/usr/bin/python3
# -*-coding:utf-8 -*-
"""Remove getcomics url in messages."""

import sys
import re
from utils.phpbb import PhpBB
from utils.settings import Settings

cfg_file = '.dctrad.cfg'
cfg_forum = 'dctrad'
targeted_user = 'Sergeileduc'

reg = r"\[url=https\:\/\/getcomics\.info\/.*?\](?P<comic>.*?)\[\/url\]"
regex1 = re.compile(reg)


def replace_message(message):
    """Replace text using regex.

    Removes [url=htts://getcomics.....] bbcodes.
    """
    return re.sub(regex1, r"\g<comic>", message)


try:
    # user = int(sys.argv[2])
    cfg = Settings(cfg_file)
    cfg_dict = cfg.read_section(cfg_forum)
    phpbb = PhpBB(cfg_dict['host'])
    # forum.setUserAgent(cfg.user_agent)
    if phpbb.login(cfg_dict['username'], cfg_dict['password']):
        print('Login')
        f_id = 139
        viewtopics = phpbb.get_forum_view_topics(f_id)
        for v in viewtopics[3:10]:
            postlist = phpbb.get_user_topic_posts(v.urlpart,
                                                  int(cfg_dict['max_count']))
            target = postlist.select_user_list(targeted_user)
            target.print_posts_user()
            for p in target:
                txt = phpbb.get_post_editmode_content(f_id, p.id)
                txt2 = replace_message(txt)

                print("============")
                phpbb.edit_post(f_id, p.id, txt2)

    else:
        print('> Login failed')
    phpbb.logout()
    phpbb.close()
except KeyboardInterrupt:
    print("\nAu revoir")
    sys.exit(0)
