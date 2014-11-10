# -*- coding: utf-8 -*-
import six
import unittest

import requests
import api_toolkit

from emites.main import Emites
from .helpers import (
    use_cassette as use_emites_cassette,
    APP_CREDENTIALS, TEST_EMITTER,
)

__all__ = ['EmitesTest', 'EmittersTest']


class EmitesTest(unittest.TestCase):

    def setUp(self):
        with use_emites_cassette('collections_options'):
            self.api_client = Emites(**APP_CREDENTIALS)

    def test_instance_has_emitters_takers_servicevalues_nfse_and_batches(self):
        self.assertTrue(hasattr(self.api_client, 'emitters'))
        self.assertTrue(isinstance(self.api_client.emitters, api_toolkit.Collection))

        self.assertTrue(hasattr(self.api_client, 'takers'))
        self.assertTrue(isinstance(self.api_client.takers, api_toolkit.Collection))

        self.assertTrue(hasattr(self.api_client, 'service_values'))
        self.assertTrue(isinstance(self.api_client.service_values, api_toolkit.Collection))

        self.assertTrue(hasattr(self.api_client, 'nfse'))
        self.assertTrue(isinstance(self.api_client.nfse, api_toolkit.Collection))

        self.assertTrue(hasattr(self.api_client, 'batches'))
        self.assertTrue(isinstance(self.api_client.batches, api_toolkit.Collection))


class EmittersTest(unittest.TestCase):


    def setUp(self):
        self.post_data = TEST_EMITTER.copy()
        with use_emites_cassette('collections_options'):
            self.api_client = Emites(**APP_CREDENTIALS)

    def test_emitters_are_a_collection(self):
        self.assertTrue(isinstance(self.api_client.emitters, api_toolkit.Collection))

    def test_emitters_are_iterable(self):
        with use_emites_cassette('emitters/list'):
            emitters = [item for item in self.api_client.emitters.all()]

    def test_emitters_can_be_created(self):
        with use_emites_cassette('emitters/create'):
            emitter = self.api_client.emitters.create(**self.post_data)

        self.assertEquals(emitter.id, 12)
        self.assertEquals(emitter.email, self.post_data['email'])
        self.assertEquals(emitter.account_id, 56)

    def test_creation_without_email_fails(self):
        del(self.post_data['email'])
        with use_emites_cassette('emitters/create_without_email'):
            self.assertRaises(requests.HTTPError, self.api_client.emitters.create, **self.post_data)

    def test_creation_without_social_reason_fails(self):
        del(self.post_data['social_reason'])
        with use_emites_cassette('emitters/create_without_social_reason'):
            self.assertRaises(requests.HTTPError, self.api_client.emitters.create, **self.post_data)

    def test_creation_without_cnpj_fails(self):
        del(self.post_data['cnpj'])
        with use_emites_cassette('emitters/create_without_cnpj'):
            self.assertRaises(requests.HTTPError, self.api_client.emitters.create, **self.post_data)

    def test_creation_without_fancy_name_fails(self):
        del(self.post_data['fancy_name'])
        with use_emites_cassette('emitters/create_without_fancy_name'):
            self.assertRaises(requests.HTTPError, self.api_client.emitters.create, **self.post_data)

    def test_creation_without_city_inscription_fails(self):
        del(self.post_data['city_inscription'])
        with use_emites_cassette('emitters/create_without_city_inscription'):
            self.assertRaises(requests.HTTPError, self.api_client.emitters.create, **self.post_data)

    def test_creation_without_state_fails(self):
        del(self.post_data['state'])
        with use_emites_cassette('emitters/create_without_state'):
            self.assertRaises(requests.HTTPError, self.api_client.emitters.create, **self.post_data)

    def test_creation_without_city_fails(self):
        del(self.post_data['city'])
        with use_emites_cassette('emitters/create_without_city'):
            self.assertRaises(requests.HTTPError, self.api_client.emitters.create, **self.post_data)

    def test_creation_without_neighborhood_fails(self):
        del(self.post_data['neighborhood'])
        with use_emites_cassette('emitters/create_without_neighborhood'):
            self.assertRaises(requests.HTTPError, self.api_client.emitters.create, **self.post_data)

    def test_creation_without_street_type_does_not_fail(self):
        del(self.post_data['street_type'])
        with use_emites_cassette('emitters/create_without_street_type'):
            emitter = self.api_client.emitters.create(**self.post_data)

        self.assertEquals(emitter.id, 13)
        self.assertEquals(emitter.email, self.post_data['email'])
        self.assertEquals(emitter.account_id, 56)

    def test_creation_without_street_fails(self):
        del(self.post_data['street'])
        with use_emites_cassette('emitters/create_without_street'):
            self.assertRaises(requests.HTTPError, self.api_client.emitters.create, **self.post_data)

    def test_creation_without_number_fails(self):
        del(self.post_data['number'])
        with use_emites_cassette('emitters/create_without_number'):
            self.assertRaises(requests.HTTPError, self.api_client.emitters.create, **self.post_data)

    def test_creation_without_zip_code_fails(self):
        del(self.post_data['zip_code'])
        with use_emites_cassette('emitters/create_without_zip_code'):
            self.assertRaises(requests.HTTPError, self.api_client.emitters.create, **self.post_data)

    def test_creation_without_phone_fails(self):
        del(self.post_data['phone'])
        with use_emites_cassette('emitters/create_without_phone'):
            self.assertRaises(requests.HTTPError, self.api_client.emitters.create, **self.post_data)

    def test_creation_without_certificate_fails(self):
        del(self.post_data['certificate'])
        with use_emites_cassette('emitters/create_without_certificate'):
            self.assertRaises(requests.HTTPError, self.api_client.emitters.create, **self.post_data)

    def test_creation_without_password_fails(self):
        del(self.post_data['password'])
        with use_emites_cassette('emitters/create_without_password'):
            self.assertRaises(requests.HTTPError, self.api_client.emitters.create, **self.post_data)

    def test_get_emitter_from_another_account_fails(self):
        with use_emites_cassette('emitters/get_from_another_account'):
            self.assertRaises(requests.HTTPError, self.api_client.emitters.get, 2)

    def test_get_emitter_from_this_account_works(self):
        with use_emites_cassette('emitters/get_from_this_account'):
            emitter = self.api_client.emitters.get(12)

        self.assertEquals(emitter.email, self.post_data['email'])
        self.assertEquals(emitter.account_id, 56)

    def test_emitters_can_be_updated(self):
        # Using PUT
        with use_emites_cassette('emitters/get_from_this_account'):
            emitter = self.api_client.emitters.get(12)

        emitter.city_inscription = '1111111'
        emitter.resource_data['password'] = self.post_data['password']
        emitter.resource_data['certificate'] = self.post_data['certificate']
        with use_emites_cassette('emitters/update_city_inscription'):
            updated_emitter = emitter.save()

        self.assertEquals(updated_emitter.city_inscription, '1111111')

    def test_emitters_can_be_deleted(self):
        with use_emites_cassette('emitters/get_from_this_account'):
            emitter = self.api_client.emitters.get(12)

        with use_emites_cassette('emitters/delete'):
            emitter.delete()

        with use_emites_cassette('emitters/list_after_deletion'):
            emitters = [item for item in self.api_client.emitters.all()]

        self.assertEquals(emitters, [])
