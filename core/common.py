#!/usr/bin/env python
# -*- coding: utf-8 -*-

from termcolor import colored

VERSION = '0.2'
AUTHOR = 'by snovvcrash'
SITE = 'https://github.com/snovvcrash/FwdSh3ll'

VERSION_FORMATTED = '{' + colored('v' + VERSION, 'blue', attrs=['bold']) + '}'
AUTHOR_FORMATTED = colored(AUTHOR, attrs=['dark'])
SITE_FORMATTED = colored(SITE, attrs=['underline', 'dark'])

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
