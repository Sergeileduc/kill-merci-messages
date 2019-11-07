#!/usr/bin/python3
# -*-coding:utf-8 -*-
"""Unit tests."""

import unittest
# import datetime
from utils.phpbb import PhpBB
from utils.post import Post, Page, Topic, Viewtopicurl
from tests.password import host, username, password
from tests.consts import (PID, REF_PID, FORUM, POST1, DELETE_POST1, PAGEURL,
                          VIEW_TOPIC1, MESSAGE_TOPIC1, AUTHOR1,
                          VIEW_TOPIC2, MESSAGE_TOPIC2)


class TestFonctionGet(unittest.TestCase):
    """Run unit tests."""

    # Chaque méthode dont le nom commence par 'test_'
    # est un test.
    def test_login(self):
        """Test PhpBB login()."""
        forum = PhpBB(host)
        return forum.login(username, password)

    def test_parse_url(self):
        """Test Viewtopicurl parse_url()."""
        viewtopicurl = Viewtopicurl(urlpart=VIEW_TOPIC2)
        viewtopicurl.parse_url()
        self.assertEqual((viewtopicurl.fid, viewtopicurl.tid), (190, 8467))

    def test_make_delete_url(self):
        """Test make_delete_req_url()."""
        url = POST1.make_delete_req_url(host)
        self.assertEqual(url, DELETE_POST1)

    # Le test le plus simple est un test d'égalité. On se
    # sert de la méthode assertEqual pour dire que l'on
    # s'attend à ce que les deux éléments soient égaux. Sinon
    # le test échoue.
    # self.assertEqual(myurl, result)

    def test_print_topic_title(self):
        """Test Topic print."""
        phpbb = PhpBB(host)
        # forum.setUserAgent(username)
        if phpbb.login(username, password):
            print(MESSAGE_TOPIC2)
            topic = Topic(phpbb, VIEW_TOPIC2)
            topic.print40()

    def test_get_post_html(self):
        """Test Post get_post_html()."""
        phpbb = PhpBB(host)
        if phpbb.login(username, password):
            post = Post(PID, phpbb=phpbb)
            post.get_post_html()

    def test_get_post_text(self):
        """Test Post.get_text()."""
        phpbb = PhpBB(host)
        if phpbb.login(username, password):
            post = Post(PID, phpbb=phpbb)
            post.get_text()
            self.assertEqual(post.text, REF_PID)

    def test_get_page_posts(self):
        """Test get_page_posts()."""
        # print('\n')
        # print("Today is : " + str(datetime.date.today()))
        forum = PhpBB(host)
        # forum.setUserAgent(username)
        if forum.login(username, password):
            print("Liste de posts")
            page = Page(PAGEURL, forum.browser.get_html(PAGEURL))
            pagelist = page.get_page_posts()
            pagelist.print_posts(1)

    def test_get_topic_posts(self):
        """Test get_topic_posts()."""
        phpbb = PhpBB(host)
        # forum.setUserAgent(username)
        if phpbb.login(username, password):
            print(MESSAGE_TOPIC1)
            posts = phpbb.get_topic_posts(VIEW_TOPIC1, 1000)
            posts.print_posts(n=1)

    def test_get_topic_posts_not_done(self):
        """Test get_topic_posts_not_done()."""
        forum = PhpBB(host)
        # forum.setUserAgent(username)
        if forum.login(username, password):
            print(MESSAGE_TOPIC1)
            nb_messages, posts = forum.get_topic_posts_not_done(
                VIEW_TOPIC1, 300, 1000)
            print(nb_messages)
            posts.print_posts(n=1)

    def test_get_page_posts_with_user(self):
        """Test get_page_posts_with_user()."""
        # print('\n')
        # print("Today is : " + str(datetime.date.today()))
        forum = PhpBB(host)
        # forum.setUserAgent(username)
        if forum.login(username, password):
            print("Liste de posts")
            page = Page(PAGEURL, forum.browser.get_html(PAGEURL))
            pagelist = page.get_page_posts_with_user()
            pagelist.print_posts_user(n=1)

    def test_get_topic_posts_with_user(self):
        """Test get_topic_posts_with_user()."""
        forum = PhpBB(host)
        # forum.setUserAgent(username)
        if forum.login(username, password):
            print(MESSAGE_TOPIC1)
            posts = forum.get_topic_posts_with_user(VIEW_TOPIC1, 1000)
            posts.print_posts_user(n=1)

    def test_select_user_list(self):
        """Test PostList select_user_list."""
        forum = PhpBB(host)
        # forum.setUserAgent(username)
        if forum.login(username, password):
            print(MESSAGE_TOPIC1)
            posts = forum.get_topic_posts_with_user(VIEW_TOPIC1, 1000)
            user_posts = posts.select_user_list(AUTHOR1)
            user_posts.print_posts_user()

    def test_get_forum_topics(self):
        """Test get_forum_topics()."""
        phpbb = PhpBB(host)
        # forum.setUserAgent(username)
        if phpbb.login(username, password):
            phpbb.get_forum_topics(FORUM)


# Ceci lance le test si on exécute le script
# directement.
if __name__ == '__main__':
    unittest.main()
