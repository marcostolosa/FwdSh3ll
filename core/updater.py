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

from os import listdir

import requests
from termcolor import cprint

from core import __version__
from core.parser import (
	get_config_parser_writer,
	get_config_parser_reader
)

CONFIG_URL = 'https://raw.githubusercontent.com/snovvcrash/FwdSh3ll/master/FwdSh3ll.ini'


def update():
	all_payloads = [pn[:-3] for pn in sorted(listdir('./payloads')) if pn.endswith('.py') and not pn.startswith('_')]
	num_of_payloads = len(all_payloads)

	lconfig_parser = get_config_parser_writer(__version__, num_of_payloads)

	with open('./FwdSh3ll.ini', 'w', encoding='utf-8') as configFile:
		lconfig_parser.write(configFile)

	cprint(f'[*] Loaded {num_of_payloads} payload(s)', 'green')

	try:
		resp = requests.get(CONFIG_URL, timeout=25)
	except Exception as e:
		cprint(f'[!] Failed to check for updates: {str(e)}', 'yellow')
	else:
		if resp.status_code == 200:
			rconfig_parser = get_config_parser_reader(resp.text.strip())

			if rconfig_parser['GENERAL']['version'] != __version__:
				cprint('[!] New version is available!', 'yellow')
			if int(rconfig_parser['payloads']['total']) > num_of_payloads:
				cprint('[!] New payloads are available!', 'yellow')

	return all_payloads
