#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from argparse import ArgumentParser
from configparser import ConfigParser


def get_arg_parser():
	arg_parser = ArgumentParser()

	arg_parser.add_argument(
		'-pp',
		'--pipes-path',
		type=str,
		default='/dev/shm',
		help='set remote path of the named pipes to PIPES_PATH (default: "/dev/shm")'
	)

	return arg_parser


def get_config_parser_writer(version, num_of_payloads):
	config_parser = ConfigParser()
	config_parser['GENERAL'] = {'version': version}
	config_parser['payloads'] = {'total': num_of_payloads}
	return config_parser


def get_config_parser_reader(config_str):
	config_parser = ConfigParser()
	config_parser.read_string(config_str)
	return config_parser
