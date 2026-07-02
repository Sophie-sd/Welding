from django.db import migrations


def update_blog_hero_image(apps, schema_editor):
    SiteBlock = apps.get_model('pages', 'SiteBlock')
    SiteBlock.objects.filter(page='blog', key='hero_image').update(
        text_html='images/hero-blog.png',
    )
    SiteBlock.objects.filter(page='blog', key='hero_image_alt').update(
        text_html=(
            'Welding standards and technical blueprints — KHODAK engineering blog'
        ),
    )


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0011_update_about_hero_image'),
    ]

    operations = [
        migrations.RunPython(update_blog_hero_image, migrations.RunPython.noop),
    ]
