from django.test import SimpleTestCase
import core.asgi


class ASGITest(SimpleTestCase):
    def test_asgi_application_import(self):
        self.assertIsNotNone(core.asgi.application)

    def test_get_application_function(self):
        app = core.asgi.get_application()
        self.assertIsNotNone(app)
