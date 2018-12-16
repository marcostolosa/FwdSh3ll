#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os import listdir

import requests
from termcolor import cprint

from core import __version__
from core.parser import configWriter, configReader

__author__    = 'Sam Freeside (@snovvcrash)'
__email__     = 'snovvcrash@protonmail[.]ch'
__copyright__ = 'Copyright (C) 2018 Sam Freeside'

__license__ = 'GPL-3.0'
__site__    = 'https://github.com/snovvcrash/FwdSh3ll'
__brief__   = 'Updater module.'

CONFIG_URL = 'https://raw.githubusercontent.com/snovvcrash/FwdSh3ll/master/FwdSh3ll.ini'


def updater():
	allPayloads = [pn[:-3] for pn in sorted(listdir('./payloads')) if pn.endswith('.py') and not pn.startswith('_')]
	numOfPayloads = len(allPayloads)

	lconfig = configWriter(__version__, numOfPayloads)

	with open('./FwdSh3ll.ini', 'w', encoding='utf-8') as configFile:
		lconfig.write(configFile)

	cprint(f'[*] Loaded {numOfPayloads} payload(s)', 'green')

	try:
		resp = requests.get(CONFIG_URL, timeout=25)
	except Exception as e:
		cprint(f'[!] Failed to check for updates: {str(e)}', 'yellow')
	else:
		if resp.status_code == 200:
			rconfig = configReader(resp.text.strip())

			if rconfig['GENERAL']['version'] != __version__:
				cprint('[!] New version is available!', 'yellow')
			if int(rconfig['payloads']['total']) > numOfPayloads:
				cprint('[!] New payloads are available!', 'yellow')

	return allPayloads
