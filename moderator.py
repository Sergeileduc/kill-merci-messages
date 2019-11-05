#!/usr/bin/python3
# -*-coding:utf-8 -*-
"""Check if words appear in a forum."""

# import datetime
# import re
import sqlite3
import sys

from sqlite_utils import Database
from sqlite_utils.db import NotFoundError

from utils import tools  # My own code in utils folder
from utils.consts import Const
from utils.phpbb import PhpBB
from utils.post import Viewtopicurl
from utils.settings import Settings

CFG_FILE = ".dctrad.cfg"
DB_FILE = ".modo.db"
CFG_FORUM = "dctrad_modo"
DB_TABLE = "modo"


try:
    # Check or create database file
    db = Database(DB_FILE)
    try:
        table = db.table(DB_TABLE).create({"topic": int, "posts": int},
                                          pk="topic")
    except sqlite3.OperationalError:
        # Table already exists
        table = db[DB_TABLE]
    # Config
    cfg = Settings(CFG_FILE)
    if cfg.load(CFG_FORUM, Const.cfg_opts_modo):
        phpbb = PhpBB(cfg.host)
        words_list = tools.configsplit(cfg.keywords)
    else:
        sys.exit(1)

    # forum.setUserAgent(cfg.user_agent)
    if phpbb.login(cfg.username, cfg.password):
        print("Login")
        # f_id = cfg.forum_id.split("&start")[0]
        mode = 0
        while True:
            mode = input(Const.MODE_CHOICE2)
            if 1 <= int(mode) <= 4:
                break
            else:
                print("\nValeur incorrect")

        if int(mode) == 1:
            f_id = input(Const.F_INPUT)
            topic_id = input(Const.T_INPUT)
            try:
                posts_done = table.get(topic_id)["posts"]
            except NotFoundError:
                posts_done = 0

            # topic = 'viewtopic.php?f=%s&t=%s' % (f_id, topic_id)
            url_part = f"viewtopic.php?f={f_id}&t={topic_id}"
            topic = Viewtopicurl(urlpart=url_part, fid=f_id, tid=topic_id)
            nb_posts, postlist = phpbb.get_topic_posts_not_done(
                topic.urlpart, posts_done, int(cfg.max_count))
            target = postlist.search_words(words_list)
            print("Target list")
            target.print_posts_full()
            # target.log_posts(logfile)
            if len(target) == 0:
                print("Nothing to do in this topic")
            else:
                print(f"Vous pouvez vérifier {len(target)} messages")
                # print("Processing")
                # phpbb.delete_post_list(target)
            # Put number of posts in the database
            table.upsert({'topic': topic_id,
                          'posts': nb_posts - len(target)})

        # Treat a forum
        elif int(mode) == 2:
            while True:
                choice = input(Const.SECTION_CHOICE2)
                if int(choice) < 1 or int(choice) > 3:
                    print("\nValeur incorrect")
                else:
                    break
            # Regex for finding topic id in string 'viewtopic.......'
            # reg = re.compile(r't\=(?P<topic>\d+)')
            f_list = ()
            if int(choice) == 1:
                f_list = cfg.general.split(",")
            elif int(choice) == 2:
                f_list = cfg.comics.split(",")
            elif int(choice) == 3:
                f_list = cfg.mediass.split(",")
            else:
                print("Mauvaise valeur")
                quit()

            # f_list = cfg.forum_list.split(",")
            for f in f_list:
                count = 0
                # viewtopics structure contain urlpart, fid and tid
                viewtopics = phpbb.get_forum_view_topics(f)
                # f_id = f.split("&start")[0]

                # v contains viewtopic url, and fid and tid
                for topic in viewtopics:
                    # m = re.search(reg, t)
                    # topic_int = int(m.group('topic'))

                    # Read number of posts already done, in the database
                    try:
                        posts_done = table.get(topic.tid)["posts"]
                    except NotFoundError:
                        posts_done = 0

                    print("===========================")
                    # Retrieve list of Post objects (not already processed)
                    nb_posts, postlist = phpbb.get_topic_posts_not_done(
                        topic.urlpart,      # viewtopic.php?f=XX&t=XXXX
                        posts_done,         # int
                        int(cfg.max_count))

                    if posts_done == nb_posts:
                        if count < 6:
                            print("Skipping")
                            count += 1
                        else:
                            print("Ce sous-forum a déjà été vérifié. Suivant.")
                            break
                    elif posts_done < nb_posts:
                        target = postlist.search_words(words_list)
                        if len(target) == 0:
                            pass
                            print("Nothing to do in this topic")
                        else:
                            print("Target list")
                            target.print_posts_full()
                            # target.log_posts(logfile)
                            print(f"Vous pouvez vérifier {len(target)} "
                                  "messages")
                            # print("Processing")
                            # phpbb.delete_post_list(target)
                        table.upsert({'topic': topic.tid,
                                      'posts': nb_posts - len(target)})

        elif int(mode) == 3:
            table.drop()
            print("La base de donnée a été nettoyée.")

        elif int(mode) == 4:
            topic_id = input(Const.T_INPUT)
            table.delete(topic_id)
            print("Ce topic sera considéré comme"
                  "n'ayant jamais été nettoyé.")

        phpbb.logout()
        phpbb.close()
    # If forum.login fails
    else:
        print("> Login failed")
    Join = input("Appuyez sur une touche pour quitter\n")
except KeyboardInterrupt:
    print("\nAu revoir")
    sys.exit(0)
# finally:
#     logfile.close()
