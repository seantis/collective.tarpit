import logging
import logging.handlers
import random
import sys

from Products.SiteErrorLog.SiteErrorLog import SiteErrorLog


logger = logging.getLogger("collective.tarpit")
address = "/dev/log"
if sys.platform == "darwin":
    address = "/var/run/syslog"
hdlr = logging.handlers.SysLogHandler(
    address=address,
    facility=logging.handlers.SysLogHandler.LOG_AUTH,
)
logger.addHandler(hdlr)

count_base = random.randint(0, 999999999)


def _do_copy_to_zlog(self, now, strtype, entry_id, url, tb_text):
    self._do_copy_to_zlog_original(now, strtype, entry_id, url, tb_text)

    global count_base

    if strtype == 'Unauthorized':
        count_base += 1

        # get the remote IP, checking sources in light of their
        # likely reliability.
        environ = self.REQUEST.environ
        remote_addr = environ.get('HTTP_X_REAL_IP', None)
        if remote_addr is None:
            remote_addr = environ.get('HTTP_X_FORWARDED_FOR', None)
            if remote_addr is not None:
                remote_addr = remote_addr.split(',')[0].strip()
        if remote_addr is None:
            remote_addr = environ.get('REMOTE_ADDR', 'NO REMOTE ADDR')

        message = 'plone[{0}]: Authentication failure from {1}, {2}'.format(
            count_base,
            remote_addr,
            tb_text.strip().split('\n')[-1]
        )
        logger.warning(message)


def patch_z_log():
    SiteErrorLog._do_copy_to_zlog_original = SiteErrorLog._do_copy_to_zlog
    SiteErrorLog._do_copy_to_zlog = _do_copy_to_zlog
