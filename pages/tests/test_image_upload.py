from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import SimpleTestCase
from PIL import Image

from pages.cms_field_hints import get_field_hint
from pages.utils.image_upload import ImageUploadError, process_admin_image


class CmsFieldHintsTests(SimpleTestCase):
    def test_hero_title_has_char_limit(self):
        hint = get_field_hint('home', 'hero_title')
        self.assertEqual(hint.char_max, 72)

    def test_hero_image_has_profile(self):
        hint = get_field_hint('home', 'hero_image')
        self.assertEqual(hint.image_profile.name, 'hero')
        self.assertIn('WebP', hint.help_text_uk())


class ImageUploadTests(SimpleTestCase):
    def _png_file(self, size=(2000, 1500), color=(220, 80, 40, 255)) -> SimpleUploadedFile:
        image = Image.new('RGBA', size, color)
        buffer = BytesIO()
        image.save(buffer, format='PNG')
        return SimpleUploadedFile('sample.png', buffer.getvalue(), content_type='image/png')

    def test_converts_png_to_webp(self):
        result = process_admin_image(self._png_file(), profile='content')
        self.assertTrue(result.name.endswith('.webp'))
        image = Image.open(BytesIO(result.read()))
        self.assertEqual(image.format, 'WEBP')

    def test_resizes_large_image(self):
        result = process_admin_image(self._png_file(size=(3200, 2400)), profile='hero')
        image = Image.open(BytesIO(result.read()))
        self.assertLessEqual(image.width, 1600)
        self.assertLessEqual(image.height, 1200)

    def test_rejects_invalid_file(self):
        broken = SimpleUploadedFile('broken.png', b'not-an-image', content_type='image/png')
        with self.assertRaises(ImageUploadError):
            process_admin_image(broken, profile='content')
