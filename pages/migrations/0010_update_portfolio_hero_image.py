from django.db import migrations


def update_portfolio_hero_image(apps, schema_editor):
    SiteBlock = apps.get_model('pages', 'SiteBlock')
    SiteBlock.objects.filter(page='portfolio', key='hero_image').update(
        text_html='images/hero-portfolio.png',
    )
    SiteBlock.objects.filter(page='portfolio', key='hero_image_alt').update(
        text_html=(
            'Fabrication workshop with completed steel structures — KHODAK portfolio'
        ),
    )


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0009_update_faq_hero_image'),
    ]

    operations = [
        migrations.RunPython(update_portfolio_hero_image, migrations.RunPython.noop),
    ]
