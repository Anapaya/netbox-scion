from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('netbox_scion', '0001_initial'),
    ]

    operations = [
        # Add PEER to relationship choices
        migrations.AlterField(
            model_name='scionlink',
            name='relationship',
            field=models.CharField(
                choices=[
                    ('PARENT', 'PARENT'),
                    ('CHILD', 'CHILD'),
                    ('CORE', 'CORE'),
                    ('PEER', 'PEER'),
                ],
                help_text='Relationship type of this SCION link',
                max_length=20,
                verbose_name='Relationship',
            ),
        ),
        # Remove old peer uniqueness constraint
        migrations.RemoveConstraint(
            model_name='scionlink',
            name='unique_peer_per_isdas',
        ),
        # Add updated constraint: only enforce uniqueness when peer contains '#'
        migrations.AddConstraint(
            model_name='scionlink',
            constraint=models.UniqueConstraint(
                condition=models.Q(('peer__contains', '#')),
                fields=['isd_as', 'peer'],
                name='unique_peer_per_isdas',
            ),
        ),
    ]
