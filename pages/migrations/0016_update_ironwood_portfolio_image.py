from django.db import migrations


def update_ironwood_image(apps, schema_editor):
    PortfolioItem = apps.get_model('pages', 'PortfolioItem')
    PortfolioItem.objects.filter(slug='ironwood-residence').update(
        static_image='portfolio-ironwood.png',
    )


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0015_update_home_showcase_and_featured_blog_images'),
    ]

    operations = [
        migrations.RunPython(update_ironwood_image, migrations.RunPython.noop),
    ]
