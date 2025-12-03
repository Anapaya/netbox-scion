from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('netbox_scion', '0012_rename_zendesk_ticket_to_ticket'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scionlinkassignment',
            name='ticket',
            field=models.CharField(
                blank=True,
                max_length=512,
                help_text='External reference (treated as URL if possible; no validation enforced)'
            ),
        ),
    ]
