#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

import requests

from termcolor import cprint

from core.common import VERSION

CONFIG_URL = 'https://raw.githubusercontent.com/snovvcrash/FwdSh3ll/master/FwdSh3ll.conf'


def updater(allPayloads):
	numOfPayloads = len(allPayloads)

	with open('./FwdSh3ll.conf', 'w', encoding='utf-8') as conf:
		conf.write('ver=' + VERSION + '\n')
		conf.write('num_of_payloads=' + str(numOfPayloads) + '\n')

	cprint(f'[*] Loaded {numOfPayloads} payload(s)', 'green')

	try:
		latestConf = requests.get(CONFIG_URL, timeout=25).text
	except Exception as e:
		cprint(f'[!] Failed to check for updates: {str(e)}', 'yellow')
		return

	ver = re.search(r'^ver=(\d+.\d+)$', latestConf, re.MULTILINE).group(1)
	num = re.search(r'^num_of_payloads=(\d+)$', latestConf, re.MULTILINE).group(1)

	if ver != VERSION:
		cprint('[!] New version is available!', 'yellow')
	if int(num) > numOfPayloads:
		cprint('[!] New payloads are available!', 'yellow')
