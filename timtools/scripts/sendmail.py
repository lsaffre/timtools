# -*- coding: utf-8 -*-
# Copyright 2002-2018 Rumma & Ko Ltd
"""\
mandatory options :
  -s, --sender     sender's Name and email
  -h, --host       name of SMTP host
  
optional options :  
  -u, --user        sender's login name
                    (anonymous access if omitted)
  -r, --recipient   recipient's Name and email
                    (taken from addrlist.txt if not given)                   
  -p, --password    sender's login password
                    (asked interactively if not given)
  -d, --debug       turn debug mode on
  -h, --help        display this text

"""

from timtools.setup_info import SETUP_INFO
from timtools.console.application import Application, \
     UsageError, OperationFailed # , ApplicationError

#from timtools.ui.console import ConsoleApplication, \
#     UsageError, ApplicationError
#from timtools import __version__

import smtplib
#import string
import socket
# import sys
import os.path

opj = os.path.join
#import getopt
import getpass
import glob
import email
import email.Utils
import mimetypes
import codecs
# import types

from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email.utils import getaddresses, formataddr, parseaddr

from timtools.i18n import itr, _

itr("Message size: %d bytes.", de=u"Größe: %d Bytes", fr=u"Taille: %d octets")
itr("Send this to %d recipients: %s",
    de=u"Mail schicken an %d Empfänger: %s",
    fr=u"Envoyer ce mail a %d destinataires: %s")
itr("Sent to %d recipients.",
    de=u"Verschickt an %d Empfänger.",
    fr=u"Envoyé ? %d destinataires.")
itr("%d recipients refused.",
    de=u"%d Empfänger verweigert.",
    fr=u"%d destinataires ont été refusés.")


class MyMessage(Message):

    def __init__(self):
        Message.__init__(self)
        """
        If I don't set transfer-encoding myself, set_charset()
        will set it to base64 which apparently is wrong
        """
        self.add_header('Content-Transfer-Encoding', '8bit')
        self.set_charset("utf-8")


##     def __setitem__(self, name, val):
##         if type(val) == types.UnicodeType:
##             try:
##                 val=val.encode('ascii')
##             except UnicodeEncodeError,e:
##                 val=Header(val,self.get_charset(),None,name,"\t")
##         elif type(val) == types.StringType:
##             try:
##                 val.decode("ascii")
##             except UnicodeDecodeError,e:
##                 val=Header(val.decode(sys.getdefaultencoding()),self.get_charset(),
##                            None,name,"\t")
##         return Message.__setitem__(self,name,val)

    def set_payload(self, payload, charset=None):
        payload = payload.encode('utf-8')
        Message.set_payload(self, payload, self.get_charset())


class Sendmail(Application):

    name = "Lino/sendmail"
    copyright = "Copyright 2002-2018 Rumma & Ko Ltd"
    # url = "http://timtools.saffre-rumma.net/sendmail.html"
    url = SETUP_INFO['url']

    usage = "usage: timtools sendmail [options] FILE"

    description = """\
sends an email stored in a FILE to a list of recipients
stored in a separate list file.
FILE is the input file (can be text or html).
"""

    def setupOptionParser(self, parser):
        #self.attach_files = []
        Application.setupOptionParser(self, parser)

        parser.add_option("-s",
                          "--subject",
                          help="the Subjet: line of the mail",
                          action="store",
                          type="string",
                          dest="subject",
                          default=None)

        ##         parser.add_option("-a", "--attach",
        ##                           help="add the specified FILE to the mail as attachment",
        ##                           action="callback",
        ##                           callback=self.attachfile,
        ##                           type="string",
        ##                           default=None)

        parser.add_option("-f",
                          "--from",
                          help="the From: line (sender) of the mail",
                          action="store",
                          type="string",
                          dest="sender",
                          default=None)

        parser.add_option("-t",
                          "--to",
                          help="""
The To: line (recipient) of the mail.
Taken from addrlist.txt if not given.
""",
                          action="store",
                          type="string",
                          dest="recipient",
                          default=None)

        parser.add_option("-r",
                          "--host",
                          help="the SMTP relay host",
                          action="store",
                          type="string",
                          dest="host",
                          default=None)

        parser.add_option("-u",
                          "--user",
                          help="the username for the SMTP host",
                          action="store",
                          type="string",
                          dest="user",
                          default=None)

        parser.add_option("-p",
                          "--password",
                          help="the password for the SMTP host",
                          action="store",
                          type="string",
                          dest="password",
                          default=None)
        parser.add_option("-e",
                          "--encoding",
                          help="the encoding of the .eml input file",
                          action="store",
                          type="string",
                          dest="encoding",
                          default=None)

##     def attachfile(self,option, opt, value, parser):
##         self.attach_files.append(value)

    def encodeaddrs(self, msg, hdr, recipients=None):
        all = msg.get_all(hdr, [])
        del msg[hdr]
        l = []
        for name, addr in getaddresses(all):
            #name=msg.get_charset().header_encode(name)
            name = str(Header(unicode(name), msg.get_charset()))
            if recipients is not None:
                recipients.append((name, addr))
            l.append(formataddr((name, addr)))
        msg[hdr] = Header(", ".join(l))
        return all

    def run(self):

        if len(self.args) == 0:
            raise UsageError("needs 1 argument")

        self.server = None
        self.dataDir = '.'
        self.count_ok = 0
        self.count_nok = 0

        if self.options.host is None:
            raise UsageError("--host must be specified")

##         for fn in  self.attach_files:
##             if not os.path.exists(fn):
##                 raise OperationFailed("File %s does not exist."%fn)

        files = []
        for pattern in self.args:
            files += glob.glob(pattern)

        self.count_todo = len(files)
        if self.count_todo == 0:
            self.notice("Nothing to do: no input files found.")
            return

        if self.options.recipient is None:
            recipients = []
        else:
            recipients = getaddresses([self.options.recipient])

        sender = self.options.sender
        subject = self.options.subject
        """

        if the first input file's name ends with .eml, then this
        becomes the outer message
        

        """
        if files[0].lower().endswith(".eml"):
            self.notice("Reading file %s...", files[0])
            first = email.message_from_file(codecs.open(
                files[0], "r", self.options.encoding),
                                            _class=MyMessage)
            if first.has_key('subject'):
                subject = first["subject"]
                del first["subject"]
                first["subject"] = Header(subject, first.get_charset())

            self.encodeaddrs(first, 'from')
            if sender is None: sender = first["from"]
            self.encodeaddrs(first, 'to', recipients)
            self.encodeaddrs(first, 'cc', recipients)
            self.encodeaddrs(first, 'bcc', recipients)
            del first['bcc']

            del files[0]
            self.count_todo -= 1
        else:
            first = None

        if len(files) == 0:
            outer = first
        else:
            # Create the enclosing (outer) message
            outer = MIMEMultipart()
            # outer.preamble = 'You will not see this in a MIME-aware mail reader.\n'
            if first is not None:
                first.add_header('Content-Disposition', 'inline')
                outer.attach(first)
                for hdr in ('to', 'cc'):
                    outer[hdr] = first[hdr]
            outer['subject'] = subject
            outer['from'] = sender
            self.notice("Attaching %d files...", self.count_todo)
            i = 1
            for filename in files:
                self.notice(u"%s (%d/%d)", filename, i, self.count_todo)
                part = self.file2msg(filename)
                # Set the filename parameter
                part.add_header('Content-Disposition',
                                'attachment',
                                filename=os.path.basename(filename))
                outer.attach(part)
                i += 1

        #for part in outer.walk():
        #if recipient is None: recipient=part["To"]
        #if bcc is None: bcc=part["Bcc"]

        if self.options.subject is not None:
            del outer['subject']
            outer['subject'] = self.options.subject
        #if self.options.sender is not None:
        #    del outer['from']
        #    outer['from'] = self.options.sender
        #del outer['to']
        #outer['to'] = recipient
        #if bcc is not None:
        #    outer['Bcc'] = bcc
        #    print "Bcc:", bcc

        #headers_i18n(outer)

        if len(recipients) == 0:
            for addr in open(opj(self.dataDir, "addrlist.txt")).xreadlines():
                addr = addr.strip()
                if len(addr) != 0 and addr[0] != "#":
                    recipients += getaddresses([addr])

        if not outer.has_key("Subject"):
            raise "Subject header is missing"
        if not outer.has_key("Date"):
            outer["Date"] = email.Utils.formatdate(None, True)

        for k, v in outer.items():
            #~ print k,":",unicode(v)
            self.notice(u"%s:%s", k, v)
        #self.notice(str(outer.keys()))
        self.notice(_("Message size: %d bytes."), len(str(outer)))
        self.notice(_("Send this to %d recipients: %s"), len(recipients),
                    ", ".join([a[1] for a in recipients]))

        sender = parseaddr(unicode(sender))[1]

        # print "sender:", unicode(sender)

        # print outer.as_string(unixfrom=0)

        if not self.confirm("Okay?"):
            return

        self.connect()

        self.sendmsg(outer, sender, recipients)

        self.server.quit()

        self.notice(_("Sent to %d recipients."), self.count_ok)
        if self.count_nok != 0:
            self.notice(_("%d recipients refused."), self.count_nok)

    def file2msg(self, filename):
        if not os.path.exists(filename):
            raise OperationFailed(u"File %s does not exist." % filename)
        self.dataDir = os.path.dirname(filename)
        if len(self.dataDir) == 0:
            self.dataDir = "."

        (root, ext) = os.path.splitext(filename)

        ctype, encoding = mimetypes.guess_type(filename)

        if ctype is None or encoding is not None:
            # No guess could be made, or the file is encoded (compressed), so
            # use a generic bag-of-bits type.
            ctype = 'application/octet-stream'

        maintype, subtype = ctype.split('/', 1)

        if maintype == 'text':
            fp = open(filename)
            # Note: we should handle calculating the charset
            msg = MIMEText(fp.read(), _subtype=subtype)
            fp.close()
        elif maintype == 'image':
            fp = open(filename, 'rb')
            msg = MIMEImage(fp.read(), _subtype=subtype)
            fp.close()
        elif maintype == 'audio':
            fp = open(filename, 'rb')
            msg = MIMEAudio(fp.read(), _subtype=subtype)
            fp.close()
        else:
            fp = open(filename, 'rb')
            msg = MIMEBase(maintype, subtype)
            msg.set_payload(fp.read())
            fp.close()
            # Encode the payload using Base64
            encoders.encode_base64(msg)

        return msg

    def connect(self):

        try:
            self.notice("Connecting to %s", self.options.host)
            self.server = smtplib.SMTP(self.options.host)
        except socket.error, e:
            raise OperationFailed("Could not connect to %s : %s" %
                                  (self.options.host, e))
        except socket.gaierror, e:
            raise OperationFailed("Could not connect to %s : %s" %
                                  (self.options.host, e))

        # server.set_debuglevel(1)

        if self.options.user is None:
            self.notice("Using anonymous SMTP")
            return

        if self.options.password is None:
            self.options.password = getpass.getpass(
                'Password for %s@%s : ' %
                (self.options.user, self.options.host))

        try:
            self.server.login(self.options.user, self.options.password)
            return

        except Exception, e:
            raise OperationFailed(str(e))

##         except smtplib.SMTPHeloError,e:
##             self.ui.error(
##                 "The server didn't reply properly to the 'HELO' greeting: %s", e)
##         except smtplib.SMTPAuthenticationError,e:
##             self.ui.error(
##                 "The server didn't accept the username/password combination: %s",e)
##         except smtplib.SMTPException,e:
##             self.ui.error(str(e))
##         return False

    def sendmsg(self, msg, sender, recipients):
        self.debug("sendmsg(%r,%r,%r)", msg, sender, recipients)

        #print msg.get_all("from")

        # note : simply setting a header does not overwrite an existing
        # header with the same key!

        #del msg["To"]
        #msg["To"] = toAddr

        #if self.options.sender is None:
        #    sender = msg['From'] # .encode('latin1')
        #else:
        #    sender = self.options.sender

        # body = str(msg)
        body = msg.as_string(unixfrom=0)
        # print body
        mail_options = ""  # "8bitmime"
        try:
            refused = self.server.sendmail(sender,
                                           [formataddr(a) for a in recipients],
                                           body, mail_options)
            # self.notice(
            #     u"Sent '%s' at %s to %s",
            #     msg["Subject"], msg["Date"], ", ".join(recipients))
            self.count_ok += len(recipients)
            #self.debug("=" * 80)
            #self.debug(body.decode('utf8'))
            #self.debug("=" * 80)
            if len(refused) > 0:
                for i in refused.items():
                    self.warning(u"refused %s : %s", *i)
                self.count_ok -= len(refused)
                self.count_nok += len(refused)
            return

        except smtplib.SMTPRecipientsRefused, e:
            self.error("%s : %s", recipients, e)
            # All recipients were refused. Nobody got the mail.
        except smtplib.SMTPHeloError, e:
            self.error("%s : %s", recipients, e)
        except smtplib.SMTPServerDisconnected, e:
            self.error("%s : %s", recipients, e)
        except smtplib.SMTPSenderRefused, e:
            self.error("%s : %s", sender, e)
        except smtplib.SMTPDataError, e:
            self.error("%s : %s", recipients, e)

        self.count_nok += len(recipients)
        return


##  def ToUserLog(self,msg):
##      try:
##          f = open("%s/user.log" % self.dataDir,"a")
##          f.write(str(msg)+"\n")
##          print msg
##      except IOError:
##          print "[no logfile] " + msg


def main(*args, **kw):
    Sendmail().main(*args, **kw)


if __name__ == '__main__':
    main()
