import logging
import os
# import time
import unittest
from config_provider import ConfigProviderJson
# from unittest.mock import patch

# import context


class ConfigProviderJsonTest(unittest.TestCase):
    SIMPLE_JSON = 'test/simple.json'

    def test_defaults(self):
        config = ConfigProviderJson()
        notifiers = config.getNotifiers()
        self.assertEqual(len(notifiers), 1, "No default notifier provided")
        listeners = config.getListeners()
        self.assertEqual(len(listeners), 1, "No default listeners provided")




    # @unittest.skipIf(os.getenv('CI'), "run on CI")
    def test_read_none_file(self):
        config = ConfigProviderJson()
        self.assertRaises(ValueError, config.read, None)
    
    def test_read_non_existing_file(self):
        config = ConfigProviderJson()
        self.assertRaises(FileNotFoundError, config.read, 'does_not_exist.json')


    def test_read_simple(self):
        config = ConfigProviderJson()
        config.read(ConfigProviderJsonTest.SIMPLE_JSON)
        notifiers = config.getNotifiers()
        self.assertEqual(len(notifiers), 1, "No notifier provided")
        listeners = config.getListeners()
        self.assertEqual(len(listeners), 1, "No listeners provided")
        self.assertEqual(listeners[0].__class__.__name__, 'SavapageIdListener')
