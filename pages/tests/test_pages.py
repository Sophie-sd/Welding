from django.test import Client, TestCase

from pages.models import BlogPost, QuoteRequest, Service, SiteSettings


class SiteViewsTests(TestCase):
    def setUp(self):
        SiteSettings.load()

    def test_home_page_renders(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_blog_htmx_pagination(self):
        service_count = Service.objects.count()
        self.assertGreaterEqual(service_count, 1)

        existing = BlogPost.objects.count()
        if existing < 4:
            for index in range(existing + 1, 5):
                BlogPost.objects.create(
                    slug=f'extra-post-{index}',
                    category='technology',
                    title=f'Post {index}',
                    excerpt='Excerpt',
                    published_at=f'2024-0{index}-01',
                    static_image='placeholder.png',
                )

        response = self.client.get('/blog/?page=2', HTTP_HX_REQUEST='true')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'blog-grid')

    def test_quote_submit_saves_request(self):
        service = Service.objects.filter(is_published=True).first()
        self.assertIsNotNone(service)

        response = self.client.post('/quote/submit/', {
            'name': 'John Smith',
            'phone': '+44 7700 900123',
            'email': 'john@example.com',
            'service': service.pk,
            'message': 'Need welding',
            'privacy_accepted': 'on',
            'compact': '1',
            'id_prefix': 'contact',
            'website': '',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(QuoteRequest.objects.filter(name='John Smith').count(), 1)

    def test_quote_submit_htmx_validation_error(self):
        response = self.client.post(
            '/quote/submit/',
            {
                'name': 'J',
                'phone': '123',
                'privacy_accepted': 'on',
                'compact': '1',
                'id_prefix': 'contact',
                'website': '',
            },
            HTTP_HX_REQUEST='true',
        )
        self.assertEqual(response.status_code, 422)
        self.assertContains(response, 'data-quote-form', status_code=422)

    def test_robots_txt(self):
        response = self.client.get('/robots.txt')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sitemap')
