#!/usr/bin/env python3
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

	return parser.parse_args()


def configWriter(version, numOfPayloads):
	config = ConfigParser()
	config['GENERAL'] = {'version': version}
	config['payloads'] = {'total': numOfPayloads}
	return config


def configReader(config_str):
	config = ConfigParser()
	config.read_string(config_str)
	return config
