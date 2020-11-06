#!/usr/bin/python3
# -*-coding:utf-8 -*-
"""Program to delete all dl.dctrad.fr urls in the forum."""

from utils.phpbb import PhpBB
from utils.settings import Settings

import re
from urllib.parse import urljoin
from utils.consts import Const

CFG_FILE = '.forum.cfg'
cfg_phpbb = 'dctrad'

ex1 = r"(\[url\=http:\/\/dl\.dctrad\.fr\/.*?\])(.*?)(\[\/url\])"
ex2 = r"\[url\]http://dl\.dctrad\.fr.*?\[\/url\]"
ex3 = r".*clique[rz]\ sur\ l.*?image[s]?\ pour .*?télécharger.*\n"
ex4 = r".*t[eé]l[eé]chargeable en cliquant sur l.*?image[s]?.*\n"
ex5 = r".*ou en cliquant sur l.*?image[s]?.*\n"
ex6 = r"\[size\=85\]Cliquez sur l.*?image[s]?\.\[\/size\]\n"
ex7 = r"(http:\/\/dl\.dctrad\.fr\/.*?)(\s|\[)"

regex1 = re.compile(ex1, re.IGNORECASE)
regex2 = re.compile(ex2, re.IGNORECASE)
regex3 = re.compile(ex3, re.IGNORECASE)
regex4 = re.compile(ex4, re.IGNORECASE)
regex5 = re.compile(ex5, re.IGNORECASE)
regex6 = re.compile(ex6, re.IGNORECASE)
regex7 = re.compile(ex7, re.IGNORECASE)


def replace_message(message):
    """Replace text using regex.

    Remove all dl.dctrad.url, and more.
    """
    temp = re.sub(regex1, r"\2", message)
    temp2 = re.sub(regex2, '', temp)
    temp3 = re.sub(regex3, '', temp2)
    temp4 = re.sub(regex4, '', temp3)
    temp5 = re.sub(regex5, '', temp4)
    temp6 = re.sub(regex6, '', temp5)
    # return temp6
    return re.sub(regex7, r"\2", temp6)


def nuke_oc(phpbb, f_id, p_id):
    """Get message (with his pid) and return new text."""
    origin = phpbb.get_post_editmode_content(f_id, p_id)
    new_mess = replace_message(origin)
    return origin, new_mess


if __name__ == '__main__':

    old_file = open("old.txt", "w")
    new_file = open("new.txt", "w")

    # Config
    cfg = Settings(CFG_FILE)
    if cfg.load(cfg_phpbb, Const.cfg_opts):
        phpbb = PhpBB(cfg.host)

        # phpbb.setUserAgent(cfg.user_agent)
        if phpbb.login(cfg.username, cfg.password):
            print('Login')

            mode = 0
            while True:
                mode = input(Const.MODE_CHOICE)
                if 1 <= int(mode) <= 2:
                    break
                else:
                    print("\nValeur incorrect")

            # Treat a topic
            if int(mode) == 1:
                f_id = input(Const.F_INPUT)
                topic_id = input(Const.T_INPUT)

                topic = 'viewtopic.php?f=%s&t=%s' % (f_id, topic_id)

                posts = phpbb.get_topic_posts_with_url(topic,
                                                       "http://dl.dctrad.fr",
                                                       int(cfg.max_count))

                # for p in posts[1:]:
                for p in posts:
                    # p_id = int(p[1])
                    print('{:>10} {}'.format(p.id, urljoin(cfg.host, 'viewtopic.php?p={id}#p{id}'.format(id=p.id))))  # noqa: E501
                    print('.........................................')
                    origin, new_mess = nuke_oc(phpbb, int(f_id), p.id)
                    # old_file.write(origin + '\n')
                    # old_file.write('------------------------------\n')
                    # new_file.write(new_mess + '\n')
                    # new_file.write('------------------------------\n')

                    phpbb.edit_post(int(f_id), p.id, new_mess)
                    print('-----------------------------------------')

                # phpbb.edit_post(12, 323626, new_message)

            # Treat a forum
            elif int(mode) == 2:
                while True:
                    choice = int(input(Const.SECTION_CHOICE))
                    if choice < 1 or choice > 10:
                        print("\nValeur incorrect")
                    else:
                        break

                try:
                    # Convert input number into forum section (rebirth, etc...)
                    # And read config for this forum section
                    forum_section = Const.SECTION_MAP[choice]
                    forum_dict = cfg.read_section("forums")
                    f_list = forum_dict[forum_section].split(",")
                except KeyError as e:
                    print(e)
                    print("Mauvaise valeur")
                    f_list = None
                    quit()

                reg = re.compile(r't=(?P<topic>\d+)')

                # f_list = cfg.phpbb_list.split(",")
                for f in f_list:
                    topics = phpbb.get_forum_topics(f)
                    f_id = f.split("&start")[0]
                    print("Processing")
                    for t in topics:
                        m = re.search(reg, t['url'])
                        topic_int = int(m.group('topic'))

                        if topic_int == 15370:
                            continue

                        topic = 'viewtopic.php?f=%s&t=%s' % (f_id, topic_int)

                        posts = phpbb.get_topic_posts_with_url(
                            topic,
                            "http://dl.dctrad.fr",
                            int(cfg.max_count)
                        )

                        # for p in posts[1:]:
                        for p in posts:
                            print('{:>10} {}'.format(p.id, urljoin(cfg.host, 'viewtopic.php?p={id}#p{id}'.format(id=p.id))))  # noqa: E501
                            print('.........................................')
                            origin, new_mess = nuke_oc(phpbb, int(f_id), p.id)
                            # old_file.write(origin + '\n')
                            # old_file.write('------------------------------\n')
                            # new_file.write(new_mess + '\n')
                            # new_file.write('------------------------------\n')

                            phpbb.edit_post(int(f_id), p.id, new_mess)
                            print('-----------------------------------------')

        Join = input('Appuyez sur une touche pour quitter\n')
        old_file.close()
        new_file.close()
