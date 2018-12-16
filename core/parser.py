#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from argparse import ArgumentParser
from configparser import ConfigParser

__author__    = 'Sam Freeside (@snovvcrash)'
__email__     = 'snovvcrash@protonmail[.]ch'
__copyright__ = 'Copyright (C) 2018 Sam Freeside'

__license__ = 'GPL-3.0'
__site__    = 'https://github.com/snovvcrash/FwdSh3ll'
__brief__   = 'Parser for options (command line and config file).'


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
