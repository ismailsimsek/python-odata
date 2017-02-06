# -*- coding: utf-8 -*-

import os
from unittest import TestCase

import responses

from odata import ODataService
from odata.entity import EntityBase

path = os.path.join(os.path.dirname(__file__), 'demo_metadata.xml')
with open(path, mode='rb') as f:
    metadata_xml = f.read()


class TestMetadataImport(TestCase):

    def test_read(self):
        with responses.RequestsMock() as rsps:
            rsps.add(rsps.GET, 'http://demo.local/odata/$metadata/',
                     body=metadata_xml, content_type='text/xml')
            Service = ODataService('http://demo.local/odata/', reflect_entities=True)

        self.assertIn('Product', Service.entities)

        # non-entityset things should not be listed in entities
        expected_keys = {'Product', 'ProductWithNavigation', 'Manufacturer',
                         'ProductManufacturerSales'}
        self.assertEqual(set(Service.entities.keys()), expected_keys)

        Product = Service.entities['Product']
        ProductWithNavigation = Service.entities['ProductWithNavigation']

        assert issubclass(Product, EntityBase)
        assert hasattr(Product, 'DemoCollectionAction')

        test_product = Product()
        assert hasattr(test_product, 'DemoActionWithParameters')
        assert hasattr(ProductWithNavigation, 'Manufacturer')
        self.assertIn('Manufacturer', Service.entities)

        self.assertIn('DemoUnboundAction', Service.actions)
