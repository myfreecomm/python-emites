# -*- coding: utf-8 -*-
import os
from vcr import VCR

__all__ = ['use_cassette', 'APP_CREDENTIALS', 'TEST_EMITTER']

def use_cassette(*args, **kwargs):
    return VCR(
        cassette_library_dir = os.path.join(os.path.dirname(__file__), 'cassettes', 'emites'),
        match_on = ['url', 'method', 'headers', 'body'],
        record_mode = 'new_episodes',
    ).use_cassette(*args, **kwargs)


APP_CREDENTIALS = {
    'host': 'https://sandbox.emites.com.br',
    'token': 'DD00027F4A76E4B79209ACBFBC72F68E',
}

CERTIFICATE = {
    'path': 'certs/test.pfx',
    'password': 'associacao',
}

with open(os.path.join(os.path.dirname(__file__), CERTIFICATE['path'])) as cert_handle:
    TEST_EMITTER = {
        'email': 'financeiro@python-emites.test',
        'cnpj': '91762868000184',
        'fancy_name': 'Empresa de Testes',
        'social_reason': 'Empresa de Testes Ltda ME',
        'state_inscription': 'ISENTO',
        'city_inscription': '00000000',
        'state': 'RJ',
        'city': 'Rio de Janeiro',
        'neighborhood': 'Centro',
        'street_type': 'RUA',
        'street': 'dos testes',
        'number': 42,
        'zip_code': '20011020',
        'phone': '21000000000',
        'certificate': cert_handle.read().encode('base-64'),
        'password': CERTIFICATE['password'],
    }
