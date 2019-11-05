#!/usr/bin/python3
# -*-coding:utf-8 -*-
"""This program deletes dummy messages "merci" in a phpbb forum."""

import sys
import datetime
from sqlite_utils import Database
from sqlite_utils.db import NotFoundError
import sqlite3
from utils.phpbb import PhpBB
from utils.settings import Settings
from utils import tools
from utils.consts import Const
from utils.post import Viewtopicurl

CFG_FILE = ".dctrad.cfg"
DB_FILE = ".topics.db"
CFG_FORUM = "dctrad"
DB_TABLE = "purged"


try:
    # Check or create database file
    db = Database(DB_FILE)
    try:
        table = db.table(DB_TABLE).create({"topic": int, "posts": int},
                                          pk="topic")
    except sqlite3.OperationalError:
        # Table already exists
        table = db[DB_TABLE]

    # Log
    logfile = open(".merci_logfile.txt", "a+")
    logfile.write(str(datetime.datetime.now()) + "\n")

    # Config
    cfg = Settings(CFG_FILE)
    cfg_dict = cfg.read_section(CFG_FORUM)
    forum_dict = cfg.read_section("forums")
    phpbb = PhpBB(cfg_dict["host"])
    regex1, regex2, regex3 = tools.compute_regex(cfg)

    if phpbb.login(cfg_dict["username"], cfg_dict["password"]):
        print("Login")

        mode = 0
        while True:
            mode = int(input(Const.MODE_CHOICE))
            if 1 <= mode <= 4:
                break
            else:
                print("\nValeur incorrect")

        # One topic
        if mode == 1:
            f_id = int(input(Const.F_INPUT))
            topic_id = int(input(Const.T_INPUT))
            try:
                posts_done = table.get(topic_id)["posts"]
            except NotFoundError:
                posts_done = 0

            # topic = 'viewtopic.php?f=%s&t=%s' % (f_id, topic_id)
            urlpart = f"viewtopic.php?f={f_id}&t={topic_id}"
            topic = Viewtopicurl(urlpart=urlpart, fid=f_id, tid=topic_id)
            nb_posts, postlist = phpbb.get_topic_posts_not_done(
                topic.urlpart, posts_done, int(cfg_dict["max_count"])
            )
            target = postlist.merci_list(regex1, regex2, regex3)
            print("Target list")
            target.print_posts()
            target.log_posts(logfile)
            if len(target) == 0:
                print("Nothing to do in this topic")
            else:
                print(f"Vous pouvez supprimer {len(target)} messages")
                # Join = input('Voulez-vous continuer ? '
                #              '(Seuls les posts humains '
                #              'seront supprimés) '
                #              '(y/n) ?\n')
                # if Join.lower() == 'yes' or Join.lower() == 'y':
                print("Processing")
                phpbb.delete_post_list(target)
                # else:
                #     print ("Ok, Exit")
            # Dump number of posts in the database
            table.upsert({'topic': topic_id,
                          'posts': nb_posts - len(target)})

        # Treat a forum
        elif mode == 2:
            while True:
                choice = int(input(Const.SECTION_CHOICE))
                if choice < 1 or choice > 10:
                    print("\nValeur incorrect")
                else:
                    break
            # Regex for finding topic id in string 'viewtopic.......'
            # reg = re.compile(r't\=(?P<topic>\d+)')

            try:
                # Convert input number into forum section (rebirth, etc...)
                # And read config for this forum section
                forum_section = Const.SECTION_MAP[choice]
                f_list = forum_dict[forum_section].split(",")
            except KeyError:
                print("Mauvaise valeur")
                f_list = None
                quit()

            for f in f_list:
                count = 0
                # viewtopics structure contain urlpart, fid and tid
                viewtopics = phpbb.get_forum_view_topics(f)

                for topic in viewtopics:

                    # Read number of posts already done, in the database
                    try:
                        posts_done = table.get(topic.tid)["posts"]
                    except NotFoundError:
                        posts_done = 0

                    print("===========================")
                    # Retrieve list of Post objects (not already processed)
                    nb_posts, postlist = phpbb.get_topic_posts_not_done(
                        topic.urlpart,  # viewtopic.php?f=XX&t=XXXX
                        posts_done,  # int
                        int(cfg_dict["max_count"]),
                    )

                    if posts_done == nb_posts:
                        if count < 6:
                            print("Skipping")
                            count += 1
                        else:
                            print("Déjà été nettoyé. Suivant.")
                            break
                    elif posts_done < nb_posts:
                        target = postlist.merci_list(regex1, regex2, regex3)
                        if len(target) == 0:
                            pass
                            print("Nothing to do in this topic")
                        else:
                            print("Target list")
                            target.print_posts()
                            target.log_posts(logfile)
                            print(f"Vous pouvez supprimer {len(target)} "
                                  "messages")
                            # Join = input(
                            #  'Voulez-vous continuer ? '
                            #  '(Seuls les posts humains seront supprimés)'
                            #  ' (y/n) ?\n')
                            # if Join.lower() == 'yes' \
                            #         or Join.lower() == 'y':
                            print("Processing")
                            phpbb.delete_post_list(target)
                            # else:
                            #     print ("Ok, pass")
                        table.upsert({'topic': topic.tid,
                                      'posts': nb_posts - len(target)})

        # Forget all (wipe database)
        elif mode == 3:
            table.drop()
            print("La base de donnée a été nettoyée.")

        # Forget one topic
        elif mode == 4:
            topic_id = int(input(Const.T_INPUT))
            table.delete(topic_id)
            print("Ce topic sera considéré comme"
                  "n'ayant jamais été nettoyé.")

        # Log out
        phpbb.logout()
        phpbb.close()
        logfile.close()

    else:  # If forum.login fails
        print("> Login failed")
        logfile.close()
    Join = input("Appuyez sur une touche pour quitter\n")
except KeyboardInterrupt:
    print("\nAu revoir")
    sys.exit(0)
