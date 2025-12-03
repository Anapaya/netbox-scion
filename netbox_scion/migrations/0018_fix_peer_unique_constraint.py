# Generated migration for netbox_scion

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('netbox_scion', '0017_remove_customer_id'),
    ]

    operations = [
        # First, remove the old unique constraint
        migrations.RemoveConstraint(
            model_name='scionlinkassignment',
            name='unique_peer_per_isdas',
        ),
        # Update the peer field to allow NULL
        migrations.AlterField(
            model_name='scionlinkassignment',
            name='peer',
            field=models.CharField(
                blank=True,
                null=True,
                max_length=255,
                help_text="Peer identifier (optional) in format '{isd}-{as}#{interface_number}' when provided"
            ),
        ),
        # Add the new conditional unique constraint
        # This constraint only applies when peer is not NULL and not empty
        migrations.AddConstraint(
            model_name='scionlinkassignment',
            constraint=models.UniqueConstraint(
                fields=['isd_as', 'peer'],
                name='unique_peer_per_isdas',
                condition=models.Q(peer__isnull=False) & ~models.Q(peer='')
            ),
        ),
    ]
