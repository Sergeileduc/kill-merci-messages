#!/usr/bin/python3
# -*-coding:utf-8 -*-

import re
from urllib.parse import urljoin

from utils.phpbb import PhpBB
from utils.settings import Settings
from utils.consts import Const

cfg_file = '.dctrad.cfg'
cfg_forum = 'dctrad'

ex1 = (r"\[url=https?\:\/\/www\.hostingpics\.net.*?\]"
       r"\[img\].*?hostingpics\.net.*?\[\/img\]\[\/url\]")
ex2 = r"\[img\]https?\:\/\/img\d*\.hostingpics\.net.*?\[\/img\]"

regex1 = re.compile(ex1)
regex2 = re.compile(ex2)


def replace_message(message):
    temp = re.sub(regex1, "IMAGE", message)
    return re.sub(regex2, 'IMAGE', temp)


def nuke_oc(forum, fid, pid):
    mess = forum.get_post_editmode_content(fid, pid)
    new_mess = replace_message(origin)
    return mess, new_mess


if __name__ == '__main__':

    old_file = open("old.txt", "w")
    new_file = open("new.txt", "w")

    # Config
    cfg = Settings(cfg_file)
    if cfg.load(cfg_forum, Const.cfg_opts):
        phpbb = PhpBB(cfg.host)
        max = int(cfg.max_count)

        if phpbb.login(cfg.username, cfg.password):
            print('Login')

            mode = 0
            while True:
                mode = input('Que voulez-vous faire ?\n'
                             '1- Traiter un seul topic\n'
                             '2- Traiter un sous forum entier '
                             '(DC Rebirth / Marvel / etc...)\n'
                             'Réponse : 1 ou 2\n')
                if 1 <= int(mode) <= 2:
                    break
                else:
                    print("\nValeur incorrect")

            if int(mode) == 1:
                f_id = input(Const.F_INPUT)
                topic_id = input(Const.T_INPUT)

                topic = 'viewtopic.php?f=%s&t=%s' % (f_id, topic_id)

                posts = phpbb.get_posts_with_hosting(topic, max)
                for p in posts:
                    p_id = int(p[1])
                    print('{:>10} {}'.format(p[1], urljoin(cfg.host, p[0])))
                    print('.........................................')
                    origin, new_mess = nuke_oc(phpbb, int(f_id), int(p[1]))
                    # old_file.write(origin + '\n')
                    # old_file.write('------------------------------\n')
                    # new_file.write(new_mess + '\n')
                    # new_file.write('------------------------------\n')
                    phpbb.edit_post(int(f_id), p_id, new_mess)
                    print('-----------------------------------------')
                # forum.edit_post(12, 323626, new_message)

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

                # f_list = cfg.forum_list.split(",")
                for f in f_list:
                    topics = phpbb.get_forum_topics(f)
                    f_id = f.split("&start")[0]
                    for t in topics:
                        m = re.search(reg, t)
                        topic_int = int(m.group('topic'))

                        topic = 'viewtopic.php?f=%s&t=%s' % (f_id, topic_int)

                        posts = phpbb.get_posts_with_hosting(topic, max)
                        for p in posts:
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
                            phpbb.edit_post(int(f_id), p_id, new_mess)
                            print('-----------------------------------------')
        Join = input('Appuyez sur une touche pour quitter\n')
        old_file.close()
        new_file.close()
        phpbb.logout()
        phpbb.close()
