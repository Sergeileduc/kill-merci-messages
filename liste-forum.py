#!/usr/bin/python3
# -*-coding:utf-8 -*-
"""List all topics in phpbb forum."""

import sys
from utils.phpbb import PhpBB
from utils.settings import Settings
from configparser import NoOptionError

CFG_FILE = '.dctrad.cfg'
CFG_FORUM = 'dctrad'

try:
    # Config
    cfg = Settings(CFG_FILE)
    cfg_dict = cfg.read_section('dctrad')
    forum_dict = cfg.read_section('forums')
    print('Config loaded')

    # Log in
    phpbb = PhpBB(cfg_dict['host'])
    phpbb.login(cfg_dict['username'], cfg_dict['password'])
    f_list = forum_dict['all_topics'].split(",")

    for f in f_list:
        phpbb.get_forum_topics(f)

    Join = input('Appuyez sur une touche pour quitter\n')
    phpbb.logout()
    phpbb.close()

except KeyboardInterrupt:
    print("\nAu revoir")
    sys.exit(0)
except NoOptionError as e:
    print(e)
