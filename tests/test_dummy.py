from unittest import TestCase


class DummyTest(TestCase):
    def setUp(self):
        pass
        
    def test_dummy(self):
        self.fail("Tests failed! Obviously you're pretty bad at coding.")
    