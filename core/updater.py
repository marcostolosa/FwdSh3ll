#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests

from os import listdir

from termcolor import cprint

from core.parser import configWriter, configReader
from core.common import VERSION

CONFIG_URL = 'https://raw.githubusercontent.com/snovvcrash/FwdSh3ll/master/FwdSh3ll.ini'


def updater():
	allPayloads = [pn[:-3] for pn in sorted(listdir('./payloads')) if pn.endswith('.py') and not pn.startswith('_')]
	numOfPayloads = len(allPayloads)

	lconfig = configWriter(VERSION, numOfPayloads)

	with open('./FwdSh3ll.ini', 'w', encoding='utf-8') as configFile:
		lconfig.write(configFile)

	cprint(f'[*] Loaded {numOfPayloads} payload(s)', 'green')

	try:
		resp = requests.get(CONFIG_URL, timeout=25)
	except Exception as e:
		cprint(f'[!] Failed to check for updates: {str(e)}', 'yellow')
	else:
		if resp.status_code == 200:
			rconfig = configReader(resp.text)

			if rconfig['GENERAL']['version'] != VERSION:
				cprint('[!] New version is available!', 'yellow')
			if int(rconfig['Payloads']['total']) > numOfPayloads:
				cprint('[!] New payloads are available!', 'yellow')

	return allPayloads
