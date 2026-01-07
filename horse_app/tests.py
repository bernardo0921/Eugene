from django.test import TestCase, RequestFactory
from horse_app import views


class ErrorPagesTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_handler404_renders_custom_template(self):
        request = self.factory.get('/non-existent/')
        response = views.handler404(request, exception=Exception('Not found'))
        self.assertEqual(response.status_code, 404)
        content = response.content.decode('utf-8')
        self.assertIn('404', content)
        self.assertIn('Page not found', content)

    def test_handler500_renders_custom_template(self):
        request = self.factory.get('/')
        response = views.handler500(request)
        self.assertEqual(response.status_code, 500)
        content = response.content.decode('utf-8')
        self.assertIn('500', content)
        self.assertIn('Server error', content)
