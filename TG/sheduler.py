import asyncio

from TG.config import *
from handlers import Reporting

import gevent
from gevent import socket
from socket import gethostbyname


class Base(object):
    """A simple DNSBL backend."""

    def __init__(self, ip=None, providers=None, timeout=2):
        if providers is None:
            providers = []
        self.ip = ip
        self.providers = providers
        self.timeout = timeout

    def build_query(self, provider):
        reverse = '.'.join(reversed(self.ip.split('.')))
        return '{reverse}.{provider}.'.format(reverse=reverse, provider=provider)

    def query(self, provider):
        try:
            result = socket.gethostbyname(self.build_query(provider))
        except socket.gaierror:
            result = False
        return provider, result

    def check(self):
        results = []
        jobs = [gevent.spawn(self.query, provider) for provider in self.providers]
        gevent.joinall(jobs, self.timeout)
        for job in jobs:
            if job.successful():
                results.append(job.value)
            else:
                results.append((job.args[0], None))
        return results


async def sheduler():
    while 1:
        get_status_url = await Reporting.get_reporting_status_false()
        for i_l in get_status_url:
            domain = i_l.url.split("/")[2]
            otchet = await dnsbl_check(gethostbyname(domain))

        await asyncio.sleep(30)


async def dnsbl_check(ip):
    backend = Base(ip=ip, providers=BASE_PROVIDERS)
    return backend.check()
