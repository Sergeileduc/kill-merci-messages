#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Module to interract with phpBB forum."""


import time
import sys
from urllib.parse import urljoin
from urllib.error import HTTPError
# from bs4 import BeautifulSoup

from utils.post import Post, Topic, Page, Forum
from utils.login import Login
from utils.browser import Browser


class PhpBB(object):
    """Class to interract with phpBB forum."""

    delete_form_id = 'confirm'
    reply_url = 'posting.php?mode=reply&f={f}&t={t}'
    edit_url = 'posting.php?mode=edit&f={f}&p={p}'
    reply_form_id = 'postform'

    def __init__(self, host):
        """Init object with forum url (host) and Browser object."""
        self.host = host
        try:
            self.browser = Browser()
        except HTTPError as e:
            print(e)
            sys.exit(1)

    def __del__(self):
        """Close the session and delete object."""
        try:
            self.browser.session.close()
        except HTTPError as e:
            print(e)
            sys.exit(1)

    def login(self, username, password):
        """Log in phpBB forum."""
        try:
            u_login = Login(self.browser.session, self.host,
                            username, password)
            u_login.send_auth()
            return u_login.is_logged()

        except HTTPError as e:
            print(e)
            return False

    def logout(self):
        """Log out of phpBB forum."""
        try:
            u_logout = Login(self.browser.session, self.host)
            u_logout.send_logout()
            return u_logout.is_logged_out()
        except HTTPError as e:
            print(e)
            return False

    def close(self):
        """Close request session (HTTP connection)."""
        try:
            self.browser.session.close()
        except HTTPError as e:
            print(e)
            sys.exit(1)

    def _get_post_text_area(self, url):
        try:
            soup = self.browser.get_html(url)
            return soup.find("textarea", id="message").text
        except HTTPError as e:
            print(e)
        except AttributeError as e:
            print("Error in _get_post_text_area")
            print(e)

    def _make_delete_confirm(self, url):
        form = self.browser.get_form(url, self.delete_form_id)
        form['values']['confirm'] = 'Oui'
        url = urljoin(self.host, form['action'])
        payload = form['values']
        return url, payload

    def _make_reply_payload(self, url, message):
        form = self.browser.get_form(url, self.reply_form_id)
        form['values']['message'] = message
        # form['values']['icon'] = 0
        del form['values']['icon']
        form['values']['post'] = 'Submit'
        url = urljoin(self.host, form['action'])
        payload = form['values']
        return url, payload

    def get_post_text(self, postid):
        """Get text of a post."""
        post = Post(postid, self)
        post.get_text()
        print(post.text)

    def get_post_editmode_content(self, forum, post):
        """Get text of a post as seen in edit mode."""
        url = urljoin(self.host, self.edit_url.format(f=forum, p=post))
        return self._get_post_text_area(url)

    def edit_post(self, forum, post, new_message):
        """Edit (modify) a message in a forum."""
        url = urljoin(self.host, self.edit_url.format(f=forum, p=post))
        try:
            form = self.browser.get_form(url, self.reply_form_id)
            form['values']['icon'] = 0
            form['values']['message'] = new_message
            form['values']['post'] = 'Submit'
            form['values']['topic_type'] = '0'

            # wait at least 2 seconds so phpBB let us post
            time.sleep(2)

            payload = form['values']

            self.browser.session.post(url,
                                      # headers=headers,
                                      data=payload)
        except HTTPError as e:
            print(f'\n>>> Error {e.code}: {e.msg}')

    def get_forum_topics(self, f):
        """Retrieve and print all topics in a forum.

        Used in list-forum.py, for example.
        """
        forum = Forum(f, self)
        forum.print_forum_title()
        forum.get_nb_topics()
        forum.get_forum_topics()
        forum.print_topics()
        return forum.get_forum_topics()

    def get_forum_view_topics(self, f):
        """Test get_forum_viewtopics()."""
        forum = Forum(f, self)
        forum.print_forum_title()
        return forum.get_forum_viewtopics()

    def get_topic_posts(self, viewtopic, max_count):
        start = 0

        # topic executes get html, get nb message and get title on creation
        topic = Topic(self, viewtopic)
        topic.print40()

        pageurl = topic.make_topic_page_url(start)

        if topic.nb_messages < max_count:
            max_count = topic.nb_messages
        while start < max_count:
            # if (start + 10) < max_count:
            #     count = 0
            # else:
            #     count = max_count - start
            page = Page(pageurl, self.browser.get_html(pageurl))
            pagelist = page.get_page_posts()
            if not pagelist:
                break
            topic.postlist.extend(pagelist)
            start += 10
            pageurl = topic.make_topic_page_url(start)

        return topic.postlist

    # Def get_topic_posts(self, f, t, max_count):
    def get_topic_posts_not_done(self, viewtopic, posts_done, max_count):
        """Return list of posts, not already done.

        Args:
            viewtopic (str): viewtopic url
            posts_done (int): number of posts already done
            max_count (int): max number

        Returns:
            PostList: list of posts not processed yet

        """
        # topic executes get html, get nb message and get title on creation
        topic = Topic(self, viewtopic)
        topic.print40()

        if topic.nb_messages > posts_done:
            print(f"{posts_done} sur {topic.nb_messages} "
                  f"messages déjà traités")
            start = posts_done

            pageurl = topic.make_topic_page_url(start)
            if topic.nb_messages < max_count:
                max_count = topic.nb_messages
            while start < max_count:
                # if (start + 10) < max_count:
                #     count = 0
                # else:
                #     count = max_count - start
                page = Page(pageurl, self.browser.get_html(pageurl))
                pagelist = page.get_page_posts()
                if not pagelist:
                    break
                topic.postlist.extend(pagelist)
                start += 10
                pageurl = topic.make_topic_page_url(start)
            return topic.nb_messages, topic.postlist
        else:
            print("already_done")
            return topic.nb_messages, topic.postlist

    # Get User on a topic
    def get_user_topic_posts(self, viewtopic, max_count):
        start = 0

        # topic executes get html, get nb message and get title on creation
        topic = Topic(self, viewtopic)
        topic.print40()

        pageurl = topic.make_topic_page_url(start)

        if topic.nb_messages < max_count:
            max_count = topic.nb_messages
        while start < max_count:
            # if (start + 10) < max_count:
            #     count = 0
            # else:
            #     count = max_count - start
            page = Page(pageurl, self.browser.get_html(pageurl))
            pagelist = page.get_page_posts_with_user()
            if not pagelist:
                break
            topic.postlist.extend(pagelist)
            start += 10
            pageurl = topic.make_topic_page_url(start)

        return topic.postlist

    def delete_post(self, post):
        """Delete one message. Send proper request."""
        try:
            url_get = post.make_delete_req_url(self.host)
            print("delete : " + url_get)

            url_post, payload = self._make_delete_confirm(url_get)
            time.sleep(1)

            self.browser.session.post(url_post,
                                      # headers=headers,
                                      data=payload)
        except HTTPError as e:
            print(e)
            print("HTTPError with post : " + post.id)
        except TypeError as e2:
            print(e2)

    def delete_post_list(self, post_list):
        """Delete multiple messages (in a list)."""
        for post in post_list:
            self.delete_post(post)

    def get_topic_posts_with_user(self, viewtopic, max_count):
        start = 0
        # topic executes get html, get nb message and get title on creation
        topic = Topic(self, viewtopic)
        topic.print40()

        if topic.nb_messages < max_count:
            max_count = topic.nb_messages
        while start < max_count:
            # print(urltopic)
            # if (start + 10) < max_count:
            #     count = 0
            # else:
            #     count = max_count - start
            pageurl = topic.make_topic_page_url(start)
            page = Page(pageurl, self.browser.get_html(pageurl))
            pagelist = page.get_page_posts_with_user()
            if not pagelist:
                break
            topic.postlist.extend(pagelist)
            start += 10

        return topic.postlist

    def post_reply(self, forum, topic, message):
        """Send a reply."""
        url = urljoin(self.host, self.reply_url.format(f=forum, t=topic))

        urlrep, payload = self._make_reply_payload(url, message)
        print(urlrep)
        print(payload)
        time.sleep(2)
        self.browser.session.post(urlrep,
                                  # headers=headers,
                                  # params=self.login_mode,
                                  data=payload)
