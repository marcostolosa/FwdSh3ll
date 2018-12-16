#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from termcolor import colored

from core import __version__

__author__    = 'Sam Freeside (@snovvcrash)'
__email__     = 'snovvcrash@protonmail[.]ch'
__copyright__ = 'Copyright (C) 2018 Sam Freeside'

__license__ = 'GPL-3.0'
__site__    = 'https://github.com/snovvcrash/FwdSh3ll'
__brief__   = 'Common items.'

VERSION_FORMATTED = '{' + colored('v' + __version__, 'blue', attrs=['bold']) + '}'
AUTHOR_FORMATTED = colored('by ' + __author__, attrs=['dark'])
SITE_FORMATTED = colored(__site__, attrs=['underline', 'dark'])

BANNER = f'''\033[1;32m
  █████▒█     █░▓█████▄   ██████  ██░ ██ ▓█████  ██▓     ██▓    
▓██   ▒▓█░ █ ░█░▒██▀ ██▌▒██    ▒ ▓██░ ██▒▓█   ▀ ▓██▒    ▓██▒    
▒████ ░▒█░ █ ░█ ░██   █▌░ ▓██▄   ▒██▀▀██░▒███   ▒██░    ▒██░    
░▓█▒  ░░█░ █ ░█ ░▓█▄   ▌  ▒   ██▒░▓█ ░██ ▒▓█  ▄ ▒██░    ▒██░    
░▒█░   ░░██▒██▓ ░▒████▓ ▒██████▒▒░▓█▒░██▓░▒████▒░██████▒░██████▒
 ▒ ░   ░ ▓░▒ ▒   ▒▒▓  ▒ ▒ ▒▓▒ ▒ ░ ▒ ░░▒░▒░░ ▒░ ░░ ▒░▓  ░░ ▒░▓  ░
 ░       ▒ ░ ░   ░ ▒  ▒ ░ ░▒  ░ ░ ▒ ░▒░ ░ ░ ░  ░░ ░ ▒  ░░ ░ ▒  ░
 ░ ░     ░   ░   ░ ░  ░ ░  ░  ░   ░  ░░ ░   ░     ░ ░     ░ ░   
           ░       ░          ░   ░  ░  ░   ░  ░    ░  ░    ░  ░
                 ░                                              
                 \033[0m
{VERSION_FORMATTED}
{AUTHOR_FORMATTED}
{SITE_FORMATTED}
'''
