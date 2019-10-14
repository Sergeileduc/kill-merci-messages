#!/usr/bin/python3
# -*-coding:utf-8 -*-

import re
from urllib.parse import parse_qs, urlparse
# from utils.post import Post


# Split config file input
def configsplit(string):
    """Split string (" // " separator) and returns a list."""
    return string.split(" // ")


def gen_regex1(list):
    """Compile regex 1.

    Args:
        list (list): list of keywords

    Returns:
        re.compile object: compiled regex

    """
    reg = '^.{0,2}(' \
        + '|'.join(map(re.escape, list)) \
        + r').{0,6}!*(:cheer:|:cheer2:|:\\o/:|:hiiii:|:\)|:fdance:|:victory:)*$'
    return re.compile(reg, re.IGNORECASE)


# Compile regex2
def gen_regex2(list):
    """Compile regex.

    Args:
        list (list): list of keywords

    Returns:
        re.compile object: compiled regex

    """
    reg = '^.{0,2}(' + '|'.join(map(re.escape, list)) \
          + r')\ .{0,2}[0-9]+.{0,6}!*' \
          r'(:cheer:|:cheer2:|:\\o/:|:hiiii:|:\)|:fdance:|:victory:)*$'
    return re.compile(reg, re.IGNORECASE)


def compute_regex(cfg):
    """Compile 3 regex for "merci"."""
    regex1_list = configsplit(cfg.config['regex']['regex1'])
    regex2_list = configsplit(cfg.config['regex']['regex1'])
    regex1 = gen_regex1(regex1_list)
    regex2 = gen_regex2(regex2_list)
    regex3 = re.compile(
        r"^Merci pour les [1-9]+ numéros.{0,5}$", re.IGNORECASE)
    # regex4 = re.compile(r"merci.{0,7}:cheer2:", re.IGNORECASE)
    return regex1, regex2, regex3


# Select posts from one user
def select_user_list(postslist, username):
    """Return a list of posts for one specific user.

    Args:
        postslist (Postlist): list of posts
        username (str): User

    Returns:
        Postlist: list of the user posts

    """
    target_list = []
    for post in postslist:
        if post.user == username:
            target_list.append(post)
    return target_list


# Parse url and get fields
def get_query_field(url, field):
    """Parse url and returns value for key (field)."""
    try:
        return parse_qs(urlparse(url).query)[field]
    except KeyError:
        return []
