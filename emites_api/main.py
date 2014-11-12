# -*- coding: utf-8 -*-
from six.moves.urllib.parse import urlsplit
from api_toolkit.entities import Collection, Resource, SessionFactory

__all__ = ['Emites']

str_keys = lambda x: dict((str(k), v) for k, v in x.items())


class EmitesSessionFactory(SessionFactory):
    default_headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Content-Length': '0',
        'Cache-Control': 'no-cache',
        'User-Agent': 'python-emites',
        'Connection': 'keep-alive',
    }

    @classmethod
    def get_auth(cls, **credentials):
        auth = super(EmitesSessionFactory, cls).get_auth(**credentials)
        if auth == ('', ''):
            auth = (credentials.get('token', ''), '')
        return auth

    @classmethod
    def safe_params(cls, **kwargs):
        kwargs.pop('token', None)
        return sorted(kwargs.items(), key=lambda t: t[0])


class EmitesResource(Resource):
    session_factory = EmitesSessionFactory

    def __init__(self, **kwargs):
        super(EmitesResource, self).__init__(**kwargs)
        self.parse_links()

    @property
    def url(self):
        return self.resource_data.get(self.url_attribute_name)

    @url.setter
    def url(self, value):
        self.resource_data[self.url_attribute_name] = value

    def parse_links(self):
        if hasattr(self, '_links'):
            # Find the resource's url
            for item in self._links:
                if item['rel'] == 'self':
                    self.url = item['href']

            self._meta['links'] = self._links

    def prepare_collections(self):
        if hasattr(self, '_links'):
            for item in self._links:
                link_url = item['href']
                if link_url == self.url:
                    continue
                link_name = item['rel']
                link_collection = EmitesCollection(
                    link_url, session=self._session
                )

                setattr(self, link_name, link_collection)

    @classmethod
    def load(cls, url, **kwargs):
        instance = super(EmitesResource, cls).load(url, **kwargs)
        instance.prepare_collections()
        return instance


class EmitesCollection(Collection):
    session_factory = EmitesSessionFactory
    resource_class = EmitesResource

    def get(self, identifier, **kwargs):
        url_template = '{0}/{1}'
        url = url_template.format(self.url, identifier)
        kwargs['session'] = self._session
        return self.resource_class.load(url, **kwargs)

    def all(self, **kwargs):
        load_options = kwargs.pop('load_options', False)

        if 'GET' not in self._meta['allowed_methods']:
            raise ValueError('This collection is not iterable.')

        url = self.url
        params = self.session_factory.safe_params(**kwargs)
        while True:
            response = self._session.get(url, params=params)
            response.raise_for_status()
            content = response.json(object_hook=str_keys)

            for item in content.get('collection', []):
                instance = self.resource_class(**item)
                instance._session = self._session
                instance.prepare_collections()
                if load_options:
                    instance.load_options()
                yield instance

            url = content.get('next', '')
            if not url:
                break


class Emites(EmitesResource):

    def __init__(self, host, token):
        self.host = host
        self.token = token
        super(Emites, self).__init__()
        self.prepare_collections()

    def prepare_collections(self, *args, **kwargs):
        self.emitters = EmitesCollection(
            url='{0}/api/v1/emitters'.format(self.host),
            token=self.token, resource_class=EmitesResource
        )
        self.emitters.load_options()

        self.takers = EmitesCollection(
            url='{0}/api/v1/takers'.format(self.host),
            token=self.token, resource_class=EmitesResource
        )
        self.takers.load_options()

        self.service_values = EmitesCollection(
            url='{0}/api/v1/service-values'.format(self.host),
            token=self.token, resource_class=EmitesResource
        )
        self.service_values.load_options()

        self.nfse = EmitesCollection(
            url='{0}/api/v1/nfse'.format(self.host),
            token=self.token, resource_class=EmitesResource
        )
        self.nfse.load_options()

        self.batches = EmitesCollection(
            url='{0}/api/v1/batches'.format(self.host),
            token=self.token, resource_class=EmitesResource
        )
        self.batches.load_options()
