from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('netbox_scion', '0014_make_peer_optional'),
    ]

    operations = [
        migrations.AddField(
            model_name='scionlinkassignment',
            name='local_underlay',
            field=models.CharField(blank=True, help_text='Local underlay endpoint in format ip:port (IPv4 or IPv6)', max_length=300),
        ),
        migrations.AddField(
            model_name='scionlinkassignment',
            name='peer_underlay',
            field=models.CharField(blank=True, help_text='Peer underlay endpoint in format ip:port (IPv4 or IPv6)', max_length=300),
        ),
    ]
