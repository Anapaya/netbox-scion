from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('netbox_scion', '0010_fix_database_schema'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='comments',
            field=models.TextField(blank=True, help_text='Free-form comments (internal notes)'),
        ),
        migrations.AddField(
            model_name='isdas',
            name='comments',
            field=models.TextField(blank=True, help_text='Free-form comments (internal notes)'),
        ),
        migrations.AddField(
            model_name='scionlinkassignment',
            name='comments',
            field=models.TextField(blank=True, help_text='Free-form comments (internal notes)'),
        ),
    ]
