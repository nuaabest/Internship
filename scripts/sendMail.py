# *=======================================================*
# -*- coding:utf-8 -*-
# * time : 2020-03-26 14:00
# * author : lichengyi
# *=======================================================*
# send mail

import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import parseaddr, formataddr
from email import encoders
import sys

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr(( \
        Header(name, 'utf-8').encode(), \
        addr.encode('utf-8') if isinstance(addr, unicode) else addr))

smtp_sever = 'smtp.qq.com'
from_addr = '1728951866@qq.com'
password = 'jqcatvluhvhvjaii'
to_addr = '1728951866@qq.com'

msg = MIMEText(sys.argv[1], 'plain', 'utf-8')
#构建一个邮件
msg['From'] = _format_addr(u'lichengyi <%s>' % from_addr)
msg['To'] = _format_addr(u'lichengyi <%s>' % to_addr)
msg['Subject'] = Header(u'上传数据丢失', 'utf-8').encode()

server = smtplib.SMTP(smtp_sever, 25)
server.set_debuglevel(1)
server.login(from_addr, password)
server.sendmail(from_addr, [to_addr], msg.as_string())
server.quit()