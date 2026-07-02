from django.contrib.auth import get_user_model
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from pages.models import SiteBlock, SiteSettings


@override_settings(
    STORAGES={
        'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
        'staticfiles': {'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage'},
    },
)
class SiteContentAdminTests(TestCase):
    def setUp(self):
        SiteSettings.load()
        user_model = get_user_model()
        self.user = user_model.objects.create_superuser(
            username='cmsadmin',
            email='cms@example.com',
            password='test-pass-123',
        )
        self.client = Client()
        self.client.force_login(self.user)

    def test_home_hero_form_uses_dark_readable_inputs(self):
        url = reverse('admin:pages_homeherosettings_changelist')
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        content = response.content.decode()
        self.assertIn('id_block__home__hero_title__text_html', content)
        self.assertIn('bg-base-900 text-base-100', content)
        field_start = content.index('id_block__home__hero_title__text_html')
        field_chunk = content[field_start:field_start + 800]
        self.assertIn('bg-base-900', field_chunk)
        self.assertNotIn('bg-white', field_chunk)

    def test_header_visibility_post_updates_block(self):
        change_url = reverse('admin:pages_siteheadersettings_change', args=[1])
        block = SiteBlock.objects.get(page='site', key='header_nav_services_visible')
        block.text_html = '1'
        block.save()

        response = self.client.post(change_url, {
            'block__site__header_nav_services_visible__visible': '',
            'block__site__header_logo_image__static_path': 'images/logo-khodak.png',
            'block__site__header_nav_services_label__text_html': 'Services',
            'block__site__header_nav_portfolio_label__text_html': 'Portfolio',
            'block__site__header_nav_portfolio_visible__visible': 'on',
            'block__site__header_nav_about_label__text_html': 'About',
            'block__site__header_nav_about_visible__visible': 'on',
            'block__site__header_nav_blog_label__text_html': 'Blog',
            'block__site__header_nav_blog_visible__visible': 'on',
            'block__site__header_nav_contact_label__text_html': 'Contact',
            'block__site__header_nav_contact_visible__visible': 'on',
            'block__site__header_cta_text__text_html': 'Request a Quote',
            'block__site__header_cta_visible__visible': 'on',
        })
        self.assertEqual(response.status_code, 302)
        block.refresh_from_db()
        self.assertEqual(block.text_html, '0')
