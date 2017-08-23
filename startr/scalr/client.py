import logging

from startr.scalr.session import ScalrApiSession

__purpose__ = 'Define Scalr API client for making RESTful API queries.'
__credit__ = 'https://github.com/mchenetz/Scalr-utils for implementation details.'


class ScalrApiClient(object):
    def __init__(self, api_url, key_id, key_secret):
        self.api_url = api_url
        self.key_id = key_id
        self.key_secret = key_secret
        self.logger = logging.getLogger('api[{0}]'.format(self.api_url))  # TODO: Deal with this logging, I don't really want it here.  Or at least use mine.
        self.logger.addHandler(logging.StreamHandler())
        self.session = ScalrApiSession(self)

    def list(self, path, **kwargs):
        data = []
        ident = False
        while path is not None:
            if ident:
                print
            body = self.session.get(path, **kwargs).json()
            data.extend(body['data'])
            path = body['pagination']['next']
            ident = True
        return data

    def get(self, *args, **kwargs):
        return self.session.get(*args, **kwargs).json()['data']

    def delete(self, *args, **kwargs):
        self.session.delete(*args, **kwargs)

    def post(self, *args, **kwargs):
        return self.session.post(*args, **kwargs).json()['data']
