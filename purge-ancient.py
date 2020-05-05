#!/usr/bin/python3
# -*-coding:utf-8 -*-
"""Delete some messages in a phpbb forum topic."""

import sys
from utils.phpbb import PhpBB
from utils.post import PostList
from utils.settings import Settings
from utils.consts import Const

CFG_FILE = ".dctrad.cfg"
CFG_FORUM = 'dctrad'


try:
    # user = int(sys.argv[2])
    cfg = Settings(CFG_FILE)
    cfg_dict = cfg.read_section(CFG_FORUM)
    phpbb = PhpBB(cfg_dict['host'])
    x = 0
    y = -1
    # forum.setUserAgent(cfg.user_agent)
    if phpbb.login(cfg_dict['username'], cfg_dict['password']):
        print('Login')
        f_id = input(Const.F_INPUT)
        topic_id = input(Const.T_INPUT)
        topic = f'viewtopic.php?f={f_id}&t={topic_id}'
        post_list = phpbb.get_topic_posts(topic, int(cfg_dict['max_count']))
        n = len(post_list)
        print(f"{n} posts dans ce topic")
        print("===================")

        post_list = PostList([p for p in post_list[1:] if p.old > 365])

        print("===================")
        post_list.print_posts()
        print("===================")
        print("TOUS LES MESSAGES précédents seront SUPPRIMÉS !!!")
        print("Vous pouvez supprimer les messages ?")
        Join = input('y/n ?\n')
        if Join.lower() == 'yes' or Join.lower() == 'y':
            Join = input('Tapez votre mot de passe\n')
            if Join == cfg_dict['password']:
                print("YOUHOU")
                phpbb.delete_post_list(post_list)
    else:
        print('> Login failed')
    phpbb.logout()
    phpbb.close()
except KeyboardInterrupt:
    print("\nAu revoir")
    sys.exit(0)
