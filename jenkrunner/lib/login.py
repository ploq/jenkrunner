import json
import os


class LoginInfoFile(object):
    def __init__(self, filename):
        self.filename = os.path.expanduser(filename)
        self.login_cache = None

    def get_login_for_url(self, url):
        if self.login_cache is None:
            with open(self.filename) as fd:
                self.login_cache = json.load(fd)
        if url not in self.login_cache:
            # This is error
            pass
        return self.login_cache[url]["username"], self.login_cache[url]["password"]
