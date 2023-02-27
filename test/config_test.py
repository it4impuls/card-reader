import logging
import os
# import time
import unittest
from config_provider import ConfigProviderIni
# from unittest.mock import patch

# import context


class ConfigProviderIniTest(unittest.TestCase):
    SIMPLE_INI = 'test/simple.ini'

    def test_defaults(self):
        config = ConfigProviderIni()
        notifiers = config.getNotifiers()
        self.assertEqual(len(notifiers), 1, "No default notifier provided")
        listeners = config.getListeners()
        self.assertEqual(len(listeners), 1, "No default listeners provided")




    # @unittest.skipIf(os.getenv('CI'), "run on CI")
    def test_read_none_file(self):
        config = ConfigProviderIni()
        self.assertRaises(ValueError, config.read, None)
    
    def test_read_non_existing_file(self):
        config = ConfigProviderIni()
        self.assertRaises(FileNotFoundError, config.read, 'does_not_exist.ini')


    def test_read_simple(self):
        config = ConfigProviderIni()
        config.read(ConfigProviderIniTest.SIMPLE_INI)
        notifiers = config.getNotifiers()
        self.assertEqual(len(notifiers), 1, "No default notifier provided")
        listeners = config.getListeners()
        self.assertEqual(len(listeners), 1, "No default listeners provided")
        self.assertEqual(listeners[0].__class__.__name__, 'SavapageIdListener')
