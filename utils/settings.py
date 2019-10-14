#!/usr/bin/python3
# -*-coding:utf-8 -*-
"""Module to read config file."""

import configparser


class Settings(object):
    """Class for parsing config .cfg file."""

    def __init__(self, configfile):
        """Init object with config file path."""
        self.config = configparser.ConfigParser(interpolation=None)
        self.config.read(configfile)

    def load(self, section, opts):
        """Read config file and set object attributes."""
        try:
            for key in opts:
                try:
                    setattr(self, key, self.config.get(section, key))
                except configparser.NoOptionError:
                    setattr(self, key, self.config.get('default', key))

        except configparser.NoSectionError:
            print(f"The section {section} does not exist")
        except configparser.NoOptionError as e:
            print("The value for {key} is missing")
            raise e
        else:
            return True
        return False

    def read_section(self, section):
        """Read a section in config file."""
        return self.config[section]
