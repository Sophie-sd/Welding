from django.db import migrations


def update_home_and_featured_blog_images(apps, schema_editor):
    SiteBlock = apps.get_model('pages', 'SiteBlock')
    BlogPost = apps.get_model('pages', 'BlogPost')
    SiteBlock.objects.filter(page='home', key='showcase_card_2_image').update(
        text_html='images/home-showcase-tig.png',
    )
    BlogPost.objects.filter(slug='future-heavy-duty-structural-installation').update(
        static_image='blog-featured-structural.png',
    )


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0014_swap_ironwood_safety_images'),
    ]

    operations = [
        migrations.RunPython(update_home_and_featured_blog_images, migrations.RunPython.noop),
    ]
