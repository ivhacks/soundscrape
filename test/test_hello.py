from unittest import TestCase

class HelloWorld(TestCase):
    def test_hello_world(self):
        print("hello world")
        self.assertEqual(1, 1)