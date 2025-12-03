from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('netbox_scion', '0013_expand_ticket_field'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scionlinkassignment',
            name='peer_name',
            field=models.CharField(blank=True, help_text='Peer name (optional)', max_length=100),
        ),
        migrations.AlterField(
            model_name='scionlinkassignment',
            name='peer',
            field=models.CharField(blank=True, help_text="Peer identifier (optional) in format '{isd}-{as}#{interface_number}' when provided", max_length=255),
        ),
    ]
