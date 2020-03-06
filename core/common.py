#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from termcolor import colored

from core import (
	__author__,
	__version__,
	__site__
)

VERSION_FORMATTED = '{' + colored(f'v{__version__}', 'blue', attrs=['bold']) + '}'
AUTHOR_FORMATTED = colored(f'by {__author__}', attrs=['dark'])
SITE_FORMATTED = colored(__site__, attrs=['underline', 'dark'])

BANNER = f"""\033[1;32m
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
"""
