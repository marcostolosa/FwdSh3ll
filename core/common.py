#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""LEGAL DISCLAIMER

FwdSh3ll was written for use in educational purposes only. Using this tool
for attacking web servers without prior mutual consistency can be considered
as an illegal activity. It is the final user's responsibility to obey all
applicable local, state and federal laws.

The author assume no liability and is not responsible for any misuse or
damage caused by this tool.
"""

"""LICENSE

Copyright (C) 2019 Sam Freeside

This file is part of FwdSh3ll.

FwdSh3ll is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

FwdSh3ll is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with FwdSh3ll.  If not, see <http://www.gnu.org/licenses/>.
"""

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
