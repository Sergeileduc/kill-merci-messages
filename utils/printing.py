#!/usr/bin/python3
# -*-coding:utf-8 -*-
"""Module to print formated strings."""


def print_title_url_40(title, url):
    """Print title (40 chars) | full url."""
    print('{title:.<40.40} | {url}'.format(title=title, url=url))


def print_title_url_60(title, url):
    """Print title (60 chars) | url (60 chars)."""
    print('{title:60.60} | {url:<60}'.format(title=title, url=url))
