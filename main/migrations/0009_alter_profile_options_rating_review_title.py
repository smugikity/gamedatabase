# Generated by Django 4.1.4 on 2023-01-02 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_rename_avatar_profile_image'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={'verbose_name_plural': 'Profiles'},
        ),
        migrations.AddField(
            model_name='rating',
            name='review_title',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]