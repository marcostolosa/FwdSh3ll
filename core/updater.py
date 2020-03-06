#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
