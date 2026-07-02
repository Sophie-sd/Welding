from django.db import migrations


def update_blog_post_image(apps, schema_editor):
    BlogPost = apps.get_model('pages', 'BlogPost')
    BlogPost.objects.filter(slug='reading-blueprints-precision').update(
        static_image='blog-blueprints.png',
    )


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0012_update_blog_hero_image'),
    ]

    operations = [
        migrations.RunPython(update_blog_post_image, migrations.RunPython.noop),
    ]
