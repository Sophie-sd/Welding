from django.db import migrations


def update_site_domain(apps, schema_editor):
    SiteSettings = apps.get_model('pages', 'SiteSettings')
    SiteSettings.objects.filter(pk=1).update(
        site_url='https://khodakmetal.com',
    )


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0004_alter_sitesettings_site_address_and_more'),
    ]

    operations = [
        migrations.RunPython(update_site_domain, migrations.RunPython.noop),
    ]
