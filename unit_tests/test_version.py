import unittest

import phuey.version

class TestVersion(unittest.TestCase):

    def test_version_should_exist(self):
        self.assertIsNotNone(phuey.version.VERSION)

    def test_version_should_be_semantic(self):
        self.assertRegexpMatches(phuey.version.VERSION, '\d+\.\d+\.\d+')
