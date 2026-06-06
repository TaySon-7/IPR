from django.test import SimpleTestCase


class CoreViewsTests(SimpleTestCase):
    def test_home_page_uses_frontend_template(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Django + PostgreSQL")
        self.assertContains(response, "Лабораторная работа Kubernetes")

    def test_live_endpoint_returns_alive_status(self):
        response = self.client.get("/live/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "alive"})
