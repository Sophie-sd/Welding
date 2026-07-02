from django.db import migrations


def swap_ironwood_and_safety_images(apps, schema_editor):
    PortfolioItem = apps.get_model('pages', 'PortfolioItem')
    BlogPost = apps.get_model('pages', 'BlogPost')
    PortfolioItem.objects.filter(slug='ironwood-residence').update(
        static_image='welder.png',
    )
    BlogPost.objects.filter(slug='aws-safety-standards').update(
        static_image='portfolio-residential.png',
    )


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0013_update_blog_blueprints_image'),
    ]

    operations = [
        migrations.RunPython(swap_ironwood_and_safety_images, migrations.RunPython.noop),
    ]
