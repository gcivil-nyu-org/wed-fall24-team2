from django.test import SimpleTestCase
import core.wsgi


class WSGITest(SimpleTestCase):
    def test_wsgi_application_import(self):
        self.assertIsNotNone(core.wsgi.application)
