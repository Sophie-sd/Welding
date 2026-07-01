from django.db import migrations


def update_contact_details(apps, schema_editor):
    SiteSettings = apps.get_model('pages', 'SiteSettings')
    SiteSettings.objects.filter(pk=1).update(
        site_phone='+44 7704 039508',
        site_email='khodakmetalsolution@gmail.com',
        site_address='564 Ashley Rd, Poole BH14 0AG, United Kingdom',
    )


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0002_seed_initial_content'),
    ]

    operations = [
        migrations.RunPython(update_contact_details, migrations.RunPython.noop),
    ]
