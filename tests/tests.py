from django.test import TestCase


urlpatterns = []


class BasicTests(TestCase):

    def test_setup(self):
        self.assertTrue("It's running!")
