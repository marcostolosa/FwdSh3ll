FwdSh3ll
==========
![FwdSh3ll Version](https://img.shields.io/badge/ver-0.1-red.svg)
[![Python Version](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org/downloads)
[![License](https://img.shields.io/badge/license-GPLv3-blue.svg)](https://raw.githubusercontent.com/snovvcrash/FwdSh3ll/master/LICENSE)
[![Built with Love](https://img.shields.io/badge/built%20with-%F0%9F%92%97%F0%9F%92%97%F0%9F%92%97-lightgrey.svg)](https://emojipedia.org/growing-heart)

**FwdSh3ll** is a tiny open source framework for crafting *forward shells*. What is a forward shell? Have you ever been caught in a situation when performing a pentest you discover an RCE vulnerability in a web app but despite that you can't get a reverse shell no matter how hard you try due to strictly filtered outbound traffic? A forward shell is a scheme of shell interacting with a vulnerable Linux machine based on the **named pipes** mechanism. Check the description for details!

> LEGAL DISCLAIMER: FwdSh3ll was written for use in educational purposes only. Using this tool for attacking web servers without prior mutual consistency can be considered as an illegal activity. It is the final user's responsibility to obey all applicable local, state and federal laws. The author assume no liability and is not responsible for any misuse or damage caused by this tool.

### Table of Contents:
  * [**Showcase**](#showcase)
  * [**Description**](#description)
  * [**Dependencies**](#dependencies)
    * [DEB Packages](#deb-packages)
    * [PIP Packages](#pip-packages)
  * [**Usage**](#usage)
  * [**Known Issues**](#known-issues)
  * [**Post Scriptum**](#post-scriptum)

Showcase
==========
[![Demo](https://asciinema.org/a/200295.png)](https://asciinema.org/a/200295?autoplay=1)

This demo is showing the [HTB Stratosphere](https://www.hackthebox.eu/home/machines/profile/129 "Hack The Box :: Stratosphere") box owning.

Description
==========
This method of getting a shell is described in a couple of IppSec's youtube write-ups ([Sokar](https://www.youtube.com/watch?v=k6ri-LFWEj4 "VulnHub - Sokar - YouTube") and [Stratosphere](https://www.youtube.com/watch?v=uMwcJQcUnmY "HackTheBox - Stratosphere - YouTube")). The main idea here is to create a named pipe with `mkfifo` command and `tail -f` its input to a bash process. The output would go into a regular text file which could be simply `cat`'ted. Here is how it looks like:

![Screenshot](https://user-images.githubusercontent.com/23141800/45257939-3b4ba380-b3b7-11e8-9f50-b4aa50b1b08a.png)

Dependencies
==========
### DEB Packages
  * python3.x (or newer) interpreter

### PIP Packages
FwdSh3ll makes use of the following external modules:
  * [requests](http://docs.python-requests.org/en/master "Requests: HTTP for Humans — Requests 2.19.1 documentation")
  * [termcolor](https://pypi.python.org/pypi/termcolor "termcolor 1.1.0 : Python Package Index")

Resolve all Python dependencies with one click via `pip`:
```
$ python3 -m pip install -r requirements.txt
```

Usage
==========
Currently only the interactive mode is supported.
```
python3 FwdSh3ll.py [-h]

* Target URL:
    Specify the vulnerable URL to attack.

* Proxy URL (optional):
    Specify proxy if needed.

* Payload:
    Choose required payload from the list.

* Mode (single command vs forward shell):
    Choose required action.
```

Known Issues
==========
* If you get the `connection timeout` error when initializing the forward shell, just rerun the script.

Post Scriptum
==========
Special thanks to [0xdf](https://www.hackthebox.eu/profile/4935 "Hack The Box :: 0xdf:: Member Profile") and [IppSec](https://www.youtube.com/channel/UCa6eh7gCkpPo5XXUDfygQQA "IppSec - YouTube") for sharing the forward shell concept.

If this tool has been useful for you, feel free to buy me a coffee :coffee:

[![Coffee](https://user-images.githubusercontent.com/23141800/45254832-8948b300-b387-11e8-9206-23c3e10af5f2.png)](https://buymeacoff.ee/snovvcrash)
