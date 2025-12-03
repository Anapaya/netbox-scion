from django.db import migrations


def forwards(apps, schema_editor):
    # Django's RenameField should handle; this is a safety net if manual SQL needed in some environments.
    pass


def backwards(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('netbox_scion', '0011_add_comments_fields'),
    ]

    operations = [
        migrations.RenameField(
            model_name='scionlinkassignment',
            old_name='zendesk_ticket',
            new_name='ticket',
        ),
    ]
