import logging
import os
import subprocess
# import time
import unittest
from config_provider import ConfigProviderJson
from cog_dbus_ctl_listener import CogDBusCtlListener
import dbus
import dbusmock
# from unittest.mock import patch

# import context


class ConfigProviderJsonTest(dbusmock.DBusTestCase):
    SIMPLE_JSON = 'test/simple.json'
    @classmethod
    def setUpClass(cls):
        cls.start_system_bus()
        cls.dbus_con = cls.get_dbus(system_bus=True)

    def setUp(self):
        self.p_mock = self.spawn_server('com.igalia.Cog', 
                                        '/com/igalia/Cog',
                                        'org.gtk.Actions',
                                        system_bus=True,
                                        stdout=subprocess.PIPE)

        # Get a proxy for the UPower object's Mock interface
        self.dbus_upower_mock = dbus.Interface(self.dbus_con.get_object(
            'com.igalia.Cog', '/com/igalia/Cog'),
            dbusmock.MOCK_IFACE)

        self.dbus_upower_mock.AddMethod('', 'Suspend', '', '', '')

    def tearDown(self):
        self.p_mock.stdout.close()
        self.p_mock.terminate()
        self.p_mock.wait()

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
    
    def test_config_file(self):
        config = ConfigProviderJson()
        config.read("test/delivery.json")
        notifiers = config.getNotifiers()
        listeners = config.getListeners()
