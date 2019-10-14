#!/usr/bin/python3
# -*-coding:utf-8 -*-
"""Delete some messages in a phpbb forum topic."""

import sys
from utils.phpbb import PhpBB
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
        while x > n or x < 1:
            x = int(input(f"Nomre de messages à conserver au début "
                          f"(entre 1 et {n}) : "))
        print(f"{x} messages seront conservés au début")
        while y > (n - x) or y < 0:
            y = int(input(f"Nombre de messages à conserver à la fin "
                          f"(entre 0 et {n-x}) : "))
        print(f"{y} messages seront conservés à la fin")
        del post_list[:x]
        if y != 0:
            del post_list[-y:]
        print("===================")
        post_list.print_posts()
        print("===================")
        print("TOUS LES MESSAGES situés au milieu "
              "(ni au début, ni à la fin) seront "
              "DÉFINITIVEMENT SUPPRIMÉS !!!")
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
