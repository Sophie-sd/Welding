from django.db import migrations


def update_about_hero_alt(apps, schema_editor):
    SiteBlock = apps.get_model('pages', 'SiteBlock')
    SiteBlock.objects.filter(page='about', key='hero_image_alt').update(
        text_html=(
            'Structural engineer inspecting steel framework — '
            'KHODAK Metal Solution About Us'
        ),
    )


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0010_update_portfolio_hero_image'),
    ]

    operations = [
        migrations.RunPython(update_about_hero_alt, migrations.RunPython.noop),
    ]
