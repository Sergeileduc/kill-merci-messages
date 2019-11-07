#!/usr/bin/python3
# -*-coding:utf-8 -*-
"""Classes for phpbb forums, topics, messages."""

import dateparser
import datetime
import re
from operator import itemgetter
from urllib.error import HTTPError
from urllib.parse import urljoin

# from utils.printing import print_title_url_60
from utils.printing import print_title_url_40
from utils.tools import get_query_field


# class for a message on a forum
class Post:
    """Class for a "post", a single message in phpbb forum."""

    post_url = 'viewtopic.php?p={p}#p{p}'
    delete_url = 'posting.php?mode=delete&f={f}&p={p}'

    def __init__(self, id, text=None, rank=None, user=None,
                 date=None, old=None, fid=None, phpbb=None):
        """Init a Post object, with his post id, and optional things."""
        self.id = id
        self.text = text
        self.rank = rank
        self.user = user
        self.date = date
        self.old = old
        self.fid = fid
        self.phpBB = phpbb
        self.url = None
        self.html = None

    def __str__(self):
        """Return formated string of post."""
        text = self.text.replace("\n", "")
        date = str(self.date)
        template = ("{id:>10} | {text:<60.60} | "
                    "{grade:<15.15} | {date:<10.10} | {old:>4} | {fid}")
        return template.format(id=self.id, text=text,
                               grade=self.rank, date=date, old=self.old,
                               fid=self.fid)

    def get_post_html(self):
        """Get html code for a post url."""
        urlpost = urljoin(self.phpBB.host, self.post_url.format(p=self.id))
        self.url = urlpost
        try:
            pid = f"p{self.id}"
            html = self.phpBB.browser.get_html(urlpost).find(id=pid)
            self.html = html
        except HTTPError as e:
            print("KO")
            print(e)

    def get_text(self):
        """Get text of a forum message."""
        self.get_post_html()
        div = self.html.select_one('div.postbody')
        self.text = div.find_all(class_="content")[0].text

    def print_with_user(self):
        """Print post with : id, text, grade, user, old date."""
        text = self.text.replace("\n", "")
        template = ("{id:>10} | {text:<60.60} | "
                    "{grade:<15.15} | {user:<10.10} | {old}")
        print(template.format(id=self.id, text=text,
                              grade=self.rank, user=self.user, old=self.old))

    def make_delete_req_url(self, host):
        """Make delete url for a phpBB post.

        Args:
            host (str): host url

        Returns:
            str: delete post url

        """
        return urljoin(host,
                       self.delete_url.format(f=self.fid, p=int(self.id)))


class PostList(list):
    """Class for a list of objects "Post"."""

    # Print posts with ID, text, rank, etc...
    def print_posts(self, n=None):
        """Print list of posts (using __str__ function in Post class).

        Args:
            n (int, optional): number of posts to print. Defaults to None.

        """
        if not n:
            for post in self:
                print(post)
        else:
            for post in self[:n]:
                print(post)

    def print_posts_user(self, n=None):
        """Print list of posts with author username.

        Args:
            n (int, optional): number of posts to print. Defaults to None.

        """
        if not n:
            for post in self:
                post.print_with_user()
        else:
            for post in self[:n]:
                post.print_with_user()

    def print_posts_full(self):
        """Print list of posts with full text."""
        for post in self:
            print(post.id)
            print(post.text)
            print("---------------------------")

    def merci_list(self, pattern1, pattern2, pattern3):
        """Search "merci" messages in list of messages."""
        target_list = PostList()
        for post in self:
            if post.rank == 'Humain' or post.rank == "unknown":
                if pattern1.match(post.text):
                    target_list.append(post)
                elif pattern2.match(post.text):
                    target_list.append(post)
                elif pattern3.match(post.text):
                    target_list.append(post)
        return target_list

    def search_words(self, list):
        """Search words messages in list of messages."""
        target_list = PostList()
        for post in self:
            # if (post.rank == 'Humain' or post.rank == "unknown"):
            for word in list:
                if word in post.text.lower():
                    target_list.append(post)
        return target_list

    def log_posts(self, file):
        """Log posts with ID, text, author rank in a file."""
        for post in self:
            file.write(str(post) + '\n')

    def select_user_list(self, username):
        """Select messages from "username" in a list of messages."""
        return PostList([p for p in self if p.user == username])


class Topic:
    """Class to work with phpbb topic."""

    topic_url = '{topic}&start={start}'

    def __init__(self, phpbb=None, viewtopic=None):
        """Init with phpbb object, and viewtopic."""
        self.phpBB = phpbb
        self.viewtopic = viewtopic
        self.url, self.html = self._get_topic_html()
        self.nb_messages = self.get_nb_posts()
        self.title = self.find_topic_title()
        self.postlist = PostList()
        self.messages = 0
        self.start = 0

    def _get_topic_html(self):
        urltopic = urljoin(self.phpBB.host, self.viewtopic)
        try:
            html = self.phpBB.browser.get_html(urltopic)
            return urltopic, html
        except HTTPError as e:
            print("KO")
            print(e)
            raise

    def find_topic_title(self):
        """Return the topic title."""
        try:
            self.title = self.html.find(class_="topic-title").text
        except AttributeError:
            self.title = "Unknown title"
        return self.title

    def make_topic_page_url(self, start):
        """Return topic url, with start=XX (several pages)."""
        pageurl = urljoin(self.phpBB.host,
                          self.topic_url.format(topic=self.viewtopic,
                                                start=start))
        return pageurl

    def get_nb_posts(self):
        """Return number of messages in a topic."""
        i = 0
        try:
            messages = self.html.find(class_="pagination").text.split()
            while True:
                try:
                    # if messages[i] == 'messages' or messages[i] == 'message':
                    # check if 'message' of 'messages'
                    if (re.match(r"message[s]?", messages[i]) and
                            messages[i - 1] != "premier"):
                        self.messages = int(messages[i - 1])
                        break
                    else:
                        i += 1
                except Exception:
                    # print(e)
                    print("Error in Topic get_nb_post")
                    self.messages = 1
                    break
        except AttributeError:
            self.messages = 1
        return self.messages

    def print40(self):
        """Print topic title and url."""
        print('{title:.<40} | {url}'.format(title=self.title, url=self.url))


class Page:
    """Class to work with phpbb topic page (i.e. with start=XX)."""

    regex = r"f\=(?P<fid>\d+)&t\=(?P<topic>\d+)&start=(?P<start>\d+)"

    def __init__(self, url, html):
        """Init a topic page with his url and html code."""
        self.url = url
        self.html = html
        self.pagelist = PostList()
        self.fid = get_query_field(url, 'f')[0]
        self.tid = get_query_field(url, 't')[0]
        self.start = None

        # def __str__(self):
    #     self.pagelist.print_posts()

    def print_page(self):
        """Print all messages in a topic page."""
        self.pagelist.print_posts()

    def _parse_url(self):
        m = re.search(self.regex, self.url)
        self.fid = int(m.group('fid'))
        self.tid = int(m.group('topic'))
        self.start = int(m.group('start'))

    def get_page_posts(self):
        """Return list of messages on a topic page."""
        res = self.html.find_all(class_=re.compile("post has-profile"))
        for r in res:
            id = r.get('id').replace('post_content', '').replace('p', '')
            text = r.find_all(class_="content")[0].text
            ranks = r.find_all(class_="profile-rank")
            if not ranks:
                rank = "unknown"
            else:
                rank = ranks[0].text
            date = r.find(class_="unread").text.split(',')[0]
            date = dateparser.parse(date).date()
            delta = (datetime.date.today() - date).days
            # out.append((id, text, rank))
            post = Post(id, text=text, rank=rank, date=date,
                        old=delta, fid=self.fid)
            self.pagelist.append(post)
        return self.pagelist

    def get_page_posts_with_user(self):
        """Return list of messages (with users name) on a topic page."""
        res = self.html.find_all(class_=re.compile("post has-profile"))
        for r in res:
            id = r.get('id').replace('post_content', '').replace('p', '')
            text = r.find_all(class_="content")[0].text
            ranks = r.find_all(class_="profile-rank")
            try:
                user = r.find(class_="username-coloured").text
            except AttributeError:
                user = r.find(class_="username").text
            if not ranks:
                rank = "unknown"
            else:
                rank = ranks[0].text
            date = r.find(class_="unread").text.split(',')[0]
            date = dateparser.parse(date).date()
            delta = (datetime.date.today() - date).days
            post = Post(id, text=text, rank=rank, date=date,
                        old=delta, fid=self.fid, user=user)
            self.pagelist.append(post)
        return self.pagelist


class Forum:
    """Class for a sub-forum."""

    forum_url = 'viewforum.php?f={}'
    forum_page = '{forum}&start={start}'
    nb_topics_regex = r"(?P<nb_topics>\d+?) sujets"

    def __init__(self, f_id, phpbb=None):
        """Init with forum id, forum url, and get html."""
        self.nb_topics = 0
        self.phpBB = phpbb
        self.f = f_id
        self.url = self._make_forum_url()
        self.topics = []
        try:
            self.html = self.phpBB.browser.get_html(self.url)
            self.get_nb_topics()
        except HTTPError as e:
            print("KO")
            print(e)

    def _make_forum_url(self):
        url = urljoin(self.phpBB.host, self.forum_url.format(self.f))
        return url

    def _make_page_url(self, start):
        view_forum = self.forum_url.format(self.f)
        url = urljoin(self.phpBB.host,
                      self.forum_page.format(forum=view_forum, start=start))
        return url

    def print_forum_title(self):
        """Print title of sub-forum (self)."""
        try:
            forum_title = self.html.find(class_="forum-title").text
        except AttributeError:
            forum_title = "Unkwnow title"
        print("===========================")
        # print(forum_title.upper())
        # print(urlforum)
        print_title_url_40(forum_title.upper(), self.url)

    def get_forum_topics(self):
        """Return list of all topics titles and urls in a sub-forum."""
        start = 0
        n = self.nb_topics
        while n > 0:
            page_url = self._make_page_url(start)
            try:
                html = self.phpBB.browser.get_html(page_url)
                res = html.find_all("a", class_="topictitle")
                for r in res:
                    t_title = r.text
                    url = urljoin(self.phpBB.host,
                                  r.get('href').replace('./', ''))
                    self.topics.append({'title': t_title, 'url': url})
            except HTTPError as e:
                print("KO")
                print(e)
            n = n - 40
            start = start + 40
        return self.topics

    def get_forum_viewtopics(self):
        """Find all 'viewtopics' url in a subforum."""
        out = []
        start = 0
        n = self.nb_topics
        while n > 0:
            try:
                html = self.phpBB.browser.get_html(self.url)
                # try:
                #     forum_title = html.find(class_="forum-title").text
                # except AttributeError:
                #     forum_title = "Unknown title"
                res = html.find_all("a", class_="topictitle")

                for r in res:
                    url = r.get('href').replace('./', '')
                    v = Viewtopicurl(url)
                    v.parse_url()
                    out.append(v)
            except HTTPError as e:
                print("KO")
                print(e)
            n = n - 40
            start = start + 40
        return out

    def print_topics(self, n=None):
        """Print all topics (title / url) in a sub-forum (self).

        Args:
            n (int, optional): number of topics to print.
            Defaults to None (all topics).

        """
        for t in sorted(self.topics, key=itemgetter('title')):
            print_title_url_40(t['title'], t['url'])

    def get_nb_topics(self):
        """Get number of topics in sub-forum (self)."""
        try:
            # bar = self.html.find('div', class_="action-bar bar-top")
            # pagination = bar.find('div', class_="pagination")
            # self.nb_pages = pagination.find_all("strong")[1].text
            raw = self.html.select(
                'div.action-bar.bar-top > div.pagination')[0].text
            n = re.search(self.nb_topics_regex, raw).group('nb_topics')
            self.nb_topics = int(n)
        except AttributeError:
            self.nb_topics = 1
        return self.nb_topics


class Viewtopicurl:
    """Class for objects like viewtopic.php?f=190&t=8467.

    Allow to construct or parse.

    """

    regex = r"f\=(?P<fid>\d+)&t\=(?P<topic>\d+)"

    def __init__(self, urlpart=None, fid=None, tid=None):
        """Init with urlpart, or forum id and topic id."""
        self.urlpart = urlpart
        self.fid = fid
        self.tid = tid

    def __str__(self):
        """Return formated string of Viewtopic."""
        template = "{fid:>10} | {tid:>10} | {url:<60.60}"
        return template.format(fid=self.fid, tid=self.tid, url=self.urlpart)

    def parse_url(self):
        """Find forum id and topic id in viewtopic url."""
        m = re.search(self.regex, self.urlpart)
        self.fid = int(m.group('fid'))
        self.tid = int(m.group('topic'))
