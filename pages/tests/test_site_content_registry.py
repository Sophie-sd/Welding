from django.test import SimpleTestCase

from pages.site_content_registry import CONTENT_SECTIONS, all_registry_block_keys


class SiteContentRegistryTests(SimpleTestCase):
    def test_block_keys_are_unique(self):
        keys = list(all_registry_block_keys())
        self.assertEqual(len(keys), len(set(keys)))

    def test_admin_model_names_are_unique(self):
        names = [section.admin_model_name for section in CONTENT_SECTIONS]
        self.assertEqual(len(names), len(set(names)))

    def test_sections_with_visibility_key_include_block(self):
        for section in CONTENT_SECTIONS:
            if not section.visibility_key:
                continue
            section_keys = {key for page, key in section.blocks if page == section.page_slug}
            self.assertIn(section.visibility_key, section_keys)
