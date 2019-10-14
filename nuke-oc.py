#!/usr/bin/python3
# -*-coding:utf-8 -*-
"""Program to delete all dl.dctrad.fr urls in the forum."""

from utils.phpbb import PhpBB
from utils.settings import Settings

import re
from urllib.parse import urljoin
from utils.consts import Const

CFG_FILE = '.dctrad.cfg'
cfg_phpbb = 'dctrad'

ex1 = r"(\[url\=http:\/\/dl\.dctrad\.fr\/.*?\])(.*?)(\[\/url\])"
ex2 = r"\[url\]http://dl\.dctrad\.fr.*?\[\/url\]"
ex3 = r".*clique[rz]\ sur\ l.*?image[s]?\ pour .*?télécharger.*\n"
ex4 = r".*t[eé]l[eé]chargeable en cliquant sur l.*?image[s]?.*\n"
ex5 = r".*ou en cliquant sur l.*?image[s]?.*\n"
ex6 = r"\[size\=85\]Cliquez sur l.*?image[s]?\.\[\/size\]\n"

regex1 = re.compile(ex1)
regex2 = re.compile(ex2)
regex3 = re.compile(ex3, re.IGNORECASE)
regex4 = re.compile(ex4, re.IGNORECASE)
regex5 = re.compile(ex5, re.IGNORECASE)
regex6 = re.compile(ex6, re.IGNORECASE)


def replace_message(message):
    """Replace text using regex.

    Remove all dl.dctrad.url, and more.
    """
    temp = re.sub(regex1, r"\2", message)
    temp2 = re.sub(regex2, '', temp)
    temp3 = re.sub(regex3, '', temp2)
    temp4 = re.sub(regex4, '', temp3)
    temp5 = re.sub(regex5, '', temp4)
    return re.sub(regex6, '', temp5)


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

            if int(mode) == 1:
                f_id = input(Const.F_INPUT)
                topic_id = input(Const.T_INPUT)

                topic = 'viewtopic.php?f=%s&t=%s' % (f_id, topic_id)

                posts = phpbb.get_posts_with_oc_links(topic,
                                                      int(cfg.max_count))
                for p in posts[1:]:
                    p_id = int(p[1])
                    print('{:>10} {}'.format(p[1], urljoin(cfg.host, p[0])))
                    print('.........................................')
                    origin, new_mess = nuke_oc(phpbb, int(f_id), int(p[1]))
                    old_file.write(origin + '\n')
                    old_file.write('------------------------------\n')
                    new_file.write(new_mess + '\n')
                    new_file.write('------------------------------\n')
                    # print('-----------------------------------------')

                    # phpbb.edit_post(int(f_id), p_id, new_mess)

                # phpbb.edit_post(12, 323626, new_message)

            # Treat a forum
            elif int(mode) == 2:
                while True:
                    choice = input(Const.SECTION_CHOICE)
                    if int(choice) < 1 or int(choice) > 10:
                        print("\nValeur incorrect")
                    else:
                        break
                f_list = ()
                if int(choice) == 1:
                    f_list = cfg.rebirth.split(",")
                elif int(choice) == 2:
                    f_list = cfg.new52.split(",")
                elif int(choice) == 3:
                    f_list = cfg.dcclassic.split(",")
                elif int(choice) == 4:
                    f_list = cfg.dchc.split(",")
                elif int(choice) == 5:
                    f_list = cfg.vertigo.split(",")
                elif int(choice) == 6:
                    f_list = cfg.marvel.split(",")
                elif int(choice) == 7:
                    f_list = cfg.indes.split(",")
                elif int(choice) == 8:
                    f_list = cfg.divers.split(",")
                elif int(choice) == 9:
                    f_list = cfg.all_topics.split(",")
                elif int(choice) == 10:
                    f_list = cfg.test_topics.split(",")
                else:
                    print("Mauvaise valeur")
                    quit()

                reg = re.compile(r't=(?P<topic>\d+)')

                # f_list = cfg.phpbb_list.split(",")
                for f in f_list:
                    topics = phpbb.get_forum_topics(f)
                    f_id = f.split("&start")[0]
                    for t in topics:
                        m = re.search(reg, t)
                        topic_int = int(m.group('topic'))

                        topic = 'viewtopic.php?f=%s&t=%s' % (f_id, topic_int)

                        posts = phpbb.get_posts_with_oc_links(
                            topic, int(cfg.max_count))
                        for p in posts[1:]:
                            p_id = int(p[1])
                            print('{:>10} {}'.format(p[1],
                                                     urljoin(cfg.host, p[0])))
                            # print('.........................................')
                            origin, new_mess = nuke_oc(phpbb,
                                                       int(f_id),
                                                       int(p[1]))
                            # old_file.write(origin + '\n')
                            # old_file.write('------------------------------\n')
                            # new_file.write(new_mess + '\n')
                            # new_file.write('------------------------------\n')
                            # phpbb.edit_post(int(f_id), p_id, new_mess)
                            print('-----------------------------------------')
        Join = input('Appuyez sur une touche pour quitter\n')
        old_file.close()
        new_file.close()
