FwdSh3ll
==========
![FwdSh3ll Version](https://img.shields.io/badge/ver-0.2-red.svg)
[![Python Version](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org/downloads)
[![License](https://img.shields.io/badge/license-GPLv3-blue.svg)](https://raw.githubusercontent.com/snovvcrash/FwdSh3ll/master/LICENSE)
[![Built with Love](https://img.shields.io/badge/built%20with-%F0%9F%92%97%F0%9F%92%97%F0%9F%92%97-lightgrey.svg)](https://emojipedia.org/growing-heart)

**FwdSh3ll** is a tiny open source framework for crafting *forward shells*. What is a forward shell? Have you ever been caught in a situation when looking for an approach to a CTF box you discover an RCE vulnerability in a web app but despite that you can't get a reverse shell no matter how hard you try due to strictly filtered outbound traffic? A forward shell is a scheme of shell interaction with a vulnerable Linux machine based on the **named pipes** mechanism. Check the [description](#description) for details!

This tool **does not claim to provide** an all-occasions usage experience out of the box. Each pentest case involes an individual basic enumeration first, whose results may require minor code adjustment.

> LEGAL DISCLAIMER: FwdSh3ll was written for use in educational purposes only. Using this tool for attacking web servers without prior mutual consistency can be considered as an illegal activity. It is the final user's responsibility to obey all applicable local, state and federal laws. The author assume no liability and is not responsible for any misuse or damage caused by this tool.

### Table of Contents:
- [**Showcase**](#showcase)
- [**Description**](#description)
- [**Dependencies**](#dependencies)
  - [DEB Packages](#deb-packages)
  - [PIP Packages](#pip-packages)
- [**Usage**](#usage)
- [**Payloads**](#payloads)
- [**Known Issues**](#known-issues)
- [**Post Scriptum**](#post-scriptum)

Showcase
==========
[![Demo](https://asciinema.org/a/200295.png)](https://asciinema.org/a/200295?autoplay=1)

This demo is showing the [HTB Stratosphere](https://www.hackthebox.eu/home/machines/profile/129 "Hack The Box :: Stratosphere") box tomcat user owning.

Description
==========
This method of getting a shell is described in a couple of IppSec's youtube write-ups ([Sokar](https://www.youtube.com/watch?v=k6ri-LFWEj4 "VulnHub - Sokar - YouTube") and [Stratosphere](https://www.youtube.com/watch?v=uMwcJQcUnmY "HackTheBox - Stratosphere - YouTube")). The main idea here is to create a named pipe with `mkfifo` command and `tail -f` its input to a `/bin/sh` process. The output would go into a regular text file which could be simply `cat`'ted. What is also very cool is that you can move around the filesystem and the shell will remember your current directory as well as spawn other pty shells and so on. Here is how it looks like:

![Screenshot](https://user-images.githubusercontent.com/23141800/45626338-f4853a00-ba97-11e8-8f1a-962b4f32a36b.png)

Dependencies
==========
### DEB Packages
  * python3.x (or newer) interpreter

### PIP Packages
FwdSh3ll makes use of the following external modules:
  * [requests](http://docs.python-requests.org/en/master "Requests: HTTP for Humans — Requests 2.19.1 documentation")
  * [termcolor](https://pypi.python.org/pypi/termcolor "termcolor 1.1.0 : Python Package Index")

To resolve all Python dependencies create a virtual environment and run `pip` from within:
```
$ virtualenv -p python3 venv && . venv/bin/activate
(venv) $ pip install -r requirements.txt
```

Or let the `pipenv` one-liner do all the dirty work for you:
```
$ pipenv install && pipenv shell
```

Usage
==========
```
usage: FwdSh3ll.py [-h] [-pp PIPES_PATH] [-b64]

non-interactive mode options

optional arguments:
  -h, --help                               show this help message and exit
  -pp PIPES_PATH, --pipes-path PIPES_PATH  set remote path of the named pipes to PIPES_PATH (default: "/dev/shm")

interactive mode options

* Target URL:
    Specify the vulnerable URL to attack.
* Proxy URL (optional):
    Specify proxy if needed.
* Payload:
    Choose required payload from the list.
* Mode (single command vs forward shell):
    Choose required action.
```

To successfully spawn the forward shell the following stuff should be reachable on the target host:
  * `/bin/sh`
  * `/usr/bin/mkfifo`
  * `/usr/bin/tail`
  * `/usr/bin/base64`

Payloads
==========
List of RCE vulnerabilities for which payloads are available (will be expanding):
  * `ApacheStruts.py` — Apache Struts 2.3.5 < 2.3.31 / 2.5 < 2.5.10 RCE — [CVE-2017-5638](https://nvd.nist.gov/vuln/detail/CVE-2017-5638 "NVD - CVE-2017-5638") ([exploit-db](https://www.exploit-db.com/exploits/41570 "Apache Struts 2.3.5 < 2.3.31 / 2.5 < 2.5.10 - Remote Code Execution"))
  * `NodejsExpress.py` — Node.js deserialization bug for RCE — [CVE-2017-5941](https://nvd.nist.gov/vuln/detail/CVE-2017-5941 "NVD - CVE-2017-5941") ([exploit-db](https://www.exploit-db.com/docs/english/41289-exploiting-node.js-deserialization-bug-for-remote-code-execution.pdf "Exploiting Node.js deserialization bug for Remote Code Execution (CVE-2017-5941)"))
  * `ShellShock.py` — Bash code injection RCE — [CVE-2014-6271](https://nvd.nist.gov/vuln/detail/CVE-2014-6271 "NVD - CVE-2014-6271")
  * `WebShell.py` — Just a web shell

Known Issues
==========
* If you get the `connection timeout` error when initializing the forward shell, just rerun the script.
* Some Linux distributions does not support the `/dev/shm` path (shared memory, availability depends on kernel config), so if something goes wrong, try changing it to `/tmp` with `-p` switch.
* When setting the named pipes, the `>& file.output` syntax for combinig *stdout* and *stderr* should be supported by both `bash/zsh` and `(t)csh`, but it's not a Bash preferable way though. So there could be issues with the redirection syntax for various shells. Keep that in mind.

Post Scriptum
==========
Special thanks to [0xdf](https://www.hackthebox.eu/profile/4935 "Hack The Box :: 0xdf:: Member Profile") and [IppSec](https://www.youtube.com/channel/UCa6eh7gCkpPo5XXUDfygQQA "IppSec - YouTube") for sharing the forward shell concept.

If this tool has been useful for you, feel free to buy me a coffee :coffee:

[![Coffee](https://user-images.githubusercontent.com/23141800/45254832-8948b300-b387-11e8-9206-23c3e10af5f2.png)](https://buymeacoff.ee/snovvcrash)
