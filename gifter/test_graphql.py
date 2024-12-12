from django.test import TestCase
from . import graphql

class TestGraphql(TestCase):

    def test_graphql(self):
        graphql.foo()
