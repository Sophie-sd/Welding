from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from PIL import Image

from pages.models import FAQItem, PortfolioImage, PortfolioItem, Service, SiteSettings
from pages.utils.richtext import has_richtext_content


def _png_bytes(size=(100, 80), color=(40, 120, 200, 255)) -> bytes:
    image = Image.new('RGBA', size, color)
    buffer = BytesIO()
    image.save(buffer, format='PNG')
    return buffer.getvalue()


class RichtextHelperTests(TestCase):
    def test_empty_and_nbsp_are_empty(self):
        self.assertFalse(has_richtext_content(''))
        self.assertFalse(has_richtext_content(None))
        self.assertFalse(has_richtext_content('<p></p>'))
        self.assertFalse(has_richtext_content('<p>&nbsp;</p>'))
        self.assertFalse(has_richtext_content('<p>   </p>'))

    def test_real_content_is_detected(self):
        self.assertTrue(has_richtext_content('<p>Custom service description.</p>'))


class PortfolioDetailTests(TestCase):
    def setUp(self):
        SiteSettings.load()
        self.item = PortfolioItem.objects.create(
            slug='test-bridge',
            category='repairs',
            title='Test Bridge Project',
            location='Poole, UK',
            detail='STRUCTURAL WELDING',
            body='<p>Full project narrative for the bridge reinforcement.</p>',
            static_image='welder.png',
            is_published=True,
            sort_order=1,
        )
        self.unpublished = PortfolioItem.objects.create(
            slug='hidden-project',
            category='industrial',
            title='Hidden Project',
            location='London',
            detail='PRIVATE',
            is_published=False,
            sort_order=2,
        )

    def test_portfolio_detail_renders(self):
        response = self.client.get('/portfolio/test-bridge/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Bridge Project')
        self.assertContains(response, 'Full project narrative')

    def test_unpublished_portfolio_detail_404(self):
        response = self.client.get('/portfolio/hidden-project/')
        self.assertEqual(response.status_code, 404)

    def test_portfolio_list_links_to_detail(self):
        response = self.client.get('/portfolio/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '/portfolio/test-bridge/')
        self.assertNotContains(response, '/portfolio/hidden-project/')

    def test_sitemap_includes_portfolio_slug(self):
        response = self.client.get('/sitemap.xml')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '/portfolio/test-bridge/')
        self.assertNotContains(response, '/portfolio/hidden-project/')

    def test_gallery_images_on_detail(self):
        uploaded = SimpleUploadedFile(
            'gallery-shot.png',
            _png_bytes(),
            content_type='image/png',
        )
        PortfolioImage.objects.create(
            item=self.item,
            image=uploaded,
            alt_text='Gallery detail shot',
            sort_order=1,
        )
        response = self.client.get('/portfolio/test-bridge/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Project Gallery')
        self.assertContains(response, 'Gallery detail shot')


class FaqHtmlTests(TestCase):
    def setUp(self):
        SiteSettings.load()
        FAQItem.objects.all().delete()
        FAQItem.objects.create(
            question='Do you offer coded welding?',
            answer='<p>Yes, our team is AWS certified.</p>',
            sort_order=1,
            is_published=True,
        )

    def test_faq_renders_html_not_escaped_tags(self):
        response = self.client.get('/faq/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<p>Yes, our team is AWS certified.</p>', html=False)
        self.assertNotContains(response, '&lt;p&gt;')
        self.assertContains(response, 'Yes, our team is AWS certified.')


class ServiceBodyTests(TestCase):
    def setUp(self):
        SiteSettings.load()
        self.service = Service.objects.filter(is_published=True).first()
        if self.service is None:
            self.service = Service.objects.create(
                slug='tig-welding',
                code='SVC-01',
                title='TIG Welding',
                short='Precision TIG welding.',
                is_published=True,
            )

    def test_filled_body_appears_on_service_page(self):
        self.service.body = '<p>Custom body content for this service.</p>'
        self.service.save(update_fields=['body'])
        response = self.client.get(f'/services/{self.service.slug}/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Custom body content for this service.')
        self.assertNotContains(response, 'What We Deliver')

    def test_empty_tinymce_body_shows_fallback(self):
        self.service.body = '<p>&nbsp;</p>'
        self.service.save(update_fields=['body'])
        response = self.client.get(f'/services/{self.service.slug}/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'What We Deliver')
        self.assertNotContains(response, '&nbsp;')
