#!/usr/bin/python3
# -*-coding:utf-8 -*-
"""Store constants."""


class Const(object):
    """Store constants."""

    cfg_opts = ['host',
                'username',
                'password',
                'delay',
                'max_count',
                'user_agent'
                ]

    cfg_opts_simple = ['host',
                       'username',
                       'password',
                       'max_count',
                       'user_agent'
                       ]

    cfg_opts_modo = ['host',
                     'username',
                     'password',
                     'delay',
                     'max_count',
                     'user_agent',
                     'general',
                     'comics',
                     'medias',
                     'keywords']

    MODE_CHOICE = ('Que voulez-vous faire ?\n'
                   '1- Traiter un seul topic\n'
                   '2- Traiter un sous forum entier '
                   '(DC Rebirth / Marvel / etc...)\n'
                   '3- Oublier les topics déjà nettoyés'
                   '(repartir à zéro)\n'
                   '4- Oublier un topic (d\'après son numéro)\n'
                   'Réponse : 1 2 3 ou 4\n')

    MODE_CHOICE2 = ('Que voulez-vous faire ?\n'
                    '1- Traiter un seul topic\n'
                    '2- Traiter un sous forum entier '
                    '(General / Comics / etc...)\n'
                    '3- Oublier les topics déjà nettoyés'
                    '(repartir à zéro)\n'
                    '4- Oublier un topic (d\'après son numéro)\n'
                    'Réponse : 1 2 3 ou 4\n')

    SECTION_CHOICE = ('Nettoyer\n'
                      '1 - DC Rebirth\n'
                      '2 - DC New 52\n'
                      '3 - DC classique\n'
                      '4 - DC Hors-continuité\n'
                      '5 - Vertigo / Hanna Barbera\n'
                      '6 - Marvel\n'
                      '7 - Indés éditeurs\n'
                      '8 - Indés Divers\n'
                      '9 - Tous les topics\n'
                      '10- Sous forum perso (voir config file)\n')
    SECTION_CHOICE2 = ('Nettoyer\n'
                       '1 - Général\n'
                       '2 - Comics\n'
                       '3 - Médias\n')

    SECTION_MAP = {1: "rebirth",
                   2: "new52",
                   3: "dcclassic",
                   4: "dchc",
                   5: "vertigo",
                   6: "marvel",
                   7: "indes",
                   8: "divers",
                   9: "all_topics",
                   10: "perso"}

    F_INPUT = ('Numéro de forum ?\n'
               '(Par exemple, pour viewtopic.php?f=259&t=15753'
               ', taper 259) :\n')

    T_INPUT = ('Numéro de topic ?\n'
               '(Par exemple, pour viewtopic.php?f=259&t=15753, '
               'taper 15753) :\n')
