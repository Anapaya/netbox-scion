from django.db import migrations, models


def set_existing_active(apps, schema_editor):
    Assignment = apps.get_model('netbox_scion', 'SCIONLinkAssignment')
    Assignment.objects.filter(status__isnull=True).update(status='ACTIVE')


class Migration(migrations.Migration):

    dependencies = [
        ('netbox_scion', '0015_add_underlay_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='scionlinkassignment',
            name='status',
            field=models.CharField(choices=[('RESERVED', 'Reserved'), ('ACTIVE', 'Active'), ('PLANNED', 'Planned')], default='ACTIVE', help_text='Operational status of this link assignment', max_length=16),
        ),
        migrations.RunPython(set_existing_active, migrations.RunPython.noop),
    ]
