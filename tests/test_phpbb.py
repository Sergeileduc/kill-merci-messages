#!/usr/bin/python3
# -*-coding:utf-8 -*-
"""Unit tests."""

import pytest
# import datetime
from utils.phpbb import PhpBB
from utils.post import Post, Page, Topic, Viewtopicurl
from tests.password import host, username, password
from tests.consts import (PID, REF_PID, FORUM, POST1, DELETE_POST1, PAGEURL,
                          VIEW_TOPIC1, MESSAGE_TOPIC1, AUTHOR1,
                          VIEW_TOPIC2, MESSAGE_TOPIC2,
                          VIEW_TOPIC3, MESSAGE_TOPIC3, AUTHOR3)


class TestTools:
    """The simpler tests for some tools."""
    def test_parse_url(self):
        """Test Viewtopicurl parse_url()."""
        viewtopicurl = Viewtopicurl(urlpart=VIEW_TOPIC2)
        viewtopicurl.parse_url()
        assert (viewtopicurl.fid, viewtopicurl.tid) == (190, 8467)

    def test_make_delete_url(self):
        """Test make_delete_req_url()."""
        url = POST1.make_delete_req_url(host)
        assert url == DELETE_POST1


def test_login():
    """Test PhpBB login()."""
    forum = PhpBB(host)
    assert forum.login(username, password)
    forum.logout()


class TestForumConnectedUser:
    """Class for all tests that required being logged in."""

    @pytest.fixture(scope="class", name='forum')
    def loggedin_forum(self):
        """Connect to forum before testing, disconnect after."""
        # Setup : log in forum
        forum = PhpBB(host)
        forum.login(username, password)
        print("Pytest fixture : Logging in forum")
        yield forum
        # this is where the testing happens
        # Teardown : log out forum
        forum.logout()
        print("Pytest fixture : Logging out forum")

    def test_print_topic_title(self, forum):
        """Test Topic print."""
        print(MESSAGE_TOPIC2)
        topic = Topic(forum, VIEW_TOPIC2)
        topic.print40()

    def test_get_post_html(self, forum):
        """Test Post get_post_html()."""
        post = Post(PID, phpbb=forum)
        post.get_post_html()

    def test_get_post_text(self, forum):
        """Test Post.get_text()."""
        post = Post(PID, phpbb=forum)
        post.get_text()
        assert post.text == REF_PID

    def test_get_page_posts(self, forum):
        """Test get_page_posts()."""
        # print('\n')
        # print("Today is : " + str(datetime.date.today()))
        print("Liste de posts")
        page = Page(PAGEURL, forum.browser.get_html(PAGEURL))
        pagelist = page.get_page_posts()
        pagelist.print_posts(1)

    def test_get_topic_posts(self, forum):
        """Test get_topic_posts()."""
        print(MESSAGE_TOPIC3)
        posts = forum.get_topic_posts(VIEW_TOPIC3, 1000)
        posts.print_posts(n=1)

    def test_get_topic_posts_not_done(self, forum):
        """Test get_topic_posts_not_done()."""
        print(MESSAGE_TOPIC3)
        nb_messages, posts = forum.get_topic_posts_not_done(
            VIEW_TOPIC3, 11, 1000)
        print(nb_messages)
        posts.print_posts(n=1)

    def test_get_page_posts_with_user(self, forum):
        """Test get_page_posts_with_user()."""
        print("Liste de posts")
        page = Page(PAGEURL, forum.browser.get_html(PAGEURL))
        pagelist = page.get_page_posts_with_user()
        pagelist.print_posts_user(n=1)

    def test_get_topic_posts_with_user(self, forum):
        """Test get_topic_posts_with_user()."""
        print(MESSAGE_TOPIC1)
        posts = forum.get_topic_posts_with_user(VIEW_TOPIC3, 1000)
        posts.print_posts_user(n=1)

    def test_select_user_list(self, forum):
        """Test PostList select_user_list."""
        print(MESSAGE_TOPIC1)
        posts = forum.get_topic_posts_with_user(VIEW_TOPIC3, 1000)
        user_posts = posts.select_user_list(AUTHOR3)
        user_posts.print_posts_user()

    def test_get_forum_topics(self, forum):
        """Test get_forum_topics()."""
        forum.get_forum_topics(FORUM)
