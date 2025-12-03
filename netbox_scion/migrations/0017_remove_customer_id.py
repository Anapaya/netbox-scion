from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('netbox_scion', '0016_add_status_field'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scionlinkassignment',
            name='customer_id',
        ),
    ]
