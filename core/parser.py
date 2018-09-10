#!/usr/bin/env python
# -*- coding: utf-8 -*-

from argparse import ArgumentParser
from configparser import ConfigParser


def cliOptions():
	parser = ArgumentParser()

	parser.add_argument(
		'-pp',
		'--pipes-path',
		type=str,
		default='/dev/shm',
		help='set remote path of the named pipes to PIPES_PATH (default: "/dev/shm")'
	)

	parser.add_argument(
		'-b64',
		'--no-base64',
		action='store_true',
		default=True,
		help='do NOT wrap the final command into Base64 encoding'
	)

	return parser.parse_args()


def configWriter(version, numOfPayloads):
	config = ConfigParser()
	config['GENERAL'] = {'version': version}
	config['Payloads'] = {'total': numOfPayloads}
	return config


def configReader(config_str):
	config = ConfigParser()
	return config.read_string(config_str)
