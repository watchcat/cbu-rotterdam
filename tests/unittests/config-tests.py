"""
Test config managment.

"""
from unittest2 import TestCase
from framework.config import Config


class ConfigTest (TestCase):
    """
    Container for config tests.
    
    """
    
    def test_load(self):
        """
        Test `load` method and that a config has been loaded.
        
        """
        Config.load()
        self.assertIsNotNone(Config.data)
        self.assertIsInstance(Config.data, dict)
    
    def test_get_all(self):
        """
        Test `get_all` method
        
        """
        data = Config.get_all()
        self.assertIsNotNone(data)
        self.assertIsInstance(data, dict)
    
    def test_dev(self):
        """
        Test `dev` method
        
        """
        dev = Config.dev()
        self.assertIsInstance(dev, bool)
    
    def test_manualSetConfig(self):
        """
        Test manually setting a value.
        
        """
        # Assert that value is not there
        self.assertNotIn('testing', Config.data)
        
        # Set new value and assert it is there
        Config.data['testing'] = True
        data = Config.get_all()
        self.assertTrue(data['testing'])