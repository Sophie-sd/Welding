from django.db import migrations


def update_faq_hero_image(apps, schema_editor):
    SiteBlock = apps.get_model('pages', 'SiteBlock')
    SiteBlock.objects.filter(page='faq', key='hero_image').update(
        text_html='images/hero-faq.png',
    )
    SiteBlock.objects.filter(page='faq', key='hero_image_alt').update(
        text_html=(
            'Welding quality inspection — KHODAK Metal Solution FAQ and support'
        ),
    )


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0008_siteblock_cms'),
    ]

    operations = [
        migrations.RunPython(update_faq_hero_image, migrations.RunPython.noop),
    ]
