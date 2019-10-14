#!/usr/bin/python3
# -*-coding:utf-8 -*-
"""Module to manage log in in forum."""

import re
import time
# import requests

from bs4 import BeautifulSoup
from urllib.parse import urljoin


class Login:
    """Class to manage log in."""

    cookie_sid_pattern = r'phpbb\d?_.*_sid'  # new cookie regex
    cookie_u_pattern = r'phpbb\d?_.*_u'  # new cookie regex

    ucp_url = 'ucp.php'
    login_mode = {'mode': 'login'}
    logout_mode = {'mode': 'logout'}

    def __init__(self, session, host, username=None, password=None):
        """Init Login object with url, username, password."""
        self.session = session
        self.host = host
        self.username = username
        self.password = password
        self.r = self.session.get(self.host)
        self.soup = BeautifulSoup(self.r.text, 'html.parser')

    def _parse_sid(self):
        for cookie in self.session.cookies:
            if re.search(self.cookie_sid_pattern, cookie.name):
                sid = cookie.value
                return sid

    def _parse_token(self):
        # tokenStart = self.r.text.find("form_token")+19
        # token = self.r.text[tokenStart:tokenStart+40]
        return self.soup.find('input', {'name': 'form_token'})['value']

    def _parse_uid(self):
        for cookie in self.session.cookies:
            # print(cookie)
            if re.search(self.cookie_u_pattern, cookie.name):
                return cookie.value

    def _parse_ctime(self):
        # timeStart = self.r.text.find("creation_time")+22
        # self.c_time = self.r.text[timeStart:timeStart+10]
        return self.soup.find('input', {'name': 'creation_time'})['value']

    def _create_login_payload(self):
        payload = [('username', self.username),
                   ('password', self.password),
                   ('redirect', './ucp.php?mode=login'),
                   ('creation_time', self._parse_ctime()),
                   ('form_token', self._parse_token()),
                   ('sid', self._parse_sid()),
                   ('redirect', 'index.php'),
                   ('login', 'Connexion')]
        return payload

    def _create_logout_params(self):
        params = {'mode': 'logout', 'sid': self._parse_sid()}
        return params

    def _create_logout_payload(self):
        payload = {'sid': self._parse_sid()}
        return payload

    def send_auth(self):
        """Send credentials."""
        payload = self._create_login_payload()
        time.sleep(1)
        forum_ucp = urljoin(self.host, self.ucp_url)
        self.r = self.session.post(forum_ucp,
                                   # headers=headers,
                                   params=self.login_mode,
                                   data=payload)
        # print(self.r.request.body)

    def send_logout(self):
        """Send logout."""
        # payload = self._create_logout_payload()
        forum_ucp = urljoin(self.host, self.ucp_url)
        self.r = self.session.post(forum_ucp,
                                   # headers=headers,
                                   params=self._create_logout_params())

    def is_logged(self):
        """Check if logged in."""
        u = int(self._parse_uid())
        if u != 1:
            print(f"login OK : {str(u)}")
            return True
        else:
            print(f"login failed : {str(u)}")
            return False

    def is_logged_out(self):
        """Check if logged out."""
        u = int(self._parse_uid())
        if u != 1:
            print(f"Still logged in : {str(u)}")
            return True
        else:
            print(f"Signed out : {str(u)}")
            return False
