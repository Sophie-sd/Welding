from django.db import migrations


def update_portfolio_images(apps, schema_editor):
    PortfolioItem = apps.get_model('pages', 'PortfolioItem')
    mapping = {
        'omega-metalworks': 'portfolio-omega.png',
        'nexus-tower': 'portfolio-nexus.png',
        'bridge-reinforcement': 'portfolio-bridge.png',
        'ironwood-residence': 'portfolio-residential.png',
    }
    for slug, static_image in mapping.items():
        PortfolioItem.objects.filter(slug=slug).update(static_image=static_image)


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0005_update_site_domain'),
    ]

    operations = [
        migrations.RunPython(update_portfolio_images, migrations.RunPython.noop),
    ]
